from flask import Blueprint, Response, request, render_template

from app import database
from app.config import BASE_URL, GITHUB_URL
from app.utils import generate_token, get_user_info

callback = Blueprint("/callback", __name__, template_folder="templates")


@callback.route("/callback")
def callback_():
    code = request.args.get("code")

    if not code:
        return Response("No code found!")

    try:
        token = generate_token(code)
        access_token = token["access_token"]
        user_id = get_user_info(access_token)["id"]
    except KeyError:
        return Response("Invalid Auth workflow! Please login correctly.")

    database.child("users").child(user_id).set(token)

    return render_template(
        "callback.html",
        id=user_id,
        base_url=BASE_URL,
        github_url=GITHUB_URL
    )
