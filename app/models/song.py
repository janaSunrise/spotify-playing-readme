from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Literal

import requests


@dataclass
class Song:
    name: str
    artist: str
    album: str

    is_explicit: bool

    currently_playing_type: Literal["track", "episode"]
    is_now_playing: bool

    image_url: str
    image: str = field(init=False, repr=False)

    def __post_init__(self):
        self.image = base64.b64encode(requests.get(self.image_url).content).decode(
            "ascii"
        )

    @classmethod
    def from_json(cls, song: dict[str, Any]) -> "Song":
        is_now_playing = song["is_now_playing"]
        currently_playing_type = song["currently_playing_type"]

        if currently_playing_type == "track":
            artist_name = song["artists"][0]["name"].replace("&", "&amp;")
            song_name = song["name"].replace("&", "&amp;")
            album_name = song["album"]["name"].replace("&", "&amp;")

            img_url = song["album"]["images"][1]["url"]
        else:
            artist_name = song["show"]["publisher"].replace("&", "&amp;")
            song_name = song["name"].replace("&", "&amp;")
            album_name = song["show"]["name"].replace("&", "&amp;")

            img_url = song["images"][1]["url"]

        return cls(
            song_name,
            f"By {artist_name}",
            f"On {album_name}",
            song["explicit"],
            currently_playing_type,
            is_now_playing,
            img_url,
        )
