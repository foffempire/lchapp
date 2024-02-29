from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, Request
from fastapi.responses import HTMLResponse
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session 
from ..utils import get_password_hash, verify_password, baseURL, generate_unique_id

from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["External"]
)

# Jinja2 templating
templates = Jinja2Templates(directory="templates")



# ***************FAQ PAGE******************
@router.get("/external/terms", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def faq(request: Request, db: Session = Depends(get_db)):

    return templates.TemplateResponse(request=request, name="tandc.html", context={"baseURL": baseURL})


# ***************ABOUT PAGE******************
@router.get("/external/about", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def about(request: Request, db: Session = Depends(get_db)):

    return templates.TemplateResponse(request=request, name="about.html", context={"baseURL": baseURL})



