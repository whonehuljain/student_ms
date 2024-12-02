from fastapi import APIRouter, Query, HTTPException, Response, status
from pymongo.collection import Collection
from models.students import Student, Student_Update
from config.db import collection
from schema.schemas import list_serializer
from bson import ObjectId
from typing import Optional

router = APIRouter()

@router.post("/students")
async def create_student(student: Student):
    # print(student)
    student_dict = student.dict(by_alias=True)
    # print(student_dict)
    result = collection.insert_one(dict(student_dict))
    return {"id": str(result.inserted_id)}



@router.get("/students")
async def get_students_list(age: Optional[int] = Query(None), country: Optional[str] = Query(None)):
    
    pipeline = []
    if age:
        pipeline.append({"$match": {"age": {"$gte": age}}})
    if country:
        pipeline.append({"$match": {"address.country": country}})

    pipeline.append({
        '$project': {
            "_id":0,
            "name":1,
            "age":1,
        }
    })

    students = list_serializer(collection.aggregate(pipeline))
    return {"data": students}



@router.get("/students/{id}")
async def get_student_by_id(id: str):

    pipeline = []

    pipeline.append({'$match': {'_id': ObjectId(id)}})


    pipeline.append({
        '$project': {
            "_id":0,
            "name":1,
            "age":1,
            "address":1,
        }
    })

    print(pipeline)
    student = list_serializer(collection.aggregate(pipeline))
    json_student = student[0]
    return json_student



@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_update: Student_Update, response: Response):

    update_data = {}

    if student_update.name is not None:
        update_data['name'] = student_update.name
    
    if student_update.age is not None:
        update_data['age'] = student_update.age
    
    if student_update.address is not None:

        update_data['address'] = {}
        if student_update.address.get('city') is not None:
            update_data['address.city'] = student_update.address['city']
        
        if student_update.address.get('country') is not None:
            update_data['address.country'] = student_update.address['country']


    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or no changes made")
        
        response.status_code = status.HTTP_204_NO_CONTENT

        return {}

    
    except Exception as e:
        print(f"Update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")
    



@router.delete("/students/{id}")
async def delete_student(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {}