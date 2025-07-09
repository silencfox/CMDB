from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

embedding = OllamaEmbeddings(model="mistral", base_url="http://ollama:11434")

DATA_PATH = "./documents"
docs = []

for filename in os.listdir(DATA_PATH):
    filepath = os.path.join(DATA_PATH, filename)
    print(f"Processing file: {filepath}")

    if filename.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(filepath)
    elif filename.endswith(".txt"):
        loader = TextLoader(filepath)
    else:
        print(f"Unsupported file type: {filename}")
        continue

    loaded_docs = loader.load()
    print(f"Loaded {len(loaded_docs)} documents from {filename}")
    docs.extend(loaded_docs)

print(f"Total documents loaded: {len(docs)}")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)
print(f"Total chunks created: {len(split_docs)}")

# Load existing DB and add new documents
db = Chroma(persist_directory="/chroma", embedding_function=embedding)
db.add_documents(split_docs)

print(f"{len(split_docs)} chunks added to vector store.")
