"""
Authentication endpoints.

SECURITY:
  - bcrypt rounds=12
  - Login uses constant-time dummy hash comparison even on unknown email (timing-safe)
  - Login error messages are intentionally vague — do not reveal which field is wrong
  - SYSTEM_ADMIN cannot be created via this API — seed script only
  - bank_id on new users ALWAYS comes from the JWT of the creating admin, never from body
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.dependencies import (
    AdminDep, CurrentUser, DbDep, get_client_ip, get_current_user,
)
from app.models.db import Bank, User, write_audit_log

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12)

_DUMMY_HASH = pwd_context.hash("__dummy__")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user: User) -> tuple[str, datetime]:
    now = datetime.now(tz=timezone.utc)
    expiry = now + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": str(user.id),
        "bank_id": str(user.bank_id),
        "role": user.role,
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, expiry


# ─── SCHEMAS ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    bank_name: str
    bank_short_code: str
    admin_email: EmailStr
    admin_password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    bank_id: uuid.UUID
    active: bool
    created_at: datetime


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    request: Request,
    db: AsyncSession = DbDep,
) -> TokenResponse:
    """Register a new bank and its first BANK_ADMIN user."""
    existing = await db.execute(
        select(Bank).where(Bank.short_code == body.bank_short_code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Bank short code already registered.")

    email_row = await db.execute(select(User).where(User.email == body.admin_email))
    if email_row.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered.")

    bank = Bank(name=body.bank_name, short_code=body.bank_short_code)
    db.add(bank)

    try:
        await db.flush()

        user = User(
            bank_id=bank.id,
            email=body.admin_email,
            password_hash=hash_password(body.admin_password),
            role="BANK_ADMIN",
        )
        db.add(user)
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Bank short code or email already registered.")

    await write_audit_log(
        db, action="BANK_REGISTER",
        user_id=user.id, case_id=None,
        detail={"bank_id": str(bank.id), "bank_short_code": bank.short_code},
        ip_address=get_client_ip(request),
    )
    await db.commit()

    token, expiry = create_access_token(user)
    return TokenResponse(access_token=token, expires_at=expiry)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = DbDep,
) -> TokenResponse:
    """Authenticate. Error messages are intentionally vague — do not hint which field is wrong."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user is None:
        # Run the dummy hash to prevent timing attacks revealing email existence
        verify_password(body.password, _DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if not user.active:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if not user.bank.active:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    await write_audit_log(
        db, action="LOGIN",
        user_id=user.id,
        ip_address=get_client_ip(request),
    )
    await db.commit()

    token, expiry = create_access_token(user)
    return TokenResponse(access_token=token, expires_at=expiry)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = DbDep,
) -> TokenResponse:
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    if user is None or not user.active:
        raise HTTPException(status_code=401, detail="User not found or inactive.")
    token, expiry = create_access_token(user)
    return TokenResponse(access_token=token, expires_at=expiry)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    body: CreateUserRequest,
    request: Request,
    current_user: CurrentUser = AdminDep,
    db: AsyncSession = DbDep,
) -> UserResponse:
    """Create a bank user. Only BANK_ADMIN or SYSTEM_ADMIN can create users.
    bank_id comes from the admin's JWT — never from the request body.
    SYSTEM_ADMIN cannot be created here — use the seed script.
    """
    if body.role not in ("BANK_OFFICER", "BANK_ADMIN"):
        raise HTTPException(
            status_code=400,
            detail="Role must be BANK_OFFICER or BANK_ADMIN. SYSTEM_ADMIN is seed-only."
        )

    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = User(
        bank_id=current_user.bank_id,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
    )
    db.add(user)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered.")

    await write_audit_log(
        db, action="USER_CREATE",
        user_id=current_user.user_id,
        detail={"new_user_id": str(user.id), "role": user.role},
        ip_address=get_client_ip(request),
    )
    await db.commit()

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        bank_id=user.bank_id,
        active=user.active,
        created_at=user.created_at,
    )


@router.get("/me", response_model=UserResponse)
async def whoami(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = DbDep,
) -> UserResponse:
    result = await db.execute(select(User).where(User.id == current_user.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        bank_id=user.bank_id,
        active=user.active,
        created_at=user.created_at,
    )
