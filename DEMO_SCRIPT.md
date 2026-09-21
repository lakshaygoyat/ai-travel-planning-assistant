# Short demo video — 4 to 5 minutes

Use on-screen captions if the laptop microphone is unavailable. Keep browser zoom at 90%, VS Code Explorer open, and do not expose `.env` or the API key.

## 0:00–0:25 — Introduction

Show the README title and architecture diagram.

Caption / speech:

> This is an AI Travel Planning Assistant for Singapore. It combines a document-based RAG knowledge base with current weather and currency data exposed by a custom MCP server. The UI is Streamlit, orchestration is LangChain, embeddings use BAAI/bge-m3 with FAISS, and Gemini 2.5 Flash generates grounded responses.

## 0:25–0:55 — Code structure

Expand `knowledge_base`, `src`, `tests`, `app.py`, and `requirements.txt` in VS Code. Briefly open `src/build_index.py`, `src/mcp_server.py`, and `src/mcp_client.py`.

Caption / speech:

> The knowledge base contains four source-attributed documents. The indexing script chunks them, creates BGE-M3 embeddings and persists a FAISS index. This custom MCP server defines weather and currency tools; the MCP client discovers and calls them over standard input/output. No ready-made MCP server is used.

## 0:55–1:35 — RAG only

Ask: `What are the must-visit attractions in Singapore?`

Open **Evidence and execution trace**. Point to `use_rag: true`, both MCP flags `false`, and the source titles/URLs.

Caption / speech:

> This is a stable destination question, so only semantic retrieval is used. The answer is grounded in retrieved chunks, shows citations, and the trace proves that no live-data tool was called.

## 1:35–2:15 — MCP tools

Ask: `What is the forecast for the next three days?` Open the trace and show `get_singapore_weather` and the Open-Meteo result.

Then ask: `Convert 50000 INR to SGD.` Show `convert_currency`, rate date and provider.

Caption / speech:

> These requests need changing information. The router calls only the appropriate custom MCP tool. The returned provider, date and values are included in the response. Tool errors are passed to the model as errors, so the system does not fabricate live data.

## 2:15–3:15 — Combined RAG + MCP

Ask: `Plan a three-day Singapore itinerary for next week and adjust it according to the weather forecast.`

Show the day-wise response, rainy-day alternatives, citations and trace.

Caption / speech:

> This is the primary combined scenario. LangChain retrieves attractions, indoor and outdoor alternatives, itinerary patterns and transport guidance. The MCP server supplies a seven-day forecast. Gemini combines both evidence types into a weather-aware plan while labelling recommendations separately.

## 3:15–3:45 — Conversation context

Ask: `Make day two family-friendly and keep the indoor backup.`

Caption / speech:

> The application retains recent session messages, so the follow-up can refer to day two without repeating the original request.

## 3:45–4:20 — Setup and close

Show README quick-start commands and the acceptance checklist.

Caption / speech:

> Evaluators can reproduce the project with Python 3.12, install the requirements, add their Gemini key in a local dot-env file, build the index and run Streamlit. The repository excludes secrets and the generated index. This completes RAG, custom MCP, combined reasoning, citations, context and failure handling.

## Recording checklist

- Close email, Teams and notifications.
- Never open `.env`; only show `.env.example`.
- Pre-run the app once so the embedding model is cached.
- Use 1080p, show the cursor clearly, and cut waiting time.
- If silent, add each speech paragraph as a short title card/caption.
- Stop after 5 minutes; do not explain every file.
