from fastapi import FastAPI
from app.routers import students

app = FastAPI(title="EduVerse AI Backend")

@app.get("/")
def root():
    return {"message" : "Success !"}

app.include_router(students.router)