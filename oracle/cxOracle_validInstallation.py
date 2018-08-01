from __future__ import print_function

import cx_Oracle
import os

oh="D:/tools/Oracle/instantclient_12_2_x8664"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]

print("Running tests for cx_Oracle version", cx_Oracle.version,"built at", cx_Oracle.buildtime)
print("File:", cx_Oracle.__file__)
print("Client Version:", ".".join(str(i) for i in cx_Oracle.clientversion()))
