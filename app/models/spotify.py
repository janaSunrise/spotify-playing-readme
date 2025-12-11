import base64
from typing import Literal

import httpx
from pydantic import BaseModel, Field


class SpotifyItem(BaseModel):
    name: str
    artist: str
    album: str

    is_explicit: bool = Field(default=False)

    currently_playing_type: Literal["track", "episode"] = "track"
    is_now_playing: bool = False

    image_url: str

    @staticmethod
    async def fetch_image(image_url: str) -> str:
        """Fetch and encode image as base64 string."""
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()
        return base64.b64encode(response.content).decode("ascii")

    @classmethod
    def from_track(cls, track_data: dict, *, is_now_playing: bool = False) -> "SpotifyItem":
        images = track_data.get("album", {}).get("images", [])
        image_url = images[1]["url"] if len(images) > 1 else images[0]["url"] if images else ""

        return cls(
            name=track_data["name"],
            artist=track_data["artists"][0]["name"],
            album=track_data["album"]["name"],
            is_explicit=track_data.get("explicit", False),
            currently_playing_type="track",
            is_now_playing=is_now_playing,
            image_url=image_url,
        )

    @classmethod
    def from_episode(cls, episode_data: dict, *, is_now_playing: bool = False) -> "SpotifyItem":
        images = episode_data.get("images", [])
        image_url = images[1]["url"] if len(images) > 1 else images[0]["url"] if images else ""

        return cls(
            name=episode_data["name"],
            artist=episode_data["show"]["publisher"],
            album=episode_data["show"]["name"],
            is_explicit=episode_data.get("explicit", False),
            currently_playing_type="episode",
            is_now_playing=is_now_playing,
            image_url=image_url,
        )
