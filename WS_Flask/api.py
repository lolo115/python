from flask import Flask, render_template
from flask_restful import Resource, Api
import socket
import os
import pandas as pd
import cx_Oracle as cx

oh="/Users/leturgezl/Applications/instantclient_12_2"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

def connectToOracle(url, username, password, mode=None):
    if mode is not None:
       connection = cx.Connection (user=username,password=password,dsn=url,mode=mode)
    else:
       connection = cx.Connection (user=username,password=password,dsn=url)
    return connection


app = Flask (__name__)
api=Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'Hello':'World'}

class OracleParams(Resource):

    c = cx.Connection
    def __init__(self):
        try:
            OracleParams.c=connectToOracle(url="192.168.99.3:1521/orcl",
                                           username="sys",
                                           password="oracle",
                                           mode=cx.SYSDBA)
        except cx.DatabaseError as ex:
            err, =ex.args
            print("Error code    = ",err.code)
            print("Error Message = ",err.message)
    def __exit__(self):
        try:
            OracleParams.c.close()
        except cx.DatabaseError as ex:
            err, =ex.args
            print("Error code    = ",err.code)
            print("Error Message = ",err.message)

    def get(self):
        df_name = pd.read_sql("select name from v$database", con=OracleParams.c)
        return df_name.to_json()

    def post(self):
        dataframe = pd.read_sql("select name,value from v$parameter order by name", con=OracleParams.c)
        return dataframe.to_json()

api.add_resource(HelloWorld, '/')
api.add_resource(OracleParams,'/oracle/')

if __name__ == "__main__":
    app.run (host=socket.gethostname(), port=5002, debug=True)