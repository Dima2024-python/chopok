from fastapi import FastAPI

from api.api_products import api_products_router
from database import create_tables


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_products_router)
