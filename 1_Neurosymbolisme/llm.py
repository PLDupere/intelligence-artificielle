import json
import ollama
import re
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
            Extract knowledge graph triples from every sentence in English.

            For each sentence, identify:

            - head_entity: the source entity
            - relation: the relationship between the entities, written in uppercase using snake_case
            - tail_entity: the target entity

            The direction of the relationship must follow the meaning of the sentence. Never reverse the head entity and the tail entity.

            Examples:

            Sentence: "Paris is the capital of France."
            - head_entity: Paris
            - relation: CAPITAL_OF
            - tail_entity: France

            Graph representation:
            (Paris)-[:CAPITAL_OF]->(France)

            Sentence: "France is located in Europe."
            - head_entity: France
            - relation: LOCATED_IN
            - tail_entity: Europe

            Graph representation:
            (France)-[:LOCATED_IN]->(Europe)

            Sentence: "The French language is spoken in France."
            - head_entity: French language
            - relation: SPOKEN_IN
            - tail_entity: France

            Graph representation:
            (French language)-[:SPOKEN_IN]->(France)

            General rules:

            1. The head_entity is the entity performing, possessing, or being described by the relation.
            2. The tail_entity is the entity receiving, containing, or completing the relation.
            3. Use a directed relation from head_entity to tail_entity.
            4. Write relation names in uppercase snake_case.
            5. Remove unnecessary articles such as "the", "a", or "an" from entity names.
            6. Preserve the original meaning of the sentence.
            7. Do not infer facts that are not explicitly stated.
            8. For multiple facts, extract one triple per fact.
            9. Use canonical entity names whenever possible.
            10. If a sentence does not express a relationship between two entities, do not create a triple.

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


# (i) une extraction d'entités/relations à partir d'un corpus
# (ii) une requête hybride (text-to-SPARQL) | Neo4j impossible , RDFLib possible 
# https://community.neo4j.com/t/neo4j-as-rdf-store-and-run-the-sparql-on-the-store-data/61579
    def pipeline_query(self, question):
        question_extraction = self.extract_facts(question)
    
        entities = set()
    
        for fact in question_extraction.get("facts", []):
            if fact.get("head_entity"):
                entities.add(fact["head_entity"])
    
            if fact.get("tail_entity"):
                entities.add(fact["tail_entity"])
    
        graph_facts = []
    
        for entity in entities:
            facts = self.graph.search_facts(entity)
    
            if facts:
                graph_facts.extend(facts)
    
        unique_facts = {
            (
                fact["head_entity"],
                fact["relation"],
                fact["tail_entity"],
            ): fact
            for fact in graph_facts
        }
    
        graph_facts = list(unique_facts.values())
    
        if not graph_facts:
            return {
                "answer": "Information is not available in the graph.",
                "graph_facts": [],
                "generated_fact": None,
                "verification_fact": "FAIL",
            }
    
        generated_fact = self.generate_structured_answer(
            question=question,
            graph_facts=graph_facts,
        )
    
        answer = generated_fact["answer"].strip()
    
        verification_fact = self.graph.fact_exists(
            head_entity=generated_fact["head_entity"],
            relation=generated_fact["relation"],
            tail_entity=generated_fact["tail_entity"],
        )

        # Vérification symbolique
        verification = self.symbolic_verification(
            generated_fact=generated_fact,
            graph_facts=graph_facts,
        )
    
        return {
            "answer": answer,
            "graph_facts": graph_facts,
            "generated_fact": generated_fact,
            "verification": verification,
            "verification_fact": (
                "PASS" if verification_fact else "FAIL"
            ),
        }

    # def pipeline_query(self, question):
    #     question_extraction = self.extract_facts(question)

    #     entities = set()

    #     for fact in question_extraction.get("facts", []):
    #         entities.add(fact["head_entity"])
    #         entities.add(fact["tail_entity"])

    #     graph_facts = []

    #     for entity in entities:
    #         facts = self.graph.search_facts(entity)

    #         if facts:
    #             graph_facts.extend(facts)

    #     # Suppression des doublons
    #     unique_facts = {
    #         (
    #             fact["head_entity"],
    #             fact["relation"],
    #             fact["tail_entity"],
    #         ): fact
    #         for fact in graph_facts
    #     }

    #     graph_facts = list(unique_facts.values())

    #     if not graph_facts:
    #         return {
    #             "answer": "Information is not available in the graph.",
    #             "graph_facts": [],
    #             "generated_fact": None,
    #             "verification": {
    #                 "verified": False,
    #                 "generated_triplet": None,
    #                 "matching_triplet": None,
    #             },
    #         }

    #     # Génération du triplet par le LLM
    #     generated_fact = self.generate_structured_answer(
    #         question=question,
    #         graph_facts=graph_facts,
    #     )

    #     # Vérification symbolique
    #     verification = self.symbolic_verification(
    #         generated_fact=generated_fact,
    #         graph_facts=graph_facts,
    #     )

    #     return {
    #         "answer": generated_fact["answer"],
    #         "graph_facts": graph_facts,
    #         "generated_fact": generated_fact,
    #         "verification": verification,
    #         "verification_fact": (
    #             "PASS" if verification["verified"] else "FAIL"
    #         ),
    #     }



    def generate_structured_answer(self, question, graph_facts):

        schema = {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "head_entity": {"type": "string"},
                "relation": {"type": "string"},
                "tail_entity": {"type": "string"},
            },
            "required": [
                "answer",
                "head_entity",
                "relation",
                "tail_entity",
            ],
        }

        prompt = f"""
            Answer the question using only the graph facts.

            Question:
            {question}

            With:
            {graph_facts}
            

            Return exactly one JSON object:
            {{
                "answer": "...",
                "head_entity": "...",
                "relation": "...",
                "tail_entity": "..."
            }}

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

        return json.loads(response["message"]["content"])



    def normalize_relation(self, relation):
        relation = str(relation).strip().upper()
        relation = re.sub(r"^[^A-Z0-9]+|[^A-Z0-9]+$", "", relation)
        relation = re.sub(r"[\s-]+", "_", relation)
        relation = re.sub(r"_+", "_", relation)
        return relation


# (iii) une vérification symbolique de la cohérence des sorties
    def verify_answer(self, answer, graph_facts):
        answer_normalized = answer.lower()
        expected_values = []

        for fact in graph_facts:
            expected_values.append(fact["head_entity"].lower())
            expected_values.append(fact["tail_entity"].lower())

        matching_values = [
            value
            for value in expected_values
            if value in answer_normalized
        ]

        return {
            "verified": bool(matching_values),
            "matching_values": matching_values,
        }



    def symbolic_verification(self, generated_fact, graph_facts):
        generated_triplet = (
            generated_fact["head_entity"].strip().lower(),
            self.normalize_relation(generated_fact["relation"]),
            generated_fact["tail_entity"].strip().lower(),
        )

        graph_triplets = {
            (
                fact["head_entity"].strip().lower(),
                self.normalize_relation(fact["relation"]),
                fact["tail_entity"].strip().lower(),
            )
            for fact in graph_facts
        }

        verified = generated_triplet in graph_triplets

        return {
            "verified": verified,
            "generated_triplet": generated_triplet,
            "matching_triplet": generated_triplet if verified else None,
        }
