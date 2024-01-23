from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session 
from datetime import timedelta, datetime, timezone, date
from .. import oauth2
from typing import List



router = APIRouter(
    tags=['subscription']
)

def subscription_price(duration, db):
    query = db.query(models.SubPrice).filter(models.SubPrice.duration == duration).first()
    return query.price


# ***************RENEW SUBSCRIPTION BEFORE EXPIRY******************
def renew_monthly_sub(business_id,  db, price):

    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)
  
    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=30)
    else:
        new_enddate = startdate + timedelta(days=30)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscription that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().end_date = new_enddate
    query.first().price = price
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert
    

def renew_six_month_sub(business_id,  db, price):
    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)
    
    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=182)
    else:
        new_enddate = startdate + timedelta(days=182)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscription that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().price = price
    query.first().end_date = new_enddate
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


def renew_yearly_sub(business_id,  db, price):
    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)

    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=365)
    else:
        new_enddate = startdate + timedelta(days=365)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscription that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().price = price
    query.first().end_date = new_enddate
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert



# ***************ADD SUBSCRIPTION******************
@router.post("/monthly_sub/", status_code=status.HTTP_200_OK)
def monthly_sub( db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    getbizid = db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    business_id = getbizid.id

    price = subscription_price("monthly", db)

    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false' )

    
    # check if there's a running subscription
    running = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )

    if expire.first():
        renew_monthly_sub(business_id, db, price)
        return {"renewal": "success"}

    elif running.first():
        renew_monthly_sub(business_id, db, price)
        return {"renewal": "success"}
    
    else:

        startdate = datetime.now()
        enddate = startdate + timedelta(days=30)

        hist = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(hist)
        db.commit()
        db.refresh(hist)

        insert = models.Subscription(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert


@router.post("/six_month_sub/", status_code=status.HTTP_200_OK)
def six_month_sub(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    getbizid = db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    business_id = getbizid.id

    price = subscription_price("six_month", db)

    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false' )

    # check if there's a running subscription
    running = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )
    
    if expire.first():
        renew_six_month_sub(business_id,  db, price)
        return {"renewal": "success"}
    
    elif running.first():
        renew_six_month_sub(business_id,  db, price)
        return {"renewal": "success"}
    
    else:
        startdate = datetime.now()
        enddate = startdate + timedelta(days=182)

        hist = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(hist)
        db.commit()
        db.refresh(hist)

        insert = models.Subscription(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert


@router.post("/yearly_sub/", status_code=status.HTTP_200_OK)
def yearly_sub(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    getbizid = db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    business_id = getbizid.id

    price = subscription_price("yearly", db)

    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false')

    # check if there's a running subscription
    running = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )

    if expire.first():
        renew_yearly_sub(business_id,  db, price)
        return {"renewal": "success"}
    

    elif running.first():
        renew_yearly_sub(business_id,  db, price)
        return {"renewal": "success"}
    
    else:
        startdate = datetime.now()
        enddate = startdate + timedelta(days=365)

        hist = models.SubHistory(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(hist)
        db.commit()
        db.refresh(hist)

        insert = models.Subscription(business_id = business_id, price = price, start_date = startdate, end_date = enddate)
        db.add(insert)
        db.commit()
        db.refresh(insert)
        return insert



# ***************GET SUBSCRIPTION PRICE*******************
@router.get("/get_subprices/", status_code=status.HTTP_200_OK, response_model=List[schemas.SubPrice])
def get_subprices( db: Session = Depends(get_db) ):

    query =  db.query(models.SubPrice).all()
    
    return query