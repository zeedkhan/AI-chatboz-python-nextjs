from starlette.routing import Route
from backend.db.mysql.users import get_current_user 
from starlette.responses import JSONResponse
from starlette.authentication import requires


async def current_user(request):
    user = request.user
    if user.is_authenticated:
        user_detail = get_current_user(user.username)
        return JSONResponse({"user": user_detail})
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


user_route = [
    Route('/', endpoint=requires('authenticated')(current_user)),
]
