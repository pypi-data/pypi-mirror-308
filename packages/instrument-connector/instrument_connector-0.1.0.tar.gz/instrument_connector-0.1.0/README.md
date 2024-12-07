# instrument_connector

**instrument_connector** è una libreria Python che semplifica la connessione a strumenti via PyVISA. La libreria fornisce un'interfaccia facile da usare per cercare, connettersi e gestire strumenti di misura utilizzando comandi standard.

## Funzionalità

- Connessione automatica a strumenti tramite modello, IDN o indirizzo.
- Lista di tutte le risorse disponibili con dettagli IDN (se supportati).
- Configurazione opzionale della verbosità per abilitare/disabilitare i messaggi di debug.
- Gestione delle eccezioni personalizzata per rilevare errori di connessione.

## Installazione

Puoi installare la libreria direttamente con pip:

```bash
pip install instrument_connector
```

Se stai sviluppando localmente, puoi installarla in modalità editabile:

```bash
pip install -e .
```

## Utilizzo

### 1. Connessione a uno strumento

Puoi connetterti a uno strumento specificando il modello o un IDN parziale:

```python
import instrument_connector

try:
    # Connetti allo strumento specificando un modello
    instrument = instrument_connector.connect_to_instrument("2380")
    print("Connected to the instrument successfully!")
    print("Instrument IDN:", instrument.query("*IDN?"))
except instrument_connector.InstrumentConnectionError as e:
    print(f"Failed to connect: {e}")
```

### 2. Lista delle risorse disponibili

Per elencare tutte le risorse disponibili e ottenere informazioni sui dispositivi connessi:

```python
resources = instrument_connector.list_available_resources()
print("Available resources:")
for resource in resources:
    print(f"Address: {resource['address']}, IDN: {resource['idn']}")
```

### 3. Abilitare o disabilitare i messaggi di debug

Puoi configurare la libreria per stampare messaggi di debug durante l'esecuzione:

```python
instrument_connector.set_verbosity(True)  # Abilita messaggi di debug
instrument_connector.set_verbosity(False) # Disabilita messaggi di debug
```

## Dipendenze

La libreria richiede **PyVISA** per la gestione della connessione agli strumenti:

```bash
pip install pyvisa
```

## Licenza

Questo progetto è distribuito sotto licenza MIT. Consulta il file [LICENSE](./LICENSE) per i dettagli.
