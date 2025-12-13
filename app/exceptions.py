class SpotifyAPIError(Exception):
    """Base exception for Spotify API errors."""


class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""


class TokenRefreshError(Exception):
    """Raised when token refresh fails."""
