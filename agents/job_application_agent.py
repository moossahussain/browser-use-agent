# agent/job_application_agent.py:

import asyncio
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatAnthropic
from agents.utils import load_json_file
from agents.config import *


async def apply_to_jobs(json_path: str = DEFAULT_JSON_PATH):
    try:
        job_data = load_json_file(json_path)
    except FileNotFoundError as e:
        print(f" {e}")
        return

    jobs = job_data.get("posts", [])
    if not jobs:
        print(" No job listings found in JSON.")
        return

    browser_session = BrowserSession(
        executable_path=BROWSER_EXECUTABLE,
        user_data_dir=USER_PROFILE_DIR
    )

    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    for job in jobs:
        job_url = job["job_url"]
        task = f"""
Go to the job URL: {job_url}


- Fill in the following details:
  - Name: {USER_NAME}
  - Email: {USER_EMAIL}
  - Phone: {USER_PHONE}
- Upload the resume file: `{RESUME_FILE}`
- Submit the application


After submitting:
- Capture whether submission was successful or failed.
- Log the status and the job title.
"""
        print(f" Applying to: {job['job_title']} at {job['company_name']}...")
        try:
            agent = Agent(task=task, llm=llm, browser_session=browser_session)
            result = await agent.run()
            print(" Result:", result.final_result())
        except Exception as e:
            print(f" Error applying to {job['job_title']}: {e}")

if __name__ == "__main__":
    asyncio.run(apply_to_jobs())  
