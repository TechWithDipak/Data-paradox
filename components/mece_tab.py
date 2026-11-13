"""
MECE Issue Tree Tab Component.
Displays the structured MECE breakdown of churn causes, evidence cards, validation status, and causality checks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, STATUS_CONFIG
from mece_tree import get_mece_tree_data, get_mece_summary_stats


def render_mece_tab():
    st.markdown("### MECE Issue Tree Analysis & Hypothesis Validation")
    st.markdown(
        "Decomposing the central business question into a **Mutually Exclusive and Collectively Exhaustive (MECE)** "
        "framework to investigate why customer churn surged from **12.0% to 16.7%**. "
        "Each branch is validated against the actual RetailCo Excel dataset and categorized as **Supported**, "
        "**Partially Supported**, or **Not Testable**."
    )

    tree_nodes = get_mece_tree_data()
    summary = get_mece_summary_stats()

    # Validation Summary Badges
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)

    with b_col1:
        st.metric(
            label="Total Sub-Branches Evaluated",
            value=f"{summary['total_sub_branches']}",
            help="Total granular hypotheses tested across 4 major dimensions"
        )
    with b_col2:
        st.metric(
            label="Supported",
            value=f"{summary['supported']} ({summary['supported_pct']}%)",
            help="Hypotheses confirmed with quantitative evidence in RetailCo data"
        )
    with b_col3:
        st.metric(
            label="Partially Supported",
            value=f"{summary['partially_supported']} ({summary['partially_pct']}%)",
            help="Hypotheses showing symptoms/correlation but lacking definitive proof of direct causation"
        )
    with b_col4:
        st.metric(
            label="Not Testable",
            value=f"{summary['not_testable']} ({summary['not_testable_pct']}%)",
            help="Plausible external factors that cannot be validated due to dataset boundaries"
        )

    st.markdown("---")

    # Interactive Visual Tree Hierarchy using Plotly Sunburst / Treemap
    st.markdown("#### Visual MECE Decomposition Hierarchy")

    # Build hierarchy dataframe for visual tree
    plot_records = []
    # Root
    plot_records.append({
        "id": "ROOT",
        "parent": "",
        "name": "Why Did Churn Rise from 12% to 16%?",
        "status": "Root",
        "color": "#1E1B4B"
    })

    # Major Branches
    for node in tree_nodes:
        if node["parent"] == "ROOT":
            plot_records.append({
                "id": node["id"],
                "parent": "ROOT",
                "name": node["title"],
                "status": node["status"],
                "color": "#2563EB" if node["status"] == "Supported" else "#64748B"
            })

    # Sub-branches
    for node in tree_nodes:
        if node["parent"] in ["B1", "B2", "B3", "B4"]:
            s_color = (
                "#10B981" if node["status"] == "Supported"
                else ("#F59E0B" if node["status"] == "Partially Supported" else "#64748B")
            )
            plot_records.append({
                "id": node["id"],
                "parent": node["parent"],
                "name": f"{node['id']}: {node['title'].split(' ', 1)[1] if ' ' in node['title'] else node['title']}",
                "status": node["status"],
                "color": s_color
            })

    tree_df = pd.DataFrame(plot_records)

    st.caption("Interactive ring map: click any ring segment to zoom in; click the center circle to zoom back out.")
    fig_tree = px.sunburst(
        tree_df,
        names="name",
        parents="parent",
        ids="id",
        color="status",
        color_discrete_map={
            "Root": "#1E1B4B",
            "Supported": "#10B981",
            "Partially Supported": "#F59E0B",
            "Not Testable": "#64748B"
        }
    )
    fig_tree.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=480,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF"
    )
    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("---")

    # Filter Controls for Branch Cards
    st.markdown("#### Detailed Branch Verification Cards")
    filter_status = st.radio(
        label="Filter Branches by Validation Status:",
        options=["All Branches", "Supported Only", "Partially Supported Only", "Not Testable Only"],
        horizontal=True
    )

    status_filter_map = {
        "Supported Only": "Supported",
        "Partially Supported Only": "Partially Supported",
        "Not Testable Only": "Not Testable"
    }

    sub_nodes = [n for n in tree_nodes if n["parent"] != "ROOT"]
    if filter_status in status_filter_map:
        sub_nodes = [n for n in sub_nodes if n["status"] == status_filter_map[filter_status]]

    # Render structured cards
    for node in sub_nodes:
        st_cfg = STATUS_CONFIG.get(node["status"], STATUS_CONFIG["Not Testable"])
        badge_bg = st_cfg["badge_color"]
        badge_txt = st_cfg["text_color"]
        badge_bdr = st_cfg["border_color"]

        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid {badge_bdr}; border-left: 6px solid {badge_txt}; border-radius: 8px; padding: 16px; margin-bottom: 16px; background-color: #FFFFFF;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="margin: 0; color: #1F2937;">{node['title']}</h4>
                        <span style="background-color: {badge_bg}; color: {badge_txt}; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 13px; border: 1px solid {badge_bdr};">
                            {node['status']}
                        </span>
                    </div>
                    <p style="margin: 6px 0 10px 0; font-size: 14px; color: #374151;"><strong>Hypothesis:</strong> {node['hypothesis']}</p>
                    <p style="margin: 4px 0; font-size: 13px; color: #4B5563;"><strong>Data Fields Required:</strong> <code>{node['data_fields']}</code></p>
                    <div style="background-color: #F9FAFB; padding: 10px; border-radius: 6px; margin: 8px 0; border: 1px solid #E5E7EB;">
                        <strong style="color: #111827;">Actual Dataset Evidence:</strong><br>
                        <span style="color: #1F2937; font-size: 13.5px;">{node['evidence']}</span>
                    </div>
                    <div style="background-color: #EFF6FF; padding: 10px; border-radius: 6px; margin: 8px 0; border: 1px solid #BFDBFE;">
                        <strong style="color: #1E40AF;">Causality vs. Correlation Check:</strong><br>
                        <span style="color: #1E3A8A; font-size: 13.5px;">{node['causality_note']}</span>
                    </div>
                    <div style="margin-top: 8px; font-size: 12.5px; color: #6B7280;">
                        <strong>Actionability:</strong> {node['actionability']} &nbsp;|&nbsp; <strong>Impact Priority Rank:</strong> #{node['impact_rank']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Scientific Rigor Note (Causality vs Correlation)
    with st.expander("Academic Rigor: Correlation vs Proven Causality Framework", expanded=False):
        st.markdown(
            """
            ### Scientific Guardrails Applied in This Investigation
            In accordance with advanced academic standards, this system enforces strict causal inference rules:
            
            1. **The Difference Between Symptoms and Causes**:
               - A high irrelevance rate in AI recommendations (39.0%) is a clear symptom of a defective recommendation engine.
               - However, when comparing customers with high irrelevance (>=50%) against low irrelevance (<50%), both groups exhibited similar churn rates (~28% vs ~31%, p = 0.79).
               - Therefore, **we do not claim that AI recommendations alone caused customer churn**. Doing so would commit the *cum hoc ergo propter hoc* (correlation implies causation) logical fallacy.
            
            2. **Direct Drivers with Structural Proof**:
               - **Gold Tier Churn (42.1%)**: Direct loss of high-margin LTV customers.
               - **Hyderabad Defection (45.8%)**: Direct localized delivery/operational failure.
               - **Marketing Capital Misallocation**: Proven financial waste ($639,644 burned on negative-ROI ads).
            
            3. **Unobservable External Dimensions**:
               - External factors (competitor pricing, macroeconomic slowdown) are explicitly classified as **Not Testable** rather than assumed or hallucinated.
            """
        )
