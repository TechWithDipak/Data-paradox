# RetailCo – Customer Churn Analysis System
## 02: Execution Log

### Initial Setup & Data Ingestion
- **2026-11-13 07:27**: Inspected workspace and discovered user-uploaded Excel workbook `media_1794534893548_691b5db5.xlsx` and assignment PDF.
- **2026-11-13 07:27**: Copied workbook into `data/RetailCo.xlsx`.
- **2026-11-13 07:27**: Installed required dependencies (`streamlit`, `plotly`, `altair`, `pyarrow`, `openpyxl`, `pandas`).
- **2026-11-13 07:28**: Executed exploratory data analysis script across all 4 sheets (`RetailCo_Customers`, `RetailCo_Recommendations`, `RetailCo_Campaigns`, `RetailCo_ChurnTrend`).
- **Key EDA Observations**:
  - `RetailCo_ChurnTrend`: Churn surged from 12.0% (Q1-2024, 60,000 lost) to 16.0% (Q1-2025, 85,000 lost) and 16.7% (Q2-2025, 90,000 lost). Net customer loss observed in Q2-2025 (65k new vs 90k churned).
  - `RetailCo_Customers`: 30% sample churn rate (30/100). Severe skew towards Gold (42.1% churn) and Silver (37.1% churn) compared to Bronze (19.6% churn). Severe regional hotspot in Hyderabad (45.8% churn) and gender imbalance (Male 35.7% vs Female 22.7%).
  - `RetailCo_Recommendations`: 200 interaction logs across 86 customers (14 customers unserved). 39% "Not relevant" feedback rate (78/200), 19.5% unrated. Serious contextual mismatch: Sarees recommended to Men 21 times (nearly 48% rated Not relevant).
  - `RetailCo_Campaigns`: $2.54M total spend across 15 campaigns. Instagram ($999K) and Facebook ($621K) consume ~64% of budget with near-zero ROI (0.042 and 0.008) and 4 negative-ROI campaigns. App Push (0.273 ROI) and SMS (0.230 ROI) are heavily underfunded.

### Application Architecture & Implementation
- **2026-11-13 07:30**: Created `requirements.txt` with verified packages (`streamlit`, `pandas`, `openpyxl`, `plotly`, `altair`).
- **2026-11-13 07:30**: Implemented `config.py` defining styling palette, corporate colors, and academic metadata.
- **2026-11-13 07:31**: Implemented `data_loader.py` with caching, Excel sheet validation, date parsing, column cleaning, and customer recommendation profile enrichment.
- **2026-11-13 07:32**: Implemented `analytics.py` containing statistical testing (Chi-square, t-tests), segmentation cuts, KPI computations, budget reallocation simulator, and revenue impact calculator.
- **2026-11-13 07:32**: Implemented `mece_tree.py` establishing the 4-branch, 11-subbranch MECE issue tree with hypotheses, required fields, quantitative evidence, validation status (8 Supported, 1 Partially Supported, 2 Not Testable), and causality guardrails.
- **2026-11-13 07:33 - 07:35**: Built modular UI components in `components/`:
  - `overview_tab.py`: Macro quarterly trajectory, customer deficit metrics, and cohort summaries.
  - `customer_tab.py`: Churn cuts by Loyalty Tier, Gender, Location, Age, Location x Tier cross-tab heatmap, and customer record search/export.
  - `recommendation_tab.py`: CTR, conversion funnel, 39% irrelevance sentiment, Sarees-to-Men context audit (21 instances), unserved customer detection.
  - `marketing_tab.py`: Channel spend vs ROI matrix, negative-ROI campaign audit ($640k leakage), interactive capital reallocation slider.
  - `mece_tab.py`: Interactive Sunburst visual tree hierarchy, filterable status cards with dataset evidence, causality vs correlation guardrails.
  - `findings_tab.py`: Synthesis of #1 critical problem, 80/20 driver ranking, two-speed implementation roadmap, and interactive revenue recovery calculator.
- **2026-11-13 07:35**: Implemented `app.py` combining custom CSS, dynamic sidebar filters (Location, Tier, Gender, Channel), reactive data flow, and 6 core tabs.
- **2026-11-13 07:35**: Created comprehensive `README.md` with local execution commands, architecture breakdown, and faculty presentation guide.
- **2026-11-13 07:36**: Verified bytecode compilation (`py_compile`) for all files with 0 errors.
- **2026-11-13 07:37**: Launched Streamlit server in headless mode on port 8501; verified HTTP 200 OK on health check.
- **2026-11-13 07:37**: Dispatched browser verification subagent to inspect visual rendering and tab navigation.
- **2026-11-13 07:44 - 07:46**: Enhanced and diversified color scheme across all views based on user feedback:
  - `config.py`: Introduced dedicated palettes for cities (`CITY_COLORS`), loyalty tiers (`TIER_COLORS`), age groups (`AGE_COLORS`), product categories (`CATEGORY_COLORS`), and marketing channels (`CHANNEL_COLORS`).
  - `customer_tab.py`: Replaced monochrome blue bars with distinct, unique colors for all cities (Hyderabad Crimson, Chennai Orange, Bangalore Cyan, Delhi Violet, Mumbai Emerald), radiant gold/slate/copper for loyalty tiers, dual colors for gender, and progressive color ramp for age cohorts. Upgraded heatmap with high-contrast perceptual palette (`#F0FDF4` to `#991B1B`).
  - `overview_tab.py`: Replaced washed-out shades with sapphire active bars, vibrant emerald new customers, vivid rose churned bars, and luminous amber churn line. Converted diagnostic callouts into distinct colored border cards.
  - `recommendation_tab.py`: Added distinct product category bar chart with 7-color palette (Sarees `#EC4899`, Kurtas `#8B5CF6`, Jeans `#2563EB`, T-Shirts `#06B6D4`, Shoes `#F59E0B`, Watches `#10B981`, Bags `#F97316`). Replaced alert with executive rose-tinted card.
  - `marketing_tab.py`: Applied brand-accurate color mapping for channels and enhanced budget reallocation summary card.
  - `findings_tab.py`: Replaced raw red block with an executive midnight-navy card with gold/rose highlights.
  - `app.py`: Upgraded header with multi-stop dark navy/blue gradient, metric cards with top accent lines and hover animations.
  - Validated end-to-end with `streamlit.testing.v1.AppTest` with 0 exceptions.
- **2026-11-13 08:04**: Removed all emojis and decorative icons across the entire application code, UI headers, sidebar filters, cards, badges, and documentation to give the dashboard a clean, authentic, human-designed enterprise appearance. Verified zero remaining emojis across all `.py` and `.toml` files via automated regex scan. Verified end-to-end with `AppTest` (0 exceptions).
- **2026-11-13 08:09**: Initialized Git repository, staged all project files and memory logs, committed as `b981b7b`, and successfully force-pushed to remote GitHub repository `https://github.com/TechWithDipak/Data-paradox.git` replacing existing files per user request.
- **2026-11-13 08:27**: Created comprehensive non-technical guide `PROJECT.md` in the project root covering project overview, end-to-end data pipeline, sheet descriptions, tour of all 6 tabs with exact numbers, explanations of all interactive features with mathematical walk-throughs, actual findings, 5-minute faculty presentation script, and 18 detailed viva Q&A for academic review.
- **2026-11-13 15:05**: Resolved visual collision on the Quarterly Churn chart (`overview_tab.py`) where the inline plot title and the horizontal legend occupied the same horizontal row. Moved subtitle into a clean Streamlit caption above the chart, gave the horizontal legend full top-width breathing room (`y=1.02`), and cleaned up redundant titles across remaining tabs (`customer_tab.py`, `recommendation_tab.py`, `marketing_tab.py`, `mece_tab.py`). Committed (`2d84357`) and pushed to GitHub.






