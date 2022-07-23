from flask import jsonify, make_response, request, Blueprint
from app.subjects.controllers import SubjectManager

module = Blueprint("subjects", __name__)


@module.route("/subjects", methods=["POST"])
def create_subject():
    json_data = request.get_json(force=True)
    res, status = SubjectManager.create_subject(json_data)
    return make_response(res), status
