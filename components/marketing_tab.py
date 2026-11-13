"""
Marketing Analysis Tab Component.
Analyzes campaign spending, conversion rates, channel ROI, and budget reallocation simulation
using distinct, brand-accurate multi-colored styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, CHANNEL_COLORS
from analytics import analyze_marketing_campaigns, simulate_budget_reallocation


def render_marketing_tab(df_campaigns: pd.DataFrame):
    st.markdown("### Marketing Campaign Performance & Capital Efficiency")
    st.markdown(
        "Evaluating marketing efficiency across **15 campaigns** and **5 channels** from `RetailCo_Campaigns`. "
        "Diagnosing why RetailCo experiences **'flat marketing ROI'** despite spending millions."
    )

    if len(df_campaigns) == 0:
        st.warning("No campaign records match the current filter selection.")
        return

    camp_res = analyze_marketing_campaigns(df_campaigns)

    # Top KPIs
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            label="Total Marketing Spend",
            value=f"${camp_res['total_spend']:,.0f}",
            help="Total campaign budget allocated across 15 initiatives"
        )
    with k2:
        st.metric(
            label="Blended Portfolio ROI",
            value=f"{round(camp_res['blended_roi'] * 100, 2)}%",
            delta=f"${camp_res['total_net_gain_loss']:,.0f} Net Gain",
            delta_color="normal"
        )
    with k3:
        st.metric(
            label="Negative-ROI Capital Burn",
            value=f"${camp_res['neg_spend']:,.0f}",
            delta=f"{camp_res['neg_share']}% of Total Spend",
            delta_color="inverse",
            help="Spend squandered on campaigns yielding negative net returns"
        )
    with k4:
        st.metric(
            label="Negative-ROI Campaigns",
            value=f"{len(camp_res['neg_campaigns'])} / {len(df_campaigns)}",
            delta="Loss-Making",
            delta_color="inverse"
        )

    st.markdown("---")

    # Channel Performance Breakdown with distinct channel colors
    st.markdown("#### Channel Efficiency Matrix: Underfunded Winners vs Overfunded Sinks")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Spend Allocation by Channel ($)**")
        fig_spend = px.pie(
            camp_res["channel_summary"],
            names="Channel",
            values="Total_Spend",
            color="Channel",
            color_discrete_map=CHANNEL_COLORS,
            hole=0.45
        )
        fig_spend.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )
        fig_spend.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=340,
            showlegend=False
        )
        st.plotly_chart(fig_spend, use_container_width=True)
        st.caption("**Concentration Risk**: Instagram & Facebook consume **63.8%** of the entire marketing budget ($1.62M).")

    with col2:
        st.markdown("**Weighted ROI by Channel (%)**")
        channel_names = camp_res["channel_summary"]["Channel"]
        channel_bar_colors = [CHANNEL_COLORS.get(ch, COLORS["secondary"]) for ch in channel_names]

        fig_roi = go.Figure()
        fig_roi.add_trace(
            go.Bar(
                x=channel_names,
                y=camp_res["channel_summary"]["Weighted_ROI"] * 100,
                text=[f"<b>{round(r * 100, 1)}%</b>" for r in camp_res["channel_summary"]["Weighted_ROI"]],
                textposition="auto",
                marker=dict(
                    color=channel_bar_colors,
                    line=dict(color="#1E293B", width=1.2)
                ),
                hovertemplate="<b>Channel</b>: %{x}<br><b>Weighted ROI</b>: %{y}%<extra></extra>"
            )
        )
        fig_roi.update_layout(
            yaxis=dict(title="Weighted ROI (%)"),
            xaxis=dict(title="Marketing Channel"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=20, b=20),
            height=340
        )
        st.plotly_chart(fig_roi, use_container_width=True)
        st.caption("**The Paradox**: **App Push (27.3% - Emerald)** and **SMS (23.0% - Amber)** generate massive ROI but receive only 26% of budget.")

    st.markdown("---")

    # Campaign Scatter Plot (Spend vs ROI vs Conversion)
    st.markdown("#### Campaign Performance Bubble Chart (Spend vs ROI)")
    fig_scatter = px.scatter(
        df_campaigns,
        x="Spend($)",
        y="ROI",
        size="Conversion(%)",
        color="Channel",
        text="Campaign_ID",
        hover_data=["Segment_Targeted", "CTR(%)", "Conversion(%)"],
        title="<b>Spend vs ROI (Bubble Size = Conversion %) — Distinct Channel Color Coding</b>",
        color_discrete_map=CHANNEL_COLORS
    )
    fig_scatter.add_hline(y=0.0, line_dash="dash", line_color="#EF4444", annotation_text="Break-even Line (ROI = 0.0)")
    fig_scatter.update_traces(
        textposition="top center",
        marker=dict(line=dict(color="#1E293B", width=1))
    )
    fig_scatter.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Section 3: Negative ROI Audit Table
    st.markdown("#### Negative-ROI Leakage Audit: The 4 Value-Destroying Campaigns")
    st.dataframe(
        camp_res["neg_campaigns"][[
            "Campaign_ID", "Channel", "Spend($)", "Segment_Targeted", "CTR(%)", "Conversion(%)", "ROI", "Net_Gain_Loss($)"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Section 4: Interactive Capital Reallocation Simulator
    st.markdown("#### Interactive Budget Reallocation Simulator")
    st.markdown(
        "Demonstrate to faculty how RetailCo can immediately recover profitability by shifting capital from "
        "low-ROI social media acquisition to high-ROI direct retention channels (App Push & SMS)."
    )

    sim_col1, sim_col2 = st.columns([1, 2])

    with sim_col1:
        shift_val = st.slider(
            label="Shift Budget from FB/IG to App Push & SMS ($):",
            min_value=50000,
            max_value=600000,
            value=350000,
            step=25000,
            format="$%d"
        )

        sim_res = simulate_budget_reallocation(df_campaigns, float(shift_val))

    with sim_col2:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(
                label="Projected Portfolio ROI",
                value=f"{sim_res['projected_roi']}%",
                delta=f"+{sim_res['roi_delta_bps']:.0f} bps",
                delta_color="normal"
            )
        with m2:
            st.metric(
                label="Net Incremental Cash Gain",
                value=f"+${sim_res['net_improvement']:,.0f}",
                help="Direct profit gained from higher-yielding channels"
            )
        with m3:
            st.metric(
                label="Total Portfolio Net Gain",
                value=f"${sim_res['projected_total_gain']:,.0f}",
                delta=f"vs ${sim_res['curr_gain']:,.0f} baseline",
                delta_color="normal"
            )

        st.markdown(
            f"""
            <div style="border-left: 5px solid #10B981; background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%); padding: 14px 16px; border-radius: 6px; margin-top: 12px; border: 1px solid #A7F3D0;">
                <strong style="color: #065F46;">Executive Action Summary:</strong><br>
                <span style="color: #047857; font-size: 13.5px;">
                    By reallocating <strong>${shift_val:,}</strong> away from loss-making Facebook & Instagram campaigns
                    and deploying it into App Push & SMS retention loops, RetailCo immediately lifts portfolio ROI from
                    <strong>{sim_res['curr_roi']}%</strong> to <strong>{sim_res['projected_roi']}%</strong>, generating
                    <strong>+${sim_res['net_improvement']:,.0f} in new net profit</strong> without adding any budget!
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
