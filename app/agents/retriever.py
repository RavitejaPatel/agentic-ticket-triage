from app.vector_store import load_kb_documents, build_index, search

_docs = load_kb_documents()
_index, _docs = build_index(_docs)


def retrieve_context(ticket_text: str, top_k: int = 2) -> list:
    return search(ticket_text, _index, _docs, top_k=top_k)


if __name__ == "__main__":
    test_ticket = "My subscription was charged twice this month, please refund the extra charge."
    results = retrieve_context(test_ticket)
    for r in results:
        print(f"--- {r['source']} ---")
        print(r["text"][:150])
        print()