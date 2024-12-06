import streamlit as st
from time import time
from time import sleep
import pandas as pd

from spark_dash.utils import *
from tz_kst import now


def list2df():
    l = docker_stats()
    l = list(filter(lambda x:"spark" in x["Name"],l))
    df = pd.DataFrame(l)

    df.set_index("Name", inplace=True)
    df=df[["CPUPerc","MemUsage","MemPerc"]]

    return df


t=time()

st.title("Spark Resource Usage")

row1 = st.empty()
row2 = st.empty()
row3 = st.empty()
l,r = row3.columns([4.5,1])
row4 = st.empty()


if l.button("scale in"):
    do_scale("in",get_worker_cnt())
    line_notify(f"worker의 수를 {get_worker_cnt()}개로 scale in하였습니다.")
    st.session_state["lowTime"]=0
    st.rerun()
if r.button("scale out"):
    do_scale("out",get_worker_cnt())
    print(line_notify(f"worker의 수를 {get_worker_cnt()}개로 scale out하였습니다."))
    st.session_state["highTime"]=0
    st.rerun()



#highTime,lowTime=0,0
if "highTime" not in st.session_state:
    st.session_state["highTime"]=0
if "lowTime" not in st.session_state:
    st.session_state["lowTime"]=0



#while 1:
def cronjob():
    #if (t+10)//10 == time()//10:
    #t=time()
    cpu_use=max(map(lambda x:float(x.replace("%","")),get_worker().values()))

    #row1.table(list2df()[["Name","CPUPerc","MemUsage","MemPerc"]])
    row1.table(list2df())

    if cpu_use > get_max_cpu_use():
        st.session_state["highTime"]+=10
    else:
        st.session_state["highTime"]=0

    if (get_worker_cnt() > 1) and (cpu_use < get_min_cpu_use()):
        st.session_state["lowTime"]+=10
    else:
        st.session_state["lowTime"]=0

    save_log("usage", f"{cpu_use},{get_worker_cnt()},{now()},{'high' if st.session_state['highTime']>0 else 'low' if st.session_state['lowTime']>0 else 'stable'}")

    if  st.session_state["highTime"]==60:
        do_scale("out",get_worker_cnt())
        print(line_notify(f"worker의 수를 {get_worker_cnt()}개로 scale out하였습니다."))
        st.session_state["highTime"]=0
        st.rerun()
    elif st.session_state["lowTime"]==60:
        do_scale("in",get_worker_cnt())
        line_notify(f"worker의 수를 {get_worker_cnt()}개로 scale in하였습니다.")
        st.session_state["lowTime"]=0
        st.rerun()

    #row2.progress(int(time()-t)*10)
    row2.progress(max(st.session_state["lowTime"],st.session_state["highTime"])*100//60, text=f"Scale {'in' if st.session_state['lowTime']>0 else 'out' } 진행률")
    #sleep(10)


#########################################################################
import schedule


# 스케줄 설정
schedule.every(10).seconds.do(cronjob)

cronjob()
while True:
    schedule.run_pending()
    sleep(3)
#########################################################################