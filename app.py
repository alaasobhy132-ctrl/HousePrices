#%%writefile app.py
import streamlit as st
import pandas as pd
#import plotly.express as px

# صورة في الهيدر
st.image(
    "https://images.unsplash.com/photo-1564013794911-6c2b98d0c9f0",  # صورة لبيوت
    use_container_width=True
)

st.set_page_config(
    page_title="House Prices Dashboard",
    layout="wide"
)

# -------------------------
# Load Data
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    # معالجة بسيطة للـ missing values
    df['LotFrontage'] = df['LotFrontage'].fillna(df['LotFrontage'].median())
    df['MasVnrArea'] = df['MasVnrArea'].fillna(0)
    df['GarageYrBlt'] = df['GarageYrBlt'].fillna(df['GarageYrBlt'].median())
    return df

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.title("Filters")

neighborhood_filter = st.sidebar.multiselect(
    "Neighborhood",
    options=df["Neighborhood"].unique(),
    default=df["Neighborhood"].unique()
)

style_filter = st.sidebar.multiselect(
    "House Style",
    options=df["HouseStyle"].unique(),
    default=df["HouseStyle"].unique()
)

year_filter = st.sidebar.slider(
    "Year Built Range",
    int(df.YearBuilt.min()),
    int(df.YearBuilt.max()),
    (int(df.YearBuilt.min()), int(df.YearBuilt.max()))
)

price_filter = st.sidebar.slider(
    "Sale Price Range",
    int(df.SalePrice.min()),
    int(df.SalePrice.max()),
    (int(df.SalePrice.min()), int(df.SalePrice.max()))
)

# -------------------------
# Apply Filters
# -------------------------

filtered_df = df[
    (df["Neighborhood"].isin(neighborhood_filter)) &
    (df["HouseStyle"].isin(style_filter)) &
    (df["YearBuilt"].between(year_filter[0], year_filter[1])) &
    (df["SalePrice"].between(price_filter[0], price_filter[1]))
]

# -------------------------
# Page Navigation
# -------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Main Dashboard",
        "Analysis",
        "Final Insights"
    ]
)

# =================================================
# MAIN PAGE
# =================================================

if page == "Main Dashboard":

    st.title("🏠 House Prices Dashboard")

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head())

    st.divider()

    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    total_records = filtered_df.shape[0]
    avg_price = filtered_df["SalePrice"].mean()
    avg_quality = filtered_df["OverallQual"].mean()
    avg_area = filtered_df["LotArea"].mean()

    col1.metric("Total Records", total_records)
    col2.metric("Average Sale Price", f"${avg_price:,.0f}")
    col3.metric("Average Quality", round(avg_quality, 2))
    col4.metric("Average Lot Area", f"{avg_area:,.0f} sqft")

# =================================================
# ANALYSIS PAGE
# =================================================

elif page == "Analysis":

    st.title("📊 Exploratory Data Analysis")

    tab1, tab2, tab3 = st.tabs([
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis"
    ])

    with tab1:
        st.subheader("Univariate Analysis")
        fig1 = px.histogram(filtered_df, x="SalePrice", nbins=50, title="Sale Price Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Bivariate Analysis")
        avg_price_by_neighborhood = filtered_df.groupby("Neighborhood")["SalePrice"].mean().reset_index()
        fig2 = px.bar(avg_price_by_neighborhood, x="Neighborhood", y="SalePrice", title="Average Sale Price by Neighborhood")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Multivariate Analysis")
        fig3 = px.scatter(filtered_df, x="GrLivArea", y="SalePrice", color="OverallQual",
                          title="Sale Price vs Living Area (colored by Quality)")
        st.plotly_chart(fig3, use_container_width=True)

# =================================================
# FINAL INSIGHTS PAGE
# =================================================

elif page == "Final Insights":

    st.title("🧠 Key Insights")

    st.markdown("""
    ### Main Findings

    - Higher quality houses (OverallQual) strongly correlate with higher SalePrice  
    - Neighborhoods differ significantly in average SalePrice  
    - Larger living area (GrLivArea) is associated with higher SalePrice  

    ### Business Recommendations

    - Focus on improving house quality to maximize value  
    - Target neighborhoods with higher average prices for premium listings  
    - Highlight living area size in marketing strategies  
    """)


#! streamlit run app1.py