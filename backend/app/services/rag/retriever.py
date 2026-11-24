from __future__ import annotations

from typing import Any
import chromadb

from .models import LegalChunk, RetrievedPassage


class CitationAwareRetriever:
    """Stores official-law chunks and returns only passages with source metadata."""

    def __init__(self, persist_directory: str = "data/processed/chroma", collection_name: str = "official_legal_sources") -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def index(self, chunks: list[LegalChunk]) -> None:
        if not chunks:
            return
        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[chunk.metadata() for chunk in chunks],
        )

    def search(self, query: str, state: str | None = None, domain: str | None = None, limit: int = 5) -> list[RetrievedPassage]:
        where: dict[str, Any] | None = None
        filters = [{key: {"$eq": value}} for key, value in {"state": state, "domain": domain}.items() if value]
        if len(filters) == 1:
            where = filters[0]
        elif len(filters) > 1:
            where = {"$and": filters}

        result = self.collection.query(query_texts=[query], n_results=limit, where=where, include=["documents", "metadatas", "distances"])
        passages: list[RetrievedPassage] = []
        for chunk_id, text, metadata, distance in zip(
            result.get("ids", [[]])[0],
            result.get("documents", [[]])[0],
            result.get("metadatas", [[]])[0],
            result.get("distances", [[]])[0],
        ):
            if not metadata.get("source_url"):
                continue
            passages.append(RetrievedPassage(chunk_id=chunk_id, text=text, distance=distance, **metadata))
        return passages
