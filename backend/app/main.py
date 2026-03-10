# backend/app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routes import analyze, rewrite

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ResumeMatch AI")

app.include_router(analyze.router)
app.include_router(rewrite.router)

@app.get("/")
def health():
    return {"status": "ok", "message": "ResumeMatch AI running with structured AI outputs 🚀"}