# backend/app/routes/analyze.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils.pdf_parser import extract_text_from_pdf
from ..services.llm import analyze_resume
from ..database import get_db
from ..crud import save_match_result

router = APIRouter(prefix="/analyze", tags=["Analyze"])

# endpoint to analyze a resume against a job description. Accepts PDF upload and job description text, 
# returns structured JSON with found/missing skills and a match score. 
# Also saves the result in the database for future reference.
router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("/")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    result = await analyze_resume(resume_text, job_description)
    save_match_result(db, resume.filename, job_description, result["match_score"])
    return result