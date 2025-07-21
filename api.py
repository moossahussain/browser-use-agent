from fastapi import FastAPI, Query
from pydantic import BaseModel
from agents.similar_job_agent import run_job_scraper
from agents.job_application_agent import apply_to_jobs
from typing import List, Optional

import asyncio

app = FastAPI()

class JobPost(BaseModel):
    job_title: str
    company_name: str
    location: str
    description: str
    job_url: str

class JobSearchResults(BaseModel):
    posts: list[JobPost]


class JobKeywordExtraction(BaseModel):
    skills: List[str]
    job_roles: List[str]
    summary: str
    industry: str
    experience_level: str


@app.post("/run-scraper", response_model=JobSearchResults)
async def run_scraper(input: JobKeywordExtraction):
    print(" Received input in run_scraper:", input.model_dump_json(indent=2))
    result = await run_job_scraper(input)
    if not result:
        return {"posts": []}
    return result


@app.post("/apply-to-jobs")
async def apply_jobs(json_path: Optional[str] = Query(default=None, description="Path to JSON file containing job posts")):
    try:
        await apply_to_jobs(json_path=json_path)
        return {"status": "success", "message": f"Job applications completed from: {json_path or 'DEFAULT_JSON_PATH'}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

