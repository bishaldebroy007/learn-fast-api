# Learn FastAPI

A project for learning FastAPI from scratch.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install "fastapi[standard]"
```

### 4. (Optional) Regenerate requirements.txt

```bash
pip freeze > requirements.txt
```

## Running the app

```bash
uvicorn main:app --reload
```
