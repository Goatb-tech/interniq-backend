from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)
