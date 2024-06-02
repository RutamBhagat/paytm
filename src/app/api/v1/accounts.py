from fastapi import APIRouter, Body, HTTPException, status
from src.app.schemas.accounts_schema import AccountsResponse, TransferRequest
from src.app.db.access_layers import db_accounts
from src.app.api.dependencies import db_dependency, user_dependency

router = APIRouter(prefix="/accounts", tags=["accounts"])


# Get the account of the user
@router.get(
    "/get_account",
    status_code=status.HTTP_200_OK,
    response_model=AccountsResponse,
)
async def get_account(db: db_dependency, user: user_dependency) -> AccountsResponse:
    account = await db_accounts.get_account(db, user.id)
    return account


# Create a new account for the user
@router.post(
    "/create_account",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountsResponse,
)
async def create_account(db: db_dependency, user: user_dependency) -> AccountsResponse:
    account = await db_accounts.create_account(db, user.id)
    return account


# Transfer money from one account id to another account id
@router.post(
    "/transfer_money",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountsResponse,
)
async def transfer_money(
    db: db_dependency,
    user: user_dependency,
    transfer=TransferRequest,
) -> AccountsResponse:
    account = await db_accounts.transfer_money(db, transfer)
    return account
