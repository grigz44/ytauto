from flask import Blueprint, redirect, render_template, request, url_for

from app import repo
from app.db import get_db

bp = Blueprint("settings", __name__, url_prefix="/settings")


@bp.route("/", methods=["GET", "POST"])
def settings_form():
    conn = get_db()
    if request.method == "POST":
        repo.update_settings(
            conn,
            language=request.form.get("language", "en").strip(),
            tone=request.form.get("tone", "engaging").strip(),
            default_duration_seconds=int(request.form.get("default_duration_seconds") or 40),
            daily_limit=int(request.form.get("daily_limit") or 1),
            publish_time=request.form.get("publish_time", "19:00").strip(),
            timezone=request.form.get("timezone", "Asia/Kolkata").strip(),
            auto_publish=request.form.get("auto_publish") == "on",
        )
        return redirect(url_for("settings.settings_form"))
    settings = repo.get_settings(conn)
    return render_template("settings/form.html", settings=settings)
