from fastapi import FastAPI

from app.llm import get_llm_provider

app = FastAPI()


@app.get("/")
def index():
    return {"details": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/llm/ping")
def llm_ping():
    provider = get_llm_provider()
    response = provider.invoke("Reply with exactly: pong")
    return {"response": response}
