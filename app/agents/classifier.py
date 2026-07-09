from app.llm_client import call_llm

CLASSIFY_PROMPT = """Classify this support ticket into a category and priority.

Ticket: {ticket_text}

Respond in exactly this format, nothing else:
category: <billing|technical|account|general>
priority: <low|medium|high>"""


def classify_ticket(ticket_text: str) -> dict:
    prompt = CLASSIFY_PROMPT.format(ticket_text=ticket_text)
    response = call_llm(prompt, temperature=0.0)
    result = {"category": "general", "priority": "medium"}
   
    for line in response.strip().splitlines():
        if line.lower().startswith("category:"):
            result["category"] = line.split(":", 1)[1].strip().lower()
        elif line.lower().startswith("priority:"):
            result["priority"] = line.split(":", 1)[1].strip().lower()
    return result
   


if __name__ == "__main__":
    test_ticket = "My subscription was charged twice this month, please refund the extra charge."
    print(classify_ticket(test_ticket))