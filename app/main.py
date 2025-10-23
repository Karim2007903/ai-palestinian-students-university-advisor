from fastapi import FastAPI

app = FastAPI(title="Palestinian Student Academic Guidance Agent", version="0.1.0")

@app.get("/")
def root():
    return {
        "name": "Palestinian Student Academic Guidance Agent",
        "version": "0.1.0",
        "status": "ok",
    }
