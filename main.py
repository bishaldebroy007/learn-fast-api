from fastapi import FastAPI
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

