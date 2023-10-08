# crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import Inventory, Sale
from db import schemas
from datetime import date, datetime


def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session, product_id: int):
    return db.query(Inventory).filter(Inventory.product_id == product_id).all()

def check_inventory_status(db: Session, product_id: int):
    current_stock = db.query(func.sum(Inventory.quantity)).filter(Inventory.product_id == product_id).scalar() or 0
    return {"product_id": product_id, "quantity": current_stock}


def update_stock_alert(db: Session, product_id: int, threshold: int):
    current_stock = db.query(func.sum(Inventory.quantity)).filter(Inventory.product_id == product_id).scalar() or 0
    if current_stock < threshold:
        # Trigger stock alert logic (e.g., send notification, log alert, etc.)
        pass
    return current_stock

def calculate_total_revenue(db: Session, start_date: date, end_date: date, category_id: int = None):
    # Use SQLAlchemy aggregation functions to calculate total revenue
    query = db.query(func.sum(Sale.quantity * Product.price)).join(Product)

    # Apply filters based on date and optionally category
    query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    return query.scalar() or 0