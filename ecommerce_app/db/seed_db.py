from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = "postgresql://ecommerce:Ap1%40Ec0mmerce@localhost/ecommerce-app"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float(precision=2), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)


fake = Faker()

# Create categories
categories = ["Electronics", "Clothing", "Books"]
for category_name in categories:
    category = Category(name=category_name)
    db.add(category)

db.commit()

# Create products
for _ in range(10):
    product = Product(
        name=fake.word(),
        description=fake.text(),
        price=fake.random_int(min=10, max=100, step=1),
        category_id=fake.random_element(elements=[1, 2, 3])
    )
    db.add(product)

db.commit()

# Create sales
for _ in range(50):
    sale = Sale(
        product_id=fake.random_element(elements=range(1, 11)),
        quantity=fake.random_int(min=1, max=10, step=1),
        sale_date=fake.date_between(start_date='-30d', end_date='today')
    )
    db.add(sale)

db.commit()

db.close()
