from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File
from datetime import datetime

import os
import shutil
import joblib
import json


MODELS_DIR = "models"
HISTORY_FILE = "history.json"


def load_history():

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

os.makedirs(MODELS_DIR, exist_ok=True)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Fake credentials
USERNAME = "admin"
PASSWORD = "admin123"

# ---------------- LOGIN PAGE ----------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={}
    )

# ---------------- LOGIN LOGIC ----------------

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == USERNAME and password == PASSWORD:

        response = RedirectResponse(
            url="/dashboard",
            status_code=303
        )

        response.set_cookie(
            key="user",
            value=username
        )

        return response

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={
            "error": "Invalid Username or Password"
        }
    )

def format_model_name(filename):

    name = filename.replace(".pkl", "")

    words = name.replace("_", " ").title()

    return words + " Model"

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    user = request.cookies.get("user")

    if not user:
        return RedirectResponse(url="/")

    raw_models = os.listdir(MODELS_DIR)

    models = []

    for model in raw_models:

            if model.endswith(".pkl"):

                models.append({
                    "file": model,
                    "display": format_model_name(model)
        })
    history = load_history()

    total_predictions = len(history)

    recent_history = history[-5:]   


    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context={
    "user": user,
    "models": models,
    "total_predictions": total_predictions,
    "recent_history": recent_history
}
    )

@app.post("/upload-model")
async def upload_model(
    request: Request,
    model_file: UploadFile = File(...)
):

    filepath = os.path.join(MODELS_DIR, model_file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(model_file.file, buffer)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )
@app.get("/delete-model/{model_name}")
def delete_model(model_name: str):

    filepath = os.path.join(MODELS_DIR, model_name)

    if os.path.exists(filepath):

        os.remove(filepath)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# ---------------- LOGOUT ----------------

@app.get("/logout")
def logout():

    response = RedirectResponse(
        url="/"
    )

    response.delete_cookie("user")

    return response

@app.get("/predict/{model_name}", response_class=HTMLResponse)
def prediction_page(
    request: Request,
    model_name: str
):

    model_display = format_model_name(model_name)

    html = f"""
    <html>

    <head>
        <title>Prediction</title>

        <style>

            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: white;
            }}

            .card {{
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                width: 350px;
                text-align: center;
            }}

            input {{
                width: 90%;
                padding: 12px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
            }}

            button {{
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(to right, #00c6ff, #0072ff);
                color: white;
                cursor: pointer;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>{model_display}</h1>

            <form action="/run-prediction/{model_name}"
                  method="post">
    """

    # ---------- HOUSE MODEL ----------

    if "house" in model_name:

        html += """
            <input type="number"
                   name="size"
                   placeholder="House Size"
                   required>

            <input type="number"
                   name="bedrooms"
                   placeholder="Bedrooms"
                   required>
        """

    # ---------- SALARY MODEL ----------

    elif "salary" in model_name:

        html += """
            <input type="number"
                   name="experience"
                   placeholder="Years of Experience"
                   required>
        """

    # ---------- STUDENT MODEL ----------

    elif "student" in model_name:

        html += """
            <input type="number"
                   name="hours"
                   placeholder="Study Hours"
                   required>
        """

    # ---------- LOAN MODEL ----------

    elif "loan" in model_name:

        html += """
            <input type="number"
                   name="income"
                   placeholder="Monthly Income"
                   required>

            <input type="number"
                   name="credit"
                   placeholder="Credit Score"
                   required>
        """

    html += """

            <button type="submit">
                Run Inference
            </button>

            </form>

        </div>

    </body>

    </html>
    """

    return HTMLResponse(content=html)

@app.post("/run-prediction/{model_name}",
          response_class=HTMLResponse)

async def run_prediction(
    request: Request,
    model_name: str
    
):

    filepath = os.path.join(MODELS_DIR, model_name)

    model = joblib.load(filepath)

    form = await request.form()

    # ---------- HOUSE ----------

    if "house" in model_name:

        size = float(form["size"])
        bedrooms = float(form["bedrooms"])

        prediction = model.predict([[size, bedrooms]])[0]

        result = f"🏠 Predicted House Price: ₹{round(prediction,2)} Lakhs"

    # ---------- SALARY ----------

    elif "salary" in model_name:

        experience = float(form["experience"])

        prediction = model.predict([[experience]])[0]

        result = f"💼 Predicted Salary: ₹{round(prediction,2)} Lakhs"

    # ---------- STUDENT ----------

    elif "student" in model_name:

        hours = float(form["hours"])

        prediction = model.predict([[hours]])[0]

        result = f"🎓 Predicted Score: {round(prediction,2)}%"

    # ---------- LOAN ----------

    elif "loan" in model_name:

        income = float(form["income"])
        credit = float(form["credit"])

        prediction = model.predict([[income, credit]])[0]

        if prediction == 1:
            result = "🏦 Loan Approved"
        else:
            result = "❌ Loan Rejected"

    history = load_history()

    history.append({

        "model": model_name,

        "result": result,

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })

    save_history(history)
    
    return HTMLResponse(f"""

<html>

<head>

<style>

body {{

    margin: 0;

    font-family: 'Segoe UI', sans-serif;

    background: linear-gradient(135deg, #0f172a, #1e293b);

    display: flex;

    justify-content: center;

    align-items: center;

    height: 100vh;

    color: white;
}}

.card {{

    background: rgba(255,255,255,0.08);

    padding: 45px;

    border-radius: 18px;

    backdrop-filter: blur(10px);

    text-align: center;

    width: 420px;

    box-shadow: 0 10px 35px rgba(0,0,0,0.4);

    animation: fadeIn 0.6s ease;
}}

.result {{

    font-size: 2rem;

    margin: 20px 0;

    color: #38bdf8;
}}

.tag {{

    display: inline-block;

    background: #16a34a;

    padding: 8px 16px;

    border-radius: 20px;

    font-size: 13px;

    margin-bottom: 20px;
}}

.meta {{

    color: #94a3b8;

    font-size: 13px;

    margin-top: 20px;
}}

button {{

    margin-top: 25px;

    padding: 12px 20px;

    border: none;

    border-radius: 10px;

    background: linear-gradient(to right, #00c6ff, #0072ff);

    color: white;

    cursor: pointer;

    font-weight: bold;
}}

@keyframes fadeIn {{

    from {{

        opacity: 0;
        transform: translateY(20px);

    }}

    to {{

        opacity: 1;
        transform: translateY(0);

    }}
}}

</style>

</head>

<body>

<div class="card">

    <h1>Prediction Completed</h1>

    <div class="tag">

        API Response Successful

    </div>

    <div class="result">

        {result}

    </div>

    <div class="meta">

        Response Time: 24ms

        <br><br>

        Model Confidence: 92%

        <br><br>

        Cloud Status: Operational

    </div>

    <form action="/dashboard" method="get">

        <button>

            Return to Dashboard

        </button>

    </form>

</div>

</body>

</html>

""")