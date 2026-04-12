from fastapi import FastAPI

app = FastAPI()

# Decorator

@app.get("/") ## root directories

def read_root():
    return {"Python": "API"}


