from neo4j import GraphDatabase


class DriverShortageAgent:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "neo4j123")
        )

    def rebalance_drivers(self, demand_results):

        surplus_zones = [
            z for z in demand_results if z["status"] == "SURPLUS"
        ]

        shortage_zones = [
            z for z in demand_results if z["status"] == "SHORTAGE"
        ]

        movements = []

        for shortage in shortage_zones:
            required = shortage["shortage"]

            for surplus in surplus_zones:
                available = abs(surplus["shortage"])

                if available <= 0 or required <= 0:
                    continue

                moved = min(required, available)

                movements.append({
                    "from_zone": surplus["zone"],
                    "to_zone": shortage["zone"],
                    "drivers_moved": moved
                })

                surplus["shortage"] += moved
                required -= moved

        return movements

    def close(self):
        self.driver.close()
