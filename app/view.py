import base64
import random

import requests
from flask import Blueprint, Response, render_template, request, redirect

from .utils import get_recently_played, get_now_playing, get_access_token

view = Blueprint("/view", __name__, template_folder="templates")


def generate_bar(bar_count=75):
    css_bar = ""
    left = 1

    for i in range(1, bar_count + 1):
        anim = random.randint(300, 600)
        css_bar += f".bar:nth-child({i})  {{ left: {left}px; animation-duration: {anim}ms; }}"
        left += 4

    return css_bar


def load_image_b64(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode("ascii")


def make_svg(item, theme, is_now_playing):
    currently_playing_type = item.get("currently_playing_type", "track")

    img = ""
    artist_name = ""
    song_name = ""

    if currently_playing_type == "track":
        img = load_image_b64(item["album"]["images"][1]["url"])
    elif currently_playing_type == "episode":
        img = load_image_b64(item["images"][1]["url"])

    if currently_playing_type == "track":
        artist_name = item["artists"][0]["name"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")
    elif currently_playing_type == "episode":
        artist_name = item["show"]["publisher"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")

    height = 0
    num_bar = 75

    if theme == "plain":
        height = 90
        num_bar = 40
    elif theme == "wavy":
        height = 120
        num_bar = 85

    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)])

    if is_now_playing:
        title_text = "Vibing to:"
    else:
        title_text = "Was listening to:"
        content_bar = ""

    css_bar = generate_bar(num_bar)

    rendered_data = {
        "height": height,
        "num_bar": num_bar,
        "content_bar": content_bar,
        "css_bar": css_bar,
        "status": title_text,
        "artist_name": artist_name,
        "song_name": song_name,
        "img": img,
        "is_now_playing": is_now_playing
    }

    return render_template(f"spotify.{theme}.html.j2", **rendered_data)


@view.route("/view")
def render_img():
    def get_song_info(uid):
        access_token = get_access_token(uid)
        data = get_now_playing(access_token)

        if data:
            item = data["item"]
            item["currently_playing_type"] = data["currently_playing_type"]
            is_now_playing = True
        else:
            recent_plays = get_recently_played(access_token)
            size_recent_play = len(recent_plays["items"])
            idx = random.randint(0, size_recent_play - 1)
            item = recent_plays["items"][idx]["track"]
            item["currently_playing_type"] = "track"
            is_now_playing = False

        return item, is_now_playing

    uid = request.args.get("id")
    theme = request.args.get("theme", default="plain")
    item, is_now_playing = get_song_info(uid)

    svg = make_svg(item, theme, is_now_playing)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
