import random
from textwrap import dedent

CARD_STYLES = {"default", "apple", "neon"}

COLOR_THEMES = {
    "light": {
        "bg": "#ffffff",
        "text": "#1e293b",
        "accent": "#3b82f6",
        "status": "#64748b",
    },
    "dark": {
        "bg": "#1c1c1e",
        "text": "#f5f5f7",
        "accent": "#0a84ff",
        "status": "#98989d",
    },
    "purple": {
        "bg": "#faf5ff",
        "text": "#4c1d95",
        "accent": "#a855f7",
        "status": "#7c3aed",
    },
    "blue": {
        "bg": "#eff6ff",
        "text": "#1e40af",
        "accent": "#3b82f6",
        "status": "#3b82f6",
    },
    "green": {
        "bg": "#f0fdf4",
        "text": "#166534",
        "accent": "#22c55e",
        "status": "#16a34a",
    },
    "orange": {
        "bg": "#fff7ed",
        "text": "#9a3412",
        "accent": "#f97316",
        "status": "#ea580c",
    },
    "tokyonight": {
        "bg": "#1a1b26",
        "text": "#c0caf5",
        "accent": "#7aa2f7",
        "status": "#9d7cd8",
    },
    "nord": {
        "bg": "#2e3440",
        "text": "#eceff4",
        "accent": "#88c0d0",
        "status": "#81a1c1",
    },
    "catppuccin": {
        "bg": "#1e1e2e",
        "text": "#cdd6f4",
        "accent": "#89b4fa",
        "status": "#cba6f7",
    },
}

WIDGET_WIDTH = 350
WIDGET_HEIGHT = 150
VISUALIZER_BAR_COUNT = 40
MAX_TEXT_LENGTH = 30
DARK_THEME_LUMINANCE_THRESHOLD = 0.5


def validate_card_style(style: str | None) -> str:
    if not style:
        return "default"
    normalized = style.lower().strip()
    return normalized if normalized in CARD_STYLES else "default"


def validate_color_theme(theme: str | None) -> str:
    if not theme:
        return "light"
    normalized = theme.lower().strip()
    return normalized if normalized in COLOR_THEMES else "light"


def get_colors(color_theme: str | None) -> dict[str, str]:
    validated = validate_color_theme(color_theme)
    return COLOR_THEMES[validated]


def generate_visualizer_css(bar_count: int = VISUALIZER_BAR_COUNT) -> str:
    css_bar = ""
    for i in range(1, bar_count + 1):
        anim = random.randint(400, 800)
        delay = random.randint(0, 400)
        css_bar += dedent(f"""
        .bar:nth-child({i}) {{
            animation-duration: {anim}ms;
            animation-delay: -{delay}ms;
        }}
        """)
    return css_bar


def is_dark_theme(color_theme: str | None) -> bool:
    validated = validate_color_theme(color_theme)
    bg_color = COLOR_THEMES[validated]["bg"]

    hex_color = bg_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    # Calculate relative luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Return True if dark (luminance < threshold)
    return luminance < DARK_THEME_LUMINANCE_THRESHOLD


def generate_visualizer_bars(bar_count: int = VISUALIZER_BAR_COUNT) -> str:
    return "".join(['<div class="bar"></div>' for _ in range(bar_count)])
