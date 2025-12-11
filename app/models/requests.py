from pydantic import BaseModel, Field


class SpotifyWidgetParams(BaseModel):
    id: str = Field(...)
    theme: str = Field(default="plain")
    image: str = Field(default="true")
    bars_when_not_listening: str = Field(default="true")
    hide_status: str = Field(default="false")
    title_color: str = Field(default="")
    text_color: str = Field(default="")
    bg_color: str = Field(default="")
    color_theme: str = Field(default="none")

    @property
    def needs_cover_image(self) -> bool:
        return self.image.lower() == "true"

    @property
    def bars_when_not_listening_flag(self) -> bool:
        return self.bars_when_not_listening.lower() == "true"

    @property
    def hide_status_flag(self) -> bool:
        return self.hide_status.lower() == "true"
