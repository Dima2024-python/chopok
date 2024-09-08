from datetime import datetime

from fastapi import Path, HTTPException, APIRouter
from pydantic import BaseModel, Field, HttpUrl
from starlette import status

import dao
from database import Products

api_products_router = APIRouter(tags=['Products'])


class NewProduct(BaseModel):
    product_name: str = Field(max_length=100, min_length=2, examples=[''])
    product_class: str = Field(min_length=2, examples=['Є такі класи: Солодке, Випічка, Молочне, Напої'])
    price: float = Field(ge=0.01)
    quantity: int = Field(ge=1, examples=[''])
    start_product_expiration_date: datetime
    end_product_expiration_date: datetime
    image: HttpUrl


class ProductData(NewProduct):
    id: int


@api_products_router.post('/create_product')
def create_product(new_product: NewProduct) -> ProductData:
    product = dao.create_product(**new_product.dict())
    return product


@api_products_router.get('/get_all_products')
def get_all_products() -> list[ProductData]:
    products = dao.get_all_products()
    return products


@api_products_router.get('/get_product_by_id')
def get_product_by_id(product_id: int) -> ProductData:
    product = dao.get_product_by_id(product_id)
    return product


@api_products_router.get('/get_product_by_class')
def get_product_by_class(product_class: str) -> list[ProductData]:
    products = dao.get_products_by_class(product_class)
    return products


@api_products_router.get('/get_products_by_price')
def get_products_by_price(price: float) -> list[ProductData]:
    products = dao.get_products_by_price(price)
    return products


@api_products_router.get('/get_products_by_name')
def get_products_by_name(name: str) -> list[ProductData]:
    products = dao.get_products_by_name(name)
    return products


@api_products_router.delete('/delete_product_by_id')
def delete_product_by_id(product_id: int):
    dao.delete_product(product_id)
    return None
