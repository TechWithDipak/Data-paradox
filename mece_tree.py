"""
MECE Issue Tree Definition and Validation Engine for RetailCo.
Structures the mutually exclusive and collectively exhaustive decomposition of churn causes.
"""

from typing import List, Dict, Any


def get_mece_tree_data() -> List[Dict[str, Any]]:
    """
    Returns the comprehensive MECE issue tree with hypotheses, evidence,
    validation status, and causality assessments.
    """
    return [
        # --- BRANCH 1: CUSTOMER SEGMENT & VALUE PROPOSITION ---
        {
            "id": "B1",
            "parent": "ROOT",
            "title": "Branch 1: Customer Value Proposition & Segment Vulnerability",
            "description": "Investigates whether churn is concentrated within specific customer cohorts due to unmet expectations or service friction.",
            "status": "Supported",
            "children": ["B1.1", "B1.2", "B1.3"]
        },
        {
            "id": "B1.1",
            "parent": "B1",
            "title": "1.1 High-Tier Loyalty Attrition (Gold & Silver Defection)",
            "hypothesis": "Premium loyalty members (Gold and Silver) are churning at significantly higher rates than entry-tier (Bronze) customers due to poor VIP retention incentives and unfulfilled loyalty value propositions.",
            "data_fields": "RetailCo_Customers: Loyalty_Tier, Churn_Flag",
            "status": "Supported",
            "evidence": "Gold tier churn is 42.11% (8/19) and Silver tier churn is 37.14% (13/35), compared to Bronze tier at only 19.57% (9/46). High-value Gold customers are churning at more than DOUBLE the rate of Bronze members.",
            "causality_note": "Strong statistical skew. High-value customers have higher expectations from the loyalty program; their defection directly depresses customer lifetime value (LTV) and revenue.",
            "actionability": "High",
            "impact_rank": 1
        },
        {
            "id": "B1.2",
            "parent": "B1",
            "title": "1.2 Regional Hotspot Defection (Hyderabad Logistics Breakdown)",
            "hypothesis": "Customer churn is geographically localized due to regional delivery delays, fulfillment bottlenecks, or localized customer service failures.",
            "data_fields": "RetailCo_Customers: Location, Churn_Flag",
            "status": "Supported",
            "evidence": "Hyderabad exhibits an alarming 45.83% churn rate (11/24 customers), far outpacing Mumbai (18.75%), Delhi (25.93%), and Bangalore (26.09%). Nearly 1 out of 2 Hyderabad customers churned.",
            "causality_note": "Significant geographic disparity indicates localized operational friction (likely 3PL delivery, warehouse fulfillment, or local delivery partner SLAs in Telangana/Hyderabad).",
            "actionability": "High",
            "impact_rank": 2
        },
        {
            "id": "B1.3",
            "parent": "B1",
            "title": "1.3 Demographic Gender Imbalance (Male Shopper Attrition)",
            "hypothesis": "Male shoppers experience higher friction or less relevant shopping journeys compared to female shoppers.",
            "data_fields": "RetailCo_Customers: Gender, Churn_Flag",
            "status": "Supported",
            "evidence": "Male customer churn is 35.71% (20/56) versus 22.73% for female shoppers (10/44). Male shoppers represent 66.7% of all churned customers in the sample.",
            "causality_note": "Correlated with gender-blind product recommendations (e.g., Sarees pushed to men), signaling catalog misalignment and lack of personalized male fashion merchandising.",
            "actionability": "Medium",
            "impact_rank": 5
        },

        # --- BRANCH 2: AI RECOMMENDATION & PERSONALIZATION BREAKDOWN ---
        {
            "id": "B2",
            "parent": "ROOT",
            "title": "Branch 2: AI Recommendation & Personalization Breakdown",
            "description": "Investigates whether the $30M investment in AI-driven personalization is failing to engage customers and driving dissatisfaction.",
            "status": "Supported",
            "children": ["B2.1", "B2.2", "B2.3"]
        },
        {
            "id": "B2.1",
            "parent": "B2",
            "title": "2.1 Critical Recommendation Irrelevance & Catalog Hallucination",
            "hypothesis": "The recommendation engine generates context-blind recommendations that alienate users, causing internal managers and shoppers to distrust the platform.",
            "data_fields": "RetailCo_Recommendations: Recommended_Category, Feedback, Clicked?, Gender",
            "status": "Supported",
            "evidence": "39.0% of recommendations (78/200) received explicit 'Not relevant' feedback. In an egregious context failure, Sarees were recommended 21 times to Men (47.6% flagged Not Relevant). Overall, 58.5% of recommendations failed to be confirmed useful.",
            "causality_note": "Directly supports the case statement that managers 'bypass available tools because they do not trust AI insights'. The Data Paradox: high tech spend without fundamental business guardrails.",
            "actionability": "Very High",
            "impact_rank": 3
        },
        {
            "id": "B2.2",
            "parent": "B2",
            "title": "2.2 Recommendation Conversion Bottleneck (Low Purchase Follow-through)",
            "hypothesis": "Recommendations fail to convert interest into purchases, depressing recommendation ROI and repeat purchasing.",
            "data_fields": "RetailCo_Recommendations: Clicked?, Purchased?",
            "status": "Supported",
            "evidence": "Only 17.0% of recommendations (34/200) resulted in a completed purchase. Even among clicked recommendations (84), only 40.5% resulted in a sale, indicating downstream pricing or product mismatch.",
            "causality_note": "Indicates weak conversion enablement. While recommendations prompt occasional clicks (42% CTR), they fail to drive the final transaction.",
            "actionability": "Medium",
            "impact_rank": 6
        },
        {
            "id": "B2.3",
            "parent": "B2",
            "title": "2.3 AI Irrelevance as the Direct Sole Cause of Customer Churn",
            "hypothesis": "Customers who receive irrelevant AI recommendations churn at a statistically higher rate than customers who receive useful recommendations.",
            "data_fields": "RetailCo_Customers & Recommendations: Customer_Irrelevance(%), Churn_Flag",
            "status": "Partially Supported",
            "evidence": "In the customer sample, churned customers experienced an average irrelevance rate of 34.0% versus 33.8% for retained customers (t-test p-value = 0.790, statistically non-significant). 14 customers received 0 recommendations, yet churn occurred in both groups.",
            "causality_note": "CRITICAL DISTINCTION: Irrelevant AI causes adoption failure and wastes the $30M investment, but CANNOT be claimed as the proven direct statistical cause of churn. It is an operational amplifier rather than the sole driver.",
            "actionability": "High",
            "impact_rank": 7
        },

        # --- BRANCH 3: MARKETING CAPITAL MISALLOCATION & RETENTION NEGLECT ---
        {
            "id": "B3",
            "parent": "ROOT",
            "title": "Branch 3: Marketing Capital Misallocation & Channel Inefficiency",
            "description": "Investigates whether marketing spending is squandered on unprofitable channels while starving high-ROI retention loops.",
            "status": "Supported",
            "children": ["B3.1", "B3.2", "B3.3"]
        },
        {
            "id": "B3.1",
            "parent": "B3",
            "title": "3.1 Over-allocation to Saturated / Negative ROI Channels (FB & IG)",
            "hypothesis": "Marketing budget is heavily concentrated in paid social channels that generate negative or near-zero returns, failing to retain customers.",
            "data_fields": "RetailCo_Campaigns: Channel, Spend($), ROI, Segment_Targeted",
            "status": "Supported",
            "evidence": "Instagram ($999,121) and Facebook ($621,030) consume 63.75% of total ad spend ($1.62M of $2.54M). 4 campaigns (M003, M004, M007, M015) delivered negative ROI (as low as -10%), burning $639,644 (25.2% of total marketing budget). Weighted ROI for Facebook is just 0.8% and Instagram is 3.8%.",
            "causality_note": "Direct financial evidence of 'flat marketing ROI' stated in the case. Marketing is pouring money into top-of-funnel acquisition on social channels while failing to protect the existing base.",
            "actionability": "Very High",
            "impact_rank": 4
        },
        {
            "id": "B3.2",
            "parent": "B3",
            "title": "3.2 Starvation of High-ROI Direct Retention Channels (App Push & SMS)",
            "hypothesis": "High-performing, high-ROI direct engagement channels are starved of budget, limiting RetailCo's ability to re-engage lapsed customers.",
            "data_fields": "RetailCo_Campaigns: Channel, Spend($), ROI, Conversion(%)",
            "status": "Supported",
            "evidence": "App Push generates a stellar 27.3% weighted ROI and SMS yields 23.0% weighted ROI. Yet together they receive only $662,973 (26.1% of budget). App Push and SMS campaigns achieved positive ROI in 100% of runs (M005, M006, M008, M010, M014).",
            "causality_note": "Clear capital misallocation. Shifting $400k from Facebook/Instagram to App Push/SMS would immediately generate +$91,063 in net incremental profit and +358 bps in blended ROI.",
            "actionability": "Very High",
            "impact_rank": 3
        },
        {
            "id": "B3.3",
            "parent": "B3",
            "title": "3.3 Macro Churn Replacement Deficit (Churn Outpacing Acquisition)",
            "hypothesis": "Customer churn volume has overtaken new customer acquisition, putting the e-commerce business into structural customer attrition.",
            "data_fields": "RetailCo_ChurnTrend: Quarter, Customers_Active, New_Customers, Churned_Customers, Churn_%",
            "status": "Supported",
            "evidence": "Quarterly churned customers escalated from 60,000 (12.0%) in Q1-2024 to 85,000 (16.0%) in Q1-2025 and 90,000 (16.7%) in Q2-2025 (+50% increase in customer defections). In Q2-2025, 90,000 churned against only 65,000 new customers, creating a net quarterly deficit of -25,000 customers.",
            "causality_note": "Validates the primary case problem statement. The business is leaking customers faster than it can acquire them despite $30M investments.",
            "actionability": "High",
            "impact_rank": 2
        },

        # --- BRANCH 4: EXTERNAL & MACROECONOMIC MARKET DYNAMICS ---
        {
            "id": "B4",
            "parent": "ROOT",
            "title": "Branch 4: External Market & Macroeconomic Pressures",
            "description": "Investigates external market pressures such as competitor price discounting and consumer spending contractions.",
            "status": "Not Testable",
            "children": ["B4.1", "B4.2"]
        },
        {
            "id": "B4.1",
            "parent": "B4",
            "title": "4.1 Competitor Discounting & Aggressive Loyalty Poaching",
            "hypothesis": "Rival fashion platforms (e.g., Myntra, Ajio, Nykaa) offered aggressive discounts, free shipping, or matching loyalty tiers, enticing RetailCo Gold/Silver members to switch.",
            "data_fields": "External: Competitor pricing, discount depth, loyalty match offers",
            "status": "Not Testable",
            "evidence": "No external competitor pricing, promotion tracking, or market share data exists in the provided RetailCo Excel dataset.",
            "causality_note": "A highly plausible real-world factor, but scientifically unverified within available data boundaries.",
            "actionability": "Low",
            "impact_rank": 8
        },
        {
            "id": "B4.2",
            "parent": "B4",
            "title": "4.2 Macroeconomic Discretionary Spending Contraction",
            "hypothesis": "Rising inflation or interest rates suppressed discretionary fashion purchases, leading shoppers to discontinue shopping apps.",
            "data_fields": "External: Consumer Price Index (CPI), fashion retail index, disposable income",
            "status": "Not Testable",
            "evidence": "No macroeconomic indicators or consumer sentiment survey data are present in the provided workbook.",
            "causality_note": "Cannot be validated or falsified using the four internal Excel sheets.",
            "actionability": "Low",
            "impact_rank": 9
        }
    ]


def get_mece_summary_stats() -> Dict[str, Any]:
    """Computes summary validation metrics across the MECE tree."""
    tree = get_mece_tree_data()
    sub_branches = [node for node in tree if node["parent"] != "ROOT"]
    
    total = len(sub_branches)
    supported = sum(1 for n in sub_branches if n["status"] == "Supported")
    partially = sum(1 for n in sub_branches if n["status"] == "Partially Supported")
    not_testable = sum(1 for n in sub_branches if n["status"] == "Not Testable")
    
    return {
        "total_sub_branches": total,
        "supported": supported,
        "partially_supported": partially,
        "not_testable": not_testable,
        "supported_pct": round((supported / total) * 100, 1),
        "partially_pct": round((partially / total) * 100, 1),
        "not_testable_pct": round((not_testable / total) * 100, 1)
    }
