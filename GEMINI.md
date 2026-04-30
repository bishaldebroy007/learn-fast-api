# Project Overview: Learn FastAPI - Patient Management System

This project is a learning resource for FastAPI, focused on building a Patient Management System. It demonstrates core FastAPI features such as Pydantic models, data validation, computed fields, and basic CRUD operations with JSON file persistence.

## Core Technologies
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/latest/)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Storage:** Local JSON file (`patient.json`)

## Architecture
The application is a single-file API (`main.py`) that uses a Pydantic model (`Patient`) to define the data structure. It includes computed fields for BMI calculation and health status verdict. Data is loaded from and saved to `patient.json` using helper functions.

---

## Building and Running

### Prerequisites
- Python 3.10+
- `pip`

### Setup
1. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   ```
2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install "fastapi[standard]"
   # Or using requirements.txt
   pip install -r requirements.txt
   ```

### Running the Application
Start the development server with auto-reload:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
- **Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## Development Conventions

### Data Modeling
- **Pydantic Models:** Always use Pydantic `BaseModel` for request/response bodies.
- **Annotated Types:** Use `typing.Annotated` with `Field` for detailed metadata and validation rules (e.g., `gt`, `lt`, `description`).
- **Computed Fields:** Use `@computed_field` for derived data that should be included in the API response but not required in the input.

### API Design
- **Endpoints:**
    - `GET /view`: Retrieve all patient records.
    - `GET /patient/{id}`: Retrieve a specific patient by ID.
    - `GET /sort`: Sort patients by `height`, `weight`, or `bmi`.
    - `POST /create`: Create a new patient record.
- **Status Codes:**
    - `201 Created` for successful creation.
    - `400 Bad Request` for validation errors or existing records.
    - `404 Not Found` for missing records.
- **Error Handling:** Use `fastapi.HTTPException` for consistent error responses.

### File Structure
- `main.py`: Contains the FastAPI app instance, Pydantic models, and route handlers.
- `patient.json`: Acts as a simple database. Ensure this file is writable by the application.
- `pydantic.md` & `post-request.md`: Contain detailed learning notes and examples related to the project.
