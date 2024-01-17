from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session 
from datetime import timedelta, datetime, timezone



router = APIRouter(
    tags=['subscription']
)

# def auto_deact(db:Session):
#     currentday: datetime = datetime.now(timezone.utc)
#     query = db.query(models.Subscription).filter(models.Subscription.is_active == 'true')

#     for i in query:
#         if (i.end_date - currentday ).days < 1:
#             i.is_active = False
#             db.commit()            



# ***************ADD SUBSCRIPTION******************
@router.post("/monthly_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def monthly_sub(business_id: int, db: Session = Depends(get_db)):

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false' )

    if expire.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has an expired subscription, renew it.")
    
    # check if there's a running subscription
    exist = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )

    if exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has a running subscription, you can only renew it.")
    
    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    startdate = datetime.now()
    enddate = startdate + timedelta(days=30)

    hist = models.SubHistory(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(hist)
    db.commit()
    db.refresh(hist)

    insert = models.Subscription(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


@router.post("/six_month_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def six_month_sub(business_id: int, db: Session = Depends(get_db)):

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false' )

    if expire.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has an expired subscription, renew it.")
    
    # check if there's a running subscription
    exist = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )

    if exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has a running subscription, you can only renew it.")
    
    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    startdate = datetime.now()
    enddate = startdate + timedelta(days=182)

    hist = models.SubHistory(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(hist)
    db.commit()
    db.refresh(hist)

    insert = models.Subscription(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


@router.post("/yearly_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def yearly_sub(business_id: int, db: Session = Depends(get_db)):

    # check if there's an expired subscription
    expire = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'false' )

    if expire.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has an expired subscription, renew it.")
    
    # check if there's a running subscription
    exist = db.query(models.Subscription).filter(models.Subscription.business_id == business_id, models.Subscription.is_active == 'true' )

    if exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This business has a running subscription, you can only renew it.")
    
    #check if business exist
    query = db.query(models.Business).filter(models.Business.id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No business with id of {business_id} found")

    startdate = datetime.now()
    enddate = startdate + timedelta(days=365)

    hist = models.SubHistory(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(hist)
    db.commit()
    db.refresh(hist)

    insert = models.Subscription(business_id = business_id, start_date = startdate, end_date = enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************RENEW SUBSCRIPTION BEFORE EXPIRY******************
@router.post("/renew_monthly_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def renew_monthly_sub(business_id: int,  db: Session = Depends(get_db)):

    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"No subscription history! Start a new subscription")

    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=30)
    else:
        new_enddate = startdate + timedelta(days=30)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscruption that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().end_date = new_enddate
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


@router.post("/renew_six_month_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def renew_six_month_sub(business_id: int,  db: Session = Depends(get_db)):

    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"No subscription history! Start a new subscription")

    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=182)
    else:
        new_enddate = startdate + timedelta(days=182)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscruption that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().end_date = new_enddate
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


@router.post("/renew_yearly_sub/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.Subscription)
def renew_yearly_sub(business_id: int,  db: Session = Depends(get_db)):

    #check it the business have a subscrition history
    query = db.query(models.Subscription).filter(models.Subscription.business_id == business_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"No subscription history! Start a new subscription")

    startdate = datetime.now(timezone.utc)
    current_enddate = query.first().end_date

    if query.first().is_active:
        new_enddate = query.first().end_date + timedelta(days=365)
    else:
        new_enddate = startdate + timedelta(days=365)

    # restrict renewal when you still have at least 60days active subscrition
    print((current_enddate - startdate).days)
    if (current_enddate - startdate).days > 60:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You cannot renew a subscruption that still have more than 60 days before expiration")

    
    #update subscription table
    query.first().start_date = startdate
    query.first().end_date = new_enddate
    query.first().is_active = True

    
    #insert into history
    insert = models.SubHistory(business_id = business_id, start_date = startdate, end_date = new_enddate)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# let frontend call the endpoint to run daily at 00:00
@router.post("/deactivate_sub/}", status_code=status.HTTP_200_OK)
def deactivate_expired_subsription(db:Session = Depends(get_db)):
    currentday: datetime = datetime.now(timezone.utc)
    query = db.query(models.Subscription).filter(models.Subscription.is_active == 'true')

    for i in query:
        if (i.end_date - currentday ).days < 1:
            i.is_active = False
            db.commit() 
            return {"message":"Subscription deactivated"}