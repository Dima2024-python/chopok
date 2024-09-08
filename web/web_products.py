from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import dao
from utils.jwt_auth import get_user_web, set_cookies_web

templates = Jinja2Templates(directory="templates")

web_router_products = APIRouter(
    prefix="",
)


@web_router_products.get('/', include_in_schema=True)
@web_router_products.post('/', include_in_schema=True)
def index(request: Request, user=Depends(get_user_web)):
    context = {
        'request': request,
        'products': dao.get_all_products(),
        'title': 'Main page',
        'user': user
    }
    response = templates.TemplateResponse('index.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies
