# FastAPI BaseModel

This repository demonstrates how to use **Pydantic's BaseModel** with **FastAPI** to build a REST API. The API is lightweight, fast, and leverages automatic validation and serialization through Pydantic models.

## 📄 File Descriptions

- `main.py` – FastAPI app that loads patient data and serves it through a REST endpoint using `BaseModel`.
- `patients.json` – Sample dataset of patient records including BMI and health verdicts.

## 🚀 Running the App

Install FastAPI, Pydantic and Uvicorn:

```
pip install fastapi pydantic uvicorn
```

Then start the API:

```
uvicorn main:app --reload
```

Visit the docs at:

```
http://127.0.0.1:8000/docs
```
