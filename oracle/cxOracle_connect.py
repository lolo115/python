from __future__ import print_function

import cx_Oracle
import os

oh="D:/tools/Oracle/instantclient_12_2_x8664"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

def printConnectionAttr(connection):
    if connection is not None and isinstance(connection,cx_Oracle.Connection):
        print("Data Source Name  = ",connection.dsn)
        a="true" if connection.autocommit==1 else "False"
        print("Autocommit         = ",a)
        print("Session Edition    = ",connection.edition)
        print("Encoding           = ",connection.encoding)
        print("National Encoding  = ",connection.nencoding)
        print("Logical Tx Id      = ",connection.ltxid)
        print("Server version     = ",connection.version)

def connectToOracle(url, username, password, mode=None):
    if mode is not None:
       connection = cx_Oracle.Connection (user=username, password=password, dsn=url, mode=mode)
    else:
       connection = cx_Oracle.Connection (user=username, password=password, dsn=url)
    
    return connection

# main
if __name__ == '__main__':
    c=cx_Oracle.Connection
    try:
        c=connectToOracle("192.168.99.2:1521/orcl","sys","oracle",mode=cx_Oracle.SYSDBA)
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        os._exit(1)

    printConnectionAttr(c)
    c.close()
