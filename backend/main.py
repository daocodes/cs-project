from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"details": "Hello from FastAPI"}


@app.get("/health")
def health():
    return {"ok": True}
