
import os
import html
import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SALESVISTA | Smart Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #f5f6fa;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #eeeaff 0%,
        #edf5ff 52%,
        #eafff7 100%
    );
    border-right: 1px solid #dfe2eb;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] h1 {
    color: #4936a8 !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] h2 {
    color: #4936a8 !important;
    font-weight: 900 !important;
}

[data-testid="stSidebar"] h3 {
    color: #292c3d !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] label {
    color: #303344 !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] .stCaption {
    color: #687085 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #d9dce6 !important;
}

[data-testid="stSidebar"] .stFileUploader {
    background: rgba(255,255,255,0.70);
    border: 1px solid #dddff0;
    border-radius: 16px;
    padding: 8px;
}


/* ============================================================
   SIDEBAR MENU TEXT
   ============================================================ */

.sidebar-menu {
    background: rgba(255,255,255,0.58);
    border: 1px solid #dedff0;
    border-radius: 16px;
    padding: 14px 16px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.sidebar-menu-item {
    color: #44485b;
    font-size: 14px;
    font-weight: 600;
    padding: 6px 2px;
}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.main-title {
    font-size: 46px;
    font-weight: 900;
    letter-spacing: -1.5px;
    color: #4936a8;
    margin-bottom: 0;
}

.subtitle {
    color: #697084;
    font-size: 16px;
    margin-top: 3px;
    margin-bottom: 20px;
}


/* ============================================================
   DARK SECTION
   ============================================================ */

.dark-section {
    background: linear-gradient(
        135deg,
        #25243f 0%,
        #363866 100%
    );
    border-radius: 20px;
    padding: 24px 27px;
    margin-top: 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(38, 38, 68, 0.13);
}

.dark-section h2 {
    color: #ffffff;
    margin: 0;
    font-size: 24px;
}

.dark-section p {
    color: #d8daea;
    margin: 6px 0 0 0;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 24px;
    font-weight: 850;
    color: #272a3b;
    margin-top: 30px;
    margin-bottom: 14px;
}


/* ============================================================
   KPI
   ============================================================ */

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e1e4ec;
    border-radius: 18px;
    padding: 18px;
    min-height: 112px;
    box-shadow: 0 6px 22px rgba(42, 46, 75, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #687085;
    font-weight: 650;
}

div[data-testid="stMetricValue"] {
    color: #302d63;
    font-weight: 850;
}


/* ============================================================
   INFO CARD
   ============================================================ */

.info-card {
    background: #ffffff;
    border: 1px solid #e2e4ec;
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 7px 25px rgba(42, 46, 75, 0.06);
}

.info-card h2 {
    color: #4936a8;
}

.info-card p,
.info-card li {
    color: #687085;
    line-height: 1.7;
}


/* ============================================================
   FILTER SUMMARY
   ============================================================ */

.filter-summary {
    background: linear-gradient(
        135deg,
        #25243f,
        #3c3e69
    );
    color: white;
    border-radius: 17px;
    padding: 17px 22px;
    margin: 10px 0 22px 0;
    box-shadow: 0 6px 18px rgba(42, 46, 75, 0.10);
}

.filter-summary strong {
    color: #ffffff;
}

.filter-summary span {
    color: #d8daea;
}


/* ============================================================
   AI CARD
   ============================================================ */

.ai-card {
    background: linear-gradient(
        135deg,
        #eeeaff,
        #eaf5ff
    );
    border: 1px solid #d8d1ff;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 6px 22px rgba(56, 50, 110, 0.06);
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    border-radius: 12px;
    font-weight: 750;
    min-height: 44px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    border-radius: 16px;
}


/* ============================================================
   EXPANDER
   ============================================================ */

[data-testid="stExpander"] {
    border: 1px solid #e0e2ea;
    border-radius: 15px;
    background: #ffffff;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #777d90;
    font-size: 13px;
    padding: 38px 0 18px 0;
    margin-top: 40px;
    border-top: 1px solid #dfe2e9;
    line-height: 1.9;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_name(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def find_column(columns, names):

    normalized = {
        normalize_name(col): col
        for col in columns
    }

    targets = [
        normalize_name(name)
        for name in names
    ]

    # Exact match first
    for target in targets:
        if target in normalized:
            return normalized[target]

    # Partial match
    for col in columns:

        current = normalize_name(col)

        for target in targets:

            if target in current or current in target:
                return col

    return None


def money(value):

    if pd.isna(value):
        return "0"

    return f"{float(value):,.0f}"


def percentage(value):

    if pd.isna(value):
        return "0.0%"

    return f"{float(value):.1f}%"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("SALESVISTA")

    st.caption("Smart Sales Data Analysis")

    st.divider()

    st.subheader("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose an Excel or CSV file",
        type=["xlsx", "csv"],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("Dashboard")

    st.caption("Sales & Revenue")
    st.caption("Profitability")
    st.caption("Products")
    st.caption("Customers")
    st.caption("Categories")
    st.caption("Regions")
    st.caption("Orders & Payments")
    st.caption("AI Business Insights")

    st.divider()

    st.caption("Created by Areeba")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<div class='main-title'>SALESVISTA</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>"
    "Smart Sales Data Analysis Dashboard"
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if uploaded_file is None:

    st.markdown("## Welcome to SALESVISTA")

    st.write(
        "Upload your sales Excel or CSV dataset from the sidebar "
        "to transform your business data into interactive analytics."
    )

    st.markdown("""
    - Sales overview and KPIs
    - Revenue and profit trends
    - Top and bottom products
    - Customer analysis
    - Category and regional analysis
    - Date-wise interactive filtering
    - Payment and order-status analysis
    - AI-powered business recommendations
    """)

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

except Exception as error:

    st.error(
        f"Unable to read the dataset: {error}"
    )

    st.stop()


if df.empty:

    st.warning(
        "The uploaded dataset contains no records."
    )

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = [
    str(column).strip()
    for column in df.columns
]


# ============================================================
# COLUMN DETECTION
# ============================================================

order_col = find_column(
    df.columns,
    [
        "order id",
        "order number",
        "order no",
        "order"
    ]
)

date_col = find_column(
    df.columns,
    [
        "order date",
        "sales date",
        "transaction date",
        "date"
    ]
)

customer_id_col = find_column(
    df.columns,
    [
        "customer id",
        "client id"
    ]
)

customer_name_col = find_column(
    df.columns,
    [
        "customer name",
        "client name"
    ]
)

customer_col = (
    customer_id_col
    if customer_id_col
    else customer_name_col
)

product_col = find_column(
    df.columns,
    [
        "product",
        "product name",
        "item",
        "item name"
    ]
)

category_col = find_column(
    df.columns,
    [
        "category",
        "product category",
        "segment"
    ]
)

region_col = find_column(
    df.columns,
    [
        "region",
        "area",
        "territory"
    ]
)

city_col = find_column(
    df.columns,
    [
        "city"
    ]
)

quantity_col = find_column(
    df.columns,
    [
        "quantity",
        "qty",
        "units"
    ]
)

unit_price_col = find_column(
    df.columns,
    [
        "unit price",
        "price"
    ]
)

sales_col = find_column(
    df.columns,
    [
        "sales",
        "revenue",
        "sales amount",
        "total sales",
        "amount"
    ]
)

profit_col = find_column(
    df.columns,
    [
        "profit",
        "net profit",
        "gross profit"
    ]
)

discount_col = find_column(
    df.columns,
    [
        "discount"
    ]
)

payment_col = find_column(
    df.columns,
    [
        "payment method",
        "payment type",
        "payment"
    ]
)

status_col = find_column(
    df.columns,
    [
        "order status",
        "status"
    ]
)


# ============================================================
# DATA TYPE CLEANING
# ============================================================

if date_col:

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )


for column in [
    quantity_col,
    unit_price_col,
    sales_col,
    profit_col,
    discount_col
]:

    if column and column in df.columns:

        if df[column].dtype == "object":

            df[column] = (
                df[column]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# DATASET STATUS
# ============================================================

st.success(
    f"Dataset loaded successfully — "
    f"{len(df):,} records and "
    f"{len(df.columns):,} columns."
)


# ============================================================
# DETECTED FIELDS
# ============================================================

with st.expander("Detected Dataset Fields"):

    detected = pd.DataFrame({

        "Dashboard Feature": [
            "Order ID",
            "Order Date",
            "Customer ID / Customer",
            "Customer Name",
            "Product",
            "Category",
            "Region",
            "City",
            "Quantity",
            "Unit Price",
            "Sales",
            "Profit",
            "Discount",
            "Payment Method",
            "Order Status"
        ],

        "Detected Column": [
            order_col or "Not detected",
            date_col or "Not detected",
            customer_col or "Not detected",
            customer_name_col or "Not detected",
            product_col or "Not detected",
            category_col or "Not detected",
            region_col or "Not detected",
            city_col or "Not detected",
            quantity_col or "Not detected",
            unit_price_col or "Not detected",
            sales_col or "Not detected",
            profit_col or "Not detected",
            discount_col or "Not detected",
            payment_col or "Not detected",
            status_col or "Not detected"
        ]

    })

    st.dataframe(
        detected,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("Interactive Filters")

filtered_df = df.copy()


# ============================================================
# DATE FILTER
# ============================================================

if date_col:

    valid_dates = df[date_col].dropna()

    if not valid_dates.empty:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(date_range, tuple):

            if len(date_range) == 2:

                start_date = date_range[0]
                end_date = date_range[1]

                filtered_df = filtered_df[
                    (
                        filtered_df[date_col].dt.date
                        >= start_date
                    )
                    &
                    (
                        filtered_df[date_col].dt.date
                        <= end_date
                    )
                ]


# ============================================================
# REGION FILTER
# ============================================================

if region_col:

    region_values = sorted(
        df[region_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_regions = st.sidebar.multiselect(
        "Region",
        region_values,
        default=region_values
    )

    if selected_regions:

        filtered_df = filtered_df[
            filtered_df[region_col]
            .astype(str)
            .isin(selected_regions)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# CATEGORY FILTER
# ============================================================

if category_col:

    category_values = sorted(
        df[category_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Category",
        category_values,
        default=category_values
    )

    if selected_categories:

        filtered_df = filtered_df[
            filtered_df[category_col]
            .astype(str)
            .isin(selected_categories)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# PRODUCT FILTER
# ============================================================

if product_col:

    product_values = sorted(
        df[product_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(product_values) <= 150:

        selected_products = st.sidebar.multiselect(
            "Product",
            product_values,
            default=product_values
        )

        if selected_products:

            filtered_df = filtered_df[
                filtered_df[product_col]
                .astype(str)
                .isin(selected_products)
            ]

        else:

            filtered_df = filtered_df.iloc[0:0]


# ============================================================
# CUSTOMER FILTER
# ============================================================

if customer_col:

    customer_values = sorted(
        df[customer_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(customer_values) <= 200:

        selected_customers = st.sidebar.multiselect(
            "Customer",
            customer_values,
            default=customer_values
        )

        if selected_customers:

            filtered_df = filtered_df[
                filtered_df[customer_col]
                .astype(str)
                .isin(selected_customers)
            ]

        else:

            filtered_df = filtered_df.iloc[0:0]


# ============================================================
# ORDER STATUS FILTER
# ============================================================

if status_col:

    status_values = sorted(
        df[status_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_status = st.sidebar.multiselect(
        "Order Status",
        status_values,
        default=status_values
    )

    if selected_status:

        filtered_df = filtered_df[
            filtered_df[status_col]
            .astype(str)
            .isin(selected_status)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# PAYMENT FILTER
# ============================================================

if payment_col:

    payment_values = sorted(
        df[payment_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_payments = st.sidebar.multiselect(
        "Payment Method",
        payment_values,
        default=payment_values
    )

    if selected_payments:

        filtered_df = filtered_df[
            filtered_df[payment_col]
            .astype(str)
            .isin(selected_payments)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ============================================================
# CHECK FILTER RESULT
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change your filter selections."
    )

    st.stop()


# ============================================================
# FILTER SUMMARY
# ============================================================

st.markdown("### Current Analysis")

st.info(
    f"Showing {len(filtered_df):,} of {len(df):,} "
    "records after applying the selected filters."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

if sales_col:

    total_sales = (
        pd.to_numeric(
            filtered_df[sales_col],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

else:

    total_sales = 0


if profit_col:

    total_profit = (
        pd.to_numeric(
            filtered_df[profit_col],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

else:

    total_profit = 0


if order_col:

    total_orders = filtered_df[order_col].nunique()

else:

    total_orders = len(filtered_df)


if customer_col:

    total_customers = filtered_df[customer_col].nunique()

else:

    total_customers = 0


average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)


# ============================================================
# BUSINESS OVERVIEW
# ============================================================

st.markdown(
    "<div class='section-title'>Business Overview</div>",
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)


with c1:
    st.metric(
        "Total Sales",
        money(total_sales)
    )


with c2:
    st.metric(
        "Total Profit",
        money(total_profit)
    )


with c3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with c4:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


# ============================================================
# SECONDARY KPIs
# ============================================================

c5, c6, c7 = st.columns(3)


with c5:
    st.metric(
        "Average Order Value",
        money(average_order_value)
    )


with c6:
    st.metric(
        "Profit Margin",
        percentage(profit_margin)
    )


with c7:
    st.metric(
        "Records Analyzed",
        f"{len(filtered_df):,}"
    )


# ============================================================
# SALES & REVENUE SECTION
# ============================================================

st.markdown("## Sales & Revenue Analytics")

st.caption(
    "Analyze revenue and profit performance across time."
)


# ============================================================
# MONTHLY REVENUE + PROFIT
# ============================================================

if date_col and sales_col:

    monthly_df = filtered_df.dropna(
        subset=[date_col]
    ).copy()

    if not monthly_df.empty:

        monthly_df["Month"] = (
            monthly_df[date_col]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_sales = (
            monthly_df
            .groupby("Month")[sales_col]
            .sum()
            .reset_index()
        )

        if profit_col:

            monthly_profit = (
                monthly_df
                .groupby("Month")[profit_col]
                .sum()
                .reset_index()
            )

            monthly = monthly_sales.merge(
                monthly_profit,
                on="Month",
                how="left"
            )

            monthly_long = monthly.melt(
                id_vars=["Month"],
                value_vars=[
                    sales_col,
                    profit_col
                ],
                var_name="Metric",
                value_name="Value"
            )

            monthly_long["Metric"] = (
                monthly_long["Metric"]
                .replace({
                    sales_col: "Revenue",
                    profit_col: "Profit"
                })
            )

            fig = px.line(
                monthly_long,
                x="Month",
                y="Value",
                color="Metric",
                markers=True,
                title="Monthly Revenue & Profit Trend"
            )

        else:

            fig = px.line(
                monthly_sales,
                x="Month",
                y=sales_col,
                markers=True,
                title="Monthly Sales Trend"
            )

        fig.update_layout(
            template="plotly_white",
            height=450,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# WEEKLY SALES TREND
# ============================================================

if date_col and sales_col:

    weekly_df = filtered_df.dropna(
        subset=[date_col]
    ).copy()

    if not weekly_df.empty:

        weekly_df["Week"] = (
            weekly_df[date_col]
            .dt.to_period("W")
            .apply(lambda x: x.start_time)
        )

        weekly_sales = (
            weekly_df
            .groupby("Week")[sales_col]
            .sum()
            .reset_index()
        )

        fig = px.line(
            weekly_sales,
            x="Week",
            y=sales_col,
            markers=True,
            title="Weekly Sales Trend"
        )

        fig.update_layout(
            template="plotly_white",
            height=420,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.markdown(
    "<div class='section-title'>Product Performance</div>",
    unsafe_allow_html=True
)

p1, p2 = st.columns(2)


# TOP PRODUCTS
with p1:

    if product_col and sales_col:

        top_products = (
            filtered_df
            .groupby(product_col)[sales_col]
            .sum()
            .reset_index()
            .sort_values(
                sales_col,
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            top_products,
            x=sales_col,
            y=product_col,
            orientation="h",
            title="Top 10 Products by Sales"
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# BOTTOM PRODUCTS
with p2:

    if product_col and sales_col:

        bottom_products = (
            filtered_df
            .groupby(product_col)[sales_col]
            .sum()
            .reset_index()
            .sort_values(
                sales_col,
                ascending=True
            )
            .head(10)
        )

        fig = px.bar(
            bottom_products,
            x=sales_col,
            y=product_col,
            orientation="h",
            title="Bottom 10 Products by Sales"
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PRODUCT PROFIT
# ============================================================

if product_col and profit_col:

    product_profit = (
        filtered_df
        .groupby(product_col)[profit_col]
        .sum()
        .reset_index()
        .sort_values(
            profit_col,
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        product_profit,
        x=product_col,
        y=profit_col,
        title="Top 10 Products by Profit"
    )

    fig.update_layout(
        template="plotly_white",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

st.markdown(
    "<div class='section-title'>Category Analysis</div>",
    unsafe_allow_html=True
)

cat1, cat2 = st.columns(2)


with cat1:

    if category_col and sales_col:

        category_sales = (
            filtered_df
            .groupby(category_col)[sales_col]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            category_sales,
            names=category_col,
            values=sales_col,
            hole=0.5,
            title="Category Sales Contribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with cat2:

    if category_col and profit_col:

        category_profit = (
            filtered_df
            .groupby(category_col)[profit_col]
            .sum()
            .reset_index()
            .sort_values(
                profit_col,
                ascending=False
            )
        )

        fig = px.bar(
            category_profit,
            x=category_col,
            y=profit_col,
            title="Profit by Category"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# REGION ANALYSIS
# ============================================================

st.markdown(
    "<div class='section-title'>Regional Performance</div>",
    unsafe_allow_html=True
)

r1, r2 = st.columns(2)


with r1:

    if region_col and sales_col:

        region_sales = (
            filtered_df
            .groupby(region_col)[sales_col]
            .sum()
            .reset_index()
            .sort_values(
                sales_col,
                ascending=False
            )
        )

        fig = px.bar(
            region_sales,
            x=region_col,
            y=sales_col,
            title="Sales by Region"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with r2:

    if region_col and profit_col:

        region_profit = (
            filtered_df
            .groupby(region_col)[profit_col]
            .sum()
            .reset_index()
            .sort_values(
                profit_col,
                ascending=False
            )
        )

        fig = px.bar(
            region_profit,
            x=region_col,
            y=profit_col,
            title="Profit by Region"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# CITY PERFORMANCE
# ============================================================

if city_col and sales_col:

    st.markdown(
        "<div class='section-title'>City Performance</div>",
        unsafe_allow_html=True
    )

    city_sales = (
        filtered_df
        .groupby(city_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(
            sales_col,
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        city_sales,
        x=sales_col,
        y=city_col,
        orientation="h",
        title="Top 10 Cities by Sales"
    )

    fig.update_layout(
        template="plotly_white",
        height=440,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

st.markdown(
    "<div class='section-title'>Customer Analysis</div>",
    unsafe_allow_html=True
)

cu1, cu2 = st.columns(2)


# CUSTOMER SALES
with cu1:

    if customer_col and sales_col:

        customer_sales = (
            filtered_df
            .groupby(customer_col)[sales_col]
            .sum()
            .reset_index()
            .sort_values(
                sales_col,
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            customer_sales,
            x=customer_col,
            y=sales_col,
            title="Top 10 Customers by Sales"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# CUSTOMER ORDERS
with cu2:

    if customer_col and order_col:

        customer_orders = (
            filtered_df
            .groupby(customer_col)[order_col]
            .nunique()
            .reset_index()
            .sort_values(
                order_col,
                ascending=False
            )
            .head(10)
        )

        customer_orders.columns = [
            "Customer",
            "Orders"
        ]

        fig = px.bar(
            customer_orders,
            x="Customer",
            y="Orders",
            title="Top 10 Customers by Orders"
        )

        fig.update_layout(
            template="plotly_white",
            height=440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PROFIT VS SALES
# ============================================================

st.markdown(
    "<div class='section-title'>Profitability Analysis</div>",
    unsafe_allow_html=True
)

if sales_col and profit_col:

    hover_columns = [
        column
        for column in [
            product_col,
            category_col,
            region_col,
            customer_col
        ]
        if column
    ]

    fig = px.scatter(
        filtered_df,
        x=sales_col,
        y=profit_col,
        color=category_col if category_col else None,
        hover_data=hover_columns,
        title="Profit vs Sales"
    )

    fig.update_layout(
        template="plotly_white",
        height=480
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ORDER STATUS
# ============================================================

if status_col and sales_col:

    st.markdown(
        "<div class='section-title'>Order Status Analysis</div>",
        unsafe_allow_html=True
    )

    status_sales = (
        filtered_df
        .groupby(status_col)[sales_col]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        status_sales,
        names=status_col,
        values=sales_col,
        hole=0.48,
        title="Sales by Order Status"
    )

    fig.update_layout(
        template="plotly_white",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAYMENT METHOD
# ============================================================

if payment_col and sales_col:

    st.markdown(
        "<div class='section-title'>Payment Method Analysis</div>",
        unsafe_allow_html=True
    )

    payment_sales = (
        filtered_df
        .groupby(payment_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(
            sales_col,
            ascending=False
        )
    )

    fig = px.bar(
        payment_sales,
        x=payment_col,
        y=sales_col,
        title="Sales by Payment Method"
    )

    fig.update_layout(
        template="plotly_white",
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AI BUSINESS ANALYST
# ============================================================

st.markdown("## AI Business Analyst")

st.caption(
    "Generate business insights and practical recommendations "
    "from the currently filtered sales data."
)


# ============================================================
# GROQ API KEY
# ============================================================

# First use the variable created by the separate getpass cell.
# If it is not available, fall back to the environment variable.

groq_key = globals().get("GROQ_API_KEY")

if not groq_key:
    groq_key = os.getenv("GROQ_API_KEY")


if groq_key:

    if st.button(
        "Generate AI Business Insights",
        use_container_width=True
    ):

        try:

            client = Groq(
                api_key=groq_key
            )

            # ---------------- TOP PRODUCT ----------------

            top_product = "Not available"

            if product_col and sales_col:

                product_summary = (
                    filtered_df
                    .groupby(product_col)[sales_col]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                if not product_summary.empty:

                    top_product = str(
                        product_summary.index[0]
                    )


            # ---------------- TOP CATEGORY ----------------

            top_category = "Not available"

            if category_col and sales_col:

                category_summary = (
                    filtered_df
                    .groupby(category_col)[sales_col]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                if not category_summary.empty:

                    top_category = str(
                        category_summary.index[0]
                    )


            # ---------------- TOP REGION ----------------

            top_region = "Not available"

            if region_col and sales_col:

                region_summary = (
                    filtered_df
                    .groupby(region_col)[sales_col]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                if not region_summary.empty:

                    top_region = str(
                        region_summary.index[0]
                    )


            prompt = f"""
You are the professional AI Business Analyst inside SALESVISTA.

Analyze ONLY the following calculated business information.

Records analyzed:
{len(filtered_df):,}

Total Sales:
{total_sales:,.2f}

Total Profit:
{total_profit:,.2f}

Total Orders:
{total_orders:,}

Unique Customers:
{total_customers:,}

Average Order Value:
{average_order_value:,.2f}

Profit Margin:
{profit_margin:.2f}%

Top Product:
{top_product}

Top Category:
{top_category}

Top Region:
{top_region}

Create a concise professional business analysis using these sections:

1. Overall Performance
2. Revenue & Profitability
3. Product & Category Insight
4. Customer & Regional Insight
5. Business Opportunity
6. Practical Recommendation

Rules:

- Do not invent statistics.
- Use only the supplied information.
- Keep the analysis practical.
- Highlight important business opportunities.
- Keep the response easy to read.
"""

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=1000
            )

            insight = (
                response
                .choices[0]
                .message
                .content
            )

            st.markdown("### AI Business Analysis")
            st.markdown(insight)

        except Exception as error:

            st.error(
                f"AI analysis could not be generated: {error}"
            )

else:

    st.info(
        "Groq AI is not connected. "
        "Run the secure Groq API key cell in Colab "
        "to enable AI Business Insights."
    )


# ============================================================
# DETAILED DATA TABLE
# ============================================================

st.markdown(
    "<div class='section-title'>Detailed Sales Data</div>",
    unsafe_allow_html=True
)

st.caption(
    f"{len(filtered_df):,} records currently displayed."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=520,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SALESVISTA • Smart Sales Data Analysis Dashboard"
)

st.caption(
    "© 2026 SALESVISTA. All Rights Reserved."
)

st.caption(
    "Designed & Developed by Areeba Imran"
)
