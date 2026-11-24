# Regional Language Legal RAG

An evidence-aware legal-information assistant for regional-language users. The first version focuses on one state and legal domain, retrieves official passages, extracts user-confirmed facts from uploaded documents, and provides cited explanations and reviewable drafts.

## Project structure

- `backend/` - FastAPI services and the RAG pipeline
- `frontend/` - user interface application
- `data/` - local development data folders; source material is not committed
- `docs/` - architecture and project documentation
- `scripts/` - ingestion and maintenance utilities
- `tests/` - automated tests

## Start here

1. Create a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set local values.
4. Run `uvicorn backend.app.main:app --reload`.
