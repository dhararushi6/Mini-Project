"""Build a reproducible 200-300 chunk corpus from official consumer-law PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from pypdf import PdfReader

SOURCES = [
    {
        "id": "consumer_protection_act_2019",
        "title": "Consumer Protection Act, 2019",
        "url": "https://www.indiacode.nic.in/bitstream/123456789/12808/1/the_consumer_protection_act%2C_2019_no._35_of_2019_date_09.08.2019.pdf",
        "act_name": "Consumer Protection Act, 2019",
    },
    {
        "id": "consumer_commission_and_general_rules_2020",
        "title": "Consumer Protection Consumer Disputes Redressal Commissions Rules and General Rules, 2020",
        "url": "https://consumeraffairs.nic.in/sites/default/files/Consumer%20Commission%20Rules%20%26%20General%20Rules.pdf",
        "act_name": "Consumer Protection Rules, 2020",
    },
    {
        "id": "consumer_ecommerce_rules_2020",
        "title": "Consumer Protection E-Commerce Rules, 2020",
        "url": "https://consumeraffairs.nic.in/sites/default/files/E%20commerce%20rules.pdf",
        "act_name": "Consumer Protection E-Commerce Rules, 2020",
    },
    {
        "id": "consumer_mediation_rules_2020",
        "title": "Consumer Protection Mediation Rules, 2020",
        "url": "https://consumeraffairs.nic.in/sites/default/files/Mediation%20Rules.pdf",
        "act_name": "Consumer Protection Mediation Rules, 2020",
    },
    {
        "id": "consumer_ecommerce_amendment_2021",
        "title": "Consumer Protection E-Commerce Amendment Rules, 2021",
        "url": "https://consumeraffairs.nic.in/sites/default/files/Consumer%20Protection%20%28E-Commerce%29%20%28Amendment%29%20Rules%2C%202021.pdf",
        "act_name": "Consumer Protection E-Commerce Amendment Rules, 2021",
    },
]


def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "RegionalLegalRAG/0.1 educational project"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def looks_english(text: str) -> bool:
    letters = sum(ch.isascii() and ch.isalpha() for ch in text)
    return len(text) >= 180 and letters / max(len(text), 1) >= 0.35


def section_hint(text: str) -> str | None:
    match = re.match(r"^(\d{1,3}[A-Z]?)\.\s+([^\.]{3,100})", text)
    return f"Section {match.group(1)} - {match.group(2).strip()}" if match else None


def make_chunks(page_text: str, size: int = 800, overlap: int = 120) -> list[str]:
    text = normalise(page_text)
    if not looks_english(text):
        return []
    chunks = []
    cursor = 0
    while cursor < len(text):
        end = min(len(text), cursor + size)
        if end < len(text):
            boundary = text.rfind(". ", cursor + size // 2, end)
            if boundary > cursor:
                end = boundary + 1
        part = text[cursor:end].strip()
        if looks_english(part):
            chunks.append(part)
        if end >= len(text):
            break
        cursor = max(end - overlap, cursor + 1)
    return chunks


def extract_candidates() -> list[dict]:
    candidates: list[dict] = []
    for source in SOURCES:
        payload = download(source["url"])
        source_hash = hashlib.sha256(payload).hexdigest()
        reader = PdfReader(BytesIO(payload))
        for page_number, page in enumerate(reader.pages, start=1):
            for chunk_index, text in enumerate(make_chunks(page.extract_text() or ""), start=1):
                record_id = f"{source['id']}-p{page_number}-c{chunk_index}"
                candidates.append({
                    "id": record_id,
                    "text": text,
                    "source_title": source["title"],
                    "source_url": source["url"],
                    "act_name": source["act_name"],
                    "section": section_hint(text),
                    "state": "Karnataka",
                    "domain": "consumer",
                    "legal_scope": "central law applicable in Karnataka",
                    "page_number": page_number,
                    "source_sha256": source_hash,
                })
    return candidates


def balanced_sample(candidates: list[dict], target: int) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in candidates:
        grouped[item["source_title"]].append(item)
    chosen: list[dict] = []
    while len(chosen) < target and any(grouped.values()):
        for key in list(grouped):
            if grouped[key] and len(chosen) < target:
                chosen.append(grouped[key].pop(0))
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/processed/karnataka_consumer_official_corpus.jsonl")
    parser.add_argument("--target", type=int, default=250, choices=range(200, 301))
    args = parser.parse_args()
    records = balanced_sample(extract_candidates(), args.target)
    if len(records) < args.target:
        raise RuntimeError(f"Only extracted {len(records)} eligible English chunks; cannot meet target {args.target}.")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} citable chunks to {output}")


if __name__ == "__main__":
    main()

