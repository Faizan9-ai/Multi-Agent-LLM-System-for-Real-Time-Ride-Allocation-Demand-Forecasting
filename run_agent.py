# run_agent.py

from agents.demand_analysis_agent import DemandAnalysisAgent
from agents.driver_allocation_agent import DriverAllocationAgent
from agents.driver_shortage_agent import DriverShortageAgent
from agents.business_recommendation_agent import BusinessRecommendationAgent


def main():

    print("\n==============================")
    print("🚕 STATION CARS AI PLATFORM")
    print("==============================\n")

    # --------------------------------------------------
    # STEP 1: DEMAND ANALYSIS AGENT
    # --------------------------------------------------

    print("📊 Running Demand Analysis Agent...\n")

    demand_agent = DemandAnalysisAgent()
    demand_results = demand_agent.analyze_demand()

    for r in demand_results[:15]:
        print(r)

    # --------------------------------------------------
    # STEP 2: DRIVER ALLOCATION AGENT
    # --------------------------------------------------

    print("\n==============================")
    print("🚗 DRIVER ALLOCATION AGENT")
    print("==============================\n")

    allocation_agent = DriverAllocationAgent(demand_results)
    allocations = allocation_agent.allocate_drivers()

    if not allocations:
        print("✅ No driver movement required.")
    else:
        for a in allocations:
            print(
                f"Move {a['drivers']} drivers "
                f"from Zone {a['from']} → Zone {a['to']}"
            )

    # --------------------------------------------------
    # STEP 3: DRIVER SHORTAGE AGENT
    # --------------------------------------------------

    print("\n==============================")
    print("⚠️ DRIVER SHORTAGE AGENT")
    print("==============================\n")

    shortage_agent = DriverShortageAgent()
    movements = shortage_agent.rebalance_drivers(demand_results)

    if not movements:
        print("✅ System already balanced.")
    else:
        for m in movements:
            print(
                f"Move {m['drivers_moved']} drivers "
                f"from Zone {m['from_zone']} → Zone {m['to_zone']}"
            )

    shortage_agent.close()
    demand_agent.close()

    # --------------------------------------------------
    # STEP 4: BUSINESS RECOMMENDATION AGENT (FINAL)
    # --------------------------------------------------

    print("\n==============================")
    print("💼 BUSINESS RECOMMENDATION AGENT")
    print("==============================\n")

    biz_agent = BusinessRecommendationAgent()
    recommendations = biz_agent.generate_recommendations(demand_results)

    for r in recommendations[:15]:
        print(f"[{r['action']}] {r['message']}")

    print("\n🎉 ALL AGENTS EXECUTED SUCCESSFULLY\n")


if __name__ == "__main__":
    main()
