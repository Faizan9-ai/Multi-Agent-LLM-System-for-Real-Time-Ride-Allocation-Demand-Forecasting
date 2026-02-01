import streamlit as st
import pandas as pd

from agents.demand_analysis_agent import DemandAnalysisAgent
from agents.driver_allocation_agent import DriverAllocationAgent
from agents.business_recommendation_agent import BusinessRecommendationAgent


# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Station Cars AI Control Center",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------
st.title("🚕 Station Cars – AI Operations Control Center")
st.caption("Real-time demand, driver allocation & business recommendations")

st.markdown("---")

# -------------------------------
# Run agents
# -------------------------------
demand_agent = DemandAnalysisAgent()
demand_results = demand_agent.analyze_demand()

allocation_agent = DriverAllocationAgent(demand_results)
allocations = allocation_agent.allocate_drivers()

biz_agent = BusinessRecommendationAgent()
recommendations = biz_agent.generate_recommendations(demand_results)

demand_agent.close()

df = pd.DataFrame(demand_results)

# -------------------------------
# KPI Metrics
# -------------------------------
total_zones = df.shape[0]
total_drivers = df["drivers"].sum()
shortage_zones = df[df["status"] == "SHORTAGE"].shape[0]
surplus_zones = df[df["status"] == "SURPLUS"].shape[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Zones", total_zones)
col2.metric("Total Drivers", total_drivers)
col3.metric("Shortage Zones", shortage_zones)
col4.metric("Surplus Zones", surplus_zones)

st.markdown("---")

# -------------------------------
# Demand vs Supply Table
# -------------------------------
st.subheader("📊 Zone-wise Demand vs Supply")

def highlight_status(row):
    if row["status"] == "SHORTAGE":
        return ["background-color: #ffcccc"] * len(row)
    elif row["status"] == "SURPLUS":
        return ["background-color: #ccffcc"] * len(row)
    else:
        return ["background-color: #fff3cd"] * len(row)

st.dataframe(
    df.style.apply(highlight_status, axis=1),
    use_container_width=True
)

# -------------------------------
# Driver Allocation
# -------------------------------
st.markdown("---")
st.subheader("🚗 Driver Allocation Recommendations")

if not allocations:
    st.success("System is balanced. No driver movement required.")
else:
    for a in allocations:
        st.write(
            f"➡️ Move **{a['drivers']} drivers** "
            f"from **Zone {a['from']}** → **Zone {a['to']}**"
        )

# -------------------------------
# Business Recommendations
# -------------------------------
st.markdown("---")
st.subheader("💼 Business Recommendations")

for r in recommendations[:10]:
    if "SURGE" in r["action"]:
        st.error(r["message"])
    elif "MARKETING" in r["action"]:
        st.info(r["message"])
    elif "REDUCE" in r["action"]:
        st.warning(r["message"])
    else:
        st.success(r["message"])
