from __future__ import annotations

from collections.abc import Callable

from .models import Citation, RAGAnswer
from .prompting import SAFETY_NOTICE, build_answer_prompt
from .retriever import CitationAwareRetriever


class LegalRAGService:
    """Orchestrates cited retrieval and safe answer creation.

    The LLM callback is injected by the backend owner so this module remains
    testable and does not depend on one model provider.
    """

    def __init__(self, retriever: CitationAwareRetriever, generate: Callable[[str], str]) -> None:
        self.retriever = retriever
        self.generate = generate

    def answer(self, question: str, *, state: str | None, domain: str | None, language: str = "en") -> RAGAnswer:
        passages = self.retriever.search(question, state=state, domain=domain)
        citations = [Citation(label=passage.citation_label, url=passage.source_url, chunk_id=passage.chunk_id) for passage in passages]
        if not passages:
            return RAGAnswer(
                answer="I could not find enough verified official material for this question. Please choose a state and domain, or provide more details.",
                language=language,
                citations=[],
                sufficient_evidence=False,
                safety_notice=SAFETY_NOTICE,
            )
        prompt = build_answer_prompt(question, passages, language)
        return RAGAnswer(
            answer=self.generate(prompt),
            language=language,
            citations=citations,
            sufficient_evidence=True,
            safety_notice=SAFETY_NOTICE,
        )
