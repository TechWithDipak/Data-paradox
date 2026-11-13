# RetailCo – Customer Churn Analysis System
## 03: Lessons Learned & Decision Registry

### Architectural & Analytical Lessons
1. **The Data Paradox in Practice**:
   - *Observation*: RetailCo invested $30M in modern tooling, yet managers bypass insights and churn is accelerating.
   - *Root Cause*: Lack of contextual data validation and guardrails. Pushing women's apparel (Sarees) to men without gender filtering destroyed credibility. High-value customers (Gold) were not targeted with specialized retention treatment.
   - *Prevention*: Always couple AI personalization with deterministic business rules (catalog taxonomy, gender filters, inventory checks) before serving recommendations.

2. **Causation vs. Correlation Guardrail**:
   - *Observation*: Customers experiencing irrelevant recommendations do not exhibit a statistically higher churn rate in the customer sample than those who experienced relevant recommendations (28.2% vs 31.1%).
   - *Insight*: Irrelevant recommendations degrade user engagement and waste ad/tech spend, but cannot be proven to be the sole *direct cause* of churn with the sample size and without time-to-churn interaction sequences. Thus, MECE branch on AI must be marked "Partially Supported / Inconclusive as Sole Root Cause".

3. **Data Quality in Excel Ingestion**:
   - *Observation*: The uploaded Excel sheets contain trailing columns with documentation notes (`Unnamed: 5`, `Unnamed: 6`, etc.).
   - *Fix*: Ingestion layer must programmatically filter out unnamed columns and coerce types (dates, integers, percentages).

4. **Streamlit Component Type Safety**:
   - *Observation*: `st.number_input` format string with leading currency symbol (e.g. `format="$%.0f"`) throws `StreamlitInvalidNumberFormatError` because Python's string modulo requires a pure format specification like `%.0f`.
   - *Fix*: Keep `format="%.0f"` and render currency symbols explicitly in labels and metric cards.
   - *Verification*: Tested end-to-end with `streamlit.testing.v1.AppTest` with 0 exceptions across all tabs, metrics, and filter combinations.

