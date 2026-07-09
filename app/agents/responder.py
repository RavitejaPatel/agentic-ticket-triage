from app.llm_client import call_llm

RESPOND_PROMPT = """You are a customer support agent. Write a short, professional reply to this ticket, using ONLY the policy context below. Do not invent information not present in the context.

Ticket: {ticket_text}

Relevant policy context:
{context}

Write a concise, empathetic reply (3-5 sentences)."""


def draft_reply(ticket_text: str, retrieved_docs: list) -> str:
    context = "\n\n".join(doc["text"] for doc in retrieved_docs)
    prompt = RESPOND_PROMPT.format(ticket_text=ticket_text, context=context)
    return call_llm(prompt, temperature=0.3)


if __name__ == "__main__":
    from app.agents.retriever import retrieve_context

    test_ticket = "My subscription was charged twice this month, please refund the extra charge."
    docs = retrieve_context(test_ticket)
    reply = draft_reply(test_ticket, docs)
    print("Draft reply:\n")
    print(reply)