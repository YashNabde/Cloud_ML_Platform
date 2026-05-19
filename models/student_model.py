from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

X = np.array([[1],[2],[3],[4],[5]])
y = np.array([35,45,60,75,90])

model = LinearRegression()
model.fit(X,y)

joblib.dump(model,"student.pkl")

print("Student model created")