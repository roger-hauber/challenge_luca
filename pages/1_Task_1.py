import sqlite3
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Data Challenge Dashboard", layout="wide")

# Set up db connection
@st.cache
def connect_db():
    conn = sqlite3.connect("data/challenge_db.db", check_same_thread=False)
    return conn

conn = connect_db()




### TASK ONE

# set up multiselect for val and time
with st.sidebar:
    val = st.selectbox("Value to display", ["total", "average"])
    time = st.selectbox("Timeframe to display", ["week", "month"])

def task_one(val, time):
    if val == "total":
        func = "SUM"
    elif val == "average":
        func = "AVG"
    if time == "week":
        dt_format = "%W"
        col_name = "week"
    elif time == "month":
        dt_format = "%m"
        col_name = "month"

    df = pd.read_sql(f"""SELECT {func}(totalAmount) AS '{val}', \
    strftime('{dt_format}', payments.paymentCreatedAt) AS {col_name} \
FROM payments \
WHERE NOT payments.status = 'ERR'\
GROUP BY {col_name}""", con = conn)
    b_plot = sns.barplot(y = df[val], x = df[time])
    b_plot.set_title(f"Payment {val} by {time}\n", fontdict={"size": 16, "weight": "bold"})
    if time == "month":
        b_plot.set_xticks(range(df[time].nunique()), labels=["April", "May", "June", "July"])
    return b_plot

#set up two columns for plots
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First task")
    fig = task_one(val=val, time=time)

    st.pyplot(fig.figure)
