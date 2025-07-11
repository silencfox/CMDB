import os
import hashlib
import sqlite3
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings  # ✅ Usa el paquete actualizado
from langchain.text_splitter import RecursiveCharacterTextSplitter
import markdown
from bs4 import BeautifulSoup
import os

# ⚡ Configuración de embeddings y vector store
embedding = OllamaEmbeddings(model="mistral", base_url="http://ollama:11434")
#embedding = OllamaEmbeddings(model="nomic-embed-text", base_url="http://ollama:11434")

db = Chroma(persist_directory="/chroma", embedding_function=embedding)

DATA_PATH = "./documents"

# ⚡ Configura SQLite DB para controlar duplicados
conn = sqlite3.connect('ingesta.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS documentos (
        hash TEXT PRIMARY KEY,
        filename TEXT,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def markdown_to_text(md_content):
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()
    
def file_hash(filepath):
    """Calcula hash SHA256 de un archivo completo."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

docs = []

# 🔄 Procesamiento de archivos
for filename in os.listdir(DATA_PATH):
    filepath = os.path.join(DATA_PATH, filename)
    print(f"📄 Procesando archivo: {filepath}")

    hash_value = file_hash(filepath)

    # ✅ Verifica si ya existe el hash en la DB
    c.execute("SELECT * FROM documentos WHERE hash=?", (hash_value,))
    if c.fetchone():
        print(f"⚠️  Archivo {filename} ya indexado. Omitiendo.")
        continue

    # 🔍 Cargar el documento según extensión
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(filepath)
    elif filename.endswith(".txt"):
        loader = TextLoader(filepath)
    elif filename.endswith(".md"):
        print(f"🔍 Leyendo archivo markdown: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()

        print(f"📏 Longitud del contenido MD original: {len(md_content)}")

        text_content = markdown_to_text(md_content)
        print(f"📏 Longitud del texto parseado: {len(text_content)}")

        root, ext = os.path.splitext(filepath)
        # Crear la nueva ruta con extensión .txt
        temp_txt = root + '.txt'
        #temp_txt = filepath + ".tmp.txt"
        with open(temp_txt, "w", encoding="utf-8") as f:
            f.write(text_content)

        print(f"✅ Archivo temporal creado: {temp_txt}")

        loader = TextLoader(temp_txt)
        #loaded_docs = list(loader.load())  # ⚠️ Forzamos la carga antes de eliminar

        print(f"✅ Archivo temporal procesado correctamente: {temp_txt}")
        #print(f"🔢 Total de documentos cargados desde temp: {len(loaded_docs)}")

        #if os.path.exists(temp_txt):
            #os.remove(temp_txt)
            #print(f"🗑️ Archivo temporal eliminado: {temp_txt}")
        #else:
        #    print(f"⚠️ Archivo temporal no encontrado al intentar eliminar: {temp_txt}")
            
        os.remove(filepath)
    else:
        print(f"❌ Tipo de archivo no soportado: {filename}")
        continue

    loaded_docs = loader.load()

    
    print(f"✅ {len(loaded_docs)} documentos cargados de {filename}")

    # 🔗 Agrega metadata con el hash
    for doc in loaded_docs:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata['source_hash'] = hash_value

    docs.extend(loaded_docs)

print(f"🔢 Total de documentos cargados: {len(docs)}")

# 🔎 Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)
print(f"🔢 Total de chunks creados: {len(split_docs)}")

# ✅ Agregar chunks a ChromaDB si hay nuevos documentos
if split_docs:
    db.add_documents(split_docs)
    print(f"🎉 {len(split_docs)} chunks añadidos al vector store.")

    # 🔧 Guarda en DB de control los hashes de archivos procesados
    for doc in docs:
        source_hash = doc.metadata.get('source_hash')
        filename = doc.metadata.get('source', 'unknown')
        c.execute("INSERT OR IGNORE INTO documentos (hash, filename) VALUES (?, ?)", (source_hash, filename))
    conn.commit()
else:
    print("⚠️  No se crearon chunks nuevos. Ningún documento añadido al vector store.")

# 🔒 Cierra conexión SQLite
conn.close()
print("✅ Ingesta completada y base de datos cerrada.")
