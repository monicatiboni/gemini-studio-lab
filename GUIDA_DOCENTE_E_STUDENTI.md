# Gemini Studio Lab 4.0 - laboratorio API con monitor JSON

## Prerequisiti

- Browser con accesso all'indirizzo Streamlit pubblicato dal docente.
- Una chiave Google Gemini API **personale**, con modello e quota utilizzabili; verificare eventuale fatturazione.
- Nessuna installazione locale sui PC universitari.

## Prima prova (5 minuti)

1. Apri l'app su Streamlit e scegli la lingua dell'interfaccia.
2. Inserisci la chiave API nel pannello laterale **Chiave API Google Gemini**. Non copiarla negli screenshot o nel codice.
3. Scegli un modello Gemini accessibile.
4. Apri **Chat multilingue**, scrivi: "Spiega che cos'è un'API in due frasi" e premi **Invia alle API**.
5. Controlla la risposta, i token e il tempo di risposta.

## Osserva richiesta e risposta JSON (10 minuti)

6. Sotto le metriche apri **Monitor JSON API**.
7. Nel pannello a sinistra cerca `model`, `contents`, `config`.
8. Nel pannello a destra cerca `candidates` e `usage_metadata`.
9. Confronta `usage_metadata.prompt_token_count`, `candidates_token_count` e `total_token_count`.
10. Apri **Parametri della chiamata API**, abilita *max_output_tokens* e invia di nuovo lo stesso prompt.
11. Confronta le due richieste JSON: il parametro configurato deve comparire nel campo `config`.

**Importante**: il monitor JSON è una rappresentazione dei dati passati all'SDK Python e della risposta interpretata dall'SDK; non è la registrazione dei pacchetti HTTPS. Il monitor esclude la chiave API. I contenuti di prompt e risposte rimangono tuttavia visibili: usare solo dati fittizi.

## Esercitazione avanzata (15 minuti)

12. Cambia **Lingua della risposta** scegliendo inglese: mantieni lo stesso prompt italiano. Controlla l'istruzione di sistema nella richiesta JSON.
13. Apri **Analisi tecnica**, inserisci "Il motore del nastro trasportatore si surriscalda". Analizza il JSON strutturato e il monitor della chiamata.
14. Apri **Esperimento token** e confronta tre testi equivalenti in italiano, inglese e tedesco.
15. Confronta il numero di token, la latenza e la qualità delle risposte. Non assumere che il token sia una parola o una lunghezza fissa di caratteri.

## Sicurezza e uso contemporaneo

- Ogni studente usa la propria chiave API: non condividere la chiave del docente.
- Streamlit conserva i risultati nello stato della **singola sessione**; l'app non impiega database o variabili globali per memorizzare chiavi e conversazioni.
- Non sono configurati utenti, ruoli o autenticazione dell'applicazione. Per dati sensibili usare un servizio appositamente approvato dall'ateneo, non questa demo didattica.
- In Community Cloud la condivisione di risorse hardware e le quote dell'API possono influenzare prestazioni e disponibilità. Verificare l'uso simultaneo da più dispositivi prima della lezione.
- Le tracce JSON sono esportabili solo con un clic esplicito dell'utente; NON contengono la chiave API, ma contengono prompt e risposte.

## Come aggiornare la versione 3 pubblicata su GitHub

1. Apri il repository già collegato a Streamlit Community Cloud.
2. Sostituisci i file `app.py` e `api_client.py` con quelli della versione 4.0, mantenendo gli stessi nomi nella radice del repository.
3. Aggiorna `README.md` e aggiungi facoltativamente questa guida.
4. Non modificare la cartella `.streamlit` e non pubblicare file con credenziali.
5. Premi **Commit changes**: Streamlit normalmente rileva il commit e riavvia automaticamente l'app.
6. Aggiorna la pagina dell'app nel browser e verifica l'indicazione **UNIVERSITY EDITION 4.0** nel pannello laterale.

Non serve creare una nuova applicazione Streamlit o un nuovo indirizzo web.
