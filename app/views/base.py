from flask import Blueprint, render_template

from app.config import GITHUB_URL

base = Blueprint("base", __name__, template_folder="templates")


@base.route("/")
def index():
    return render_template("index.html", github_url=GITHUB_URL)
