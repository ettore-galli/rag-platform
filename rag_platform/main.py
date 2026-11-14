import click

from rag_platform.entrypoints.rag_loader.rag_loader import load_documents
from rag_platform.entrypoints.rag_query.rag_query import query_documents


@click.group()
def cli() -> None:
    pass


@cli.command()
def acquire() -> None:
    print(load_documents())


@cli.command()
@click.argument("prompt")
def query(prompt: str) -> None:
    print(query_documents(query=prompt))
