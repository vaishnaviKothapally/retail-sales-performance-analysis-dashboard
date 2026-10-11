"""
generate_dashboard_visuals.py
-----------------------------
Generates high-resolution dashboard visuals & screenshots
for GitHub documentation and portfolio presentation.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

CSV_PATH = os.path.join("data", "cleaned", "cleaned_retail_sales.csv")
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)

def generate_dashboard_preview():
    print("Generating comprehensive Executive Dashboard visual preview...")
    fig = plt.figure(figsize=(16, 10), facecolor="#F8FAFC")
    gs = fig.add_gridspec(3, 3, height_ratios=[0.45, 1.2, 1.2], hspace=0.35, wspace=0.25)

    # 1. Title Banner
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis("off")
    ax_title.fill_between([0, 1], 0, 1, color="#0F172A", transform=ax_title.transAxes)
    ax_title.text(0.5, 0.65, "RETAIL SALES PERFORMANCE ANALYSIS & EXECUTIVE DASHBOARD",
                  ha="center", va="center", color="#FFFFFF", fontsize=16, weight="bold")
    ax_title.text(0.5, 0.25, "Omnichannel Performance Monitoring | 2,850 Orders | FY 2023 - 2024 | Reconciled Audit",
                  ha="center", va="center", color="#94A3B8", fontsize=10, style="italic")

    # KPI Sub-cards embedded in Title area
    # KPI 1: Sales
    ax_kpi1 = fig.add_axes([0.10, 0.80, 0.18, 0.08], facecolor="#FFFFFF")
    ax_kpi1.text(0.5, 0.7, "TOTAL NET SALES", ha="center", va="center", color="#64748B", fontsize=8, weight="bold")
    ax_kpi1.text(0.5, 0.35, "$1,845,890", ha="center", va="center", color="#0F172A", fontsize=14, weight="bold")
    ax_kpi1.text(0.5, 0.1, "YoY: +12.9% | AOV: $648", ha="center", va="center", color="#2563EB", fontsize=7)
    ax_kpi1.axis("off")
    for spine in ax_kpi1.spines.values():
        spine.set_edgecolor("#CBD5E1")

    # KPI 2: Profit
    ax_kpi2 = fig.add_axes([0.31, 0.80, 0.18, 0.08], facecolor="#FFFFFF")
    ax_kpi2.text(0.5, 0.7, "NET PROFIT", ha="center", va="center", color="#64748B", fontsize=8, weight="bold")
    ax_kpi2.text(0.5, 0.35, "$255,342", ha="center", va="center", color="#0F172A", fontsize=14, weight="bold")
    ax_kpi2.text(0.5, 0.1, "Net Margin Contribution", ha="center", va="center", color="#059669", fontsize=7)
    ax_kpi2.axis("off")

    # KPI 3: Margin %
    ax_kpi3 = fig.add_axes([0.52, 0.80, 0.18, 0.08], facecolor="#FFFFFF")
    ax_kpi3.text(0.5, 0.7, "PROFIT MARGIN %", ha="center", va="center", color="#64748B", fontsize=8, weight="bold")
    ax_kpi3.text(0.5, 0.35, "13.83%", ha="center", va="center", color="#0F172A", fontsize=14, weight="bold")
    ax_kpi3.text(0.5, 0.1, "Target: 15.0% | Bleed: Furniture", ha="center", va="center", color="#D97706", fontsize=7)
    ax_kpi3.axis("off")

    # KPI 4: Orders
    ax_kpi4 = fig.add_axes([0.73, 0.80, 0.18, 0.08], facecolor="#FFFFFF")
    ax_kpi4.text(0.5, 0.7, "TOTAL TRANSACTIONS", ha="center", va="center", color="#64748B", fontsize=8, weight="bold")
    ax_kpi4.text(0.5, 0.35, "2,850 Orders", ha="center", va="center", color="#0F172A", fontsize=14, weight="bold")
    ax_kpi4.text(0.5, 0.1, "7,204 Units | 50 Clients", ha="center", va="center", color="#6366F1", fontsize=7)
    ax_kpi4.axis("off")

    # 2. Panel 1: Monthly Trend Line Chart (gs[1, :2])
    ax_trend = fig.add_subplot(gs[1, :2])
    monthly = df.groupby("Order_Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    ax_trend.plot(monthly["Order_Month"], monthly["Sales"], color="#2563EB", lw=2.5, marker="o", markersize=4, label="Net Sales ($)")
    ax_trend.plot(monthly["Order_Month"], monthly["Profit"], color="#059669", lw=2.5, marker="s", markersize=4, label="Net Profit ($)")
    ax_trend.set_title("Monthly Net Sales & Profit Trajectory (2023 - 2024)", fontsize=11, weight="bold", color="#1E293B", pad=10)
    ax_trend.set_ylabel("USD ($)", fontsize=9, color="#475569")
    ax_trend.tick_params(axis="x", rotation=45, labelsize=8)
    ax_trend.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax_trend.legend(frameon=True, facecolor="#FFFFFF", fontsize=8)
    ax_trend.grid(True, linestyle="--", alpha=0.5)

    # 3. Panel 2: Category Revenue vs Profit (gs[1, 2])
    ax_cat = fig.add_subplot(gs[1, 2])
    cat_summary = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    x = np.arange(len(cat_summary))
    w = 0.35
    ax_cat.bar(x - w/2, cat_summary["Sales"] / 1000, width=w, label="Sales ($k)", color="#3B82F6", edgecolor="none")
    ax_cat.bar(x + w/2, cat_summary["Profit"] / 1000, width=w, label="Profit ($k)", color="#10B981", edgecolor="none")
    ax_cat.set_xticks(x)
    ax_cat.set_xticklabels(cat_summary["Category"], fontsize=8, weight="bold")
    ax_cat.set_title("Category Sales vs. Profit ($k)", fontsize=11, weight="bold", color="#1E293B", pad=10)
    ax_cat.set_ylabel("USD ($ Thousands)", fontsize=9, color="#475569")
    ax_cat.legend(frameon=True, facecolor="#FFFFFF", fontsize=8)
    ax_cat.grid(True, linestyle="--", alpha=0.5)

    # 4. Panel 3: Regional Performance (gs[2, 0])
    ax_reg = fig.add_subplot(gs[2, 0])
    reg_summary = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index().sort_values(by="Sales", ascending=False)
    x_r = np.arange(len(reg_summary))
    ax_reg.bar(x_r - w/2, reg_summary["Sales"] / 1000, width=w, label="Sales ($k)", color="#1E40AF")
    ax_reg.bar(x_r + w/2, reg_summary["Profit"] / 1000, width=w, label="Profit ($k)", color="#047857")
    ax_reg.set_xticks(x_r)
    ax_reg.set_xticklabels(reg_summary["Region"], fontsize=8, weight="bold")
    ax_reg.set_title("Regional Distribution ($k)", fontsize=11, weight="bold", color="#1E293B", pad=10)
    ax_reg.set_ylabel("USD ($ Thousands)", fontsize=8, color="#475569")
    ax_reg.legend(frameon=True, facecolor="#FFFFFF", fontsize=7)
    ax_reg.grid(True, linestyle="--", alpha=0.5)

    # 5. Panel 4: Customer Segment Share (gs[2, 1])
    ax_seg = fig.add_subplot(gs[2, 1])
    seg_summary = df.groupby("Segment")["Sales"].sum()
    colors = ["#2563EB", "#60A5FA", "#93C5FD"]
    wedges, texts, autotexts = ax_seg.pie(seg_summary, labels=seg_summary.index, autopct="%1.1f%%",
                                          colors=colors, startangle=140,
                                          textprops={'fontsize': 8, 'weight': 'bold'})
    for at in autotexts:
        at.set_color("white")
    ax_seg.set_title("Revenue by Customer Segment", fontsize=11, weight="bold", color="#1E293B", pad=10)

    # 6. Panel 5: Top 7 Products by Profit (gs[2, 2])
    ax_top = fig.add_subplot(gs[2, 2])
    top_prods = df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=True).tail(7)
    y_pos = np.arange(len(top_prods))
    ax_top.barh(y_pos, top_prods / 1000, color="#6366F1", edgecolor="none")
    ax_top.set_yticks(y_pos)
    ax_top.set_yticklabels([p[:20] for p in top_prods.index], fontsize=7)
    ax_top.set_title("Top Products by Net Profit ($k)", fontsize=11, weight="bold", color="#1E293B", pad=10)
    ax_top.set_xlabel("Net Profit ($ Thousands)", fontsize=8, color="#475569")
    ax_top.grid(True, linestyle="--", alpha=0.5)

    out_preview = os.path.join(ASSETS_DIR, "dashboard_preview.png")
    plt.savefig(out_preview, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved dashboard preview image to {out_preview}")

def generate_discount_cliff():
    print("Generating Discount Cliff analysis visual...")
    fig, ax1 = plt.subplots(figsize=(10, 5), facecolor="#F8FAFC")
    
    disc_summary = df.groupby("Discount").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    disc_summary["Margin%"] = (disc_summary["Profit"] / disc_summary["Sales"]) * 100
    disc_summary["Discount_Label"] = (disc_summary["Discount"] * 100).astype(int).astype(str) + "%"

    x = np.arange(len(disc_summary))
    bars = ax1.bar(x, disc_summary["Margin%"], color=[
        "#059669" if m >= 15 else ("#10B981" if m >= 5 else ("#F59E0B" if m >= 0 else "#EF4444"))
        for m in disc_summary["Margin%"]
    ], width=0.55)

    ax1.axhline(0, color="#0F172A", lw=1.2, linestyle="-")
    ax1.set_xticks(x)
    ax1.set_xticklabels(disc_summary["Discount_Label"], fontsize=10, weight="bold")
    ax1.set_title("The 'Discount Cliff': Profit Margin % Collapse by Promotional Discount Tier", fontsize=12, weight="bold", color="#1E293B", pad=15)
    ax1.set_xlabel("Promotional Discount Tier Applied", fontsize=10, weight="bold", color="#334155")
    ax1.set_ylabel("Net Operating Margin (%)", fontsize=10, weight="bold", color="#334155")
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    for bar in bars:
        h = bar.get_height()
        va = "bottom" if h >= 0 else "top"
        ax1.annotate(f"{h:.1f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3 if h >= 0 else -10),
                     textcoords="offset points",
                     ha="center", va=va, fontsize=8, weight="bold")

    ax1.grid(True, linestyle="--", alpha=0.4)
    out_cliff = os.path.join(ASSETS_DIR, "discount_cliff_analysis.png")
    plt.savefig(out_cliff, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved discount cliff image to {out_cliff}")

if __name__ == "__main__":
    generate_dashboard_preview()
    generate_discount_cliff()

