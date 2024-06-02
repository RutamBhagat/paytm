from typing import List, Optional
from fastapi import APIRouter, HTTPException, status

from src.app.core.hash import get_password_hash, verify_password
from src.app.schemas.schema import ChangePasswordBody, PatchUserBody, UserResponse
from src.app.db.access_layers import db_users
from src.app.api.dependencies import db_dependency, user_dependency


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def read_users_me(user: user_dependency) -> UserResponse:
    return user


# change password of current user
@router.patch("/me/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: db_dependency, user: user_dependency, password_change: ChangePasswordBody
):
    is_password_correct = verify_password(
        password_change.password, user.hashed_password
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect previous password",
        )

    hashed_password = get_password_hash(password_change.new_password)
    user.hashed_password = hashed_password
    await db_users.update_user(db, user)


# Patch user
@router.patch("/patch_user", status_code=status.HTTP_204_NO_CONTENT)
async def patch_user(
    db: db_dependency, user: user_dependency, user_update: PatchUserBody
):
    await db_users.patch_user(db, user, user_update)


# A route to get users from the backend, filterable via first_name, last_name
@router.get(
    "/get_users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
)
async def get_users(
    db: db_dependency,
    user: user_dependency,
    search_filter: Optional[str] = None,
):
    users = await db_users.get_filtered_users(db, search_filter)
    return users
