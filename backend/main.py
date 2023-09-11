from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import os
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from backend.auth.jwt import JWTAuthenticationBackend
from starlette.routing import Mount
from backend.auth.route import auth_route
from backend.db.mysql.route import user_route
from backend.agent.chatbot import chat_router

SECRET_KEY = os.getenv("SECRET_KEY")


middlewares = [
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend()),
]
app = Starlette(
    debug=True,
    middleware=middlewares,
    routes=[
        Mount('/user', routes=user_route),
        Mount('/chat', routes=chat_router),
        Mount('/', routes=auth_route),
    ]
)


app.add_middleware(
    CORSMiddleware,
    # Allow requests from any origin during development
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
