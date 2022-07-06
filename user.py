from starlette import datastructures as ds
import starlette.applications
from starlette.applications import Starlette, Request as rq
from starlette.config import Config
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from nacl import pwhash, exceptions, utils
from starlette.templating import Jinja2Templates
from db import dataBase
from starlette.formparsers import FormParser as fp
from starlette_login import login_manager
import starlette_wtf
from starlette.endpoints import HTTPEndpoint
from rforms import checkFormData
from starlette.authentication import requires
from starlette.responses import RedirectResponse
import os
import binascii
import DateTime
import time

templates = Jinja2Templates(directory='templates')


async def login(request):
    if request.method == "GET":
        return templates.TemplateResponse('login.html', {'request': request})
    if request.method == "POST":
        rformsdata = await request.form()
        chkuser = rformsdata['username']
        db = dataBase.getdb()
        coll = db["Userbase"]
        mtchuser = coll.find_one({'username': chkuser})
        if mtchuser:
            dbpass = mtchuser["password"]
            pin = mtchuser["pin"]
            mypass = pwhash.scryptsalsa208sha256_str(bytes(rformsdata['password'], encoding="UTF-8"))
            chkpin = pwhash.scryptsalsa208sha256_str(bytes(rformsdata['pin'], encoding="UTF-8"))
            if mypass == dbpass and chkpin ==  pin:
                return templates.TemplateResponse('profile.html', {'request': request})
            else:
                return templates.TemplateResponse('register.html', {'request': request})
        else:
            password = pwhash.scryptsalsa208sha256_str(bytes(rformsdata['password'], encoding="UTF-8"))
            pin = pwhash.scryptsalsa208sha256_str(bytes(rformsdata['pin'], encoding="UTF-8"))
            print("Username not found.  Please register to create an account")
            useradd = dataBase.addUser(chkuser, password, pin)
            return useradd[ObjectId]


class session:
    def __init__(self, key, ttl_seconds, expires, path, domain, secure, http, samesite):
        self.key = binascii.hexlify(os.urandom(24))
        self.ttl_seconds = int(600)
        self.expires = datetime.datetime.now() + int(600)
        self.path = '/user'
        self.domain = 'localhost'
        self.secure = pwhsh.argon2i.str(domain)
        self.http = True
        self.samesite = 'CORS[*]'

class loginMgr:
    def __init__(self):
        self.key,
        self.ttl=0,
        self.expires=3600,
        path=path,
        domain=domain,
        secure=secure,
        httponly=httponly,
        samesite=samesite


async def home(request):
    return templates.TemplateResponse('home.html', {'request': request})
