
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df_perf = pd.read_csv("df_performance.csv")
summary = pd.read_csv("band_year_summary.csv")

st.set_page_config(page_title="Spectrum Auction Dashboard", layout="wide")
st.title("Spectrum Auction Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
bands = sorted(df_perf['Band'].astype(str).unique())
years = sorted(df_perf['Year'].astype(str).unique())
areas = sorted(df_perf['Service_Area'].astype(str).unique())

selected_band = st.sidebar.selectbox("Select Band", bands)
selected_year = st.sidebar.selectbox("Select Year", years)
selected_area = st.sidebar.selectbox("Select Service Area", areas)

# Clean and ensure consistent types
df_perf['Band'] = df_perf['Band'].astype(str).str.strip()
df_perf['Year'] = df_perf['Year'].astype(str).str.strip()
df_perf['Service_Area'] = df_perf['Service_Area'].astype(str).str.strip()

selected_band = str(selected_band).strip()
selected_year = str(selected_year).strip()
selected_area = str(selected_area).strip()

# Filtered Data
filtered = df_perf[
    (df_perf['Band'] == selected_band) &
    (df_perf['Year'] == selected_year) &
    (df_perf['Service_Area'] == selected_area)
]

# Display KPIs and charts only if data is available
if not filtered.empty:
    row = filtered.iloc[0]

    st.subheader(f"Auction Summary for {selected_area}, Band {selected_band}, Year {selected_year}")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Blocks Offered", int(row['Blocks_Offered']))
    col2.metric("Blocks Bought", int(row['Blocks_Bought']))
    col3.metric("% Spectrum Sold", f"{row['Percent_Sold']:.2f}%")
    col4.metric("Companies Participated", int(row['Companies']))

    st.subheader("WP vs RP Comparison")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Sum of RP for all blocks offered ", "Sum of WP for all sold blocks"], [
        row['Reserve_Price_Total'],
        row['Winning_Price_Total']
    ])
    ax.set_ylabel("₹ in Crores")
    st.pyplot(fig)
else:
    st.warning("⚠️ No data available for the selected combination. Try a different Band, Year, or Service Area.")

# Band-Year Summary Chart
st.subheader("% Spectrum Sold by Band-Year")
summary['Label'] = summary['Band'].astype(str) + "_" + summary['Year'].astype(str)
fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.bar(summary['Label'], summary['Avg_Percent_Sold'])
ax2.set_xticklabels(summary['Label'], rotation=90)
ax2.set_ylabel('% Sold')
st.pyplot(fig2)

# Heatmap
st.subheader("Heatmap: % Spectrum Sold by Service Area")
heatmap_df = df_perf.copy()
heatmap_df['Band_Year'] = heatmap_df['Band'].astype(str) + "_" + heatmap_df['Year'].astype(str)
pivot = heatmap_df.pivot(index='Service_Area', columns='Band_Year', values='Percent_Sold')

fig3, ax3 = plt.subplots(figsize=(14, 8))
sns.heatmap(pivot, cmap="YlGnBu", linewidths=.3, ax=ax3)
st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("Made with Streamlit | Data Source: DoT & TRAI | Author: WPC")
