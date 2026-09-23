## Prérequis

- python 3.13.15
- numpy
- pandas
- matplotlib
- scipy
- Scikit-Learn
- ollama
- neo4j

## Telechargment de Ollama dans socker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker ps
docker exec -it ollama ollama pull llama3.1 (3.3 Server)
docker exec -it ollama ollama list
docker exec -it ollama ollama run llama3.1



## Shemas et references
main.py
   ↓
localhost:11434 (API)
   ↓
Conteneur Docker Ollama
   ↓
Modèle llama


docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/changez-moi -v neo4j_data:/data neo4j:2026.09.0

http://localhost:7474
Utilisateur : neo4j
Mot de passe : changez-moi


## References
https://www.aitooldiscovery.com/how-to/run-ollama-locally 
https://neo4j.com/docs/operations-manual/current/docker/introduction/
