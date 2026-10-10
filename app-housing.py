import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- 页面标题 ----------------------
st.title("California Housing Data (1990) by Mohan Xu")
st.subheader("See more filters in the sidebar:")

# ---------------------- 读取csv数据 ----------------------
df = pd.read_csv("housing.csv")

# ---------------------- 侧边栏筛选组件 ----------------------
st.sidebar.header("Filter Options")

# 1. 房价滑块 Minimal Median House Value
min_house_value = st.sidebar.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)
df_filtered = df[df["median_house_value"] >= min_house_value]

# 2. multiselect 多选 ocean_proximity
location_types = st.sidebar.multiselect(
    "Choose the location type",
    options=df["ocean_proximity"].unique(),
    default=df["ocean_proximity"].unique()
)
df_filtered = df_filtered[df_filtered["ocean_proximity"].isin(location_types)]

# 3. Radio单选框 收入等级 Low / Medium / High
income_level = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"]
)

if income_level == "Low":
    df_filtered = df_filtered[df_filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    df_filtered = df_filtered[(df_filtered["median_income"] > 2.5) & (df_filtered["median_income"] < 4.5)]
elif income_level == "High":
    df_filtered = df_filtered[df_filtered["median_income"] >= 4.5]


# ---------------------- Matplotlib绘制地图（经纬度散点图） ----------------------
st.subheader("The map shows the filtered districts:")
fig_map, ax_map = plt.subplots(figsize=(8, 6))
# 散点：longitude x轴，latitude y轴，红色点（和示例图一致）
ax_map.scatter(df_filtered["longitude"], df_filtered["latitude"], color="red", alpha=0.6, s=8)
ax_map.set_xlabel("Longitude")
ax_map.set_ylabel("Latitude")
ax_map.set_title("Filtered California Housing Districts")
ax_map.grid(alpha=0.3)
st.pyplot(fig_map)


# ---------------------- Matplotlib绘制直方图 bins=30 ----------------------
st.subheader("The histogram goes below the map:")
fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
ax_hist.hist(df_filtered["median_house_value"], bins=30, color="#1f77b4")
ax_hist.set_xlabel("Median House Value")
ax_hist.set_ylabel("Count")
ax_hist.set_title("Histogram of Median House Value")
st.pyplot(fig_hist)
