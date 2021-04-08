import base64
import random

import requests
from flask import Blueprint, Response, render_template, request
from memoization import cached

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


@cached(ttl=5, max_size=128)
def make_svg(item, theme, is_now_playing):
    currently_playing_type = item.get("currently_playing_type", "track")

    img, artist_name, song_name = "", "", ""

    title_text_mapping = {
        True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
        False: ["Was listening to", "Previously binging to", "Was vibing to"]
    }

    theme_mapping = {
        "plain": {
            "height": 90,
            "num_bar": 40
        },
        "wavy": {
            "height": 120,
            "num_bar": 85
        },
        None: {
            "height": 40,
            "num_bar": 30
        }
    }

    if currently_playing_type == "track":
        img = load_image_b64(item["album"]["images"][1]["url"])
        artist_name = item["artists"][0]["name"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")
    elif currently_playing_type == "episode":
        img = load_image_b64(item["images"][1]["url"])
        artist_name = item["show"]["publisher"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")

    height = theme_mapping[theme]["height"]
    num_bar = theme_mapping[theme]["num_bar"]
    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)])
    css_bar = generate_bar(num_bar)

    if is_now_playing:
        title_text = random.choice(title_text_mapping[True]) + ":"
    else:
        title_text = random.choice(title_text_mapping[False]) + ":"
        content_bar = ""

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


@view.route("/spotify")
def render_img():
    def get_song_info(user_id):
        access_token = get_access_token(user_id)
        data = get_now_playing(access_token)

        if data is not None and data != {}:
            item = data["item"]
            item["currently_playing_type"] = data["currently_playing_type"]
            is_now_playing = data["is_playing"]
        else:
            recent_plays = get_recently_played(access_token)
            size_recent_play = len(recent_plays["items"])
            idx = random.randint(0, size_recent_play - 1)

            item = recent_plays["items"][idx]["track"]
            item["currently_playing_type"] = "track"
            is_now_playing = data["is_playing"]

        return item, is_now_playing

    user_id = request.args.get("id")
    theme = request.args.get("theme", default="plain")
    item, is_now_playing = get_song_info(user_id)

    # Generate the SVG
    svg = make_svg(item, theme, is_now_playing)

    # Generate the response with the SVG
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
