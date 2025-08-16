import getpass
import os
# set langsmith api key
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()

from langchain.chat_models import init_chat_model
# get gemini API Key
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("enter api key for google gemini: ")

llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai")

# get embeddings for the model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

# select vector store in this case(In-memory)
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# using specific website for answering questions RAG chain
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

# load the chunk contents of the blog
loader = WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
bs_kwargs = dict(parse_only = bs4.SoupStrainer(class_=("post-content","post-title","post-header")
)
),
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index chunks
_= vector_store.add_documents(documents = all_splits)

# define prompt for question answering
# api_url = "https://api.smith.langchain.com" in hub.pull
prompt = hub.pull("rlm/rag-prompt")

# Define state for application
class State(TypedDict):
    question: str 
    context: List[Document]
    answer: str 
# Define application steps
def retrieve(state:State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state:State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question":state["question"],"context":docs_content})
    response = llm.invoke(messages)
    return {"answer":response.content}

# compile the application and test
graph_builder = StateGraph(State).add_sequence([retrieve,generate])
graph_builder.add_edge(START,"retrieve")
graph = graph_builder.compile()

# print the response
response = graph.invoke({"question":"what is Task Decomposition?"})
print(response["answer"])


# print the second response
sec_response = graph.invoke({"question":"what is data science?"})
print(sec_response["answer"])

