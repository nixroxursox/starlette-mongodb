from db import dataBase
from starlette import applications
from starlette.config import Config
from starlette.applications import Starlette
from user import login, home
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse, RedirectResponse, Response
from starlette.requests import Request
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn
from dotenv import find_dotenv, load_dotenv
templates = Jinja2Templates(directory='templates')
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, BaseUser
)
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.authentication import AuthenticationMiddleware
from auth import BasicAuthBackend, oauth2
from starlette.exceptions import HTTPException


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


def userme(request):
    username = "Site Admin"
    return PlainTextResponse('Hello, %s!' % username)

async def startup():
    assert scope['type'] == 'http'
    request = Request(scope)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    repomse.headers["X-Forwarded-From"]
    response(scope)
    db=dataBase.getdb()
    return db

routes = [
    Route('/', homepage),
    Route('/user/me', userme),
    Route('/auth/login', login, methods=["GET", "POST"]),
    Route('/auth/register', login, methods=["GET", "POST"]),
    Route('/home',home, methods=["GET", "POST"]),
    Route('/templates', templates),
    Mount('/static', StaticFiles(directory="static"), name='static'),
    Mount('/style', StaticFiles(directory="style"), name='style')
]


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({"error": str(exc)}, status_code=401)

app = Starlette(debug=True, routes=routes, middleware=middleware, on_startup=[startup])

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)

@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)

@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8050, log_level="debug", workers=4)
