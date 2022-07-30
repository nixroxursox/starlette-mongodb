from starlette.config import Config
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse, RedirectResponse, Response
from starlette.requests import Request, HTTPConnection
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn
from db import dataBase
from starlette.middleware.exceptions import HTTPException
from user import login, home
from auth import authClass, user, protected_page
import exceptions
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from starlette.middleware import Middleware
from starlette_login.backends import SessionAuthBackend, BaseAuthenticationBackend
from starlette_login import login_manager
from starlette_login.login_manager import LoginManager
from starlette_login.middleware import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette import status
from login import login_page, logout_page, home_page
from models.loginmodel import UserList, User, user_list


templates = Jinja2Templates(directory='templates')
config = Config(".env")

middleware = [
    Middleware(SessionMiddleware, secret_key=config("SECRET_KEY"), max_age=config("MAX_AGE")),
    Middleware(AuthenticationMiddleware, secret_key=config("SECRET_KEY"), login_manager=login_manager, login_route='login', backend=SessionAuthBackend(login_manager)),
    Middleware(RawContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(),
        plugins.CorrelationIdPlugin(),
        plugins.ForwardedForPlugin(),
        plugins.UserAgentPlugin(),
        plugins.ApiKeyPlugin()
    ),
   )
]

receive = Request["receive"]
scope = Request["Scope", receive]


async def homepage(request):
    template = 'index.html'
    context = {"request": request}
    return templates.TemplateResponse(template, context)

async def startup():
    scope = ["receive", "send"]
async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    await response(scope, receive, send)

routes = [
    Route('/', homepage),
    Route('/auth/login', login, methods=["GET", "POST"]),
    Route('/user/{username}', user),
    Route('/auth/register', login, methods=["GET", "POST"]),
    Route('/home',home, methods=["GET", "POST"]),
    Route('/templates', templates),
    Route('/login', login, methods=['GET', 'POST'], name='login'),
    Route('/logout', logout_page, name='logout'),
    Route('/protected', protected_page, name='protected'),
    Mount('/static', StaticFiles(directory="static"), name='static'),
    Mount('/style', StaticFiles(directory="style"), name='style')
    ]


#login_manager = LoginManager(redirect_to='login', secret_key=config('secret_key_app'))
#login_manager.set_user_loader(user_list.user_loader)
secret_key_app=config("secret_key_app")
key = secret_key_app
SESSION_NAME_KEY=config("SESSION_NAME_KEY")


app = Starlette(debug=True, middleware=middleware, routes=routes,on_startup=[startup])


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

@app.exception_handler(401)
async def unprocessable(request, exc):
    """
    Return an HTTP 401 page.
    """
    template = "401.html"
    context = {"request": request}
    content={"Error": "Invalid request"}
    return templates.TemplateResponse(template, context, content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host='0.0.0.0', port=8050, log_level="debug", workers=2)
