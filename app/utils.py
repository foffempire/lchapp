from passlib.context import CryptContext
import secrets
import random

#**********password Hashing****************
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


#**********random uid****************
def generate_unique_id(len):
    return secrets.token_hex(len)


def generate_referral_code():
    w = random.randint(100000,900000)
    x = generate_unique_id(1)
    y = x.upper()
    z = str(w) + y
    return z


# baseURL = 'http://127.0.0.1:8000/'
baseURL = 'https://lchapp.com.ng/'





