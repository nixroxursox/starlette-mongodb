from wtforms import DateTimeField, HiddenField, SubmitField, validators, PasswordField, FormField, utils, widgets, Form
from starlette import datastructures as ds
import starlette.applications
from starlette.applications import Starlette, Request as rq
from starlette.config import Config
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from nacl import pwhash, exceptions
import requests
from starlette.templating import Jinja2Templates
from db import dataBase
from starlette.formparsers import FormParser as fp
from starlette.endpoints import HTTPEndpoint


class checkFormData():
    def __init__(form, vars, values):
        self.form = []
        self.form = rformsdata
    def formcheck(form):
        for i in form.items():
            if i == 'username':
                min = int(3)
                max = int(56)
                if i < min:
                    invalid = True
                elif i > max:
                    invalid = True
                return PlainTextResponse("Username Invalid, Please try again" + "\n")
            elif i == 'pass':
                min = int(8)
                illegal_chars = []
                illegal_chars = ['!','?','@','/','\\','|','>','<','*','%','&','{','}','\'','\"']

                return print("checked the stupid Password")
            elif i == 'pin':
                valid = pwhash.verify_scryptsalsa208sha256(dbpin, pin)
            else:
                return print("your mom")


def add_headers(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "deny"
    response.headers["Access-Control-Allow-Origin"] = request.client.host
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "cache-control,x-requested-with,content-type,authorization"
    response.headers[
        "Access-Control-Allow-Methods"
    ] = "POST, PUT, GET, OPTIONS, DELETE"
    return response
