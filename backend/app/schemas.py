# backend/app/schemas.py
# Structured Pydantic model for OpenAI that guarantees perfect JSON every time

from pydantic import BaseModel
from typing import List

# this is the structured output I want from the LLM for the analysis endpoint
class AnalysisResult(BaseModel):
    found_skills: List[str]
    missing_skills: List[str]
    experience_match: int          # 0-100 from LLM
    keyword_match: int             # 0-100 from LLM
    suggested_edits: List[str]