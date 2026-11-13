# RetailCo – Customer Churn Analysis System
## 01: Problem Statement & Specification

### Project Context
RetailCo is a leading fashion e-commerce platform that invested $30M in data analytics, AI recommendation engines, modern CRM platforms, marketing automation, and customer loyalty systems. Despite this investment:
- Customer churn has risen sharply from 12.0% in Q1-2024 to 16.0% in Q1-2025 and 16.7% in Q2-2025.
- Marketing ROI remains flat/depressed despite significant ad spend.
- AI-powered recommendation adoption is declining, with internal business managers bypassing AI tools due to low trust ("drowning in data, starving for insights").

### Assigned Research Question
"Customer churn has increased from 12% to 16%. Develop a MECE issue tree to investigate the possible causes of this increase. Validate the major branches using the available dataset and identify the most critical business problem that RetailCo should address first."

### Key Constraints & Requirements
1. **Source of Truth**: Primary Excel dataset `RetailCo.xlsx` containing four sheets:
   - `RetailCo_Customers` (100 customer profile records)
   - `RetailCo_Recommendations` (200 AI recommendation interaction records)
   - `RetailCo_Campaigns` (15 marketing campaign performance records)
   - `RetailCo_ChurnTrend` (6 quarters of macro churn trajectory)
2. **Methodology**: MECE (Mutually Exclusive, Collectively Exhaustive) decomposition.
3. **Evidence-Based Validation**: Classify all hypotheses into:
   - *Supported*: Confirmed with statistical evidence in the dataset.
   - *Partially Supported*: Consistent with indicators but incomplete proof.
   - *Not Testable*: Plausible business driver, but unobservable within the available dataset.
4. **Causation vs. Correlation Discipline**: Strictly distinguish correlation from proven causation.
5. **Interactive Corporate Dashboard**:
   - Built with Python, Streamlit, Pandas, Plotly.
   - Clean professional executive design.
   - Genuine interactivity (filters dynamically update metrics, issue tree nodes, and charts).
   - Zero hardcoding of analytical outputs; dynamic calculation from loaded Excel sheets.

### Out of Scope
- External web scraping or unverified competitor datasets.
- Production multi-tenant authentication systems.
- Unnecessary animations or complex non-standard UI libraries.

### Testable Success Criteria
- [ ] Application starts cleanly with `streamlit run app.py` without errors.
- [ ] Loads all 4 sheets from `data/RetailCo.xlsx` dynamically.
- [ ] Overview section shows dynamic KPI metrics and quarterly churn trend.
- [ ] Customer Analysis tab provides interactive breakdown by Loyalty Tier, Gender, and Location.
- [ ] AI Recommendation Analysis tab tracks CTR, Purchase Conversion, and Feedback sentiment.
- [ ] Marketing Analysis tab computes Channel/Segment spend, CTR, Conversion, and ROI.
- [ ] MECE Issue Tree tab displays visual interactive hierarchy with validation status, evidence cards, and statistical testing.
- [ ] Final Findings tab ranks critical business problems and actionable 30-day / 12-month recommendations.
- [ ] Global interactive filters (Location, Loyalty Tier, Gender, Channel) update charts and KPI cards seamlessly.
