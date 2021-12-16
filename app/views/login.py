from flask import Blueprint, redirect, render_template

from app.config import GITHUB_URL, SPOTIFY__LOGIN

login = Blueprint("login", __name__, template_folder="templates")


@login.route("/")
def index():
    return render_template("index.html", github_url=GITHUB_URL)


@login.route("/login")
def login_():
    return redirect(SPOTIFY__LOGIN)