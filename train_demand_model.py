import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.model_selection import train_test_split # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import RandomForestRegressor # pyright: ignore[reportMissingModuleSource]
from sklearn.metrics import mean_absolute_error # pyright: ignore[reportMissingModuleSource]
import joblib # pyright: ignore[reportMissingImports]

# Load data
df = pd.read_csv(r'C:/Users/station cars projects/zone_daily_demand.csv')

# Feature engineering
df["day"] = pd.to_datetime(df["day"])
df["day_of_week"] = df["day"].dt.dayofweek
df["day_of_month"] = df["day"].dt.day
df["month"] = df["day"].dt.month

X = df[["day_of_week", "day_of_month", "month", "avg_fare"]]
y = df["total_rides"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print("MAE:", mae)

# Save model
joblib.dump(model, "demand_forecast_model.pkl")
