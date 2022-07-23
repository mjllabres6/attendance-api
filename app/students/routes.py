from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("students", __name__)


@module.route("/students", methods=["GET"])
def get_students():
    res = StudentManager.get_students()
    return make_response(res)


@module.route("/students", methods=["POST"])
def add_students():
    response, status = StudentManager.create_student(request.form)
    return make_response(jsonify(response)), status


@module.route("/students/<id>", methods=["GET"])
def get_student_by_id(id):
    res = StudentManager.get_student_by_id(id)
    return make_response(res)


@module.route("/students/login", methods=["POST"])
def login_student():
    res, status = StudentManager.login_student(request.form)
    return make_response(res), status
