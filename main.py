from db import dataBase
from starlette import applications
from starlette.config import Config
from starlette.applications import Starlette
from user import login, home
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn
import starlette_login
import starlette_wtf
from os import environ as env
from urllib.parse import quote_plus, urlencode
from dotenv import find_dotenv, load_dotenv
from rforms import checkFormData
templates = Jinja2Templates(directory='templates')
from starlette.authentication import requires
from starlette.responses import RedirectResponse
from auth import oauth2

async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


def userme(request):
    username = "Site Admin"
    return PlainTextResponse('Hello, %s!' % username)

def startup():
    scope = ["receive", "send"]
    db=dataBase.getdb()
    return db

routes = [
    Route('/', homepage),
    Route('/user/me', userme),
    Route('/auth/login', login, methods=["GET", "POST"]),
    Route('/auth/register', login, methods=["GET", "POST"]),
    Route('/auth/token', oauth2, methods=["GET", "POST"]),
    Route('/home',home, methods=["GET", "POST"]),
    Route('/templates', templates),
    Mount('/static', StaticFiles(directory="static"), name='static'),
    Mount('/style', StaticFiles(directory="style"), name='style')
]


app = Starlette(debug=True, routes=routes, on_startup=[startup])


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
