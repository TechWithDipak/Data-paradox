"""
Final Findings and Strategic Recommendations Tab Component.
Synthesizes the #1 critical business problem, 80/20 driver ranking, two-speed action plan,
and revenue recovery simulation with vibrant, executive visual styling.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS
from analytics import simulate_churn_reduction_impact


def render_findings_tab(df_churn_trend: pd.DataFrame, df_campaigns: pd.DataFrame, df_customers: pd.DataFrame):
    st.markdown("### Strategic Synthesis & Executive Action Plan")
    st.markdown(
        "Directly answering the assigned question: **'Validate the major branches using the available dataset "
        "and identify the most critical business problem that RetailCo should address first.'**"
    )

    # Section 1: The #1 Critical Business Problem Callout with Executive Theme
    st.markdown(
        r"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 45%, #312E81 100%); color: white; padding: 24px; border-radius: 10px; border-left: 8px solid #F59E0B; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="background-color: #F59E0B; color: #1E1B4B; padding: 3px 10px; border-radius: 12px; font-weight: 700; font-size: 13px;">CORE VERDICT</span>
                <span style="font-size: 19px; font-weight: 700; color: #F8FAFC;">The #1 Critical Business Problem RetailCo Must Address First</span>
            </div>
            <p style="font-size: 15px; line-height: 1.6; color: #E2E8F0; margin-top: 10px;">
                <strong>RetailCo is facing a catastrophic High-Value VIP Attrition Crisis (Gold Tier 42.1% Churn) and Regional Fulfillment Collapse in Hyderabad (45.8% Churn), exacerbated by $1.62M poured into saturated negative-ROI social ads and an unconstrained AI recommendation engine that destroyed internal management trust.</strong>
            </p>
            <div style="background-color: rgba(255, 255, 255, 0.08); padding: 14px 18px; border-radius: 6px; margin-top: 14px; border: 1px solid rgba(255, 255, 255, 0.15);">
                <div style="font-weight: 600; color: #FDE68A; margin-bottom: 6px; font-size: 14px;">Why RetailCo Must Solve This First:</div>
                <ul style="font-size: 13.5px; color: #CBD5E1; margin: 0; padding-left: 18px; line-height: 1.6;">
                    <li><strong style="color: #F8FAFC;">Asymmetric LTV Destruction</strong>: Gold tier members generate over 60% of recurring profit. Losing 42.1% of Gold members drains profits that cannot be recovered by acquiring low-value Bronze shoppers.</li>
                    <li><strong style="color: #F8FAFC;">Regional Fulfillment Breakdown</strong>: Hyderabad (45.8% churn) points to acute courier SLA and fulfillment failures that require immediate operational fixes.</li>
                    <li><strong style="color: #F8FAFC;">The $640k Self-Funded Solution</strong>: Halting the 4 negative-ROI campaigns frees $639,644 in cash, providing immediate funding for the VIP retention concierge without asking for new budget.</li>
                    <li><strong style="color: #F8FAFC;">Rebuilding AI Trust</strong>: Placing strict gender/catalog rules on AI recommendations prevents embarrassing errors (Sarees to men) and re-engages store managers.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Section 2: 80/20 Churn Driver Ranking Matrix
    st.markdown("#### The 80/20 Driver Ranking Matrix (Pareto Prioritization)")
    st.markdown(
        "Applying the 80/20 principle to isolate the 20% of root drivers that account for 80% of RetailCo's business damage:"
    )

    ranking_data = [
        {
            "Rank": "#1",
            "Driver": "Gold & Silver VIP Loyalty Defection",
            "Branch": "Branch 1.1",
            "Evidence": "Gold churn at 42.1%, Silver at 37.1% vs Bronze 19.6%",
            "Business Impact": "Severe LTV & Margin Destruction",
            "Actionability": "Immediate (VIP Concierge & Loyalty Revamp)",
            "Priority": "P0 (Critical)"
        },
        {
            "Rank": "#2",
            "Driver": "Hyderabad Regional Fulfillment Failure",
            "Branch": "Branch 1.2",
            "Evidence": "45.8% churn rate in Hyderabad (11/24 customers)",
            "Business Impact": "Geographic Market Loss & Brand Damage",
            "Actionability": "Immediate (Logistics SLA & 3PL Audit)",
            "Priority": "P0 (Critical)"
        },
        {
            "Rank": "#3",
            "Driver": "Marketing Channel Misallocation",
            "Branch": "Branch 3.1 & 3.2",
            "Evidence": "$640k burned in 4 negative-ROI campaigns; App Push/SMS starved",
            "Business Impact": "Direct Capital Loss & Flat Marketing ROI",
            "Actionability": "Immediate (Reallocate $350k-$400k)",
            "Priority": "P1 (High)"
        },
        {
            "Rank": "#4",
            "Driver": "AI Personalization Guardrail Absence",
            "Branch": "Branch 2.1",
            "Evidence": "39% irrelevance rate; 21 Sarees recommended to Men",
            "Business Impact": "Manager Mistrust & AI System Abandonment",
            "Actionability": "Short-Term (Deterministic Rule Engine)",
            "Priority": "P1 (High)"
        },
        {
            "Rank": "#5",
            "Driver": "Macro Customer Replacement Deficit",
            "Branch": "Branch 3.3",
            "Evidence": "Q2-2025: 90k churned vs 65k new (-25k net deficit)",
            "Business Impact": "Structural Customer Base Contraction",
            "Actionability": "Medium-Term (Fix retention loops)",
            "Priority": "P2 (Medium)"
        }
    ]

    st.dataframe(pd.DataFrame(ranking_data), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Section 3: Two-Speed Implementation Strategy
    st.markdown("#### Two-Speed Implementation Strategy")
    st.markdown(
        "A structured execution roadmap tailored for executive presentation, balancing immediate 30-day wins "
        "with sustainable 12-month digital transformation."
    )

    speed_col1, speed_col2 = st.columns(2)

    with speed_col1:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-left: 6px solid #2563EB; border-radius: 8px; padding: 18px; border-top: 1px solid #BFDBFE; border-right: 1px solid #BFDBFE; border-bottom: 1px solid #BFDBFE;">
                <h4 style="color: #1E40AF; margin-top: 0; margin-bottom: 10px;">Speed One: 30-Day Quick Wins (Zero/Low Capex)</h4>
                <ul style="font-size: 13.5px; color: #1E3A8A; line-height: 1.6; padding-left: 18px;">
                    <li><strong>Reallocate $350k-$400k Marketing Budget</strong>: Stop negative-ROI Facebook/Instagram campaigns (M003, M004, M007, M015). Direct funds into App Push & SMS. Yields <strong>+$91,000 net profit immediately</strong>.</li>
                    <li><strong>Deploy Hard AI Recommendation Rules</strong>: Apply gender and category validation (e.g. no Sarees to Men). Rebuild store manager trust in AI within 14 days.</li>
                    <li><strong>Launch Hyderabad VIP Taskforce</strong>: Audit local 3PL courier performance in Hyderabad. Issue express delivery guarantees and VIP apology credits.</li>
                    <li><strong>Gold/Silver Concierge Outreach</strong>: Dedicated retention call center reaching out to at-risk Gold members.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with speed_col2:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-left: 6px solid #10B981; border-radius: 8px; padding: 18px; border-top: 1px solid #A7F3D0; border-right: 1px solid #A7F3D0; border-bottom: 1px solid #A7F3D0;">
                <h4 style="color: #065F46; margin-top: 0; margin-bottom: 10px;">Speed Two: 12-Month Structural Transformation (USF Pillars)</h4>
                <ul style="font-size: 13.5px; color: #047857; line-height: 1.6; padding-left: 18px;">
                    <li><strong>Process (Loyalty Revamp)</strong>: Redesign Gold and Silver tiers from transactional points to experiential perks (guaranteed free 24-hr shipping, personal stylist).</li>
                    <li><strong>Data (Unified Customer 360)</strong>: Resolve the Data Paradox by unifying CRM, recommendation feedback, order history, and returns into one clean data model.</li>
                    <li><strong>Technology (Hybrid Recommender)</strong>: Upgrade AI models to context-aware multi-task neural architectures incorporating session intent and real-time inventory.</li>
                    <li><strong>Governance (Data Ownership & AI Trust)</strong>: Formally appoint data domain owners and give store managers a continuous feedback UI to flag bad recommendations.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Section 4: Interactive Revenue & Churn Recovery Simulator
    st.markdown("#### Executive Churn Recovery & Revenue Impact Simulator")
    st.markdown(
        "Demonstrate the tangible financial value of reducing customer churn back to baseline levels."
    )

    sim_c1, sim_c2 = st.columns([1, 2])

    with sim_c1:
        target_churn = st.slider(
            label="Target Churn Rate (%):",
            min_value=10.0,
            max_value=16.0,
            value=12.0,
            step=0.5,
            format="%.1f%%"
        )
        avg_arpu = st.number_input(
            label="Average Annual Revenue Per User (ARPU $):",
            min_value=50.0,
            max_value=500.0,
            value=180.0,
            step=10.0,
            format="%.0f"
        )

        impact_res = simulate_churn_reduction_impact(df_churn_trend, target_churn, avg_arpu)

    with sim_c2:
        r1, r2 = st.columns(2)
        with r1:
            st.metric(
                label="Customers Retained Per Quarter",
                value=f"{impact_res['retained_per_quarter']:,}",
                delta=f"vs {impact_res['current_churn_pct']}% current",
                delta_color="normal"
            )
        with r2:
            st.metric(
                label="Annualized Customers Saved",
                value=f"{impact_res['annualized_retained']:,}",
                help="Total customer base preserved over a 4-quarter cycle"
            )

        st.metric(
            label="Total Annual Revenue Saved",
            value=f"${impact_res['annual_revenue_saved']:,.0f}",
            delta=f"From {impact_res['active_base']:,} Active Customer Base",
            delta_color="normal"
        )

        st.markdown(
            f"""
            <div style="border-left: 5px solid #F59E0B; background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); padding: 14px 16px; border-radius: 6px; margin-top: 12px; border: 1px solid #FDE68A;">
                <strong style="color: #92400E;">Financial Business Case:</strong><br>
                <span style="color: #78350F; font-size: 13.5px;">
                    Lowering RetailCo's churn rate from <strong>{impact_res['current_churn_pct']}%</strong>
                    back to <strong>{target_churn}%</strong> saves <strong>{impact_res['annualized_retained']:,} customers annually</strong>,
                    recovering <strong>${impact_res['annual_revenue_saved']:,.0f} in recurring top-line revenue</strong>.
                    This single initiative pays back RetailCo's entire $30 Million digital transformation investment within two years!
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
