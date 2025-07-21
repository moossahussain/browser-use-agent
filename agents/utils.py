# agents/utils.py

import os
import json
from datetime import datetime
from pydantic import BaseModel
from typing import Union


def save_markdown_file(content: str, filename: str) -> str:
    os.makedirs("job_results", exist_ok=True)
    filepath = os.path.join("job_results", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f" Markdown saved: {filepath}")
    return filepath


def save_json_file(data: BaseModel, filename: str) -> str:
    os.makedirs("job_results", exist_ok=True)
    filepath = os.path.join("job_results", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data.model_dump(), f, indent=2, ensure_ascii=False)
    print(f" JSON saved: {filepath}")
    return filepath

def load_json_file(filepath: str) -> dict:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_markdown(data: Union[BaseModel, dict], metadata: dict = {}) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    posts = data.posts if isinstance(data, BaseModel) else data.get("posts", [])

    lines = [
        "#  Job Search Results",
        f"**Search Date:** {timestamp}",
        "**Search Queries:**",
        "- AI Engineer",
        "- GenAI Developer",
        "**Location:** Canada",
        f"**Total Jobs Found:** {len(posts)}",
        "\n---\n## Job Listings\n"
    ]

    for idx, job in enumerate(posts, start=1):
        lines.append(f"""{idx}. **{job.job_title}** – {job.company_name}  
*{job.location}*  
{job.description.strip()}  
[View Job Posting]({job.job_url})\n""")

    lines.append(f"---\n*Generated on {timestamp} by Browser-Use Agent*")
    return "\n".join(lines)


def log_error_markdown(error: Exception) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = f"""#   Job Search - Error Log

**Search Date:** {timestamp}  
**Status:** Failed

## Error Details

{str(error)}

---

*Generated on {timestamp} by Browser-Use Agent*
"""
    filename = f" _jobs_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    return save_markdown_file(content, filename)
