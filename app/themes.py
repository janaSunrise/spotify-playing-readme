from typing import TypedDict


class ThemeColors(TypedDict):
    title_color: str
    text_color: str
    bg_color: str


THEMES: dict[str, ThemeColors] = {
    "none": {
        "title_color": "",
        "text_color": "",
        "bg_color": "",
    },
    "dark": {
        "title_color": "#fff",
        "text_color": "#9f9f9f",
        "bg_color": "#151515",
    },
    "radical": {
        "title_color": "#fe428e",
        "text_color": "#a9fef7",
        "bg_color": "#141321",
    },
    "tokyonight": {
        "title_color": "#70a5fd",
        "text_color": "#38bdae",
        "bg_color": "#1a1b27",
    },
    "onedark": {
        "title_color": "#e4bf7a",
        "text_color": "#df6d74",
        "bg_color": "#282c34",
    },
    "cobalt": {
        "title_color": "#e683d9",
        "text_color": "#75eeb2",
        "bg_color": "#193549",
    },
    "synthwave": {
        "title_color": "#e2e9ec",
        "text_color": "#e5289e",
        "bg_color": "#2b213a",
    },
    "algolia": {
        "title_color": "#00AEFF",
        "text_color": "#FFFFFF",
        "bg_color": "#050F2C",
    },
    "great_gatsby": {
        "title_color": "#ffa726",
        "text_color": "#ffd95b",
        "bg_color": "#000000",
    },
    "darcula": {
        "title_color": "#BA5F17",
        "text_color": "#BEBEBE",
        "bg_color": "#242424",
    },
    "outrun": {
        "title_color": "#ffcc00",
        "text_color": "#8080ff",
        "bg_color": "#141439",
    },
    "city_lights": {
        "title_color": "#5D8CB3",
        "text_color": "#718CA1",
        "bg_color": "#1D252C",
    },
}
