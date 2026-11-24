# System Architecture

User input flows through the frontend to the FastAPI backend. The backend routes the query by state and legal domain, retrieves dated official passages from the vector store, and generates a cited answer. Uploaded documents pass through OCR and fact extraction; the user confirms the facts before they can be used in an answer or draft.

Core safeguards are source citations, state/domain metadata, missing-evidence notices, user confirmation of extracted facts, and deadline calculations only when an official rule and trigger date are verified.
