"""
AI Recommendation Analysis Tab Component.
Investigates recommendation clicks, purchases, irrelevance, and context/gender mismatches
using rich multi-colored categorical visual styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, CATEGORY_COLORS, GENDER_COLORS
from analytics import analyze_recommendations


def render_recommendation_tab(df_recommendations: pd.DataFrame, df_customers: pd.DataFrame):
    st.markdown("### AI Recommendation Engine Performance Audit")
    st.markdown(
        "Evaluating RetailCo's **$30 Million AI Personalization Engine** using interaction logs from "
        "`RetailCo_Recommendations`. Assessing click-through rates, purchase conversions, and "
        "the critical **irrelevance rate** that eroded management trust."
    )

    rec_res = analyze_recommendations(df_recommendations, df_customers)
    if not rec_res:
        st.warning("No recommendation records found.")
        return

    # Section 1: KPI Summary Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            label="Total Recommendations Delivered",
            value=f"{rec_res['total_recs']}",
            help="Total AI recommendations delivered to customers in sample"
        )
    with kpi2:
        st.metric(
            label="Click-Through Rate (CTR)",
            value=f"{rec_res['ctr']}%",
            delta=f"{rec_res['total_clicks']} Clicks",
            delta_color="normal"
        )
    with kpi3:
        st.metric(
            label="Purchase Conversion Rate",
            value=f"{rec_res['purchase_rate']}%",
            delta=f"{rec_res['total_purchases']} Purchases",
            delta_color="normal"
        )
    with kpi4:
        st.metric(
            label="Irrelevance Rate",
            value=f"{rec_res['irrelevance_rate']}%",
            delta="78 Flagged 'Not Relevant'",
            delta_color="inverse",
            help="Percentage of recommendations explicitly marked as 'Not relevant' by shoppers"
        )

    st.markdown("---")

    # Section 2: Conversion Funnel & Feedback Sentiment
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### AI Recommendation Engagement Funnel")
        funnel_fig = go.Figure(
            go.Funnel(
                y=["Delivered Recommendations", "Clicked Recommendations", "Completed Purchases"],
                x=[rec_res["total_recs"], rec_res["total_clicks"], rec_res["total_purchases"]],
                textinfo="value+percent initial",
                marker=dict(
                    color=["#312E81", "#0284C7", "#10B981"],
                    line=dict(color="#1E293B", width=1.5)
                )
            )
        )
        funnel_fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=340
        )
        st.plotly_chart(funnel_fig, use_container_width=True)
        st.caption(
            "**Conversion Drop-off**: Out of 200 recommendations, only 34 led to purchases (17.0% overall conversion). "
            "Even among users who clicked (84), fewer than half completed a transaction."
        )

    with col2:
        st.markdown("#### Recommendation Feedback Sentiment")
        labels = ["Useful", "Not Relevant", "No Feedback (-)"]
        values = [
            rec_res["useful_rate"],
            rec_res["irrelevance_rate"],
            rec_res["no_feedback_rate"]
        ]
        sentiment_colors = ["#10B981", "#EF4444", "#94A3B8"]

        pie_fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.48,
                marker=dict(
                    colors=sentiment_colors,
                    line=dict(color="#FFFFFF", width=2)
                ),
                textinfo="label+percent",
                textfont=dict(size=12, family="sans-serif")
            )]
        )
        pie_fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=340,
            showlegend=False
        )
        st.plotly_chart(pie_fig, use_container_width=True)
        st.caption(
            "**Trust Deficit**: Almost 4 out of 10 recommendations (**39.0% - Crimson**) are actively rejected by customers as 'Not relevant'. "
            "Adding unrated recommendations, **58.5% failed to be confirmed useful**."
        )

    st.markdown("---")

    # Section 3: The Critical AI Failure – Gender Mismatch & Catalog Hallucination
    st.markdown("#### Deep Dive: The Data Paradox & Context Hallucination")
    st.markdown(
        "A primary finding from the case study is that *'Managers increasingly bypass the available tools "
        "because they do not trust the AI-generated insights.'* The data reveals why: "
        "the recommendation engine lacks basic business guardrails and gender-context awareness."
    )

    alert_col1, alert_col2 = st.columns([1, 2])

    with alert_col1:
        st.markdown(
            f"""
            <div style="border-left: 6px solid #EF4444; background: linear-gradient(135deg, #FEF2F2 0%, #FFF1F2 100%); padding: 18px; border-radius: 8px; border-top: 1px solid #FECDD3; border-right: 1px solid #FECDD3; border-bottom: 1px solid #FECDD3;">
                <h4 style="color: #9F1239; margin-top: 0; margin-bottom: 8px;">Critical Context Breakdown</h4>
                <div style="font-size: 17px; font-weight: 700; color: #BE123C; margin-bottom: 8px;">
                    Sarees Recommended to Men
                </div>
                <ul style="font-size: 13.5px; color: #881337; margin: 0; padding-left: 18px; line-height: 1.6;">
                    <li><strong>21 Sarees</strong> were recommended directly to Male shoppers.</li>
                    <li><strong>{rec_res['sarees_to_men_not_rel']} of 21</strong> were explicitly rejected as 'Not relevant'.</li>
                    <li>Saree was the <em>#1 most recommended</em> item to men, ahead of Kurtas (15) and T-Shirts (14)!</li>
                </ul>
                <p style="margin-top: 10px; margin-bottom: 0; font-size: 12.5px; color: #9F1239; font-style: italic;">
                    This catastrophic catalog mismatch explains why business managers lost faith in AI insights.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with alert_col2:
        st.markdown("**Product Category Distribution by Customer Gender**")
        gender_cat_df = rec_res["gender_cat_matrix"].reset_index()

        fig_gcat = go.Figure()
        fig_gcat.add_trace(
            go.Bar(
                x=gender_cat_df["Recommended_Category"],
                y=gender_cat_df["M"],
                name="Men (M)",
                marker=dict(color=GENDER_COLORS["M"], line=dict(color="#1E293B", width=1))
            )
        )
        fig_gcat.add_trace(
            go.Bar(
                x=gender_cat_df["Recommended_Category"],
                y=gender_cat_df["F"],
                name="Women (F)",
                marker=dict(color=GENDER_COLORS["F"], line=dict(color="#1E293B", width=1))
            )
        )
        fig_gcat.update_layout(
            barmode="group",
            xaxis=dict(title="Recommended Product Category"),
            yaxis=dict(title="Recommendation Volume"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=20, b=20),
            height=320
        )
        st.plotly_chart(fig_gcat, use_container_width=True)

    st.markdown("---")

    # Section 4: Product Category Performance Chart
    st.markdown("#### Category-by-Category Recommendation Volume & Conversion")
    cat_df = rec_res["category_summary"]

    cat_bar_colors = [CATEGORY_COLORS.get(cat, COLORS["secondary"]) for cat in cat_df["Recommended_Category"]]

    fig_cat_vol = go.Figure()
    fig_cat_vol.add_trace(
        go.Bar(
            x=cat_df["Recommended_Category"],
            y=cat_df["Total_Recs"],
            name="Delivered Volume",
            text=[f"<b>{t} recs</b><br>(CTR: {ctr}%)" for t, ctr in zip(cat_df["Total_Recs"], cat_df["CTR(%)"])],
            textposition="auto",
            marker=dict(color=cat_bar_colors, line=dict(color="#1E293B", width=1.2))
        )
    )
    fig_cat_vol.update_layout(
        xaxis=dict(title="Product Category"),
        yaxis=dict(title="Total Recommendations Delivered"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=20, b=20),
        height=320
    )
    st.plotly_chart(fig_cat_vol, use_container_width=True)

    # Detailed Table
    st.markdown("#### Product Category Performance Matrix")
    st.dataframe(
        cat_df,
        use_container_width=True,
        hide_index=True
    )

    # Section 5: Unserved Customers Audit
    unserved_count = (df_customers["Total_Recs"] == 0).sum()
    st.info(
        f"**Cold Start & Coverage Gap**: **{unserved_count} out of {len(df_customers)} customers** "
        f"({round(unserved_count / len(df_customers) * 100, 1)}%) received zero AI recommendations in this cycle, "
        f"including premium Gold and Silver tier members."
    )
