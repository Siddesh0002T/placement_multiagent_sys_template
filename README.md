<div align="center">

# 🎓 Placement Agent

**A 4-agent career-prep system built on Google's Agent Development Kit (ADK)**

![Python](https://img.shields.io/badge/python-3.11-3776AB?logo=python&logoColor=white)
![Google ADK](https://img.shields.io/badge/Google%20ADK-2.8.0-4285F4?logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/model-gemini--flash--lite--latest-8E44AD)

</div>

---

## Table of Contents

- [Clone the Repo](#clone-the-repo)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Deploy to GCP (Vertex AI Agent Engine)](#deploy-to-gcp-vertex-ai-agent-engine)
- [Troubleshooting](#troubleshooting)

---

## Clone the Repo

```bash
git clone https://github.com/voidgremlin19/placement_multiagent_system.git
cd placement_multiagent_system
```

---

## Prerequisites

- **Python 3.11+**
- A **Google AI Studio API key** — free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- [`uv`](https://github.com/astral-sh/uv) (recommended) or plain `pip`

---

## Setup

**1. Create and activate a virtual environment**

```bash
uv venv
source .venv/bin/activate
```

**2. Install dependencies**

```bash
uv pip install -r requirements.txt
```

<details>
<summary>Using plain pip instead</summary>

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

</details>

**3. Configure your API key**

```bash
cp .env.example .env
```

Open `.env` and paste your key:

```dotenv
GOOGLE_API_KEY="AIza..."
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

**4. Verify the install**

```bash
python -c "from placement_agent.coordinator import root_agent; print(root_agent.name, 'OK')"
```

You should see `placement_coordinator OK`.

---

## Running the Project

Everything runs through ADK's own CLI, pointed at the project root (where `agent.py` lives).

### `adk web .` — dev console (recommended)

```bash
adk web --port 8001 .
```

Open **http://127.0.0.1:8001** — chat UI, event/trace inspector, and an agent-graph view.

### `adk run .` — terminal chat

```bash
adk run .
```

A plain terminal conversation against `root_agent`, no browser needed.

### `adk api_server .` — REST API

```bash
adk api_server --port 8000 .
```

Exposes the same agent graph as a REST API (session creation + `/run`/`/run_sse` endpoints).

> All three commands run the exact same `root_agent` defined in `agent.py`. Run more than one at once, on different ports — they don't conflict.

### Parsing a resume file (PDF/DOCX/TXT)

Resume parsing isn't wired up as an in-chat upload — run it yourself first, then paste the printed text into the chat:

```bash
python -c "
from placement_agent.tools.resume_parser import extract_resume_text
with open('resume.pdf', 'rb') as f:
    print(extract_resume_text(f.read(), 'resume.pdf'))
"
```

---

## Deploy to GCP (Vertex AI Agent Engine)

Deploys the same `placement_coordinator` agent graph to Vertex AI Agent Engine — Google's managed, serverless runtime for ADK agents.

### Prerequisites

- A GCP project with **billing enabled**
- The Vertex AI API enabled: `gcloud services enable aiplatform.googleapis.com`
- Application Default Credentials: `gcloud auth application-default login`
- A Cloud Storage bucket in the same project/region:
  ```bash
  gcloud storage buckets create gs://YOUR_BUCKET_NAME --location=us-central1
  ```

### Setup

```bash
uv pip install "google-cloud-aiplatform[adk,agent_engines]"
```

In `.env`, set:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_CLOUD_STAGING_BUCKET="your-bucket-name"
```

### Deploy

```bash
python deploy/deploy_agent_engine.py
```

On success it prints a resource name — paste it into `.env` as `AGENT_ENGINE_RESOURCE_NAME`.

### Test the deployment

```bash
python deploy/query_agent_engine.py
```

A terminal chat against the *deployed* agent (not your local one).

### Delete it when you're done

```bash
python deploy/delete_agent_engine.py
```

**Agent Engine bills for model calls and management overhead even when idle.** Delete the resource after testing rather than leaving it deployed indefinitely.

---

## Troubleshooting

<details>
<summary><b>Error: <code>GOOGLE_API_KEY environment variable is not set</code></b></summary>

You haven't created `.env`, or it's empty. Run `cp .env.example .env` and paste your key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

</details>

<details>
<summary><b>Error: <code>404 NOT_FOUND ... no longer available to new users</code></b></summary>

You changed `MODEL_NAME` in `placement_agent/config.py` to a retired model (e.g. `gemini-2.5-flash`). This is a Google account-level block, not a bug. Set `MODEL_NAME` back to `gemini-flash-lite-latest`.

</details>

<details>
<summary><b>Error: <code>429 RESOURCE_EXHAUSTED ... generate_content_free_tier_requests</code></b></summary>

You've hit the free-tier daily request cap for the model. Options:
1. Wait for the quota to reset (resets at midnight Pacific time)
2. Enable billing on your AI Studio project for higher limits
3. Keep `MODEL_NAME` on a lite model, which has a higher free-tier ceiling than flagship models

</details>

<details>
<summary><b><code>adk</code>: command not found</b></summary>

The `adk` CLI ships with the `google-adk` package and lands on your `PATH` once your virtualenv is activated (`source .venv/bin/activate`). If it's still missing, reinstall with `uv pip install google-adk` inside the active venv.

</details>

<details>
<summary><b>IDE shows "Cannot find module google.adk.agents"</b></summary>

Your editor's language server is pointed at a different Python interpreter than this project's `.venv`. Point your IDE's interpreter at `.venv/bin/python` — it doesn't affect actually running the project.

</details>
