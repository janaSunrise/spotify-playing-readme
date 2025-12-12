from typing import Literal

from pydantic import BaseModel, Field


class SpotifyImage(BaseModel):
    url: str

    model_config = {"extra": "ignore"}


class SpotifyArtist(BaseModel):
    name: str

    model_config = {"extra": "ignore"}


class SpotifyAlbum(BaseModel):
    name: str
    images: list[SpotifyImage] = Field(default_factory=list)

    model_config = {"extra": "ignore"}


class SpotifyShow(BaseModel):
    name: str
    publisher: str

    model_config = {"extra": "ignore"}


class SpotifyTrack(BaseModel):
    name: str
    artists: list[SpotifyArtist] = Field(default_factory=list)
    album: SpotifyAlbum | None = None
    explicit: bool = False
    images: list[SpotifyImage] = Field(default_factory=list)

    model_config = {"extra": "ignore"}


class SpotifyEpisode(BaseModel):
    name: str
    show: SpotifyShow
    explicit: bool = False
    images: list[SpotifyImage] = Field(default_factory=list)

    model_config = {"extra": "ignore"}


class SpotifyTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_in: int
    token_type: str = "Bearer"
    scope: str | None = None

    model_config = {"extra": "ignore"}


class SpotifyCurrentlyPlayingResponse(BaseModel):
    item: SpotifyTrack | SpotifyEpisode | None = None
    is_playing: bool = False
    currently_playing_type: Literal["track", "episode"] = "track"

    model_config = {"extra": "ignore"}


class SpotifyRecentlyPlayedItem(BaseModel):
    track: SpotifyTrack

    model_config = {"extra": "ignore"}


class SpotifyRecentlyPlayedResponse(BaseModel):
    items: list[SpotifyRecentlyPlayedItem] = Field(default_factory=list)

    model_config = {"extra": "ignore"}


class SpotifyUserInfoResponse(BaseModel):
    id: str

    model_config = {"extra": "ignore"}
