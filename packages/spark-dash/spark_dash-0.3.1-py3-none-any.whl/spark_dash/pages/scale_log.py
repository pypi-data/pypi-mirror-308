import streamlit as st
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

from spark_dash.utils import get_log_path

log_path = f"{get_log_path()}/scale"
log_list = list(map(lambda x:x.replace(log_path+"/",""),glob(f"{log_path}/*.log")))

st.title("Scale Log Dashboard")

option = st.selectbox(
    "Select logfile",
    log_list,
)

st.markdown("### Scale Log DataFrame")
df = pd.read_csv(f"{log_path}/{option}")
df

st.markdown(f"### \# of Worker Plot")

scale_cnt=df["cnt_after"].to_list()
scale_cnt.insert(0,int(df["cnt_before"][0]))

time_list=df["time"].to_list()
time_list.insert(0,df["time"][0])

fig, ax  = plt.subplots()
ax.set_ylabel("# of Worker")
ax.plot(time_list,scale_cnt)
plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

st.pyplot(fig)

st.markdown("### Scale I/O Plot")
method_cnt = df.value_counts(df["method"])

fig, ax  = plt.subplots()
ax.set_xlabel("I/O")
ax.set_ylabel("Counts")

ax.bar(method_cnt.index, method_cnt.values)

st.pyplot(fig)