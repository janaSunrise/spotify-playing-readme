from __future__ import annotations

from typing import Any


def form_url(url: str, data: dict[str, Any]) -> str:
    url += "?" + "&".join(
        [f"{dict_key}={dict_value}" for dict_key, dict_value in data.items()]
    )

    return url
