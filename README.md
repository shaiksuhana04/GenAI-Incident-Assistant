# GenAI-Powered Incident Assistant (MVP)

Small demo that uses an LLM to analyze logs, classify severity, and suggest remediation steps.
Good for SRE-focused resumes and interviews: demonstrates GenAI exposure, automation thinking, and observability.

## Features (MVP)
- Paste or upload logs
- LLM summarizes issues, suggests root causes and remediation steps
- Shows a CLI command snippet for diagnosis/mitigation
- Saves analysis history locally (for demo)

## Tech stack
- Python
- Streamlit (quick UI)
- OpenAI API (LLM for analysis)
- Docker (optional)

## Setup (local)
1. Clone repo
2. Create virtualenv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
