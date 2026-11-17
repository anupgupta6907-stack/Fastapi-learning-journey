import json

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

def load_data():
    with open("student.json","r") as file:
        return json.load(file)

    

@app.get("/students")
def home():
    return load_data()


# path parameter
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

#Query Parameter
@app.get("/filter")
def filter_course(course:str = Query(None)):
    data = load_data()

    if course is None:
        return data

    
    filtered_data=[]
    for x in data:
        if x["course"]==course:
            filtered_data.append(x)
    return filtered_data


