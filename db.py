from pymongo import MongoClient as mc
import pymongo as pm
import dns
import sys
from starlette.config import Config
from nacl import pwhash
import time
import datetime

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')


class dataBase():
    def getdb():
        try:
            uri1 = DATABASE_URL
            client = mc(uri1,tls=False)
            return client["appdb"]
        except Exception as e:
            print(e)

    def findUser(chkUser):
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            userinfo = coll.find_one({'username': chkUser})
            if userinfo:
                return True
        except Exception as e:
            print(e)

    def addUser(chkUser, password, pin):
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            data = ({'username': chkUser,
                'password': password,
                'pin': pin,
                'isActive': True,
                'isVendor': False,
                'broquerage': int(3),
                'created': datetime.datetime.now(),
                'vendorBond': float(500.00)
                })
            result = coll.insert_one(data)
            if result:
                return True
        except Exception as e:
            print("An exception occurred :", e)
            return False

    def modUser(chkUser, password, pin):
        try:
            db = dataBase.getdb()
            coll = db["userBase"]
            data = ({'username': chkUser})
            result = coll.find_one({'username': chkUser})
            if result:
                changerow = result[ObjectId]
                coll.find_one_and_update
        except pymongo.errors as e:
            print(e)
