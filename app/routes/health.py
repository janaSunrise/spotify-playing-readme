from flask import Blueprint, jsonify
from flask.wrappers import Response

blueprint = Blueprint("health", __name__)


@blueprint.route("/health")
def health() -> Response:
    return jsonify({"status": "OK"})
