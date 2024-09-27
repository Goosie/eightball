from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

eightball_ext_generic = APIRouter(tags=["eightball"])


@eightball_ext_generic.get(
    "/", description="Example generic endpoint", response_class=HTMLResponse
)
async def index(
    request: Request,
    user: User = Depends(check_user_exists),
):
    return template_renderer(["eightball/templates"]).TemplateResponse(
        request, "eightball/index.html", {"user": user.dict()}
    )
