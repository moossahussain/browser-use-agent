# agents/similar_job_agent.py

import os
import asyncio
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from browser_use import Agent, BrowserSession, Controller
from browser_use.llm import ChatOpenAI
from browser_use.llm import ChatAnthropic

from agents.utils import (
    save_markdown_file,
    save_json_file,
    format_markdown,
    log_error_markdown
)

# Load .env
load_dotenv()

# ----------------------------
# Data Models
# ----------------------------
class JobPost(BaseModel):
    job_title: str
    company_name: str
    location: str
    description: str
    job_url: str

class JobSearchResults(BaseModel):
    posts: List[JobPost]

class JobKeywordExtraction(BaseModel):
    skills: List[str]
    job_roles: List[str]
    summary: str
    industry: str
    experience_level: str

controller = Controller(output_model=JobSearchResults)

# ----------------------------
# Agent Logic
# ----------------------------
def get_task_prompt() -> str:
    return """
Objective:
Log in to LinkedIn using the default browser profile, perform job searches for --your role and location -- using direct URLs, and extract up to 4 relevant job postings in total.

Instructions:

1. Navigate to: --your job portal--
2. Log in using saved credentials from the browser's default profile.
3. Wait for the page to fully load.
4. search for --your job --
5. For each search:
   - Wait for job listings to appear.
   - Select up to 2 relevant job posts (total max: 4).
   - Only include jobs that are remote or located in --your location--.
   - Skip sponsored, duplicate, or expired listings.
6. For each selected job:
   - Click the job title to open the detailed job description.
   - Wait until the full detail panel or page loads.
   -  ** Extract the job URL *only after* the detail panel has fully loaded
   - Extract:
     - Job Title
     - Company Name
     - Location
     - A brief job description (~3 lines)
     - **Job URL (from the full job view after clicking into the job)**
7. Return the output as structured JSON using this format:
{
  "posts": [
    {
      "job_title": "AI Engineer",
      "company_name": "Microsoft",
      "location": "Toronto, ON",
      "description": "Lead development of AI systems using Azure cloud and LLMs.",
      "job_url": "https://www.linkedin.com/jobs/view/123456789"
    }
  ]
}
Return only the JSON result above so it can be parsed.
"""

async def run_job_scraper(input: JobKeywordExtraction) -> JobSearchResults | None:
    llm = ChatOpenAI(model="gpt-4.1")

    browser_session = BrowserSession(
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        user_data_dir='~/.config/browseruse/profiles/default'
    )
    agent = Agent(
        task=get_task_prompt(),
        llm=llm,
        browser_session=browser_session,
        controller=controller
    )
    result = await agent.run()
    if final := result.final_result():
        return JobSearchResults.model_validate_json(final)
    return None

# ----------------------------
# Entrypoint
# ----------------------------
async def main():
    try:
        result = await run_job_scraper()
        if result:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_markdown_file(format_markdown(result), f"linkedin_jobs_{timestamp}.md")
            save_json_file(result, f"linkedin_jobs_{timestamp}.json")
        else:
            print(" No structured result returned by agent.")
    except Exception as e:
        print(f" Agent execution failed: {e}")
        log_error_markdown(e)

if __name__ == "__main__":
    asyncio.run(main())
