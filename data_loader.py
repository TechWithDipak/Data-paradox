"""
Data Loader module for RetailCo Churn Analysis System.
Loads and preprocesses all four sheets from the primary Excel file.
"""

from typing import Dict, Tuple
import os
import pandas as pd
import streamlit as st

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "RetailCo.xlsx")


def clean_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Removes trailing unnamed columns and strips column names."""
    cols_to_keep = [col for col in df.columns if not str(col).startswith("Unnamed")]
    cleaned_df = df[cols_to_keep].copy()
    cleaned_df.columns = [str(c).strip() for c in cleaned_df.columns]
    return cleaned_df


@st.cache_data(show_spinner=False)
def load_all_data(file_path: str = DATA_FILE_PATH) -> Dict[str, pd.DataFrame]:
    """
    Loads all four sheets from the uploaded RetailCo Excel workbook.
    Returns a dictionary of cleaned DataFrames.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"RetailCo Excel dataset not found at: {file_path}")

    xls = pd.ExcelFile(file_path)
    required_sheets = [
        "RetailCo_Customers",
        "RetailCo_Recommendations",
        "RetailCo_Campaigns",
        "RetailCo_ChurnTrend"
    ]

    for req in required_sheets:
        if req not in xls.sheet_names:
            raise ValueError(f"Required sheet '{req}' not found in Excel. Found sheets: {xls.sheet_names}")

    # 1. Customers Sheet
    df_customers = clean_dataframe_columns(pd.read_excel(file_path, sheet_name="RetailCo_Customers"))
    df_customers["Customer_ID"] = df_customers["Customer_ID"].astype(str).str.strip()
    df_customers["Gender"] = df_customers["Gender"].astype(str).str.strip()
    df_customers["Location"] = df_customers["Location"].astype(str).str.strip()
    df_customers["Loyalty_Tier"] = df_customers["Loyalty_Tier"].astype(str).str.strip()
    df_customers["Churn_Flag"] = df_customers["Churn_Flag"].astype(str).str.strip().str.upper()
    df_customers["Age"] = pd.to_numeric(df_customers["Age"], errors="coerce")
    df_customers["Last_Purchase_Date_Parsed"] = pd.to_datetime(
        df_customers["Last_Purchase_Date"], format="mixed", errors="coerce"
    )
    df_customers["Last_Purchase_Date"] = df_customers["Last_Purchase_Date_Parsed"].dt.strftime("%Y-%m-%d")

    # Age Group Binning
    bins = [0, 25, 35, 45, 100]
    labels = ["18-25", "26-35", "36-45", "46+"]
    df_customers["Age_Group"] = pd.cut(df_customers["Age"], bins=bins, labels=labels, right=True)

    # 2. Recommendations Sheet
    df_recommendations = clean_dataframe_columns(pd.read_excel(file_path, sheet_name="RetailCo_Recommendations"))
    df_recommendations["Customer_ID"] = df_recommendations["Customer_ID"].astype(str).str.strip()
    df_recommendations["Recommended_Category"] = df_recommendations["Recommended_Category"].astype(str).str.strip()
    df_recommendations["Clicked?"] = df_recommendations["Clicked?"].astype(str).str.strip()
    df_recommendations["Purchased?"] = df_recommendations["Purchased?"].astype(str).str.strip()
    df_recommendations["Feedback"] = df_recommendations["Feedback"].astype(str).str.strip()

    # Standardize boolean indicators
    df_recommendations["Is_Clicked"] = df_recommendations["Clicked?"].str.lower() == "yes"
    df_recommendations["Is_Purchased"] = df_recommendations["Purchased?"].str.lower() == "yes"
    df_recommendations["Is_Not_Relevant"] = df_recommendations["Feedback"].str.lower() == "not relevant"
    df_recommendations["Is_Useful"] = df_recommendations["Feedback"].str.lower() == "useful"
    df_recommendations["Is_No_Feedback"] = df_recommendations["Feedback"].str.strip() == "-"

    # 3. Campaigns Sheet
    df_campaigns = clean_dataframe_columns(pd.read_excel(file_path, sheet_name="RetailCo_Campaigns"))
    df_campaigns["Campaign_ID"] = df_campaigns["Campaign_ID"].astype(str).str.strip()
    df_campaigns["Channel"] = df_campaigns["Channel"].astype(str).str.strip()
    df_campaigns["Segment_Targeted"] = df_campaigns["Segment_Targeted"].astype(str).str.strip()
    df_campaigns["Spend($)"] = pd.to_numeric(df_campaigns["Spend($)"], errors="coerce").fillna(0)
    df_campaigns["CTR(%)"] = pd.to_numeric(df_campaigns["CTR(%)"], errors="coerce").fillna(0.0)
    df_campaigns["Conversion(%)"] = pd.to_numeric(df_campaigns["Conversion(%)"], errors="coerce").fillna(0.0)
    df_campaigns["ROI"] = pd.to_numeric(df_campaigns["ROI"], errors="coerce").fillna(0.0)

    # Net Return estimate
    df_campaigns["Net_Gain_Loss($)"] = df_campaigns["Spend($)"] * df_campaigns["ROI"]
    df_campaigns["Is_Negative_ROI"] = df_campaigns["ROI"] < 0

    # 4. Churn Trend Sheet
    df_churn_trend = clean_dataframe_columns(pd.read_excel(file_path, sheet_name="RetailCo_ChurnTrend"))
    df_churn_trend["Quarter"] = df_churn_trend["Quarter"].astype(str).str.strip()
    df_churn_trend["Customers_Active"] = pd.to_numeric(df_churn_trend["Customers_Active"], errors="coerce")
    df_churn_trend["New_Customers"] = pd.to_numeric(df_churn_trend["New_Customers"], errors="coerce")
    df_churn_trend["Churned_Customers"] = pd.to_numeric(df_churn_trend["Churned_Customers"], errors="coerce")
    df_churn_trend["Churn_%"] = pd.to_numeric(df_churn_trend["Churn_%"], errors="coerce")
    df_churn_trend["Net_Customer_Addition"] = df_churn_trend["New_Customers"] - df_churn_trend["Churned_Customers"]

    # Pre-aggregate Customer Recommendation Profile
    rec_agg = df_recommendations.groupby("Customer_ID").agg(
        Total_Recs=("Recommended_Category", "count"),
        Total_Clicks=("Is_Clicked", "sum"),
        Total_Purchases=("Is_Purchased", "sum"),
        Total_Not_Relevant=("Is_Not_Relevant", "sum"),
        Total_Useful=("Is_Useful", "sum"),
        Total_No_Feedback=("Is_No_Feedback", "sum")
    ).reset_index()

    rec_agg["Customer_CTR(%)"] = (rec_agg["Total_Clicks"] / rec_agg["Total_Recs"] * 100).round(2)
    rec_agg["Customer_Conv(%)"] = (rec_agg["Total_Purchases"] / rec_agg["Total_Recs"] * 100).round(2)
    rec_agg["Customer_Irrelevance(%)"] = (rec_agg["Total_Not_Relevant"] / rec_agg["Total_Recs"] * 100).round(2)

    # Merge aggregated recommendation data into customer dataframe
    df_customers_enriched = df_customers.merge(rec_agg, on="Customer_ID", how="left")
    df_customers_enriched["Total_Recs"] = df_customers_enriched["Total_Recs"].fillna(0).astype(int)
    df_customers_enriched["Total_Clicks"] = df_customers_enriched["Total_Clicks"].fillna(0).astype(int)
    df_customers_enriched["Total_Purchases"] = df_customers_enriched["Total_Purchases"].fillna(0).astype(int)
    df_customers_enriched["Total_Not_Relevant"] = df_customers_enriched["Total_Not_Relevant"].fillna(0).astype(int)
    df_customers_enriched["Total_Useful"] = df_customers_enriched["Total_Useful"].fillna(0).astype(int)
    df_customers_enriched["Total_No_Feedback"] = df_customers_enriched["Total_No_Feedback"].fillna(0).astype(int)
    df_customers_enriched["Has_Recommendations"] = df_customers_enriched["Total_Recs"] > 0

    return {
        "customers": df_customers_enriched,
        "recommendations": df_recommendations,
        "campaigns": df_campaigns,
        "churn_trend": df_churn_trend
    }
