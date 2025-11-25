from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from database import get_db
from models import users_table
from sqlalchemy import select, insert
from auth.jwt_handler import create_access_token
import re

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Argon2 hashing (secure and Windows-friendly)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ----------------------------------------------------------
# Pydantic Schemas
# ----------------------------------------------------------

class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# ----------------------------------------------------------
# Password Strength Validation
# ----------------------------------------------------------

def validate_password_strength(password: str):
    if (not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[@$!%*?&]", password)):
        raise HTTPException(
            status_code=400,
            detail="Password must include uppercase, lowercase, number, and special character."
        )


# ----------------------------------------------------------
# Register User
# ----------------------------------------------------------

@router.post("/register")
def register_user(payload: RegisterSchema, db=Depends(get_db)):
    username = payload.username
    email = payload.email
    password = payload.password

    validate_password_strength(password)

    # Check duplicates
    existing = db.execute(
        select(users_table).where(
            (users_table.c.email == email) |
            (users_table.c.username == username)
        )
    ).fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists.")

    hashed_pw = pwd_context.hash(password)

    stmt = insert(users_table).values(
        username=username,
        email=email,
        password=hashed_pw,
        is_online=0
    )

    db.execute(stmt)

    return {"message": "User registered successfully"}


# ----------------------------------------------------------
# Login User (email + password only)
# ----------------------------------------------------------

@router.post("/login")
def login(payload: LoginSchema, db=Depends(get_db)):
    email = payload.email
    password = payload.password

    # Fetch user by email only
    user = db.execute(
        select(users_table).where(users_table.c.email == email)
    ).fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Mark online
    db.execute(
        users_table.update()
        .where(users_table.c.id == user.id)
        .values(is_online=1)
    )

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
