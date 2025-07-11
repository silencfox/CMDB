# CMDB

docker compose up --build -d
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull nomic-embed-text

docker exec -it ollama ollama list

#docker exec -it ollama ollama pull llama3				#
# embedding = OllamaEmbeddings(model="llama3", base_url="http://ollama:11434")

#docker exec -it ollama ollama pull nomic-embed-text	#Embeddings más rápido y eficientes que mistral
# embedding = OllamaEmbeddings(model="nomic-embed-text", base_url="http://ollama:11434")

docker exec -it knowledge_api python ingest.py


curl -X POST "http://localhost:8001/ask" -H "Content-Type: application/json" -d "{\"question\":\"¿Cuál es el procedimiento de instalación?\"}"


## eliminar chunks
#docker exec -it knowledge_api rm -rf /chroma/*

################
$response = Invoke-RestMethod -Method POST `
  -Uri 'http://localhost:8001/ask?question=Cual%20entidad%20bancaria%20de%20la%20Rep%C3%BAblica%20Dominicana%20se%20conoce%20como%20BSC' `
  -Headers @{ "accept" = "application/json" } `
  -Body ''

$response.answer
###################

& curl -X POST "http://localhost:8001/ask?question=Cual%20entidad%20bancaria%20de%20la%20Rep%C3%BAblica%20Dominicana%20se%20conoce%20como%20BSC" -H "accept: application/json" -d ""

Fast Api
http://localhost:8001/docs
http://localhost:8001/ask

gradio
http://localhost:7860

wiki
http://localhost:3000/a/dashboard

docker exec -it knowledge_api python ingest.py

docker exec -it knowledge_api python sync_wiki.py
docker exec -it knowledge_api python update_knowledge_base.py



ver la DB posgres

docker exec -it wikidb bash
psql -U wikijs -d wikijs
## ver tablas
\dt

\d pages
\q


##logo wiki
##https://static.requarks.io/logo/wikijs-butterfly.svg