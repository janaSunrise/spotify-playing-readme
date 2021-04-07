from flask import Blueprint, Response, request, render_template

from .config import BASE_URL
from .utils import generate_token, get_user_info

callback = Blueprint("/callback", __name__, template_folder="templates")


@callback.route("/callback")
def cb():
    code = request.args.get("code")

    if not code:
        return Response("No code!")

    access_token = generate_token(code)["access_token"]
    user_id = get_user_info(access_token)["id"]

    return render_template(
        "cb.html.j2",
        id=user_id,
        base_url=BASE_URL,
    )
