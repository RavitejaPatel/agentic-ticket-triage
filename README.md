Here's your README — paste this into `README.md` in your project root (replace the placeholder auto-generated one from repo creation).

```markdown
# Agentic AI Ticket Triage

A multi-agent AI system that automatically classifies, researches, drafts replies to, and routes customer support tickets — built to explore agentic AI architecture patterns (multi-agent orchestration, RAG, human-in-the-loop routing) end-to-end on real cloud infrastructure.

## What it does

Given a raw support ticket, the system:
1. **Classifies** it by category and priority (LLM-based)
2. **Retrieves** relevant knowledge base content using semantic search (RAG)
3. **Drafts** a policy-grounded reply using the retrieved context
4. **Routes** the ticket to auto-send or human escalation, based on deterministic business rules

Each step is an independent agent, orchestrated as a LangGraph workflow, exposed via a FastAPI endpoint, and demoed through a Streamlit UI.

## Architecture

```
Ticket in (Streamlit / API / replay script)
        │
        ▼
   [Classifier] ── category + priority (LLM)
        │
        ▼
   [Retriever] ── relevant KB docs (FAISS + Bedrock Titan Embeddings)
        │
        ▼
   [Responder] ── grounded reply draft (LLM)
        │
        ▼
   [Router] ── auto-send or escalate (rule-based, deterministic)
        │
        ▼
     Result + logged to logs/ticket_log.jsonl
```

## Tech stack

| Component | Choice | Why |
|---|---|---|
| LLM | AWS Bedrock (Amazon Nova Micro) | Provider-agnostic client also supports Azure OpenAI as a fallback |
| Orchestration | LangGraph | Explicit state graph across classify → retrieve → respond → route |
| Embeddings + vector search | Bedrock Titan Embeddings + FAISS | RAG retrieval without local ML dependencies |
| API | FastAPI | HTTP interface for ticket submission |
| Demo UI | Streamlit | Live, interactive demo |
| Language | Python | — |

## Design decisions worth noting

- **Routing is rule-based, not LLM-based.** Auto-send/escalate decisions need to be predictable and auditable — this is deliberately deterministic code, not model judgment, since you don't want escalation behavior to vary unpredictably.
- **LLM provider is swappable via one environment variable** (`LLM_PROVIDER=azure|bedrock`), behind a single `call_llm()` interface — built this way after hitting real deployment/quota constraints on Azure OpenAI mid-project, and needing a same-day fallback.
- **FAISS index is rebuilt in memory on startup**, not persisted to disk. At this KB scale (a handful of docs) that's effectively free; at production scale, this would move to `faiss.write_index()`/`read_index()` to avoid re-embedding on every restart.

## Setup

```bash
git clone <your-repo-url>
cd agentic-ticket-triage
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your AWS/Azure credentials
```

## Running it

**API server:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Demo UI:**
```bash
streamlit run frontend/streamlit_app.py
```

**Replay real tickets from a dataset:**
```bash
python3 scripts/replay.py
```

**Analyze logged results:**
```bash
python3 scripts/analyze_logs.py
```

## Results (tested against 45 real tickets from a public customer support dataset)

- **Category classification**: 95.6% of tickets classified as "technical," consistent with the dataset's actual product-support nature (electronics/software issues)
- **Routing distribution**: 51% escalated for human review, 49% auto-sent — a reasonable split for a system that deliberately escalates high-priority and billing-related tickets
- **Note on priority evaluation**: the dataset's own priority labels showed no consistent correlation with ticket content (urgent-sounding tickets labeled "low," generic tickets labeled "high"), suggesting these labels are synthetic rather than human-judged ground truth. Rather than report a misleading agreement percentage against them, this was identified and excluded as a metric — a legitimate finding in itself when validating against real-world data.

## Possible next steps

- Persist the FAISS index instead of rebuilding on every run
- Move from root AWS credentials to a scoped IAM user/role
- Containerize and deploy to Azure Container Apps / AWS Lambda
- Expand the KB and re-evaluate retrieval precision at scale
```