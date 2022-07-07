import pymongo
from flask import Flask, Blueprint
from app import modules
from flask import url_for
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
try:
    conn = pymongo.MongoClient(host="localhost", port=27017)
    db = conn.attendance
except:
    print("An error has occurred while trying to connect to the database.")


module = Blueprint("/", __name__)


@module.route("/")
def ping():
    return "Root"


modules.register()
