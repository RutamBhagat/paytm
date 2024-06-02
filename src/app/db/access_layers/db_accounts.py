from random import randint
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from src.app.schemas.accounts_schema import TransferRequest
from src.app.models.models import DBAccounts, DBUsers


account_not_found = HTTPException(
    status.HTTP_400_BAD_REQUEST, detail="Account not found"
)
infufficient_funds = HTTPException(
    status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
)


class TransferError(Exception):
    """Exception raised for errors in the transfer process."""

    def __init__(self, message="An error occurred during the transfer"):
        self.message = message
        super().__init__(self.message)


# find account by user_id or account id
async def get_account(
    db: Session, user_id: Optional[int] = None, account_id: Optional[int] = None
) -> DBAccounts:
    if user_id is None and account_id is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="User ID or account ID is required"
        )

    if user_id is not None:
        account = (
            db.query(DBAccounts).filter(DBAccounts.user_id == user_id).one_or_none()
        )
        return account
    elif account_id is not None:
        account = db.query(DBAccounts).filter(DBAccounts.id == account_id).one_or_none()
        return account
    else:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="User ID or account ID is required"
        )


# create account for user if user_id is already in the database throw an error
async def create_account(db: Session, user_id: int) -> DBAccounts:
    account = await get_account(db, user_id=user_id)
    if account is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Account already exists for this user"
        )
    # Ideally, the balance should be 0 by default but for testing purposes, we'll set it to a random number between 100 and 1000
    # Generate a random balance between 100 and 1000
    account = DBAccounts(user_id=user_id, account_balance=randint(100, 1000))
    # account = DBAccounts(user_id=user_id)
    db.add(account)
    db.commit()
    return account


# transfer money from one account to another
# Note: This function should be a transaction and should properly deduct the amount from the from_account and add it to the to_account
# This function should also check for sufficient funds in the from_account
async def transfer_money(
    db: Session, user: DBUsers, transfer: TransferRequest
) -> DBAccounts:
    from_account = await get_account(db, user_id=user.id)
    to_account = await get_account(db, account_id=transfer.to_account_id)

    if from_account is None or to_account is None:
        raise account_not_found

    if from_account.account_balance < transfer.amount:
        raise infufficient_funds

    try:
        # Lock the source account to prevent concurrent transfers
        db.query(DBAccounts).filter(
            DBAccounts.id == from_account.id
        ).with_for_update().one()

        from_account.account_balance -= transfer.amount
        to_account.account_balance += transfer.amount
        db.add(from_account)
        db.add(to_account)
        db.commit()
    except Exception as e:
        db.rollback()
        raise TransferError(str(e))

    return from_account


# withdraw money from the user account
async def withdraw_money(db: Session, user_id: int, amount: int) -> DBAccounts:
    account = await get_account(db, user_id=user_id)
    if account is None:
        raise account_not_found

    if account.account_balance < amount:
        raise infufficient_funds

    try:
        # Lock the source account to prevent concurrent transfers
        db.query(DBAccounts).filter(DBAccounts.id == account.id).with_for_update().one()

        account.account_balance -= amount
        db.add(account)
        db.commit()
    except Exception as e:
        db.rollback()
        raise TransferError(str(e))


# deposit money to the user account
async def deposit_money(db: Session, user_id: int, amount: int) -> DBAccounts:
    account = await get_account(db, user_id=user_id)
    if account is None:
        raise account_not_found

    try:
        # Lock the source account to prevent concurrent transfers
        db.query(DBAccounts).filter(DBAccounts.id == account.id).with_for_update().one()

        account.account_balance += amount
        db.add(account)
        db.commit()
    except Exception as e:
        db.rollback()
        raise TransferError(str(e))
