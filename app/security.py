from datetime import datetime, timedelta, timezone
from app.config import settings
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

def decode_access_token(token : str):
    try:
        payload = jwt.decode(token, settings.secret_key, [settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="unauthorized")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="unauthorized")
    return user_id
