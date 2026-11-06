from rag_platform.comproot import ollama_model_client


def try_ollama():

    testo = "hi"

    embeddings = ollama_model_client.embed(
        input=[testo],
    )

    chat = ollama_model_client.chat(
        messages=[{"role": "user", "content": testo}],
    )

    print(embeddings)
    print(chat)


if __name__ == "__main__":
    try_ollama()
