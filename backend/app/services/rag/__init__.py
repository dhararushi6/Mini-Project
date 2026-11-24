"""Citation-aware retrieval tools for the legal RAG service."""

from .models import LegalChunk, RetrievedPassage, RAGAnswer
from .retriever import CitationAwareRetriever
from .service import LegalRAGService

__all__ = ["CitationAwareRetriever", "LegalChunk", "LegalRAGService", "RAGAnswer", "RetrievedPassage"]
