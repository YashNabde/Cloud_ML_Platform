import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------------- DATASET ----------------

np.random.seed(42)

samples = 3000

experience = np.random.randint(0, 25, samples)

education = np.random.randint(1, 5, samples)

skills = np.random.randint(1, 10, samples)

certifications = np.random.randint(0, 8, samples)

salary = (
    experience * 2.5 +
    education * 5 +
    skills * 3 +
    certifications * 2 +
    np.random.normal(0, 5, samples)
)

salary = np.clip(salary, 3, None)

# ---------------- DATAFRAME ----------------

df = pd.DataFrame({
    "experience": experience,
    "education": education,
    "skills": skills,
    "certifications": certifications,
    "salary": salary
})

# ---------------- SPLIT ----------------

X = df.drop("salary", axis=1)

y = df["salary"]

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

joblib.dump(model, "salary.pkl")

print("Professional Salary Model Saved!")