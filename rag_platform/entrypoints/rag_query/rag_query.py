from rag_platform.comproot import rag_search

BlockType = tuple[float, float, float, float, str, int, int]


def query_documents(query: str) -> str:
    result = rag_search.search(query=query)
    return str(result)
