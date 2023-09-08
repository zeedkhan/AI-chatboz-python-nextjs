from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    sub = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)  # Specify a length
    name = Column(String(255))
    picture = Column(String(255))
    given_name = Column(String(255))
    family_name = Column(String(255))
    email_verified = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)


class AccessToken(Base):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String(255), unique=True, index=True)
    expires_at = Column(DateTime)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String(255), unique=True, index=True)
    expires_at = Column(DateTime)