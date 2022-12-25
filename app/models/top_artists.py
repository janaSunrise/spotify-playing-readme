from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class TopArtists:
    artist: str

    image_url: str
    image: str = field(init=False, repr=False)

    def __post_init__(self):
        self.image = base64.b64encode(requests.get(self.image_url).content).decode(
            "ascii"
        )

    @classmethod
    def from_json(cls, data: dict[str, Any], count: int = 5) -> list[TopArtists]:
        top_artists = []
        artists = data["items"][:count]

        for artist in artists:
            top_artists.append(
                cls(
                    artist["name"].replace("&", "&amp;"),
                    artist["images"][1]["url"],
                )
            )

        return top_artists
