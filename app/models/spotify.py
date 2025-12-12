from typing import Literal

from pydantic import BaseModel, Field

from app.models.spotify_api import SpotifyEpisode, SpotifyTrack


class SpotifyItem(BaseModel):
    name: str
    artist: str
    album: str

    is_explicit: bool = Field(default=False)

    currently_playing_type: Literal["track", "episode"] = "track"
    is_now_playing: bool = False

    image_url: str

    @classmethod
    def from_track(cls, track: SpotifyTrack, *, is_now_playing: bool = False) -> "SpotifyItem":
        images = track.album.images if track.album else track.images
        image_url = images[1].url if len(images) > 1 else images[0].url if images else ""

        artist_name = track.artists[0].name if track.artists else ""
        album_name = track.album.name if track.album else ""

        return cls(
            name=track.name,
            artist=artist_name,
            album=album_name,
            is_explicit=track.explicit,
            currently_playing_type="track",
            is_now_playing=is_now_playing,
            image_url=image_url,
        )

    @classmethod
    def from_episode(cls, episode: SpotifyEpisode, *, is_now_playing: bool = False) -> "SpotifyItem":
        images = episode.images
        image_url = images[1].url if len(images) > 1 else images[0].url if images else ""

        return cls(
            name=episode.name,
            artist=episode.show.publisher,
            album=episode.show.name,
            is_explicit=episode.explicit,
            currently_playing_type="episode",
            is_now_playing=is_now_playing,
            image_url=image_url,
        )
