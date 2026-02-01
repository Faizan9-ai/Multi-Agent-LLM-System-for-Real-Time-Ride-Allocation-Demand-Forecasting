from neo4j import GraphDatabase
import joblib
import pandas as pd
from datetime import datetime, timedelta

# -----------------------
# Neo4j connection
# -----------------------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j123"

# -----------------------
# Load ML model
# -----------------------
model = joblib.load("demand_forecast_model.pkl")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

tomorrow = datetime.today() + timedelta(days=1)

# -----------------------
# Write forecast to graph
# -----------------------
def write_forecast(tx, zone_node_id, predicted):
    tx.run("""
        MATCH (z)
        WHERE id(z) = $zone_node_id

        CREATE (f:DemandForecast {
            date: date($date),
            predicted_rides: $predicted,
            model_version: "rf_v1",
            created_at: datetime()
        })

        CREATE (z)-[:HAS_FORECAST]->(f)
    """,
    zone_node_id=zone_node_id,
    predicted=int(round(predicted)),
    date=tomorrow.strftime("%Y-%m-%d")
    )

# -----------------------
# Run forecasting
# -----------------------
with driver.session() as session:

    zones = session.run("""
        MATCH (z:Zone)
        RETURN id(z) AS zid, z.zone_id AS zone
        ORDER BY zone
    """)

    for record in zones:
        zid = record["zid"]

        features = pd.DataFrame([{
            "day_of_week": tomorrow.weekday(),
            "day_of_month": tomorrow.day,
            "month": tomorrow.month,
            "avg_fare": 30
        }])

        prediction = model.predict(features)[0]

        session.execute_write(
            write_forecast,
            zid,
            prediction
        )

driver.close()

print("✅ Demand forecast successfully written to Neo4j")
