from __future__ import annotations

from flask import Blueprint, render_template, request
from flask.wrappers import Response

from ..app import spotify
from ..config import Config
from ..lib.supabase import get_user, insert_user, update_user_refresh_token

blueprint = Blueprint("dashboard", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    return render_template("index.html", github_url=Config.GITHUB_URL)


@blueprint.route("/dashboard")
def dashboard() -> str:
    code = request.args.get("code")

    if not code:
        return render_template("error.html", error="No code found, Please login!")

    # Get the refresh & access token from the code
    try:
        token = spotify.get_reresh_token(code)
        access_token = token["access_token"]

        user_id = spotify.get_user_info(access_token)["id"]
    except KeyError:
        return render_template(
            "error.html",
            error="Invalid Spotify OAuth workflow. Please login correctly.",
        )

    # Get the user from the database
    user = get_user(user_id)

    if not user:
        insert_user(
            user_id,
            token["refresh_token"],
            access_token,
            token["expires_in"],
            token["scope"],
        )
    else:
        update_user_refresh_token(user_id, token["refresh_token"])

    return render_template(
        "dashboard.html",
        id=user_id,
        base_url=Config.BASE_URL,
        github_url=Config.GITHUB_URL,
    )


# NOTE: Debug Route - Remove after testing.
@blueprint.route("/error")
def error() -> Response:
    response = Response(
        render_template("error/error-svg.html.j2", error="Test error!"),
        mimetype="image/svg+xml",
    )
    response.headers["Cache-Control"] = "s-maxage=1"

    return response
