# Data Analyst Interview Preparation & Defense Guide
**Project:** Retail Sales Performance Analysis & Interactive Excel Dashboard

This guide equips you with interview answers, technical formula explanations, and behavioral stories to discuss this project with hiring managers.

---

## 1. The 60-Second "Elevator Pitch"

> *"For my portfolio, I built an end-to-end retail performance analysis and executive Excel dashboard analyzing \$1.85M in revenue across 2,850 orders for a multi-regional US retailer. I started by building an ETL data cleaning pipeline in Python to handle real-world data flaws like duplicates, corrupt date strings, and keystroke outliers. Then, I engineered an audited semantic data model in Excel with KPI cards and multi-series PivotCharts.*
> 
> *The key business discovery was uncovering a 'Discount Cliff'—where promotions exceeding 20% destroyed \$41.2K in operating profit, and Furniture lost \$6.5K due to under-priced Tables. I modeled a 15% promotional cap policy that recovers over \$41K in margin while ensuring 100% mathematical reconciliation across all dashboard tabs."*

---

## 2. Top 5 Technical & Behavioral Interview Questions

### Q1: "Walk me through how you handled data quality issues in your dataset."
- **STAR Answer:**
  - **Situation:** The raw transaction log contained 2,868 records with operational data quality flaws typical of point-of-sale systems.
  - **Task:** Ensure zero data distortion before building executive reports while leaving raw data immutable.
  - **Action:** I identified 17 exact duplicate order rows from POS sync retries and removed them. I standardized 55 inconsistent date formats (`DD/MM/YYYY` vs. `MM/DD/YYYY`) by validating against shipping dates. I restored truncated leading zeros on East Coast ZIP codes using text padding (`02116`), imputed missing customer names using `Customer_ID` cross-referencing, and caught a keypunch typo where a \$19.92 fastener was recorded as \$45,000.
  - **Result:** Created an audited dataset of 2,851 records with zero missing values and an automated QA reconciliation script verifying 0.00% formula variance.

### Q2: "What Excel features and functions did you use, and why?"
- **Answer:**
  - **Structured Excel Tables (`Ctrl + T`):** For dynamic range expansion and cleaner structured references (`[@Sales]`).
  - **Formulas:** `SUMIFS`, `COUNTIFS`, `XLOOKUP`, `DATE`, `TEXT`, `IF`, and `AVERAGEIFS`.
  - **PivotTables & PivotCharts:** To aggregate sales by region, category, month, and customer segment.
  - **KPI Cards & UI Design:** Designed card containers using fill colors, borders, and custom number formatting (`$#,##0`, `0.0%`) to display high-level metrics clearly for executive stakeholders.

### Q3: "What was the most surprising business insight from your analysis?"
- **Answer:**
  - *"The disconnect between revenue volume and profit margin. Technology drove 66% of sales and 82.6% of profit, but Furniture lost -\$6,471 despite generating \$421K in sales.*
  - *When I analyzed profitability across discount tiers, I discovered that every discount tier $\ge 30\%$ was deeply negative, resulting in \$41.2K of destroyed profit. Tables alone lost -\$17,419 because their initial markup was too thin to support discounts above 0%."*

### Q4: "How did you validate that your dashboard metrics were accurate?"
- **Answer:**
  - *"I developed an automated 8-point reconciliation test suite (`validate_dashboard_qa.py`). It verified that total sales (\$1,845,890.07) and profit (\$255,342.44) reconciled across the underlying data table, summary pivot tables, monthly trend series, and dashboard KPI cards. I also tested that all percentage metrics used the correct net sales denominator."*

### Q5: "If the CEO only had 2 minutes, what 3 actions would you recommend?"
- **Answer:**
  1. **Institute an immediate 15% discount cap policy** and eliminate all discounts on Tables to recover **+\$41.2K in profit**.
  2. **Renegotiate furniture supplier costs by 8–10%** or add a heavy-freight delivery surcharge to flip Furniture to **+\$28.5K profit**.
  3. **Bundle Technology copiers and machines with high-margin Office Supplies** for Corporate clients to raise B2B Average Order Value by ~12%.

---

## 3. Core Financial Formulas Cheat Sheet

- **Net Sales:** $\text{Unit Price} \times \text{Quantity} \times (1 - \text{Discount})$
- **Cost of Goods Sold (COGS):** $\text{Unit Cost} \times \text{Quantity}$
- **Net Profit:** $\text{Net Sales} - \text{COGS}$
- **Profit Margin (%):** $\frac{\text{Net Profit}}{\text{Net Sales}} \times 100\%$
- **Average Order Value (AOV):** $\frac{\text{Total Net Sales}}{\text{Distinct Order Count}}$
- **YoY Growth (%):** $\frac{\text{Sales}_{2024} - \text{Sales}_{2023}}{\text{Sales}_{2023}} \times 100\%$

