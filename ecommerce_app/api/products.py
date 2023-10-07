# app/api/products.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import Product
from db.db_config import SessionLocal
from db import schemas

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-product/")
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
