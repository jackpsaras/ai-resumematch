# backend/app/crud.py
from sqlalchemy.orm import Session
from .models import MatchResult

# CRUD functions for database interactions. Currently just saving match results, but can be expanded in the future.
def save_match_result(db: Session, filename: str, job_title: str, score: float):
    db_result = MatchResult(resume_filename=filename, job_title=job_title[:100], match_score=score)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result