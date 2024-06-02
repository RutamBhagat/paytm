from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.app.core.auth import get_current_user
from src.app.db.database import get_db


login_dependency = Annotated[
    OAuth2PasswordRequestForm, Depends()
]  # NOTE: The Depends() does not need any params
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]
