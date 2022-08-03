def generate_oauth_url(client_id: str, redirect_uri: str, scopes: list) -> str:
    return (
        "https://accounts.spotify.com/authorize"
        f"?client_id={client_id}"
        "&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={','.join(scopes)}"
    )
