import uuid
from datetime import datetime

import config
from sqlalchemy import Column, DateTime, Float, Integer, Text, create_engine, String, Sequence, UUID, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Products(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    product_name = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    product_class = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    start_product_expiration_date = Column(DateTime, default=datetime.now)
    end_product_expiration_date = Column(DateTime, )
    image = Column(String, nullable=False)

    def __str__(self):
        return (f'Product ==> name:{self.product_name}; price: {self.price};'
                f' product expiration date: {self.start_product_expiration_date} -> {self.end_product_expiration_date}')

    __repr__ = __str__


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    user_uuid = Column(UUID, default=uuid.uuid4)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
