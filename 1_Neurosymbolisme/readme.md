## Prérequis

- python 3.13.15
- ollama
- neo4j
- numpy
- pandas
- matplotlib
- scipy
- Scikit-Learn


## Téléchargent de Ollama dans docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker ps
docker exec -it ollama ollama pull llama3.1 (3.3 Server)
docker exec -it ollama ollama list
docker exec -it ollama ollama run llama3.1



## Shemas et references
1. input.txt
   │
   ▼
2. Ollama extrait les faits
   │
   ▼
3. Neo4j stocke les relations
   │
   ▼
4. Ollama pose une question au graphe
   │
   ▼
5. Neo4j retourne les faits pertinents
   │
   ▼
6. Ollama génère une réponse
   │
   ▼
7. Neo4j vérifie symboliquement la relation
   │
   ▼
8. output.txt



docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/changez-moi -v neo4j_data:/data neo4j:2026.09.0

http://localhost:7474
Utilisateur : neo4j
Mot de passe : changez-moi



Commande
MATCH (head:Entity)-[relation]->(tail:Entity)
RETURN head, relation, tail;

MATCH (n)
DETACH DELETE n;




## References
https://www.aitooldiscovery.com/how-to/run-ollama-locally 
https://neo4j.com/docs/operations-manual/current/docker/introduction/
