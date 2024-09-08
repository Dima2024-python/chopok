import uuid

from database import Products, session, User
from utils.utils_hashlib import get_password_hash


def create_product(
        product_name: str,
        product_class: str,
        price: float,
        quantity: int,
        start_product_expiration_date,
        end_product_expiration_date,
        image
        ) -> Products:
    product = Products(
        product_name=product_name,
        product_class=product_class,
        price=price,
        quantity=quantity,
        start_product_expiration_date=start_product_expiration_date,
        end_product_expiration_date=end_product_expiration_date,
        image=str(image)
    )
    session.add(product)
    session.commit()
    return product


def get_all_products() -> list[Products]:
    products = session.query(Products).all()
    return products


def get_product_by_id(product_id: int) -> Products | None:
    product = session.query(Products).filter(Products.id == product_id).first()
    return product


def get_products_by_class(product_class: str) -> list[Products]:
    products = session.query(Products).filter(Products.product_class == product_class).all()
    return products


def get_products_by_price(price: float) -> list[Products]:
    products = session.query(Products).filter(Products.price == price).all()
    return products


def get_products_by_name(name: str) -> list[Products]:
    products = session.query(Products).filter(Products.product_name.icontains(name)).all()
    return products


def delete_product(product_id) -> None:
    session.query(Products).filter(Products.id == product_id).delete()
    session.commit()


def create_user(name: str, email: str, password: str) -> User:
    user = User(
        name=name,
        email=email,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    return user


def get_user_by_email(email: str) -> User | None:
    query = session.query(User).filter(User.email == email).first()
    return query


def get_user_by_uuid(user_uuid: uuid.UUID) -> User | None:
    query = session.query(User).filter(User.user_uuid == user_uuid).first()
    return query


def activate_account(user: User) -> User:
    if user.is_verified:
        return user

    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
