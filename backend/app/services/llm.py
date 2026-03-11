# backend/app/services/llm.py
import os
import hashlib
import json
import redis.asyncio as redis
from openai import AsyncOpenAI
from dotenv import load_dotenv
from ..schemas import AnalysisResult

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
redis_client = redis.from_url("redis://localhost:6379")

async def analyze_resume(resume_text: str, job_description: str):
    cache_key = hashlib.md5((resume_text + job_description).encode()).hexdigest()
    cached = await redis_client.get(cache_key)
    if cached:
        return AnalysisResult(**json.loads(cached))
    # prompt engineering is key to getting good results from the LLM
    prompt = f"""
    You are an expert recruiter. Analyze this resume against the job description.

    Resume: {resume_text[:8000]}
    Job: {job_description}

    Return ONLY JSON matching this structure (no extra text):
    """

    # this is the structured output I want from the LLM for the analysis endpoint
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=AnalysisResult,
        temperature=0.2
    )

    result = response.choices[0].message.parsed

    # REAL weighted match score (this is what makes it high-ROI)
    skill_score = max(0, 100 - len(result.missing_skills) * 8)
    final_score = round(
        0.5 * skill_score +
        0.25 * result.experience_match +
        0.25 * result.keyword_match
    )

    full_result = result.model_dump()
    full_result["match_score"] = final_score

    await redis_client.setex(cache_key, 86400, json.dumps(full_result))
    return full_result