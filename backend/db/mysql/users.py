from backend.db.mysql.main import create_database_session
from backend.schemas.user import User, AccessToken
from typing import List
from sqlalchemy.orm import class_mapper
from datetime import datetime


def serialize_user(user):
    serialized = {column.name: getattr(
        user, column.name) for column in class_mapper(User).mapped_table.columns}

    # Convert datetime to string representation
    if 'created_at' in serialized and isinstance(serialized['created_at'], datetime):
        serialized['created_at'] = serialized['created_at'].isoformat()

    return serialized


def get_users_db() -> List[User]:
    session = create_database_session()
    users = session.query(User).all()
    serialized_users = [serialize_user(user) for user in users]
    return serialized_users


def get_current_user(email):
    session = create_database_session()
    user = session.query(User).filter_by(email=email).first()
    # access_token = session.query(AccessToken).filter(token=access_token)
    if user:
        user_se = serialize_user(user)

        print("*" * 20)
        print(user_se)
        print("*" * 20)

        return user_se
    return None
