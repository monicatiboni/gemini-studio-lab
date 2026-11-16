"""Isolated Gemini API integration for Gemini Studio Lab.

Calls are real requests to Google's Gemini Developer API. No mock mode.
SDK reference: https://googleapis.github.io/python-genai/
"""
import json
import re
import time
import socket
from typing import Any

from google import genai
from google.genai import types

REDACT = re.compile(r"AIza[0-9A-Za-z_-]{15,}")
API_TIMEOUT_SECONDS = 45


def new_client(api_key: str) -> genai.Client:
    """Per-request deadline, no automatic retries (important for classroom quotas)."""
    return genai.Client(
        api_key=api_key.strip(),
        http_options=types.HttpOptions(
            timeout=API_TIMEOUT_SECONDS * 1000,  # SDK expects milliseconds
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )


def friendly_error(exc: Exception) -> str:
    """Student-facing diagnostics. Never include raw responses or credentials."""
    code = getattr(exc, 'code', None)
    status = str(getattr(exc, 'status', '')).upper()
    raw = str(exc).lower()
    if code == 404 or '404' in status or 'not_found' in status or ('model' in raw and ('not found' in raw or 'no longer available' in raw)):
        return 'Modello non disponibile (404). Premi «Aggiorna modelli disponibili» nella barra laterale e seleziona un altro modello.'
    if code == 429 or 'resource_exhausted' in status or '429' in raw or 'quota exceeded' in raw:
        return 'Quota API raggiunta (429). Controlla i limiti del tuo progetto Google AI Studio e riprova più tardi; non inviare richieste ripetute.'
    if code in (401, 403) or any(x in raw for x in ('api key not valid', 'invalid api key', 'permission_denied')):
        return 'Accesso non autorizzato (401/403). Controlla la chiave API e i permessi del progetto Google.'
    if code == 400 or 'invalid_argument' in status:
        return 'Richiesta non valida (400). Controlla le opzioni avanzate: alcuni parametri non sono compatibili con il modello selezionato.'
    if isinstance(exc, (TimeoutError, socket.timeout)) or any(x in raw for x in ('timed out', 'timeout', 'deadline exceeded', 'readtimeout')):
        return f'Tempo massimo raggiunto ({API_TIMEOUT_SECONDS} s per richiesta). Seleziona un modello disponibile, riduci le opzioni e riprova solo una volta.'
    if code in (500, 502, 503, 504) or any(x in raw for x in ('service unavailable', 'server error', 'connection error', 'connecterror')):
        return 'Servizio Gemini momentaneamente non raggiungibile. Verifica la connessione e riprova più tardi.'
    return 'La chiamata API non è riuscita. Controlla il modello e i parametri; per dettagli tecnici consulta i log di Streamlit (senza divulgare credenziali).'



def safe_error(exc: Exception) -> str:
    """Avoid exposing a key accidentally included in remote error messages."""
    text = REDACT.sub("[API KEY REDACTED]", str(exc))
    return text[:500]


def make_config(options: dict[str, Any], system_instruction: str) -> types.GenerateContentConfig:
    """Only send explicitly enabled optional parameters.

    A model can reject unsupported settings; don't silently remove them.
    """
    cfg: dict[str, Any] = {"system_instruction": system_instruction}
    mapping = {
        "temperature": "temperature", "top_p": "top_p", "top_k": "top_k",
        "candidate_count": "candidate_count", "max_output_tokens": "max_output_tokens",
        "presence_penalty": "presence_penalty", "frequency_penalty": "frequency_penalty",
        "seed": "seed", "response_logprobs": "response_logprobs",
        "logprobs": "logprobs",
    }
    for k, target in mapping.items():
        if options.get("enable_" + k, False):
            cfg[target] = options[k]
    stops = [s.strip() for s in options.get("stop_sequences", "").splitlines() if s.strip()]
    if options.get("enable_stops") and stops:
        cfg["stop_sequences"] = stops[:5]
    if options.get("output_format") == "JSON":
        cfg["response_mime_type"] = "application/json"
        schema_text = options.get("json_schema", "").strip()
        if options.get("enable_schema") and schema_text:
            cfg["response_json_schema"] = json.loads(schema_text)
    if options.get("enable_thinking"):
        if options.get("thinking_mode") == "budget":
            cfg["thinking_config"] = types.ThinkingConfig(thinking_budget=int(options["thinking_budget"]))
        else:
            cfg["thinking_config"] = types.ThinkingConfig(thinking_level=options["thinking_level"])
    safety = options.get("safety_settings", {})
    if options.get("enable_safety") and safety:
        cfg["safety_settings"] = [
            types.SafetySetting(category=k, threshold=v) for k, v in safety.items()
        ]
    if options.get("enable_google_search"):
        cfg["tools"] = [types.Tool(google_search=types.GoogleSearch())]
    return types.GenerateContentConfig(**cfg)


def call_gemini(api_key: str, model: str, prompt: str, system_instruction: str, options: dict[str, Any], history: list[dict] | None = None, trace: dict | None = None):
    """Send a request; return text, timing, token usage, and raw model metadata."""
    if not api_key.strip():
        raise ValueError("API key missing / Chiave API mancante")
    client = new_client(api_key)
    contents = []
    for turn in (history or [])[-12:]:
        contents.append(types.Content(role=turn["role"], parts=[types.Part.from_text(text=turn["text"])]))
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
    config = make_config(options, system_instruction)
    if trace is not None:
        # This is the SDK request representation, not a captured HTTPS packet.
        # API key is passed only to genai.Client, never to this payload.
        trace.clear()
        trace["request"] = {
            "method": "models.generate_content",
            "model": model,
            "contents": [c.model_dump(mode="json", exclude_none=True) for c in contents],
            "config": config.model_dump(mode="json", exclude_none=True),
        }
        trace["response"] = None
        trace["note"] = "Rappresentazione SDK della chiamata, non dump HTTP. La chiave API e le intestazioni di autenticazione sono escluse."
    start = time.perf_counter()
    try:
        res = client.models.generate_content(model=model, contents=contents, config=config)
        if trace is not None:
            trace["response"] = res.model_dump(mode="json", exclude_none=True, exclude_unset=True)
        elapsed = round(time.perf_counter() - start, 3)
        texts = []
        for cand in res.candidates or []:
            parts = getattr(getattr(cand, "content", None), "parts", []) or []
            content = "".join(getattr(p, "text", "") or "" for p in parts)
            if content:
                texts.append(content)
        main = texts[0] if texts else (res.text or "")
        if not main:
            raise RuntimeError("No text in response / Nessun testo nella risposta (verificare filtri e limiti)")
        usage = getattr(res, "usage_metadata", None)
        metrics = {"seconds": elapsed, "input_tokens": getattr(usage, "prompt_token_count", None),
                   "output_tokens": getattr(usage, "candidates_token_count", None),
                   "total_tokens": getattr(usage, "total_token_count", None),
                   "thinking_tokens": getattr(usage, "thoughts_token_count", None),
                   "cached_tokens": getattr(usage, "cached_content_token_count", None),
                   "candidates_returned": len(res.candidates or [])}
        if trace is not None:
            trace["usage"] = metrics.copy()
        return main, texts, metrics
    except Exception as exc:
        if trace is not None:
            trace["error"] = friendly_error(exc)
            trace["elapsed_seconds"] = round(time.perf_counter() - start, 3)
        raise
    finally:
        client.close()


def classify(prompt: str, language_name: str) -> str:
    return (f"Reply exclusively in {language_name}. Analyze an industrial incident. "
            "Return ONLY a JSON object with category (string), priority (low/medium/high), "
            "explanation (string), checks (array of short strings). "
            "Priority codes remain English. Don't assume certainty or bypass safety procedures.")


def parse_analysis(raw: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.I)
    obj = json.loads(cleaned)
    keys = {"category", "priority", "explanation", "checks"}
    if not isinstance(obj, dict) or not keys.issubset(obj) or not isinstance(obj["checks"], list):
        raise ValueError("Unexpected analysis JSON / Struttura JSON non conforme")
    return obj


def count_prompt_tokens(api_key: str, model: str, prompt: str) -> int:
    """Use Gemini's real token-counting endpoint (prompt only, no conversation history)."""
    if not api_key.strip():
        raise ValueError("API key missing / Chiave API mancante")
    client = new_client(api_key)
    try:
        result = client.models.count_tokens(model=model, contents=prompt)
        if result.total_tokens is None:
            raise RuntimeError("Token count missing from API response")
        return int(result.total_tokens)
    finally:
        client.close()


SENSITIVE_KEYS = {"api_key", "apikey", "x-goog-api-key", "authorization", "access_token", "secret", "password"}

def sanitized_trace(trace: dict, api_key: str = "") -> dict:
    """Strip common credentials from trace payloads without modifying the original."""
    def scrub(value):
        if isinstance(value, dict):
            return {str(k): ("[REDACTED]" if str(k).lower() in SENSITIVE_KEYS else scrub(v))
                    for k, v in value.items()}
        if isinstance(value, list):
            return [scrub(v) for v in value]
        if isinstance(value, str):
            value = REDACT.sub("[API KEY REDACTED]", value)
            if api_key.strip():
                value = value.replace(api_key.strip(), "[API KEY REDACTED]")
            return value
        return value
    return scrub(trace)
