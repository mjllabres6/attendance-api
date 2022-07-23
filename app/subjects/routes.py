from flask import jsonify, make_response, request, Blueprint
from app.subjects.controllers import SubjectManager

module = Blueprint("subjects", __name__)


@module.route("/subjects", methods=["POST"])
def create_subject():
    res, status = SubjectManager.create_subject(request.form)
    return make_response(res), status
