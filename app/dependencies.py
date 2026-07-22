"""
FastAPI dependency factories.

SECURITY:
  - bank_id MUST come from the JWT payload — never from request body.
  - verify_case_bank_access returns 404 (not 403) to avoid leaking case existence.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Callable

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.db import AsyncSessionLocal, Case

_bearer = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    user_id: uuid.UUID
    bank_id: uuid.UUID
    role: str
    email: str


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


DbDep = Depends(get_db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    try:
        return CurrentUser(
            user_id=uuid.UUID(payload["sub"]),
            bank_id=uuid.UUID(payload["bank_id"]),
            role=payload["role"],
            email=payload["email"],
        )
    except (KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Malformed token payload.")


CurrentUserDep = Depends(get_current_user)


def require_role(*allowed_roles: str) -> Callable:
    """Factory: returns a dependency that raises 403 if the user's role is not in allowed_roles."""
    async def _check(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access requires one of: {', '.join(allowed_roles)}.",
            )
        return current_user
    return Depends(_check)


AdminDep   = require_role("BANK_ADMIN", "SYSTEM_ADMIN")
OfficerDep = require_role("BANK_OFFICER", "BANK_ADMIN", "SYSTEM_ADMIN")


async def verify_case_bank_access(
    case_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession,
) -> Case:
    """Return the Case if it belongs to the user's bank, else raise 404.

    404 (not 403) is intentional — do not reveal that a case exists in another bank.
    """
    result = await db.execute(
        select(Case).where(
            Case.id == case_id,
            Case.bank_id == current_user.bank_id,
        )
    )
    case = result.scalar_one_or_none()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found.")
    return case


def get_client_ip(request: Request) -> str | None:
    """X-Forwarded-For is only trusted when it comes from a known reverse
    proxy — otherwise any caller could spoof the IP recorded in audit_log."""
    direct_ip = request.client.host if request.client else None
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for and direct_ip in settings.trusted_proxy_ips:
        return forwarded_for.split(",")[0].strip()
    return direct_ip
