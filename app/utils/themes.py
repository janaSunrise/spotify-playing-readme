from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    title_color: str
    text_color: str
    background_color: str


THEMES: dict[str, Theme] = {
    "none": Theme("", "", ""),
    "dark": Theme("#ffffff", "#9f9f9f", "#151515"),
    "radical": Theme("#fe428e", "#a9fef7", "#141321"),
    "tokyo-night": Theme("#70a5fd", "#38bdae", "#1a1b27"),
    "one-dark": Theme("#e4bf7a", "#df6d74", "#282c34"),
    "cobalt": Theme("#e683d9", "#75eeb2", "#193549"),
    "synthwave": Theme("#e2e9ec", "#e5289e", "#2b213a"),
    "algolia": Theme("#00AEFF", "#FFFFFF", "#050F2C"),
    "great-gatsby": Theme("#ffa726", "#ffd95b", "#000000"),
    "darcula": Theme("#BA5F17", "#BEBEBE", "#242424"),
    "outrun": Theme("#ffcc00", "#8080ff", "#141439"),
    "city-lights": Theme("#5D8CB3", "#718CA1", "#1D252C"),
}
