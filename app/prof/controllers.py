from app import db
import json
from flask import jsonify
from bson.objectid import ObjectId


class ProfManager(object):
    @classmethod
    def get_prof_by_id(cls, id):
        data = db.prof.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})

    @classmethod
    def create_prof(cls, body):
        prof_body = {
            "name": body.get("name"),
            "prof_code": body.get("prof_code"),
            "password": body.get("password"),
        }

        try:
            db.prof.insert_one(prof_body)
            return {"message": "Sucessfully created prof record."}
        except Exception as e:
            print(e)
            return {"message": "There was a problem creating the prof record."}

    @classmethod
    def login_prof(cls, body):
        prof_body = {
            "prof_code": body.get("prof_code"),
            "password": body.get("password"),
        }

        student = db.prof.find_one(
            {"srcode": prof_body["srcode"], "password": prof_body["password"]}
        )
        if student:
            return {"message": "Found a match on a student record."}

        return {"message": "Invalid login credentials."}
