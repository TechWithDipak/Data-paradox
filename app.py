"""
RetailCo – Customer Churn Analysis System
Main Streamlit Application Entrypoint.
Academic Project: SRMIST 21IPE341T - Mastering the Data Paradox with AI and ML
"""

import streamlit as st
import pandas as pd
from config import APP_TITLE, APP_SUBTITLE, ACADEMIC_META, COLORS
from data_loader import load_all_data
from components.overview_tab import render_overview_tab
from components.customer_tab import render_customer_tab
from components.recommendation_tab import render_recommendation_tab
from components.marketing_tab import render_marketing_tab
from components.mece_tab import render_mece_tab
from components.findings_tab import render_findings_tab


# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern, Professional Corporate Look
st.markdown(
    """
    <style>
    /* Main container styling */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }
    /* Header card styling */
    .header-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 35%, #1E40AF 70%, #0284C7 100%);
        color: white;
        padding: 26px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2), 0 4px 6px -2px rgba(15, 23, 42, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .header-title {
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #FFFFFF;
    }
    .header-sub {
        font-size: 15.5px;
        color: #E0E7FF;
        margin-top: 6px;
        margin-bottom: 12px;
        font-weight: 400;
    }
    .header-meta {
        font-size: 13px;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.25);
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        color: #F8FAFC;
        font-weight: 500;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-size: 14.5px;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        padding: 0 18px;
        color: #475569;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%) !important;
        color: #1E40AF !important;
        border-bottom: 3.5px solid #2563EB !important;
    }
    /* Metric Card Styling with vibrant accent borders */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #2563EB;
        padding: 16px 18px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #475569 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800;
        color: #0F172A !important;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
        border-right: 1px solid #E2E8F0;
    }
        font-size: 24px !important;
        font-weight: 700;
        color: #111827 !important;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    # Load Verified Excel Dataset
    try:
        data = load_all_data()
    except Exception as e:
        st.error(f"Error loading Excel dataset: {e}")
        st.stop()

    df_customers_raw = data["customers"]
    df_recommendations_raw = data["recommendations"]
    df_campaigns_raw = data["campaigns"]
    df_churn_trend = data["churn_trend"]

    # Header Card
    st.markdown(
        f"""
        <div class="header-card">
            <h1 class="header-title">{APP_TITLE}</h1>
            <div class="header-sub">{APP_SUBTITLE}</div>
            <div class="header-meta">{ACADEMIC_META}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Filter Controls
    with st.sidebar:
        st.markdown("### Analysis Controls & Filters")
        st.caption("Filters update all dashboard charts and statistical calculations automatically.")

        # Location Filter
        all_locations = sorted(df_customers_raw["Location"].unique().tolist())
        selected_locations = st.multiselect(
            "Filter by Customer Location:",
            options=all_locations,
            default=all_locations
        )

        # Loyalty Tier Filter
        all_tiers = ["Bronze", "Silver", "Gold"]
        selected_tiers = st.multiselect(
            "Filter by Loyalty Tier:",
            options=all_tiers,
            default=all_tiers
        )

        # Gender Filter
        all_genders = ["M", "F"]
        selected_genders = st.multiselect(
            "Filter by Gender:",
            options=all_genders,
            default=all_genders,
            format_func=lambda g: "Male (M)" if g == "M" else "Female (F)"
        )

        # Campaign Channel Filter
        all_channels = sorted(df_campaigns_raw["Channel"].unique().tolist())
        selected_channels = st.multiselect(
            "Filter Marketing Channels:",
            options=all_channels,
            default=all_channels
        )

        # Reset button
        if st.button("Reset All Filters", use_container_width=True):
            st.rerun()

        st.markdown("---")
        st.markdown("#### Verified Dataset Status")
        st.caption(
            f"**Customers**: {len(df_customers_raw)} records\n\n"
            f"**Recommendations**: {len(df_recommendations_raw)} records\n\n"
            f"**Campaigns**: {len(df_campaigns_raw)} records\n\n"
            f"**Churn Trend**: {len(df_churn_trend)} quarters\n\n"
            f"*Primary data source: RetailCo.xlsx.*"
        )

    # Apply Filters to Customer Dataset
    df_customers = df_customers_raw[
        (df_customers_raw["Location"].isin(selected_locations if selected_locations else all_locations)) &
        (df_customers_raw["Loyalty_Tier"].isin(selected_tiers if selected_tiers else all_tiers)) &
        (df_customers_raw["Gender"].isin(selected_genders if selected_genders else all_genders))
    ]

    # Filtered Customer IDs for Recommendation linkage
    filtered_cust_ids = set(df_customers["Customer_ID"].unique())
    df_recommendations = df_recommendations_raw[df_recommendations_raw["Customer_ID"].isin(filtered_cust_ids)]

    # Filtered Campaigns
    df_campaigns = df_campaigns_raw[df_campaigns_raw["Channel"].isin(selected_channels if selected_channels else all_channels)]

    # Main Tabs
    tab_overview, tab_cust, tab_rec, tab_mkt, tab_mece, tab_findings = st.tabs([
        "Executive Overview",
        "Customer Analysis",
        "AI Recommendations",
        "Marketing & ROI",
        "MECE Issue Tree",
        "Final Findings & Actions"
    ])

    with tab_overview:
        render_overview_tab(df_customers, df_churn_trend, df_campaigns, df_recommendations)

    with tab_cust:
        render_customer_tab(df_customers)

    with tab_rec:
        render_recommendation_tab(df_recommendations, df_customers)

    with tab_mkt:
        render_marketing_tab(df_campaigns)

    with tab_mece:
        render_mece_tab()

    with tab_findings:
        render_findings_tab(df_churn_trend, df_campaigns, df_customers)


if __name__ == "__main__":
    main()
