from fastapi import FastAPI
from pydantic import BaseModel

from app.graph import run_pipeline

app = FastAPI(title="Agentic Ticket Triage")


class TicketRequest(BaseModel):
    ticket_text: str


@app.post("/submit-ticket")
def submit_ticket(request: TicketRequest):
    result = run_pipeline(request.ticket_text)
    return {
        "classification": result["classification"],
        "retrieved_docs": [d["source"] for d in result["retrieved_docs"]],
        "draft_reply": result["draft_reply"],
        "routing_decision": result["routing_decision"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}