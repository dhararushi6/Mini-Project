from .models import RetrievedPassage


def recall_at_k(retrieved: list[RetrievedPassage], expected_chunk_id: str, k: int = 3) -> float:
    """Return 1 when the expected official passage appears in the first k results."""
    return float(any(passage.chunk_id == expected_chunk_id for passage in retrieved[:k]))


def citation_coverage(answer_text: str, citation_count: int) -> bool:
    """Minimal release gate: evidence-backed answers must expose at least one citation."""
    return bool(answer_text.strip() and citation_count > 0)
