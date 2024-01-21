from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas_admin, oauth2_admin
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import timedelta, datetime, timezone, date

router = APIRouter(
    tags=['Admin Subscription']
)


# ***************GET SUBSCRIPTION HISTORY*******************
@router.get("/admin/subhistory/{id}", status_code=status.HTTP_200_OK, response_model=List[schemas_admin.SubHistory])
def get_sub_history( id: int, db: Session = Depends(get_db)):
    results =  db.query(models.SubHistory).filter(models.SubHistory.business_id == id).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business no found.")
    
    return results



# let frontend call the endpoint to run daily at 00:00
@router.post("/admin/deactivate_sub/}", status_code=status.HTTP_200_OK)
def deactivate_expired_subsription(db:Session = Depends(get_db)):
    currentday: datetime = datetime.now(timezone.utc)
    query = db.query(models.Subscription).filter(models.Subscription.is_active == 'true')

    for i in query:
        if (i.end_date - currentday ).days < 1:
            i.is_active = False
            db.commit() 
            return {"message":"Subscriptions deactivated"}
        


# ***************SUBSCRIPTION DURATION*******************
@router.get("/admin/subduration/", status_code=status.HTTP_200_OK)
def get_sub_duration():
    return {"monthly", "quaterly", "six_month", "yearly"}



# ***************UPDATE SUBSCRIPTION PRICE*******************
@router.post("/admin/add_subprices/", status_code=status.HTTP_200_OK)
def add_subprices( data: schemas_admin.SubPrice, db: Session = Depends(get_db) ):

    query =  db.query(models.SubPrice).filter(models.SubPrice.duration == data.duration)
    
    if not query.first():
        insert = models.SubPrice(**data.model_dump())
        db.add(insert)
        db.commit()
        return {"data": "success"}
    
    else:
        query.first().price = data.price
        db.commit()
        return {"data": "success"}


# ***************GET REPORT*******************
@router.post("/admin/report/", status_code=status.HTTP_200_OK)
def sub_report(startdate: date, enddate: date, db: Session = Depends(get_db)):
    
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    return query

@router.post("/admin/reportamt/", status_code=status.HTTP_200_OK)
def sub_amt_report(startdate: date, enddate: date, db: Session = Depends(get_db)):
    
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    sum = 0
    for biz in query:
        sum = sum + biz.price

    return sum



# ***************LAST DAY REPORT*******************
@router.post("/admin/reportlastday/", status_code=status.HTTP_200_OK)
def day_amt_report(db: Session = Depends(get_db)):
    enddate = date.today() 
    startdate = enddate - timedelta(days=1)
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    sum = 0
    for biz in query:
        sum = sum + biz.price

    return sum


# ***************LAST WEEK REPORT*******************
@router.post("/admin/reportlastweek/", status_code=status.HTTP_200_OK)
def week_amt_report(db: Session = Depends(get_db)):
    enddate = date.today() 
    startdate = enddate - timedelta(days=7)
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    sum = 0
    for biz in query:
        sum = sum + biz.price

    return sum


# ***************LAST MONTH REPORT*******************
@router.post("/admin/reportlastmonth/", status_code=status.HTTP_200_OK)
def month_amt_report(db: Session = Depends(get_db)):
    enddate = date.today() 
    startdate = enddate - timedelta(days=30)
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    sum = 0
    for biz in query:
        sum = sum + biz.price

    return sum


# ***************LAST YEAR REPORT*******************
@router.post("/admin/reportlastyear/", status_code=status.HTTP_200_OK)
def year_amt_report(db: Session = Depends(get_db)):
    enddate = date.today() 
    startdate = enddate - timedelta(days=365)
    #date format - YYYY-MM-DD
    query = db.query(models.SubHistory).filter(models.SubHistory.date_created.between(startdate, enddate)).all()

    sum = 0
    for biz in query:
        sum = sum + biz.price

    return sum