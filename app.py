import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/sales_data.csv", parse_dates=["date"])

df = load_data()

st.title("📊 Sales Performance Analytics Dashboard")

# Filters
st.sidebar.header("Filters")
region_filter = st.sidebar.multiselect("Select Region", df["region"].unique())
category_filter = st.sidebar.multiselect("Select Category", df["category"].unique())

filtered_df = df.copy()

if region_filter:
    filtered_df = filtered_df[filtered_df["region"].isin(region_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

# KPIs
total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units_sold"].sum()
avg_price = filtered_df["unit_price"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Avg Unit Price", f"₹{avg_price:,.2f}")

# Revenue Trend
st.subheader("Revenue Trend Over Time")
rev_trend = filtered_df.groupby("date")["revenue"].sum()

fig1, ax1 = plt.subplots()
rev_trend.plot(ax=ax1)
ax1.set_xlabel("Date")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# Region Performance
st.subheader("Region-wise Revenue")
region_rev = filtered_df.groupby("region")["revenue"].sum()

fig2, ax2 = plt.subplots()
region_rev.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Revenue")
st.pyplot(fig2)

# Category Performance
st.subheader("Category-wise Units Sold")
cat_units = filtered_df.groupby("category")["units_sold"].sum()

fig3, ax3 = plt.subplots()
cat_units.plot(kind="bar", color="orange", ax=ax3)
ax3.set_ylabel("Units Sold")
st.pyplot(fig3)

st.write("Data Preview")
st.dataframe(filtered_df)
