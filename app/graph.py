from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.agents.classifier import classify_ticket
from app.agents.retriever import retrieve_context
from app.agents.responder import draft_reply
from app.agents.router import route_ticket


class TicketState(TypedDict):
    ticket_text: str
    classification: dict
    retrieved_docs: list
    draft_reply: str
    routing_decision: dict


def classify_node(state: TicketState) -> dict:
    classification = classify_ticket(state["ticket_text"])
    return {"classification": classification}


def retrieve_node(state: TicketState) -> dict:
    docs = retrieve_context(state["ticket_text"])
    return {"retrieved_docs": docs}


def respond_node(state: TicketState) -> dict:
    reply = draft_reply(state["ticket_text"], state["retrieved_docs"])
    return {"draft_reply": reply}


def route_node(state: TicketState) -> dict:
    decision = route_ticket(state["classification"])
    return {"routing_decision": decision}


def build_graph():
    workflow = StateGraph(TicketState)

    workflow.add_node("classify", classify_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("respond", respond_node)
    workflow.add_node("route", route_node)

    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "respond")
    workflow.add_edge("respond", "route")
    workflow.add_edge("route", END)

    return workflow.compile()


_graph = build_graph()


def run_pipeline(ticket_text: str) -> dict:
    result = _graph.invoke({"ticket_text": ticket_text})
    return result


if __name__ == "__main__":
    test_ticket = "how to connect to my VM."
    result = run_pipeline(test_ticket)
    print("-----------------------------------------------------------------------------")
    print("Classification:", result["classification"])
    print("-----------------------------------------------------------------------------")
    print("Routing decision:", result["routing_decision"])
    print("-----------------------------------------------------------------------------")
    print("\nDraft reply:\n", result["draft_reply"])
    print("-----------------------------------------------------------------------------")