from flask import Blueprint, redirect

from .config import SPOTIFY__LOGIN

login = Blueprint("login", __name__)


@login.route("/login")
def login_():
    return redirect(SPOTIFY__LOGIN)
