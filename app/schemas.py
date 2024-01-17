from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Any, Dict

# ***********USER SCHEMAS*************
class RegisterUser(BaseModel):
    email: EmailStr
    password: str

class Password(BaseModel):
    password: str
    old_password: str

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]
    image: Optional[str]
    is_active: bool
    date_created: datetime
    verification_code: Optional[int]
    email_verified: Optional[int]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]
    image: Optional[str]
    is_active: bool
    date_created: datetime
    email_verified: Optional[int]
    

class Personal(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    sex: Optional[str]

class PersonalImg(BaseModel):
    image: str

class ResetPassword(BaseModel):
    email: EmailStr

class VerifyResetPassword(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class VerifyPhone(BaseModel):
    phone: str
    code: int


# authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


#************ RESPOSNSE SCHEMAS ******************
class RegResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    date_created: datetime

    class Config:
        from_attributes = True


class UserResponse(RegResponse):
    pass
    # firstname: Optional[str]
    # lastname: Optional[str]
    # phone: Optional[int]
    # address: Optional[str]
    # city: Optional[str]
    # state: Optional[str]
    # country: Optional[str]

    class Config:
        from_attributes = True



#******************CATALOG SCHEMAS ***********************
class Catalog(BaseModel):
    name: str
    price: Optional[float] 
    description: Optional[str]
    images: List[str]

class CatalogImg(BaseModel):
    image: str

class CatalogExplore(BaseModel):
    catalog_id: int
    image: str

class CatalogResponse(BaseModel):
    id: int
    name: str
    price: Optional[float] 
    description: Optional[str]
    images: List[CatalogImg]


#************ CERTIFICATION SCHEMAs ******************
class Cert(BaseModel):
    name: str
    image: str

class CertResponse(Cert):
    id: int


#******************COMMENTS SCHEMAS ***********************
class Comment(BaseModel):
    msg: str

class CommentResponse(Comment):
    id: int
    business_id: int
    user_id: int
    commenter: UserOut

class Commenter(BaseModel):
    user_id: int



#************ CONVERSATION SCHEMAS ******************
class Conversation(BaseModel):
    conversation_id: str
    sender_id: int
    receiver_id: int
    

#************ MESSAGE SCHEMAS ******************
class Message(BaseModel):
    message: Optional[str]
    image: Optional[str]

class MessageResponse(Message):
    conversation_id: int
    message: str
    image: Optional[str]
    sender_id: int
    read: int
    date_added: datetime

class Conversation(BaseModel):
    id: int
    last_message: str
    date_updated: datetime
    # chat_with: UserOut

#************ RATING SCHEMAS ******************
class Rating(BaseModel):
    rating: int

class RatingResponse(Rating):
    id: int
    business_id: int
    user_id: int
    date_added: datetime


#************ SUBSCRIPTION SCHEMAS ******************
class SubscriptionResponse(BaseModel):
    is_active: bool

class Subscription(BaseModel):
    start_date: datetime
    end_date: datetime

class SubscriptionRenew(BaseModel):
    days: int

class SubHistory(BaseModel):
    id: int
    business_id: int
    start_date: datetime
    end_date: datetime


#************ BUSINESS SCHEMAS ******************

class Business(BaseModel):
    id: int
    bid: str
    name: str
    about: Optional[str]
    category: Optional[str]
    image: Optional[str]
    years_of_experience: Optional[int]
    work_experience: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    location: Optional[str]
    days: Optional[str]
    hour_from: Optional[str]
    hour_to: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    linkedin: Optional[str]
    is_active: bool
    owner: UserOut
    subscription: List[SubscriptionResponse]
    catalog: List[CatalogResponse]
    certifications: List[CertResponse]
    comments: List[CommentResponse]
    # sub_history: List[SubHistory]


class BusinessAbout(BaseModel):
    name: str
    about: Optional[str]
    category: Optional[str]
    work_experience: Optional[str]
    years_of_experience: Optional[int]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

class BusinessExperience(BaseModel):
    work_experience: Optional[str]
    years_of_experience: Optional[int]

class BusinessAddress(BaseModel):
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

class BusinessSocial(BaseModel):
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    linkedin: Optional[str]

class BusinessHour(BaseModel):
    days: Optional[str]
    hour_from: Optional[str]
    hour_to: Optional[str]

class BusinessImage(BaseModel):
    image: str

class BusinessLocation(BaseModel):
    location: str


class BusinessBasic(BaseModel):
    id: int
    name: str
    about: Optional[str]
    category: Optional[str]
    image: Optional[str]    
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]   



#************ SAVED BUSINESS SCHEMA ******************
class Favorite(BaseModel):
    id: int
    user_id: int
    # business_id: int
    business: BusinessBasic


#************ CATEGORY SCHEMA ******************
class Category(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]
    parent_id: int

class CategoryResponse(Category):
    id: int

