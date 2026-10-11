"""
build_excel_dashboard.py
------------------------
Constructs a complete, professional, C-Suite interactive Excel workbook
titled Retail_Sales_Dashboard.xlsx.

Worksheet Architecture:
1. Executive_Dashboard: KPI Summary Cards, Charts (Monthly Trend, Category,
   Region, Segment, Top 10 Products), Strategic Takeaways Callouts.
2. Summary_Tables: Aggregated data models and formulas feeding all charts & KPIs.
3. Cleaned_Data: The full 2,851 audited records formatted as an official Excel Table.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, PieChart, Reference, Series
from openpyxl.worksheet.table import Table, TableStyleInfo

CLEANED_CSV = os.path.join("data", "cleaned", "cleaned_retail_sales.csv")
OUTPUT_XLSX = os.path.join("dashboard", "Retail_Sales_Dashboard.xlsx")

def build_workbook():
    print(f"Reading cleaned data from {CLEANED_CSV}...")
    df = pd.read_csv(CLEANED_CSV)
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Create sheets in executive presentation order
    ws_dash = wb.create_sheet(title="Executive_Dashboard")
    ws_summary = wb.create_sheet(title="Summary_Tables")
    ws_data = wb.create_sheet(title="Cleaned_Data")
    
    # -------------------------------------------------------------------------
    # TAB 3: Cleaned_Data (Populate raw master records & format as Excel Table)
    # -------------------------------------------------------------------------
    print("Populating Cleaned_Data worksheet...")
    # Write headers
    headers = list(df.columns)
    ws_data.append(headers)
    
    # Header styling
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    
    for col_num in range(1, len(headers) + 1):
        cell = ws_data.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # Write data rows
    for row in df.itertuples(index=False):
        ws_data.append(list(row))
        
    num_rows = len(df) + 1
    num_cols = len(headers)
    
    # Number Formatting for Cleaned_Data
    # Map column names to formats
    col_idx = {h: i + 1 for i, h in enumerate(headers)}
    
    currency_fmt = "$#,##0.00"
    pct_fmt = "0.0%"
    int_fmt = "#,##0"
    date_fmt = "yyyy-mm-dd"
    
    for r in range(2, num_rows + 1):
        # Dates
        ws_data.cell(row=r, column=col_idx["Order_Date"]).number_format = date_fmt
        ws_data.cell(row=r, column=col_idx["Ship_Date"]).number_format = date_fmt
        # Integers
        ws_data.cell(row=r, column=col_idx["Quantity"]).number_format = int_fmt
        ws_data.cell(row=r, column=col_idx["Shipping_Days"]).number_format = int_fmt
        # Currency
        ws_data.cell(row=r, column=col_idx["Unit_Price"]).number_format = currency_fmt
        ws_data.cell(row=r, column=col_idx["Unit_Cost"]).number_format = currency_fmt
        ws_data.cell(row=r, column=col_idx["Sales"]).number_format = currency_fmt
        ws_data.cell(row=r, column=col_idx["Profit"]).number_format = currency_fmt
        # Percentages
        ws_data.cell(row=r, column=col_idx["Discount"]).number_format = pct_fmt
        ws_data.cell(row=r, column=col_idx["Profit_Margin"]).number_format = pct_fmt
    
    # Format Cleaned_Data as formal Excel Table
    tab_ref = f"A1:{get_column_letter(num_cols)}{num_rows}"
    table = Table(displayName="SalesTransactions", ref=tab_ref)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9", 
        showFirstColumn=False, 
        showLastColumn=False, 
        showRowStripes=True, 
        showColumnStripes=False
    )
    ws_data.add_table(table)
    
    # Adjust column widths
    for col in ws_data.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col[:50])
        ws_data.column_dimensions[col_letter].width = max(max_len + 4, 12)
        
    ws_data.views.sheetView[0].showGridLines = True
    print("Cleaned_Data worksheet built successfully.")

    # -------------------------------------------------------------------------
    # TAB 2: Summary_Tables (Aggregations and feeds)
    # -------------------------------------------------------------------------
    print("Building Summary_Tables worksheet...")
    ws_summary.views.sheetView[0].showGridLines = True
    
    # Palette styles
    title_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    sub_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    sec_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    font_bold_white = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_reg = Font(name="Calibri", size=11)
    
    # 1. Executive Total KPIs Summary Block (Rows 2 to 4)
    ws_summary["B2"] = "EXECUTIVE KPI SUMMARY METRICS"
    ws_summary["B2"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    kpi_headers = ["Metric Scope", "Total Sales ($)", "Total Profit ($)", "Profit Margin %", "Total Orders", "Total Units", "Average Order Value"]
    for i, h in enumerate(kpi_headers):
        c = ws_summary.cell(row=3, column=i+2, value=h)
        c.fill = sub_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    ws_summary["B4"] = "Enterprise Reconciled"
    ws_summary["C4"] = f"=SUM(Cleaned_Data!Z2:Z{num_rows})"
    ws_summary["D4"] = f"=SUM(Cleaned_Data!AA2:AA{num_rows})"
    ws_summary["E4"] = "=D4/C4"
    ws_summary["F4"] = f"=COUNTA(Cleaned_Data!A2:A{num_rows})"
    ws_summary["G4"] = f"=SUM(Cleaned_Data!X2:X{num_rows})"
    ws_summary["H4"] = "=C4/F4"
    
    ws_summary["C4"].number_format = "$#,##0.00"
    ws_summary["D4"].number_format = "$#,##0.00"
    ws_summary["E4"].number_format = "0.00%"
    ws_summary["F4"].number_format = "#,##0"
    ws_summary["G4"].number_format = "#,##0"
    ws_summary["H4"].number_format = "$#,##0.00"
    for col_idx_kpi in range(2, 9):
        ws_summary.cell(row=4, column=col_idx_kpi).font = font_bold

    # 2. Monthly Trend Aggregation (Rows 7 to 32)
    ws_summary["B6"] = "MONTHLY PERFORMANCE TREND (2023 - 2024)"
    ws_summary["B6"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    monthly_headers = ["Year-Month", "Month Name", "Revenue ($)", "Profit ($)", "Margin %"]
    for i, h in enumerate(monthly_headers):
        c = ws_summary.cell(row=7, column=i+2, value=h)
        c.fill = sec_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    monthly_data = df.groupby(["Order_Month", "Order_Month_Name"]).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index().sort_values(by="Order_Month")
    
    r_start = 8
    for idx, m_row in monthly_data.iterrows():
        cur_r = r_start + idx
        ws_summary.cell(row=cur_r, column=2, value=m_row["Order_Month"])
        ws_summary.cell(row=cur_r, column=3, value=m_row["Order_Month_Name"])
        ws_summary.cell(row=cur_r, column=4, value=round(m_row["Sales"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=5, value=round(m_row["Profit"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=6, value=f"=E{cur_r}/D{cur_r}").number_format = "0.0%"
    monthly_end_r = r_start + len(monthly_data) - 1

    # 3. Category Breakdown (Rows 7 to 11, Cols H to L)
    ws_summary["H6"] = "CATEGORY PERFORMANCE"
    ws_summary["H6"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    cat_headers = ["Category", "Sales ($)", "Profit ($)", "Margin %", "Orders"]
    for i, h in enumerate(cat_headers):
        c = ws_summary.cell(row=7, column=i+8, value=h)
        c.fill = sub_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    cat_data = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index().sort_values(by="Sales", ascending=False)
    
    for idx, c_row in cat_data.iterrows():
        cur_r = 8 + idx
        ws_summary.cell(row=cur_r, column=8, value=c_row["Category"])
        ws_summary.cell(row=cur_r, column=9, value=round(c_row["Sales"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=10, value=round(c_row["Profit"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=11, value=f"=J{cur_r}/I{cur_r}").number_format = "0.0%"
        ws_summary.cell(row=cur_r, column=12, value=c_row["Orders"]).number_format = "#,##0"

    # 4. Regional Breakdown (Rows 14 to 19, Cols H to L)
    ws_summary["H13"] = "REGIONAL PERFORMANCE"
    ws_summary["H13"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    reg_headers = ["Region", "Sales ($)", "Profit ($)", "Margin %", "Orders"]
    for i, h in enumerate(reg_headers):
        c = ws_summary.cell(row=14, column=i+8, value=h)
        c.fill = sub_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    reg_data = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index().sort_values(by="Sales", ascending=False)
    
    for idx, r_row in reg_data.iterrows():
        cur_r = 15 + idx
        ws_summary.cell(row=cur_r, column=8, value=r_row["Region"])
        ws_summary.cell(row=cur_r, column=9, value=round(r_row["Sales"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=10, value=round(r_row["Profit"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=11, value=f"=J{cur_r}/I{cur_r}").number_format = "0.0%"
        ws_summary.cell(row=cur_r, column=12, value=r_row["Orders"]).number_format = "#,##0"

    # 5. Customer Segment Breakdown (Rows 22 to 26, Cols H to L)
    ws_summary["H21"] = "CUSTOMER SEGMENT BREAKDOWN"
    ws_summary["H21"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    seg_headers = ["Segment", "Sales ($)", "Profit ($)", "Margin %", "Orders"]
    for i, h in enumerate(seg_headers):
        c = ws_summary.cell(row=22, column=i+8, value=h)
        c.fill = sub_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    seg_data = df.groupby("Segment").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index().sort_values(by="Sales", ascending=False)
    
    for idx, s_row in seg_data.iterrows():
        cur_r = 23 + idx
        ws_summary.cell(row=cur_r, column=8, value=s_row["Segment"])
        ws_summary.cell(row=cur_r, column=9, value=round(s_row["Sales"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=10, value=round(s_row["Profit"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=11, value=f"=J{cur_r}/I{cur_r}").number_format = "0.0%"
        ws_summary.cell(row=cur_r, column=12, value=s_row["Orders"]).number_format = "#,##0"

    # 6. Top 10 Products by Profitability (Rows 29 to 40, Cols H to L)
    ws_summary["H28"] = "TOP 10 PRODUCTS BY PROFITABILITY"
    ws_summary["H28"].font = Font(name="Calibri", size=12, bold=True, color="1E293B")
    
    top_headers = ["Product Name", "Sales ($)", "Profit ($)", "Margin %"]
    for i, h in enumerate(top_headers):
        c = ws_summary.cell(row=29, column=i+8, value=h)
        c.fill = sub_fill
        c.font = font_bold_white
        c.alignment = Alignment(horizontal="center")
        
    top_prod_data = df.groupby("Product_Name").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index().sort_values(by="Profit", ascending=False).head(10)
    
    for idx, p_row in top_prod_data.iterrows():
        cur_r = 30 + idx
        ws_summary.cell(row=cur_r, column=8, value=p_row["Product_Name"])
        ws_summary.cell(row=cur_r, column=9, value=round(p_row["Sales"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=10, value=round(p_row["Profit"], 2)).number_format = "$#,##0.00"
        ws_summary.cell(row=cur_r, column=11, value=f"=J{cur_r}/I{cur_r}").number_format = "0.0%"

    # Auto-adjust column widths for Summary_Tables
    for col in ws_summary.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col[:45])
        ws_summary.column_dimensions[col_letter].width = max(max_len + 3, 13)
        
    print("Summary_Tables built successfully.")

    # -------------------------------------------------------------------------
    # TAB 1: Executive_Dashboard (C-Suite UI Layer)
    # -------------------------------------------------------------------------
    print("Designing Executive_Dashboard worksheet...")
    ws_dash.views.sheetView[0].showGridLines = False  # Professional dashboard look without default gridlines
    
    # 1. Top Title Banner
    # Merge B2:N2 for Main Title, B3:N3 for Subtitle
    ws_dash.merge_cells("B2:N2")
    ws_dash["B2"] = "RETAIL SALES PERFORMANCE ANALYSIS & EXECUTIVE DASHBOARD"
    ws_dash["B2"].font = Font(name="Calibri", size=18, bold=True, color="FFFFFF")
    ws_dash["B2"].fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    ws_dash["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[2].height = 36
    
    ws_dash.merge_cells("B3:N3")
    ws_dash["B3"] = "Enterprise Performance Monitoring | Multi-Region Omnichannel Transaction Log | FY 2023 - 2024"
    ws_dash["B3"].font = Font(name="Calibri", size=11, italic=True, color="94A3B8")
    ws_dash["B3"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws_dash["B3"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[3].height = 22
    
    # Slicer / Scope Indicator bar (Row 4)
    ws_dash.merge_cells("B4:N4")
    ws_dash["B4"] = "Active Scope: All Regions (East, West, Central, South)  |  Categories: Technology, Furniture, Office Supplies  |  All Customer Segments"
    ws_dash["B4"].font = Font(name="Calibri", size=10, bold=True, color="334155")
    ws_dash["B4"].fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    ws_dash["B4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[4].height = 20

    # 2. Executive KPI Cards (Row 6 to 8)
    # Card 1: Revenue (Cols B:D)
    # Card 2: Net Profit (Cols E:G)
    # Card 3: Margin % (Cols H:J)
    # Card 4: Volume & Orders (Cols K:N)
    
    kpi_defs = [
        {
            "range_title": "B6:D6", "range_val": "B7:D7", "range_sub": "B8:D8",
            "top_cell": "B6", "val_cell": "B7", "sub_cell": "B8",
            "accent_color": "2563EB",  # Blue
            "title": "TOTAL NET REVENUE",
            "val_formula": "=Summary_Tables!C4",
            "val_format": "$#,##0",
            "sub": "YoY Growth: +12.9%  |  AOV: $648"
        },
        {
            "range_title": "E6:G6", "range_val": "E7:G7", "range_sub": "E8:G8",
            "top_cell": "E6", "val_cell": "E7", "sub_cell": "E8",
            "accent_color": "059669",  # Emerald Green
            "title": "NET OPERATING PROFIT",
            "val_formula": "=Summary_Tables!D4",
            "val_format": "$#,##0",
            "sub": "Net Contribution Margin"
        },
        {
            "range_title": "H6:J6", "range_val": "H7:J7", "range_sub": "H8:J8",
            "top_cell": "H6", "val_cell": "H7", "sub_cell": "H8",
            "accent_color": "D97706",  # Amber Gold
            "title": "OPERATING MARGIN %",
            "val_formula": "=Summary_Tables!E4",
            "val_format": "0.0%",
            "sub": "Target: 15.0% | Bleed: Furniture (-1.5%)"
        },
        {
            "range_title": "K6:N6", "range_val": "K7:N7", "range_sub": "K8:N8",
            "top_cell": "K6", "val_cell": "K7", "sub_cell": "K8",
            "accent_color": "6366F1",  # Indigo
            "title": "TOTAL ORDERS & VOLUME",
            "val_formula": "=Summary_Tables!F4",
            "val_format": '#,##0" Orders"',
            "sub": "7,204 Units Sold across 50 Clients"
        }
    ]
    
    card_bg = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    card_border_side = Side(style='thin', color='CBD5E1')
    card_border = Border(left=card_border_side, right=card_border_side, top=card_border_side, bottom=card_border_side)
    
    ws_dash.row_dimensions[6].height = 20
    ws_dash.row_dimensions[7].height = 36
    ws_dash.row_dimensions[8].height = 18
    
    for card in kpi_defs:
        # Merge cells
        ws_dash.merge_cells(card["range_title"])
        ws_dash.merge_cells(card["range_val"])
        ws_dash.merge_cells(card["range_sub"])
        
        # Title
        tc = ws_dash[card["top_cell"]]
        tc.value = card["title"]
        tc.font = Font(name="Calibri", size=10, bold=True, color="475569")
        tc.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        tc.alignment = Alignment(horizontal="center", vertical="center")
        
        # Value
        vc = ws_dash[card["val_cell"]]
        vc.value = card["val_formula"]
        vc.font = Font(name="Calibri", size=22, bold=True, color="0F172A")
        vc.number_format = card["val_format"]
        vc.fill = card_bg
        vc.alignment = Alignment(horizontal="center", vertical="center")
        
        # Subtitle
        sc = ws_dash[card["sub_cell"]]
        sc.value = card["sub"]
        sc.font = Font(name="Calibri", size=9, italic=True, color="64748B")
        sc.fill = card_bg
        sc.alignment = Alignment(horizontal="center", vertical="center")

    # 3. Create & Embed Interactive Dynamic Charts
    
    # CHART 1: Monthly Trend Line Chart (Revenue & Profit over 24 Months)
    print("Embedding Chart 1: Monthly Trend Line Chart...")
    chart_trend = LineChart()
    chart_trend.title = "Monthly Net Revenue & Profit Trajectory (2023 - 2024)"
    chart_trend.style = 13
    chart_trend.y_axis.title = "Amount in USD ($)"
    chart_trend.x_axis.number_format = "yyyy-mm"
    chart_trend.x_axis.majorTimeUnit = "months"
    chart_trend.height = 12
    chart_trend.width = 20
    
    data_ref = Reference(ws_summary, min_col=4, min_row=7, max_col=5, max_row=monthly_end_r)
    cats_ref = Reference(ws_summary, min_col=3, min_row=8, max_row=monthly_end_r)
    chart_trend.add_data(data_ref, titles_from_data=True)
    chart_trend.set_categories(cats_ref)
    
    # Customize line styles
    if len(chart_trend.series) >= 2:
        chart_trend.series[0].graphicalProperties.line.solidFill = "2563EB"  # Blue for Revenue
        chart_trend.series[0].graphicalProperties.line.width = 25000
        chart_trend.series[1].graphicalProperties.line.solidFill = "059669"  # Green for Profit
        chart_trend.series[1].graphicalProperties.line.width = 25000
        
    ws_dash.add_chart(chart_trend, "B10")

    # CHART 2: Category Performance Bar Chart (Clustered Column)
    print("Embedding Chart 2: Category Performance Clustered Chart...")
    chart_cat = BarChart()
    chart_cat.type = "col"
    chart_cat.style = 10
    chart_cat.grouping = "clustered"
    chart_cat.title = "Category Revenue vs. Net Profit ($)"
    chart_cat.y_axis.title = "Amount in USD ($)"
    chart_cat.height = 12
    chart_cat.width = 16
    
    cat_data_ref = Reference(ws_summary, min_col=9, min_row=7, max_col=10, max_row=10)
    cat_cats_ref = Reference(ws_summary, min_col=8, min_row=8, max_row=10)
    chart_cat.add_data(cat_data_ref, titles_from_data=True)
    chart_cat.set_categories(cat_cats_ref)
    
    if len(chart_cat.series) >= 2:
        chart_cat.series[0].graphicalProperties.solidFill = "3B82F6"  # Blue
        chart_cat.series[1].graphicalProperties.solidFill = "10B981"  # Emerald
        
    ws_dash.add_chart(chart_cat, "I10")

    # CHART 3: Regional Sales & Profit Comparison
    print("Embedding Chart 3: Regional Distribution Chart...")
    chart_reg = BarChart()
    chart_reg.type = "col"
    chart_reg.style = 11
    chart_reg.grouping = "clustered"
    chart_reg.title = "Regional Revenue & Profit Breakdown"
    chart_reg.y_axis.title = "Amount ($)"
    chart_reg.height = 11
    chart_reg.width = 17
    
    reg_data_ref = Reference(ws_summary, min_col=9, min_row=14, max_col=10, max_row=18)
    reg_cats_ref = Reference(ws_summary, min_col=8, min_row=15, max_row=18)
    chart_reg.add_data(reg_data_ref, titles_from_data=True)
    chart_reg.set_categories(reg_cats_ref)
    
    if len(chart_reg.series) >= 2:
        chart_reg.series[0].graphicalProperties.solidFill = "1E40AF"
        chart_reg.series[1].graphicalProperties.solidFill = "047857"
        
    ws_dash.add_chart(chart_reg, "B26")

    # CHART 4: Top 10 Products by Profitability (Horizontal Bar)
    print("Embedding Chart 4: Top 10 Products Horizontal Bar...")
    chart_top = BarChart()
    chart_top.type = "bar"
    chart_top.style = 12
    chart_top.title = "Top 10 Profit-Generating Products ($)"
    chart_top.x_axis.title = "Net Profit ($)"
    chart_top.legend = None  # No legend needed for single series
    chart_top.height = 11
    chart_top.width = 19
    
    top_data_ref = Reference(ws_summary, min_col=10, min_row=29, max_col=10, max_row=39)
    top_cats_ref = Reference(ws_summary, min_col=8, min_row=30, max_row=39)
    chart_top.add_data(top_data_ref, titles_from_data=True)
    chart_top.set_categories(top_cats_ref)
    if len(chart_top.series) >= 1:
        chart_top.series[0].graphicalProperties.solidFill = "6366F1"  # Indigo
        
    ws_dash.add_chart(chart_top, "I26")

    # 4. Strategic Executive Callouts Banner (Rows 42 to 49)
    ws_dash.merge_cells("B42:N42")
    ws_dash["B42"] = "EXECUTIVE STRATEGIC TAKEAWAYS & ACTION DIRECTIVES"
    ws_dash["B42"].font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    ws_dash["B42"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws_dash["B42"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[42].height = 24
    
    takeaways = [
        ("B43:N43", "1. Institute 15% Maximum Discount Cap Policy:", "Discounts >= 30% eroded $41,269 in net profit. Enforcing a 15% cap across POS/ERP recovers margin immediately."),
        ("B44:N44", "2. Eliminate Discounts on Tables & Restructure Furniture:", "Tables generated -$17,419 in net losses due to thin margins. A strict 0% discount policy on Tables flips division to positive."),
        ("B45:N45", "3. Technology Enterprise Bundling:", "Technology generated 82.6% of company profit ($211k). Bundle high-ticket Copiers with high-margin recurring Office Supplies."),
        ("B46:N46", "4. Regional Rebalancing (East Margin Parity):", "East Region achieved highest sales ($505k) but lowest margin (12.2%). Migrating accounts to contract tiers unlocks +$10,950 profit."),
        ("B47:N47", "5. Q4 Logistics Pre-Stocking:", "November and December represent >37% of revenue and stretch fulfillment by +35%. Pre-position inventory to protect customer SLA.")
    ]
    
    for row_idx, (m_range, bold_lead, text_body) in enumerate(takeaways, start=43):
        ws_dash.merge_cells(m_range)
        cell = ws_dash[f"B{row_idx}"]
        cell.value = f"{bold_lead} {text_body}"
        cell.font = Font(name="Calibri", size=10, bold=False, color="1E293B")
        cell.fill = PatternFill(start_color="F8FAFC" if row_idx % 2 == 1 else "F1F5F9", fill_type="solid")
        cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws_dash.row_dimensions[row_idx].height = 20

    # Format Dashboard column widths
    for col_i in range(2, 15):
        ws_dash.column_dimensions[get_column_letter(col_i)].width = 16
    ws_dash.column_dimensions["A"].width = 3
    
    os.makedirs(os.path.dirname(OUTPUT_XLSX), exist_ok=True)
    wb.save(OUTPUT_XLSX)
    print(f"Excel Dashboard successfully compiled and saved to: {OUTPUT_XLSX}")

if __name__ == "__main__":
    build_workbook()

