import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import os
import pandas as pd

import os
import pandas as pd

# Load original CSV file
df = pd.read_csv("sales_data_cleaned.csv")

# Create data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Save cleaned CSV
file_path = os.path.join(DATA_DIR, "sales_data_cleaned.csv")
df.to_csv(file_path, index=False)

print("File saved successfully at:", file_path)

# page configuration
st.set_page_config(
    page_title = "Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Cleand data
df = pd.read_csv("Sales_data_cleaned.csv")
df.to_csv("data/sales_data_cleaned.csv", index=False)

# Dashboard  Title
st.title("📊 Sales Analysis Dashboard")
st.write("Explore your sales data interactively.")

# Convert column to numeric
for col in ["Sales", "Profit"]:
    df[col] = pd.to_numeric(df[col], errors= "coerce")


# Sidebar Fiter
st.sidebar.header("Filters")

if"City" in df.columns:
    cities = sorted(df["City"].dropna().unique())
    selected_cities = st.sidebar.multiselect(
        "Select City",
        cities,
        default=cities
    )
    df = df[df["City"].isin(selected_cities)]


# Date filter
if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"], errors="coerce"
    )

    valid_dates = df["Order_Date"].dropna()

    if not valid_dates.empty:
        start_date = st.sidebar.date_input(
            "Start Date",
            value=valid_dates.min().date()
        )

        end_date = st.sidebar.date_input(
            "End Date",
            value=valid_dates.max().date()
        )

        if start_date <= end_date:
            df = df[
                df["Order_Date"].isna()
                | (
                    df["Order_Date"].dt.date.between(
                        start_date, end_date
                    )
                )
            ]
        else:
            st.sidebar.error(
                "Start Date, End Date se pehle honi chahiye."
            )

# Category filter
if "Category" in df.columns:
    categories = sorted(
        df["Category"].dropna().unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )

    df = df[
        df["Category"].isin(selected_categories)
    ]



# KPI metrics
total_sales = df["Sales"].sum(min_count=1)
total_orders = df["Order_ID"].nunique()
total_profit = df["Profit"].sum(min_count=1)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Sales",
    f"₹{total_sales:,.2f}"
    if pd.notna(total_sales) else "N/A"
)

c2.metric("Total Orders", f"{total_orders:,}")

c3.metric(
    "Recorded Profit",
    f"₹{total_profit:,.2f}"
    if pd.notna(total_profit) else "N/A"
)

st.divider()

# Top products chart
st.subheader("Top 5 Products by Sales")

if {"Product", "Sales"}.issubset(df.columns):
    top_products = (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.bar_chart(top_products)

# City-wise sales
st.subheader("City-wise Sales")

if {"City", "Sales"}.issubset(df.columns):
    city_sales = (
        df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(city_sales)



st.subheader("📈 Monthly Sales Trend")

if "Order_Date" in df.columns and "Sales" in df.columns:
    monthly_sales = (
        df.dropna(subset=["Order_Date"])
        .groupby(
            df.dropna(subset=["Order_Date"])[
                "Order_Date"
            ].dt.to_period("M")
        )["Sales"]
        .sum()
    )

    monthly_sales.index = monthly_sales.index.astype(str)

    st.line_chart(monthly_sales)



st.subheader("📊 Sales by Category")

if {"Category", "Sales"}.issubset(df.columns):
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)


# Data preview
st.subheader("Cleaned Data Preview")
st.dataframe(df, use_container_width=True)


st.subheader("Download Filtered Data")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="sales_analysis_filtered.csv",
    mime="text/csv"
)

 
