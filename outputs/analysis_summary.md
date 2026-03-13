# Frittenwerk Sales Seasonality Summary

## Business context
My manager expectation that the following week would be busier was translated into a structured analytics workflow using restaurant sales, NRW school holidays, German festival windows, menu launches, and the January 1, 2026 gastronomy VAT change.

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
- Highest-selling food trend: Tijuana Street Fries (1,830,918.69)
- Strongest weather factor by total sales: Rainy (1,397,441.17)
- Anomalous sales days flagged: 12

## Pricing and menu changes
- From January 1, 2026, the food VAT relief phase lowered the average food-item price by 3.7% versus the pre-2026 period.
- Top new poutine launch: Chicken BBQ Poutine with 65,294.59 in total net sales and a 'Medium' sales label.

## Inventory ordering and wastage observation
- Inventory review was added after seasonality using a twice-weekly replenishment rule.
- Monday delivery was modelled to cover Tue-Wed-Thu demand.
- Thursday delivery was modelled to cover Fri-Sat-Mon demand, with Sunday treated as spillover because the dataset includes Sunday trading.
- Recommended stock volume stayed near 20.0% to 25.0% of cycle unit demand, depending on the sales band.
- Cycles with low sales but inconsistent order value were flagged 17 times as a potential wastage driver.
- Festival-linked cycles had an average estimated wastage rate of 15.0%.
- Largest estimated wastage driver: Festival stock uplift (4,175.7 excess stock units).
- Highest-risk stock cycle started on 2025-12-11 with 213.9 estimated excess stock units.

## Operational recommendation
Staffing, prep volume, and promo coordination should be increased ahead of late-Q4 weeks, Karneval, Christmas-market periods, and high-footfall holiday windows. The inventory plan should then translate those demand signals into Monday/Thursday stock orders while capping additional festival buffers and reviewing low-sales, high-variance product mixes to reduce wastage.
