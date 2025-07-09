from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
import os

# Configurar embeddings
embedding = OllamaEmbeddings(model="mistral", base_url="http://ollama:11434")

# Carpeta con tus documentos
DATA_PATH = "./documents"

docs = []

# Procesar cada archivo
for filename in os.listdir(DATA_PATH):
    filepath = os.path.join(DATA_PATH, filename)
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(filepath)
    elif filename.endswith(".txt"):
        loader = TextLoader(filepath)
    else:
        continue

    docs.extend(loader.load())

# Split en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)

# Guardar en ChromaDB
db = Chroma.from_documents(split_docs, embedding, persist_directory="/chroma")
db.persist()

print(f"{len(split_docs)} documents loaded and indexed.")
