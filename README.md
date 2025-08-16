# RAG-Application
Built a rag Gemini 2.5 Flash chatbot application in langchain framework monitoring llm invocations using Langsmith, LangGraph to compile retrieval and generation into single step. This project retrieves related queries from online blogsite.

# RAG Application typically has 2 stages.
1) Indexing: Data is ingested from source and indexing it.
2) retrieval and generation: The actual RAG chain takes user query and retrieves the relevant data from the index, then passes that to the model.

Indexing

1) Load: First we need to load our data. This is done with Document Loaders.

2) Split: Text splitters break large Documents into smaller chunks. This is useful both for indexing data and passing it into a model, as large chunks are harder to search over and won't fit in a model's finite context window.

3) Store:We need somewhere to store and index our splits, so that they can be searched over later. This is often done using a VectorStore and Embeddings model.

4) Retrieve: Given a user input, relevant splits are retrieved from storage using a Retriever.

5)Generate: A ChatModel / LLM produces an answer using a prompt that includes both the question with the retrieved data.
Detailed walkthrough code explained with comments
