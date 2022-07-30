from pymongo import MongoClient as mc
import pymongo as pm
import sys
from starlette.config import Config
from nacl import pwhash, utils, exceptions
import time
import datetime

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')
secret_key_app = config('secret_key_app')


class dataBase():
    def getdb():
        try:
            uri1 = DATABASE_URL
            client = mc(uri1,tls=False)
            return client["appdb"]
        except exceptions as e:
            print(e)

    def getUser(chkUser):
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            userinfo = coll.find_one({'username': chkUser})
            if userinfo:
                return True
        except Exception as e:
            print(e)
    def findAllUsers():
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            userinfo = list(coll.find({},{'_id': 0, 'username': 1}))
            return userinfo
        except exceptons as e:
            print(e)

    def addUser(chkUser, password, pin, a):
        a = a
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            data = ({'username': chkUser,
                'password': pwhash.scryptsalsa208sha256_str(password),
                'pin': pwhash.scryptsalsa208sha256_str(pin),
                'isActive': True,
                'isVendor': False,
                'broquerage': int(3),
                'created': datetime.datetime.now(),
                'vendorBond': float(500.0),
                'is_admin': a,
                'identifier': utils.random(32).hex()
                })
            result = coll.insert_one(data)
            if result:
                return True
        except Exception as e:
            print("An exception occurred :", e)
            return False

    def modUser(chkUser, appPass, newAppPass, pin, newPin):
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            data = ({'username': chkUser})
            if data:
                update = coll.find_one_and_update({'username': chkUser}, { '$set': { 'appPass' : newAppPass, 'pin': newPin}} )
                return update.AFTER
        except Exception as e:
            print("An exception occurred :", e)
            return False
