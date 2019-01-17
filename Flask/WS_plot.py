import io
import pandas as pd
import os
import cx_Oracle
from flask import Response, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib as plt;
from flask import Flask

oh="D:/tools/Oracle/instantclient_12_2_x8664"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"


def connectToOracle(url, username, password, mode=None):
    if mode is not None:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url, mode=mode)
    else:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url)
    return connection

def executeStmt(conn, stmt):
    if conn is not None and isinstance (conn, cx_Oracle.Connection):
        cur = conn.cursor()
        cur.execute(stmt)
    return cur


## FLASK PART
app = Flask (__name__)
@app.route("/plot.png")
def plot_png():

    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():

    c = cx_Oracle.Connection;
    try:
        c = connectToOracle ("lnvfr99720427.fr.auchan.com:1521/ACCESS_DQMDM.FR.AUCHAN.COM", "datacentric_monitor",
                             "datacentric_monitor")
        df = pd.read_sql_query ("select t.analysis_date, t.tablespace_name, \
                                    t.size_go, t.free_space_go, t.maxsize_go, \
                                    t.MAXSIZE_GO-t.SIZE_GO+t.FREE_SPACE_GO usable_GO \
                                    from datacentric_monitor.tbs_monitor t \
                                    where tablespace_name ='ICRFR2_DATA' \
                                    order by 1", c)
    except cx_Oracle.DatabaseError as dberror:
        print dberror

    fig = plt.figure.Figure()
    #xs = range(100)
    ax0=fig.add_subplot(1,1,1)
    xs = df["ANALYSIS_DATE"]
    ax0.plot(xs,df["USABLE_GO"])
    ax0.plot(xs,df["SIZE_GO"])
    ax0.plot(xs,df["MAXSIZE_GO"])
    ax0.legend(loc=0)
    return fig

@app.route("/")
def root():
    return render_template('test.html')

if __name__ == '__main__':
   app.run(host="DESKTOP_2105", port=80, debug = True)