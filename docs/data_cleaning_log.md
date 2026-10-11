# Data Cleaning & Transformation Documentation (ETL Log)

## 1. Executive Summary
- **Raw Data Ingestion:** 2868 records
- **Cleaned Data Production:** 2851 records
- **Data Reduction:** 17 records removed (100% attributable to exact transactional duplicates)
- **Data Quality Score Post-Cleaning:** 100% compliant with schema, no missing primary keys, zero unparsed dates, zero mathematical discrepancies.

---

## 2. Detailed Audit & Remediation Log

| Defect Category | Issue Identified in Raw Data | Impact / Risk | Remediation Applied | Excel Equivalent Technique | Python / ETL Function | Records Affected |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Duplicates** | Exact duplicate order lines | Double-counts revenue & inflated volume | Removed identical duplicate rows, keeping first logged occurrence | Data Tab > *Remove Duplicates* | `df.drop_duplicates()` | 17 rows |
| **Date Inconsistency** | Mixed date formats (`YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY`) | Breaks chronological sorting, MoM trends, and timeline slicers | Standardized to ISO 8601 (`YYYY-MM-DD`) using context validation against `Ship_Date` | Text to Columns > Date parsing or `=DATE(YEAR, MONTH, DAY)` | `pd.to_datetime()` with custom format fallbacks | 55 rows |
| **Text & Whitespace** | Leading/trailing spaces & mixed case (`"  furniture "`, `"WEST  "`) | Creates split categories in PivotTables (e.g. 'West' vs 'WEST') | Stripped leading/trailing whitespace and standardized to Title Case | `=TRIM(PROPER(text))` | `.str.strip().str.title()` | ~60 values |
| **Missing Customer** | Missing `Customer_Name` where `Customer_ID` existed | Incomplete customer segment reporting | Imputed name via master `Customer_ID` cross-reference | `=XLOOKUP(Customer_ID, ID_Col, Name_Col)` | `df.groupby('Customer_ID')` mapping | 12 rows |
| **Missing Postal Code** | Blank `Postal_Code` for known US cities | Geographic mapping & regional drill-down gaps | Imputed postal code using `(City, State)` mapping table | `=XLOOKUP(City&State, CityState_Col, Zip_Col)` | City/State lookup dictionary | 15 rows |
| **Postal Code Padding** | Truncated leading zeros in East coast zip codes (`2116` vs `02116`) | Corrupted postal records in Massachusetts/New Jersey | Left-padded numeric zip codes to standard 5 digits | `=TEXT(cell, "00000")` | `.apply(lambda z: str(z).zfill(5))` | 15 rows |
| **Quantity Typo** | Negative quantity (`-2`) in sales log | Artificially distorted unit volumes | Recomputed valid integer quantity based on `Sales / Unit_Price` | `IF(Quantity <= 0, ABS(Quantity), Quantity)` | Logical imputation | 1 row |
| **Discount Outlier** | Typo discount value (`2.0` entered for 20%) | Distorts margin % and causes massive artificial losses | Recomputed true discount from `1 - (Sales / Gross_Sales)` | Data Validation rules ($0 \le \text{Disc} \le 0.70$) | Bound threshold correction | 1 row |
| **Sales Keystroke Error** | Outlier \$45,000 recorded on a \$4.85 item | Distorts revenue totals by \$44,980+ | Re-verified financial formula: $\text{Sales} = \text{Price} \times \text{Qty} \times (1 - \text{Disc})$ | Re-evaluated calculation column in Excel Table | Vectorized recalculation | 14 rows |

---

## 3. Engineered Attributes for Business Intelligence
To prepare the dataset for dynamic Excel Dashboard reporting, the following calculated columns were introduced:
1. `Order_Year`: Calendar year extracted from `Order_Date` (`2023`, `2024`).
2. `Order_Month`: Year-Month string (`2023-01` to `2024-12`) for chronological time series analysis.
3. `Order_Month_Name`: Human-readable month label (`Jan 2023`, etc.).
4. `Order_Quarter`: Quarter label (`Q1 2023`, etc.).
5. `Shipping_Days`: Order-to-ship fulfillment lead time in integer days ($=\text{Ship\_Date} - \text{Order\_Date}$).
6. `Profit_Margin`: Line-item net margin ratio ($=\text{Profit} / \text{Sales}$).

---

## 4. Post-Cleaning Quality Verification Summary
- **Total Revenue:** \$1,845,890.07
- **Total Profit:** \$255,342.44
- **Overall Net Profit Margin:** 13.83%
- **Total Units Sold:** 7,204
- **Distinct Orders:** 2,850
- **Distinct Customers:** 50
- **Null Values Remaining:** 0 across all 29 fields.
