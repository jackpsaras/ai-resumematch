# backend/app/routes/rewrite.py
from fastapi import APIRouter, Body
from ..services.llm import rewrite_bullet

router = APIRouter(prefix="/rewrite", tags=["Rewrite"])

# endpoint to rewrite a single bullet point from a resume to better match the job description. 
# Accepts the original bullet and the job description, returns a rewritten bullet that is optimized for the job
@router.post("/")
async def rewrite_bullet_endpoint(data: dict = Body(...)):
    return await rewrite_bullet(data["bullet"], data["job_description"])