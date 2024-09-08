from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, Form
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

import dao
from background_tasks_chopok.confirm_registration import confirm_registration
from utils.jwt_auth import get_user_web, set_cookies_web

templates = Jinja2Templates(directory="templates")

web_router_user = APIRouter(
    prefix="",
)


@web_router_user.get('/register/', include_in_schema=True)
@web_router_user.post('/register/', include_in_schema=True)
def web_register(
        request: Request,
        background_tasks: BackgroundTasks,
        name: str = Form(None),
        email: str = Form(None),
        password: str = Form(None),
        user=Depends(get_user_web)
):
    if user:
        redirect_url = request.url_for('index')
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies

    if request.method == 'GET':
        context = {
            'request': request,
            'navbar': 'None',
            'title': 'Register'
        }
        return templates.TemplateResponse('registration.html', context=context)

    maybe_user = dao.get_user_by_email(email)
    context = {
        'request': request,
        'title': 'Register',
        'navbar': 'None',
        'travels': dao.get_all_products(),
        'user': maybe_user
    }
    if not maybe_user:
        created_user = dao.create_user(name, email, password)
        background_tasks.add_task(confirm_registration, created_user, request.base_url)
        context['user'] = created_user

    # response = templates.TemplateResponse('index.html', context=context)
    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response_with_cookies = set_cookies_web(context['user'], response)
    return response_with_cookies
