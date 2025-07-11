import subprocess

# Descarga páginas de Wiki.js
subprocess.run(["python", "sql.py"])

# Ingesta en ChromaDB
subprocess.run(["python", "ingest.py"])

print("✅ Base de conocimiento actualizada con Wiki.js.")
