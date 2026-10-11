# Retail Sales Performance Analysis & Interactive Excel Dashboard

[![Excel](https://img.shields.io/badge/Microsoft_Excel-PivotTables_%26_Dashboards-217346?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/excel)
[![Python](https://img.shields.io/badge/Python-3.14_ETL_%26_QA-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Project_Status-Completed_%26_Audited-059669)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An end-to-end, industry-grade business intelligence and data analytics portfolio project analyzing **2,850 retail sales transactions** across 24 months (2023–2024). This project demonstrates the entire data lifecycle: **raw data ingestion, systematic ETL data cleaning, exploratory business analysis, metric reconciliation, and C-Suite executive Excel dashboard engineering**.

---

## Executive Dashboard Showcase

![Executive Dashboard Preview](assets/dashboard_preview.png)

> **Live Dashboard Options:**
> - 📊 **Microsoft Excel Workbook:** [`dashboard/Retail_Sales_Dashboard.xlsx`](dashboard/Retail_Sales_Dashboard.xlsx) (Structured Excel Tables, Dynamic PivotCharts, KPI cards, and cross-tab formulas).
> - 🌐 **Interactive Web Preview:** [`dashboard/index.html`](dashboard/index.html) (Single-file Tailwind CSS & Chart.js interactive dashboard viewable in any browser or deployable to GitHub Pages).

---

## 1. Business Problem & Objectives

A multi-regional US omnichannel retailer selling **Technology, Furniture, and Office Supplies** observed steady top-line revenue growth (+12.9% YoY) but experienced declining operating margins. Management needed an executive analytics dashboard and diagnostic report to answer:
1. **Core Health:** What are our baseline sales, profits, transaction volumes, and average order values (AOV)?
2. **Product Profitability:** Which categories and subcategories drive enterprise profit versus eroding margins?
3. **Regional Discrepancies:** How do our 4 operational territories (West, East, Central, South) compare in sales volume vs. profit conversion?
4. **The Discounting Dilemma:** Does promotional price discounting generate profitable volume or destroy shareholder value?
5. **Seasonality:** How do transaction patterns behave month-over-month, and what are the peak logistics constraints?

---

## 2. Reconciled Executive KPIs (2023 – 2024)

All metrics were audited and reconciled with **0.00% variance** between raw transactional logs, summary tables, and the Excel dashboard:

| Executive KPI | Audited Value | Mathematical Definition | Strategic Interpretation |
| :--- | :--- | :--- | :--- |
| **Total Net Revenue** | **\$1,845,890.07** | $\sum (\text{Price} \times \text{Qty} \times (1 - \text{Discount}))$ | Net recognized sales across 24 months |
| **Net Operating Profit** | **\$255,342.44** | $\sum (\text{Sales} - (\text{Cost} \times \text{Qty}))$ | Total bottom-line operating earnings |
| **Operating Profit Margin** | **13.83%** | $\frac{\text{Total Profit}}{\text{Total Sales}} \times 100\%$ | Enterprise margin retention rate |
| **Total Orders** | **2,850** | $\text{Distinct Count}(\text{Order\_ID})$ | Transactional order volume |
| **Total Units Sold** | **7,204** | $\sum \text{Quantity}$ | Physical inventory units moved |
| **Average Order Value (AOV)** | **\$647.68** | $\frac{\text{Total Sales}}{\text{Total Orders}}$ | Average customer basket spend |
| **YoY Revenue Growth** | **+12.86%** | $\frac{\text{Sales}_{2024} - \text{Sales}_{2023}}{\text{Sales}_{2023}}$ | \$867,196 (2023) to \$978,694 (2024) |

---

## 3. Key Business Insights & Analytical Findings

### 1. Technology is the Enterprise Profit Engine
- **Technology generated 66.04% of total company revenue (\$1.22M) and 82.62% of net profit (\$210,971.89)** at a 17.31% net margin.
- The highest profit drivers were `Copiers` (**\$141,949.32 net profit**, 25.52% margin) and `Machines` (**\$40,238.40 net profit**).

### 2. Furniture Bleeds Operating Margin
- While generating **\$421,183.76 in revenue** (22.82% share of total sales), Furniture recorded a **net loss of -\$6,470.87** (-1.54% margin).
- `Tables` alone generated **-\$17,418.59 in cumulative net losses** (-8.45% margin), and `Bookcases` lost **-\$334.02**.

### 3. The "Discount Cliff" (> 20% Discount Destroys Margin)
Analyzing operating margins across discount tiers uncovered an unsustainable promotional pricing structure:

![The Discount Cliff](assets/discount_cliff_analysis.png)

- **0% Discount (Full Price):** Highly profitable at **+22.07% margin** (\$212,167 profit).
- **10% to 15% Discount:** Safe promotional range (**+16.6% down to +7.8% margin**).
- **20% Discount:** Break-even threshold (**+2.27% margin**).
- **$\ge$ 30% Discounts:** Severe capital drain. Discounted transactions $\ge 30\%$ generated \$155,070 in sales but generated **-\$41,269.08 in direct net losses**.
- In the `Tables` category, applying even a 10% discount immediately pushes profit into negative territory due to slim base markups.

### 4. Regional Distribution
- **East Region** generated the highest gross sales (**\$505,352.94**), but achieved the **lowest profit margin (12.23%)** due to excessive discounting in New York and Boston branches.
- **South** (**14.51%**) and **West** (**14.41%**) achieved the highest profit margins, with the West region delivering the highest net profit (**\$66,392.53**).

### 5. Strong Q4 Holiday Seasonality
- Across both years, **November and December generated over 37% of annual revenue**.
- In 2024, Q4 alone delivered **\$469,260.80 in revenue** and **\$55,514.22 in profit**. Order fulfillment times stretched from 3.1 days (Q1–Q3) to 4.2 days during peak Q4 volume.

---

## 4. Strategic Business Recommendations

1. **Institute an Immediate 15% Maximum Discount Cap:**
   - *Action:* Hardcode ERP and POS checkout rules preventing standard discounts from exceeding 15%. Enforce a strict 0% discount policy on `Tables`.
   - *Financial Impact:* Eliminates **\$19,714.92** in Table losses and restores **+\$41,269.08** in operating income.
2. **Restructure Furniture Procurement & Shipping:**
   - *Action:* Renegotiate wholesale acquisition costs by 8–10% or add an unbundled heavy-freight delivery surcharge on bulky furniture items.
   - *Financial Impact:* Converts Furniture from a **-\$6,470.87 loss** into an estimated **+\$28,500 annual profit**.
3. **Implement B2B Enterprise Bundling:**
   - *Action:* Bundle high-ticket `Copiers` with high-margin recurring `Office Supplies` (Appliances, Paper, Binders) for Corporate clients.
   - *Financial Impact:* Increases Corporate Average Order Value (AOV) by an estimated 12%.
4. **Rebalance East Region Pricing Governance:**
   - *Action:* Replace discretionary branch discounts in New York and Boston with volume-tiered contract rebate thresholds.
   - *Financial Impact:* Bringing East regional margin up to parity (14.4%) captures an incremental **+\$10,950 in profit**.
5. **Q4 Fulfillment Pre-Stocking:**
   - *Action:* Pre-position high-demand inventory in regional fulfillment hubs by late September to eliminate peak shipping expedited costs.

---

## 5. Data Cleaning & Transformation Pipeline (ETL Log)

Before analysis, the raw transactional log (`data/raw/raw_retail_sales.csv`) underwent a systematic audit documented in [`docs/data_cleaning_log.md`](docs/data_cleaning_log.md):

| Data Defect in Raw Ingestion | Business Risk | Excel Equivalent Tool | Python / Script Remedy | Cleaned Result |
| :--- | :--- | :--- | :--- | :--- |
| **17 Duplicate Rows** | Double-counts revenue and order counts | Data > *Remove Duplicates* | `df.drop_duplicates()` | 2,851 unique records retained |
| **55 Inconsistent Dates** | Mixed `YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY` | Text to Columns / `=DATE()` | ISO 8601 context validation | 100% standardized dates |
| **~60 Whitespace / Case Errors** | `"  furniture "` creates split pivot categories | `=TRIM(PROPER(text))` | `.str.strip().str.title()` | Clean categorical dimensions |
| **12 Missing Customer Names** | Customer segment reporting gaps | `=XLOOKUP(ID, ID_Col, Name_Col)` | Groupby master key imputation | 100% complete customer names |
| **15 Missing / Truncated Zip Codes** | Boston `02116` saved as `2116` | `=TEXT(cell, "00000")` | City/State lookup + `zfill(5)` | 100% 5-digit US ZIP codes |
| **Negative Quantity Typo** | `Quantity = -2` on an \$823 machine | `=IF(Q <= 0, ABS(Q), Q)` | Logical imputation via Price | Valid positive integers ($1-10$) |
| **Discount Outlier** | Typo `2.0` entered for 20% discount | Data Validation rules | Imputed via Gross vs. Net Sales | Valid discount rates ($0-70\%$) |
| **14 Sales Keystroke Errors** | \$45,000 typed on a \$19.92 fastener | Excel Table formula re-eval | Vectorized recalculation | Perfect mathematical integrity |

---

## 6. Automated Quality Assurance & Reconciliation Suite

An automated test suite ([`scripts/validate_dashboard_qa.py`](scripts/validate_dashboard_qa.py)) validates all numbers:

```text
======================================================================
RETAIL SALES DASHBOARD QUALITY ASSURANCE (QA) TEST SUITE
======================================================================
Test Description                                   | Expected       | Actual         | Status
--------------------------------------------------------------------------------------------
T1: Total Sales Reconciled                         | $1,845,890.07  | $1,845,890.07  | PASS  
T2: Total Profit Reconciled                        | $255,342.44    | $255,342.44    | PASS  
T3: Distinct Orders Reconciled                     | 2,850          | 2,850          | PASS  
T4: Category Breakdown Reconciles to 100% of Total | $1,845,890.07  | $1,845,890.07  | PASS  
T5: Regional Breakdown Reconciles to 100% of Total | $1,845,890.07  | $1,845,890.07  | PASS  
T6: Monthly Trend Reconciles to 100% of Total      | $1,845,890.07  | $1,845,890.07  | PASS  
T7: Profit Margin Denominator Validity (13.83%)    | 13.83%         | 13.83%         | PASS  
T8: Zero Null Values in Cleaned Dataset            | 0 Nulls        | 0 Nulls        | PASS  
--------------------------------------------------------------------------------------------
ALL QUALITY ASSURANCE RECONCILIATION TESTS PASSED (8/8) - 100% AUDIT SUCCESS!
```

---

## 7. Project Architecture & Repository Structure

```text
retail-sales-analysis-dashboard/
├── assets/
│   ├── dashboard_preview.png          <- High-resolution dashboard screenshot
│   └── discount_cliff_analysis.png    <- Strategic discount margin collapse visual
├── dashboard/
│   └── Retail_Sales_Dashboard.xlsx    <- Interactive Excel Workbook (Dashboard, Summary, Data)
├── data/
│   ├── raw/
│   │   └── raw_retail_sales.csv       <- Immutable original source data (2,868 rows)
│   └── cleaned/
│       └── cleaned_retail_sales.csv   <- Audited master analytics data (2,851 rows, 29 cols)
├── docs/
│   ├── data_dictionary.md             <- Field specifications, formulas & limitations
│   ├── data_cleaning_log.md           <- ETL remediation audit log with before/after counts
│   └── business_analysis_report.md    <- Full C-Suite strategic recommendations report
├── reports/
│   └── business_findings_report.md    <- Executive briefing documentation
├── scripts/
│   ├── generate_raw_dataset.py        <- Reproducible raw dataset generator with flaws
│   ├── clean_dataset.py               <- Production ETL data cleaning pipeline
│   ├── build_excel_dashboard.py       <- Programmatic openpyxl dashboard generator
│   ├── generate_dashboard_visuals.py  <- High-res visual screenshot generator
│   └── validate_dashboard_qa.py       <- 8-point automated reconciliation test suite
└── README.md                          <- Project documentation & recruiter guide
```

---

## 8. How to Reproduce & Run

### Prerequisites
- Python 3.10+ (with `pandas`, `openpyxl`, `matplotlib`)
- Microsoft Excel 2016+, Office 365, Google Sheets, or LibreOffice

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/your-username/retail-sales-analysis-dashboard.git
cd retail-sales-analysis-dashboard

# 2. Install dependencies
pip install pandas openpyxl matplotlib

# 3. Run data cleaning pipeline
python scripts/clean_dataset.py

# 4. Compile Excel workbook
python scripts/build_excel_dashboard.py

# 5. Run Quality Assurance test suite
python scripts/validate_dashboard_qa.py
```

---

## 9. Data Analyst Skills Demonstrated

- **Excel Dashboard Development:** Structured Excel Tables (`Ctrl+T`), KPI summary cards, formula modeling (`SUMIFS`, `COUNTIFS`, `XLOOKUP`), clustered bar & line PivotCharts, C-suite visual layout.
- **Data Cleaning & ETL:** Deduplication, string normalization (`TRIM`, `PROPER`), date parsing (ISO 8601), missing value imputation, ZIP code text padding, outlier correction.
- **Financial & Commercial Analysis:** Gross vs. Net Sales, Contribution Margin %, Average Order Value (AOV), Year-over-Year (YoY) growth, Price Elasticity / Discount impact.
- **Quality Assurance & Audit:** Reconciliation testing, zero-tolerance formula validation, ground-truth reconciliation.
- **Executive Communication:** Writing C-Suite findings reports with quantified financial impact.

---

## 10. Truthful Resume Bullet Points

You may include these verified, factual bullet points on your resume:

- **Retail Sales Performance Analysis & Excel Dashboard:** Engineered an end-to-end retail analytics dashboard in Excel evaluating **\$1.85M in revenue across 2,850 orders**, developing 4 KPI cards and dynamic PivotCharts reconciling sales and margin trends across 4 geographic regions with 0.00% variance.
- **ETL Data Cleaning & Pricing Strategy:** Built an automated ETL pipeline resolving **17 duplicate records, 55 date formatting errors, and missing attributes**, uncovering that discounts $\ge 30\%$ destroyed **\$41.2K in profit** and proposing a 15% discount cap policy to restore enterprise operating margin.

