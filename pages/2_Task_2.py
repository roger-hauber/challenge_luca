import sqlite3
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Data Challenge Dashboard", layout="wide")

# Set up db connection
@st.cache
def connect_db():
    conn = sqlite3.connect("data/challenge_db.db", check_same_thread=False)
    return conn

conn = connect_db()




### TASK TWO

#top 123 cities of Germany from de.csv
big_cities = pd.read_csv("data/de.csv")


transactions_per_city = pd.read_sql("""
SELECT COUNT(totalAmount) AS num_trans, city
FROM payments JOIN locations ON payments.locationId = locations.uuid
WHERE NOT payments.status = "ERR"
GROUP BY city
""", con = conn)

trans_big_cities = transactions_per_city[transactions_per_city.city.isin(big_cities.city)]
trans_big_cities = trans_big_cities.merge(big_cities, on = "city")

fig = px.scatter_geo(trans_big_cities, lat='lat', lon='lng',
                     hover_name="city", hover_data = {"lat": False, "lng": False, "num_trans": True}, size="num_trans",
                     scope="europe", title='Number of transactions by (big) city',
                    center=dict(lat=51.0057, lon=13.7274)
                )

fig = fig.update_layout(
    autosize=True,
    height=600,
    geo=dict(
        center=dict(
            lat=51.0057,
            lon=13.7274
        ),
        scope='europe',
        projection_scale=6
    )
)
#set up two columns for plots
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Second task")

    st.write(fig)
