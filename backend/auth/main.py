from datetime import datetime
from backend.schemas.user import AccessToken, RefreshToken, User
from backend.db.mysql.main import create_database_session


def store_access_token(user_id: int, token: str, expires_at: datetime):
    session = create_database_session()
    cur_session = session.query(AccessToken).filter_by(user_id=user_id, token=token, expires_at=expires_at)

    if cur_session:
        return cur_session

    access_token = AccessToken(user_id=user_id, token=token, expires_at=expires_at)
    session.add(access_token)
    session.commit()
    session.refresh(access_token)
    session.close()


# Store refresh token and user mapping
def store_refresh_token(user_id: int, token: str, expires_at: datetime):
    session = create_database_session()
    
    cur_refresh_token = session.query(RefreshToken).filter_by(user_id=user_id, token=token, expires_at=expires_at)

    if cur_refresh_token:
        return cur_refresh_token

    refresh_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)
    session.close()


def get_or_create_user(user_info: dict) -> int:
    email = user_info.get('email')
    session = create_database_session()
    print(user_info)
    # Check if user already exists
    user = session.query(User).filter_by(email=email).first()
    print(user)
    if user:
        return user.id
    
    # Create a new user    
    # Extract keys from User class attributes
    user_attributes = [attr.key for attr in User.__table__.columns]
    filtered_user_data = {key: value for key, value in user_info.items() if key in user_attributes}

    new_user = User(**filtered_user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
    return new_user.id