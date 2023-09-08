import jwt
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser
import os


ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class JWTUser(SimpleUser):
    def __init__(self, email, jwt_token):
        super().__init__(email)
        self.jwt_token = jwt_token


class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            jwt_token = auth_header.split()[1]
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
                email = payload.get("sub")
                if email:
                    user = JWTUser(email=email, jwt_token=jwt_token)
                    return AuthCredentials(["authenticated"]), user
            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass
        return None
