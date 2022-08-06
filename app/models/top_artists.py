from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class TopArtist:
    artist: str

    image_url: str
    image: str = field(init=False, repr=False)

    def __post_init__(self):
        self.image = base64.b64encode(requests.get(self.image_url).content).decode(
            "ascii"
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> list[TopArtist]:
        top_artists = []

        for track in data["items"]:
            top_artists.append(
                cls(
                    track["name"].replace("&", "&amp;"),
                    track["images"][1]["url"],
                )
            )

        return top_artists
