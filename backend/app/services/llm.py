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

# core function that interacts with the LLM to analyze a resume against a job description, returning structured data about found/missing skills and a match score. Uses caching to speed up repeated analyses. This is the heart of the application and where most of the "magic" happens in terms of leveraging AI to provide value. The better this function is, the more impressive the app will be.
async def analyze_resume(resume_text: str, job_description: str):
    cache_key = hashlib.md5((resume_text + job_description).encode()).hexdigest()
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # prompt to the LLM to analyze the resume and job description, asking for a structured JSON output that matches the AnalysisResult schema. The prompt is designed to be clear and specific to get the best possible response from the LLM. The resume text is truncated to 8000 characters to fit within token limits while still providing enough context for analysis.
    prompt = f"""
    You are an expert recruiter. Analyze this resume against the job description.

    Resume: {resume_text[:8000]}
    Job: {job_description}

    Return ONLY JSON matching this structure (no extra text):
    """

    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=AnalysisResult,
        temperature=0.2
    )

    result = response.choices[0].message.parsed

    # REAL weighted match score (highest-ROI feature)
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

async def rewrite_bullet(bullet: str, job_description: str):
    cache_key = hashlib.md5(f"rewrite:{bullet}:{job_description}".encode()).hexdigest()
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    # prompt to rewrite a single bullet point to better match the job description, returning exactly 3 improved bullet points in a JSON array. This is a super high-ROI feature that can really boost the match score if the original bullet is weak. The LLM can add relevant keywords and rephrase for maximum impact.
    prompt = f"""
    You are an expert resume writer.
    Original bullet: {bullet}
    Target job: {job_description}
    Return ONLY a JSON array with exactly 3 improved bullet points.
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    rewrites = json.loads(response.choices[0].message.content)["rewrites"]
    await redis_client.setex(cache_key, 86400, json.dumps(rewrites))
    return rewrites