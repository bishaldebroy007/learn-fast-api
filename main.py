from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Decorator

# Lets make a helper function to load data from the json file
def load_data():
    with open("PatientData.json", "r") as file:
        data = json.load(file)
        
    return data


@app.get("/") ## root directories
def read_root():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fuly functional API to manage your patient records."}

@app.get()
