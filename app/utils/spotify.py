import random
from typing import cast

from ..app import spotify
from ..lib.supabase import get_access_token
from ..models.song import Song


def get_song_info(user_id: str) -> Song:
    access_token = cast(str, get_access_token(user_id))
    now_playing = spotify.currently_playing(access_token)

    # Check if song is playing.
    if now_playing and now_playing["currently_playing_type"] != "ad":
        song = now_playing["item"]

        # Ensure that there is a currently playing type
        song["currently_playing_type"] = now_playing["currently_playing_type"]

        # Ensure now playing exists
        song["is_now_playing"] = now_playing["is_playing"]
    else:
        # Get recently played songs.
        recently_played = spotify.recently_played(access_token)

        size_recently_played = len(recently_played["items"])
        idx = random.randint(0, size_recently_played - 1)

        song = recently_played["items"][idx]["track"]

        # Add track type, if not actively playing.
        song["currently_playing_type"] = "track"
        song["is_now_playing"] = False

    return Song.from_json(song)
