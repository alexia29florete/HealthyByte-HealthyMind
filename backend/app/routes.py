from flask import Flask, jsonify
from .user.user_controller import user_bp
from .journal.journal_controller import journal_bp
from .stats.stats_controller import stats_bp

def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(stats_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})
