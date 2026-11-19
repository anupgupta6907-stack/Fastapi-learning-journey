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


# Sorted
Sort_fields =["age","name"]
Field_order =["asc","desc"]
@app.get("/sort")
def sort(sort_by :str ,order:str):
    if sort_by not in Sort_fields:
        raise HTTPException(status_code=404,detail=f"Invalid Sorting , Select Sort from {Sort_fields}")

    if order not in Field_order:
            raise HTTPException(status_code=404,detail=f"Invalid Sorting order ,Select from {Sort_fields}")

    data = load_data()
    reverse =(order =="desc")
    sorted_students = sorted(data,key=lambda x:x[sort_by],reverse=reverse)

    return sorted_students


# pagination
@app.get("/paginate") 
def paginate_student(page:int =Query(1,ge=1,description="Which apge you want (start from 1)") , limit : int=Query(10,ge=1,le=100,description="How many students on one page you want(start from 1) ")):
    data = load_data()

    start = (page-1)*limit
    end = start + limit

    page_student = data[start:end]

    return{
        "Page":page,
        "Limit": limit,
        "students" :page_student
    }
