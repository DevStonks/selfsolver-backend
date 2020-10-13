"""Provide routes for user authentication."""
from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import fields, Schema, ValidationError
from selfsolver.models import User
from selfsolver.password import verify

auth = Blueprint("auth", __name__)


class LoginSchema(Schema):
    """Schema for login request data."""

    email = fields.Email(required=True)
    password = fields.String(required=True)


@auth.route("/login", methods=["POST"])
def login():
    """Check request credentials and return a JWT."""
    if not request.is_json:
        abort(400)

    try:
        data = LoginSchema().load(request.json)
    except ValidationError:
        abort(400)

    email, password = data["email"], data["password"]

    if not email or not password:
        abort(400)

    user = User.query.filter(User.email == email).first()

    if not user or not verify(password, user.password):
        abort(401)

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)
