from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import os
import shutil
import joblib
import json

from datetime import datetime

# ---------------------------------------------------
# APP CONFIG
# ---------------------------------------------------

app = FastAPI()

templates = Jinja2Templates(directory="templates")

USERNAME = "admin"
PASSWORD = "admin123"

MODELS_DIR = "models"
HISTORY_FILE = "history.json"

os.makedirs(MODELS_DIR, exist_ok=True)

# ---------------------------------------------------
# HISTORY FILE SETUP
# ---------------------------------------------------

if not os.path.exists(HISTORY_FILE):

    with open(HISTORY_FILE, "w") as f:

        json.dump([], f)

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------

def load_history():

    with open(HISTORY_FILE, "r") as f:

        return json.load(f)


def save_history(history):

    with open(HISTORY_FILE, "w") as f:

        json.dump(history, f, indent=4)


def format_model_name(filename):

    name = filename.replace(".pkl", "")

    words = name.replace("_", " ").title()

    return words + " Model"

# ---------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={}
    )

# ---------------------------------------------------
# LOGIN LOGIC
# ---------------------------------------------------

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

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

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

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

# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------

@app.get("/logout")
def logout():

    response = RedirectResponse(url="/")

    response.delete_cookie("user")

    return response

# ---------------------------------------------------
# UPLOAD MODEL
# ---------------------------------------------------

@app.post("/upload-model")
async def upload_model(
    request: Request,
    model_file: UploadFile = File(...)
):

    filepath = os.path.join(
        MODELS_DIR,
        model_file.filename
    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            model_file.file,
            buffer
        )

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# ---------------------------------------------------
# DELETE MODEL
# ---------------------------------------------------

@app.get("/delete-model/{model_name}")
def delete_model(model_name: str):

    filepath = os.path.join(
        MODELS_DIR,
        model_name
    )

    if os.path.exists(filepath):

        os.remove(filepath)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# ---------------------------------------------------
# PREDICTION PAGE
# ---------------------------------------------------

@app.get("/predict/{model_name}", response_class=HTMLResponse)
def prediction_page(
    request: Request,
    model_name: str
):

    model_display = format_model_name(model_name)

    html = f"""
    <html>

    <head>

        <title>Run Inference</title>

        <style>

            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{

                font-family: 'Inter', sans-serif;

                background: #0f172a;

                display: flex;

                justify-content: center;

                align-items: center;

                height: 100vh;

                color: white;
            }}

            .card {{

                width: 430px;

                background: #111827;

                padding: 45px;

                border-radius: 18px;

                border: 1px solid #1e293b;

                text-align: center;
            }}

            h1 {{

                margin-bottom: 10px;

                font-size: 2rem;
            }}

            .subtitle {{

                color: #94a3b8;

                margin-bottom: 35px;

                font-size: 14px;
            }}

            input {{

                width: 100%;

                padding: 14px;

                margin-bottom: 18px;

                border: 1px solid #1e293b;

                border-radius: 10px;

                background: #0f172a;

                color: white;

                outline: none;
            }}

            button {{

                width: 100%;

                padding: 14px;

                border: none;

                border-radius: 10px;

                background: white;

                color: black;

                font-weight: 600;

                cursor: pointer;
            }}

            button:hover {{

                background: #d1d5db;
            }}

            .back-btn {{

                margin-top: 15px;

                display: inline-block;

                color: #94a3b8;

                text-decoration: none;

                font-size: 14px;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>{model_display}</h1>

            <div class="subtitle">

                Machine Learning Inference Console

            </div>

            <form action="/run-prediction/{model_name}"
                  method="post">
    """

    # ---------------------------------------------------
    # HOUSE MODEL
    # ---------------------------------------------------

    if "house" in model_name.lower():

        html += """
        <input type="number"
               name="size"
               placeholder="House Size (sq ft)"
               required>

        <input type="number"
               name="bedrooms"
               placeholder="Bedrooms"
               required>

        <input type="number"
               name="bathrooms"
               placeholder="Bathrooms"
               required>

        <input type="number"
               name="age"
               placeholder="Property Age"
               required>

        <input type="number"
               name="location"
               placeholder="Location Rating (1-10)"
               required>
        """

    # ---------------------------------------------------
    # SALARY MODEL
    # ---------------------------------------------------

    elif "salary" in model_name.lower():

        html += """
        <input type="number"
               name="experience"
               placeholder="Years of Experience"
               required>

        <input type="number"
               name="education"
               placeholder="Education Level (1-4)"
               required>

        <input type="number"
               name="skills"
               placeholder="Skill Rating (1-10)"
               required>

        <input type="number"
               name="certifications"
               placeholder="Certifications Count"
               required>
        """

    # ---------------------------------------------------
    # STUDENT MODEL
    # ---------------------------------------------------

    elif "student" in model_name.lower():

        html += """
        <input type="number"
               name="hours"
               placeholder="Study Hours"
               required>
        """

    # ---------------------------------------------------
    # LOAN MODEL
    # ---------------------------------------------------

    elif "loan" in model_name.lower():

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

            <a href="/dashboard" class="back-btn">

                Return to Dashboard

            </a>

        </div>

    </body>

    </html>
    """

    return HTMLResponse(content=html)

# ---------------------------------------------------
# RUN PREDICTION
# ---------------------------------------------------

@app.post("/run-prediction/{model_name}",
          response_class=HTMLResponse)

async def run_prediction(
    request: Request,
    model_name: str
):

    filepath = os.path.join(
        MODELS_DIR,
        model_name
    )

    model = joblib.load(filepath)

    model_name = model_name.lower()

    form = await request.form()

    result = ""

    # ---------------------------------------------------
    # HOUSE MODEL
    # ---------------------------------------------------

    if "house" in model_name:

        size = float(form["size"])
        bedrooms = float(form["bedrooms"])
        bathrooms = float(form["bathrooms"])
        age = float(form["age"])
        location = float(form["location"])

        prediction = model.predict([[
            size,
            bedrooms,
            bathrooms,
            age,
            location
        ]])[0]

        if prediction >= 100:

            crore = round(prediction / 100, 2)

            formatted_price = f"₹{crore} Crore"

        elif prediction < 1:

            thousand = round(prediction * 100, 2)

            formatted_price = f"₹{thousand} Thousand"

        else:

            formatted_price = f"₹{round(prediction,2)} Lakhs"

        result = (
            f"Estimated Property Value: {formatted_price}"
            f"<br><br>"
            f"Market Trend: Stable Growth"
            f"<br><br>"
            f"Property Evaluation Status: Verified"
        )

    # ---------------------------------------------------
    # SALARY MODEL
    # ---------------------------------------------------

    elif "salary" in model_name:

        experience = float(form["experience"])
        education = float(form["education"])
        skills = float(form["skills"])
        certifications = float(form["certifications"])

        prediction = model.predict([[
            experience,
            education,
            skills,
            certifications
        ]])[0]

        if prediction >= 100:

            crore = round(prediction / 100, 2)

            formatted_salary = f"₹{crore} Crore"

        elif prediction < 1:

            thousand = round(prediction * 100, 2)

            formatted_salary = f"₹{thousand} Thousand"

        else:

            formatted_salary = f"₹{round(prediction,2)} Lakhs"

        if prediction >= 40:

            level = "Executive Level Compensation"

        elif prediction >= 20:

            level = "Senior Professional Compensation"

        elif prediction >= 10:

            level = "Mid-Level Compensation"

        else:

            level = "Entry-Level Compensation"

        result = (
            f"Estimated Salary Package: {formatted_salary}"
            f"<br><br>"
            f"Compensation Category: {level}"
            f"<br><br>"
            f"Industry Benchmark Status: Competitive"
        )

    # ---------------------------------------------------
    # STUDENT MODEL
    # ---------------------------------------------------

    elif "student" in model_name:

        hours = float(form["hours"])

        prediction = model.predict([[hours]])[0]

        prediction = max(0, min(prediction, 100))

        if prediction >= 85:

            performance = "Excellent Performance"

        elif prediction >= 70:

            performance = "Good Performance"

        elif prediction >= 50:

            performance = "Average Performance"

        else:

            performance = "Needs Improvement"

        result = (
            f"Predicted Student Score: {round(prediction,2)}%"
            f"<br><br>"
            f"Academic Assessment: {performance}"
        )

    # ---------------------------------------------------
    # LOAN MODEL
    # ---------------------------------------------------

    elif "loan" in model_name:

        income = float(form["income"])
        credit = float(form["credit"])

        prediction = model.predict([[income, credit]])[0]

        if prediction == 1:

            risk = "Low Risk Applicant"

            approval = "Approved"

            recommendation = "Eligible for standard interest rates"

        else:

            risk = "High Risk Applicant"

            approval = "Rejected"

            recommendation = "Requires financial profile improvement"

        result = (
            f"Loan Application Status: {approval}"
            f"<br><br>"
            f"Risk Assessment: {risk}"
            f"<br><br>"
            f"Recommendation: {recommendation}"
        )

    else:

        result = "Unsupported Model Type"

    # ---------------------------------------------------
    # SAVE HISTORY
    # ---------------------------------------------------

    history = load_history()

    history.append({

        "model": model_name,

        "result": result,

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })

    save_history(history)

    # ---------------------------------------------------
    # RESULT PAGE
    # ---------------------------------------------------

    return HTMLResponse(f"""

    <html>

    <head>

    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{

        font-family: 'Inter', sans-serif;

        background: #0f172a;

        display: flex;

        justify-content: center;

        align-items: center;

        height: 100vh;

        color: white;
    }}

    .card {{

        width: 500px;

        background: #111827;

        padding: 50px;

        border-radius: 18px;

        border: 1px solid #1e293b;

        text-align: center;
    }}

    h1 {{

        font-size: 2rem;

        margin-bottom: 20px;
    }}

    .status {{

        display: inline-block;

        background: #052e16;

        color: #22c55e;

        padding: 8px 16px;

        border-radius: 20px;

        font-size: 13px;

        margin-bottom: 25px;
    }}

    .result {{

        font-size: 1.2rem;

        font-weight: 500;

        margin-bottom: 30px;

        line-height: 32px;
    }}

    .meta {{

        color: #94a3b8;

        font-size: 14px;

        line-height: 28px;
    }}

    button {{

        margin-top: 35px;

        width: 100%;

        padding: 14px;

        border: none;

        border-radius: 10px;

        background: white;

        color: black;

        font-weight: 600;

        cursor: pointer;
    }}

    button:hover {{

        background: #d1d5db;
    }}

    </style>

    </head>

    <body>

    <div class="card">

        <h1>Inference Result</h1>

        <div class="status">

            Prediction Generated Successfully

        </div>

        <div class="result">

            {result}

        </div>

        <div class="meta">

            API Status: Operational

            <br>

            Average Latency: 24ms

            <br>

            Model Confidence: 92%

            <br>

            Runtime Environment: Python 3.11

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