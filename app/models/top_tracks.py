from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class TopTrack:
    name: str
    artist: str

    is_explicit: bool

    image_url: str
    image: str = field(init=False, repr=False)

    def __post_init__(self):
        self.image = base64.b64encode(requests.get(self.image_url).content).decode(
            "ascii"
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> list[TopTrack]:
        top_tracks = []

        for track in data["items"]:
            top_tracks.append(
                cls(
                    track["name"].replace("&", "&amp;"),
                    track["artists"][0]["name"].replace("&", "&amp;"),
                    track["explicit"],
                    track["album"]["images"][1]["url"],
                )
            )

        return top_tracks
