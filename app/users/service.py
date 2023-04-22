import bcrypt

async def hash_password(data):
    return bcrypt.hashpw(data.encode('utf-8'), bcrypt.gensalt())

async def verify_password(data, hash_pass):
    return bcrypt.checkpw(data.encode('utf-8'), hash_pass.encode('utf-8'))

def ResponseOut(message, status, data):
    return {
        "message_id" : message,
        "status" : status,
        "data" : data
    }
    
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError, decode
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
BLACKLIST = set()

bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = credentials.credentials
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        now = datetime.utcnow()
        expire = datetime.fromtimestamp(payload["exp"])
        if now > expire:
            raise HTTPException(status_code=401, detail="Token has expired")
        if token in BLACKLIST:
            raise HTTPException(status_code=401, detail="User has logout")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload