import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="Pro Xtra Analytics Dashboard")

# Load data
df = pd.read_csv('data/proxtra_advanced_customers_data.csv', parse_dates=['signup_date', 'last_purchase_date'])

# Feature engineering
df['purchase_quarter'] = df['last_purchase_date'].dt.to_period('Q').astype(str)
df['days_since_last_purchase'] = (pd.Timestamp.today() - df['last_purchase_date']).dt.days

# Simple churn risk definition
df['churn_risk'] = np.where((df['days_since_last_purchase'] > 180) | (df['visits'] < 10), 'High', 'Low')

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
tiers = st.sidebar.multiselect("Select Tier(s):", sorted(df['tier_status'].unique()), default=sorted(df['tier_status'].unique()))
churn_levels = st.sidebar.multiselect("Select Churn Risk:", sorted(df['churn_risk'].unique()), default=sorted(df['churn_risk'].unique()))

df_filtered = df[(df['tier_status'].isin(tiers)) & (df['churn_risk'].isin(churn_levels))]

# --- 1. Descriptive Analytics ---
st.title("🔨 Pro Xtra Customer Insights Dashboard")
st.header("1. 📊 Descriptive Analytics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Customers", f"{len(df_filtered):,}")
kpi2.metric("Avg Total Spend", f"${df_filtered['total_spent'].mean():,.0f}")
kpi3.metric("Avg Visits", f"{df_filtered['visits'].mean():.1f}")
kpi4.metric("Avg Basket Size", f"${df_filtered['avg_basket_size'].mean():.2f}")

st.subheader("Average Total Spend by Tier and Quarter")
spend_by_quarter = df_filtered.groupby(['purchase_quarter', 'tier_status'])['total_spent'].mean().reset_index()
pivot_spend = spend_by_quarter.pivot(index='purchase_quarter', columns='tier_status', values='total_spent')
st.bar_chart(pivot_spend)

# --- 2. Diagnostic Analytics ---
st.header("2. 🧪 Diagnostic Analytics")
st.subheader("Correlation Heatmap of Key Metrics")

corr_cols = ['total_spent', 'visits', 'avg_basket_size', 'loyalty_spend', 'pro_desk_visits', 'credit_card_usage', 'age']
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df_filtered[corr_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.subheader("Trade Type vs. Average Spend")
trade_spend = df_filtered.groupby('trade_type')['total_spent'].mean().sort_values(ascending=False)
st.bar_chart(trade_spend)

# --- 3. Predictive Analytics ---
st.header("3. 🤖 Predictive Analytics")
st.subheader("Churn Risk by Tier")
churn_by_tier = df_filtered.groupby(['tier_status', 'churn_risk']).size().unstack().fillna(0)
st.bar_chart(churn_by_tier)

st.subheader("🚨 High-Risk Customers")
high_risk_df = df_filtered[df_filtered['churn_risk'] == 'High']
st.dataframe(high_risk_df[[
    'customer_id', 'last_purchase_date', 'visits', 'total_spent', 'tier_status', 'churn_risk'
]].sort_values(by='last_purchase_date'))

st.subheader("🚀 Upgrade Tier Candidates")

# Define upgrade thresholds
spend_threshold = 15000
visit_threshold = 30

upgrade_candidates = df_filtered[
    (df_filtered['tier_status'] != 'VIP') &
    (
        (df_filtered['total_spent'] >= spend_threshold) |
        (df_filtered['visits'] >= visit_threshold)
    )
]

st.dataframe(upgrade_candidates[[
    'customer_id', 'tier_status', 'total_spent', 'visits'
]].sort_values(by='total_spent', ascending=False))

# --- 4. Prescriptive Analytics ---
st.header("4. 🧠 Prescriptive Analytics")
st.subheader("Target Campaign Suggestions")

low_loyalty = df_filtered[(df_filtered['loyalty_spend'] < 500) & (df_filtered['visits'] > 10)]
near_upgrade = df_filtered[(df_filtered['tier_status'] != 'VIP') & (df_filtered['total_spent'] > 18000)]

st.markdown("**🎁 Recommend Loyalty Program Boosts:**")
st.dataframe(low_loyalty[['customer_id', 'total_spent', 'loyalty_spend', 'visits', 'tier_status']])

st.markdown("**🚀 Recommend Tier Upgrade Offers:**")
st.dataframe(near_upgrade[['customer_id', 'total_spent', 'tier_status']])
