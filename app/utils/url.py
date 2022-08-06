from __future__ import annotations

from typing import Any


def form_url(url: str, data: dict[str, Any]) -> str:
    url += "?" + "&".join(
        [f"{dict_key}={dict_value}" for dict_key, dict_value in data.items()]
    )

    return url


def generate_oauth_url(client_id: str, redirect_uri: str, scopes: list) -> str:
    return form_url(
        "https://accounts.spotify.com/authorize",
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": ",".join(scopes),
        },
    )
