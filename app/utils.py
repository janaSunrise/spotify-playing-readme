import base64
from time import time

import requests
from flask import Response
from memoization import cached

from . import database
from .config import (
    SPOTIFY__REFRESH_TOKEN, SPOTIFY__GENERATE_TOKEN,
    SPOTIFY__NOW_PLAYING, SPOTIFY__RECENTLY_PLAYED,
    SPOTIFY__USER_INFO,
    SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID,
    REDIRECT_URI
)


def get_refresh_token(refresh_token):
    headers = {
        "Authorization": f"Basic {generate_base64_auth(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID)}"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(SPOTIFY__REFRESH_TOKEN, data=payload, headers=headers)
    return response.json()


def generate_token(authorization_code):
    headers = {"Authorization": f"Basic {generate_base64_auth(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID)}"}
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(SPOTIFY__GENERATE_TOKEN, data=payload, headers=headers)
    return response.json()


@cached(ttl=60, max_size=128)
def generate_base64_auth(client_id, client_secret):
    return base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("utf-8")


def get_now_playing(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY__NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}

    return response.json()


def get_recently_played(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY__RECENTLY_PLAYED, headers=headers)

    if response.status_code == 204:
        return {}

    return response.json()


@cached(ttl=5, max_size=128)
def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY__USER_INFO, headers=headers)
    return response.json()


@cached(ttl=5, max_size=128)
def get_access_token(uid):
    user = database.child("users").child(uid).get()

    if not user:
        return Response("User doesn't exist. Please login first.")

    token_info = user.val()

    current_time = int(time())
    access_token = token_info["access_token"]
    expired_time = token_info.get("expired_time")

    if expired_time is None or current_time >= expired_time:
        refresh_token = token_info["refresh_token"]
        new_token = get_refresh_token(refresh_token)
        expired_time = int(time()) + new_token["expires_in"]

        update_data = {"access_token": new_token["access_token"], "expired_time": expired_time}

        database.child("users").child(uid).update(update_data)

        access_token = new_token["access_token"]

    return access_token

