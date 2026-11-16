"""Isolated Gemini API integration for Gemini Studio Lab.

Calls are real requests to Google's Gemini Developer API. No mock mode.
SDK reference: https://googleapis.github.io/python-genai/
"""
import json
import re
import time
from typing import Any

from google import genai
from google.genai import types

REDACT = re.compile(r"AIza[0-9A-Za-z_-]{15,}")


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


def call_gemini(api_key: str, model: str, prompt: str, system_instruction: str, options: dict[str, Any], history: list[dict] | None = None):
    """Send a request; return text, timing, token usage, and raw model metadata."""
    if not api_key.strip():
        raise ValueError("API key missing / Chiave API mancante")
    client = genai.Client(api_key=api_key.strip())
    contents = []
    for turn in (history or [])[-12:]:
        contents.append(types.Content(role=turn["role"], parts=[types.Part.from_text(text=turn["text"])]))
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
    start = time.perf_counter()
    try:
        res = client.models.generate_content(model=model, contents=contents,
                                             config=make_config(options, system_instruction))
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
        return main, texts, metrics
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
    client = genai.Client(api_key=api_key.strip())
    try:
        result = client.models.count_tokens(model=model, contents=prompt)
        if result.total_tokens is None:
            raise RuntimeError("Token count missing from API response")
        return int(result.total_tokens)
    finally:
        client.close()
