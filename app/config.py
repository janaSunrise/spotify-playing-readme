from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    debug: bool = Field(default=True, alias="DEBUG")
    base_url: str = Field(..., alias="BASE_URL")

    # Spotify credentials
    spotify_client_id: str = Field(..., alias="SPOTIFY_CLIENT_ID")
    spotify_secret_id: str = Field(..., alias="SPOTIFY_SECRET_ID")

    # Supabase credentials
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_key: str = Field(..., alias="SUPABASE_KEY")

    # Spotify scopes
    spotify_scopes: list[str] = Field(
        default=["user-read-currently-playing", "user-read-recently-played"],
    )

    @property
    def redirect_uri(self) -> str:
        """Get redirect URI for OAuth."""
        return f"{self.base_url}/callback"

    @property
    def github_url(self) -> str:
        """GitHub repository URL."""
        return "https://github.com/janaSunrise/spotify-playing-readme"


settings = Settings()
