from fastapi import FastAPI
from .routes import users, auth, business, category, catalog, certifications, comments, messages, rating, subscriptions, password_reset, identity, notify, external, auth_google
from .admin_routes import admin_auth, admin_users, admin_business, admin_subscription, admin_details, admin_category, admin_certification, admin_id_card, admin_notify
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ************************ CORS ************************
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

# make uploads folder readable from outside world
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")



app.include_router(auth.router)
app.include_router(auth_google.router)
app.include_router(users.router)
app.include_router(password_reset.router)
app.include_router(business.router)
app.include_router(notify.router)
app.include_router(messages.router)
app.include_router(catalog.router)
app.include_router(certifications.router)
app.include_router(identity.router)
app.include_router(comments.router)
app.include_router(rating.router)
app.include_router(subscriptions.router)
app.include_router(category.router)
app.include_router(external.router)

# admin routes
app.include_router(admin_auth.router)
app.include_router(admin_details.router)
app.include_router(admin_users.router)
app.include_router(admin_business.router)
app.include_router(admin_subscription.router)
app.include_router(admin_category.router)
app.include_router(admin_certification.router)
app.include_router(admin_id_card.router)
app.include_router(admin_notify.router)
