# agents/driver_allocation_agent.py

class DriverAllocationAgent:

    def __init__(self, demand_results):
        self.data = demand_results

    def allocate_drivers(self):

        shortage_zones = []
        surplus_zones = []

        for z in self.data:
            if z["status"] == "SHORTAGE":
                shortage_zones.append(z)
            elif z["status"] == "SURPLUS":
                surplus_zones.append(z)

        allocations = []

        for shortage in shortage_zones:
            needed = shortage["shortage"]

            for surplus in surplus_zones:
                available = abs(surplus["shortage"])

                if available <= 0:
                    continue

                move = min(needed, available)

                if move > 0:
                    allocations.append({
                        "from": surplus["zone"],
                        "to": shortage["zone"],
                        "drivers": move
                    })

                    needed -= move
                    surplus["shortage"] += move

                if needed <= 0:
                    break

        return allocations
