from fastapi import APIRouter, Request

from app.config import settings
from app.templates import templates

index_router = APIRouter(tags=["home"])


@index_router.get("/")
async def index(request: Request):
    """Homepage route."""
    return templates.TemplateResponse(request, "index.html", {"github_url": settings.github_url})
