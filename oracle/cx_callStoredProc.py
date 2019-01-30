from __future__ import print_function

import cx_Oracle
import os
import numpy as np
import pandas as pd

# REFERENCE : https://www.oracle.com/technetwork/articles/prez-stored-proc-084100.html

oh="/Users/leturgezl/Applications/instantclient_12_2"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

def connectToOracle(url, username, password, mode=None):
    if mode is not None:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url, mode=mode)
    else:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url)
    return connection

def executeStmt(conn, stmt, parameters):
    if conn is not None and isinstance (conn, cx_Oracle.Connection):
        cur = conn.cursor()
        if parameters is None:
            cur.execute (stmt)
        else:
            cur.execute(stmt,parameters)
    return cur

def printCursor(cur):
    if cur is not None and isinstance(cur, cx_Oracle.Cursor):
        for row in cur.fetchall():
            print(row)

# main
if __name__ == '__main__':
    c=cx_Oracle.Connection
    stmt="select avg(salary) from emp"
    try:
        c=connectToOracle("192.168.99.3:1521/orcl","laurent","laurent")
        curs=executeStmt(c,stmt,parameters=None); print('Before : '); printCursor(curs)
        curs=c.cursor();
        # CREATE OR REPLACE PROCEDURE GENERAL_SAL_INCREASE (pct in number default 0)
        curs.callproc("GENERAL_SAL_INCREASE",[0])
        curs = executeStmt (c, stmt, parameters=None); print ('After : '); printCursor (curs)

        curs = executeStmt (c, stmt, parameters=None); print ('Before : '); printCursor (curs)
        curs = c.cursor ();
        avgsal = curs.var(cx_Oracle.NUMBER)

        # CREATE OR REPLACE PROCEDURE GENERAL_SAL_INCREASE_OUT (pct in number default 0, avg_sal out number) is
        curs.callproc ("GENERAL_SAL_INCREASE_OUT", [ 5, avgsal ])
        curs = executeStmt (c, stmt, parameters=None); print ('After : '); printCursor (curs), print('avgsal = ',avgsal.getvalue(pos=0))

        curs = c.cursor ();
        # CREATE OR REPLACE EDITIONABLE FUNCTION "LAURENT"."GET_SAL" (fname in varchar2, lname in varchar2) return number
        janette_king_sal = curs.callfunc("GET_SAL",cx_Oracle.NUMBER, ["Janette","King"]);
        print("janette king sal", janette_king_sal)

        curs.close()
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        os._exit(1)
    c.close()
