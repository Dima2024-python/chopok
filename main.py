from fastapi import FastAPI

from api.api_products import api_products_router
from api.api_users import api_router_user
from database import create_tables
from web.web_products import web_router_products
from web.web_users import web_router_user


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_products_router)
app.include_router(api_router_user)
app.include_router(web_router_products)
app.include_router(web_router_user)
