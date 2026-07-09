def route_ticket(classification: dict) -> dict:
    """
    Decides whether to auto-send the drafted reply or escalate to a human.

    Simple rule-based routing (deliberately not LLM-based) — routing/escalation
    decisions should be predictable and auditable, not left to model judgment.
    """
    priority = classification.get("priority", "medium")
    category = classification.get("category", "general")

    if priority == "high":
        return {"action": "escalate", "reason": "High priority ticket requires human review"}

    if category == "billing":
        return {"action": "escalate", "reason": "Billing/financial tickets always reviewed by a human"}

    return {"action": "auto_send", "reason": "Low/medium priority, non-billing ticket"}


if __name__ == "__main__":
    test_cases = [
        {"category": "billing", "priority": "high"},
        {"category": "technical", "priority": "low"},
        {"category": "account", "priority": "medium"},
    ]
    for case in test_cases:
        print(case, "->", route_ticket(case))