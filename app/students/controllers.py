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
            "srcode": body.get("srcode"),
            "name": body.get("name"),
            "password": body.get("password"),
        }

        try:
            db.students.insert_one(user_body)
            return {"message": "Sucessfully created student record."}
        except Exception as e:
            return {"message": "There was a problem creating the student record."}

    @classmethod
    def login_student(cls, body):
        user_body = {"srcode": body.get("srcode"), "password": body.get("password")}

        student = db.students.find_one(
            {"srcode": user_body["srcode"], "password": user_body["password"]}
        )
        if student:
            return {"message": "Found a match on a student record."}

        return {"message": "Invalid login credentials."}
