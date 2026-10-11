"""
generate_raw_dataset.py
-----------------------
Generates a realistic, portfolio-grade retail sales transaction dataset
containing intentional real-world data flaws (duplicates, date format issues,
whitespace inconsistencies, missing values, and numeric edge-cases).

Schema adheres to industry standard retail analytics benchmarks (similar to Global Superstore).
"""

import os
import random
import datetime
import pandas as pd
import numpy as np

# Ensure reproducible generation
random.seed(42)
np.random.seed(42)

# Configuration
NUM_RECORDS = 2850
START_DATE = datetime.date(2023, 1, 1)
END_DATE = datetime.date(2024, 12, 31)

# Master Data Definitions
CATEGORIES = {
    "Technology": {
        "Phones": {"price_range": (150, 950), "margin_range": (0.15, 0.35)},
        "Accessories": {"price_range": (20, 180), "margin_range": (0.30, 0.55)},
        "Copiers": {"price_range": (500, 2200), "margin_range": (0.25, 0.45)},
        "Machines": {"price_range": (350, 1600), "margin_range": (0.05, 0.25)}
    },
    "Furniture": {
        "Chairs": {"price_range": (90, 450), "margin_range": (0.10, 0.28)},
        "Bookcases": {"price_range": (120, 550), "margin_range": (-0.05, 0.20)},
        "Tables": {"price_range": (200, 850), "margin_range": (-0.15, 0.15)},
        "Furnishings": {"price_range": (15, 120), "margin_range": (0.25, 0.45)}
    },
    "Office Supplies": {
        "Binders": {"price_range": (5, 65), "margin_range": (0.35, 0.60)},
        "Paper": {"price_range": (10, 80), "margin_range": (0.30, 0.50)},
        "Storage": {"price_range": (30, 220), "margin_range": (0.15, 0.35)},
        "Appliances": {"price_range": (60, 320), "margin_range": (0.20, 0.40)},
        "Art": {"price_range": (8, 55), "margin_range": (0.25, 0.50)},
        "Envelopes": {"price_range": (6, 35), "margin_range": (0.35, 0.55)},
        "Labels": {"price_range": (5, 30), "margin_range": (0.40, 0.65)},
        "Fasteners": {"price_range": (3, 20), "margin_range": (0.30, 0.55)},
        "Supplies": {"price_range": (15, 110), "margin_range": (0.10, 0.30)}
    }
}

REGIONS = {
    "West": [
        ("California", "Los Angeles", "90036"),
        ("California", "San Francisco", "94109"),
        ("California", "San Diego", "92154"),
        ("Washington", "Seattle", "98105"),
        ("Oregon", "Portland", "97206"),
        ("Arizona", "Phoenix", "85023"),
        ("Colorado", "Denver", "80219")
    ],
    "East": [
        ("New York", "New York City", "10024"),
        ("Pennsylvania", "Philadelphia", "19140"),
        ("Massachusetts", "Boston", "02116"),
        ("Ohio", "Columbus", "43229"),
        ("New Jersey", "Newark", "07102"),
        ("Maryland", "Baltimore", "21215")
    ],
    "Central": [
        ("Texas", "Houston", "77095"),
        ("Texas", "Dallas", "75217"),
        ("Illinois", "Chicago", "60653"),
        ("Michigan", "Detroit", "48227"),
        ("Minnesota", "Minneapolis", "55407"),
        ("Indiana", "Indianapolis", "46201"),
        ("Wisconsin", "Milwaukee", "53209")
    ],
    "South": [
        ("Florida", "Miami", "33180"),
        ("Florida", "Jacksonville", "32216"),
        ("Florida", "Tampa", "33612"),
        ("North Carolina", "Charlotte", "28205"),
        ("Georgia", "Atlanta", "30318"),
        ("Virginia", "Richmond", "23223"),
        ("Tennessee", "Nashville", "37211")
    ]
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
SHIP_WEIGHTS = [0.60, 0.20, 0.15, 0.05]

PAYMENT_METHODS = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
PAYMENT_WEIGHTS = [0.55, 0.25, 0.12, 0.08]

CUSTOMER_NAMES = [
    "Aarav Patel", "Emily Davis", "Michael Brown", "Jessica Taylor", "David Wilson",
    "Sophia Martinez", "James Anderson", "Olivia Thomas", "Daniel Jackson", "Emma White",
    "Christopher Harris", "Ava Martin", "Matthew Thompson", "Isabella Garcia", "Andrew Martinez",
    "Mia Robinson", "Joshua Clark", "Abigail Rodriguez", "Nathan Lewis", "Charlotte Lee",
    "Alexander Walker", "Amelia Hall", "Ethan Allen", "Harper Young", "Ryan Hernandez",
    "Evelyn King", "Lucas Wright", "Chloe Lopez", "Benjamin Hill", "Ella Scott",
    "Jacob Green", "Avery Adams", "Logan Baker", "Grace Gonzalez", "Jackson Nelson",
    "Zoey Carter", "Jack Mitchell", "Penelope Perez", "Samuel Roberts", "Riley Turner",
    "Sebastian Phillips", "Victoria Campbell", "Henry Parker", "Hannah Evans", "Owen Edwards",
    "Lillian Collins", "Gabriel Stewart", "Addison Sanchez", "Carter Morris", "Aubrey Rogers"
]

CUSTOMER_IDS = {name: f"CUST-{1000 + i}" for i, name in enumerate(CUSTOMER_NAMES)}

PRODUCT_CATALOG = []
prod_id_counter = 100
for cat, subcats in CATEGORIES.items():
    cat_code = cat[:3].upper()
    for subcat, info in subcats.items():
        sub_code = subcat[:2].upper()
        for variant in ["Standard", "Pro", "Plus", "Enterprise", "Eco"]:
            prod_name = f"{subcat[:-1] if subcat.endswith('s') else subcat} {variant} Edition"
            prod_id = f"{cat_code}-{sub_code}-{prod_id_counter}"
            prod_id_counter += 1
            min_p, max_p = info["price_range"]
            unit_price = round(random.uniform(min_p, max_p), 2)
            base_margin = random.uniform(*info["margin_range"])
            unit_cost = round(unit_price * (1.0 - base_margin), 2)
            PRODUCT_CATALOG.append({
                "product_id": prod_id,
                "category": cat,
                "sub_category": subcat,
                "product_name": prod_name,
                "unit_price": unit_price,
                "unit_cost": unit_cost
            })

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + datetime.timedelta(days=random_days)

# Generate Records
records = []
total_days = (END_DATE - START_DATE).days

for i in range(1, NUM_RECORDS + 1):
    order_id = f"ORD-{2023 + (1 if random.random() > 0.48 else 0)}-{10000 + i}"
    
    # Seasonality weighting: Q4 (Nov, Dec) higher sales volume
    dt = random_date(START_DATE, END_DATE)
    if random.random() < 0.25:
        # Boost Q4
        year = dt.year
        month = random.choice([11, 12])
        day = random.randint(1, 28)
        dt = datetime.date(year, month, day)
    
    order_date = dt
    ship_delay = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.1, 0.25, 0.35, 0.15, 0.08, 0.05, 0.02])[0]
    ship_date = order_date + datetime.timedelta(days=ship_delay)
    
    ship_mode = random.choices(SHIP_MODES, weights=SHIP_WEIGHTS)[0]
    cust_name = random.choice(CUSTOMER_NAMES)
    cust_id = CUSTOMER_IDS[cust_name]
    segment = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    
    region = random.choice(list(REGIONS.keys()))
    state, city, postal = random.choice(REGIONS[region])
    
    prod = random.choice(PRODUCT_CATALOG)
    qty = random.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[0.35, 0.28, 0.16, 0.10, 0.05, 0.03, 0.02, 0.01])[0]
    
    # Realistic discount policy
    # Higher discount on Tables and Binders occasionally
    discount = random.choices([0.0, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.70],
                              weights=[0.50, 0.18, 0.12, 0.08, 0.05, 0.03, 0.03, 0.01])[0]
    
    # Financials
    gross_sales = round(prod["unit_price"] * qty, 2)
    sales = round(gross_sales * (1.0 - discount), 2)
    total_cost = round(prod["unit_cost"] * qty, 2)
    profit = round(sales - total_cost, 2)
    
    payment = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS)[0]
    
    records.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Ship_Date": ship_date.strftime("%Y-%m-%d"),
        "Ship_Mode": ship_mode,
        "Customer_ID": cust_id,
        "Customer_Name": cust_name,
        "Segment": segment,
        "Country": "United States",
        "City": city,
        "State": state,
        "Postal_Code": postal,
        "Region": region,
        "Product_ID": prod["product_id"],
        "Category": prod["category"],
        "Sub_Category": prod["sub_category"],
        "Product_Name": prod["product_name"],
        "Unit_Price": prod["unit_price"],
        "Unit_Cost": prod["unit_cost"],
        "Quantity": qty,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "Payment_Method": payment
    })

df = pd.DataFrame(records)

# --- INJECT REALISTIC DATA QUALITY DEFECTS (For Data Cleaning Phase) ---
print(f"Injecting intentional data flaws into raw dataset...")

# 1. Duplicate Rows (Simulating POS re-transmissions / sync duplicates)
duplicate_indices = random.sample(range(len(df)), 18)
df_duplicates = df.iloc[duplicate_indices].copy()
df = pd.concat([df, df_duplicates], ignore_index=True)
print(f" -> Added 18 duplicate records.")

# 2. Inconsistent Date Formats (e.g., DD/MM/YYYY vs YYYY-MM-DD vs MM/DD/YYYY)
date_flaw_indices = random.sample(range(len(df)), 55)
for idx in date_flaw_indices[:28]:
    d = datetime.datetime.strptime(df.at[idx, "Order_Date"], "%Y-%m-%d")
    df.at[idx, "Order_Date"] = d.strftime("%d/%m/%Y")  # European / DD/MM/YYYY
for idx in date_flaw_indices[28:]:
    d = datetime.datetime.strptime(df.at[idx, "Order_Date"], "%Y-%m-%d")
    df.at[idx, "Order_Date"] = d.strftime("%m/%d/%Y")  # US style

# 3. Text Inconsistencies & Leading/Trailing Whitespace
text_flaw_indices = random.sample(range(len(df)), 60)
for idx in text_flaw_indices[:20]:
    df.at[idx, "Category"] = "  " + df.at[idx, "Category"].lower() + " "
for idx in text_flaw_indices[20:40]:
    df.at[idx, "Region"] = df.at[idx, "Region"].upper() + "  "
for idx in text_flaw_indices[40:]:
    df.at[idx, "Segment"] = " " + df.at[idx, "Segment"] + "  "

# 4. Missing Values (Blanks / NaN in non-critical descriptive fields)
missing_cust_indices = random.sample(range(len(df)), 12)
for idx in missing_cust_indices:
    df.at[idx, "Customer_Name"] = np.nan

missing_zip_indices = random.sample(range(len(df)), 15)
for idx in missing_zip_indices:
    df.at[idx, "Postal_Code"] = np.nan

# 5. Outliers and Data Entry Typos
typo_indices = random.sample(range(len(df)), 5)
# One negative quantity (return recorded as negative sales)
df.at[typo_indices[0], "Quantity"] = -2
# One discount entered as percentage integer instead of decimal (e.g. 20 instead of 0.20)
df.at[typo_indices[1], "Discount"] = 2.0
# Outlier sales amount due to extra zero key-in
df.at[typo_indices[2], "Sales"] = 45000.00

# 6. Postal codes with leading zero lost (e.g. 02116 -> 2116 or 07102 -> 7102)
leading_zero_indices = df[df["Postal_Code"].str.startswith("0", na=False)].index
for idx in leading_zero_indices[:15]:
    val = df.at[idx, "Postal_Code"]
    if pd.notna(val) and val.startswith("0"):
        df.at[idx, "Postal_Code"] = str(int(val))

# Shuffle dataset
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

# Save Raw Dataset
output_raw_csv = os.path.join("data", "raw", "raw_retail_sales.csv")
df.to_csv(output_raw_csv, index=False)
print(f"Successfully generated raw retail sales dataset with {len(df)} rows at: {output_raw_csv}")

