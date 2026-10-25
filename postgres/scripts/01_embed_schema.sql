CREATE TABLE text_embeddings (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(768) NOT NULL,
    content TEXT NOT NULL,
    file_name TEXT NOT NULL,
    sentence_number INTEGER NOT NULL
)
;

CREATE INDEX idx_text_embeddings_embedding
ON text_embeddings
USING hnsw (embedding vector_cosine_ops)
;