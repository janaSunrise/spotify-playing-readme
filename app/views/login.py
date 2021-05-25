from flask import Blueprint, redirect, render_template

from app.config import SPOTIFY__LOGIN, GITHUB_URL

login = Blueprint("login", __name__, template_folder="templates")


@login.route("/")
def index():
    return render_template("index.html", github_url=GITHUB_URL)


@login.route("/login")
def login_():
    return redirect(SPOTIFY__LOGIN)
