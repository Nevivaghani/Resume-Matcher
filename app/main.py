from fastapi import FastAPI
from app.routes import resume

app = FastAPI()

app.include_router(resume.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Resume API"}

