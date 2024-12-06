import streamlit as st
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

from spark_dash.utils import get_log_path

log_path = f"{get_log_path()}/usage"
log_list = list(map(lambda x:x.replace(log_path+"/",""),glob(f"{log_path}/*.log")))

st.title("Usage Log Dashboard")

option = st.selectbox(
    "Select logfile",
    log_list,
)

st.markdown("### Usage Log DataFrame")
df = pd.read_csv(f"{log_path}/{option}")
df

st.markdown("### Usage Log Plot")
fig, ax  = plt.subplots()
ax.set_ylabel("CPU Usage(%)")
ax.plot(df.index,df["cpu_use"])

st.pyplot(fig)

st.markdown("### Usage Status Plot")
status_cnt = df.value_counts(df["status"])

fig, ax  = plt.subplots()
ax.set_xlabel("Status")
ax.set_ylabel("Counts")

ax.bar(status_cnt.index, status_cnt.values)

st.pyplot(fig)