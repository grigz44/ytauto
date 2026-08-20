from flask import Blueprint, abort, redirect, render_template, request, url_for

from app import repo
from app.db import get_db

bp = Blueprint("topics", __name__, url_prefix="/topics")


@bp.route("/")
def list_topics():
    topics = repo.list_topics(get_db())
    return render_template("topics/list.html", topics=topics)


@bp.route("/new", methods=["GET", "POST"])
def new_topic():
    if request.method == "POST":
        repo.create_topic(
            get_db(),
            name=request.form["name"].strip(),
            description=request.form.get("description", "").strip() or None,
            style=request.form.get("style", "").strip() or None,
            tone=request.form.get("tone", "").strip() or None,
            duration_seconds=int(request.form.get("duration_seconds") or 40),
        )
        return redirect(url_for("topics.list_topics"))
    return render_template("topics/form.html", topic=None)


@bp.route("/<uuid:topic_id>/edit", methods=["GET", "POST"])
def edit_topic(topic_id):
    conn = get_db()
    topic_id = str(topic_id)
    if request.method == "POST":
        repo.update_topic(
            conn,
            topic_id=topic_id,
            name=request.form["name"].strip(),
            description=request.form.get("description", "").strip() or None,
            style=request.form.get("style", "").strip() or None,
            tone=request.form.get("tone", "").strip() or None,
            duration_seconds=int(request.form.get("duration_seconds") or 40),
        )
        return redirect(url_for("topics.list_topics"))
    topic = repo.get_topic(conn, topic_id)
    if topic is None:
        abort(404)
    return render_template("topics/form.html", topic=topic)


@bp.route("/<uuid:topic_id>/toggle", methods=["POST"])
def toggle_topic(topic_id):
    conn = get_db()
    topic_id = str(topic_id)
    topic = repo.get_topic(conn, topic_id)
    if topic is None:
        abort(404)
    repo.set_topic_active(conn, topic_id, not topic["active"])
    return redirect(url_for("topics.list_topics"))
