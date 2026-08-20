from flask import Blueprint, abort, render_template

from app import repo
from app.db import get_db

bp = Blueprint("shorts", __name__, url_prefix="/shorts")


@bp.route("/")
def list_shorts():
    shorts = repo.list_shorts(get_db())
    return render_template("shorts/list.html", shorts=shorts)


@bp.route("/<uuid:short_id>")
def short_detail(short_id):
    short = repo.get_short(get_db(), str(short_id))
    if short is None:
        abort(404)
    return render_template("shorts/detail.html", short=short)
