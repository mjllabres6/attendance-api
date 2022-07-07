from flask import make_response, request, Blueprint, send_file
from app.classes.controllers import ClassManager

module = Blueprint("classes", __name__)


@module.route("/classes", methods=["POST"])
def create_class():
    res = ClassManager.create_class(request.form)
    return make_response(res)


@module.route("/classes/<id>", methods=["GET"])
def get_class_qr(id):

    res = ClassManager.produce_qr(id)

    return send_file(res, mimetype="image/gif")


@module.route("/classes/<code>", methods=["GET"])
def reg_qr(code):

    res = ClassManager.register_attendance()
    return make_response(res)
