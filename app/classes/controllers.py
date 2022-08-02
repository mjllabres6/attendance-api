import csv
from bson import ObjectId
import qrcode
import uuid
from flask import jsonify
from app import db
from datetime import datetime, timedelta
from io import BytesIO
import xlsxwriter
from app.students.controllers import StudentManager
import csv
from datetime import date

class ClassManager(object):
    @classmethod
    def create_class(cls, body):
        code = str(uuid.uuid4())
        today = date.today()
        subject_body = {
            "subject_name": body.get("subject_name"),
            "duration": body.get("duration"),
            "date": today.strftime("%B %d, %Y"),
            "prof_code": body.get("prof_code"),
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
    def register_attendance(cls, code, body):
        current_class = db.classes.find_one({"code": code})
        if current_class:
            if current_class["expires_at"] < datetime.now():
                return {"message": "Class attendance has expired."}

            attended = db.attendance.find_one(
                {"class_code": code, "srcode": body.get("srcode")}
            )
            if attended:
                return {"message": "You have already attended this class."}

            clss = db.classes.find_one({"code": code})
            subject = db.subjects.find_one({"name": clss["subject_name"]})
            prof = db.prof.find_one({"prof_code": clss["prof_code"]})

            today = date.today()
            db.attendance.insert_one(
                {"class_code": code, "srcode": body.get("srcode"), "subject": subject["name"], "date": today.strftime("%B %d, %Y"), "prof_name": prof["name"]}
            )
            return {"message": "Class attendance has been registered"}

        else:
            return {"message": "Invalid class code was scanned"}

    @classmethod
    def get_classes(cls):
        data = list(db.classes.find())
        for student in data:
            student["_id"] = str(student["_id"])
        return jsonify({"data": data})
    
    @classmethod
    def get_student_count(cls, code):
        data = db.attendance.count_documents({"class_code": code})
        return {"count": data}
    
    @classmethod
    def get_student_attendance(cls, srcode):
        data = list(db.attendance.find({"srcode": srcode}))
        for attendance in data:
            attendance["_id"] = str(attendance["_id"])
        return {"results": data}
    
    @classmethod
    def get_prof_classes(cls, srcode):
        data = list(db.classes.find({"prof_code": srcode}))
        for attendance in data:
            attendance["_id"] = str(attendance["_id"])
        return {"results": data}
    
    @classmethod
    def export_as_excel(cls, code):
        import io
        data = list(db.attendance.find({"class_code": code}))
        srcode = ""
        name = ""

        proxy = io.StringIO()
        
        writer = csv.writer(proxy)
        writer.writerow(['SR-CODE', 'NAME'])

        for student in data:
            name = StudentManager.get_student_by_code(student["srcode"])["name"]
            writer.writerow([student["srcode"], name])

        mem = io.BytesIO()
        mem.write(proxy.getvalue().encode())
        mem.seek(0)
        proxy.close()
        return mem