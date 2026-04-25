from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Decorator

# Lets make a helper function to load data from the json file
def load_data():
    with open("patient.json", "r") as file:  # Add the file name and open in read mode.
        data = json.load(file)     
    return data

# Endpoints start
@app.get("/") ## root directories
def read_root():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fuly functional API to manage your patient records."}


@app.get("/view")
def view():
    data = load_data() # Loading the data from json using the helper function, for viewing purpose.
    return data


# Dynamic endpoint to view a specific patient record by ID
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient", example="P001")):
    data = load_data()
    patient_id = patient_id.upper() # Made it upper case for exact match
    patient = data.get(patient_id)  # safer lookup
    if patient:
        return patient
    # return {"error": f"Patient {patient_id}, not found"}
    raise HTTPException(status_code= 404, detail= f"{patient_id} not fount")

