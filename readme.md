# 🔍 AI-Powered Job Scraper & Auto-Applier

This project automates the process of finding AI-related jobs on job portal and applying to them using browser automation and LLM-based reasoning agents.

---

## 📂 Project Structure

```
.
├── agents/
│   ├── job_application_agent.py    # Automatically applies to jobs
│   ├── similar_job_agent.py        # Scrapes job portal for job listings
│   ├── config.py                   # Stores constants like resume path, user details
│   ├── utils.py                    # Utility functions for reading/writing files
├── job_results/                    # Stores job scraping results (.json/.md)
├── api.py                          # FastAPI interface to trigger scraping and applications
├── .env                            # Secrets and API keys (excluded from Git)
└── .gitignore                      # Ignores env, cache, results, etc.
```

---

## ⚙️ Features

### ✅ `similar_job_agent.py`
- Logs into job portal using a persistent browser session.
- Scrapes up to 4 relevant job postings (job roles for your location).
- Filters remote and non-sponsored jobs.
- Extracts structured data: title, company, location, summary, canonical job URL.
- Outputs results in both `.json` and `.md`.

### ✅ `job_application_agent.py`
- Loads saved job listings.
- Uses `browser-use` to apply to jobs via job portal.
- Auto-fills personal info and uploads resume.
- Tracks and logs application success/failure per job.

### ✅ `api.py`
- `POST /run-scraper`: Run the job scraper via API.
- `POST /apply-to-jobs`: Auto-apply to jobs using the saved JSON.

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file with:
```env
ANTHROPIC_API_KEY=your_claude_api_key
```

### 4. Run FastAPI server
```bash
uvicorn api:app --reload
```

### 5. (Optional) Run the scraper standalone
```bash
python agents/similar_job_agent.py
```

### 6. (Optional) Run auto-applier standalone
```bash
python agents/job_application_agent.py
```

---

## 📦 Example API Request (via cURL)

### 🔍 Job Scraper
```bash
curl -X POST http://localhost:8000/run-scraper   -H "Content-Type: application/json"   -d '{
    "skills": ["Python", "LLMs"],
    "job_roles": ["AI Engineer"],
    "summary": "Looking for AI jobs in USA",
    "industry": "Tech",
    "experience_level": "Mid-Senior"
}'
```

### 🧑‍💼 Auto Apply
```bash
curl -X POST "http://localhost:8000/apply-to-jobs?json_path=job_results/ljoportal_20250720_153000.json"
```

---

## 🧠 Tech Stack

- 🧠 LLMs: Claude 3.5 Sonnet (`ChatAnthropic`), GPT-4 (optional)
- 🌐 Automation: `browser-use` with Playwright
- 🖥️ Frontend (optional): Can be extended to React or Streamlit
- ⚙️ Backend: FastAPI
- 📦 Agentic Design: Modular `Agent + Task + Controller` logic

---

## 🛡️ Disclaimer

This project is intended for educational and personal use only. Automated job applications should be used responsibly and comply with platform terms of service.

---
