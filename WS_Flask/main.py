import matplotlib as mpl
mpl.use("TkAgg")
from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
import socket
import os
import io
import pandas as pd
import cx_Oracle as cx

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


app = Flask (__name__)
@app.route ("/")
def index():
    return "Hello U"

@app.route ("/members/<string:name>/")
def getMember(name):
    return name

@app.route('/hello/<user>/')
def hello_name(user):
   return render_template('HelloWorld.html', name=user)

@app.route('/oracle/')
def connOracle():

    c=cx.Connection
    try:
        c=connectToOracle(url="192.168.99.3:1521/orcl",
                          username="sys",
                          password="oracle",
                          mode=cx.SYSDBA)
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
    else:
        dataframe = pd.read_sql("select name,value from v$parameter order by name", con=c)
        df_name = pd.read_sql("select name from v$database", con=c)
    finally:
        c.close()
    return render_template('OracleSimpleRenderer.html', result=dataframe, name=df_name.iloc[0]["NAME"])

@app.route("/storage/plot.png")
def plot_png():

    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():

    c = cx.Connection;
    qry="""
        SELECT ts.tablespace_name, NVL(ROUND("SIZEMB" - "FREEMB", 2),0) "USEDMB",
        NVL(ROUND("FREEMB",2),0) "FREEMB"
        FROM ( SELECT tablespace_name, SUM(bytes) / (1024 * 1024) "FREEMB" FROM dba_free_space GROUP BY tablespace_name) fr,
             ( SELECT tablespace_name, SUM(bytes) / (1024 * 1024) "SIZEMB", COUNT(*) "File Count",
               SUM(maxbytes) / (1024 * 1024) "MAX_EXT" FROM dba_data_files GROUP BY tablespace_name) df,
             ( SELECT tablespace_name,EXTENT_MANAGEMENT,ALLOCATION_TYPE,SEGMENT_SPACE_MANAGEMENT FROM dba_tablespaces) ts
        WHERE fr.tablespace_name (+) = df.tablespace_name
        AND df.tablespace_name = ts.tablespace_name
        order by 1
    """
    try:
        c = connectToOracle ("192.168.99.3:1521/orcl", "system", "oracle")
        df = pd.read_sql_query (qry, c)
    except cx.DatabaseError as dberror:
        print(dberror)
    finally:
        c.close()

    fig, ax = plt.subplots()
    cmap = mpl.colors.ListedColormap(["red", "blue"])
    ax = df.plot.bar(stacked=True, xticks=df.index, ax=ax, colormap=cmap)
    ax.set_xticklabels(df.TABLESPACE_NAME, rotation=0, fontsize=8)

    return fig

@app.route("/storage/")
def storage_display():
    return render_template('storageRenderer.html')

if __name__ == "__main__":
    app.run (host=socket.gethostname(), port=5001, debug=True)