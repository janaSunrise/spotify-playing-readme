from flask import Blueprint, redirect
from werkzeug.wrappers.response import Response

from ..config import Config
from ..utils.oauth import generate_oauth_url

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login")
def login() -> Response:
    return redirect(
        generate_oauth_url(
            Config.SPOTIFY_CLIENT_ID, Config.REDIRECT_URI, Config.SPOTIFY_SCOPES
        )
    )
