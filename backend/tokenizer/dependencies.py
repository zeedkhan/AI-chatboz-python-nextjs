from fastapi import Request

from src.tokenizer.tokenizer import TokenService


def get_token_service(request: Request) -> TokenService:
    return TokenService(request.app.state.token_encoding)