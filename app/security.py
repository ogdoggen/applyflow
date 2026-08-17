from datetime import datetime, timedelta, timezone
from app.config import settings
import jwt

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return  password_hash.hash(password)


def verify_password(password:str, hashed_password:str):
    return password_hash.verify(password, hashed_password)

def create_access_token(subject):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub" : str(subject),
        "exp" : expire,
    }
    token = jwt.encode(payload, settings.secret_key, settings.jwt_algorithm)
    return token
