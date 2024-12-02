def student_serializer(student: dict) -> dict:
    serialized_student = {}

    if "_id" in student:
        serialized_student["id"] = str(student["_id"])
    if "name" in student:
        serialized_student["name"] = student["name"]
    if "age" in student:
        serialized_student["age"] = student["age"]
    if "address" in student:
        serialized_student["address"] = student["address"]

    return serialized_student


def list_serializer(students) -> list:
    return [student_serializer(student) for student in students]