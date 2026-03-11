# Power BI / Tableau Dashboard Guide

This package gives you two dashboard sheets built from the processed CSV outputs in this repository.

## Sheet 1: Uncovering Seasonal Trends
- KPI cards: Peak Month, Weakest Month, Top Promotion Lift, Top Food Trend
- Main line chart: `monthly_sales_summary.csv` using `year_month` vs `total_net_sales`
- Bar chart: `monthly_seasonality_index.csv` using `month_name` vs `seasonality_index`
- Bar chart: `daily_sales_profile.csv` using `profile_name` vs `median_daily_sales`
- Bar chart: `festival_impact_summary.csv` using `festival_name` vs `avg_daily_sales`
- Bar chart: `food_trend_summary.csv` using `food_trend_theme` vs `total_net_sales`
- Suggested slicers: `year`, `month_name`, `festival_name`, `promotion_group`, `school_holiday_name`

Recommended headline metrics:
- Peak month: Dec (1.194)
- Strongest promotion lift: Karneval Combo (40.2%)
- Strongest festival period: Easter Weekend
- Strongest NRW holiday window: Easter Holiday
- Top food trend: Tijuana Street Fries

## Sheet 2: Inventory Management
- KPI cards: Excess Stock Units, Wastage Rate, Top Wastage Driver, Highest-Risk Cycle
- Dual-line chart: `inventory_cycle_summary.csv` using `stock_delivery_date` vs `recommended_stock_units` and `observed_stock_order_units`
- Bar chart: `primary_wastage_driver` vs `estimated_waste_units`
- Scatter chart: `cycle_total_sales` vs `estimated_waste_units`, sized by `observed_stock_order_units`, colored by `primary_wastage_driver`
- Detail table: `stock_delivery_date`, `inventory_cycle`, `dominant_festival`, `primary_wastage_driver`, `estimated_waste_units`
- Suggested slicers: `inventory_cycle`, `coverage_window`, `dominant_festival`, `dominant_holiday`, `cycle_sales_band`

Recommended headline metrics:
- Top wastage driver: Festival stock uplift (4,175.7 units)
- Highest-risk cycle: 2025-12-11
- Overall wastage rate: 4.8%

## Files to use
- [seasonal_trends_dashboard.png](/Users/yeswanth/Desktop/Analytics project/outputs/dashboards/seasonal_trends_dashboard.png)
- [inventory_management_dashboard.png](/Users/yeswanth/Desktop/Analytics project/outputs/dashboards/inventory_management_dashboard.png)
- [monthly_sales_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/monthly_sales_summary.csv)
- [monthly_seasonality_index.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/monthly_seasonality_index.csv)
- [promotion_impact_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/promotion_impact_summary.csv)
- [festival_impact_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/festival_impact_summary.csv)
- [school_holiday_impact_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/school_holiday_impact_summary.csv)
- [daily_sales_profile.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/daily_sales_profile.csv)
- [food_trend_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/food_trend_summary.csv)
- [inventory_cycle_summary.csv](/Users/yeswanth/Desktop/Analytics project/data/processed/inventory_cycle_summary.csv)
