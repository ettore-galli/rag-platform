from ollama import Client


def try_ollama():
    host = "http://ollama:11434"
    client = Client(host=host)

    testo = "What temperature is pizza best cooked at?"

    embeddings = client.embed(
        model="nomic-embed-text",
        input=[testo],
    )

    chat = client.chat(
        model="qwen_3_6b_deterministic",
        messages=[{"role": "user", "content": testo}],
    )

    print(embeddings)
    print(chat)


if __name__ == "__main__":
    try_ollama()
