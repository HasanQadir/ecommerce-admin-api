# app/api/sales.py

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from datetime import date
from db.models import Product, Sale, Category
from db import schemas
from sqlalchemy import func
from datetime import datetime, timedelta
from db import crud

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/compare-revenue-across-periods", response_model=list[schemas.PeriodRevenue])
def compare_revenue(start_date_1: date, end_date_1: date,
                    start_date_2: date, end_date_2: date,
                    category_id: int = None,
                    db: Session = Depends(get_db)):
    db = SessionLocal()

    # Calculate total revenue for the first period
    total_revenue_1 = crud.calculate_total_revenue(db, start_date_1, end_date_1, category_id)

    # Calculate total revenue for the second period
    total_revenue_2 = crud.calculate_total_revenue(db, start_date_2, end_date_2, category_id)

    db.close()

    return [schemas.PeriodRevenue(start_date=start_date_1, end_date=end_date_1, total_revenue=total_revenue_1),
            schemas.PeriodRevenue(start_date=start_date_2, end_date=end_date_2, total_revenue=total_revenue_2)]

@router.get("/sales-by-date-range", response_model=list[schemas.Sale])
def get_sales_data(start_date: date , end_date: date ,
                   product_id: int = None, category_id: int = None,
                   db: Session = Depends(get_db)):
    
    # Query sales data based on date range, category, and product
    query = db.query(Sale).join(Product)

    query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)

    sales_data = query.all()

    db.close()

    return sales_data

@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
    db.close()
    if sale:
        return sale
    else:
        raise HTTPException(status_code=404, detail="Sale not found")

@router.get("/revenue/daily", response_model=schemas.DailyRevenue)
def get_daily_revenue(date: date, db: Session = Depends(get_db)):
    total_revenue = db.query(Sale.quantity * Product.price).\
        join(Product).filter(Sale.sale_date == date).scalar()
    db.close()
    return schemas.DailyRevenue(date=date, total_revenue=total_revenue)

@router.get("/revenue/weekly", response_model=schemas.WeeklyRevenue)
def get_weekly_revenue(start_date: date , end_date: date, db: Session = Depends(get_db)):
    # Use func.sum to aggregate the total revenue for the specified week
    total_revenue = db.query(func.sum(Sale.quantity * Product.price)).\
        join(Product).\
        filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()
    db.close()
    return schemas.WeeklyRevenue(start_date=start_date, end_date=end_date, total_revenue=total_revenue)

@router.get("/revenue/monthly", response_model=schemas.MonthlyRevenue)
def get_monthly_revenue(year: int , month: int, db: Session = Depends(get_db)):
    start_date = date(year, month, 1)
    end_date = date(year, month + 1, 1) - timedelta(days=1)
    # Use func.sum to aggregate the total revenue for the specified month
    total_revenue = db.query(func.sum(Sale.quantity * Product.price)).\
        join(Product).\
        filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()

    db.close()
    return schemas.MonthlyRevenue(year=year, month=month, total_revenue=total_revenue)

@router.get("/revenue/annual", response_model=schemas.AnnualRevenue)
def get_annual_revenue(year: int, db: Session = Depends(get_db)):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    # Use func.sum to aggregate the total revenue for the specified year
    total_revenue = db.query(func.sum(Sale.quantity * Product.price)).\
        join(Product).filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).scalar()
    db.close()
    return schemas.AnnualRevenue(year=year, total_revenue=total_revenue)
