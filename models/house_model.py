import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------------- DATASET ----------------

np.random.seed(42)

samples = 3000

size = np.random.randint(500, 5000, samples)

bedrooms = np.random.randint(1, 7, samples)

bathrooms = np.random.randint(1, 5, samples)

age = np.random.randint(0, 30, samples)

location_factor = np.random.randint(1, 10, samples)

price = (
    size * 5500 +
    bedrooms * 400000 +
    bathrooms * 300000 -
    age * 50000 +
    location_factor * 700000 +
    np.random.randint(-500000, 500000, samples)
)

price = price / 100000

# ---------------- DATAFRAME ----------------

df = pd.DataFrame({
    "size": size,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "age": age,
    "location": location_factor,
    "price": price
})

# ---------------- TRAIN TEST SPLIT ----------------

X = df.drop("price", axis=1)

y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------- MODEL ----------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------

predictions = model.predict(X_test)

score = r2_score(y_test, predictions)

print(f"Model Accuracy: {score:.2f}")

# ---------------- SAVE ----------------

joblib.dump(model, "house.pkl")

print("Professional House Model Saved!")