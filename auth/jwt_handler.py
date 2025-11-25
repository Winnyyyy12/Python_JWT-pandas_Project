import jwt
from datetime import datetime, timedelta
from typing import Optional

# Replace with secure secret from env / config in production
SECRET_KEY = "051f7880c895f467bfc925eace9cdf781b0b4704248c5c1aee1bab6120a1a06a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict, expires_minutes: Optional[int] = None):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=(expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
