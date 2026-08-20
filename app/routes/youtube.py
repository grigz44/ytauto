from flask import Blueprint, render_template

from app import repo
from app.db import get_db

bp = Blueprint("youtube_account", __name__, url_prefix="/youtube")


@bp.route("/")
def status():
    account = repo.get_youtube_account(get_db())
    return render_template("youtube/index.html", account=account)
