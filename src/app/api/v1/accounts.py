import httpx
import asyncio
from fastapi import APIRouter, status
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
@router.patch("/transfer_money", status_code=status.HTTP_204_NO_CONTENT)
async def transfer_money(
    db: db_dependency,
    user: user_dependency,
    transfer: TransferRequest,
):
    await db_accounts.transfer_money(db, user, transfer)


# Withdraw money from the users account
@router.patch("/withdraw_money", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_money(db: db_dependency, user: user_dependency, amount: int):
    await db_accounts.withdraw_money(db, user.id, amount)


# Deposit money to the users account
@router.patch("/deposit_money", status_code=status.HTTP_204_NO_CONTENT)
async def deposit_money(db: db_dependency, user: user_dependency, amount: int):
    await db_accounts.deposit_money(db, user.id, amount)


# Get random todos from https://sum-server.100xdevs.com/todos
@router.get("/get_random_todos", status_code=status.HTTP_200_OK)
async def get_random_todos():
    urls = ["https://sum-server.100xdevs.com/todos"] * 10
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
    todos = [response.json() for response in responses]
    return todos
