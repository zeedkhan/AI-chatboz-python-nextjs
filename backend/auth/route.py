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

    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    redirect_domain = request.session.get("source")

    if user_info:
        user_id = get_or_create_user(user_info)

        # Store the access token and refresh token in the database
        jwt_token = jwt.encode(
            {'sub': user_info['email']}, JWT_SECRET_KEY, algorithm=ALGORITHM)
        store_access_token(user_id, jwt_token, datetime.utcnow(
        ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = jwt.encode({'sub': user_info['email'], 'exp': datetime.utcnow(
        ) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)}, JWT_SECRET_KEY, algorithm=ALGORITHM)
        store_refresh_token(user_id, refresh_token, datetime.utcnow(
        ) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        # store in session
        request.session['jwt_token'] = jwt_token
        response = RedirectResponse(url=redirect_domain)

        # Set cookies in the response
        response.set_cookie("jwt_token", jwt_token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES *
                            60, httponly=True, secure=True, samesite="Lax")
        response.set_cookie("refresh_token", refresh_token, max_age=REFRESH_TOKEN_EXPIRE_DAYS *
                            24 * 60 * 60, httponly=True, secure=True, samesite="Lax")

        return response

    return RedirectResponse(url=redirect_domain)


async def logout(request):
    source = request.query_params.get('source')
    request.session.clear()
    res = RedirectResponse(url=source)

    res.delete_cookie("jwt_token")
    res.delete_cookie("refresh_token")

    return res


def custom_print(t, tt):
    print("*" * 20)
    print(tt)
    print(t)
    print("*" * 20)


async def get_access_token(request):
    try:
        jwt_token = request.session.get('jwt_token')
        if jwt_token:
            return JSONResponse({'access_token': jwt_token})
        else:
            return JSONResponse({'error': "No token found"}, status_code=401)
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=401)
    except Exception as e:
        # Handle other potential exceptions
        return JSONResponse({'error': str(e)}, status_code=500)


# Route to refresh access tokens using a refresh token
async def refresh_access_token(request):
    user = request.user

    jwt_token = request.session.get('jwt_token')

    if user.is_authenticated:
        jwt_token = user.jwt_token

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET_KEY,
                                 algorithms=[ALGORITHM])
            email = payload.get('sub')
            if email:
                new_jwt_token = jwt.encode(
                    {'sub': email}, JWT_SECRET_KEY, algorithm=ALGORITHM)
                response = JSONResponse({'access_token': new_jwt_token})

                response.set_cookie("jwt_token", new_jwt_token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES *
                                    60, httponly=True, secure=True, samesite="Lax")
            return response

        except jwt.ExpiredSignatureError:
            return JSONResponse({"error": "Expired JWT token"}, status_code=401)

        except jwt.InvalidTokenError:
            return JSONResponse({"error": "Invalid JWT token"}, status_code=401)

    return JSONResponse({"error": "No JWT token"}, status_code=401)


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
