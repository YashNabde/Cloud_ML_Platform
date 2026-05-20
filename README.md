# Cloud ML Platform

A cloud-based machine learning deployment and inference platform built using FastAPI and Scikit-learn.

The platform enables users to upload machine learning models, run predictions dynamically, monitor prediction activity, and manage deployed models through a professional web dashboard.

---

## Features

- Secure Authentication System
- Professional Cloud Dashboard
- Dynamic Model Uploading
- Multi-Model Machine Learning Support
- Real-Time Prediction Engine
- Prediction Analytics & History
- Loan Approval Prediction
- House Price Prediction
- Salary Prediction
- Student Performance Prediction
- Enterprise-Style UI
- Cloud Deployment Ready

---

## Technologies Used

### Backend
- FastAPI
- Python
- Jinja2

### Machine Learning
- Scikit-learn
- Random Forest Regressor
- Decision Tree Classifier
- Joblib
- NumPy
- Pandas

### Frontend
- HTML
- CSS
- Jinja Templates

### Deployment
- GitHub
- Render

---

## Machine Learning Models

### House Price Prediction
Predicts property value using:
- House Size
- Bedrooms
- Bathrooms
- Property Age
- Location Rating

### Salary Prediction
Predicts salary package using:
- Years of Experience
- Education Level
- Skill Rating
- Certifications

### Student Performance Prediction
Predicts student score using:
- Study Hours

### Loan Approval Prediction
Predicts loan approval using:
- Monthly Income
- Credit Score

---

## Project Structure

```bash
project/
│
├── main.py
├── requirements.txt
├── history.json
│
├── models/
│   ├── house.pkl
│   ├── salary.pkl
│   ├── student.pkl
│   └── loan.pkl
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
└── static/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Cloud_ML_Platform.git
```

### Navigate to Project

```bash
cd Cloud_ML_Platform
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn main:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000
```

---

## Default Login Credentials

```text
Username: admin
Password: admin123
```

---

## Deployment

The application can be deployed using:

- Render
- Railway
- AWS EC2
- Docker

---

## Future Enhancements

- Docker Containerization
- Real Cloud Storage Integration
- User Role Management
- REST API Documentation
- Kubernetes Deployment
- Real-Time Monitoring
- Model Versioning
- Database Integration
- CI/CD Pipeline

---

## Author

Yash Nabde

---

## License

This project is developed for educational and academic purposes.
