import config
from sqlalchemy import Column, DateTime, Float, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Products(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    product_name = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    product_class = Column(Text, nullable=False)
    start_product_expiration_date = Column(DateTime, nullable=False)
    end_product_expiration_date = Column(DateTime, nullable=False)

    def __str__(self):
        return (f'Product ==> name:{self.product_name}; price: {self.price};'
                f' product expiration date: {self.start_product_expiration_date} -> {self.end_product_expiration_date}')

    __repr__ = __str__


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()



def create_tables():
    Base.metadata.create_all(engine)
