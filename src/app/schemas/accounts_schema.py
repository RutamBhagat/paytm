from pydantic import BaseModel, Field

from src.app.schemas.user_schema import UserResponse


class TransferRequest(BaseModel):
    amount: int = Field(..., gt=0)
    to_account_id: int = Field(..., gt=0)


class AccountsResponse(BaseModel):
    id: int
    account_balance: int
    user: UserResponse

    class Config:
        from_attributes = True
