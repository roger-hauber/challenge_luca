import sqlite3
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Challenge Dashboard", layout="wide")

# Set up db connection
@st.cache
def connect_db():
    conn = sqlite3.connect("data/challenge_db.db", check_same_thread=False)
    return conn

conn = connect_db()




### TASK Three
rank_two = pd.read_sql("""
WITH incl_rank AS (SELECT SUM(totalAmount) as total, AVG(totalAmount) as average, MAX(totalAmount), locationId, city,
RANK() OVER (
PARTITION BY city
ORDER BY city ASC, MAX(totalAmount) DESC
) AS order_rank

FROM payments JOIN locations ON payments.locationId=locations.uuid
WHERE NOT payments.status = "ERR"
GROUP BY city, locationId
ORDER BY city ASC, MAX(totalAmount) DESC)

SELECT *
FROM incl_rank
WHERE order_rank = 2
""", con = conn)

# set up multiselect for val and time
with st.sidebar:
    city = st.selectbox("City to display", rank_two.city.values)


def plot_spec_city(city):
    plt = sns.barplot(y = pd.Series([rank_two.loc[rank_two.city == city,"average"].values[0],
                                     rank_two.loc[rank_two.city == city,"total"].values[0]],
                              index= [0, 1]),
                x = pd.Series(["average", "total"]))
    plt.set_title(f"Average + total of location w/ second largest single payment in {city}\n",
                  fontdict={"size": 16, "va":"top", "weight": "bold"})

    plt.bar_label(plt.containers[0])
    return plt

#set up two columns for plots
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Third task")
    plt.figure(figsize=(10,8))
    fig = plot_spec_city(city=city)

    st.pyplot(fig.figure)
