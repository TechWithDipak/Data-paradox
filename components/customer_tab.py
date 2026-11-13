"""
Customer Analysis Tab Component.
Provides deep-dive churn segmentation across Loyalty Tier, Gender, Location, and Age
using distinct, vibrant, high-contrast color styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, CITY_COLORS, TIER_COLORS, GENDER_COLORS, AGE_COLORS
from analytics import compute_segment_churn, compute_crosstab_churn


def render_customer_tab(df_customers: pd.DataFrame):
    st.markdown("### Customer Demographic & Segmentation Analysis")
    st.markdown(
        "Investigating churn risk across **Loyalty Tier**, **Geographic Location**, "
        "**Gender**, and **Age Cohorts** using distinct, multi-colored visual mapping."
    )

    if len(df_customers) == 0:
        st.warning("No customers match the current filter selection.")
        return

    # Section 1: Loyalty Tier & Location Breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Churn by Loyalty Tier")
        loyalty_df = compute_segment_churn(df_customers, "Loyalty_Tier")

        fig_tier = go.Figure()
        fig_tier.add_trace(
            go.Bar(
                x=loyalty_df["Loyalty_Tier"],
                y=loyalty_df["Churn_Rate(%)"],
                text=[f"<b>{v}%</b><br>({c}/{t})" for v, c, t in zip(
                    loyalty_df["Churn_Rate(%)"],
                    loyalty_df["Churned_Customers"],
                    loyalty_df["Total_Customers"]
                )],
                textposition="auto",
                marker=dict(
                    color=[TIER_COLORS.get(t, COLORS["secondary"]) for t in loyalty_df["Loyalty_Tier"]],
                    line=dict(color="#1E293B", width=1.2)
                ),
                hovertemplate="<b>Tier</b>: %{x}<br><b>Churn Rate</b>: %{y}%<extra></extra>"
            )
        )
        fig_tier.update_layout(
            yaxis=dict(title="Churn Rate (%)", range=[0, max(50, loyalty_df["Churn_Rate(%)"].max() + 10)]),
            xaxis=dict(title="Loyalty Tier", tickfont=dict(size=12, family="sans-serif")),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=30, b=30),
            height=340
        )
        st.plotly_chart(fig_tier, use_container_width=True)

        st.caption(
            "**Key Insight**: **Gold tier churn is 42.1%** (Amber) and **Silver is 37.1%** (Slate), "
            "more than double **Bronze at 19.6%** (Copper). High-value VIP customers are abandoning RetailCo at severe rates."
        )

    with col2:
        st.markdown("#### Churn by Geographic Location (City Hubs)")
        loc_df = compute_segment_churn(df_customers, "Location")

        # Distinct custom color for every individual city
        city_bar_colors = [CITY_COLORS.get(loc, COLORS["secondary"]) for loc in loc_df["Location"]]

        fig_loc = go.Figure()
        fig_loc.add_trace(
            go.Bar(
                x=loc_df["Location"],
                y=loc_df["Churn_Rate(%)"],
                text=[f"<b>{v}%</b><br>({c}/{t})" for v, c, t in zip(
                    loc_df["Churn_Rate(%)"],
                    loc_df["Churned_Customers"],
                    loc_df["Total_Customers"]
                )],
                textposition="auto",
                marker=dict(
                    color=city_bar_colors,
                    line=dict(color="#1E293B", width=1.2)
                ),
                hovertemplate="<b>City</b>: %{x}<br><b>Churn Rate</b>: %{y}%<extra></extra>"
            )
        )
        fig_loc.update_layout(
            yaxis=dict(title="Churn Rate (%)", range=[0, max(55, loc_df["Churn_Rate(%)"].max() + 10)]),
            xaxis=dict(title="City / Hub", tickfont=dict(size=12, family="sans-serif")),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=30, b=30),
            height=340
        )
        st.plotly_chart(fig_loc, use_container_width=True)

        st.caption(
            "**Geographic Hotspots**: **Hyderabad (45.8% - Crimson)** has nearly 1 in 2 defecting, "
            "followed by **Chennai (30.0% - Orange)** and **Bangalore (26.1% - Cyan)**. "
            "**Mumbai (18.8% - Emerald)** retains best."
        )

    st.markdown("---")

    # Section 2: Gender & Age Cohort Breakdown
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Churn by Gender")
        gender_df = compute_segment_churn(df_customers, "Gender")

        gender_bar_colors = [GENDER_COLORS.get(g, COLORS["secondary"]) for g in gender_df["Gender"]]

        fig_gender = go.Figure()
        fig_gender.add_trace(
            go.Bar(
                x=gender_df["Gender"].map({"M": "Male Shoppers (M)", "F": "Female Shoppers (F)"}),
                y=gender_df["Churn_Rate(%)"],
                text=[f"<b>{v}%</b><br>({c}/{t})" for v, c, t in zip(
                    gender_df["Churn_Rate(%)"],
                    gender_df["Churned_Customers"],
                    gender_df["Total_Customers"]
                )],
                textposition="auto",
                marker=dict(
                    color=gender_bar_colors,
                    line=dict(color="#1E293B", width=1.2)
                ),
                hovertemplate="<b>Gender</b>: %{x}<br><b>Churn Rate</b>: %{y}%<extra></extra>"
            )
        )
        fig_gender.update_layout(
            yaxis=dict(title="Churn Rate (%)", range=[0, 45]),
            xaxis=dict(title="Gender Group"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=30, b=30),
            height=320
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        st.caption(
            "**Gender Gap**: **Male shoppers churn at 35.7%** (Blue) vs **22.7% for Female shoppers** (Magenta). "
            "Men represent 66.7% of all churned customers in the sample."
        )

    with col4:
        st.markdown("#### Churn by Age Cohort")
        age_df = compute_segment_churn(df_customers, "Age_Group")

        # Distinct progressive colors for each age cohort
        age_bar_colors = [AGE_COLORS.get(str(ag), COLORS["primary"]) for ag in age_df["Age_Group"]]

        fig_age = go.Figure()
        fig_age.add_trace(
            go.Bar(
                x=age_df["Age_Group"].astype(str),
                y=age_df["Churn_Rate(%)"],
                text=[f"<b>{v}%</b><br>({c}/{t})" for v, c, t in zip(
                    age_df["Churn_Rate(%)"],
                    age_df["Churned_Customers"],
                    age_df["Total_Customers"]
                )],
                textposition="auto",
                marker=dict(
                    color=age_bar_colors,
                    line=dict(color="#1E293B", width=1.2)
                ),
                hovertemplate="<b>Age Cohort</b>: %{x}<br><b>Churn Rate</b>: %{y}%<extra></extra>"
            )
        )
        fig_age.update_layout(
            yaxis=dict(title="Churn Rate (%)", range=[0, 45]),
            xaxis=dict(title="Age Cohort"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=30, b=30),
            height=320
        )
        st.plotly_chart(fig_age, use_container_width=True)

        st.caption(
            "**Cohort Profile**: Core career professionals in the **26-35 (Blue)** and **36-45 (Violet)** "
            "brackets experience elevated churn, correlating with higher digital service expectations."
        )

    st.markdown("---")

    # Section 3: Bivariate Cross-Tabulation Heatmap (Location x Loyalty Tier)
    st.markdown("#### Cross-Segmentation Heatmap: Churn Rate (%) by Location & Loyalty Tier")
    cross_df = compute_crosstab_churn(df_customers, "Location", "Loyalty_Tier")

    if not cross_df.empty:
        # Elegant multi-step perceptual color palette (Peach to Crimson to Burgundy)
        custom_diverging_scale = [
            [0.0, "#F0FDF4"],   # Low churn: Soft Mint White
            [0.25, "#FEF08A"],  # Low-mid: Soft Yellow
            [0.5, "#FDBA74"],   # Mid: Warm Peach
            [0.75, "#F87171"],  # High: Coral Red
            [1.0, "#991B1B"]    # Extreme: Deep Crimson
        ]

        fig_heat = px.imshow(
            cross_df,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=custom_diverging_scale,
            labels=dict(x="Loyalty Tier", y="City Location", color="Churn %"),
            title="<b>Intersection Matrix: Churn Risk by City and Loyalty Tier</b>"
        )
        fig_heat.update_traces(
            texttemplate="<b>%{z:.1f}%</b>",
            textfont=dict(size=13)
        )
        fig_heat.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=360,
            margin=dict(l=40, r=40, t=50, b=30)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # Section 4: Interactive Customer Explorer Table
    with st.expander("View & Search Individual Customer Records", expanded=False):
        st.dataframe(
            df_customers[[
                "Customer_ID", "Age", "Gender", "Location", "Loyalty_Tier",
                "Last_Purchase_Date", "Churn_Flag", "Total_Recs", "Customer_CTR(%)", "Customer_Irrelevance(%)"
            ]],
            use_container_width=True,
            hide_index=True
        )

        csv_data = df_customers.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Customer Dataset as CSV",
            data=csv_data,
            file_name="RetailCo_Filtered_Customers.csv",
            mime="text/csv"
        )
