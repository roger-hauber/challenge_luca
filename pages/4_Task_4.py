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




### TASK Four
sales_by_hour = pd.read_sql("""
SELECT AVG(totalAmount) AS average,
SUM(totalAmount) AS total,
city,
strftime("%H", paymentCreatedAt) AS hour
FROM payments JOIN locations ON payments.locationId=locations.uuid
WHERE NOT payments.status = "ERR"
GROUP BY city, hour
""", con = conn)

def by_hour(city):
    plt = sns.barplot(y = sales_by_hour.loc[sales_by_hour.city == city, "total"],
                x = sales_by_hour.loc[sales_by_hour.city == city, "hour"])
    plt.set_title(f"Sales per hour in {city}\n", fontdict={"size": 18, "weight":"bold"})
    return plt

# set up multiselect for val and time
choices = ["Potsdam", "Kiel", "Karlsruhe", "Hamburg", "Berlin"]
with st.sidebar:
    city = st.selectbox("City to display", choices)





#set up two columns for plots
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Third task")
    plt.figure(figsize=(10,8))
    fig = by_hour(city=city)

    st.pyplot(fig.figure)
