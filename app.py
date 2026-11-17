"""Gemini Studio Lab v6: multilingual Streamlit API teaching application."""
from __future__ import annotations
import io
import hashlib
from html import escape
import json
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from google import genai
from api_client import call_gemini, classify, parse_analysis, safe_error, count_prompt_tokens, sanitized_trace, friendly_error, new_client, translate_with_gemini, API_TIMEOUT_SECONDS
from educational_content import EDU, PARAMETERS, CODE_SAMPLES
from interface_localization import UI_V6
from unibs_logo import UNIBS_LOGO_B64

st.set_page_config(page_title="Gemini Studio Lab · API Academy", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

LANGS = {"it":"Italiano 🇮🇹", "en":"English 🇬🇧", "fr":"Français 🇫🇷", "es":"Español 🇪🇸", "de":"Deutsch 🇩🇪", "pt":"Português 🇵🇹", "zh":"中文 🇨🇳", "ja":"日本語 🇯🇵"}
LANG_NAMES = {"it":"Italian", "en":"English", "fr":"French", "es":"Spanish", "de":"German", "pt":"Portuguese", "zh":"Simplified Chinese", "ja":"Japanese"}
COPY = {
"it": {"subtitle":"LABORATORIO UNIVERSITARIO DI INTELLIGENZA ARTIFICIALE", "hero":"Laboratorio di sperimentazione delle API", "desc":"Sperimenta le Gemini API, cambia lingua e parametri, analizza dati e scopri il codice dietro ogni richiesta.", "interface":"Lingua dell'interfaccia", "response":"Lingua della risposta", "key":"Chiave API Google Gemini", "keyhint":"Non viene salvata su disco. Non condividerla.", "model":"Modello Gemini", "refresh":"Aggiorna modelli disponibili", "custom":"Identificativo modello personalizzato", "connect":"Connessione", "params":"Parametri della chiamata API", "chat":"Chat multilingue", "single":"Analisi tecnica", "batch":"Analisi CSV", "guide":"Guida API", "code":"Spiegazione del codice", "send":"Invia alle API", "analyze":"Analizza con Gemini", "ask":"Scrivi la tua domanda in qualsiasi lingua…", "issue":"Descrivi l'anomalia industriale…", "history":"Conversazione", "reset":"Nuova conversazione", "csv":"Carica un file CSV", "csvcol":"Colonna con le descrizioni", "csvmax":"Numero di righe", "csvrun":"Analizza il file tramite API", "csvget":"Scarica Excel", "sample":"Scarica CSV di esempio", "advanced":"Impostazioni avanzate", "advancedhelp":"Attiva un parametro solo se desideri inviarlo all'API. La compatibilità dipende dal modello.", "request":"Richiesta effettiva (chiave esclusa)", "metrics":"Metriche della risposta", "no_key":"Inserisci prima la chiave API nel pannello laterale.", "working":"Chiamata API in corso… (timeout 45 s per richiesta)", "errors":"Errore API", "safety":"Non inserire dati personali, segreti o informazioni aziendali riservate. Una chiave gratuita non garantisce l'assenza di addebiti per un progetto con fatturazione attiva.", "json":"Formato della risposta", "system":"Istruzioni di sistema aggiuntive", "resetparams":"Ripristina parametri", "learn":"Perché questo parametro?", "preview":"Anteprima dei parametri", "result":"Risultato", "help":"Le opzioni non supportate dal modello possono generare un errore: disattivale e riprova.", "back":"Puoi utilizzare questa applicazione sul web; non serve installare nulla sul PC degli studenti.","experiment":"Esperimento token","experiment_intro":"Confronta tre testi equivalenti in lingue diverse. Misura i token con l’API di conteggio, oppure genera le risposte per misurare anche tempi e token effettivamente consumati.","count":"Conta token (solo input)","runcompare":"Genera e confronta (3 chiamate)","tokenchart":"Confronto dei token","prompttokens":"Token del prompt","outputtokens":"Token di risposta","latency":"Tempo (s)","inspector":"Monitor JSON API","reqjson":"Richiesta JSON","resjson":"Risposta JSON","trace":"Traccia della chiamata","tracewarn":"Contiene prompt e risultati: non esportare dati riservati. La chiave API è esclusa."},
"en": {"subtitle":"UNIVERSITY ARTIFICIAL INTELLIGENCE LAB", "hero":"API Experimentation Laboratory", "desc":"Explore Gemini APIs, change languages and parameters, analyze data, and understand the code behind each request.", "interface":"Interface language", "response":"Response language", "key":"Google Gemini API key", "keyhint":"Never saved to disk. Do not share it.", "model":"Gemini model", "refresh":"Refresh available models", "custom":"Custom model ID", "connect":"Connection", "params":"API request parameters", "chat":"Multilingual chat", "single":"Technical analysis", "batch":"CSV analysis", "guide":"API guide", "code":"Code walkthrough", "send":"Send API request", "analyze":"Analyze with Gemini", "ask":"Ask a question in any language…", "issue":"Describe the industrial issue…", "history":"Conversation", "reset":"New conversation", "csv":"Upload a CSV file", "csvcol":"Text column", "csvmax":"Number of rows", "csvrun":"Analyze via API", "csvget":"Download Excel", "sample":"Download sample CSV", "advanced":"Advanced settings", "advancedhelp":"Enable a setting only if you want to send it. Support varies by model.", "request":"Actual request (key excluded)", "metrics":"Response metrics", "no_key":"Enter your API key in the sidebar first.", "working":"Calling the API…", "errors":"API error", "safety":"Do not submit personal, confidential or secret data. Free keys do not guarantee zero charges if billing is enabled.", "json":"Response format", "system":"Extra system instructions", "resetparams":"Reset parameters", "learn":"What does this do?", "preview":"Parameter preview", "result":"Result", "help":"Unsupported model options may cause an error: disable them and retry.", "back":"Runs in a browser; students need no local installations.","experiment":"Token experiment","experiment_intro":"Compare equivalent texts in three languages. Count prompt tokens via the API, or generate replies to compare latency and actual tokens used.","count":"Count tokens (input only)","runcompare":"Generate and compare (3 calls)","tokenchart":"Token comparison","prompttokens":"Prompt tokens","outputtokens":"Output tokens","latency":"Latency (s)","inspector":"API JSON inspector","reqjson":"Request JSON","resjson":"Response JSON","trace":"API call trace","tracewarn":"Includes prompts and outputs: do not export confidential data. API key excluded."},
"fr": {"subtitle":"ATELIER UNIVERSITAIRE D'INTELLIGENCE ARTIFICIELLE", "hero":"Laboratoire d’expérimentation des API", "desc":"Explorez les API Gemini, les langues, les paramètres et le code.", "interface":"Langue de l'interface", "response":"Langue de la réponse", "key":"Clé API Google Gemini", "connect":"Connexion", "params":"Paramètres API", "chat":"Chat multilingue", "single":"Analyse technique", "batch":"Analyse CSV", "guide":"Guide API", "code":"Explication du code", "send":"Envoyer à l'API", "analyze":"Analyser", "ask":"Écrivez votre question…", "issue":"Décrivez l'anomalie…", "working":"Appel API en cours…", "result":"Résultat"},
"es": {"subtitle":"LABORATORIO UNIVERSITARIO DE INTELIGENCIA ARTIFICIAL", "hero":"Laboratorio de experimentación de API", "desc":"Explora Gemini, idiomas, parámetros y código.", "interface":"Idioma de la interfaz", "response":"Idioma de respuesta", "key":"Clave API Google Gemini", "connect":"Conexión", "params":"Parámetros API", "chat":"Chat multilingüe", "single":"Análisis técnico", "batch":"Análisis CSV", "guide":"Guía API", "code":"Explicación del código", "send":"Enviar a API", "analyze":"Analizar", "ask":"Escribe tu pregunta…", "issue":"Describe la anomalía…", "working":"Llamada API…", "result":"Resultado"},
"de": {"subtitle":"UNIVERSITÄRES KI-LABOR", "hero":"Labor zur Erprobung von APIs", "desc":"Erkunde Gemini APIs, Sprachen, Parameter und Code.", "interface":"Oberflächensprache", "response":"Antwortsprache", "key":"Google Gemini API-Schlüssel", "connect":"Verbindung", "params":"API-Parameter", "chat":"Mehrsprachiger Chat", "single":"Technische Analyse", "batch":"CSV-Analyse", "guide":"API-Anleitung", "code":"Code-Erklärung", "send":"API-Anfrage senden", "analyze":"Analysieren", "ask":"Schreibe deine Frage…", "issue":"Beschreibe das Problem…", "working":"API-Aufruf läuft…", "result":"Ergebnis"},
"pt": {"subtitle":"LABORATÓRIO UNIVERSITÁRIO DE IA", "hero":"Laboratório de experimentação de APIs", "desc":"Explore Gemini APIs, idiomas, parâmetros e código.", "interface":"Idioma da interface", "response":"Idioma da resposta", "key":"Chave de API Google Gemini", "connect":"Conexão", "params":"Parâmetros API", "chat":"Chat multilíngue", "single":"Análise técnica", "batch":"Análise CSV", "guide":"Guia de API", "code":"Explicação do código", "send":"Enviar à API", "analyze":"Analisar", "ask":"Digite sua pergunta…", "issue":"Descreva a anomalia…", "working":"Chamada API…", "result":"Resultado"},
}

# Provide complete fallback keys and apply eight-language v6 overrides.
for _language in LANGS:
    COPY[_language] = {**COPY["en"], **COPY.get(_language, {}), **UI_V6[_language]}

def t(key):
    return COPY.get(st.session_state.ui, {}).get(key, COPY["en"].get(key, key))

# Contrast-first design: light neutral canvas, white interactive controls.
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [data-testid="stApp"], [data-testid="stMarkdownContainer"] {font-family:Inter,Arial,sans-serif;color:#243247;}
[data-testid="stAppViewContainer"],.stApp {background:#eef1f5 !important; color:#243247 !important;}
[data-testid="stSidebar"] {background:#e3e9f0 !important;border-right:1px solid #cbd5e1;}
[data-testid="stHeader"] {background:#eef1f5e8 !important;}
.block-container{max-width:1320px;padding-top:2.0rem;padding-bottom:3.0rem;}
h1,h2,h3,h4 {color:#16253b !important;letter-spacing:-.025em;}
p,li,label,[data-testid="stWidgetLabel"] {color:#2e415a !important;}
[data-baseweb="input"]>div,[data-baseweb="select"]>div,[data-baseweb="textarea"]>div,
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"]>div>div {background:#fff !important;color:#192c43 !important;border-color:#b9c7d8 !important;}
[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,[data-baseweb="select"] input {color:#192c43!important;}
[data-testid="stFileUploader"], [data-testid="stChatMessage"], [data-testid="stMetric"],
[data-testid="stExpander"] {background:#fff!important;border:1px solid #d7e0ea!important;border-radius:14px!important;color:#1b2b42!important;}
[data-testid="stTabs"] button {color:#405574!important;font-weight:750;font-size:15px;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#184fba!important;}
[data-baseweb="tab-highlight"] {background:#2563eb!important;}
.stButton>button {border-radius:10px!important;background:#fff!important;color:#1b4b98!important;border:1px solid #aebfd7!important;font-weight:700!important;}
.stButton>button[kind="primary"] {background:#2563eb!important;color:#fff!important;border:none!important;}
.stDownloadButton>button {background:#fff!important;color:#174c97!important;border:1px solid #b1c6e4!important;border-radius:10px!important;}
/* High contrast for Streamlit primary buttons, including form submit and dark/light modes */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"],
button[kind="primary"] {
    background-color:#1d4ed8 !important; color:#ffffff !important;
    border:1px solid #1d4ed8 !important; font-weight:800 !important;
}
.stButton > button[kind="primary"] *,
.stFormSubmitButton > button[kind="primary"] *,
button[data-testid="stBaseButton-primary"] *,
button[kind="primary"] * { color:#ffffff !important; fill:#ffffff !important; }
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover,
button[kind="primary"]:hover {background-color:#1e40af !important; color:#ffffff !important;}
/* v5: force white glyphs and text on PRIMARY Streamlit buttons (including forms). */
button[data-testid="stBaseButton-primary"],
[data-testid="stFormSubmitButton"] button,
.st-key-send_api_chat button {
  background:#2446d8 !important;
  color:#ffffff !important;
  border-color:#2446d8 !important;
  font-weight:800 !important;
  opacity:1 !important;
}
button[data-testid="stBaseButton-primary"] :is(p,span,div,svg),
[data-testid="stFormSubmitButton"] button :is(p,span,div,svg),
.st-key-send_api_chat button :is(p,span,div,svg) {
  color:#ffffff !important;
  fill:currentColor !important;
  -webkit-text-fill-color:#ffffff !important;
}
button[data-testid="stBaseButton-primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover,
.st-key-send_api_chat button:hover {background:#162f9a !important;color:#ffffff !important;}
button:disabled {opacity:.6!important;cursor:not-allowed!important;}
/* Clear input focus and contrast */
input:focus,textarea:focus {outline-color:#2563eb!important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#243247!important;}

/* UNIBS identity: original uploaded university logo on the right, responsive. */
.hero-with-logo{display:flex;align-items:center;justify-content:space-between;gap:28px;min-height:208px;}
.hero-copy{flex:1;min-width:0;}
.hero-brand{flex:0 0 255px;display:flex;align-items:center;justify-content:center;padding:10px;background:#fff;border-radius:12px;}
.hero-brand img{display:block;max-width:100%;height:auto;object-fit:contain;}
@media(max-width:880px){.hero-with-logo{flex-wrap:wrap;}.hero-brand{flex-basis:225px;}.hero h1{font-size:30px!important;}}
.hero {background:#fff;border:1px solid #d4dce9;border-left:6px solid #2563eb;border-radius:19px;padding:25px 30px;margin-bottom:18px;box-shadow:0 8px 24px #34476712;}
.hero h1{color:#162d53!important;margin:8px 0;font-size:36px;font-weight:800;}
.hero p{color:#536781!important;font-size:16px;max-width:870px;}
.eyebrow{color:#0d6b89;font-size:12px;font-weight:800;letter-spacing:1.4px;}
.soft-card{background:#fff;padding:18px 20px;border-radius:14px;border:1px solid #d8e1ec;margin:7px 0 15px;}
.soft-card h4 {margin:0 0 7px;color:#1554a1!important;}
.tag{display:inline-block;background:#dff4ec;color:#16634b;border-radius:30px;padding:6px 12px;font-size:12px;font-weight:750;margin-right:7px;}
[data-testid="stAlert"] {border-radius:12px;}
footer{visibility:hidden;}
</style>""", unsafe_allow_html=True)

DEFAULT = {"temperature":0.7,"top_p":0.95,"top_k":40,"candidate_count":1,
           "max_output_tokens":1024,"presence_penalty":0.0,"frequency_penalty":0.0,
           "seed":1234,"response_logprobs":False,"logprobs":2,
           "stop_sequences":"", "output_format":"Text", "json_schema":"", "thinking_mode":"level",
           "thinking_level":"LOW","thinking_budget":1024,"safety_settings":{},"enable_google_search":False}
for key, value in {"ui":"it","answer":"it","history":[],"last_single":None,"batch":None,"model_options":None,"experiment_translations_cache":None,"experiment_results":None,"last_chat_trace":None,"last_single_trace":None,"last_batch_traces":[],"experiment_traces":{}}.items():
    if key not in st.session_state:
        st.session_state[key]=value

with st.sidebar:
    st.markdown("## ✦ GEMINI STUDIO LAB")
    st.caption("API ACADEMY  /  UNIVERSITY EDITION  6.0")
    st.selectbox("🌐 " + t("interface"), list(LANGS), format_func=lambda v:LANGS[v], key="ui")
    st.divider()
    st.markdown("### 🔑 " + t("connect"))
    api_key=st.text_input(t("key"),type="password",help=t("keyhint"),key="api_key")
    st.link_button("↗ Google AI Studio", "https://aistudio.google.com/api-keys",use_container_width=True)
    if api_key: st.success("API key ready / Chiave inserita")
    else: st.info(t("no_key"))
    st.divider()
    st.selectbox("🌍 " + t("response"),list(LANGS), format_func=lambda v:LANGS[v], key="answer")
    if st.button("↻ " + t("refresh"), disabled=not bool(api_key),use_container_width=True):
        try:
            client=new_client(api_key)
            st.session_state.model_options=sorted({(m.name or "").removeprefix("models/") for m in client.models.list() if "gemini" in (m.name or "").lower() and "embed" not in (m.name or "").lower()})
            client.close()
        except Exception as exc: st.error(friendly_error(exc))
    models=st.session_state.model_options or ["gemini-3-flash-preview"]
    default_idx=models.index("gemini-3-flash-preview") if "gemini-3-flash-preview" in models else 0
    picked=st.selectbox(t("model"),models,index=default_idx,key="selected_gemini_model")
    custom=st.text_input(t("custom"),placeholder="es. gemini-3-flash-preview")
    model=custom.strip() or picked
    st.caption("⚠ "+t("model_notice"))
    st.divider()
    st.caption("🔒 "+t("safety"))

st.markdown(
    "<div class='hero hero-with-logo'>"
    f"<div class='hero-copy'><span class='eyebrow'>✦ {escape(t('subtitle'))}</span>"
    f"<h1>{escape(t('hero'))}</h1><p>{escape(t('desc'))}</p></div>"
    f"<div class='hero-brand'><img src='data:image/png;base64,{UNIBS_LOGO_B64}' "
    "alt='Logo ufficiale Università di Brescia'></div></div>",
    unsafe_allow_html=True,
)
st.markdown(f"<span class='tag'>● REAL GEMINI API</span><span class='tag'>🌍 {LANGS[st.session_state.answer]}</span><span class='tag'>◈ {escape(model)}</span>",unsafe_allow_html=True)
st.write("")

# All shared request settings are controlled here, not inside the individual tasks.
with st.expander("⚙️ " + t("params"), expanded=False):
    st.caption(t("advancedhelp"))
    base1,base2=st.columns([1,1])
    with base1:
        output_format=st.selectbox(t("json"),["Text","JSON"],help="JSON forces application/json where supported.")
        system_extra=st.text_area(t("system"),value="",height=86,placeholder="Example: Answer in 3 short paragraphs.")
    with base2:
        enable_schema=st.checkbox("JSON schema",disabled=output_format!="JSON",help="Only used if JSON output is selected.")
        json_schema=st.text_area("JSON Schema",value='{"type":"object","properties":{"answer":{"type":"string"}},"required":["answer"]}',height=86,disabled=not enable_schema)
    st.markdown("#### Sampling & length / Campionamento e lunghezza")
    st.caption("Important: Gemini 3.x may ignore or reject several sampling parameters. Leave unchecked unless your model supports them.")
    fields=[("temperature","Temperature",0.0,2.0,0.1,"Randomness; high values can vary the wording."),
            ("top_p","Top P",0.0,1.0,0.01,"Probability mass used when sampling tokens."),
            ("top_k","Top K",1,100,1,"Limit on candidate next tokens (model-dependent)."),
            ("candidate_count","Candidates",1,4,1,"Number of alternative outputs, if supported."),
            ("max_output_tokens","Max output tokens",32,8192,32,"Upper bound on length of generated response."),
            ("presence_penalty","Presence penalty",-2.0,2.0,0.1,"Discourages repeating topics already seen."),
            ("frequency_penalty","Frequency penalty",-2.0,2.0,0.1,"Discourages repeating the same words."),
            ("seed","Seed",0,999999,1,"Best-effort repeatability; not guaranteed."),
            ("logprobs","Top log probabilities",1,5,1,"How many alternative-token probabilities to return.")]
    options=dict(DEFAULT)
    options.update({"output_format": "JSON" if output_format=="JSON" else "Text", "enable_schema":enable_schema,"json_schema":json_schema})
    for i in range(0,len(fields),3):
        cols=st.columns(3)
        for col, f in zip(cols,fields[i:i+3]):
            name,label,low,high,step,helptext=f
            with col:
                enabled=st.checkbox("Send " + label,key="enable_"+name,help=helptext)
                value=st.number_input(label,min_value=low,max_value=high,value=DEFAULT[name],step=step,disabled=not enabled,key="val_"+name)
                options["enable_"+name]=enabled
                options[name]=value
    c1,c2,c3=st.columns(3)
    with c1:
        options["enable_stops"]=st.checkbox("Send stop sequences",help="Up to 5 stop strings")
        options["stop_sequences"]=st.text_area("Stop sequences (one per line)",height=75,disabled=not options["enable_stops"])
    with c2:
        options["enable_thinking"]=st.checkbox("Send thinking config",help="Compatible models only")
        options["thinking_mode"]=st.radio("Thinking control",["level","budget"],horizontal=True,disabled=not options["enable_thinking"])
        if options["thinking_mode"]=="level":
            options["thinking_level"]=st.selectbox("Thinking level",["MINIMAL","LOW","MEDIUM","HIGH"],index=1,disabled=not options["enable_thinking"])
        else:
            options["thinking_budget"]=st.number_input("Thinking budget",min_value=0,max_value=32768,value=1024,step=256,disabled=not options["enable_thinking"])
    with c3:
        options["enable_response_logprobs"]=st.checkbox("Return log probabilities")
        options["response_logprobs"]=True
        options["enable_google_search"]=st.checkbox("Google Search tool",help="Ground responses via Google Search if the model supports the tool; check pricing.")
    with st.expander("🛡 Safety settings (advanced)"):
        st.caption("Blocking thresholds apply only to supported safety categories; the API may reject unsupported settings.")
        options["enable_safety"]=st.checkbox("Override default safety thresholds")
        thresholds=["BLOCK_NONE","BLOCK_ONLY_HIGH","BLOCK_MEDIUM_AND_ABOVE","BLOCK_LOW_AND_ABOVE"]
        safety={}
        for cat in ["HARM_CATEGORY_HARASSMENT","HARM_CATEGORY_HATE_SPEECH","HARM_CATEGORY_SEXUALLY_EXPLICIT","HARM_CATEGORY_DANGEROUS_CONTENT"]:
            safety[cat]=st.selectbox(cat,thresholds,index=2,disabled=not options["enable_safety"])
        options["safety_settings"]=safety
    with st.expander("🔎 " + t("preview")):
        from api_client import make_config
        try:
            view=make_config(options,system_extra or "Assistant")
            st.json(view.model_dump(exclude_none=True,mode="json"))
        except Exception as exc:
            st.warning(safe_error(exc))
    st.info(t("help"))

def show_api_trace(trace: dict | None, label: str = "", download_key: str = "trace"):
    """Show redacted request / response structures for teaching purposes."""
    if not trace:
        return
    safe = sanitized_trace(trace, api_key)
    with st.expander("🔍 " + t("inspector") + (" · " + label if label else ""), expanded=False):
        st.caption(t("tracewarn"))
        st.info("These are the SDK content/config and parsed response objects; not the raw HTTPS request or headers. / Dati dell'SDK, non pacchetti HTTP catturati.")
        lcol, rcol = st.columns(2)
        with lcol:
            st.markdown("**↑ " + t("reqjson") + "**")
            st.json(safe.get("request") or {})
        with rcol:
            st.markdown("**↓ " + t("resjson") + "**")
            if safe.get("response") is not None:
                st.json(safe["response"])
            else:
                st.warning(safe.get("error", "No response received / Nessuna risposta ricevuta"))
        st.download_button("↓ Export JSON trace (redacted)",
                           json.dumps(safe, ensure_ascii=False, indent=2),
                           file_name="gemini_api_trace.json",mime="application/json",key=download_key)

def show_metrics(metrics, key_prefix="usage"):
    """Visible dashboard of actual usage returned by Gemini (not rough estimates)."""
    a,b,c,d=st.columns(4)
    def pretty(value): return str(value) if value is not None else "n/d"
    a.metric("↑ Input tokens", pretty(metrics.get("input_tokens")))
    b.metric("↓ Output tokens", pretty(metrics.get("output_tokens")))
    c.metric("Σ Total tokens", pretty(metrics.get("total_tokens")))
    d.metric("⏱ Seconds", pretty(metrics.get("seconds")))
    thinking=metrics.get("thinking_tokens")
    if thinking is not None and thinking>0:
        st.caption(f"Thinking tokens (included in API total, not in visible output count): {thinking}")
    st.caption("Usage values come from Gemini usage_metadata. Total may include reasoning, caching or other tokens; it need not equal input + visible output.")

def ask(prompt,mode="chat",history=None,trace=None):
    lang=LANG_NAMES[st.session_state.answer]
    if mode=="analysis":
        instruction=classify(prompt,lang)
        # A classifier must keep its stable contract; arbitrary JSON schemas could conflict.
        local=dict(options, output_format="JSON",enable_schema=False,json_schema="")
        # Search grounding is not necessary for classification, and may conflict with JSON.
        local["enable_google_search"]=False
    else:
        instruction=f"You are a university AI laboratory assistant. Answer in {lang}, even if the input is another language. Explain uncertainty."
        local=options
    if system_extra.strip(): instruction += "\nExtra user-selected instructions: "+system_extra
    return call_gemini(api_key,model,prompt,instruction,local,history,trace=trace)

st.caption(f"⏱ Timeout delle richieste: {API_TIMEOUT_SECONDS} s · Tentativi automatici: disattivati · Se la richiesta fallisce, controlla modello e quota prima di riprovare.")

chat_tab,one_tab,batch_tab,experiment_tab,guide_tab,code_tab=st.tabs([
    "💬 "+t("chat"),"🛠 "+t("single"),"📊 "+t("batch"),"🧪 "+t("experiment"),"📘 "+t("guide"),"🧩 "+t("code")])

with chat_tab:
    st.markdown("### "+t("chat"))
    st.caption("The same prompt can be submitted in different output languages; sampling settings are set above.")
    if st.button("↻ "+t("reset")):
        st.session_state.history=[]
        st.session_state.last_chat_trace=None
        st.session_state.last_metrics=None
        st.rerun()
    for turn in st.session_state.history:
        with st.chat_message("user" if turn["role"]=="user" else "assistant"):
            st.markdown(turn["text"])
    with st.form("chat",clear_on_submit=False):
        prompt=st.text_area(t("ask"),height=110)
        go=st.form_submit_button("↗ "+t("send"),type="primary",use_container_width=True, key="send_api_chat")
    if go:
        if not api_key: st.warning(t("no_key"))
        elif not prompt.strip(): st.warning("Please write a prompt.")
        else:
            with st.spinner(t("working")):
                try:
                    trace={}
                    answer,alternatives,metrics=ask(prompt,history=st.session_state.history,trace=trace)
                    st.session_state.last_chat_trace=trace
                    st.session_state.history.extend([{"role":"user","text":prompt},{"role":"model","text":answer}])
                    st.session_state.last_metrics=metrics
                    st.session_state.last_alternatives=alternatives
                    st.rerun()
                except Exception as exc:
                    st.session_state.last_chat_trace=trace
                    st.error(t("errors")+": "+friendly_error(exc))
    if st.session_state.get("last_metrics"):
        st.markdown("#### 📈 " + t("metrics"))
        show_metrics(st.session_state.last_metrics, "chat")
        with st.expander("◈ Full API metrics / Dettaglio"):
            st.json(st.session_state.last_metrics)
            if len(st.session_state.get("last_alternatives",[]))>1:
                for i,txt in enumerate(st.session_state.last_alternatives):
                    st.text_area(f"Candidate {i+1}",txt,height=130,key=f"candidate{i}")
    show_api_trace(st.session_state.get("last_chat_trace"), download_key="trace_chat")
    if st.session_state.history:
        st.download_button("↓ Export chat JSON",json.dumps(st.session_state.history,ensure_ascii=False,indent=2),"chat.json","application/json")

with one_tab:
    st.markdown("### "+t("single"))
    st.caption("Anomaly classification produces a fixed JSON contract. The app overrides response format and any custom JSON schema in this tab.")
    issue=st.text_area(t("issue"),height=145,placeholder="Il motore elettrico si surriscalda durante il funzionamento…")
    if st.button("↗ "+t("analyze"),type="primary",use_container_width=True):
        if not api_key: st.warning(t("no_key"))
        elif not issue.strip(): st.warning("Provide an issue.")
        else:
            with st.spinner(t("working")):
                try:
                    trace={}
                    output,_,metrics=ask(issue,"analysis",trace=trace)
                    st.session_state.last_single_trace=trace
                    st.session_state.last_single={"result":parse_analysis(output),"metrics":metrics}
                except Exception as exc:
                    st.session_state.last_single_trace=trace if "trace" in locals() else None
                    st.error(t("errors")+": "+friendly_error(exc))
    if st.session_state.last_single:
        value=st.session_state.last_single["result"]
        c1,c2=st.columns(2)
        c1.metric("Category / Categoria",value["category"])
        c2.metric("Priority / Priorità",value["priority"])
        st.markdown("**Explanation / Spiegazione**")
        st.write(value["explanation"])
        st.markdown("**Checks / Controlli**")
        for x in value["checks"]: st.write("• "+str(x))
        st.json(value)
        show_metrics(st.session_state.last_single["metrics"],"anomaly")
        show_api_trace(st.session_state.get("last_single_trace"),download_key="trace_analysis")
        st.download_button("↓ JSON",json.dumps(value,ensure_ascii=False,indent=2),"analisi.json","application/json")

with batch_tab:
    st.markdown("### "+t("batch"))
    sample="id,segnalazione\n1,Il motore si surriscalda\n2,Il cilindro idraulico avanza a scatti\n3,Il sensore non rileva il pezzo\n"
    st.download_button("↓ "+t("sample"),sample.encode("utf-8-sig"),"segnalazioni.csv","text/csv")
    uploaded=st.file_uploader(t("csv"),type="csv")
    if uploaded:
        try:
            content=uploaded.getvalue()
            try: df=pd.read_csv(io.BytesIO(content),sep=None,engine="python",encoding="utf-8-sig")
            except UnicodeDecodeError: df=pd.read_csv(io.BytesIO(content),sep=None,engine="python",encoding="latin-1")
            if df.empty: st.warning("Empty CSV")
            else:
                st.dataframe(df.head(20),hide_index=True,use_container_width=True)
                col=st.selectbox(t("csvcol"),df.columns,index=min(1,len(df.columns)-1))
                nr=st.slider(t("csvmax"),1,min(len(df),20),min(len(df),5))
                if st.button("↗ "+t("csvrun"),type="primary",use_container_width=True):
                    if not api_key: st.warning(t("no_key"))
                    else:
                        rows=[]; traces=[]; bar=st.progress(0)
                        for i,(_,row) in enumerate(df.head(nr).iterrows()):
                            r=row.to_dict()
                            trace={}
                            try:
                                txt,_,metrics=ask(str(row[col]),"analysis",trace=trace)
                                val=parse_analysis(txt)
                                r.update({"AI_category":val["category"],"AI_priority":val["priority"],
                                          "AI_explanation":val["explanation"],"AI_checks":"; ".join(map(str,val["checks"])),
                                          "API_seconds":metrics["seconds"],"API_input_tokens":metrics.get("input_tokens"),"API_output_tokens":metrics.get("output_tokens"),"API_total_tokens":metrics.get("total_tokens"),"API_error":""})
                            except Exception as exc:
                                r["API_error"]=safe_error(exc)
                            traces.append({"row":i+1,"trace":trace})
                            rows.append(r);bar.progress((i+1)/nr)
                        st.session_state.batch=pd.DataFrame(rows)
                        st.session_state.last_batch_traces=traces
        except Exception as exc:st.error(friendly_error(exc))
    if st.session_state.batch is not None:
        st.dataframe(st.session_state.batch,use_container_width=True,hide_index=True)
        out=io.BytesIO()
        with pd.ExcelWriter(out,engine="openpyxl") as writer:
            st.session_state.batch.to_excel(writer,index=False,sheet_name="Gemini")
        batch_traces=st.session_state.get("last_batch_traces",[])
        if batch_traces:
            st.markdown("#### 🔍 "+t("inspector"))
            selected_trace=st.selectbox("CSV row / Riga", list(range(len(batch_traces))),
                                        format_func=lambda k:f"Row {batch_traces[k]['row']}",key="selected_batch_trace")
            show_api_trace(batch_traces[selected_trace]["trace"],download_key="trace_csv")
        st.download_button("↓ "+t("csvget"),out.getvalue(),"analisi_api.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with experiment_tab:
    st.markdown("## 🧪 " + t("experiment"))
    st.write(t("experiment_intro"))
    st.info(t("comparison_calls") + " " + t("translation_cost"))

    a,b,c=st.columns(3)
    with a:
        master=st.selectbox(t("master_lang"),list(LANGS),format_func=lambda k:LANGS[k],key="experiment_master_lang")
    with b:
        target_candidates=[k for k in LANGS if k!=master]
        first_index=target_candidates.index("en") if "en" in target_candidates else 0
        target1=st.selectbox(t("target_one"),target_candidates,format_func=lambda k:LANGS[k],index=first_index,key="experiment_target1")
    with c:
        last_candidates=[k for k in LANGS if k not in (master,target1)]
        second_index=last_candidates.index("de") if "de" in last_candidates else 0
        target2=st.selectbox(t("target_two"),last_candidates,format_func=lambda k:LANGS[k],index=second_index,key="experiment_target2")

    examples={
        "it":"Spiega in due frasi come funziona un sensore di temperatura industriale.",
        "en":"Explain in two sentences how an industrial temperature sensor works.",
        "de":"Erkläre in zwei Sätzen, wie ein industrieller Temperatursensor funktioniert.",
        "fr":"Explique en deux phrases le fonctionnement d'un capteur de température industriel.",
        "es":"Explica en dos frases cómo funciona un sensor de temperatura industrial.",
        "pt":"Explica em duas frases como funciona um sensor de temperatura industrial.",
        "zh":"用两句话解释工业温度传感器的工作原理。",
        "ja":"産業用温度センサーの仕組みを二文で説明してください。",
    }
    # The user edits only the master text. A language switch loads an example
    # in the selected language without silently translating student content.
    if st.session_state.get("experiment_last_master") != master:
        st.session_state.experiment_master_text=examples[master]
        st.session_state.experiment_last_master=master
    source_text=st.text_area(t("source_text"),height=125,key="experiment_master_text",max_chars=3000)
    alt_model=st.text_input(t("other_model"),placeholder=model,key="experiment_model")
    selected_model=alt_model.strip() or model

    signature=hashlib.sha256(json.dumps([source_text,master,target1,target2,selected_model],ensure_ascii=False).encode('utf-8')).hexdigest()
    cache=st.session_state.get("experiment_translations_cache")
    valid_cache=bool(cache and cache.get("signature")==signature and all(cache.get("texts",{}).get(v) for v in (target1,target2)))
    if valid_cache:
        st.success(t("translation_ready"))
    else:
        st.caption(t("translation_needed"))

    left,mid,right=st.columns(3)
    do_translate=left.button("🌐 "+t("translate"),use_container_width=True)
    count_clicked=mid.button("🔢 "+t("count"),use_container_width=True)
    generate_clicked=right.button("⚡ "+t("runcompare"),type="primary",use_container_width=True)
    proceed=False
    if do_translate or count_clicked or generate_clicked:
        if not api_key:
            st.warning(t("no_key"))
        elif not source_text.strip():
            st.warning(t("invalid_source"))
        elif len({master,target1,target2})!=3:
            st.warning(t("distinct_langs"))
        else:
            if not valid_cache:
                try:
                    translations={}
                    translation_metrics={}
                    for target in (target1,target2):
                        with st.spinner(t("translate_progress")+" "+LANGS[target]):
                            translated, usage=translate_with_gemini(
                                api_key, selected_model, source_text,
                                LANG_NAMES[master], LANG_NAMES[target])
                            translations[target]=translated
                            translation_metrics[target]=usage
                    cache={"signature":signature,"texts":translations,"metrics":translation_metrics}
                    st.session_state.experiment_translations_cache=cache
                    valid_cache=True
                except Exception as exc:
                    st.error(t("errors")+": "+friendly_error(exc))
            proceed=(count_clicked or generate_clicked) and valid_cache

    if valid_cache:
        texts={master:source_text,target1:cache["texts"][target1],target2:cache["texts"][target2]}
        preview_cols=st.columns(3)
        for col, code in zip(preview_cols,[master,target1,target2]):
            with col:
                st.markdown("**"+LANGS[code]+"**")
                st.text_area(t("source_tag") if code==master else t("translated_from"),
                             value=texts[code],height=135,disabled=True,key="preview_"+code+"_"+signature[:12])
        st.caption(t("translations_note"))
        used=list(cache.get("metrics",{}).values())
        if used:
            total_tokens=sum(int(m.get("total_tokens") or 0) for m in used)
            total_seconds=sum(float(m.get("seconds") or 0) for m in used)
            st.caption(f"🌐 {t('translation_usage')}: 2 API calls · {total_tokens} tokens · {total_seconds:.2f} s")
        if proceed:
            records=[]; traces={}
            for code in [master,target1,target2]:
                rec={"Lingua":LANGS[code],"Modello":selected_model,"Input_tokens":None,
                     "Output_tokens":None,"Totale_tokens":None,"Secondi":None,"Errore":""}
                trace={}
                with st.spinner(LANGS[code]+": API…"):
                    try:
                        if generate_clicked:
                            instruction=f"Reply in {LANG_NAMES[code]}. Answer concisely."
                            local=dict(options,output_format="Text",enable_schema=False,json_schema="",
                                       enable_google_search=False,enable_safety=False)
                            result,_,metrics=call_gemini(api_key,selected_model,texts[code],
                                instruction,local,history=[],trace=trace)
                            rec.update(Input_tokens=metrics.get("input_tokens"),Output_tokens=metrics.get("output_tokens"),
                                       Totale_tokens=metrics.get("total_tokens"),Secondi=metrics.get("seconds"),Risposta=result)
                        else:
                            count=count_prompt_tokens(api_key,selected_model,texts[code])
                            rec["Input_tokens"]=count
                            trace={"request":{"method":"models.count_tokens","model":selected_model,
                                              "contents":texts[code]},
                                   "response":{"total_tokens":count},
                                   "note":"SDK token counting representation; API key not included."}
                    except Exception as exc:
                        rec["Errore"]=friendly_error(exc)
                        trace["error"]=friendly_error(exc)
                    traces[LANGS[code]]=trace
                    records.append(rec)
            st.session_state.experiment_traces=traces
            st.session_state.experiment_results=pd.DataFrame(records)
            st.session_state.experiment_kind="generate" if generate_clicked else "count"
            st.session_state.experiment_result_signature=signature

    if (st.session_state.get("experiment_results") is not None and
        st.session_state.get("experiment_result_signature")==signature):
        table=st.session_state.experiment_results
        st.markdown("### 📊 " + t("tokenchart"))
        st.dataframe(table,use_container_width=True,hide_index=True)
        if table["Input_tokens"].notna().any():
            st.bar_chart(table.set_index("Lingua")[["Input_tokens"]])
        if st.session_state.get("experiment_kind")=="generate":
            cols=[v for v in ("Input_tokens","Output_tokens") if table[v].notna().any()]
            if cols: st.bar_chart(table.set_index("Lingua")[cols])
            for _,item in table.iterrows():
                if isinstance(item.get("Risposta"),str):
                    with st.expander("🌍 "+str(item["Lingua"])+" — "+str(item["Secondi"])+" s"):
                        st.write(item["Risposta"])
        traces=st.session_state.get("experiment_traces",{})
        if traces:
            chosen=st.selectbox("🔍 "+t("inspector"),list(traces),key="experiment_trace_lang_v6")
            show_api_trace(traces[chosen],download_key="trace_experiment")
        st.download_button("↓ CSV",table.to_csv(index=False).encode("utf-8-sig"),
                           "confronto_token.csv","text/csv")
        st.caption(t("compare_prompt_only") if st.session_state.get("experiment_kind")=="count"
                   else t("translations_note"))

with guide_tab:
    localized=EDU[st.session_state.ui]
    headings=localized["titles"]
    paragraphs=localized["body"]
    st.markdown("## 📘 "+t("guide"))
    st.markdown("### 1 · "+headings[0])
    st.markdown(paragraphs[0])
    st.code("USER → Streamlit → Python SDK → HTTPS → Gemini API\nUSER ← Streamlit ← Parsed JSON ← HTTPS response",language="text")
    st.markdown("### 2 · "+headings[1])
    st.markdown(paragraphs[1])
    st.markdown("### 3 · "+headings[2])
    st.write(paragraphs[2])
    st.dataframe(pd.DataFrame({t("guide_parameter"):PARAMETERS,
                               t("guide_meaning"):localized["params"]}),
                 hide_index=True,use_container_width=True)
    st.markdown("### 4 · "+headings[3])
    st.info(paragraphs[3])
    st.markdown("### 5 · "+headings[4])
    st.code('''import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain what an API is in Italian",
    config=types.GenerateContentConfig(max_output_tokens=300),
)
print(response.text)''',language="python")
    st.markdown("### 6 · "+headings[5])
    st.markdown(paragraphs[4])
    st.markdown("### 7 · "+headings[6])
    st.markdown(paragraphs[5])
    st.code('''count = client.models.count_tokens(model=model, contents=prompt)
print(count.total_tokens)
print(response.usage_metadata.prompt_token_count)''',language="python")
    st.markdown("### 8 · "+headings[7])
    st.markdown(paragraphs[6])
    st.markdown("### 9 · "+headings[8])
    st.markdown(paragraphs[7])
    st.link_button("Gemini API · docs", "https://ai.google.dev/api/generate-content")
    st.link_button("Python SDK · docs", "https://googleapis.github.io/python-genai/")
    st.link_button("Token counting · docs", "https://ai.google.dev/gemini-api/docs/tokens")

with code_tab:
    localized=EDU[st.session_state.ui]
    st.markdown("## 🧩 "+t("code"))
    st.markdown(localized["body"][8])
    st.caption(t("code_fragments"))
    for index,(name,description,snippet) in enumerate(zip(localized["code_names"],
                       localized["code_desc"], CODE_SAMPLES)):
        with st.expander(name,expanded=index==0):
            st.write(description)
            st.code(snippet,language="python")
    st.markdown("### "+localized["titles"][10])
    for name in ("app.py","api_client.py","educational_content.py","interface_localization.py"):
        path=Path(__file__).parent/name
        with st.expander(name):
            st.download_button("↓ "+name,path.read_text(encoding="utf-8"),
                               file_name=name,mime="text/x-python",key="download_"+name)
            st.code(path.read_text(encoding="utf-8")[:14000],language="python")

st.divider()
st.caption(f"Gemini Studio Lab · API Academy v6 · {datetime.now().year} · Google Gemini Developer API · Research & teaching demo")
