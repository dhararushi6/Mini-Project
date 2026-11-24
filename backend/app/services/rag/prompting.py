from .models import RetrievedPassage


SAFETY_NOTICE = "This provides legal information from retrieved official sources, not legal advice. Verify important action with a qualified legal professional or official service."


def build_answer_prompt(question: str, passages: list[RetrievedPassage], language: str = "en") -> str:
    """Build a constrained prompt that does not permit unsupported legal claims."""
    evidence = "\n\n".join(
        f"[Source {index}] {passage.citation_label}\nURL: {passage.source_url}\nPassage: {passage.text}"
        for index, passage in enumerate(passages, start=1)
    )
    return f"""You are a legal-information assistant. Answer in {'Kannada' if language == 'kn' else 'English'}.

Rules:
- Use only the evidence passages below.
- Do not invent an Act, section, deadline, eligibility rule, procedure, or fact.
- If the evidence is insufficient, say exactly what information or official source is missing.
- Attach [Source n] to each material legal statement.
- Do not say that the user will win, must file a case, or has a guaranteed deadline.

User question: {question}

Evidence:
{evidence}
"""
