# LinkedIn Case Study Draft

## LinkedIn Post Draft

My manager said there would be an increase in work in the coming week, so I decided to validate that operational assumption with data instead of relying only on intuition.

I took the last two years of restaurant sales data, cleaned inconsistent records, checked missing values, outliers, skewness, and anomalies, and then analyzed seasonal demand patterns, promotions, festivals, NRW school holidays, menu trends, and pricing changes.

A few insights from the project:
- Dec was the strongest seasonal month, while Aug was the weakest.
- Normal weekend sales were around 6,857-8,699 per day.
- Festival Saturdays were around 10,197-11,441 per day.

Demand and sales insights:
- Strongest promotion lift: Karneval Combo (40.2%)
- Strongest festival period: Easter Weekend
- Strongest NRW holiday window: Easter Holiday
- Highest-selling food trend: Tijuana Street Fries
- New poutine launch tracked in the analysis: Chicken BBQ Poutine (Medium)
- Average food-item price moved -3.7% after the VAT policy shift.

More seasonal-trend details are in the markdown summary: https://github.com/yeswanth2715/Frittenwerk-Seasonal-Trend-Analysis/blob/main/outputs/analysis_summary.md

After the seasonal analysis, I also checked inventory management using the weekly stock pattern: Monday stock for Tue-Wed-Thu and Thursday stock for Fri-Sat-Mon, with Sunday treated as spillover.

Inventory insights:
- Estimated excess stock across the modeled cycles: 5,971.9 units
- Estimated overall wastage rate: 4.8%
- Largest wastage driver: Festival stock uplift (4,175.7 units)
- Low-sales but inconsistent-order-value cycles flagged: 17
- Highest-risk stock cycle: 2025-12-11 with 213.9 excess units.

More inventory observations are in the markdown file: https://github.com/yeswanth2715/Frittenwerk-Seasonal-Trend-Analysis/blob/main/outputs/inventory_observation.md

Finally, I generated dashboards to visualize both the seasonal trends and the inventory-management side, so the outputs and recommendations can be communicated more clearly.

Recommendations from the project:
- Increase staffing and prep before late-Q4 weeks, Karneval, Christmas-market periods, and strong holiday windows.
- Translate demand signals into tighter Monday/Thursday stock planning instead of applying blanket stock uplifts.
- Review festival buffers and low-sales, high-variance product mixes more carefully to reduce waste.

Note:
This project was completed with AI support. I wanted to understand how AI can help analysts find things faster and work more efficiently. My view is that AI is most useful when you already understand the business context behind the data. AI should complement analyst work, not replace it. Through this project, I strengthened how I use AI in data analysis.

Dashboard visuals:
![Seasonal Trends Dashboard](https://raw.githubusercontent.com/yeswanth2715/Frittenwerk-Seasonal-Trend-Analysis/main/outputs/dashboards/seasonal_trends_dashboard.png)

![Inventory Management Dashboard](https://raw.githubusercontent.com/yeswanth2715/Frittenwerk-Seasonal-Trend-Analysis/main/outputs/dashboards/inventory_management_dashboard.png)
