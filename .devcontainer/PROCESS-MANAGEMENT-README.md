# Dev Container Workflow

## Architettura

```text
VS Code
   ↓
Docker Compose
   ↓
+----------------+
| dev            |
| workspace      |
+----------------+

+----------------+
| ollama         |
| servizio LLM   |
+----------------+
```

Il container di lavoro è `dev`.

Il server LLM gira nel container `ollama`.

---

## Principio fondamentale

Docker Compose è il proprietario dei container.

VS Code è soltanto un client che si collega al container `dev`.

La fonte di verità è sempre:

```bash
docker ps
```

---

## Avvio del progetto

Aprire la cartella in VS Code e selezionare:

```text
Dev Containers: Reopen in Container
```

VS Code:

1. legge `.devcontainer/devcontainer.json`
2. avvia Docker Compose
3. crea i container se necessario
4. si collega al container `dev`

Verifica:

```bash
docker ps
```

Output atteso:

```text
rag-platform_devcontainer-dev-1
rag-platform_devcontainer-ollama-1
```

---

## Verifica connettività verso Ollama

Dal terminale nel devcontainer:

```bash
curl http://ollama:11434/api/version
```

Verifica modelli:

```bash
curl http://ollama:11434/api/tags
```

---

## Chiusura VS Code

Comando:

```text
Close Remote Connection
```

Effetto:

- VS Code si scollega
- i container continuano a girare

Verifica:

```bash
docker ps
```

I container devono essere ancora presenti.

---

## Riapertura

Aprire VS Code e selezionare:

```text
Dev Containers: Reopen in Container
```

VS Code si ricollega ai container esistenti senza ricrearli.

---

## Rebuild del container

Usare:

```text
Dev Containers: Rebuild Container
```

quando si modificano:

- Dockerfile
- docker-compose.yml
- devcontainer.json
- configurazioni del container

---

## Spegnimento completo

Fermare e rimuovere i container del progetto:

```bash
docker compose -p rag-platform_devcontainer down
```

Verifica:

```bash
docker ps
```

I container del progetto non devono più apparire.

---

## Riaccensione da terminale

```bash
docker compose -p rag-platform_devcontainer up -d
```

Verifica:

```bash
docker ps
```

Dev e Ollama devono risultare attivi.

---

## Diagnostica rapida

Visualizzare i container attivi:

```bash
docker ps
```

Log di Ollama:

```bash
docker compose -p rag-platform_devcontainer logs ollama
```

Entrare nel container Ollama:

```bash
docker compose -p rag-platform_devcontainer exec ollama sh
```

Entrare nel container Dev:

```bash
docker compose -p rag-platform_devcontainer exec dev sh
```

---

## Regola pratica

Quando qualcosa non torna:

1. Controllare sempre `docker ps`
2. Verificare che `dev` e `ollama` siano attivi
3. Verificare la connettività:

```bash
curl http://ollama:11434/api/version
```

4. Solo dopo analizzare problemi di volumi, modelli o variabili d'ambiente