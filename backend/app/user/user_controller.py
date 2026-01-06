from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.errors import error
from .user_service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.post("/signup")
def signup():
    payload = request.get_json(silent=True) or {}
    try:
        user = UserService.signup(
            email=str(payload.get("email", "")),
            password=str(payload.get("password", "")),
            name=payload.get("name"),
            dietary_preferences=payload.get("dietary_preferences")
        )
        return jsonify({"id": user.id, "email": user.email}), 201
    except ValueError as e:
        return error(str(e), 400)

@user_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    try:
        token = UserService.login(
            email=str(payload.get("email", "")),
            password=str(payload.get("password", ""))
        )
        return jsonify({"access_token": token})
    except ValueError as e:
        return error(str(e), 401)

@user_bp.get("/profile")
@jwt_required()
def profile_get():
    try:
        user_id = int(get_jwt_identity())
        return jsonify(UserService.get_profile(user_id))
    except ValueError as e:
        return error(str(e), 404)

@user_bp.put("/profile")
@jwt_required()
def profile_put():
    payload = request.get_json(silent=True) or {}
    try:
        user_id = int(get_jwt_identity())
        updated = UserService.update_profile(
            user_id=user_id,
            name=payload.get("name"),
            dietary_preferences=payload.get("dietary_preferences")
        )
        return jsonify(updated)
    except ValueError as e:
        return error(str(e), 400)
