import random
from neo4j import GraphDatabase


class DemandAnalysisAgent:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "neo4j123")
        )

    def analyze_demand(self):

        query = """
        MATCH (z:Zone)
        OPTIONAL MATCH (d:Driver)-[:WORKED_IN]->(z)
        WITH z.zone_id AS zone, COUNT(d) AS drivers
        RETURN zone, drivers
        """

        with self.driver.session() as session:
            data = session.run(query)

            results = []

            for row in data:
                drivers = row["drivers"]

                # realistic simulated demand
                demand = drivers + random.randint(-200, 300)

                diff = demand - drivers

                if diff > 50:
                    status = "SHORTAGE"
                elif diff < -50:
                    status = "SURPLUS"
                else:
                    status = "BALANCED"

                results.append({
                    "zone": row["zone"],
                    "demand": demand,
                    "drivers": drivers,
                    "shortage": diff,
                    "status": status
                })

            return results

    def close(self):
        self.driver.close()
