# api/sales.py or api/inventory.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import schemas, crud
from db.db_config import SessionLocal
from db import crud

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/create-inventory", response_model=schemas.Inventory)
def create_inventory(inventory_data: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_inventory(db, inventory_data)

@router.post("/update-inventory", response_model=schemas.Inventory)
def update_inventory(inventory: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    # Update inventory
    db_inventory = crud.create_inventory(db, inventory)

    # Update stock alert based on product_id and a predefined threshold
    threshold = 10  # Set your desired threshold here
    crud.update_stock_alert(db, inventory.product_id, threshold)

    return db_inventory

@router.get("/inventory/track-changes/{product_id}", response_model=list[schemas.Inventory])
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    # Implement a function in crud.py to get inventory for a product
    return crud.get_inventory(db, product_id)

@router.get("/inventory/check-status/{product_id}", response_model=schemas.InventoryStatus)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    # Implement a function in crud.py to get inventory for a product
    return crud.check_inventory_status(db, product_id)