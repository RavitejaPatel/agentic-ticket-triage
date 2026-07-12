import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.graph import run_pipeline

st.set_page_config(page_title="Agentic Ticket Triage", page_icon="🎫", layout="centered")

st.title("Agentic AI ticket triage")
st.caption("Multi-agent pipeline: classify → retrieve → draft → route")

ticket_text = st.text_area(
    "Paste a support ticket",
    placeholder="e.g. My subscription was charged twice this month, please refund the extra charge.",
    height=100,
)

if st.button("Submit ticket", type="primary"):
    if not ticket_text.strip():
        st.warning("Enter a ticket first.")
    else:
        with st.spinner("Agent pipeline running..."):
            result = run_pipeline(ticket_text)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Classification")
            st.json(result["classification"])
        with col2:
            st.subheader("Routing decision")
            action = result["routing_decision"]["action"]
            if action == "escalate":
                st.error(f"🚩 {action.upper()}")
            else:
                st.success(f"✅ {action.upper()}")
            st.caption(result["routing_decision"]["reason"])

        st.subheader("Retrieved knowledge base context")
        for doc in result["retrieved_docs"]:
            st.text(f"📄 {doc['source']}")

        st.subheader("Drafted reply")
        st.write(result["draft_reply"])