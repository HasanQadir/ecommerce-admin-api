from typing import Union

from pydantic import BaseModel
from datetime import date


class Product(BaseModel):
    product_id: int
    title: str
    name: str
    description: str
    price: float
    category_id: int

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
    start_date: date


class AnnualRevenue(Revenue):
    year: int


class MonthlyRevenue(AnnualRevenue):
    month: int