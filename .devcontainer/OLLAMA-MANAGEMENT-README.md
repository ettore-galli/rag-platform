# Ollama CLI Cheat Sheet

## Verifica installazione

Versione client:

```bash
ollama --version
```

Verifica server:

```bash
curl http://localhost:11434/api/version
```

---

## Gestione modelli

Elenca i modelli installati:

```bash
ollama list
```

Mostra informazioni su un modello:

```bash
ollama show mistral
```

Mostra il Modelfile generato:

```bash
ollama show mistral --modelfile
```

Rimuove un modello:

```bash
ollama rm mistral
```

---

## Download modelli

Scarica un modello:

```bash
ollama pull mistral
```

Scarica una versione specifica:

```bash
ollama pull qwen2.5-coder:7b
```

Aggiorna il modello all'ultima versione disponibile:

```bash
ollama pull mistral
```

---

## Esecuzione

Avvia una chat interattiva:

```bash
ollama run mistral
```

Specifica un prompt:

```bash
ollama run mistral "Spiegami Docker Compose"
```

Esce dalla chat:

```text
/bye
```

---

## Gestione modelli personalizzati

Creare un file `Modelfile`:

```text
FROM qwen2.5-coder:7b

SYSTEM You are a Senior Python Developer.
```

Creazione del modello:

```bash
ollama create my-coder -f Modelfile
```

Verifica:

```bash
ollama list
```

Utilizzo:

```bash
ollama run my-coder
```

---

## API HTTP

Elenco modelli:

```bash
curl http://localhost:11434/api/tags
```

Versione server:

```bash
curl http://localhost:11434/api/version
```

Generazione testo:

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "mistral",
    "prompt": "Spiegami Docker Compose"
  }'
```

Chat:

```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "mistral",
    "messages": [
      {
        "role": "user",
        "content": "Ciao"
      }
    ]
  }'
```

---

## Debug

Verificare che il server risponda:

```bash
curl http://localhost:11434/api/version
```

Verificare i modelli disponibili:

```bash
curl http://localhost:11434/api/tags
```

Confrontare API e CLI:

```bash
ollama list
```

```bash
curl http://localhost:11434/api/tags
```

I risultati dovrebbero essere coerenti.

---

## Posizioni tipiche dei dati

Linux / Container:

```text
/root/.ollama
```

macOS:

```text
~/.ollama
```

Contenuti tipici:

```text
~/.ollama
├── blobs
├── manifests
├── models
└── cache
```

---

## Comandi utili durante lo sviluppo

Scarica e prova rapidamente un modello:

```bash
ollama pull mistral
ollama run mistral

# Esempi utili:
ollama pull qwen3:0.6b
ollama pull nomic-embed-text
 
```

Elenca i modelli:

```bash
ollama list
```

Verifica che il server sia raggiungibile:

```bash
curl http://localhost:11434/api/version
```

Verifica che il modello sia registrato:

```bash
curl http://localhost:11434/api/tags
```
``