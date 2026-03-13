# Frittenwerk Sales Seasonality Case Study

This project is a portfolio-safe restaurant analytics case study inspired in my part-time work at Frittenwerk.

## Scenario

While working part-time, my manager mentioned that the following week would likely be busier than usual. Instead of relying only on intuition, this project turns that operational comment into an analytics workflow:

- collect the last two years of sales data
- make the dataset consistent
- check missing values, duplicates, anomalies, outliers, and skewness
- test whether NRW school holidays, festivals, new poutine launches, discounts, VAT-driven price changes, and other outside factors explain demand spikes
- visualize the findings

## Portfolio note

The sample dataset in this repository is synthetic and anonymized.(Referred the entities and tables from the original database)


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
5. `Communication`
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
- `outputs/charts/`: workflow and insight visuals
- `outputs/analysis_summary.md`: business summary of findings
- `outputs/linkedin_case_study.md`: portfolio-ready wording for LinkedIn
- `src/generate_sample_data.py`: generates a Frittenwerk-style raw dataset
- `src/analyze_sales_seasonality.py`: runs the cleaning, QA, and demand-driver analysis

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
- `order_value_boxplot.png`
- `analysis_summary.md`
- `linkedin_case_study.md`

## Using real data later

After geting a real export, replaced `data/raw/frittenwerk_sales_raw.csv` with actual file and kept the same columns where possible. If the schema changes, update the column mapping in `src/analyze_sales_seasonality.py`.
