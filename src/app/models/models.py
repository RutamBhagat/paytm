from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.app.db.database import Base


class DBUsers(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")

    account = relationship("DBAccounts", uselist=False, back_populates="user")


class DBAccounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_balance = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("DBUsers", back_populates="account")
