from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 
from typing import List

router = APIRouter(
    tags=['comments']
)

def verify_owner(comment_id, user_id, db):    
    comm = db.query(models.Comments).filter(models.Comments.id == comment_id).first()
    if user_id == comm.user_id:
        return True

# ***************ADD COMMENT*******************
@router.post("/comment/{business_id}", status_code=status.HTTP_200_OK, response_model=schemas.CommentResponse)
def add_comment(business_id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Comments).filter(models.Comments.user_id == current_user.id, models.Comments.business_id == business_id)

    if not current_user.firstname:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Update your firstname and lastname to post a comment")

    if query.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"You already commented on this business")
    
    insert = models.Comments(business_id = business_id, user_id = current_user.id, **comment.model_dump())
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert


# ***************UPDATE COMMENT*******************
@router.put("/comment/{comment_id}", status_code=status.HTTP_200_OK)
def update_comment(comment_id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found")
    
    if not verify_owner(comment_id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to edit someone else's comment")
    
    query.update(comment.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()




 

# ***************DELETE COMMENT*******************
@router.delete('/comment/{comment_id}')
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found")


    if not verify_owner(comment_id, current_user.id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete someone else's comment")


    query.delete(synchronize_session=False)
    db.commit()
    return{"data":"deleted"}


# ***************GET COMMENTS*******************
@router.get('/comment/{business_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CommentResponse])
def get_comments(business_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Comments).filter(models.Comments.business_id == business_id).all()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No certificates found")   
    return query