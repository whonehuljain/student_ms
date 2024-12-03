from fastapi import APIRouter, Query, HTTPException, Response, status
from pymongo.collection import Collection
from models.students import Student, Student_Update
from config.db import collection
from schema.schemas import list_serializer
from bson import ObjectId
from typing import Optional

router = APIRouter()

@router.post("/students", status_code=201)
async def create_student(student: Student, response: Response):

    try:
        # print(student)
        student_dict = student.dict(by_alias=True)
        # print(student_dict)
        result = collection.insert_one(dict(student_dict))

        response.status_code = status.HTTP_201_CREATED

        return {"id": str(result.inserted_id)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")



@router.get("/students", status_code=200)
async def get_students_list(age: Optional[int] = Query(None), country: Optional[str] = Query(None)):

    try:
    
        sl_pipeline = []
        if age:
            sl_pipeline.append({"$match": {"age": {"$gte": age}}})
        if country:
            sl_pipeline.append({"$match": {"address.country": country}})

        sl_pipeline.append({
            '$project': {
                "_id":0,
                "name":1,
                "age":1,
            }
        })

        students = list_serializer(collection.aggregate(sl_pipeline))
        return {"data": students}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")




@router.get("/students/{id}", status_code=200)
async def get_student_by_id(id: str, response: Response):

    try:

        pipeline = [{'$match': {'_id': ObjectId(id)}},
                    {'$project': {"_id":0,"name":1,"age":1,"address":1,}}]

        # print(pipeline)
        
        student = list_serializer(collection.aggregate(pipeline))

        response.status_code = status.HTTP_200_OK
        return student[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {str(e)}")



@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_update: Student_Update, response: Response):

    update_data = {}

    if student_update.name is not None:
        update_data['name'] = student_update.name
    
    if student_update.age is not None:
        update_data['age'] = student_update.age
    
    if student_update.address is not None:

        if student_update.address.city is not None:
            update_data['address.city'] = student_update.address.city
        if student_update.address.country is not None:
            update_data['address.country'] = student_update.address.country


    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    try:
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )
        # print(result)

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or no changes made")
        
        response.status_code = status.HTTP_204_NO_CONTENT

        return {}

    
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")
    



@router.delete("/students/{id}")
async def delete_student(id: str):

    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")