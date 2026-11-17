# Guida rapida per l'aula — Gemini Studio Lab 6.0

## Docente: pubblicazione senza installazioni in laboratorio

1. Apri il repository GitHub già associato alla tua applicazione Streamlit.
2. Aggiorna `app.py` e `api_client.py` con i file della versione 6.0.
3. Aggiungi in radice `educational_content.py`, `interface_localization.py`, `unibs_logo.py`.
4. Non devi modificare `.streamlit/config.toml` né `requirements.txt`.
5. Esegui **Commit changes** e apri l'indirizzo dell'app Streamlit esistente.
6. Verifica nella barra laterale **UNIVERSITY EDITION 6.0**, la presenza del logo e il modello di partenza `gemini-3-flash-preview`.
7. Collauda con una chiave personale e verifica l'accesso degli studenti al progetto Google AI Studio e alle quote disponibili.

## Studenti: attività iniziale

1. Apri il link Streamlit fornito dal docente dal browser (nessuna installazione).
2. Scegli la lingua dell'interfaccia, tra cui **中文** e **日本語**.
3. Inserisci la chiave personale Gemini nel pannello laterale; non condividerla.
4. Scegli un modello disponibile; il default `gemini-3-flash-preview` potrebbe non essere accessibile al tuo account.
5. Scrivi una domanda in Chat multilingue, inviala e osserva risposta, tempo e token.
6. Apri Guida API e Spiegazione del codice. Cambia lingua e verifica che le spiegazioni cambino senza chiamate API.

## Esperimento token — test suggerito

- Lingua master: **italiano**.
- Testo: «Spiega in due frasi come funziona un sensore di temperatura industriale».
- Lingue target: **inglese** e **giapponese** (o cinese).
- Premi **Genera automaticamente le traduzioni**. L'app effettua fino a due chiamate Gemini; i token della traduzione sono separati dal confronto.
- Premi **Conta token** e osserva la differenza tra le tre lingue.
- Premi **Genera e confronta** e confronta i token di risposta e la durata.
- Modifica il testo originale e ripeti: le traduzioni vengono rigenerate perché il testo è cambiato.
- Scarica il CSV dell'esperimento e commenta i risultati.

## Tre domande per la discussione

1. Perché frasi semanticamente equivalenti non hanno necessariamente lo stesso numero di token?
2. Perché le metriche dopo la generazione possono differire dal semplice count_tokens del prompt?
3. Quali chiamate aggiuntive esegue l'app per tradurre i testi e come si distinguono dal confronto vero e proprio?

## Sicurezza

Usare soltanto dati fittizi. La chiave API è personale; eventuali quote e costi dipendono dal progetto Google. Non inserire credenziali nelle richieste, nei file CSV o nei materiali consegnati. L'app didattica è pubblica e non dispone di un sistema di login per studenti.
