from sklearn.tree import DecisionTreeClassifier
import joblib
import numpy as np

X = np.array([
    [30000,700],
    [20000,500],
    [50000,800],
    [25000,600]
])

y = np.array([1,0,1,0])

model = DecisionTreeClassifier()
model.fit(X,y)

joblib.dump(model,"loan.pkl")

print("Loan model created")