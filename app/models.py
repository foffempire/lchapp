from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, Float, Date, DATE
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, func
from sqlalchemy.orm import relationship
from datetime import timedelta, datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    image = Column(String, default="uploads/users/default.png", nullable=True)
    is_active = Column(Boolean, default=True)
    verification_code = Column(Integer, default=111111, nullable=False)
    email_verified = Column(Integer, default=0, nullable=False)
    phone_verified = Column(Integer, default=0, nullable=False)
    date_created = Column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=False)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    level = Column(Integer, default=1)
    date_created = Column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=False)


class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)

    business = relationship("Business")

  
class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, index=True)
    bid = Column(String, nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    about = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    category = Column(String, nullable=True)
    image = Column(String, default="uploads/banner/default.png", nullable=True)
    tag = Column(Text, nullable=False)
    work_experience = Column(Text, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    days = Column(String, nullable=True)
    hour_from = Column(String, nullable=True)
    hour_to = Column(String, nullable=True)
    website = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    has_valid_cert = Column(Integer, nullable=True, default=0)
    has_valid_id = Column(Integer, nullable=True, default=0)
    level = Column(Integer, default=1, nullable=False)
    location = Column(Text, nullable=True)

    subscription = relationship("Subscription")
    owner = relationship("User")
    catalog = relationship("Catalog")
    certifications = relationship("Certifications")
    comments = relationship("Comments")
    sub_history = relationship("SubHistory")


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    image = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    images = relationship("CatalogImg")


class CatalogImg(Base):
    __tablename__ = "catalog_img"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    catalog_id = Column(Integer, ForeignKey("catalog.id", ondelete="CASCADE"), nullable=False)
    image = Column(String, nullable=False)

   
class Certifications(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    disapproved = Column(Integer, default=0, nullable=True)


class Identity(Base):
    __tablename__ = "identity"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    disapproved = Column(Integer, default=0, nullable=True)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    msg = Column(Text, nullable=False)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)    
    date_created = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
    commenter = relationship("User")
    

class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, nullable=False)
    last_message = Column(String, nullable=False)
    date_updated = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    read = Column(Integer, nullable=False, default=0)
    date_added = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    date_created = Column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False, default="uploads/category/default.png")
    description = Column(String, nullable=True)
    parent_id = Column(Integer, nullable=False, default=0)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    date_created = Column(Date, server_default=text("now()"), nullable=False)


class SubHistory(Base):
    __tablename__ = "sub_history"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    date_created = Column(Date, server_default=text("now()"), nullable=False)


class SubPrice(Base):
    __tablename__ = "sub_price"

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date_updated = Column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Integer, default=0)
    date_created = Column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=False)
