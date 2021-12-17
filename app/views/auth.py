from flask import Blueprint, Response, redirect, render_template, request

from app import database
from app.config import BASE_URL, GITHUB_URL, SPOTIFY__LOGIN
from app.utils import generate_token, get_user_info

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login")
def login():
    return redirect(SPOTIFY__LOGIN)


@auth.route("/callback")
def callback():
    # Get the code.
    code = request.args.get("code")

    # Handle if code does not exist.
    if not code:
        return Response("No code found!")

    # Get the access token.
    try:
        token = generate_token(code)
        access_token = token["access_token"]

        user_id = get_user_info(access_token)["id"]
    except KeyError:
        return Response("Invalid Auth workflow! Please login correctly.")

    # Save the user in the database.
    database.child("users").child(user_id).set(token)

    # Render the callback template.
    return render_template(
        "callback.html",
        id=user_id,
        base_url=BASE_URL,
        github_url=GITHUB_URL
    )
