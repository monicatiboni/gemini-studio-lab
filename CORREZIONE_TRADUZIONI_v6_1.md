# Gemini Studio Lab 6.1 - correzione traduzione dei prompt

## Errore corretto
Nell'esperimento multilingue la funzione di traduzione poteva eseguire il prompt originale invece di tradurne il testo (per esempio generando una spiegazione anziche tradurre "Spiega...").

## Modifica tecnica
- Il prompt master e passato come campo `source_text` di un oggetto JSON, non come comando da eseguire.
- La richiesta contiene istruzioni esplicite: tradurre l'imperativo senza eseguirlo.
- Si usa uno schema di risposta JSON con il campo obbligatorio `translation`.
- Il testo mostrato come traduzione e estratto SOLO da quel campo.
- Nessuna chiamata supplementare viene eseguita: una richiesta di traduzione per lingua di destinazione.
- La funzione conserva la separazione dei token spesi per tradurre rispetto all'esperimento.

## Come installare su Streamlit
Sostituire entrambi i file `api_client.py` e `app.py` nella cartella principale del repository GitHub `monicatiboni/gemini-studio-lab`. Non cambiare gli altri file. Salvare con Commit changes, quindi attendere il redeploy e ricaricare la pagina. La cache dei testi tradotti e nella sessione Streamlit: ricreare una sessione o cambiare il testo master per forzare una nuova traduzione.

## Prova consigliata
Master italiano: `Spiega in due frasi come funziona un sensore di temperatura industriale.`
Lingua destinazione inglese: risultato atteso nella forma `Explain in two sentences how an industrial temperature sensor works.`
NON accettare una spiegazione del sensore: quella e la risposta alla domanda e non la traduzione del prompt.

## Compatibilita
Il modello selezionato deve supportare l'output JSON strutturato per `generate_content`. L'applicazione mostra un errore se la risposta non e conforme. Test automatici locali sono eseguiti con API simulate; la chiamata reale richiede una chiave Gemini personale.

## Correzioni aggiuntive all'interfaccia
- Il pulsante "Genera automaticamente le traduzioni" esegue realmente una nuova traduzione anche se era disponibile una traduzione memorizzata.
- I due campi di traduzione sono modificabili: gli studenti possono correggere eventuali errori prima di contare i token o generare risposte.
- Alla rigenerazione si eliminano i risultati sperimentali obsoleti.
