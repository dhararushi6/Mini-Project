# Arushi RAG Module

This module is responsible for reliable legal retrieval and source-linked answers.

## Rules

1. Index only verified official sources.
2. Attach source URL, Act/rule, section, state, domain, and effective-date metadata to each chunk.
3. Retrieve by state and domain before prompting the language model.
4. Do not generate an answer if no citable passage is retrieved.
5. Test English and Kannada queries separately and record Recall@k and citation coverage.

## Integration contract

Sindhu's backend can create `CitationAwareRetriever`, index `LegalChunk` objects, and inject an LLM function into `LegalRAGService`.
