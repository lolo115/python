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
if sys.platform.startswith('win'):
    root_dir = 'D:\JetBrains_projects\PycharmProjects\work'
    os.chdir (root_dir)
    oh="D:/tools/Oracle/instantclient_12_2_x8664"

os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"


if __name__ == '__main__':
    c = cx_Oracle.Connection
    try:

        c = cx_Oracle.Connection (user="laurent", password="laurent", dsn="192.168.99.3:1521/orcl")

        cur = c.cursor()
        cur.execute('select b from bin_file where status=999') # BigOne (Share must be (x,y,4 if in color)
        #cur.execute('select b from bin_file where status=1 and rownum=1')  # BigOne (Share must be (x,y,1) if in gray)

        c1=cur.fetchone()[0]

        #c1 = [row[0] for row in r][0]
        print("type(c1)=", type(c1))

        #c2 = [row[1] for row in r][0]
        #print("c2=", c2)


        s=c1.read()
        im=Image.open(BytesIO(s))
        #imgsize=8,8
        #im.thumbnail(imgsize)
        im.show()
        A=np.array(im,dtype=np.float32)
        print("A=",A)
        print("A.shape = ",A.shape)
        cur.close()
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
    finally:
        c.close()