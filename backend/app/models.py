from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime

class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String)
    job_title = Column(String)
    match_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)