"""Curated, offline translations for the two educational sections.

All eight languages are statically available: no Gemini calls and no cost when
opening the guide or source-code walkthrough.  Python identifiers remain Python.
"""
from __future__ import annotations

PARAMETERS = [
    'model', 'contents', 'system_instruction', 'temperature', 'top_p',
    'top_k', 'candidate_count', 'max_output_tokens', 'presence_penalty',
    'frequency_penalty', 'seed', 'stop_sequences', 'response_mime_type',
    'thinking_config', 'safety_settings', 'tools (google_search)',
]

CODE_SAMPLES = [
'''import streamlit as st
from google import genai
from api_client import call_gemini
st.set_page_config(page_title="Gemini Studio Lab", layout="wide")''',
'''if "history" not in st.session_state:
    st.session_state.history = []''',
'''api_key = st.text_input("API key", type="password")
model = st.selectbox("Model", ["gemini-3-flash-preview"])
response_language = "Italian"''',
'''cfg = {"system_instruction": "Reply in Italian"}
if options.get("enable_max_output_tokens"):
    cfg["max_output_tokens"] = options["max_output_tokens"]
config = types.GenerateContentConfig(**cfg)''',
'''client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model=model, contents=prompt, config=config)
answer = response.text''',
'''st.write(answer)
st.caption(f"Time: {elapsed:.2f}s")''',
'''result = json.loads(raw_response)
category = result["category"]
priority = result["priority"]''',
'''df = pd.read_csv(file)
for _, row in df.iterrows():
    answer = call_gemini(...)  # illustration only
# Export rows and AI output to Excel''',
'''try:
    answer = call_gemini(...)
except Exception as exc:
    st.error(friendly_error(exc))''',
'''count = client.models.count_tokens(model=model, contents=prompt)
print(count.total_tokens)
usage = response.usage_metadata
print(usage.prompt_token_count, usage.candidates_token_count)''',
'''trace = {}
answer, alternatives, metrics = call_gemini(
    api_key, model, prompt, instruction, options, trace=trace
)
show_api_trace(trace)''',
'''source_language = "Italian"
target_language = "Japanese"
translated = translate_with_gemini(api_key, model, text,
                                   source_language, target_language)''',
]

EDU = {
'it': dict(
 titles=['Che cosa sono le API', 'Come si svolge una richiesta', 'Parametri di una chiamata', 'Timeout, quote ed errori', 'Esempio Python con SDK', 'Esperimento pratico', 'Token e loro conteggio', 'Monitor JSON delle API', 'Funzioni non incluse', 'Organizzazione del codice', 'Codice sorgente completo'],
 body=[
 'Un’API (Application Programming Interface) definisce le regole con cui un programma comunica con un servizio remoto. L’applicazione invia una richiesta HTTPS autenticata; il provider restituisce una risposta strutturata, spesso in JSON.',
 '1. L’utente scrive il prompt e sceglie i parametri. 2. L’SDK autentica la richiesta con la chiave API. 3. Il client invia i dati in HTTPS. 4. Gemini elabora il contenuto. 5. L’app interpreta la risposta e mostra risultato, tempi e token.',
 'I parametri opzionali vengono inviati solo quando attivati. Disponibilità e valori ammessi dipendono dal modello: un’impostazione non supportata può generare un errore.',
 'Le richieste hanno un timeout di 45 secondi e non vengono ritentate automaticamente. 404: modello non disponibile; 429: quota esaurita; 400: richiesta o parametri non validi. Un timeout non garantisce che il provider non abbia conteggiato la chiamata.',
 'Invia lo stesso prompt due volte modificando un solo parametro compatibile alla volta. Confronta testo, lunghezza, tempi, JSON e token. Nell’esperimento multilingue usa un testo master e due traduzioni create dall’app.',
 'I token non hanno lunghezza fissa. count_tokens misura i token del testo prima della generazione; usage_metadata riporta quelli effettivi dopo la risposta, talvolta includendo token di ragionamento. Le chiamate di traduzione consumano token aggiuntivi, visualizzati separatamente.',
 'Il monitor mostra la rappresentazione SDK di richiesta e risposta, non una cattura dei pacchetti HTTPS. Chiavi e intestazioni di autenticazione sono escluse; prompt e risposte restano visibili e non devono contenere dati riservati.',
 'Questo laboratorio riguarda soprattutto la generazione di testo. Le API Gemini includono anche input multimodali, audio, video, immagini, caching e gestione file, che richiedono operazioni e parametri specifici.',
 'Il file app.py gestisce interfaccia, sessione e controlli. api_client.py gestisce il client, la chiamata Gemini, i token e gli errori. educational_content.py contiene le traduzioni didattiche disponibili senza chiamate API.',
 ],
 params=['Identificativo del modello LLM.', 'Testo, parti e turni della conversazione.', 'Istruzioni globali sul comportamento del modello.', 'Regola la variabilità della generazione, se supportato.', 'Limita la probabilità cumulata dei token candidati.', 'Considera un numero massimo di token candidati.', 'Numero di risposte alternative richieste.', 'Limite dei token generati, inclusi eventuali token interni.', 'Penalizza la ricomparsa di elementi già presenti.', 'Penalizza le ripetizioni frequenti di token.', 'Seme per una ripetibilità indicativa, non garantita.', 'Sequenze che interrompono la generazione.', 'Formato della risposta, ad esempio JSON.', 'Configura il ragionamento interno, se supportato.', 'Soglie dei filtri di sicurezza disponibili.', 'Attiva la ricerca web, quando supportata.'],
 code_names=['01 · Preparazione', '02 · Stato della sessione', '03 · Input e chiave API', '04 · Configurazione', '05 · Chiamata HTTPS', '06 · Risposta e metriche', '07 · JSON strutturato', '08 · Elaborazione CSV', '09 · Gestione degli errori', '10 · Conteggio dei token', '11 · Monitor JSON', '12 · Traduzione automatica'],
 code_desc=['Le importazioni caricano Streamlit e l’SDK Gemini; set_page_config prepara la pagina.', 'Streamlit riesegue lo script dopo le interazioni: session_state conserva chat, lingue e risultati.', 'I widget raccolgono chiave, modello e lingua. La chiave non compare in chiaro nel campo password.', 'La configurazione include solo i parametri esplicitamente abilitati.', 'L’SDK prepara e invia la richiesta HTTPS al modello e restituisce un oggetto risposta.', 'Il testo viene visualizzato; durata e token provengono dalla chiamata effettiva.', 'L’analisi delle anomalie richiede campi JSON stabili che il codice può elaborare.', 'Ogni riga del CSV viene analizzata separatamente e i risultati esportati in Excel.', 'Gli errori sono catturati e spiegati senza mostrare credenziali.', 'L’endpoint di conteggio misura l’input; la risposta effettiva restituisce le metriche.', 'L’app salva una rappresentazione della richiesta e della risposta SDK, con credenziali oscurate.', 'L’esperimento token parte da una lingua master e genera due traduzioni mediante chiamate aggiuntive a Gemini.'],
 ),
'en': dict(
 titles=['What is an API?', 'The request lifecycle', 'Request parameters', 'Timeouts, quotas and errors', 'Python SDK example', 'Practical experiment', 'Tokens and token counting', 'API JSON inspector', 'What is not included', 'Code organization', 'Complete source code'],
 body=['An API (Application Programming Interface) specifies how software communicates with a remote provider. The app sends an authenticated HTTPS request; the provider returns structured data, commonly JSON.',
 '1. Enter a prompt and settings. 2. The SDK adds API-key authentication. 3. The client sends an HTTPS request. 4. Gemini processes the content. 5. The app displays the answer, latency and token usage.',
 'Optional parameters are sent only when enabled. Availability and valid ranges depend on the model; unsupported settings may produce errors.',
 'Requests have a 45-second HTTP timeout and no automatic retries. 404: unavailable model; 429: quota exceeded; 400: unsupported parameter or malformed request. A timeout does not guarantee the provider did not process or bill the call.',
 'Repeat one prompt while changing only one supported parameter. Compare output, length, latency, JSON validity and token usage. The multilingual experiment translates one master prompt into two languages.',
 'Tokens are not fixed-size pieces of text. count_tokens measures the prompt before generation; usage_metadata reports actual usage afterwards, possibly including thinking tokens. Translation API calls have separate token usage.',
 'The inspector shows the SDK request and parsed response, not captured HTTPS packets. Credentials are excluded, but prompts and outputs are visible: use only non-confidential data.',
 'The lab focuses on text generation. Gemini APIs also cover multimodal inputs, audio, images, video, caching and files, which require dedicated operations and parameters.',
 'app.py handles layout, sessions and controls. api_client.py handles Gemini requests, token counting and errors. educational_content.py provides offline translations for the teaching material.'],
 params=['LLM model identifier.', 'Prompt parts and conversation turns.', 'Global instructions that steer the model.', 'Controls sampling variability if supported.', 'Cumulative probability mass for token sampling.', 'Maximum number of candidate next tokens.', 'Number of alternative responses requested.', 'Upper bound for generated tokens including possible internal tokens.', 'Discourages returning to previously used elements.', 'Discourages frequent token repetition.', 'Best-effort seed for repeatability; no guarantee.', 'Strings that stop generation.', 'Response format, for example JSON.', 'Controls model reasoning, where supported.', 'Available safety-filter thresholds.', 'Enables web search where supported.'],
 code_names=['01 · Setup', '02 · Session state', '03 · Inputs and API key', '04 · Configuration', '05 · HTTPS call', '06 · Response and metrics', '07 · Structured JSON', '08 · CSV processing', '09 · Error handling', '10 · Token count', '11 · JSON inspector', '12 · Automatic translation'],
 code_desc=['Imports load Streamlit and the Gemini SDK; set_page_config initializes the page.', 'Streamlit reruns after interactions; session_state preserves chat, language and results.', 'Widgets collect the key, model and language. A password field masks the API key.', 'Only explicitly enabled parameters are added to the configuration.', 'The SDK prepares and sends the HTTPS request and returns a response object.', 'Text is displayed; timing and token metrics come from the actual call.', 'Anomaly classification requests predictable fields so the app can parse JSON.', 'Each CSV row is analyzed separately before exporting results to Excel.', 'Errors are caught and explained without revealing credentials.', 'The counting endpoint measures input; response metadata reports actual usage.', 'The app records the SDK request and response representation with redacted credentials.', 'The token experiment starts with a master-language prompt and generates two translations using additional Gemini calls.'],
 ),
'fr': dict(
 titles=['Qu’est-ce qu’une API ?', 'Déroulement d’une requête', 'Paramètres de la requête', 'Délais, quotas et erreurs', 'Exemple Python avec SDK', 'Expérience pratique', 'Jetons et comptage', 'Inspecteur JSON de l’API', 'Fonctions non incluses', 'Organisation du code', 'Code source complet'],
 body=['Une API (interface de programmation) définit les règles de communication avec un fournisseur distant. L’application envoie une requête HTTPS authentifiée et reçoit une réponse structurée, souvent en JSON.',
 '1. Saisir le texte et les paramètres. 2. Le SDK utilise la clé API. 3. Le client envoie une requête HTTPS. 4. Gemini traite le contenu. 5. L’application affiche la réponse, le temps et les jetons.',
 'Les paramètres optionnels ne sont envoyés que s’ils sont activés. Leur prise en charge dépend du modèle.',
 'Délai HTTP de 45 secondes, sans nouvel essai automatique. 404 : modèle indisponible ; 429 : quota dépassé ; 400 : paramètre incorrect. Un délai dépassé n’exclut pas une facturation.',
 'Modifier un seul paramètre compatible à la fois et comparer le résultat, la durée et les jetons. L’expérience multilingue traduit automatiquement un texte maître.',
 'Un jeton n’a pas de longueur fixe. count_tokens compte les jetons du texte ; usage_metadata mesure l’utilisation réelle. Les traductions entraînent des appels et des jetons supplémentaires.',
 'L’inspecteur montre les données du SDK, pas le trafic HTTPS brut. Les clés sont masquées, mais les textes restent visibles : évitez les informations confidentielles.',
 'Ce laboratoire traite principalement la génération de texte. Les autres fonctions Gemini (images, audio, vidéo, fichiers) nécessitent des API spécifiques.',
 'app.py gère l’interface et les sessions ; api_client.py les requêtes Gemini ; educational_content.py les traductions pédagogiques sans appels API.'],
 params=['Identifiant du modèle LLM.', 'Texte et tours de conversation.', 'Consignes générales au modèle.', 'Variabilité de génération, si prise en charge.', 'Probabilité cumulée lors du choix des jetons.', 'Nombre de jetons candidats.', 'Nombre de réponses alternatives.', 'Limite de jetons générés, y compris internes.', 'Limite la réapparition d’éléments déjà employés.', 'Réduit la répétition fréquente des jetons.', 'Graine de reproductibilité approximative.', 'Chaînes qui arrêtent la génération.', 'Format de réponse, par exemple JSON.', 'Réglages de raisonnement si disponibles.', 'Seuils des filtres de sécurité.', 'Recherche Web si disponible.'],
 code_names=['01 · Préparation', '02 · État de session', '03 · Saisie et clé API', '04 · Configuration', '05 · Appel HTTPS', '06 · Réponse et mesures', '07 · JSON structuré', '08 · Traitement CSV', '09 · Gestion des erreurs', '10 · Comptage des jetons', '11 · Inspecteur JSON', '12 · Traduction automatique'],
 code_desc=['Les imports chargent Streamlit et le SDK ; set_page_config prépare la page.', 'session_state conserve les données malgré la réexécution du script.', 'Les widgets reçoivent la clé, le modèle et la langue ; la clé est masquée.', 'Seuls les paramètres activés sont envoyés.', 'Le SDK réalise la requête HTTPS et retourne la réponse.', 'L’application affiche le texte, la durée et les jetons.', 'Le classificateur renvoie des champs JSON attendus.', 'Le programme analyse les lignes CSV et exporte les résultats.', 'Les erreurs sont expliquées sans divulguer la clé.', 'Les jetons d’entrée et la consommation réelle sont mesurés séparément.', 'La trace expose les objets SDK en masquant les identifiants.', 'Le texte maître est traduit automatiquement dans deux langues avec Gemini.'],
 ),
'es': dict(
 titles=['¿Qué es una API?', 'Ciclo de una solicitud', 'Parámetros de solicitud', 'Tiempo límite, cuotas y errores', 'Ejemplo de SDK Python', 'Experimento práctico', 'Tokens y recuento', 'Inspector JSON de API', 'Funciones no incluidas', 'Organización del código', 'Código fuente completo'],
 body=['Una API (interfaz de programación) define cómo se comunica un programa con un proveedor remoto. La aplicación envía una solicitud HTTPS autenticada y recibe una respuesta estructurada, normalmente JSON.',
 '1. Introducir texto y parámetros. 2. El SDK autentica con la clave API. 3. Se envía la solicitud HTTPS. 4. Gemini procesa los datos. 5. La aplicación presenta respuesta, tiempo y tokens.',
 'Los parámetros opcionales se envían únicamente si están activos. Algunos modelos no admiten determinadas opciones.',
 'Tiempo límite HTTP de 45 segundos y sin reintentos automáticos. 404: modelo no disponible; 429: cuota agotada; 400: parámetros o solicitud no válidos. Un timeout no garantiza que no se cobre la llamada.',
 'Enviar el mismo texto cambiando solo un parámetro compatible. Comparar resultados y tokens. El experimento multilingüe crea dos traducciones a partir del texto principal.',
 'Los tokens no tienen longitud fija. count_tokens mide el texto de entrada; usage_metadata informa del consumo real, posiblemente con tokens de razonamiento. Las traducciones consumen tokens adicionales.',
 'El inspector enseña objetos del SDK, no paquetes HTTPS capturados. Las claves se ocultan; el texto y las respuestas permanecen visibles.',
 'El laboratorio se centra en texto. Imágenes, audio, vídeo, archivos y otras funciones requieren llamadas distintas.',
 'app.py gestiona la interfaz y sesiones; api_client.py las llamadas Gemini; educational_content.py las traducciones didácticas sin costes de API.'],
 params=['Identificador del modelo LLM.', 'Texto y mensajes de la conversación.', 'Instrucciones globales para el modelo.', 'Variabilidad de generación cuando se admite.', 'Probabilidad acumulada para elegir tokens.', 'Cantidad de tokens candidatos.', 'Número de respuestas alternativas.', 'Límite de tokens generados, incluidos los internos.', 'Desincentiva reutilizar elementos ya mencionados.', 'Reduce repeticiones frecuentes.', 'Semilla de repetibilidad aproximada.', 'Secuencias que detienen la generación.', 'Formato de salida como JSON.', 'Configuración del razonamiento, si se admite.', 'Umbrales de los filtros de seguridad.', 'Activa búsqueda web si está disponible.'],
 code_names=['01 · Preparación', '02 · Estado de sesión', '03 · Entradas y clave API', '04 · Configuración', '05 · Llamada HTTPS', '06 · Respuesta y métricas', '07 · JSON estructurado', '08 · Procesamiento CSV', '09 · Gestión de errores', '10 · Recuento de tokens', '11 · Inspector JSON', '12 · Traducción automática'],
 code_desc=['Las importaciones cargan Streamlit y el SDK; set_page_config inicializa la página.', 'session_state conserva los datos tras cada actualización.', 'Los controles recogen clave, modelo e idioma; el campo de clave está oculto.', 'Solo se envían los parámetros activados.', 'El SDK realiza la llamada HTTPS y recibe la respuesta.', 'Se muestran el texto y las métricas reales.', 'La clasificación usa campos JSON definidos.', 'Cada fila CSV se analiza y exporta a Excel.', 'Los errores se explican sin mostrar secretos.', 'Se mide el prompt antes y el uso real después.', 'La traza enseña datos del SDK con claves ocultas.', 'El texto principal se traduce automáticamente a otros dos idiomas con Gemini.'],
 ),
'de': dict(
 titles=['Was ist eine API?', 'Ablauf einer Anfrage', 'Anfrageparameter', 'Zeitlimits, Kontingente und Fehler', 'Python-SDK-Beispiel', 'Praktisches Experiment', 'Token und ihre Zählung', 'API-JSON-Inspektor', 'Nicht enthaltene Funktionen', 'Programmstruktur', 'Vollständiger Quellcode'],
 body=['Eine API (Programmierschnittstelle) legt fest, wie eine Anwendung mit einem entfernten Anbieter kommuniziert. Die App sendet eine authentifizierte HTTPS-Anfrage und erhält eine strukturierte Antwort, meist JSON.',
 '1. Text und Parameter eingeben. 2. Das SDK verwendet den API-Schlüssel. 3. Die HTTPS-Anfrage wird gesendet. 4. Gemini verarbeitet den Inhalt. 5. Antwort, Dauer und Token werden angezeigt.',
 'Optionale Parameter werden nur bei Aktivierung gesendet. Welche Einstellungen funktionieren, hängt vom Modell ab.',
 'HTTP-Zeitlimit: 45 Sekunden; keine automatischen Wiederholungen. 404: Modell nicht verfügbar; 429: Kontingent erschöpft; 400: ungültige Eingaben. Ein Timeout schließt eine Abrechnung nicht aus.',
 'Ändern Sie jeweils nur einen unterstützten Parameter und vergleichen Sie Ergebnisse, Laufzeit und Token. Das Sprachexperiment übersetzt einen Ausgangstext automatisch.',
 'Token haben keine feste Länge. count_tokens misst den Eingabetext; usage_metadata enthält den tatsächlichen Verbrauch, gegebenenfalls auch Denk-Token. Übersetzungen verbrauchen zusätzliche Token.',
 'Der Inspektor zeigt SDK-Daten, keinen abgefangenen HTTPS-Verkehr. Schlüssel werden ausgeblendet; Eingaben und Ergebnisse bleiben sichtbar.',
 'Der Schwerpunkt liegt auf Text. Bild-, Audio-, Video- und Datei-Funktionen erfordern besondere API-Aufrufe.',
 'app.py verwaltet Oberfläche und Sitzungen; api_client.py die Gemini-Anfragen; educational_content.py die offline verfügbaren Lehrtexte.'],
 params=['Kennung des LLM-Modells.', 'Text und Gesprächsverlauf.', 'Globale Anweisungen zum Modellverhalten.', 'Steuert die Variabilität, falls unterstützt.', 'Kumulierte Wahrscheinlichkeit bei der Token-Auswahl.', 'Anzahl möglicher nächster Token.', 'Anzahl alternativer Antworten.', 'Obergrenze erzeugter Token einschließlich interner Token.', 'Bremst die erneute Verwendung früherer Inhalte.', 'Reduziert häufige Wiederholungen.', 'Startwert für näherungsweise Reproduzierbarkeit.', 'Zeichenfolgen zum Stoppen.', 'Antwortformat, etwa JSON.', 'Steuerung des Schlussfolgerns, falls verfügbar.', 'Verfügbare Grenzwerte der Sicherheitsfilter.', 'Websuche, falls unterstützt.'],
 code_names=['01 · Einrichtung', '02 · Sitzungszustand', '03 · Eingaben und API-Schlüssel', '04 · Konfiguration', '05 · HTTPS-Aufruf', '06 · Antwort und Messwerte', '07 · Strukturiertes JSON', '08 · CSV-Verarbeitung', '09 · Fehlerbehandlung', '10 · Token-Zählung', '11 · JSON-Inspektor', '12 · Automatische Übersetzung'],
 code_desc=['Importe laden Streamlit und SDK; set_page_config richtet die Seite ein.', 'session_state bewahrt Daten zwischen Ausführungen auf.', 'Eingabefelder erfassen Schlüssel, Modell und Sprache; der Schlüssel wird verdeckt.', 'Nur aktivierte Parameter werden übertragen.', 'Das SDK sendet HTTPS-Anfragen und liest die Antworten.', 'Text, Dauer und tatsächliche Token-Werte werden dargestellt.', 'Die Klassifizierung verlangt vorgegebene JSON-Felder.', 'CSV-Zeilen werden analysiert und nach Excel exportiert.', 'Fehler werden ohne Veröffentlichung von Schlüsseln erklärt.', 'Prompt-Token und tatsächlicher Verbrauch werden getrennt erfasst.', 'SDK-Anfrage und -Antwort werden mit ausgeblendeten Zugangsdaten gezeigt.', 'Ein Ausgangstext wird mit Gemini in zwei ausgewählte Sprachen übersetzt.'],
 ),
'pt': dict(
 titles=['O que é uma API?', 'Ciclo de uma chamada', 'Parâmetros da chamada', 'Tempo limite, quotas e erros', 'Exemplo Python com SDK', 'Experiência prática', 'Tokens e contagem', 'Monitor JSON das API', 'Funcionalidades não incluídas', 'Estrutura do código', 'Código-fonte completo'],
 body=['Uma API (interface de programação) define como uma aplicação comunica com um fornecedor remoto. A aplicação envia um pedido HTTPS autenticado e recebe uma resposta estruturada, normalmente em JSON.',
 '1. Introduzir texto e parâmetros. 2. O SDK autentica com a chave API. 3. É enviado o pedido HTTPS. 4. Gemini processa o texto. 5. A aplicação mostra resposta, tempo e tokens.',
 'Os parâmetros opcionais só são enviados quando ativados. A compatibilidade depende do modelo escolhido.',
 'Tempo limite HTTP de 45 segundos, sem tentativas automáticas. 404: modelo indisponível; 429: quota excedida; 400: pedido inválido. Um timeout não garante que a chamada não tenha sido cobrada.',
 'Repetir um texto alterando apenas um parâmetro compatível; comparar respostas e tokens. A experiência multilingue traduz automaticamente um texto principal.',
 'Os tokens não têm comprimento fixo. count_tokens mede a entrada; usage_metadata apresenta o consumo real, incluindo por vezes tokens de raciocínio. As traduções geram consumo adicional.',
 'O monitor mostra objetos do SDK, e não pacotes HTTPS. As chaves são ocultadas, mas os textos permanecem visíveis.',
 'O laboratório centra-se na geração de texto. Imagens, áudio, vídeo e ficheiros exigem outras operações da API.',
 'app.py gere interface e sessões; api_client.py efetua chamadas Gemini; educational_content.py contém traduções didáticas sem chamadas API.'],
 params=['Identificador do modelo LLM.', 'Texto e mensagens da conversa.', 'Instruções globais de comportamento.', 'Variabilidade da geração, se suportada.', 'Probabilidade acumulada para seleção de tokens.', 'Número de possíveis tokens seguintes.', 'Quantidade de respostas alternativas.', 'Limite de tokens gerados, incluindo internos.', 'Desencoraja reutilização de elementos anteriores.', 'Reduz repetição frequente de tokens.', 'Semente para repetibilidade aproximada.', 'Sequências que terminam a geração.', 'Formato de resposta, como JSON.', 'Controla raciocínio quando disponível.', 'Limiares de filtros de segurança.', 'Ativa pesquisa web, quando suportada.'],
 code_names=['01 · Preparação', '02 · Estado da sessão', '03 · Entradas e chave API', '04 · Configuração', '05 · Pedido HTTPS', '06 · Resposta e métricas', '07 · JSON estruturado', '08 · Processamento CSV', '09 · Tratamento de erros', '10 · Contagem de tokens', '11 · Monitor JSON', '12 · Tradução automática'],
 code_desc=['As importações carregam Streamlit e SDK; set_page_config prepara a página.', 'session_state guarda os dados entre interações.', 'Os controlos recolhem chave, modelo e idioma, com chave oculta.', 'Só os parâmetros ativados são incluídos.', 'O SDK envia o pedido HTTPS e recebe a resposta.', 'São mostrados o texto, a duração e os tokens reais.', 'A classificação devolve campos JSON definidos.', 'As linhas CSV são analisadas e exportadas para Excel.', 'Os erros são explicados sem revelar segredos.', 'A entrada e o consumo real são medidos separadamente.', 'A rastreabilidade mostra objetos do SDK com credenciais ocultadas.', 'O texto principal é traduzido automaticamente para duas línguas pelo Gemini.'],
 ),
'zh': dict(
 titles=['什么是 API？', '请求的处理流程', 'API 请求参数', '超时、配额与错误', 'Python SDK 示例', '课堂实践', 'Token 与计数', 'API JSON 检查器', '本实验未涵盖的功能', '代码结构', '完整源代码'],
 body=['API（应用程序编程接口）规定应用程序与远程服务通信的方式。应用程序通过 HTTPS 发送经过身份验证的请求，服务商返回结构化数据，通常采用 JSON 格式。',
 '1. 输入提示词并设置参数；2. SDK 使用 API 密钥进行验证；3. 发送 HTTPS 请求；4. Gemini 处理输入；5. 应用程序显示结果、响应时间及 Token 用量。',
 '只有主动启用的可选参数才会发送。不同模型支持的参数可能不同，不受支持的设置可能导致错误。',
 '单次 HTTP 请求超时时间为 45 秒，且不自动重试。404 表示模型不可用；429 表示超过配额；400 表示请求或参数错误。超时不代表服务商一定未处理或计费。',
 '保持提示词不变，每次只修改一个兼容参数，比较输出、时间和 Token 用量。多语言实验从主语言文本自动生成两种翻译。',
 'Token 并非固定长度。count_tokens 统计生成前的输入；usage_metadata 报告实际用量，其中可能包含推理 Token。自动翻译也会额外消耗 Token。',
 '检查器展示 SDK 请求和解析后的响应，并非原始 HTTPS 抓包。API 密钥会被隐藏，但提示词和回答仍可见，请勿输入机密信息。',
 '本实验主要关注文本生成。图片、音频、视频、文件及缓存等功能需要使用其他 API 操作。',
 'app.py 管理界面和会话；api_client.py 管理 Gemini 请求、Token 和错误；educational_content.py 提供不需要 API 调用的教学内容翻译。'],
 params=['要调用的 LLM 模型标识符。', '提示词内容和对话历史。', '控制模型行为的全局指令。', '控制生成的随机性（如模型支持）。', '按累积概率筛选候选 Token。', '限制下一 Token 的候选数量。', '要求生成的备选回答数量。', '生成 Token 的上限，可能包含内部 Token。', '降低已出现内容再次出现的概率。', '减少高频重复 Token。', '尽量提高可重复性的随机种子。', '生成到指定字符串时停止。', '输出格式，例如 JSON。', '模型推理配置（如支持）。', '安全过滤类别和阈值。', '启用网络搜索（如支持）。'],
 code_names=['01 · 初始化', '02 · 会话状态', '03 · 输入和 API 密钥', '04 · 请求配置', '05 · HTTPS 调用', '06 · 回答与指标', '07 · 结构化 JSON', '08 · CSV 处理', '09 · 错误处理', '10 · Token 计数', '11 · JSON 检查器', '12 · 自动翻译'],
 code_desc=['导入 Streamlit 和 Gemini SDK，并使用 set_page_config 设置页面。', 'session_state 保存聊天、语言和结果，避免页面刷新时丢失。', '输入控件接收密钥、模型和语言；密码框隐藏密钥。', '只发送用户已启用的可选参数。', 'SDK 发送 HTTPS 请求，并返回响应对象。', '显示模型回答以及实际耗时和 Token 用量。', '异常分类要求固定的 JSON 字段以方便处理。', '逐行处理 CSV，并将结果导出 Excel。', '捕获错误并给出提示，避免泄露密钥。', '分别读取请求前的输入计数和生成后的实际用量。', '展示经过凭据脱敏处理的 SDK 请求及响应。', '将主语言文本通过 Gemini 自动翻译为另外两种语言。'],
 ),
'ja': dict(
 titles=['API とは何か', 'リクエストの流れ', 'API リクエストのパラメータ', 'タイムアウト・制限・エラー', 'Python SDK の例', '実習課題', 'トークンとカウント', 'API JSON インスペクター', '対象外の機能', 'コードの構成', 'ソースコード全体'],
 body=['API（アプリケーションプログラミングインターフェース）は、アプリケーションと外部サービスの通信方法を定義します。HTTPS で認証済みのリクエストを送り、通常 JSON 形式の構造化データを受け取ります。',
 '1. プロンプトと設定を入力。2. SDK が API キーで認証。3. HTTPS で送信。4. Gemini が処理。5. アプリが回答、処理時間、トークン数を表示します。',
 '任意のパラメータは有効化した場合にのみ送信します。利用可能な設定はモデルごとに異なり、非対応の指定はエラーの原因になります。',
 'HTTP タイムアウトは 45 秒、自動再試行はありません。404 はモデル未対応、429 は利用枠超過、400 は不正なリクエストです。タイムアウトしても課金対象にならないとは限りません。',
 '同じプロンプトで対応しているパラメータを一つずつ変更し、回答、時間、トークンを比較します。多言語実験では基準言語の文章から２言語に自動翻訳します。',
 'トークンの長さは一定ではありません。count_tokens は生成前の入力数、usage_metadata は実際の利用量を示します。思考トークンや翻訳処理の追加トークンにも注意してください。',
 'インスペクターは SDK のリクエストと解析済みレスポンスを表示します。HTTPS の生通信ではありません。キーは除外されますが、入力文と回答は表示されます。',
 'この実習は主にテキスト生成を扱います。画像、音声、動画、ファイル、キャッシュ等は別の API 操作が必要です。',
 'app.py は UI とセッション、api_client.py は Gemini 通信、educational_content.py は API を呼び出さず利用できる教材翻訳を担当します。'],
 params=['呼び出す LLM モデルの識別子。', 'プロンプトの内容と会話履歴。', 'モデルの基本的な動作指示。', '対応モデルで生成のばらつきを調整。', '累積確率による候補トークンの選択。', '次の候補トークン数を制限。', '代替回答の件数。', '生成トークンの上限。内部トークンを含む場合があります。', '既出の話題や要素の再利用を抑制。', '頻繁なトークンの繰り返しを抑制。', '再現性を補助するシード値（保証なし）。', '指定文字列で生成を停止。', 'JSON などの応答形式。', 'モデルの思考処理を設定（対応時）。', '安全フィルターのしきい値。', '対応モデルでウェブ検索を使用。'],
 code_names=['01 · 初期設定', '02 · セッション状態', '03 · 入力と API キー', '04 · 設定', '05 · HTTPS 呼び出し', '06 · 回答と測定値', '07 · 構造化 JSON', '08 · CSV 処理', '09 · エラー処理', '10 · トークン計測', '11 · JSON インスペクター', '12 · 自動翻訳'],
 code_desc=['Streamlit と Gemini SDK を読み込み、set_page_config で画面を設定します。', 'session_state に会話や言語、結果を保持します。', 'キー、モデル、言語を入力し、パスワード欄ではキーを隠します。', '有効化された設定のみリクエストに含めます。', 'SDK が HTTPS リクエストを送信して回答を取得します。', '回答と実際の応答時間、トークン数を表示します。', '異常分析の結果を一定の JSON フィールドにまとめます。', 'CSV の各行を分析し、Excel に書き出します。', '秘密情報を表示せずにエラーを説明します。', '生成前の入力数と生成後の実際の使用量を確認します。', 'キーを伏せた SDK リクエスト・レスポンスを表示します。', '基準言語の文章を Gemini によって選択した２言語へ翻訳します。'],
 ),
}

for language, value in EDU.items():
    assert len(value['titles']) == 11, language
    assert len(value['body']) == 9, language
    assert len(value['params']) == len(PARAMETERS), language
    assert len(value['code_names']) == len(CODE_SAMPLES) == len(value['code_desc']), language
