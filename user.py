from starlette import datastructures as ds
import starlette.applications
from starlette.applications import Starlette, Request as rq
from starlette.config import Config
from starlette.responses import PlainTextResponse, Response, RedirectResponse, JSONResponse
from starlette.routing import Route
from nacl import pwhash, exceptions, utils
from starlette.templating import Jinja2Templates
from db import dataBase
from starlette.formparsers import FormParser as fp
from starlette_login import login_manager
import starlette_wtf
from starlette.endpoints import HTTPEndpoint
import base64
from starlette.requests import Request, HTTPConnection
import os
import binascii
import DateTime
import time
import exceptions


templates = Jinja2Templates(directory='templates')


async def login(request):
    def showlogin():
        if request.method == "GET":
            return templates.TemplateResponse('login.html', {"request": request})
    async def authentication():
        if request.method == "GET":
            return login.showlogin
        if request.method == "POST":
            rformsdata = await request.form()
            chkUser = rformsdata['username']
            db = dataBase.getdb()
            coll = db["userBase"]
            mtcUser = coll.find_one({},{'username': 1, 'appPass': 1, 'pin': 1})
            if mtcUser:
                exception = None
                dbpass = mtcUser["appPass"]
                pin = mtcUser["pin"]
                try:
                    credCheck = pwhash.verify(dbpass, bytes(rformsdata['password'], encoding="UTF-8"))
                    pincheck = pwhash.verify(pin, bytes(rformsdata['pin'], encoding="UTF-8"))
                except:
                    e = "wrong password jackass"
                    template = 'login.html'
                    context = {"request": request, 'data': e }
                    headers = {
                        "WWW-Authenticate": "Bearer"
                    }
                    return templates.TemplateResponse(template, context, headers, status_code=InvalidCredentialsException.status_code)

                if credCheck == True:
                    try:
                        if pincheck == True:
                            template = 'profile.html'
                            context = {"request": request, 'name': chkUser}
                            headers = {
                                "WWW-Authenticate": True
                            }
                            return templates.TemplateResponse(template, context, headers)

                    except:
                        template = '404.html'
                        context = {"request": request, 'data': nacl.exceptions}
                        return templates.TemplateResponse(template, context)
                else:
                    exception = exceptions
                    print(exception)
            else:
                print("Username not found.  Please register to create an account")
                useradd = dataBase.addUser(chkUser, appPass, pin)
    #            return useradd[ObjectId]


async def home(request: Request):
    template = 'home.html'
    context = {"request": request}
    content = {"Error": "logged in as {% username %}"}
    return templates.TemplateResponse(template, context, content)
