from backend.app.services.rag.evaluation import citation_coverage, recall_at_k
from backend.app.services.rag.models import RetrievedPassage


def passage(chunk_id: str) -> RetrievedPassage:
    return RetrievedPassage(
        chunk_id=chunk_id,
        text="Official consumer-law text.",
        source_title="Consumer Protection Act",
        source_url="https://consumeraffairs.nic.in/",
    )


def test_recall_at_k_finds_expected_passage() -> None:
    assert recall_at_k([passage("a"), passage("b")], "b", k=2) == 1.0


def test_citation_coverage_requires_a_citation() -> None:
    assert citation_coverage("A source-linked answer", 1)
    assert not citation_coverage("A source-linked answer", 0)
