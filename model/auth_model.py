import mysql.connector
import json
from flask import make_response, request
from datetime import datetime
from datetime import timedelta
import jwt
import re
from config.config import dbconfig
from functools import wraps


class auth_model ():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('Connection Succesfull')
        except:
            print('Connection Failed')


#the func is the function below the decorator
    def token_auth(self, endpoint = ""):
        def inner1(func):
            @wraps(func)                                                                                                                    
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization = request.headers.get("authorization")
                # if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                if re.match("Bearer ", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token, "mohit", algorithms="HS256")
                    except:
                        return make_response({"Error" : "Token Expired"})
                    role_id = jwtdecoded['payload']['role_id']
                    print(role_id)
                    self.cur.execute(f"SELECT roles FROM accessbility_view WHERE endpoint = '{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        allowed_roles = json.loads(result[0]['roles'])
                        print(allowed_roles)
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"Error" : "Invalid Role"}, 403)
                    else:
                        return make_response({"Error" : "Unknown Endpoint"}, 404)

                else:
                    return make_response({"Error": "Invalid Token"}, 401)
            return inner2
        return inner1 