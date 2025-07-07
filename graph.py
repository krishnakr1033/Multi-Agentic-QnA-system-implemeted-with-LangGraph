from packages import *
from nodes import *

builder = StateGraph(AgentState)

builder.add_node("ValidityChecker", validity_checker)
builder.add_node("MemorySearch", memory_search_node)
builder.add_node("WebScraper", web_scraper_node)
builder.add_node("Summarizer", summarizer_node)
builder.add_node("MemoryStore", memory_store_node)
builder.add_node("FinalAnswer", final_answer)
builder.add_node("FinalInvalid", final_invalid)

builder.add_edge(START,"ValidityChecker")

builder.add_conditional_edges(
    "ValidityChecker",
    lambda s: s.valid,
    {True: "MemorySearch", False: "FinalInvalid"}
)

builder.add_conditional_edges(
    "MemorySearch",
    lambda s: s.similar_query,
    {True: "FinalAnswer", False: "WebScraper"}
)
builder.add_edge("WebScraper", "Summarizer")
builder.add_edge("Summarizer", "MemoryStore")
builder.add_edge("MemoryStore", "FinalAnswer")
builder.add_edge("FinalAnswer",END)
builder.add_edge("FinalInvalid",END)
