from db import dataBase
from starlette.config import Config
from starlette.applications import Starlette
from user import login, home
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse, RedirectResponse, Response
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn
templates = Jinja2Templates(directory='templates')
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.authentication import AuthenticationMiddleware
from auth import BasicAuthBackend, oauth2
from starlette.exceptions import HTTPException
import exceptions



async def homepage(request):
    template = 'index.html'
    context = {'request': request}
    return templates.TemplateResponse(template, context)


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    await response(scope, receive, send)

routes = [
    Route('/', homepage),
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


app = Starlette(debug=True, routes=routes, middleware=middleware)

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

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
