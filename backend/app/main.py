from fastapi import FastAPI

app = FastAPI(title="Regional Language Legal RAG")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
