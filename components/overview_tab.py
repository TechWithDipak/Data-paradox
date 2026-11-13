"""
Overview Tab Component.
Displays high-level executive KPIs, quarterly churn trajectory, and cohort summaries
with an upgraded, vibrant multi-color theme.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import COLORS, TIER_COLORS, CITY_COLORS
from analytics import calculate_overview_metrics, compute_segment_churn


def render_overview_tab(df_customers: pd.DataFrame, df_churn_trend: pd.DataFrame, df_campaigns: pd.DataFrame, df_recommendations: pd.DataFrame):
    st.markdown("### Executive Overview & Macro Churn Trajectory")
    st.markdown(
        "A holistic diagnostic view of RetailCo's customer base, quarterly churn escalation from **12.0% to 16.7%**, "
        "and active vs churned customer dynamics."
    )

    metrics = calculate_overview_metrics(df_customers, df_churn_trend)

    # Top Level KPI Row (Macro Churn Trend)
    st.markdown("#### Macro Corporate Trajectory (RetailCo_ChurnTrend)")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.metric(
            label="Latest Churn Rate (Q2-2025)",
            value=f"{metrics['macro_churn_rate']}%",
            delta=f"+{metrics['churn_rate_delta']}% vs Q1-2024",
            delta_color="inverse"
        )
    with kpi_col2:
        st.metric(
            label="Active Customers",
            value=f"{metrics['macro_active']:,}",
            help="Total active customer base reported in Q2-2025"
        )
    with kpi_col3:
        st.metric(
            label="Quarterly Churned Customers",
            value=f"{metrics['macro_churned']:,}",
            delta="+30,000 (+50%) vs Q1-2024",
            delta_color="inverse"
        )
    with kpi_col4:
        net_addition = metrics['macro_new'] - metrics['macro_churned']
        st.metric(
            label="Net Quarterly Customer Flow",
            value=f"{net_addition:,}",
            delta="Customer Deficit (-25,000)" if net_addition < 0 else "Net Growth",
            delta_color="inverse" if net_addition < 0 else "normal",
            help="New Customers (65,000) minus Churned Customers (90,000) in Q2-2025"
        )

    st.markdown("---")

    # Filtered Sample KPI Row
    st.markdown("#### Filtered Customer Sample Health (RetailCo_Customers)")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)

    with s_col1:
        st.metric(
            label="Filtered Sample Size",
            value=f"{metrics['total_sample_cust']}",
            help="Total customers matching current sidebar filter criteria"
        )
    with s_col2:
        st.metric(
            label="Sample Churned Count",
            value=f"{metrics['sample_churned']}",
            delta="Defected",
            delta_color="inverse"
        )
    with s_col3:
        st.metric(
            label="Sample Churn Rate",
            value=f"{metrics['sample_churn_rate']}%",
            delta="High-Risk Cohort" if metrics['sample_churn_rate'] > 25 else "Normal",
            delta_color="inverse" if metrics['sample_churn_rate'] > 25 else "normal"
        )
    with s_col4:
        st.metric(
            label="Sample Retained Count",
            value=f"{metrics['sample_retained']}",
            help="Customers currently retained (Churn_Flag == 'N')"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Macro Churn Trend Chart with Distinct Harmonious Colors
    st.markdown("#### Quarterly Churn & Customer Base Dynamics")
    fig = go.Figure()

    # Active Customers Bar (Slate Indigo with gentle transparency)
    fig.add_trace(
        go.Bar(
            x=df_churn_trend["Quarter"],
            y=df_churn_trend["Customers_Active"],
            name="Active Customers",
            marker=dict(
                color="rgba(37, 99, 235, 0.25)",
                line=dict(color="#2563EB", width=1.5)
            ),
            yaxis="y"
        )
    )

    # Quarterly Churned Customers Bar (Vivid Rose Red)
    fig.add_trace(
        go.Bar(
            x=df_churn_trend["Quarter"],
            y=df_churn_trend["Churned_Customers"],
            name="Quarterly Churned Customers",
            marker=dict(
                color="#F43F5E",
                line=dict(color="#BE123C", width=1.2)
            ),
            yaxis="y"
        )
    )

    # Quarterly New Customers Bar (Vibrant Emerald Green)
    fig.add_trace(
        go.Bar(
            x=df_churn_trend["Quarter"],
            y=df_churn_trend["New_Customers"],
            name="Quarterly New Customers",
            marker=dict(
                color="#10B981",
                line=dict(color="#047857", width=1.2)
            ),
            yaxis="y"
        )
    )

    # Churn Rate Line on Secondary Axis (Luminous Amber / Gold)
    fig.add_trace(
        go.Scatter(
            x=df_churn_trend["Quarter"],
            y=df_churn_trend["Churn_%"],
            name="Churn Rate (%)",
            mode="lines+markers+text",
            text=[f"<b>{v}%</b>" for v in df_churn_trend["Churn_%"]],
            textposition="top center",
            textfont=dict(color="#B45309", size=12),
            line=dict(color="#F59E0B", width=3.5, dash="solid"),
            marker=dict(size=10, color="#D97706", line=dict(color="#FFFFFF", width=2)),
            yaxis="y2"
        )
    )

    fig.update_layout(
        title="<b>Quarterly Trajectory: Customer Churn Surge vs Net Acquisition Deficit</b>",
        barmode="group",
        xaxis=dict(title="Quarter", tickfont=dict(size=12, family="sans-serif")),
        yaxis=dict(
            title="Customer Volume",
            side="left",
            showgrid=True,
            gridcolor="#F1F5F9"
        ),
        yaxis2=dict(
            title="Churn Rate (%)",
            side="right",
            overlaying="y",
            range=[10, 20],
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # Quick Summary Cards with distinct, colorful border and tint styling
    st.markdown("#### High-Level Diagnostic Insights")
    c1, c2, c3 = st.columns(3)

    loyalty_summary = compute_segment_churn(df_customers, "Loyalty_Tier")
    top_churn_tier = loyalty_summary.iloc[0] if len(loyalty_summary) > 0 else None

    loc_summary = compute_segment_churn(df_customers, "Location")
    top_churn_loc = loc_summary.iloc[0] if len(loc_summary) > 0 else None

    with c1:
        st.markdown(
            f"""
            <div style="border-left: 5px solid #F59E0B; background-color: #FFFBEB; padding: 14px 16px; border-radius: 6px; border-top: 1px solid #FEF3C7; border-right: 1px solid #FEF3C7; border-bottom: 1px solid #FEF3C7;">
                <h4 style="margin: 0 0 6px 0; color: #B45309;">Vulnerable Tier: {top_churn_tier['Loyalty_Tier'] if top_churn_tier is not None else 'N/A'}</h4>
                <div style="font-size: 22px; font-weight: 700; color: #92400E; margin-bottom: 4px;">
                    {top_churn_tier['Churn_Rate(%)'] if top_churn_tier is not None else 'N/A'}% Churn Rate
                </div>
                <div style="font-size: 13px; color: #78350F;">
                    ({top_churn_tier['Churned_Customers'] if top_churn_tier is not None else 0}/{top_churn_tier['Total_Customers'] if top_churn_tier is not None else 0} defected)
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: #92400E;">High-margin VIP customers are abandoning the platform at severe rates.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div style="border-left: 5px solid #EF4444; background-color: #FEF2F2; padding: 14px 16px; border-radius: 6px; border-top: 1px solid #FEE2E2; border-right: 1px solid #FEE2E2; border-bottom: 1px solid #FEE2E2;">
                <h4 style="margin: 0 0 6px 0; color: #B91C1C;">Hotspot Hub: {top_churn_loc['Location'] if top_churn_loc is not None else 'N/A'}</h4>
                <div style="font-size: 22px; font-weight: 700; color: #991B1B; margin-bottom: 4px;">
                    {top_churn_loc['Churn_Rate(%)'] if top_churn_loc is not None else 'N/A'}% Churn Rate
                </div>
                <div style="font-size: 13px; color: #7F1D1D;">
                    ({top_churn_loc['Churned_Customers'] if top_churn_loc is not None else 0}/{top_churn_loc['Total_Customers'] if top_churn_loc is not None else 0} defected)
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: #991B1B;">Severe local fulfillment or 3PL delivery friction in Hyderabad.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div style="border-left: 5px solid #8B5CF6; background-color: #F5F3FF; padding: 14px 16px; border-radius: 6px; border-top: 1px solid #EDE9FE; border-right: 1px solid #EDE9FE; border-bottom: 1px solid #EDE9FE;">
                <h4 style="margin: 0 0 6px 0; color: #6D28D9;">Net Deficit: Q2-2025</h4>
                <div style="font-size: 22px; font-weight: 700; color: #5B21B6; margin-bottom: 4px;">
                    -25,000 Customers
                </div>
                <div style="font-size: 13px; color: #4C1D95;">
                    (65,000 New vs 90,000 Churned)
                </div>
                <p style="margin: 8px 0 0 0; font-size: 13px; color: #5B21B6;">RetailCo is in net customer contraction despite the $30M digital investment.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
