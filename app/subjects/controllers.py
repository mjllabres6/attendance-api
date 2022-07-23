from msilib.schema import Error
from app import db
import json
from bson.objectid import ObjectId
from flask import jsonify
import pymongo


class SubjectManager(object):
    @classmethod
    def create_subject(cls, body):
        subject_body = {
            "name": body.get("name"),
            "prof_id": body.get("prof_id"),
        }

        try:
            db.subjects.insert_one(subject_body)
            return {"message": "Successfully created subject."}, 200
        except pymongo.errors.DuplicateKeyError:
            return {"message": "You have entered an existing subject."}, 500
        except Exception:
            return {"message": "There was a problem creating subject record"}, 500

    @classmethod
    def get_subject_by_prof(cls, id):
        data = list(db.subjects.find({"prof_id": id}))
        for subject in data:
            subject["_id"] = str(subject["_id"])
        return jsonify({"data": data})
