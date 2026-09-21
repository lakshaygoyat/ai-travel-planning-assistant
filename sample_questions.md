# Sample questions and expected behaviour

Live values are intentionally not hard-coded. Screenshots or copied outputs should be captured on the demo day.

| Question | Expected route | Expected evidence |
|---|---|---|
| What are the must-visit attractions in Singapore? | RAG | Retrieved chunks and source links; no MCP call |
| What is the forecast for the next three days? | MCP | `get_singapore_weather`; no destination retrieval |
| Convert 50000 INR to SGD. | MCP | `convert_currency` with current reference-rate date |
| Plan a three-day Singapore trip and adjust it according to the weather forecast. | RAG + MCP | Attractions, itinerary, transport chunks plus weather tool result |
| I have 60000 INR. Convert 60000 INR to SGD and suggest a cultural itinerary. | RAG + MCP | Cultural sources plus currency tool result |
| Make day two family-friendly instead. | Conversation + RAG | Previous itinerary preference retained in Streamlit session |

Failure demonstrations:

- Ask `Convert my budget to SGD` without an amount or source currency. The assistant must request missing values rather than inventing them.
- Disconnect the network and ask for weather. The MCP result must have `status: error`, and the assistant must state that it could not verify current weather.
