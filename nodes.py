from packages import *
from backend import *
 
class AgentState(BaseModel):
    query: str
    valid: Optional[bool] = None
    answer: Optional[str] = None
    similar_query: Optional[bool] = None
    scraped_pages: Optional[List[str]] = Field(default_factory=list)



@traceable
def validity_checker(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Is the user's input a real search-worthy question? Answer only 'yes' or 'no'."),
        ("user", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"query": state.query}).strip().lower()
    
    if "yes" in result:
        return state.model_copy(update={"valid": True})
    else:
        return state.model_copy(update={"valid": False, "answer": "Please rephrase your query as a meaningful question."})
    



@traceable
def memory_search_node(state: AgentState) -> AgentState:
    response = retrieve_similar_response(str(state.query))
    if response is not None:
        # Update answer and mark as found from memory
        return state.model_copy(update={
            "answer": response,
            "similar_query": True
        })

    # Indicate no similar query was found in memory
    return  state.model_copy(update={
                "answer": None,
                "similar_query": False
            })


@traceable
def web_scraper_node(state: AgentState) -> AgentState:
    pages = scrape_top_results(str(state.query))
    return state.model_copy(update={"scraped_pages": pages})


@traceable
def summarizer_node(state: AgentState) -> AgentState:
    summary = summarize_content(state.scraped_pages, state.query)
    return state.model_copy(update={"answer": summary})



@traceable
def memory_store_node(state: AgentState) -> AgentState:
     store_query_response(state.query, state.answer)
     return state



@traceable
def final_answer(state: AgentState) -> AgentState:
    return state



@traceable
def final_invalid(state: AgentState) -> AgentState:
    return state