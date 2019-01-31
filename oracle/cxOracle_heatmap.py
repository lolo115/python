import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import cx_Oracle as cx
import sys
import os

platform=sys.platform
if platform=='darwin':
    root_dir = '/Users/leturgezl/PycharmProjects/work'
    oh="/Users/leturgezl/Applications/instantclient_12_2"


if platform.startswith('win'):
    root_dir = 'D:/JetBrains_projects/PycharmProjects/work'
    oh='D:/tools/Oracle/instantclient_12_2_x8664'

os.chdir (root_dir)
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

def connectToOracle(url, username, password, mode=None):
    if mode is not None:
        connection = cx.Connection (user=username, password=password, dsn=url, mode=mode)
    else:
        connection = cx.Connection (user=username, password=password, dsn=url)
    return connection

def executeStmt(conn, stmt):
    if conn is not None and isinstance (conn, cx.Connection):
        cur = conn.cursor()
        cur.execute(stmt)
    return cur

if __name__ == '__main__':
    c=cx.Connection
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
        c=connectToOracle("192.168.99.3:1521/orcl","sys","oracle",mode=cx.SYSDBA)
        df=pd.read_sql_query(qry, c)

    except cx.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        os._exit(1)
    finally:
        c.close()

    # DataFrame processing

    # Getting first column
    df_date = df['MTIME']

    # Getting dataframe data after dropping MTIME column and values in numpy format
    df_data = df.drop('MTIME', axis=1)
    np_data=df_data.values

    # Getting column labels
    np_column_name = np.asarray(list(df_data))

    fig, ax = plt.subplots()
    colormap = cm.jet
    im=ax.imshow(np_data, cmap=colormap, vmin=0., vmax=2)

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
    plt.setp(ax.get_xticklabels(), rotation=55, ha="right",rotation_mode="anchor")

    # Grid creation
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(np_data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(np_data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    fig.tight_layout()
    plt.show()