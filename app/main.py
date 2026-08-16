import os

from flask import Flask, render_template

from app.db import check_connection


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev")

    @app.route("/")
    def index():
        db_status, db_error = check_connection()
        return render_template(
            "index.html",
            db_status=db_status,
            db_error=db_error,
        )

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
