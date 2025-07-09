# CMDB

docker compose up --build -d
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama list

#docker exec -it ollama ollama pull llama3
##  embedding = OllamaEmbeddings(model="llama3", base_url="http://ollama:11434")

docker exec -it knowledge_api python ingest.py

curl -X POST "http://localhost:8001/ask" -H "Content-Type: application/json" -d "{\"question\":\"¿Cuál es el procedimiento de instalación?\"}"