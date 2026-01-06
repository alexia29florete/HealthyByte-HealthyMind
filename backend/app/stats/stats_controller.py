from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.errors import error
from .statistics_service import compute_summary

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")

@stats_bp.get("/summary")
@jwt_required()
def summary():
    try:
        user_id = int(get_jwt_identity())
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        return jsonify(compute_summary(user_id, date_from=date_from, date_to=date_to))
    except Exception as e:
        return error(str(e), 400)
