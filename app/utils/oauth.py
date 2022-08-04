from .url import form_url


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
