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

# main function to analyze a resume against a job description, returns a structured analysis including missing skills, experience match, keyword match, and an overall match score. Caches results in Redis for 24 hours to improve performance on repeated analyses.
async def analyze_resume(resume_text: str, job_description: str):
    cache_key = hashlib.md5((resume_text + job_description).encode()).hexdigest()
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    # promp should be concise to fit within token limits, but informative enough for the model to analyze effectively
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

    skill_score = max(0, 100 - len(result.missing_skills) * 8)
    final_score = round(0.5 * skill_score + 0.25 * result.experience_match + 0.25 * result.keyword_match)

    full_result = result.model_dump()
    full_result["match_score"] = final_score

    await redis_client.setex(cache_key, 86400, json.dumps(full_result))
    return full_result

# function to rewrite a single bullet point, can be used in the future for a resume optimization feature. Currently not integrated into the main flow, but can be called separately if needed.
async def rewrite_bullet(bullet: str, job_description: str):
    cache_key = hashlib.md5(f"rewrite:{bullet}:{job_description}".encode()).hexdigest()
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # prompt should be concise to fit within token limits, but informative enough for the model to generate relevant rewrites
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