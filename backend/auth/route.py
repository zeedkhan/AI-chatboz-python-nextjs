from starlette.routing import Route
from backend.auth.google import oauth
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
import os
from datetime import datetime, timedelta
import jwt
from backend.auth.main import get_or_create_user, store_access_token, store_refresh_token


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = 30
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def login(request):
    source = request.query_params.get('source')

    request.session['source'] = source

    print("*" * 20)
    print(source)
    print("*" * 20)

    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    redirect_domain = request.session.get("source")

    if user_info:
        jwt_token = jwt.encode({'sub': user_info['email']}, JWT_SECRET_KEY, algorithm=ALGORITHM)
        request.session['jwt_token'] = jwt_token
        # Store the access token and refresh token in the database
        
        user_id = get_or_create_user(user_info)

        store_access_token(user_id, jwt_token, datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = jwt.encode({'sub': user_info['email'], 'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)}, JWT_SECRET_KEY, algorithm=ALGORITHM)
        store_refresh_token(user_id, refresh_token, datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return RedirectResponse(url=redirect_domain)


async def logout(request):
    source = request.query_params.get('source')
    request.session.clear()
    
    return RedirectResponse(url=source)


async def get_access_token(request):
    try:
        jwt_token = request.session.get('jwt_token')
        if jwt_token:
            print(jwt_token)
            return JSONResponse({'access_token': jwt_token})
    except ValueError as e:
        return JSONResponse({'error': e}, status_code=401)
    
    return JSONResponse({'error': "Unauthorize"}, status_code=401)


# Route to refresh access tokens using a refresh token
async def refresh_access_token(request):
    jwt_token = request.session.get('jwt_token')
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get('sub')
            if email:
                new_jwt_token = jwt.encode({'sub': email}, JWT_SECRET_KEY, algorithm=ALGORITHM)
                return JSONResponse({'access_token': new_jwt_token})

        except jwt.ExpiredSignatureError:
            return JSONResponse({"error": "Expired JWT token"}, status_code=401)

        except jwt.InvalidTokenError:
            return JSONResponse({"error": "Invalid JWT token"}, status_code=401)

    return JSONResponse({"error": "JWT token not found"}, status_code=401)


async def homepage(request):
    user = request.user
    if user.is_authenticated:
        html = (
            f'<pre>{f"{user}"}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


auth_route = [
    Route('/login/', endpoint=login),
    Route('/logout/', endpoint=logout),
    Route('/auth', endpoint=auth),
    Route('/token/', endpoint=get_access_token),
    Route('/refresh-token/', endpoint=refresh_access_token),
    Route('/', endpoint=homepage),
]