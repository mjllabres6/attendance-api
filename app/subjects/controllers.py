from msilib.schema import Error
from app import db
import json
from bson.objectid import ObjectId


class SubjectManager(object):
    @classmethod
    def create_subject(cls, body):
        subject_body = {
            "name": body.get("name"),
            "prof_id": body.get("prof_id"),
        }

        try:
            db.subjects.insert_one(subject_body)
            return {"message": "Sucessfully created subject."}
        except Exception as e:
            return {"message": "There was a problem creating the subject."}
