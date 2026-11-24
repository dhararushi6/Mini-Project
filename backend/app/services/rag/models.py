from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class LegalChunk(BaseModel):
    """A small, citable passage from an official legal source."""

    id: str
    text: str = Field(min_length=1)
    source_title: str = Field(min_length=1)
    source_url: HttpUrl
    act_name: str | None = None
    section: str | None = None
    state: str | None = None
    domain: str | None = None
    effective_date: str | None = None

    def metadata(self) -> dict[str, str]:
        return {
            key: value
            for key, value in {
                "source_title": self.source_title,
                "source_url": str(self.source_url),
                "act_name": self.act_name,
                "section": self.section,
                "state": self.state,
                "domain": self.domain,
                "effective_date": self.effective_date,
            }.items()
            if value is not None
        }


class RetrievedPassage(BaseModel):
    chunk_id: str
    text: str
    source_title: str
    source_url: HttpUrl
    act_name: str | None = None
    section: str | None = None
    effective_date: str | None = None
    distance: float | None = None

    @property
    def citation_label(self) -> str:
        parts = [self.act_name or self.source_title]
        if self.section:
            parts.append(self.section)
        return ", ".join(parts)


class Citation(BaseModel):
    label: str
    url: HttpUrl
    chunk_id: str


class RAGAnswer(BaseModel):
    answer: str
    language: Literal["en", "kn"] = "en"
    citations: list[Citation] = []
    sufficient_evidence: bool
    safety_notice: str
