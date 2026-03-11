# Frittenwerk Sales Seasonality Case Study

This project is a portfolio-safe restaurant analytics case study inspired by a part-time work context at Frittenwerk.

## Scenario

While working part-time, a manager mentioned that the following week would likely be busier than usual. Instead of relying only on intuition, this project turns that operational comment into an analytics workflow:

- collect the last two years of sales data
- make the dataset consistent
- check missing values, duplicates, anomalies, outliers, and skewness
- test whether NRW school holidays, festivals, new poutine launches, discounts, VAT-driven price changes, and other outside factors explain demand spikes
- translate the seasonal signal into Monday/Thursday inventory ordering rules
- check whether extra festival stock, inconsistent order value, and product mix shifts increase wastage or expiry risk
- visualize the findings in a way that is easy to share on LinkedIn

## Portfolio note

The sample dataset in this repository is synthetic and anonymized. If you use this project publicly, describe it as:

`a sales seasonality and demand-driver case study inspired by my restaurant operations experience, built with anonymized/simulated data`

That keeps the story strong without implying you are sharing confidential company numbers.

## Workflow

The code and outputs follow this funnel:

1. `Raw intake`
   Load restaurant sales with promotions, festival periods, NRW school holidays, local events, food trend themes, new poutine launches, and the January 1, 2026 VAT-relief phase.
2. `Data consistency`
   Standardize categories, enforce numeric types, recalculate net sales, and clean inconsistent labels.
3. `Quality checks`
   Measure missing values, duplicates, invalid records, outliers, skewness, and daily anomalies.
4. `Business analysis`
   Quantify seasonal trends, promotion lift, festival impact, outside factors, and food trend performance.
5. `Inventory analysis`
   Convert the demand pattern into Monday/Thursday stock cycles, estimate recommended stock volume, and flag wastage risk from festival buffers and volatile product mix.
6. `Communication`
   Save charts, cleaned datasets, markdown summaries, and a LinkedIn-ready project note.

## Project structure

- `data/raw/frittenwerk_sales_raw.csv`: raw sales data with intentional quality issues for demonstration
- `data/processed/frittenwerk_sales_clean.csv`: cleaned analysis-ready dataset
- `data/processed/data_cleaning_funnel.csv`: row counts at each cleaning stage
- `data/processed/missing_values_summary.csv`: missing-value profile before and after cleaning
- `data/processed/numeric_skewness_summary.csv`: skewness checks for numeric metrics
- `data/processed/outlier_orders.csv`: flagged order-level outliers removed from the main analysis
- `data/processed/daily_sales_anomalies.csv`: flagged anomalous sales days
- `data/processed/monthly_sales_summary.csv`: monthly revenue and order summary
- `data/processed/monthly_seasonality_index.csv`: month-level seasonality score
- `data/processed/promotion_impact_summary.csv`: promotion performance
- `data/processed/festival_impact_summary.csv`: festival performance
- `data/processed/external_factor_summary.csv`: weather and local-event effect
- `data/processed/school_holiday_impact_summary.csv`: NRW school-holiday daily-sales effect
- `data/processed/tax_policy_summary.csv`: pricing and sales effect of the gastronomy VAT phase
- `data/processed/new_poutine_summary.csv`: performance of new poutine launches
- `data/processed/daily_sales_profile.csv`: normal-day, weekend, festival, and Christmas sales ranges
- `data/processed/food_trend_summary.csv`: food trend performance
- `data/processed/daily_inventory_inputs.csv`: daily inventory planning inputs derived from sales
- `data/processed/inventory_cycle_summary.csv`: Monday/Thursday stock-cycle view with recommended stock and estimated wastage
- `data/processed/inventory_wastage_cases.csv`: cycles where festival stock, inconsistent order value, or product mix created excess-stock risk
- `outputs/charts/`: workflow and insight visuals
- `outputs/analysis_summary.md`: business summary of findings
- `outputs/inventory_observation.md`: separate observation note on stock ordering and wastage
- `outputs/linkedin_case_study.md`: portfolio-ready wording for LinkedIn
- `src/generate_sample_data.py`: generates a Frittenwerk-style raw dataset
- `src/analyze_sales_seasonality.py`: runs the cleaning, QA, demand-driver, inventory, and wastage analysis

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_sales_seasonality.py
```

## Main outputs

After running the project, you can point to:

- `data_cleaning_funnel.png`
- `missing_values_overview.png`
- `skewness_profile.png`
- `monthly_sales_trend.png`
- `daily_sales_anomalies.png`
- `promotion_impact.png`
- `festival_impact.png`
- `school_holiday_impact.png`
- `tax_policy_impact.png`
- `new_poutine_performance.png`
- `day_type_sales_profile.png`
- `food_trend_sales_mix.png`
- `inventory_wastage_by_driver.png`
- `order_value_boxplot.png`
- `analysis_summary.md`
- `inventory_observation.md`
- `linkedin_case_study.md`

## Using real data later

When you get a real export, replace `data/raw/frittenwerk_sales_raw.csv` with your actual file and keep the same columns where possible. If the schema changes, update the column mapping in `src/analyze_sales_seasonality.py`.
