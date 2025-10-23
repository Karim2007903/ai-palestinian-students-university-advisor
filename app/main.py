from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Palestinian Student Academic Guidance Agent", version="0.1.0")
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "name": "Palestinian Student Academic Guidance Agent",
        "version": "0.1.0",
        "status": "ok",
    }
