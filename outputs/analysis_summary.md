# Frittenwerk Sales Seasonality Summary

## Business context
A manager expectation that the following week would be busier was translated into a structured analytics workflow using restaurant sales, NRW school holidays, German festival windows, menu launches, and the January 1, 2026 gastronomy VAT change.

## Data quality workflow
- Raw rows analysed: 243,555
- Final clean rows used for analysis: 238,789
- Rows excluded from the primary analysis dataset: 4,766
- Outlier orders flagged separately: 4,415
- Main raw missing-value pressure points: promotion_name (135), weather_condition (110), food_trend_theme (110)
- Most skewed raw metric: discount_eur (+4.984)

## Demand and seasonality findings
- Strongest seasonal month: Dec (index 1.194)
- Weakest seasonal month: Aug (index 0.811)
- Normal weekdays typically land around 3,191-3,814 in daily sales.
- Normal weekends typically land around 6,857-8,699 in daily sales.
- Festival weekdays typically land around 6,516-8,455 in daily sales.
- Festival Saturdays typically land around 10,197-11,441 in daily sales.
- Christmas Market Saturdays typically land around 10,421-11,435 in daily sales.
- Promotion with strongest daily-sales lift: Karneval Combo (40.2%)
- Highest average festival sales: Easter Weekend (9,323.39 per day)
- Strongest NRW school holiday window: Easter Holiday (5,771.55 per day)
- Highest-selling food trend: Loaded Indulgence (1,830,918.69)
- Strongest weather factor by total sales: Rainy (1,397,441.17)
- Anomalous sales days flagged: 12

## Pricing and menu changes
- From January 1, 2026, the food VAT relief phase lowered the average food-item price by 3.7% versus the pre-2026 period.
- Top new poutine launch: Chicken BBQ Poutine with 65,294.59 in total net sales and a 'Medium' sales label.

## Operational recommendation
Staffing, prep volume, and promo coordination should be increased ahead of late-Q4 weeks, Karneval, Christmas-market periods, and high-footfall holiday windows. The price-reset from the 2026 VAT change should also be monitored because it lowered menu prices while keeping demand resilient.
