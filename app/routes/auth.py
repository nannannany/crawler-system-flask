import configparser
import os

from flask import Blueprint, request, jsonify

bp = Blueprint("auth", __name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "../../config/config.ini"))
bp_login = Blueprint('login', __name__, url_prefix='/api/login')


@bp_login.route("/", methods=["POST"])
def login():
    data = request.get_json()
    password = data.get("password")
    if password == config.get("LOGIN", "loginpassword", fallback="password"):
        return jsonify({"success": True})
    return jsonify({"success": False})
