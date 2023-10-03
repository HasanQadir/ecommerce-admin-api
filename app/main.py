
from fastapi import FastAPI

app = FastAPI()

# Include the routes from api/sales.py and api/products.py
from app.api import sales, products

app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(products.router, prefix="/products", tags=["products"])
