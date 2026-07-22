"""
Seed script — creates the Demo Bank and SYSTEM_ADMIN user.

Run once after alembic upgrade head:
    .venv\\Scripts\\python.exe scripts/seed_db.py

Idempotent — safe to re-run. Checks for existing bank short_code before inserting.

SYSTEM_ADMIN cannot be created via the API — this script is the only way.
Default credentials (CHANGE AFTER FIRST LOGIN):
    Email:    admin@slrai.internal
    Password: Admin@1234!Change
"""

from __future__ import annotations

import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from passlib.context import CryptContext

from app.config import settings

SYNC_URL = settings.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")

DEMO_BANK_NAME = "SLRAI Demo Bank"
DEMO_BANK_SHORT_CODE = "SLRAI_DEMO"
ADMIN_EMAIL = "admin@slrai.internal"
ADMIN_PASSWORD = "Admin@1234!Change"

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12)


def main() -> None:
    engine = create_engine(SYNC_URL, echo=False)

    with engine.begin() as conn:
        # Check if demo bank already exists
        row = conn.execute(
            text("SELECT id FROM banks WHERE short_code = :code"),
            {"code": DEMO_BANK_SHORT_CODE},
        ).fetchone()

        if row:
            bank_id = row[0]
            print(f"[seed] Demo bank already exists: {bank_id}")
        else:
            bank_id = str(uuid.uuid4())
            conn.execute(
                text("""
                    INSERT INTO banks (id, name, short_code, active)
                    VALUES (:id, :name, :short_code, TRUE)
                """),
                {"id": bank_id, "name": DEMO_BANK_NAME, "short_code": DEMO_BANK_SHORT_CODE},
            )
            print(f"[seed] Created demo bank: {bank_id}")

        # Check if SYSTEM_ADMIN already exists
        admin_row = conn.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": ADMIN_EMAIL},
        ).fetchone()

        if admin_row:
            print(f"[seed] SYSTEM_ADMIN already exists: {admin_row[0]}")
        else:
            user_id = str(uuid.uuid4())
            password_hash = pwd_context.hash(ADMIN_PASSWORD)
            conn.execute(
                text("""
                    INSERT INTO users (id, bank_id, email, password_hash, role, active)
                    VALUES (:id, :bank_id, :email, :password_hash, 'SYSTEM_ADMIN', TRUE)
                """),
                {
                    "id": user_id,
                    "bank_id": bank_id,
                    "email": ADMIN_EMAIL,
                    "password_hash": password_hash,
                },
            )
            print(f"[seed] Created SYSTEM_ADMIN: {user_id}")
            print(f"[seed] Email:    {ADMIN_EMAIL}")
            print(f"[seed] Password: {ADMIN_PASSWORD}")
            print("[seed] IMPORTANT: Change this password after first login!")

    print("[seed] Done.")


if __name__ == "__main__":
    main()
