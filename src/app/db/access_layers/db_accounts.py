from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.schemas.accounts_schema import TransferRequest
from src.app.models.models import DBAccounts


class TransferError(Exception):
    """Exception raised for errors in the transfer process."""

    def __init__(self, message="An error occurred during the transfer"):
        self.message = message
        super().__init__(self.message)


# find account by user_id
async def get_account(db: Session, user_id: Optional[int] = None) -> DBAccounts:
    if user_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User ID is required")
    account = db.query(DBAccounts).filter(DBAccounts.user_id == user_id).first()
    return account


# create account for user if user_id is already in the database throw an error
async def create_account(db: Session, user_id: int) -> DBAccounts:
    account = db.query(DBAccounts).filter(DBAccounts.user_id == user_id).first()
    if account is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Account already exists for this user"
        )
    account = DBAccounts(user_id=user_id)
    db.add(account)
    db.commit()
    return account


# transfer money from one account to another
# Note: This function should be a transaction and should properly deduct the amount from the from_account and add it to the to_account
# This function should also check for sufficient funds in the from_account
async def transfer_money(db: Session, transfer: TransferRequest) -> DBAccounts:
    from_account = await get_account(db, transfer.from_account_id)
    to_account = await get_account(db, transfer.to_account_id)

    if from_account is None or to_account is None:
        raise TransferError("Account not found")

    if from_account.account_balance < transfer.amount:
        raise TransferError("Insufficient funds")

    try:
        with db.begin():
            # Lock the source account to prevent concurrent transfers
            db.query(DBAccounts).filter(
                DBAccounts.id == from_account.id
            ).with_for_update().one()

            from_account.account_balance -= transfer.amount
            to_account.account_balance += transfer.amount
    except Exception as e:
        db.rollback()
        raise TransferError(str(e))

    return from_account
