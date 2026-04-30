import json
from typing import Annotated, Any, Dict, Literal

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

app = FastAPI()


class Patient(BaseModel):
    """
    Pydantic model representing a patient.
    Includes computed fields for BMI and health status.
    """

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

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculates BMI from weight and height."""
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Determines health status based on BMI."""
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


def load_data() -> Dict[str, Any]:
    """Helper to load patient data from the JSON file."""
    try:
        with open("patient.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(data: Dict[str, Any]) -> None:
    """Helper to save patient data to the JSON file."""
    with open("patient.json", "w") as file:
        json.dump(data, file, indent=4)


def enrich_patient(data: Dict[str, Any]) -> Dict[str, Any]:
    """Injects computed fields into raw data records for API responses."""
    # Convert dict to Pydantic object to trigger computed fields, then back to dict
    patient_obj = Patient(**data)
    return patient_obj.model_dump()


@app.get("/")
def read_root():
    return {"message": "Patient Management System API"}


@app.get("/view")
def view():
    """Returns all patient records with computed fields injected."""
    data = load_data()
    return {pid: enrich_patient(record) for pid, record in data.items()}


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
):
    """Returns a specific patient record with computed fields injected."""
    data = load_data()
    record = data.get(patient_id.upper())
    if not record:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return enrich_patient(record)


@app.get("/sort")
def patient_sort(
    sort_by: str = Query(..., description="Sort by: height/weight/bmi"),
    order: str = Query("asc", description="Sort order: asc/desc"),
):
    """Returns sorted list of patients, calculating BMI on-the-fly."""
    valid_fields = ["weight", "height", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field. Choose from {valid_fields}"
        )
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose asc/desc")

    data = load_data()
    # Enrich all records first so 'bmi' exists for sorting
    enriched_data = [enrich_patient(r) for r in data.values()]

    sort_order = order == "desc"
    sorted_data = sorted(
        enriched_data, key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    """Creates a new patient record."""
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Save raw input to JSON (id excluded automatically by Pydantic if needed,
    # but kept here for schema compliance)
    data[patient.id] = patient.model_dump()
    save_data(data)

    return {"message": "Patient created successfully"}
