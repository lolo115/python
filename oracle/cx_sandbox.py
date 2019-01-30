import cx_Oracle as cx
import os
import pandas as pd
import numpy as np

oh="/Users/leturgezl/Applications/instantclient_12_2"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"


def connectToOracle(url, username, password, mode=None):
    if mode is not None:
       connection = cx.Connection (user=username,
                                   password=password,
                                   dsn=url,
                                   mode=mode)
    else:
       connection = cx.Connection (user=username,
                                   password=password,
                                   dsn=url)
    return connection

# main
if __name__ == '__main__':
    df = pd.DataFrame(np.random.randn(6, 4),index=list('abcdef'),columns=list('ABCD'))
    print(df)

    print(type(df['B'].values))
    print(df.values)
    print(df['B'].values)



    exit(0)
    c=cx.Connection
    try:
        c=connectToOracle(url="192.168.99.3:1521/orcl",
                          username="sys",
                          password="oracle",
                          mode=cx.SYSDBA)
    except cx.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        os._exit(1)
    else:
        print("Data Source Name  = ", c.dsn)
        a = "true" if c.autocommit == 1 else "False"
        print("Autocommit         = ", a)
        print("Session Edition    = ", c.edition)
        print("Encoding           = ", c.encoding)
        print("National Encoding  = ", c.nencoding)
        print("Logical Tx Id      = ", c.ltxid)
        print("Server version     = ", c.version)
    finally:
        c.close()
