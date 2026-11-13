"""
Analytics and Statistical Engine for RetailCo Churn Analysis System.
Provides rigorous calculations, segmentation cuts, cross-tabulations, and hypothesis testing.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from scipy import stats


def calculate_overview_metrics(df_customers: pd.DataFrame, df_churn_trend: pd.DataFrame) -> Dict[str, Any]:
    """Computes headline macro KPIs and sample-level KPIs."""
    # Macro Trend KPIs (from RetailCo_ChurnTrend)
    latest_trend = df_churn_trend.iloc[-1]
    baseline_trend = df_churn_trend.iloc[0]
    
    macro_active = latest_trend["Customers_Active"]
    macro_churned = latest_trend["Churned_Customers"]
    macro_new = latest_trend["New_Customers"]
    macro_churn_rate = latest_trend["Churn_%"]
    
    baseline_churn_rate = baseline_trend["Churn_%"]
    churn_rate_delta = macro_churn_rate - baseline_churn_rate

    # Sample-level KPIs (from filtered df_customers)
    total_sample_cust = len(df_customers)
    if total_sample_cust > 0:
        sample_churned = (df_customers["Churn_Flag"] == "Y").sum()
        sample_retained = (df_customers["Churn_Flag"] == "N").sum()
        sample_churn_rate = round((sample_churned / total_sample_cust) * 100, 2)
    else:
        sample_churned = 0
        sample_retained = 0
        sample_churn_rate = 0.0

    return {
        "macro_active": macro_active,
        "macro_churned": macro_churned,
        "macro_new": macro_new,
        "macro_churn_rate": macro_churn_rate,
        "baseline_churn_rate": baseline_churn_rate,
        "churn_rate_delta": round(churn_rate_delta, 2),
        "total_sample_cust": total_sample_cust,
        "sample_churned": sample_churned,
        "sample_retained": sample_retained,
        "sample_churn_rate": sample_churn_rate
    }


def compute_segment_churn(df_customers: pd.DataFrame, segment_col: str) -> pd.DataFrame:
    """
    Computes churn rate, total customers, churned count, and retained count for any segment column.
    """
    if segment_col not in df_customers.columns or len(df_customers) == 0:
        return pd.DataFrame()

    grouped = df_customers.groupby(segment_col).agg(
        Total_Customers=("Customer_ID", "count"),
        Churned_Customers=("Churn_Flag", lambda s: (s == "Y").sum()),
        Retained_Customers=("Churn_Flag", lambda s: (s == "N").sum())
    ).reset_index()

    grouped["Churn_Rate(%)"] = (grouped["Churned_Customers"] / grouped["Total_Customers"] * 100).round(2)
    grouped["Retention_Rate(%)"] = (100 - grouped["Churn_Rate(%)"]).round(2)
    grouped["Segment_Share(%)"] = (grouped["Total_Customers"] / grouped["Total_Customers"].sum() * 100).round(2)
    grouped = grouped.sort_values(by="Churn_Rate(%)", ascending=False)
    return grouped


def compute_crosstab_churn(df_customers: pd.DataFrame, row_col: str, col_col: str) -> pd.DataFrame:
    """Computes a pivot matrix showing churn rate by two intersecting dimensions."""
    if row_col not in df_customers.columns or col_col not in df_customers.columns or len(df_customers) == 0:
        return pd.DataFrame()

    pivot = df_customers.pivot_table(
        index=row_col,
        columns=col_col,
        values="Churn_Flag",
        aggfunc=lambda s: round((s == "Y").mean() * 100, 1),
        fill_value=0.0
    )
    return pivot


def analyze_recommendations(df_rec: pd.DataFrame, df_cust: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes the AI recommendation log and evaluates category-gender mismatch."""
    total_recs = len(df_rec)
    if total_recs == 0:
        return {}

    total_clicks = df_rec["Is_Clicked"].sum()
    total_purchases = df_rec["Is_Purchased"].sum()
    total_not_relevant = df_rec["Is_Not_Relevant"].sum()
    total_useful = df_rec["Is_Useful"].sum()
    total_no_feedback = df_rec["Is_No_Feedback"].sum()

    ctr = round((total_clicks / total_recs) * 100, 2)
    purchase_rate = round((total_purchases / total_recs) * 100, 2)
    click_to_purchase_rate = round((total_purchases / total_clicks * 100), 2) if total_clicks > 0 else 0.0
    irrelevance_rate = round((total_not_relevant / total_recs) * 100, 2)
    useful_rate = round((total_useful / total_recs) * 100, 2)
    no_feedback_rate = round((total_no_feedback / total_recs) * 100, 2)

    # Category performance
    cat_summary = df_rec.groupby("Recommended_Category").agg(
        Total_Recs=("Customer_ID", "count"),
        Clicks=("Is_Clicked", "sum"),
        Purchases=("Is_Purchased", "sum"),
        Not_Relevant=("Is_Not_Relevant", "sum"),
        Useful=("Is_Useful", "sum"),
        No_Feedback=("Is_No_Feedback", "sum")
    ).reset_index()

    cat_summary["CTR(%)"] = (cat_summary["Clicks"] / cat_summary["Total_Recs"] * 100).round(2)
    cat_summary["Conversion(%)"] = (cat_summary["Purchases"] / cat_summary["Total_Recs"] * 100).round(2)
    cat_summary["Irrelevance(%)"] = (cat_summary["Not_Relevant"] / cat_summary["Total_Recs"] * 100).round(2)
    cat_summary = cat_summary.sort_values(by="Total_Recs", ascending=False)

    # Merge with customers for gender and loyalty analysis
    merged_rec = df_rec.merge(df_cust[["Customer_ID", "Gender", "Loyalty_Tier", "Location", "Churn_Flag"]], on="Customer_ID", how="left")

    # Gender vs Category cross-tab
    gender_cat = pd.crosstab(merged_rec["Recommended_Category"], merged_rec["Gender"])

    # Sarees to Men audit
    sarees_to_men = merged_rec[(merged_rec["Recommended_Category"] == "Sarees") & (merged_rec["Gender"] == "M")]
    sarees_to_men_count = len(sarees_to_men)
    sarees_to_men_not_rel = sarees_to_men["Is_Not_Relevant"].sum()
    sarees_to_men_useful = sarees_to_men["Is_Useful"].sum()

    # Feedback by Gender
    feedback_by_gender = pd.crosstab(merged_rec["Feedback"], merged_rec["Gender"], normalize="columns") * 100

    return {
        "total_recs": total_recs,
        "total_clicks": total_clicks,
        "total_purchases": total_purchases,
        "ctr": ctr,
        "purchase_rate": purchase_rate,
        "click_to_purchase_rate": click_to_purchase_rate,
        "irrelevance_rate": irrelevance_rate,
        "useful_rate": useful_rate,
        "no_feedback_rate": no_feedback_rate,
        "category_summary": cat_summary,
        "gender_cat_matrix": gender_cat,
        "sarees_to_men_count": sarees_to_men_count,
        "sarees_to_men_not_rel": sarees_to_men_not_rel,
        "sarees_to_men_useful": sarees_to_men_useful,
        "feedback_by_gender": feedback_by_gender.round(2),
        "merged_rec": merged_rec
    }


def analyze_marketing_campaigns(df_camp: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes campaign ROI, channel effectiveness, and negative ROI leakages."""
    total_spend = df_camp["Spend($)"].sum()
    total_net_gain_loss = df_camp["Net_Gain_Loss($)"].sum()
    blended_roi = round(total_net_gain_loss / total_spend, 4) if total_spend > 0 else 0.0

    # Negative ROI audit
    neg_campaigns = df_camp[df_camp["Is_Negative_ROI"]].sort_values(by="ROI", ascending=True)
    neg_spend = neg_campaigns["Spend($)"].sum()
    neg_share = round((neg_spend / total_spend) * 100, 2) if total_spend > 0 else 0.0

    # Channel summary
    channel_summary = df_camp.groupby("Channel").agg(
        Campaign_Count=("Campaign_ID", "count"),
        Total_Spend=("Spend($)", "sum"),
        Avg_CTR=("CTR(%)", "mean"),
        Avg_Conversion=("Conversion(%)", "mean"),
        Weighted_ROI=("Net_Gain_Loss($)", lambda s: round(s.sum() / df_camp.loc[s.index, "Spend($)"].sum(), 4)),
        Total_Net_Return=("Net_Gain_Loss($)", "sum")
    ).reset_index()

    channel_summary["Spend_Share(%)"] = (channel_summary["Total_Spend"] / total_spend * 100).round(2)
    channel_summary["Avg_CTR"] = channel_summary["Avg_CTR"].round(2)
    channel_summary["Avg_Conversion"] = channel_summary["Avg_Conversion"].round(2)
    channel_summary = channel_summary.sort_values(by="Total_Spend", ascending=False)

    # Segment summary
    segment_summary = df_camp.groupby("Segment_Targeted").agg(
        Campaign_Count=("Campaign_ID", "count"),
        Total_Spend=("Spend($)", "sum"),
        Avg_CTR=("CTR(%)", "mean"),
        Avg_Conversion=("Conversion(%)", "mean"),
        Weighted_ROI=("Net_Gain_Loss($)", lambda s: round(s.sum() / df_camp.loc[s.index, "Spend($)"].sum(), 4)),
        Total_Net_Return=("Net_Gain_Loss($)", "sum")
    ).reset_index()

    segment_summary["Spend_Share(%)"] = (segment_summary["Total_Spend"] / total_spend * 100).round(2)
    segment_summary["Avg_CTR"] = segment_summary["Avg_CTR"].round(2)
    segment_summary["Avg_Conversion"] = segment_summary["Avg_Conversion"].round(2)
    segment_summary = segment_summary.sort_values(by="Total_Spend", ascending=False)

    return {
        "total_spend": total_spend,
        "total_net_gain_loss": total_net_gain_loss,
        "blended_roi": blended_roi,
        "neg_campaigns": neg_campaigns,
        "neg_spend": neg_spend,
        "neg_share": neg_share,
        "channel_summary": channel_summary,
        "segment_summary": segment_summary
    }


def run_statistical_tests(df_cust: pd.DataFrame) -> Dict[str, Any]:
    """Runs Chi-Square tests to evaluate statistical dependency on Churn."""
    results = {}

    for col in ["Loyalty_Tier", "Location", "Gender"]:
        contingency = pd.crosstab(df_cust[col], df_cust["Churn_Flag"])
        if contingency.shape[0] > 1 and contingency.shape[1] > 1:
            chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
            results[col] = {
                "chi2": round(chi2, 3),
                "p_value": round(p_val, 4),
                "significant": p_val < 0.10,  # Alpha = 0.10 for exploratory sample
                "dof": dof,
                "table": contingency
            }

    # Test recommendation counts and irrelevance rate between churned and retained
    churned_recs = df_cust[df_cust["Churn_Flag"] == "Y"]["Customer_Irrelevance(%)"].dropna()
    retained_recs = df_cust[df_cust["Churn_Flag"] == "N"]["Customer_Irrelevance(%)"].dropna()

    if len(churned_recs) > 0 and len(retained_recs) > 0:
        t_stat, t_pval = stats.ttest_ind(churned_recs, retained_recs, equal_var=False)
        results["Irrelevance_vs_Churn"] = {
            "t_stat": round(t_stat, 3),
            "p_value": round(t_pval, 4),
            "significant": t_pval < 0.05,
            "mean_churned": round(churned_recs.mean(), 2),
            "mean_retained": round(retained_recs.mean(), 2)
        }

    return results


def simulate_budget_reallocation(df_camp: pd.DataFrame, shift_amount: float = 300000.0) -> Dict[str, Any]:
    """
    Simulates shifting marketing budget from low-ROI channels (FB/IG) to high-ROI channels (App Push/SMS).
    """
    total_spend = df_camp["Spend($)"].sum()
    curr_gain = df_camp["Net_Gain_Loss($)"].sum()
    curr_roi = curr_gain / total_spend if total_spend > 0 else 0.0

    fb_ig = df_camp[df_camp["Channel"].isin(["Facebook", "Instagram"])]
    push_sms = df_camp[df_camp["Channel"].isin(["App Push", "SMS"])]

    avg_fb_ig_roi = fb_ig["Net_Gain_Loss($)"].sum() / fb_ig["Spend($)"].sum()
    avg_push_sms_roi = push_sms["Net_Gain_Loss($)"].sum() / push_sms["Spend($)"].sum()

    lost_return_from_shift = shift_amount * avg_fb_ig_roi
    gained_return_from_shift = shift_amount * avg_push_sms_roi
    net_improvement = gained_return_from_shift - lost_return_from_shift
    projected_total_gain = curr_gain + net_improvement
    projected_roi = projected_total_gain / total_spend

    return {
        "shift_amount": shift_amount,
        "curr_roi": round(curr_roi * 100, 2),
        "curr_gain": round(curr_gain, 2),
        "avg_fb_ig_roi": round(avg_fb_ig_roi * 100, 2),
        "avg_push_sms_roi": round(avg_push_sms_roi * 100, 2),
        "net_improvement": round(net_improvement, 2),
        "projected_total_gain": round(projected_total_gain, 2),
        "projected_roi": round(projected_roi * 100, 2),
        "roi_delta_bps": round((projected_roi - curr_roi) * 10000, 0)
    }


def simulate_churn_reduction_impact(df_churn_trend: pd.DataFrame, target_churn_pct: float = 12.0, avg_annual_arpu: float = 180.0) -> Dict[str, Any]:
    """
    Simulates reducing churn from current rate to target baseline (12%) in terms of retained customers and revenue saved.
    """
    latest = df_churn_trend.iloc[-1]
    active_base = latest["Customers_Active"]
    current_churn_pct = latest["Churn_%"]
    current_churned = latest["Churned_Customers"]

    target_churned = int(active_base * (target_churn_pct / 100.0))
    retained_per_quarter = max(0, current_churned - target_churned)
    annualized_retained = retained_per_quarter * 4
    annual_revenue_saved = annualized_retained * avg_annual_arpu

    return {
        "current_churn_pct": current_churn_pct,
        "target_churn_pct": target_churn_pct,
        "retained_per_quarter": retained_per_quarter,
        "annualized_retained": annualized_retained,
        "annual_revenue_saved": annual_revenue_saved,
        "active_base": active_base
    }
