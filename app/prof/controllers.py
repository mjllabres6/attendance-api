from app import db
import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
import pymongo


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
            return {"message": "Successfully created prof record."}, 200
        except pymongo.errors.DuplicateKeyError:
            return {"message": "You have entered an existing prof code."}, 200
        except Exception:
            return {"message": "There was a problem creating prof record"}, 200

    @classmethod
    def login_prof(cls, body):
        prof_body = {
            "prof_code": body.get("prof_code"),
            "password": body.get("password"),
        }

        prof = db.prof.find_one(
            {"prof_code": prof_body["prof_code"], "password": prof_body["password"]}
        )
        if prof:
            return {"message": "Found a match on a prof record.", "name": prof["name"]}, 200

        return {"message": "Invalid login credentials."}, 200
