import os
from datetime import datetime, timedelta
from fastapi import Request
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.app.db.database import get_db
from src.app.db.access_layers import db_users


JWT_SECRET = os.environ.get("JWT_SECRET")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=48)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid authentication credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         # The token is already extracted from the Authorization header by OAuth2PasswordBearer
#         payload = jwt.decode(
#             token,
#             JWT_SECRET,
#             algorithms=[ALGORITHM],
#         )
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         user = await db_users.get_user(db, username)
#         return user
#     except JWTError:
#         raise credentials_exception


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await db_users.get_user(db, username)
        return user
    except JWTError:
        raise credentials_exception
