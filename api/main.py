from fastapi import FastAPI
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

app = FastAPI()

# Configurar embeddings y vector store
embedding = OllamaEmbeddings(model="mistral", base_url="http://ollama:11434")
vectordb = Chroma(persist_directory="/chroma", embedding_function=embedding)

# Configurar LLM
llm = Ollama(model="mistral", base_url="http://ollama:11434")

# Crear cadena RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever()
)

@app.get("/")
def read_root():
    return {"message": "Knowledge Base API is running"}

@app.post("/ask")
def ask_question(question: str):
    result = qa.run(question)
    return {"answer": result}
