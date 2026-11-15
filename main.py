import json

from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

def load_data():
    with open("student.json","r") as file:
        return json.load(file)

    

@app.get("/students")
def home():
    return load_data()

@app.get("/students/{student_id}")
def student(student_id : int = Path(...,description="This is student id",example="1")):
    # the path is module imported and path(...) makes its compulsory to do 
    data=load_data()

    for x in data:
        if x["id"]==student_id:
            return x
        
    raise HTTPException(
        status_code=404,
        detail=f"Student with id '{student_id}' doesn't exist "
        )
