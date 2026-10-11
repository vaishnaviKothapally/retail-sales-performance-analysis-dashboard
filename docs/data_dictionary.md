# Data Dictionary: Retail Sales Performance Dataset

## 1. Overview & Dataset Lineage
- **Dataset Title:** US Retail Sales & Performance Dataset
- **Domain:** Retail & E-Commerce Operations
- **Time Coverage:** January 1, 2023 – December 31, 2024 (24 months)
- **Granularity:** One record per line item order transaction
- **Total Raw Records:** 2,868 rows
- **Status & Classification:** Realistic synthetic transactional dataset modeled closely on industry-standard retail enterprise benchmarks (e.g., Global Superstore, National Retail Federation operational standards). Intentionally seeded with documented real-world data flaws for audit, data cleaning, and ETL portfolio demonstration.

---

## 2. Field Specifications

| Field Name | Raw Data Type | Target Clean Type | Allowed / Sample Values | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| **Order_ID** | String | String | `ORD-2023-10042` | Unique transaction order identifier. Format: `ORD-[Year]-[SequentialNumber]`. |
| **Order_Date** | String (Mixed) | Date (`YYYY-MM-DD`) | `2023-01-15`, `15/01/2023` | Date when customer placed the transaction. |
| **Ship_Date** | String | Date (`YYYY-MM-DD`) | `2023-01-18` | Date when items were dispatched from fulfillment hub. |
| **Ship_Mode** | String | String | Standard Class, Second Class, First Class, Same Day | Delivery logistics service level. |
| **Customer_ID** | String | String | `CUST-1001` to `CUST-1049` | Unique customer account number. |
| **Customer_Name** | String (with NaNs) | String | *Emily Davis*, *Ryan Hernandez* | Full legal or registered profile name. Missing values imputable via Customer_ID. |
| **Segment** | String (Whitespaces) | String | Consumer, Corporate, Home Office | Target market customer classification. Consumer represents individual buyers; Corporate represents enterprise accounts; Home Office represents small businesses. |
| **Country** | String | String | United States | Sovereign country of sale and delivery. |
| **City** | String | String | Los Angeles, Chicago, New York City | Municipality / delivery destination city. |
| **State** | String | String | California, New York, Texas, Florida | Destination state / sub-national jurisdiction. |
| **Postal_Code** | String (Truncated) | String (5-digit padded) | `90036`, `02116`, `07102` | US ZIP code. Must retain leading zeros (`02116`). |
| **Region** | String (Mixed Case) | String | West, East, Central, South | Sales operational territory division. |
| **Product_ID** | String | String | `TEC-PH-100`, `FUR-BO-105` | Stock Keeping Unit (SKU) identifier. Category-SubCategory-Item code. |
| **Category** | String (Whitespace) | String | Technology, Furniture, Office Supplies | High-level merchandise department classification. |
| **Sub_Category** | String | String | Phones, Chairs, Binders, Tables, etc. | Specific product line segment within parent category (17 sub-categories). |
| **Product_Name** | String | String | *Phone Pro Edition*, *Bookcase Standard Edition* | Commercial merchandise title. |
| **Unit_Price** | Float | Currency ($) | \$3.00 – \$2,200.00 | Catalog MSRP / selling price per individual unit. |
| **Unit_Cost** | Float | Currency ($) | \$1.50 – \$1,600.00 | Cost of goods sold (COGS) incurred to procure/manufacture one unit. |
| **Quantity** | Integer | Integer | 1 – 10 (valid range) | Units purchased per transaction line. Must be positive integer. |
| **Discount** | Float / Mixed | Percentage (%) | 0.00 to 0.70 (0% to 70%) | Promotional price reduction rate applied at checkout. |
| **Sales** | Float | Currency ($) | \$3.00 – \$15,000.00 | Net revenue earned: $\text{Sales} = (\text{Unit\_Price} \times \text{Quantity}) \times (1 - \text{Discount})$. |
| **Profit** | Float | Currency ($) | -\$1,500.00 to \$3,500.00 | Net profit contribution: $\text{Profit} = \text{Sales} - (\text{Unit\_Cost} \times \text{Quantity})$. Can be negative if deep discounting exceeds margin. |
| **Payment_Method** | String | String | Credit Card, PayPal, Bank Transfer, Cash on Delivery | Transaction checkout settlement channel. |

---

## 3. Business Calculations & Derived Metrics
1. **Gross Revenue (Pre-Discount):**
   $$\text{Gross Sales} = \text{Unit\_Price} \times \text{Quantity}$$
2. **Net Sales Revenue:**
   $$\text{Net Sales} = \text{Gross Sales} \times (1 - \text{Discount})$$
3. **Total Cost of Goods Sold (COGS):**
   $$\text{COGS} = \text{Unit\_Cost} \times \text{Quantity}$$
4. **Net Profit:**
   $$\text{Profit} = \text{Net Sales} - \text{COGS}$$
5. **Profit Margin (%):**
   $$\text{Profit Margin} = \frac{\text{Profit}}{\text{Net Sales}} \times 100\%$$
6. **Average Order Value (AOV):**
   $$\text{AOV} = \frac{\text{Total Net Sales}}{\text{Distinct Orders Count}}$$
7. **Order Fulfillment Cycle (Days):**
   $$\text{Shipping Lead Time} = \text{Ship\_Date} - \text{Order\_Date}$$

---

## 4. Known Data Limitations & Assumptions
1. **Aggregated Unit Line Items:** Taxes and regional sales shipping fees are assumed included or net-neutral in this operational report.
2. **Returns Handling:** In the raw dataset, transaction cancellations and returns appear as dirty input records (e.g., negative quantities) that must be handled during ETL.
3. **Currency:** All financial figures are denominated in United States Dollars (USD - \$).
4. **Calendar Boundaries:** Covers 2023 to 2024. Does not reflect macroeconomic inflation indexing across year boundaries.

