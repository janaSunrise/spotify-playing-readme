from typing import TypedDict

from markupsafe import escape


class ThemeColors(TypedDict):
    title_color: str
    text_color: str
    bg_color: str


class ThemeDimensions(TypedDict):
    width: int
    height: int
    num_bar: int


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

THEME_DIMENSIONS: dict[str | None, ThemeDimensions] = {
    "plain": {
        "width": 350,
        "height": 140,
        "num_bar": 40,
    },
    "wavy": {
        "width": 480,
        "height": 175,
        "num_bar": 90,
    },
    None: {
        "width": 150,
        "height": 75,
        "num_bar": 15,
    },
}

DEFAULT_COLORS: ThemeColors = {
    "bg_color": "white",
    "title_color": "#212122",
    "text_color": "#212122",
}


def get_theme_colors(
    color_theme: str,
    title_color: str = "",
    text_color: str = "",
    bg_color: str = "",
) -> ThemeColors:
    if color_theme not in THEMES:
        color_theme = "none"

    theme_colors = THEMES[color_theme]
    bg_color_final = theme_colors["bg_color"]
    title_color_final = theme_colors["title_color"]
    text_color_final = theme_colors["text_color"]

    # Override with custom colors if provided
    if title_color:
        title_color_final = str(escape(title_color))
    if text_color:
        text_color_final = str(escape(text_color))
    if bg_color:
        bg_color_final = str(escape(bg_color))

    # Apply defaults
    if not bg_color_final:
        bg_color_final = DEFAULT_COLORS["bg_color"]

    # Default color matching
    if not title_color_final and not text_color_final:
        text_color_final = title_color_final = DEFAULT_COLORS["title_color"]
    elif not title_color_final and text_color_final:
        title_color_final = text_color_final
    elif title_color_final and not text_color_final:
        text_color_final = title_color_final

    return {
        "bg_color": bg_color_final,
        "title_color": title_color_final,
        "text_color": text_color_final,
    }


def get_theme_dimensions(theme: str | None) -> ThemeDimensions:
    return THEME_DIMENSIONS.get(theme, THEME_DIMENSIONS[None])
