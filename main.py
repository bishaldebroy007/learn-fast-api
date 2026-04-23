from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Decorator

@app.get("/") ## root directories
def read_root():
    return {"Python": "API"}


@app.get("/aiquest")
def aiquest():
    return {"AI": "QUEST"}

@app.get("/python")
def python():
    return {"Python": "xyz."}

