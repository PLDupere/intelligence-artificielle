from neo4j import GraphDatabase
# https://neo4j.com/docs/query-api/current/query/

class Graph:
    def __init__(
        self,
        uri="bolt://localhost:7687",
        username="neo4j",
        password="changez-moi",
        database="neo4j",
    ):
        self.database = database
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password),
        )

    def verify_connection(self):
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()



    def add_fact(self, head_entity, relation, tail_entity ):
        relation = self.clean_relation(relation)

        query = f"""
        MERGE (head:Entity {{name: $head_entity}})
        MERGE (tail:Entity {{name: $tail_entity}})
        MERGE (head)-[r:{relation}]->(tail)

        RETURN head.name AS head_entity,
            type(r) AS relation,
            tail.name AS tail_entity
        """

        records, _, _ = self.driver.execute_query(
            query,
            head_entity=head_entity,
            tail_entity=tail_entity,
            database_=self.database,
        )

        return records[0].data() if records else None



    def search_facts(self, entity):
        query = """
        MATCH (head:Entity)-[relation]->(tail:Entity)
        WHERE toLower(head.name) CONTAINS toLower($entity)
        OR toLower(tail.name) CONTAINS toLower($entity)

        RETURN head.name AS head_entity,
            type(relation) AS relation,
            tail.name AS tail_entity

        LIMIT 20
        """

        records, _, _ = self.driver.execute_query(
            query,
            entity=entity,
            database_=self.database,
        )

        return [record.data() for record in records]



    @staticmethod
    def clean_relation(relation):
        relation = relation.upper()
        relation = relation.replace(" ", "_")
        relation = relation.replace("-", "_")

        allowed_characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789")

        relation = "".join(
            character
            for character in relation
            if character in allowed_characters
        )

        return relation or "RELATED_TO"
