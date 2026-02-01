from neo4j import GraphDatabase

class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password)
        )

    def run(self, query, params=None):
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
