from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    debug: bool = Field(default=True, alias="DEBUG")
    base_url: str = Field(..., alias="BASE_URL")
    session_secret_key: str = Field(..., alias="SESSION_SECRET_KEY")

    # Spotify
    spotify_client_id: str = Field(..., alias="SPOTIFY_CLIENT_ID")
    spotify_secret_id: str = Field(..., alias="SPOTIFY_SECRET_ID")
    spotify_scopes: list[str] = Field(
        default=["user-read-currently-playing", "user-read-recently-played"],
    )

    # Supabase
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_key: str = Field(..., alias="SUPABASE_KEY")

    @property
    def redirect_uri(self) -> str:
        return f"{self.base_url}/callback"

    @property
    def github_url(self) -> str:
        return "https://github.com/janaSunrise/spotify-playing-readme"


settings = Settings()  # pyright: ignore[reportCallIssue]
