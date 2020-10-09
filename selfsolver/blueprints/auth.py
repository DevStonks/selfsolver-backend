from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from selfsolver import password
from selfsolver.models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        abort(400)

    email = request.json.get("email", None)
    passwd = request.json.get("password", None)

    if not email or not password:
        abort(400)

    user = User.query.filter(User.email == email).first()
    if user and password.verify(passwd, user.password):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)
