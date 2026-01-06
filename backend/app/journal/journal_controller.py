from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.errors import error
from .journal_service import JournalService

journal_bp = Blueprint("journal", __name__, url_prefix="/journal")

@journal_bp.post("")
@jwt_required()
def create_entry():
    payload = request.get_json(silent=True) or {}
    try:
        user_id = int(get_jwt_identity())
        created = JournalService.create_entry(
            user_id=user_id,
            entry_text=str(payload.get("entry_text", "")),
            entry_date=payload.get("date")
        )
        return jsonify(created), 201
    except ValueError as e:
        return error(str(e), 400)

@journal_bp.get("")
@jwt_required()
def list_entries():
    try:
        user_id = int(get_jwt_identity())
        limit = int(request.args.get("limit", 50))
        offset = int(request.args.get("offset", 0))
        data = JournalService.list_entries(user_id, limit=limit, offset=offset)
        return jsonify({"items": data, "limit": limit, "offset": offset})
    except ValueError as e:
        return error(str(e), 400)

@journal_bp.get("/<int:entry_id>")
@jwt_required()
def get_entry(entry_id: int):
    try:
        user_id = int(get_jwt_identity())
        return jsonify(JournalService.get_entry(user_id, entry_id))
    except ValueError as e:
        return error(str(e), 404)

@journal_bp.delete("/<int:entry_id>")
@jwt_required()
def delete_entry(entry_id: int):
    try:
        user_id = int(get_jwt_identity())
        JournalService.delete_entry(user_id, entry_id)
        return jsonify({"deleted": True})
    except ValueError as e:
        return error(str(e), 404)
