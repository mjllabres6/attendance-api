import csv
import qrcode
import uuid
from flask import jsonify
from app import db
from datetime import datetime, timedelta
from io import BytesIO


class ClassManager(object):
    @classmethod
    def create_class(cls, body):
        code = str(uuid.uuid4())
        subject_body = {
            "subject_id": body.get("subject_id"),
            "duration": body.get("duration"),
        }

        expiry = datetime.now() + timedelta(hours=int(subject_body.pop("duration")))

        subject_body.update({"code": code, "expires_at": expiry})

        try:
            db.classes.insert_one(subject_body)
            return {"code": code}
        except Exception:
            return {"message": "There was a problem creating the class."}

    @classmethod
    def produce_qr(cls, id):

        buffer = BytesIO()

        img = qrcode.make(str(id))
        img.save(buffer)
        buffer.seek(0)
        return buffer

    @classmethod
    def register_attendance(cls):
        return "sample"

    @classmethod
    def get_classes(cls):
        data = list(db.classes.find())
        for student in data:
            student["_id"] = str(student["_id"])
        return jsonify({"data": data})
