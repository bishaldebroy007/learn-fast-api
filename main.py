import json
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

# -------Imports --------

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient"),
    ]
    height: Annotated[
        float, Field(..., gt=0, description="Height of the patient in mtrs")
    ]
    weight: Annotated[
        float, Field(..., gt=0, description="Weight of the patient in kgs")
    ]

    ## Computed field for BMI
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(
        self,
    ) -> str:  ## Decision making based on BMI value, to determine the health status of the patient.

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# Lets make a helper function to load data from the json file
def load_data():
    with open("patient.json", "r") as file:  # Add the file name and open in read mode.
        data = json.load(file)
    return data


# Lets make another helper function to add data to the json
def save_data(data):
    with open("patient.json", "w") as file:
        json.dump(data, file)


# Endpoints start
@app.get("/")  ## root directories
def read_root():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records."}


@app.get("/view")
def view():
    data = (
        load_data()
    )  # Loading the data from json using the helper function, for viewing purpose.
    return data


# Dynamic endpoint to view a specific patient record by ID
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
):
    data = load_data()
    patient_id = patient_id.upper()  # Made it upper case for exact match
    patient = data.get(patient_id)  # safer lookup
    if patient:
        return patient
    # return {"error": f"Patient {patient_id}, not found"}
    raise HTTPException(status_code=404, detail=f"{patient_id} not fount")


# Sorting Data on the basis of query parameters
@app.get("/sort")
def patient_sort(
    sort_by: str = Query(..., description="Sort- height/weight/bmi"),
    order: str = Query("asc", description="sort in asc/desc order"),
):

    # List of all the valid fields. sort_orders
    valid_fields = ["weight", "height", "bmi"]
    sort_types = ["asc", "desc"]

    # Error handeling for sort_by
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field selected, {valid_fields}"
        )

    # Error handeling for order
    if order not in sort_types:
        raise HTTPException(
            status_code=400,
            detail="You've selected invalid order, chose between asc/desc",
        )

    # Loading the data using load_data()
    data = load_data()

    sort_order = True if order == "desc" else False

    """
    - Sort the dictionary values by the field specified in 'sort_by' (e.g., height/weight/bmi).
    - If the field is missing, default to 0. The 'reverse' flag applies the chosen sort order.
    """

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data

    # Test by running the server and accessing the endpoint with different query parameters, e.g., /sort?sort_by=height&order=desc
    # endpoint: http://127.0.0.1:8000/sort?sort_by=height&order=desc


## POST
@app.post("/create")
def creat_patient(patient: Patient):  # here "patient" is a pydancic object
    # load existing data from json in this case
    data = load_data()

    # checking if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exists")

    # Now if things are alright, add those to database: add patient to pydantic object(patient)
    else:
        data[patient.id] = patient.model_dump(
            exclude=["id"]
        )  # Convert the object to python disctionary using, model_dump()

    # Save into the json file
    save_data(data)

    return JSONResponse(
        status_code=201, content={"message": {"Patient created successfully"}}
    )
