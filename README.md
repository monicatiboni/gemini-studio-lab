# Gemini Studio Lab — API Academy · v4

Applicazione web didattica multilingue, realizzata con **Streamlit** e SDK ufficiale **Google Gen AI**. Le chiamate alle Gemini API sono reali: non ci sono risposte simulate in caso di errore.

## Funzioni della versione 4

- Pulsanti principali ad alto contrasto con testo bianco; campi e selettori bianchi.
- **Monitor JSON API** in Chat, Analisi tecnica, CSV (per riga) ed Esperimento token: rappresentazione dei parametri della richiesta e della risposta interpretata dall'SDK. Chiave API esclusa, con filtro difensivo delle credenziali e export opzionale della traccia.
- Per uso pubblico, nessuna chiave predefinita viene letta dall'ambiente del server: ogni studente inserisce la propria.
- Design chiaro: sfondo grigio chiaro, pannelli e campi di inserimento bianchi, testi ad alto contrasto, accenti blu/verde.
- Lingue dell'interfaccia: italiano, inglese, francese, spagnolo, tedesco e portoghese; lingua delle risposte indipendente dalla lingua dell'interfaccia.
- Chat multilingue, analisi singola di anomalie industriali, caricamento CSV e scaricamento Excel.
- Pannello per il controllo dei parametri della generazione: temperatura, top-p, top-k, numero di candidati, max token, penalita, seed, stop sequences, formato JSON e schema, thinking, safety e ricerca Google, probabilita dei token.
- Ogni parametro opzionale e inviato **solo se attivato**; alcuni parametri sono incompatibili con determinati modelli, e Google puo ignorarli o restituire un errore.
- Sezioni **Guida API** e **Spiegazione del codice**, con schemi, tabella dei parametri e frammenti Python.
- Integrazione Gemini separata nel file `api_client.py`, per rendere piu facile lo studio del codice.
- Dashboard nelle sezioni Chat e Analisi con **token di input, token di output, totale token e tempo di risposta** ottenuti da `usage_metadata` (nessuna stima arbitraria).
- Analisi CSV: aggiunte colonne `API_input_tokens`, `API_output_tokens`, `API_total_tokens` e `API_seconds` nel file Excel esportato.
- Nuova scheda **Esperimento token**: confronto italiano/inglese/tedesco, conteggio preventivo con API `count_tokens`, oppure 3 generazioni sequenziali con tempo e token effettivi. Grafici e download CSV.
- Il conteggio preventivo misura solo il prompt inserito nella scheda; la generazione include anche istruzioni di sistema. Il totale restituito da Gemini puo includere token di ragionamento e altri token non visibili.


## Aggiornamento della versione 3 già pubblicata

Sostituisci **solo** `app.py` e `api_client.py` nella radice del repository GitHub, poi esegui **Commit changes**. Streamlit Community Cloud di norma aggiorna automaticamente l'app allo stesso indirizzo. Aggiorna anche `README.md` e aggiungi `GUIDA_DOCENTE_E_STUDENTI.md` per distribuire le istruzioni.

## Pubblicazione cloud (nessuna installazione sui PC degli studenti)

1. Crea un repository su GitHub, ad esempio `gemini-studio-lab`.
2. Carica **i file contenuti in questa cartella** nella radice del repository (`app.py`, `api_client.py`, `requirements.txt` ecc.).
3. Apri <https://share.streamlit.io/>, scegli **Create app**, collega il repository, seleziona `app.py` come entry point e pubblica.
4. Verifica che la pagina sia visibile da un PC del laboratorio con Chrome/Edge.
5. Gli studenti accedono all'indirizzo HTTPS dell'applicazione e inseriscono la propria chiave Google AI Studio nel campo protetto.

**Nota sicurezza:** questa app didattica non autentica gli utenti. Evitare dati personali, aziendali o sensibili. Streamlit gestisce le chiavi come input di sessione lato server, ma l'hosting condiviso richiede valutazione delle policy dell'istituto. Usare API key personali, mai una chiave comune pubblica, e applicare limiti/quote appropriati al progetto Google. La chiave non viene inclusa negli export.

## Avvio locale (solo per il docente o un PC che consenta installazioni)

Prerequisiti: Python 3.10+ e connessione Internet.

- Windows: `AVVIA_WINDOWS.bat`
- Mac/Linux: `sh AVVIA_MAC_LINUX.sh`
- Manuale: `python -m pip install -r requirements.txt` e `python -m streamlit run app.py`

## Uso passo per passo

1. Apri l'app dal browser.
2. Seleziona la **lingua dell'interfaccia** in alto a sinistra.
3. Crea una chiave su <https://aistudio.google.com/api-keys> e inseriscila nel campo **Chiave API**. Verifica che non siano abilitate fatturazioni indesiderate.
4. Seleziona un modello accessibile e la **lingua delle risposte**.
5. Apri **Parametri della chiamata API**. Lascia i parametri avanzati disattivati per il primo esperimento: l'API adottera i propri default.
6. Nella scheda **Chat multilingue**, scrivi una domanda e inviala.
7. Attiva `max_output_tokens` e confronta una risposta con limite 256 e una con limite 1024; prova altri parametri solo dopo aver verificato che il modello li supporti.
8. Leggi **Guida API** per comprendere i campi della richiesta e **Spiegazione del codice** per esaminare i passaggi.
9. In **Analisi tecnica**, prova una segnalazione e ispeziona il JSON risultante.
10. In **Analisi CSV**, scarica l'esempio, caricalo, elabora poche righe e scarica il file Excel.
11. In **Esperimento token**, confronta i tre prompt equivalenti: prima usa **Conta token (solo input)** e confronta le barre. Successivamente usa **Genera e confronta** per misurare risposta, token e durata. Sono chiamate API reali: rispetta quote e fatturazione.
12. Apri **Monitor JSON API** per confrontare `model`, `contents`, `config`, `candidates` e `usage_metadata`. Non è un dump HTTPS; i prompt e le risposte possono contenere contenuti privati.
13. Osserva il pannello metriche nelle schede **Chat** e **Analisi tecnica**: i valori provengono dal provider, non dalla lunghezza stimata delle stringhe.

## Scelte tecniche

Il client utilizza `client.models.generate_content`, documentato dall'SDK ufficiale, con `types.GenerateContentConfig`. Le sezioni Chat e Analisi condividono le impostazioni; l'analisi impone il formato JSON e disabilita lo schema JSON personalizzato e la ricerca integrata per conservare la struttura del classificatore. Le credenziali non vengono scritte su file, esportate, o inserite nell'URL. La cronologia chat resta nella sessione Streamlit.

Il pannello mostra i parametri principali per **generazione testuale**. L'API Gemini comprende anche chiamate per input multimodali, immagini, audio, video, file, caching e batch service, che **non** condividono tutti gli stessi parametri e richiedono flussi applicativi separati.

## Nota su compatibilita, costi e collaudo

- I parametri non hanno supporto uniforme: Gemini 3.x puo non supportare alcuni controlli di sampling (temperature/top-p/top-k, penalita e candidate count). Disattivarli se restituiscono errori.
- L'accesso gratuito dipende dalla chiave, dal modello, dal progetto e dalle quote. Le chiamate possono essere addebitate se l'account/progetto prevede fatturazione.
- La sintassi Python e stata verificata mediante compilazione statica. Non e stato possibile eseguire l'interfaccia Streamlit in questo ambiente o effettuare una chiamata reale priva di credenziali: verificare prima dell'uso in aula.

## Documentazione ufficiale

- <https://ai.google.dev/api/generate-content>
- <https://googleapis.github.io/python-genai/>
- <https://ai.google.dev/gemini-api/docs/pricing>
- <https://docs.streamlit.io/deploy/streamlit-community-cloud>

## Verifica della versione 4

Effettuato controllo sintattico Python e verifica integrita dello ZIP. Non e stato possibile eseguire chiamate Gemini reali senza una chiave personale, ne verificare il layout in un browser Streamlit in questo ambiente.

Documentazione ufficiale: https://ai.google.dev/gemini-api/docs/tokens e https://googleapis.github.io/python-genai/ .

## Verifica delle sessioni

Ogni browser con una propria sessione Streamlit ha `session_state` indipendente. Non vengono usati file di stato o cache globali per chiavi e risultati. Non abbiamo eseguito un test end-to-end con più utenti su Streamlit Cloud: fare una prova su due browser differenti prima della lezione.
