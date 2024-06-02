from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.user_schema import UserResponse


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: int


class AccountsResponse(BaseModel):
    id: int
    account_balance: int
    user: UserResponse

    class Config:
        orm_mode = True
