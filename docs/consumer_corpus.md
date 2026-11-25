# Consumer Law Corpus

This corpus is generated from the five official PDFs listed in `data/manifests/official_consumer_sources.json`.

## Build

```bash
python scripts/build_consumer_corpus.py --target 250
```

The builder writes `data/processed/karnataka_consumer_official_corpus.jsonl`. Every record includes the official source URL, page number, document checksum, Act/rule name, Karnataka/consumer metadata, and a section hint where one can be detected.

## Quality gate

- Keep the target between 200 and 300 chunks.
- Index only these official source URLs or new approved government URLs.
- Preserve the original text; never translate or rewrite the stored legal passage.
- Keep Kannada explanations separate from the retrieved source passage.
