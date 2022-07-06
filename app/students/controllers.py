from app import db
import json
from flask import jsonify
from bson.objectid import ObjectId


class StudentManager(object):
    @classmethod
    def get_students(cls):
        data = list(db.students.find())
        for student in data:
            student["_id"] = str(student["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_student_by_id(cls, id):
        data = db.students.find_one({"_id": ObjectId(id)})
        print(data)
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})

    @classmethod
    def create_student(cls, body):
        user_body = {
            "sr-code": body.get("sr-code"),
            "name": body.get("name"),
            "subjects": body.get("subjects"),
            "classes": body.get("classes"),
        }

        try:
            db.students.insert_one(user_body)
            return {"message": "Sucessfully created student record."}
        except Exception as e:
            print(e)
            return {"message": "There was a problem creating the student record."}
