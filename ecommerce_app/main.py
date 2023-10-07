from fastapi import FastAPI
from db.db_config import engine, SessionLocal, Base
from api import sales, products

app = FastAPI()

# Include the routes from api/sales.py and api/products.py
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(products.router, prefix="/products", tags=["products"])

# Dependency to create tables on startup
def create_tables():
    Base.metadata.create_all(bind=engine)

# Event handler to create tables on startup
app.add_event_handler("startup", create_tables)
