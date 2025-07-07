from packages import *
load_dotenv() 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# making a vectorstore db using LangChain
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    encode_kwargs={"normalize_embeddings": True}  # enables cosine sim
)

embedding_dim = len(embeddings.embed_query("hello world"))

index = faiss.IndexFlatIP(embedding_dim)
vectorstore = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)


def store_query_response(query: str, response: str):
     vectorstore.add_texts([query], metadatas=[{"response": response}])

def retrieve_similar_response(query: str, threshold: float = 0.8) -> Optional[str]:
    results =  vectorstore.similarity_search_with_score(query, k=1)
    if results and results[0][1] >= (threshold):  # FAISS uses L2 distance, so higher score = less similar
        return results[0][0].metadata["response"]
    return None

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    api_key= GROQ_API_KEY
    # other params...
)


search_tool = GoogleSearchAPIWrapper()

def scrape_top_results(query: str, max_results: int = 5) -> List[str]:
    """
    Returns top result snippets (descriptions) from GoogleSearchAPIWrapper.
    This avoids full scraping and just uses API summaries.
    """
    search_results = search_tool.results(query, max_results)
    
    descriptions = []
    for result in search_results:
        if "snippet" in result:
            descriptions.append(result["snippet"])
        if len(descriptions) >= max_results:
            break

    return descriptions


def summarize_content(contents: list[str], query: str) -> str:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = [Document(page_content=chunk) for content in contents for chunk in splitter.split_text(content)]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize the content below to answer the query: {query}"),
        ("user", "{doc}")
    ])

    summary = ""
    for doc in docs:
        response = llm(prompt.format_messages(query=query, doc=doc.page_content))
        summary += response.content.strip() + "\n"
    return summary.strip()


def store_query_response(query: str, response: str):
    """
    Store a query and its corresponding response into the in-memory vectorstore.
    This allows the system to retrieve this response in future if a similar query is asked.

    Args:
        query (str): The user's original query.
        response (str): The response generated for the query (e.g., summarized web result).
    """
    vectorstore.add_texts([query], metadatas=[{"response": response}])