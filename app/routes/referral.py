from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from .. import models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 
router = APIRouter(
    tags=["referral"]
)




@router.get("/user/referral/", status_code=status.HTTP_200_OK)
def referral(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    result = []
    history = []
    #query user
    query = db.query(models.User).filter(models.User.id == current_user.id)

    #amount for each referral
    refQuery = db.query(models.Settings).filter(models.Settings.item == "referral").first()
    ref_amount = int(refQuery.value)

    # get payment history
    hist = db.query(models.Referral.amount_paid).filter(models.Referral.user_id == current_user.id)
    for y in hist.all():
        history.append(y[0])

    # get total amount paid to user
    stmt = db.query(func.sum(models.Referral.amount_paid).label("sum")).filter(models.Referral.user_id == current_user.id)
    total_amount = stmt.all()[0][0]
    if total_amount is None:
        paid_out = 0
    else:
        paid_out = stmt.all()[0][0]
    
    #if user exist
    if query.first():
        #total number of referral
        ref = query.first().referral_code
        counter = db.query(models.User).join(models.Business).filter((models.User.referrer == ref), (models.Business.is_active==True))
        
        total_refferal = len(counter.all())

        available_earnings = (ref_amount*len(counter.all())) - paid_out
        
        return {"total_refferal": total_refferal, "earnings": available_earnings, "payment_history": history}
    else:
        return 0
