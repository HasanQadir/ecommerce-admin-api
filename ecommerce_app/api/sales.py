# app/api/sales.py

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from datetime import date
from db import schemas

router = APIRouter()

@router.get("/{sale_id}")
def read_sale(sale_id: int, response_model=schemas.Sale):
    db = SessionLocal()
    sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
    db.close()
    if sale:
        return sale
    else:
        raise HTTPException(status_code=404, detail="Sale not found")

@router.get("/revenue/daily")
def get_daily_revenue(date: date, response_model=schemas.DailyRevenue):
    db = SessionLocal()
    total_revenue = db.query(Sale.quantity * Product.price).\
        join(Product).filter(Sale.sale_date == date).scalar()
    db.close()
    return {"date": date, "total_revenue": total_revenue}

@router.get("/revenue/weekly")
def get_weekly_revenue(start_date: date , end_date: date, response_model=schemas.WeeklyRevenue ):
    db = SessionLocal()
    total_revenue = db.query(Sale.quantity * Product.price).\
        join(Product).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()
    db.close()
    return {"start_date": start_date, "end_date": end_date, "total_revenue": total_revenue}

@router.get("/revenue/monthly")
def get_monthly_revenue(year: int , month: int, response_model=schemas.MonthlyRevenue):
    db = SessionLocal()
    start_date = date(year, month, 1)
    end_date = date(year, month + 1, 1) - timedelta(days=1)
    total_revenue = db.query(Sale.quantity * Product.price).\
        join(Product).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()
    db.close()
    return {"year": year, "month": month, "total_revenue": total_revenue}

@router.get("/revenue/annual")
def get_annual_revenue(year: int, response_model=schemas.AnnualRevenue):
    db = SessionLocal()
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    total_revenue = db.query(Sale.quantity * Product.price).\
        join(Product).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()
    db.close()
    return {"year": year, "total_revenue": total_revenue}

@router.get("/compare-revenue-across-periods")
def compare_revenue(start_date_1: date, end_date_1: date,
                    start_date_2: date, end_date_2: date,
                    category_id: int = None):
    db = SessionLocal()

    # Calculate total revenue for the first period
    total_revenue_1 = calculate_total_revenue(db, start_date_1, end_date_1, category_id)

    # Calculate total revenue for the second period
    total_revenue_2 = calculate_total_revenue(db, start_date_2, end_date_2, category_id)

    db.close()

    return {
        "period_1": {"start_date": start_date_1, "end_date": end_date_1, "total_revenue": total_revenue_1},
        "period_2": {"start_date": start_date_2, "end_date": end_date_2, "total_revenue": total_revenue_2},
    }

def calculate_total_revenue(db: Session, start_date: date, end_date: date, category_id: int = None):
    # Use SQLAlchemy aggregation functions to calculate total revenue
    query = db.query(func.sum(Sale.quantity * Product.price)).join(Product)

    # Apply filters based on date and optionally category
    query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    return query.scalar() or 0

@router.get("/sales-by-date-range")
def get_sales_data(start_date: date , end_date: date ,
                   product_id: int = None, category_id: int = None):
    db = SessionLocal()
    
    # Query sales data based on date range, category, and product
    query = db.query(Sale).join(Product)

    query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    sales_data = query.all()

    db.close()

    return {"sales_data": sales_data}