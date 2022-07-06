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
            #uri1 = "mongodb+srv://btc-cluster.gghyb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
            uri1 = DATABASE_URL
            client = mc(uri1,tls=False)
            return client["AUTHDB"]
        except Exception as e:
            print(e)

    def findUser(x):
        try:
            db = dataBase.getdb()
            coll = db["Userbase"]
            userinfo = coll.find_one({'username': x})
            if userinfo:
                return render_template('index.html', x + "exists")
        except Exception as e:
            print(e)

    def addUser(chkuser, password, pin):
        try:
            db = dataBase.getdb()
            coll = db["Userbase"]
            data = ({'username': chkuser,
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
