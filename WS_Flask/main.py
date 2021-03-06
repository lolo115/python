import matplotlib as mpl
mpl.use("TkAgg")
from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
from matplotlib import cm
import socket
import os
import io
import pandas as pd
import numpy as np
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

@app.route("/storage/bar_plot.png")
def plot_storage_bar_png():

    fig = create_storage_figure_bar()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_storage_figure_bar():

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
        c = connectToOracle("192.168.99.3:1521/orcl", "system", "oracle")
        df = pd.read_sql_query (qry, c)
    except cx.DatabaseError as dberror:
        print(dberror)
    finally:
        c.close()

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 7)
    cmap = mpl.colors.ListedColormap(["red", "darkblue"])
    ax = df.plot.bar(stacked=True, xticks=df.index, ax=ax, colormap=cmap)
    ax.set_xticklabels(df.TABLESPACE_NAME, rotation=0, fontsize=8)
    ax.get_xaxis().set_label_text(label="Tablespaces")
    ax.get_yaxis().set_label_text(label="MBytes")

    return fig

@app.route("/storage/")
def storage_display():
    return render_template('storageRenderer.html')

# HEATMAP

@app.route("/heatmap/hm.png")
def plot_heatmap_png():

    fig = create_perf_figure_HM()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_perf_figure_HM():
    c = cx.Connection;
    qry="""
        with t as (
        select to_char(mtime,'YYYY/MM/DD') mtime, to_char(mtime,'HH24') d, LOAD as value from (
            select to_date(mtime,'YYYY-MM-DD HH24') mtime,
            round(sum(c1),2) AAS_WAIT,
            round(sum(c2),2) AAS_CPU,
            round(sum(cnt),2) AAS,
            round(sum(load),2) LOAD
            from (
                 select to_char(sample_time,'YYYY-MM-DD HH24') mtime,
                        decode(session_state,'WAITING',count(*),0)/360 c1,
                        decode(session_state,'ON CPU',count(*),0) /360 c2,
                        count(*)/360 cnt,
                        count(*)/360/nvl(cpu.core_nb,1) load
                 from dba_hist_active_sess_history, (select value as core_nb from v$osstat where stat_name='NUM_CPU_CORES') cpu
                 where sample_time > sysdate - 30
                 group by to_char(sample_time,'YYYY-MM-DD HH24'),session_state, cpu.core_nb
                 )
            group by mtime
            )
        )
        select mtime,
           nvl("00-01_ ",0) "00-01_ ",nvl("01-02_ ",0) "01-02_ ",nvl("02-03_ ",0) "02-03_ ",nvl("03-04_ ",0) "03-04_ ",nvl("04-05_ ",0) "04-05_ ",
           nvl("05-06_ ",0) "05-06_ ",nvl("06-07_ ",0) "06-07_ ",nvl("07-08_ ",0) "07-08_ ",nvl("08-09_ ",0) "08-09_ ",nvl("09-10_ ",0) "09-10_ ",
           nvl("10-11_ ",0) "10-11_ ",nvl("11-12_ ",0) "11-12_ ",nvl("12-13_ ",0) "12-13_ ",nvl("13-14_ ",0) "13-14_ ",nvl("14-15_ ",0) "14-15_ ",
           nvl("15-16_ ",0) "15-16_ ",nvl("16-17_ ",0) "16-17_ ",nvl("17-18_ ",0) "17-18_ ",nvl("18-19_ ",0) "18-19_ ",nvl("19-20_ ",0) "19-20_ ",
           nvl("20-21_ ",0) "20-21_ ",nvl("21-22_ ",0) "21-22_ ",nvl("22-23_ ",0) "22-23_ ",nvl("23-24_ ",0) "23-24_ "
        from t
        pivot(
          sum(value) as " " for d in ('00' AS "00-01",'01' AS "01-02",'02' AS "02-03",'03' AS "03-04",'04' AS "04-05",'05' AS "05-06",'06' AS "06-07",'07' AS "07-08",'08' AS "08-09",'09' AS "09-10",'10' AS "10-11",
                                    '11' AS "11-12",'12' AS "12-13",'13' AS "13-14",'14' AS "14-15",'15' AS "15-16",'16' AS "16-17",'17' AS "17-18",'18' AS "18-19",'19' AS "19-20",'20' AS "20-21",'21' AS "21-22",
                                    '22' AS "22-23",'23' AS "23-24")
        )
        order by mtime
    """

    try:
        c = connectToOracle("192.168.99.3:1521/orcl", "system", "oracle")
        df = pd.read_sql_query (qry, c)
    except cx.DatabaseError as dberror:
        print(dberror)
    finally:
        c.close()

    # Getting first column
    df_date = df['MTIME']

    # Getting dataframe data after dropping MTIME column and values in numpy format
    df_data = df.drop('MTIME', axis=1)
    np_data = df_data.values

    # Getting column labels
    np_column_name = np.asarray(list(df_data))

    fig, ax = plt.subplots()
    fig.set_size_inches(10,7)
    colormap = cm.jet
    im = ax.imshow(np_data, cmap=colormap, vmin=0., vmax=2)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, cmap=colormap)
    cbar.ax.set_ylabel("DataBase Load", rotation=-90, va="bottom")

    # We want to show all ticks
    ax.set_xticks(np.arange(len(np_column_name)))
    ax.set_yticks(np.arange(len(df_date.values)))
    # We set ticks labels
    ax.set_xticklabels(np_column_name)
    ax.set_yticklabels(df_date.values)
    # Rotate tick labels and set their alignments
    plt.setp(ax.get_xticklabels(), rotation=55, ha="right", rotation_mode="anchor")

    # Grid creation
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(np_data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(np_data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    fig.tight_layout()
    return fig

@app.route("/heatmap/")
def heatmap_display():
    return render_template('heatmapRenderer.html')

if __name__ == "__main__":
    app.run (host=socket.gethostname(), port=5001, debug=True)