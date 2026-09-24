import json
import ollama
from graph import Graph


class LLM:
    def __init__(
        self,
        model="llama3.1:latest",
        graph=None,
    ):
        self.model = model
        self.graph = graph or Graph()



    def extract_facts(self, text):
        schema = {
            "type": "object",
            "properties": {
                "facts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "head_entity": {
                                "type": "string"
                            },
                            "relation": {
                                "type": "string"
                            },
                            "tail_entity": {
                                "type": "string"
                            },
                        },
                        "required": [
                            "head_entity",
                            "relation",
                            "tail_entity",
                        ],
                    },
                }
            },
            "required": ["facts"],
        }

        prompt = f"""
            Extract factual knowledge graph triples
            from the following text.

            Return only facts explicitly present in the text.

            Each fact must contain:

            - head_entity
            - relation in uppercase with underscores
            - tail_entity

            Text:
            {text}
        """

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format=schema,
        )

        content = response["message"]["content"]
        return json.loads(content)



    def store_facts(self, text):
        extraction = self.extract_facts(text)
        stored_facts = []

        for fact in extraction["facts"]:
            stored_fact = self.graph.add_fact(
                head_entity=fact["head_entity"],
                relation=fact["relation"],
                tail_entity=fact["tail_entity"],
            )

            stored_facts.append(stored_fact)

        return stored_facts



    def pipeline_query(self, question):
        """
        1. Extraire les entités de la question
        2. Rechercher les informations dans Neo4j
        3. Transmettre les faits du graphe au LLM
        4. Générer une réponse fondée sur les informations du graphe
        """

        question_extraction = self.extract_facts(question)

        entities = set()

        for fact in question_extraction["facts"]:
            entities.add(fact["head_entity"])
            entities.add(fact["tail_entity"])

        graph_facts = []

        for entity in entities:
            graph_facts.extend(
                self.graph.search_facts(entity)
            )

        # Remove duplicate facts
        unique_facts = {
            (
                fact["head_entity"],
                fact["relation"],
                fact["tail_entity"],
            ): fact
            for fact in graph_facts
        }

        graph_facts = list(unique_facts.values())

        context = "\n".join(
            f"- {fact['head_entity']} "
            f"--{fact['relation']}--> "
            f"{fact['tail_entity']}"
            for fact in graph_facts
        )

        if not context:
            context = "No fact was found in Neo4j."

        prompt = f"""
            Answer the question using only the facts
            provided by the knowledge graph.

            Question:
            {question}

            Knowledge graph facts:
            {context}

            If the graph does not contain enough information,
            answer exactly:

            Information is not available in the graph.
        """

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return {
            "answer": response["message"]["content"],
            "graph_facts": graph_facts,
        }
