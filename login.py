from starlette.requests import Request
import starlette_login





async def login_page(request: Request):
    error = ''
    if request.user.is_authenticated:
        return RedirectResponse('/', 302)
    if request.method == 'POST':
        body = (await request.body()).decode()
        data = dict(parse_qsl(body))
        user = user_list.get_by_username(data['username'])
        if not user:
            error = 'Invalid username'
        elif user.check_password(data['password']) is False:
            error = 'Invalid password'
        else:
            await login_user(request, user)
            return RedirectResponse('/', 302)
    return HTMLResponse(LOGIN_PAGE.format(error=error))


async def logout_page(request: Request):
    if request.user.is_authenticated:
        content = 'Logged out'
        await logout_user(request)
    else:
        content = 'You not logged in'
    return PlainTextResponse(content)


async def home_page(request: Request):
    if request.user.is_authenticated:
        content = f'You are logged in as {request.user.username}'
    else:
        content = 'You are not logged in'
    return PlainTextResponse(content=content)
