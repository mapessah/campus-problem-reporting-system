from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db

router = APIRouter(tags=["Health"])


@router.get("/health/database")
async def database_health(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        await db.execute(text("SELECT 1"))

        return {
            "success": True,
            "message": "Database connection successful"
        }

    except SQLAlchemyError:
        return {
            "success": False,
            "message": "Database connection failed"
        }
