from rag_platform.comproot import db_conection, text_embedding_repo


def try_db():
    print(db_conection)
    remaining_dims: list[float] = [0.0] * 765
    text_embedding_repo.insert_embeddings(
        [
            [1, 0, 0, *remaining_dims],
            [0, 1, 0, *remaining_dims],
            [0, 0, 1, *remaining_dims],
        ],
        ["x", "y", "z"],
        ["x_", "y_", "z_"],
    )
    for example_vector in [[0.8, 0.1, 0.03], [0.3, 0.6, 0.03], [0.2, 0.1, 0.63]]:

        print(
            example_vector,
            text_embedding_repo.get_similar_embeddings(example_vector + remaining_dims),
        )


if __name__ == "__main__":
    try_db()
