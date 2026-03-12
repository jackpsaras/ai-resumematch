# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import analyze, rewrite

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ResumeMatch AI")

# Configure CORS with explicit settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5175", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(rewrite.router)

@app.get("/")
def health():
    return {"status": "ok", "message": "ResumeMatch AI running with structured AI outputs 🚀"}