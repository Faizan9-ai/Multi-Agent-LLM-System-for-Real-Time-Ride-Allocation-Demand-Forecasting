import pandas as pd # pyright: ignore[reportMissingModuleSource]
import random
from datetime import datetime, timedelta
import uuid

random.seed(42)

# -------------------------------
# CONFIGURATION
# -------------------------------
NUM_DRIVERS = 500
NUM_PASSENGERS = 10000
NUM_ZONES = 40
NUM_RIDES = 50000

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 1, 31)

# -------------------------------
# HELPERS
# -------------------------------
def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# -------------------------------
# ZONES
# -------------------------------
zones = []
for i in range(1, NUM_ZONES + 1):
    zones.append({
        "zone_id": f"Z{i:02}",
        "name": f"Zone_{i}"
    })

zones_df = pd.DataFrame(zones)
zones_df.to_csv("../data/zones.csv", index=False)

# -------------------------------
# DRIVERS
# -------------------------------
drivers = []
for i in range(1, NUM_DRIVERS + 1):
    drivers.append({
        "driver_id": f"D{i:04}",
        "name": f"Driver_{i}",
        "rating": round(random.uniform(4.0, 5.0), 2),
        "acceptance_rate": round(random.uniform(0.70, 0.98), 2),
        "join_date": random_date(
            datetime(2019, 1, 1),
            datetime(2024, 12, 31)
        ).strftime("%Y-%m-%d")
    })

drivers_df = pd.DataFrame(drivers)
drivers_df.to_csv("../data/drivers.csv", index=False)

# -------------------------------
# PASSENGERS
# -------------------------------
passengers = []
for i in range(1, NUM_PASSENGERS + 1):
    passengers.append({
        "passenger_id": f"P{i:05}",
        "name": f"Passenger_{i}"
    })

passengers_df = pd.DataFrame(passengers)
passengers_df.to_csv("../data/passengers.csv", index=False)

# -------------------------------
# RIDES
# -------------------------------
rides = []

for i in range(1, NUM_RIDES + 1):

    ride_time = random_date(START_DATE, END_DATE)
    hour = ride_time.hour

    # peak-hour simulation
    if 18 <= hour <= 22:
        status = random.choices(
            ["COMPLETED", "CANCELLED"],
            weights=[85, 15]
        )[0]
    else:
        status = random.choices(
            ["COMPLETED", "CANCELLED"],
            weights=[92, 8]
        )[0]

    rides.append({
        "ride_id": f"R{i:06}",
        "driver_id": f"D{random.randint(1, NUM_DRIVERS):04}",
        "passenger_id": f"P{random.randint(1, NUM_PASSENGERS):05}",
        "from_zone": f"Z{random.randint(1, NUM_ZONES):02}",
        "to_zone": f"Z{random.randint(1, NUM_ZONES):02}",
        "request_time": ride_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": status,
        "fare": round(random.uniform(8, 60), 2) if status == "COMPLETED" else 0
    })

rides_df = pd.DataFrame(rides)
rides_df.to_csv("../data/rides.csv", index=False)

# -------------------------------
# COMMISSIONS
# -------------------------------
commissions = []
months = pd.period_range("2024-01", "2025-01", freq="M")

for driver in drivers:
    for month in months:
        amount = round(random.uniform(300, 1500), 2)
        status = random.choices(
            ["PAID", "UNPAID"],
            weights=[80, 20]
        )[0]

        commissions.append({
            "commission_id": str(uuid.uuid4()),
            "driver_id": driver["driver_id"],
            "month": str(month),
            "amount": amount,
            "status": status
        })

commissions_df = pd.DataFrame(commissions)
commissions_df.to_csv("../data/commissions.csv", index=False)

# -------------------------------
# PAYMENTS
# -------------------------------
payments = []

for c in commissions:
    if c["status"] == "PAID":
        payments.append({
            "payment_id": str(uuid.uuid4()),
            "commission_id": c["commission_id"],
            "paid_on": random_date(
                START_DATE,
                END_DATE
            ).strftime("%Y-%m-%d"),
            "method": random.choice(["CASH", "BANK_TRANSFER", "CARD"])
        })

payments_df = pd.DataFrame(payments)
payments_df.to_csv("../data/payments.csv", index=False)

# -------------------------------
# DONE
# -------------------------------
print("✅ All CSV files generated successfully")
