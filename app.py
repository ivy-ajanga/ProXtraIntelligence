import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Pro Xtra Dashboard")

# Load data
df = pd.read_csv('data/proxtra_advanced_customers_data.csv', parse_dates=['last_purchase_date'])

# Feature engineering
df['purchase_quarter'] = df['last_purchase_date'].dt.to_period('Q').astype(str)

st.title("🔨 Retail Pro Xtra Customer Insights Dashboard")

# Filters
st.sidebar.header("🔍 Filter Data")
tiers = st.sidebar.multiselect("Select Tier(s):", df['tier_status'].unique(), default=df['tier_status'].unique())
df_filtered = df[df['tier_status'].isin(tiers)]

# Grouped Data
grouped = df_filtered.groupby(['purchase_quarter', 'tier_status'])['total_spent'].mean().reset_index()
pivot = grouped.pivot(index='purchase_quarter', columns='tier_status', values='total_spent')

# Chart: Average Spend by Tier per Quarter
st.subheader("📊 Average Total Spend by Tier per Quarter")
st.bar_chart(pivot)

# Line chart for loyalty trends (optional)
loyalty = df_filtered.groupby(['purchase_quarter', 'tier_status'])['loyalty_spend'].mean().reset_index()
pivot_loyalty = loyalty.pivot(index='purchase_quarter', columns='tier_status', values='loyalty_spend')

st.subheader("📈 Average Loyalty Spend by Tier per Quarter")
st.line_chart(pivot_loyalty)

# Data Table
#st.subheader("🧾 Filtered Data Table")
#st.dataframe(df_filtered)


