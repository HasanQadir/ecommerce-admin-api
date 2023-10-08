from typing import Union

from pydantic import BaseModel
from datetime import date, datetime


class Product(BaseModel):
    name: str
    price: float
    category_id: int


class ProductCreate(Product):
    product_id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class Sale(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    sale_date: date

    class Config:
        from_attributes = True


class Revenue(BaseModel):
    total_revenue: float


class DailyRevenue(Revenue):
    date: date


class WeeklyRevenue(Revenue):
    start_date: date
    end_date: date


class MonthlyRevenue(Revenue):
    year: int
    month: int


class AnnualRevenue(Revenue):
    year: int


class PeriodRevenue(Revenue):
    start_date: date
    end_date: date


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int


class InventoryStatus(BaseModel):
    product_id: int
    quantity: int


class InventoryUpdate(InventoryCreate):
    pass


class Inventory(BaseModel):
    inventory_id: int
    product_id: int
    quantity: int
    timestamp: datetime

    class Config:
        from_attributes = True
