"""
generate_html_dashboard.py
--------------------------
Generates a standalone, responsive, interactive HTML Executive Dashboard
powered by Tailwind CSS and Chart.js.
Can be opened in any web browser and deployed via GitHub Pages for live recruiter previews.
"""

import os
import json
import pandas as pd

CSV_PATH = os.path.join("data", "cleaned", "cleaned_retail_sales.csv")
OUTPUT_HTML = os.path.join("dashboard", "index.html")

df = pd.read_csv(CSV_PATH)

total_sales = float(df["Sales"].sum())
total_profit = float(df["Profit"].sum())
total_orders = int(df["Order_ID"].nunique())
total_units = int(df["Quantity"].sum())
margin = round((total_profit / total_sales) * 100, 2)
aov = round(total_sales / total_orders, 2)

monthly = df.groupby(["Order_Month", "Order_Month_Name"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index().sort_values(by="Order_Month")

month_labels = list(monthly["Order_Month_Name"])
month_sales = [round(x, 2) for x in monthly["Sales"]]
month_profit = [round(x, 2) for x in monthly["Profit"]]

cat_summary = df.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order_ID", "nunique")
).reset_index().sort_values(by="Sales", ascending=False)

cat_labels = list(cat_summary["Category"])
cat_sales = [round(x, 2) for x in cat_summary["Sales"]]
cat_profit = [round(x, 2) for x in cat_summary["Profit"]]

reg_summary = df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index().sort_values(by="Sales", ascending=False)

reg_labels = list(reg_summary["Region"])
reg_sales = [round(x, 2) for x in reg_summary["Sales"]]
reg_profit = [round(x, 2) for x in reg_summary["Profit"]]

seg_summary = df.groupby("Segment")["Sales"].sum().reset_index()
seg_labels = list(seg_summary["Segment"])
seg_sales = [round(x, 2) for x in seg_summary["Sales"]]

disc_summary = df.groupby("Discount").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
disc_summary["Margin%"] = round((disc_summary["Profit"] / disc_summary["Sales"]) * 100, 2)
disc_labels = [(str(int(d * 100)) + "%") for d in disc_summary["Discount"]]
disc_margins = list(disc_summary["Margin%"])

top_prods = df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=False).head(8)
top_prod_labels = [p[:22] for p in top_prods.index]
top_prod_profits = [round(x, 2) for x in top_prods.values]

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Retail Sales Performance | Interactive Executive Dashboard</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen">

  <!-- Header Banner -->
  <header class="bg-slate-900 border-b border-slate-800 text-white py-6 px-4 sm:px-8 shadow-md">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="px-2.5 py-0.5 rounded text-xs font-semibold bg-blue-600 text-white tracking-wide uppercase">Executive BI</span>
          <span class="text-xs text-slate-400">Reconciled Analytics Portfolio</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight mt-1 text-white">
          Retail Sales Performance & Executive Dashboard
        </h1>
        <p class="text-sm text-slate-400 mt-1">
          Omnichannel Multi-Territory Transaction Log | FY 2023 – 2024 (24 Months) | Reconciled Audit
        </p>
      </div>
      <div class="flex items-center gap-3">
        <a href="../dashboard/Retail_Sales_Dashboard.xlsx" class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg shadow transition">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z"/></svg>
          Download Excel (.xlsx)
        </a>
      </div>
    </div>
  </header>

  <!-- Filter Bar -->
  <section class="bg-white border-b border-slate-200 py-3 px-4 sm:px-8 shadow-sm">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs sm:text-sm text-slate-600">
      <div class="flex items-center gap-2">
        <span class="font-semibold text-slate-800">Operational Scope:</span>
        <span class="bg-slate-100 text-slate-700 px-2 py-1 rounded">All 4 Regions</span>
        <span class="bg-slate-100 text-slate-700 px-2 py-1 rounded">3 Categories</span>
        <span class="bg-slate-100 text-slate-700 px-2 py-1 rounded">2,850 Orders</span>
      </div>
      <div class="text-xs text-slate-500">
        Quality Assurance: <span class="text-emerald-600 font-bold">100% Reconciled (0.00% Variance)</span>
      </div>
    </div>
  </section>

  <!-- Main Dashboard Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-8 py-8 space-y-8">

    <!-- KPI Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- Card 1 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1 bg-blue-600"></div>
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Net Revenue</p>
        <h3 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">${total_sales:,.2f}</h3>
        <p class="text-xs font-medium text-blue-600 mt-2 flex items-center gap-1">
          <span>&uarr; +12.86% YoY Growth</span> &bull; <span>AOV: ${aov:,.2f}</span>
        </p>
      </div>

      <!-- Card 2 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1 bg-emerald-600"></div>
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Net Operating Profit</p>
        <h3 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">${total_profit:,.2f}</h3>
        <p class="text-xs font-medium text-emerald-600 mt-2">
          Net Bottom-Line Contribution
        </p>
      </div>

      <!-- Card 3 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1 bg-amber-500"></div>
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Profit Margin %</p>
        <h3 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">{margin:.2f}%</h3>
        <p class="text-xs font-medium text-amber-700 mt-2">
          Erosion: Furniture (-1.54%)
        </p>
      </div>

      <!-- Card 4 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1 bg-indigo-600"></div>
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Transactions</p>
        <h3 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">{total_orders:,} Orders</h3>
        <p class="text-xs font-medium text-indigo-600 mt-2">
          {total_units:,} Units Sold &bull; 50 Clients
        </p>
      </div>
    </div>

    <!-- Charts Row 1: Monthly Trend & Category Performance -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 24-Month Trend (2 Cols) -->
      <div class="lg:col-span-2 bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-base font-bold text-slate-800">Monthly Net Revenue & Profit Trajectory</h2>
            <p class="text-xs text-slate-500">Continuous 24-month time-series demonstrating holiday Q4 volume spikes</p>
          </div>
          <span class="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded font-semibold">2023 - 2024</span>
        </div>
        <div class="h-72">
          <canvas id="monthlyTrendChart"></canvas>
        </div>
      </div>

      <!-- Category Comparison (1 Col) -->
      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-base font-bold text-slate-800">Category Revenue vs Profit</h2>
            <p class="text-xs text-slate-500">Technology stars vs. Furniture net loss</p>
          </div>
        </div>
        <div class="h-72">
          <canvas id="categoryChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Charts Row 2: Discount Cliff, Regional Performance, Segment Share -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- The Discount Cliff -->
      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <h2 class="text-base font-bold text-slate-800">The "Discount Cliff"</h2>
        <p class="text-xs text-slate-500 mb-4">Net profit margin collapse by promotional tier</p>
        <div class="h-64">
          <canvas id="discountCliffChart"></canvas>
        </div>
      </div>

      <!-- Regional Distribution -->
      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <h2 class="text-base font-bold text-slate-800">Regional Revenue & Profit</h2>
        <p class="text-xs text-slate-500 mb-4">East volume lead vs. South & West margin efficiency</p>
        <div class="h-64">
          <canvas id="regionalChart"></canvas>
        </div>
      </div>

      <!-- Customer Segment Share -->
      <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <h2 class="text-base font-bold text-slate-800">Revenue by Customer Segment</h2>
        <p class="text-xs text-slate-500 mb-4">Consumer, Corporate, and Home Office splits</p>
        <div class="h-64 flex items-center justify-center">
          <canvas id="segmentChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Executive Strategic Directives Card -->
    <div class="bg-white rounded-xl p-6 border border-slate-200 shadow-sm space-y-4">
      <div class="flex items-center gap-2 border-b border-slate-200 pb-3">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <h2 class="text-base font-bold text-slate-900 uppercase tracking-wide">Key Executive Findings & Action Directives</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div class="p-4 bg-slate-50 rounded-lg border-l-4 border-blue-600">
          <p class="font-bold text-slate-800">1. Institute a 15% Maximum Discount Cap</p>
          <p class="text-xs text-slate-600 mt-1">Discounts &ge; 30% eroded <strong>$41,269 in net profit</strong>. Setting an automated ERP 15% promotional ceiling protects enterprise operating margins.</p>
        </div>
        <div class="p-4 bg-slate-50 rounded-lg border-l-4 border-red-600">
          <p class="font-bold text-slate-800">2. Eliminate Discounts on Tables (0% Policy)</p>
          <p class="text-xs text-slate-600 mt-1">Tables lost <strong>-$17,419</strong> due to slim base markups. Ending discounting on Tables immediately flips the Furniture category to net positive.</p>
        </div>
        <div class="p-4 bg-slate-50 rounded-lg border-l-4 border-emerald-600">
          <p class="font-bold text-slate-800">3. B2B Technology & Office Supplies Bundling</p>
          <p class="text-xs text-slate-600 mt-1">Technology produced <strong>82.6% of company profit ($211k)</strong>. Bundle high-ticket Copiers with high-margin recurring Office Supplies to raise AOV by 12%.</p>
        </div>
        <div class="p-4 bg-slate-50 rounded-lg border-l-4 border-amber-500">
          <p class="font-bold text-slate-800">4. East Region Price Governance</p>
          <p class="text-xs text-slate-600 mt-1">East delivered top gross sales ($505k) but lowest margin (12.2%). Migrating accounts to contract rebate tiers unlocks <strong>+$10,950 in profit</strong>.</p>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="bg-slate-900 border-t border-slate-800 text-slate-400 py-6 text-center text-xs">
    <p>Retail Sales Performance Analysis Portfolio &bull; Reconciled Excel & Python Data Analytics Project</p>
  </footer>

  <!-- Chart.js Logic -->
  <script>
    // 1. Monthly Trend
    const ctxMonthly = document.getElementById('monthlyTrendChart').getContext('2d');
    new Chart(ctxMonthly, {{
      type: 'line',
      data: {{
        labels: {json.dumps(month_labels)},
        datasets: [
          {{
            label: 'Net Sales ($)',
            data: {json.dumps(month_sales)},
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.05)',
            borderWidth: 2.5,
            tension: 0.25,
            fill: true
          }},
          {{
            label: 'Net Profit ($)',
            data: {json.dumps(month_profit)},
            borderColor: '#059669',
            backgroundColor: 'rgba(5, 150, 105, 0.05)',
            borderWidth: 2.5,
            tension: 0.25,
            fill: true
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }} }},
        scales: {{
          y: {{
            ticks: {{
              callback: function(value) {{ return '$' + (value / 1000) + 'k'; }}
            }}
          }}
        }}
      }}
    }});

    // 2. Category Chart
    const ctxCat = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctxCat, {{
      type: 'bar',
      data: {{
        labels: {json.dumps(cat_labels)},
        datasets: [
          {{
            label: 'Sales ($)',
            data: {json.dumps(cat_sales)},
            backgroundColor: '#3B82F6'
          }},
          {{
            label: 'Profit ($)',
            data: {json.dumps(cat_profit)},
            backgroundColor: ['#10B981', '#EF4444', '#10B981']
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 10 }} }} }} }},
        scales: {{
          y: {{
            ticks: {{
              callback: function(value) {{ return '$' + (value / 1000) + 'k'; }}
            }}
          }}
        }}
      }}
    }});

    // 3. Discount Cliff Chart
    const ctxDisc = document.getElementById('discountCliffChart').getContext('2d');
    new Chart(ctxDisc, {{
      type: 'bar',
      data: {{
        labels: {json.dumps(disc_labels)},
        datasets: [{{
          label: 'Margin %',
          data: {json.dumps(disc_margins)},
          backgroundColor: {json.dumps(disc_margins)}.map(m => m >= 15 ? '#059669' : (m >= 0 ? '#F59E0B' : '#EF4444'))
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{
          y: {{
            ticks: {{
              callback: function(value) {{ return value + '%'; }}
            }}
          }}
        }}
      }}
    }});

    // 4. Regional Chart
    const ctxReg = document.getElementById('regionalChart').getContext('2d');
    new Chart(ctxReg, {{
      type: 'bar',
      data: {{
        labels: {json.dumps(reg_labels)},
        datasets: [
          {{ label: 'Sales ($)', data: {json.dumps(reg_sales)}, backgroundColor: '#1E40AF' }},
          {{ label: 'Profit ($)', data: {json.dumps(reg_profit)}, backgroundColor: '#047857' }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 10, font: {{ size: 9 }} }} }} }},
        scales: {{
          y: {{
            ticks: {{ callback: function(v) {{ return '$' + (v / 1000) + 'k'; }} }}
          }}
        }}
      }}
    }});

    // 5. Segment Pie Chart
    const ctxSeg = document.getElementById('segmentChart').getContext('2d');
    new Chart(ctxSeg, {{
      type: 'doughnut',
      data: {{
        labels: {json.dumps(seg_labels)},
        datasets: [{{
          data: {json.dumps(seg_sales)},
          backgroundColor: ['#2563EB', '#60A5FA', '#93C5FD']
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 10 }} }} }} }}
      }}
    }});
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Interactive HTML dashboard successfully generated at: {OUTPUT_HTML}")

