import base64
import random
from textwrap import dedent

import requests
from flask import Blueprint, Response, escape, render_template, request
from memoization import cached

from app.utils import get_recently_played, get_now_playing, get_access_token
from app.themes import THEMES

view = Blueprint("view", __name__, template_folder="templates")


@cached(ttl=60, max_size=128)
def generate_bar(bar_count=75):
    css_bar = ""
    left = 1

    for i in range(1, bar_count + 1):
        anim = random.randint(300, 600)
        css_bar += dedent(f"""
        .bar:nth-child({i}) {{
            left: {left}px;
            animation-duration: {anim}ms;
        }}
        """)
        left += 4

    return css_bar


@cached(ttl=5, max_size=128)
def load_image_b64(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode("ascii")


@cached(ttl=5, max_size=128)
def make_svg(item, info):
    theme = info["theme"]
    is_now_playing = info["is_now_playing"]
    needs_cover_image = info["needs_cover_image"]
    bars_when_not_listening = info["bars_when_not_listening"]
    hide_status = info["hide_status"]

    color_theme = info["color_theme"]

    currently_playing_type = item.get("currently_playing_type", "track")

    # Initialize the variables on a function-global scope
    img, artist_name, song_name, explicit = "", "", "", False

    # Get the info
    if currently_playing_type == "track":
        img = load_image_b64(item["album"]["images"][1]["url"])
        artist_name = item["artists"][0]["name"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")
    elif currently_playing_type == "episode":
        img = load_image_b64(item["images"][1]["url"])
        artist_name = item["show"]["publisher"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")

    # Mappings
    title_text_mapping = {
        True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
        False: ["Was listening to", "Previously binging to", "Was vibing to"]
    }

    theme_mapping = {
        "plain": {
            "width": 350,
            "height": 140,
            "num_bar": 40
        },
        "wavy": {
            "width": 480,
            "height": 175,
            "num_bar": 90
        },
        None: {
            "width": 150,
            "height": 75,
            "num_bar": 15
        }
    }

    is_explicit = item["explicit"]

    height = theme_mapping[theme]["height"]
    width = theme_mapping[theme]["width"]
    num_bar = theme_mapping[theme]["num_bar"]

    # THEME MAPPING
    if color_theme not in THEMES:
        color_theme = "none"

    bg_color = THEMES[color_theme]["bg_color"]
    title_color = THEMES[color_theme]["title_color"]
    text_color = THEMES[color_theme]["text_color"]

    # ------------- Default Matching ------------- #
    if info["title_color"] != "":
        title_color = info["title_color"]

    if info["text_color"] != "":
        text_color = info["text_color"]

    if info["bg_color"] != "":
        bg_color = info["bg_color"]

    if bg_color == "":
        bg_color = "white"
    # -------------------------------------------- #

    if title_color == "" and text_color == "":
        text_color, title_color = "#212122", "#212122"
    elif title_color == "" and text_color != "":
        title_color = text_color
    elif title_color != "" and text_color == "":
        text_color = title_color

    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)])
    css_bar = generate_bar(num_bar)

    if is_now_playing:
        title_text = random.choice(title_text_mapping[True]) + ":"
    else:
        title_text = random.choice(title_text_mapping[False]) + ":"
        if not bars_when_not_listening:
            content_bar = ""

    rendered_data = {
        "width": width,
        "height": height,

        "num_bar": num_bar,
        "content_bar": content_bar,
        "css_bar": css_bar,

        "status": title_text,

        "artist_name": artist_name,
        "song_name": song_name,
        "img": img,
        "is_now_playing": is_now_playing,
        "explicit": is_explicit,

        "show_animation": len(song_name) > 27,
        "needs_cover_image": needs_cover_image,
        "hide_status": hide_status,

        "bg_color": bg_color,
        "title_color": title_color,
        "text_color": text_color,
    }

    return render_template(f"spotify.{theme}.html.j2", **rendered_data)


@view.route("/spotify")
def render_img():
    def get_song_info(user_id_):
        access_token = get_access_token(user_id_)
        data = get_now_playing(access_token)

        if data is not None and data != {}:
            song = data["item"]

            if not data.get("currently_playing_type"):
                song["currently_playing_type"] = data["currently_playing_type"]

            is_now_playing_ = data["is_playing"]
        else:
            recent_plays = get_recently_played(access_token)
            size_recent_play = len(recent_plays["items"])
            idx = random.randint(0, size_recent_play - 1)

            song = recent_plays["items"][idx]["track"]
            song["currently_playing_type"] = "track"

            is_now_playing_ = False

        return song, is_now_playing_

    user_id = request.args.get("id")

    theme = request.args.get("theme", default="plain")

    needs_cover_image = True if request.args.get("image", default="true") == "true" else False
    bars_when_not_listening = True if request.args.get("bars_when_not_listening", default="true") == "true" else False
    hide_status = True if request.args.get("hide_status", default="false") == "true" else False

    title_color = str(escape(request.args.get("title_color", default="")))
    text_color = str(escape(request.args.get("text_color", default="")))
    bg_color = str(escape(request.args.get("bg_color", default="")))
    color_theme = request.args.get("color_theme", default="none")

    item, is_now_playing = get_song_info(user_id)

    info = {
        "theme": theme,
        "is_now_playing": is_now_playing,
        "needs_cover_image": needs_cover_image,
        "bars_when_not_listening": bars_when_not_listening,
        "hide_status": hide_status,
        "color_theme": color_theme,
        "title_color": title_color,
        "text_color": text_color,
        "bg_color": bg_color,
    }

    # Generate the SVG
    svg = make_svg(item, info)

    # Generate the response with the SVG
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
