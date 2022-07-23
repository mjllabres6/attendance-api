from flask import Blueprint
from flask import jsonify, make_response, request
from app.prof.controllers import ProfManager
from flask import url_for

from app.subjects.controllers import SubjectManager

module = Blueprint("prof", __name__)


@module.route("/prof", methods=["POST"])
def add_prof():
    response, status = ProfManager.create_prof(request.form)
    return make_response(jsonify(response)), status


@module.route("/prof/<id>", methods=["GET"])
def get_prof_by_id(id):
    res = ProfManager.get_student_by_id(id)
    return make_response(res)


@module.route("/prof/<id>/subjects", methods=["GET"])
def get_subjects_by_prof(id):
    res = SubjectManager.get_subject_by_prof(id)
    return make_response(res)


@module.route("/prof/login", methods=["POST"])
def login_prof():
    res, status = ProfManager.login_prof(request.form)
    return make_response(res), status
