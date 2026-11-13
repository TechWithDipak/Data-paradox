# RetailCo – Customer Churn Analysis System
**Academic Case Study Project: SRM Institute of Science and Technology**  
*Course: 21IPE341T - Mastering the Data Paradox with AI and ML (Academic Year 2026-27)*  
*Assigned Case Question: Part B, Question 18 (RetailCo Churn Issue Tree)*

---

## Project Overview & Assigned Question

> **Assigned Problem Statement:**  
> *"Customer churn has increased from 12% to 16%. Develop a MECE issue tree to investigate the possible causes of this increase. Validate the major branches using the available dataset and identify the most critical business problem that RetailCo should address first."*

This repository delivers a **fully functional, interactive Streamlit analytics dashboard** that connects directly to the uploaded `RetailCo.xlsx` workbook across all four official sheets:
1. `RetailCo_Customers` (100 customer records: demographics, loyalty tier, last purchase, churn flag)
2. `RetailCo_Recommendations` (200 AI recommendation interaction logs: clicks, purchases, feedback)
3. `RetailCo_Campaigns` (15 marketing campaigns: channel spend, CTR, conversion rate, ROI)
4. `RetailCo_ChurnTrend` (6 quarters of macro corporate customer churn trajectory)

---

## Key Features of the Dashboard

- **Executive Overview**:
  - Macro KPI cards tracking quarterly churn escalation from 12.0% to 16.7% and the net customer deficit (-25,000 in Q2-2025).
  - Filtered sample health metrics updating dynamically in real time.
  - Interactive dual-axis chart showing active customer base, new additions, quarterly defections, and churn percentage.
- **Customer Demographic Analysis**:
  - Churn breakdown by **Loyalty Tier** (Gold at 42.1% vs Bronze at 19.6%).
  - Churn breakdown by **Location** (Hyderabad regional hotspot at 45.8% vs Mumbai at 18.8%).
  - Churn breakdown by **Gender** (Men at 35.7% vs Women at 22.7%) and **Age Groups**.
  - Interactive cross-segmentation heatmap (Location x Loyalty Tier).
  - Searchable, sortable customer explorer with one-click CSV export.
- **AI Recommendation Audit**:
  - Conversion funnel from Delivered (200) → Clicked (84, 42.0%) → Purchased (34, 17.0%).
  - Customer feedback distribution: 39.0% explicitly flagged as "Not relevant".
  - **The Context Breakdown Audit**: Discovers that **21 Sarees were recommended to Men** (47.6% rejected as irrelevant), explaining why internal managers bypass the $30M AI system.
  - Identification of 14 unserved customers with zero recommendations.
- **Marketing & ROI Analysis**:
  - Channel efficiency comparison highlighting that Facebook (0.8% ROI) and Instagram (3.8% ROI) consume 63.8% of spend ($1.62M).
  - Negative-ROI campaign audit isolating 4 value-destroying campaigns burning $639,644 (25.2% of spend).
  - Identification of underfunded high-ROI retention channels: App Push (27.3% ROI) and SMS (23.0% ROI).
  - **Interactive Budget Reallocation Simulator**: Real-time slider simulating capital shifts from social ads to App Push/SMS, projecting immediate ROI lift (+358 bps) and net profit gains.
- **MECE Issue Tree (Mutually Exclusive, Collectively Exhaustive)**:
  - Visual interactive hierarchy mapping all 4 branches and 11 sub-branches.
  - Objective verification of each branch categorized into:
    - **Supported (8 branches)**: Supported with quantitative metrics from the dataset.
    - **Partially Supported (1 branch)**: Distinct symptom of failure, but lacks statistical causality proof.
    - **Not Testable (2 branches)**: External competitor and macroeconomic factors unobservable in internal data.
  - Academic causality vs correlation guardrails to avoid logical fallacies.
- **Final Findings & Strategic Action Plan**:
  - Identification of the **#1 Critical Business Problem** RetailCo must address first: The High-Value VIP Defection (Gold 42.1%) & Regional Fulfillment Failure (Hyderabad 45.8%).
  - **80/20 Driver Ranking Matrix** prioritizing interventions by impact and feasibility.
  - **Two-Speed Implementation Roadmap**: Speed One (30-day low-capex quick wins) and Speed Two (12-month transformation across Process, Data, Technology, Governance).
  - **Interactive Churn Recovery & Revenue Simulator**: Demonstrating how reducing churn back to 12.0% retains 100,800 customers and saves **$18.1 Million** in recurring revenue.

---

## Project Structure

```
paradox/
├── app.py                      # Main Streamlit application entry point
├── config.py                   # Corporate color palette, styling, metadata
├── data_loader.py              # Ingestion, validation, cleaning, and customer enrichment
├── analytics.py                # Core statistical engine, segmentation cuts, hypothesis tests
├── mece_tree.py                # MECE tree definition, evidence mapping, status classifications
├── requirements.txt            # Python dependencies
├── README.md                   # Setup guide and presentation documentation
├── components/                 # Reusable dashboard UI modules
│   ├── overview_tab.py         # Macro KPI cards and quarterly churn trend charts
│   ├── customer_tab.py         # Loyalty, gender, location, and age churn deep-dive
│   ├── recommendation_tab.py   # AI CTR, conversion, irrelevance, gender mismatch audit
│   ├── marketing_tab.py        # Channel spend vs ROI, negative-ROI audit, budget simulator
│   ├── mece_tab.py             # Visual MECE issue tree, branch evidence cards, causality checks
│   └── findings_tab.py         # Executive synthesis, 80/20 driver ranking, revenue impact simulator
├── data/
│   └── RetailCo.xlsx           # Primary official Excel dataset (4 sheets)
└── docs/
    └── project-memory/         # Architectural governance and decision logs
        ├── 01_PROBLEM_STATEMENT.md
        ├── 02_EXECUTION_LOG.md
        └── 03_LESSONS_LEARNED.md
```

---

## How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

The application will launch automatically in your default browser at:  
**http://localhost:8501**

---

## Faculty Demonstration Guide (Key Talking Points)

1. **How the Data Connects**: Point out that every number in the dashboard is calculated live from `data/RetailCo.xlsx`. Filters in the left sidebar update the metrics, distributions, and charts reactively.
2. **The Data Paradox**: Highlight that RetailCo spent $30M on modern tools, yet managers don't use them. Show the **AI Recommendations tab** where 21 Sarees were recommended to Men, proving why managers lost trust in the system.
3. **The #1 Critical Problem**: Navigate to the **Final Findings tab** to show that Gold members (highest LTV) are defecting at 42.1%, while Hyderabad has a 45.8% churn rate. Explain that RetailCo is bleeding its most profitable customers.
4. **Capital Efficiency & Simulation**: Show the **Marketing tab** and use the interactive Budget Reallocation Slider to demonstrate that shifting $350k from negative-ROI Facebook/Instagram ads to App Push/SMS generates +$91k in profit immediately without increasing the budget.
5. **Causality vs Correlation**: Demonstrate that the MECE tree rigorously distinguishes correlation from causation (e.g., proving that while AI irrelevance is 39%, it does not statistically differentiate churned vs retained customers, so it is an operational amplifier rather than the sole cause).
