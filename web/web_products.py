from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import dao

templates = Jinja2Templates(directory="templates")

web_router = APIRouter(
    prefix="",
)


@web_router.get('/')
def index(request: Request):
    context = {
        'request': request,
        'products': dao.get_all_products(),
        "title": "Main page"}
    return templates.TemplateResponse("index.html", context=context)
