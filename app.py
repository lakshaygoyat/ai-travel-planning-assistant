from __future__ import annotations

import streamlit as st

from src.assistant import TravelAssistant

st.set_page_config(page_title="AI Travel Planning Assistant", page_icon="✈️", layout="wide")
st.title("✈️ AI Travel Planning Assistant")
st.caption("Singapore knowledge base + custom MCP weather and currency tools")


def render_evidence(trace: dict) -> None:
    sources = trace.get("knowledge_sources", [])
    if sources:
        links = [
            f"[{item['title']}]({item['url']})" if item.get("url") else item["title"]
            for item in sources
        ]
        st.markdown("**Knowledge sources:** " + " · ".join(links))
    tool_results = trace.get("mcp_results", {})
    providers = []
    for result in tool_results.values():
        if isinstance(result, dict) and result.get("provider"):
            provider = result["provider"]
            url = result.get("provider_url")
            providers.append(f"[{provider}]({url})" if url else provider)
    if providers:
        st.markdown("**Current-data providers (via MCP):** " + " · ".join(providers))

with st.sidebar:
    st.header("Try these questions")
    st.markdown(
        """
- What are the must-visit attractions in Singapore?
- What is the three-day weather forecast?
- Convert 50000 INR to SGD.
- Plan a three-day Singapore trip and adjust it to the weather forecast.
- I have a budget of 60000 INR. Convert it to SGD and suggest a cultural itinerary.
"""
    )
    st.info("Live weather and exchange-rate values are returned by our custom MCP server.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    @st.cache_resource(show_spinner="Loading BAAI/bge-m3 and the vector index...")
    def load_assistant() -> TravelAssistant:
        return TravelAssistant()

    assistant = load_assistant()
except Exception as exc:
    st.error(str(exc))
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("trace"):
            render_evidence(message["trace"])
            with st.expander("Evidence and execution trace"):
                st.json(message["trace"])

question = st.chat_input("Ask about a Singapore trip...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    history = [
        {"role": item["role"], "content": item["content"]}
        for item in st.session_state.messages[:-1]
    ]
    with st.chat_message("assistant"):
        with st.spinner("Retrieving evidence and selecting tools..."):
            try:
                response = assistant.ask(question, history)
                st.markdown(response.answer)
                render_evidence(response.trace)
                with st.expander("Evidence and execution trace"):
                    st.json(response.trace)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response.answer,
                        "trace": response.trace,
                    }
                )
            except Exception as exc:
                error = f"I could not complete the request: {type(exc).__name__}. Please try again."
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})
