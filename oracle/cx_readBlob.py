import os
import cx_Oracle
import sys
import numpy as np
from PIL import Image
from io import BytesIO

if sys.platform=='darwin':
    root_dir = '/Users/leturgezl/PycharmProjects/work'
    os.chdir (root_dir)
    oh="/Users/leturgezl/Applications/instantclient_12_2"

os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"


if __name__ == '__main__':
    c = cx_Oracle.Connection
    try:

        c = cx_Oracle.Connection (user="laurent", password="laurent", dsn="192.168.99.3:1521/orcl")

        cur = c.cursor()
        cur.execute('select b,status from bin_file where rownum=1')
        r=cur.fetchall()

        c1 = [row[0] for row in r][0]
        print("type(c1)=", type(c1))
        c2 = [row[1] for row in r][0]
        print("c2=", c2)


        s=c1.read()
        im=Image.open(BytesIO(s))
        imgsize=32,32
        im.thumbnail(imgsize)
        A=np.array(im,dtype=np.float32)
        print("A=",A)

        cur.close()
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        c.close()
    c.close()