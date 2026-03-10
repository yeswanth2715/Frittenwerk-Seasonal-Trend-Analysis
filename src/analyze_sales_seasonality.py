from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MPLCONFIG_DIR = BASE_DIR / ".matplotlib"
MPLCONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIG_DIR))

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "frittenwerk_sales_raw.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"
SUMMARY_PATH = BASE_DIR / "outputs" / "analysis_summary.md"
LINKEDIN_PATH = BASE_DIR / "outputs" / "linkedin_case_study.md"

CLEAN_DATA_PATH = PROCESSED_DIR / "frittenwerk_sales_clean.csv"
FUNNEL_PATH = PROCESSED_DIR / "data_cleaning_funnel.csv"
MISSING_PATH = PROCESSED_DIR / "missing_values_summary.csv"
SKEWNESS_PATH = PROCESSED_DIR / "numeric_skewness_summary.csv"
QUALITY_CHECKS_PATH = PROCESSED_DIR / "data_quality_checks.csv"
OUTLIERS_PATH = PROCESSED_DIR / "outlier_orders.csv"
ANOMALIES_PATH = PROCESSED_DIR / "daily_sales_anomalies.csv"
MONTHLY_PATH = PROCESSED_DIR / "monthly_sales_summary.csv"
SEASONALITY_PATH = PROCESSED_DIR / "monthly_seasonality_index.csv"
PROMOTION_PATH = PROCESSED_DIR / "promotion_impact_summary.csv"
FESTIVAL_PATH = PROCESSED_DIR / "festival_impact_summary.csv"
EXTERNAL_FACTORS_PATH = PROCESSED_DIR / "external_factor_summary.csv"
HOLIDAY_PATH = PROCESSED_DIR / "school_holiday_impact_summary.csv"
TAX_POLICY_PATH = PROCESSED_DIR / "tax_policy_summary.csv"
NEW_POUTINE_PATH = PROCESSED_DIR / "new_poutine_summary.csv"
DAILY_PROFILE_PATH = PROCESSED_DIR / "daily_sales_profile.csv"
FOOD_TREND_PATH = PROCESSED_DIR / "food_trend_summary.csv"

MONTH_ORDER = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

CHANNEL_MAP = {
    "dine-in": "Dine-In",
    "dine in": "Dine-In",
    "dinein": "Dine-In",
    "takeaway": "Takeaway",
    "take away": "Takeaway",
    "delivery": "Delivery",
}

CATEGORY_MAP = {
    "loaded fries": "Loaded Fries",
    "poutine": "Poutine",
    "vegan bowl": "Vegan Bowl",
    "wraps": "Wraps",
    "snacks": "Snacks",
    "drinks": "Drinks",
}


def load_raw_sales() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            "Missing raw dataset. Run `python src/generate_sample_data.py` first."
        )

    return pd.read_csv(RAW_DATA_PATH, parse_dates=["order_date"])


def summarize_missing_values(sales: pd.DataFrame, stage: str) -> pd.DataFrame:
    missing_rows = []
    total_rows = len(sales)
    for column in sales.columns:
        missing_count = int(sales[column].isna().sum())
        missing_rows.append(
            {
                "stage": stage,
                "column": column,
                "missing_count": missing_count,
                "missing_pct": round((missing_count / total_rows) * 100, 2) if total_rows else 0.0,
            }
        )
    return pd.DataFrame(missing_rows).sort_values(["stage", "missing_count"], ascending=[True, False])


def summarize_numeric_skewness(sales: pd.DataFrame, stage: str) -> pd.DataFrame:
    numeric_columns = [
        "quantity",
        "base_unit_price",
        "unit_price",
        "gross_sales",
        "discount_eur",
        "net_sales",
    ]
    skew_rows = []
    for column in numeric_columns:
        numeric_values = pd.to_numeric(sales[column], errors="coerce")
        skew_rows.append(
            {
                "stage": stage,
                "metric": column,
                "skewness": round(float(numeric_values.skew()), 3),
            }
        )
    return pd.DataFrame(skew_rows)


def format_no_label(series: pd.Series, label: str) -> pd.Series:
    return (
        series.fillna(label)
        .astype(str)
        .str.strip()
        .replace({"": label, "nan": label, "None": label})
    )


def iqr_outlier_mask(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    return (series < lower_bound) | (series > upper_bound)


def prepare_sales_features(sales: pd.DataFrame) -> pd.DataFrame:
    prepared_sales = sales.copy()
    prepared_sales["year"] = prepared_sales["order_date"].dt.year
    prepared_sales["month"] = prepared_sales["order_date"].dt.month
    prepared_sales["month_name"] = prepared_sales["order_date"].dt.strftime("%b")
    prepared_sales["year_month"] = prepared_sales["order_date"].dt.to_period("M").astype(str)
    prepared_sales["day_name"] = prepared_sales["order_date"].dt.day_name()
    prepared_sales["avg_item_price"] = (prepared_sales["net_sales"] / prepared_sales["quantity"]).round(2)
    prepared_sales["is_food_item"] = prepared_sales["menu_category"] != "Drinks"
    return prepared_sales


def run_cleaning_pipeline(
    raw_sales: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sales = raw_sales.copy()

    duplicate_rows = sales.duplicated().sum()
    sales = sales.drop_duplicates()
    duplicate_order_ids = sales.duplicated(subset=["order_id"]).sum()
    sales = sales.drop_duplicates(subset=["order_id"], keep="first")
    rows_after_duplicate_removal = len(sales)

    sales["order_date"] = pd.to_datetime(sales["order_date"], errors="coerce")
    numeric_columns = [
        "quantity",
        "base_unit_price",
        "unit_price",
        "gross_sales",
        "discount_eur",
        "net_sales",
        "vat_rate_pct",
        "vat_relief_pass_through_pct",
    ]
    for column in numeric_columns:
        sales[column] = pd.to_numeric(sales[column], errors="coerce")

    sales["sales_channel"] = (
        sales["sales_channel"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(CHANNEL_MAP)
        .fillna("Unknown")
    )
    sales["menu_category"] = (
        sales["menu_category"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(CATEGORY_MAP)
        .fillna("Unknown")
    )
    sales["meal_period"] = format_no_label(sales["meal_period"], "Unknown").str.title()
    sales["store_city"] = format_no_label(sales["store_city"], "Unknown").str.title()
    sales["menu_item"] = format_no_label(sales["menu_item"], "Unknown")
    sales["launch_name"] = format_no_label(sales["launch_name"], "Core Menu")
    sales["launch_sales_band"] = format_no_label(sales["launch_sales_band"], "Core").str.title()
    sales["promotion_name"] = format_no_label(sales["promotion_name"], "No Promotion")
    sales["festival_name"] = format_no_label(sales["festival_name"], "No Festival")
    sales["weather_condition"] = format_no_label(sales["weather_condition"], "Unknown").str.title()
    sales["school_holiday_name"] = format_no_label(sales["school_holiday_name"], "No School Holiday")
    sales["food_trend_theme"] = format_no_label(sales["food_trend_theme"], "Unknown")
    sales["tax_policy_phase"] = format_no_label(sales["tax_policy_phase"], "Pre-2026 19% VAT")
    sales["price_adjustment_reason"] = format_no_label(
        sales["price_adjustment_reason"],
        "No Base Price Reduction",
    )

    boolean_columns = [
        "promotion_applied_flag",
        "school_holiday_flag",
        "local_event_flag",
        "new_poutine_flag",
        "vat_relief_eligible_flag",
    ]
    for column in boolean_columns:
        sales[column] = sales[column].fillna(False).astype(bool)

    sales["recomputed_net_sales"] = (sales["gross_sales"] - sales["discount_eur"]).round(2)
    invalid_mask = (
        sales["order_date"].isna()
        | sales["quantity"].isna()
        | sales["base_unit_price"].isna()
        | sales["unit_price"].isna()
        | sales["gross_sales"].isna()
        | sales["discount_eur"].isna()
        | sales["vat_rate_pct"].isna()
        | (sales["quantity"] <= 0)
        | (sales["base_unit_price"] <= 0)
        | (sales["unit_price"] <= 0)
        | (sales["gross_sales"] <= 0)
        | (sales["discount_eur"] < 0)
        | (sales["recomputed_net_sales"] <= 0)
        | (sales["vat_rate_pct"] <= 0)
    )

    invalid_rows = sales.loc[invalid_mask].copy()
    valid_sales = sales.loc[~invalid_mask].copy()
    valid_sales["net_sales"] = valid_sales["recomputed_net_sales"]
    valid_sales = valid_sales.drop(columns=["recomputed_net_sales"])
    invalid_rows = invalid_rows.drop(columns=["recomputed_net_sales"])

    valid_sales["quantity_outlier_flag"] = iqr_outlier_mask(valid_sales["quantity"])
    valid_sales["gross_sales_outlier_flag"] = iqr_outlier_mask(valid_sales["gross_sales"])
    valid_sales["net_sales_outlier_flag"] = iqr_outlier_mask(valid_sales["net_sales"])
    outlier_mask = (
        valid_sales[
            ["quantity_outlier_flag", "gross_sales_outlier_flag", "net_sales_outlier_flag"]
        ].sum(axis=1)
        >= 2
    )

    outlier_orders = valid_sales.loc[outlier_mask].copy()
    clean_sales = valid_sales.loc[~outlier_mask].copy()
    clean_sales = prepare_sales_features(clean_sales)

    funnel = pd.DataFrame(
        [
            {"stage": "Raw rows", "row_count": len(raw_sales)},
            {"stage": "After duplicate removal", "row_count": rows_after_duplicate_removal},
            {"stage": "After invalid record removal", "row_count": len(valid_sales)},
            {"stage": "Final clean rows", "row_count": len(clean_sales)},
        ]
    )
    funnel["row_count"] = funnel["row_count"].clip(lower=0)

    quality_checks = pd.DataFrame(
        [
            {"metric": "raw_rows", "value": len(raw_sales)},
            {"metric": "exact_duplicates_removed", "value": int(duplicate_rows)},
            {"metric": "duplicate_order_ids_removed", "value": int(duplicate_order_ids)},
            {"metric": "invalid_rows_removed", "value": int(len(invalid_rows))},
            {"metric": "outlier_orders_flagged", "value": int(len(outlier_orders))},
            {"metric": "clean_rows", "value": int(len(clean_sales))},
        ]
    )

    return clean_sales, outlier_orders, funnel, quality_checks


def build_monthly_sales_summary(sales: pd.DataFrame) -> pd.DataFrame:
    monthly_sales = (
        sales.groupby(["year", "month", "year_month"], as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_orders=("order_id", "nunique"),
            total_units=("quantity", "sum"),
            avg_order_value=("net_sales", "mean"),
        )
        .sort_values(["year", "month"])
    )
    monthly_sales["month_name"] = pd.Categorical(
        [MONTH_ORDER[month - 1] for month in monthly_sales["month"]],
        categories=MONTH_ORDER,
        ordered=True,
    )
    monthly_sales["avg_order_value"] = monthly_sales["avg_order_value"].round(2)
    return monthly_sales


def build_seasonality_index(monthly_sales: pd.DataFrame) -> pd.DataFrame:
    seasonality = (
        monthly_sales.groupby("month", as_index=False)["total_net_sales"]
        .mean()
        .rename(columns={"total_net_sales": "avg_monthly_sales"})
        .sort_values("month")
    )
    seasonality["month_name"] = pd.Categorical(
        [MONTH_ORDER[month - 1] for month in seasonality["month"]],
        categories=MONTH_ORDER,
        ordered=True,
    )
    overall_average = seasonality["avg_monthly_sales"].mean()
    seasonality["seasonality_index"] = (seasonality["avg_monthly_sales"] / overall_average).round(3)
    return seasonality


def build_promotion_impact(sales: pd.DataFrame) -> pd.DataFrame:
    daily_promotion = (
        sales.groupby(["order_date", "promotion_name"], as_index=False)
        .agg(
            daily_net_sales=("net_sales", "sum"),
            daily_orders=("order_id", "nunique"),
            redemption_rate=("promotion_applied_flag", "mean"),
        )
    )
    promotion_summary = (
        daily_promotion.groupby("promotion_name", as_index=False)
        .agg(
            promotion_days=("order_date", "nunique"),
            avg_daily_sales=("daily_net_sales", "mean"),
            avg_daily_orders=("daily_orders", "mean"),
            avg_redemption_rate=("redemption_rate", "mean"),
        )
        .rename(columns={"promotion_name": "promotion_group"})
        .sort_values("avg_daily_sales", ascending=False)
    )
    baseline = promotion_summary.loc[
        promotion_summary["promotion_group"] == "No Promotion", "avg_daily_sales"
    ]
    baseline_value = (
        float(baseline.iloc[0]) if not baseline.empty else float(promotion_summary["avg_daily_sales"].mean())
    )
    promotion_summary["avg_daily_sales_lift_pct"] = (
        ((promotion_summary["avg_daily_sales"] / baseline_value) - 1) * 100
    ).round(1)
    promotion_summary["avg_daily_sales"] = promotion_summary["avg_daily_sales"].round(2)
    promotion_summary["avg_daily_orders"] = promotion_summary["avg_daily_orders"].round(2)
    promotion_summary["avg_redemption_rate"] = (promotion_summary["avg_redemption_rate"] * 100).round(1)
    return promotion_summary


def build_festival_impact(sales: pd.DataFrame) -> pd.DataFrame:
    daily_festival = (
        sales.groupby(["order_date", "festival_name"], as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_orders=("order_id", "nunique"),
        )
    )
    festival_summary = (
        daily_festival.groupby("festival_name", as_index=False)
        .agg(
            festival_days=("order_date", "nunique"),
            avg_daily_sales=("total_net_sales", "mean"),
            avg_daily_orders=("total_orders", "mean"),
        )
        .sort_values("avg_daily_sales", ascending=False)
    )
    festival_summary["avg_daily_sales"] = festival_summary["avg_daily_sales"].round(2)
    festival_summary["avg_daily_orders"] = festival_summary["avg_daily_orders"].round(2)
    return festival_summary


def build_external_factor_summary(sales: pd.DataFrame) -> pd.DataFrame:
    weather_summary = (
        sales.groupby("weather_condition", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            avg_order_value=("net_sales", "mean"),
            orders=("order_id", "nunique"),
        )
        .assign(factor_group="Weather", factor_label=lambda df: df["weather_condition"])
    )
    local_event_summary = (
        sales.groupby("local_event_flag", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            avg_order_value=("net_sales", "mean"),
            orders=("order_id", "nunique"),
        )
        .assign(
            factor_group="Local Event",
            factor_label=lambda df: np.where(df["local_event_flag"], "Local Event Days", "Standard Days"),
        )
    )

    factor_summary = pd.concat(
        [
            weather_summary[["factor_group", "factor_label", "total_net_sales", "avg_order_value", "orders"]],
            local_event_summary[["factor_group", "factor_label", "total_net_sales", "avg_order_value", "orders"]],
        ],
        ignore_index=True,
    )
    factor_summary["avg_order_value"] = factor_summary["avg_order_value"].round(2)
    return factor_summary.sort_values(["factor_group", "total_net_sales"], ascending=[True, False])


def build_school_holiday_summary(sales: pd.DataFrame) -> pd.DataFrame:
    daily_holiday = (
        sales.groupby(["order_date", "school_holiday_name"], as_index=False)
        .agg(
            daily_net_sales=("net_sales", "sum"),
            daily_orders=("order_id", "nunique"),
        )
    )
    holiday_summary = (
        daily_holiday.groupby("school_holiday_name", as_index=False)
        .agg(
            holiday_days=("order_date", "nunique"),
            avg_daily_sales=("daily_net_sales", "mean"),
            avg_daily_orders=("daily_orders", "mean"),
        )
        .sort_values("avg_daily_sales", ascending=False)
    )
    holiday_summary["avg_daily_sales"] = holiday_summary["avg_daily_sales"].round(2)
    holiday_summary["avg_daily_orders"] = holiday_summary["avg_daily_orders"].round(2)
    return holiday_summary


def build_tax_policy_summary(sales: pd.DataFrame) -> pd.DataFrame:
    food_sales = sales[sales["is_food_item"]].copy()
    policy_daily = (
        food_sales.groupby(["order_date", "tax_policy_phase"], as_index=False)
        .agg(
            daily_net_sales=("net_sales", "sum"),
            daily_orders=("order_id", "nunique"),
        )
    )
    policy_sales_summary = (
        food_sales.groupby("tax_policy_phase", as_index=False)
        .agg(
            avg_unit_price=("unit_price", "mean"),
            avg_base_unit_price=("base_unit_price", "mean"),
            avg_vat_rate_pct=("vat_rate_pct", "mean"),
            avg_pass_through_pct=("vat_relief_pass_through_pct", "mean"),
            orders=("order_id", "nunique"),
        )
    )
    policy_daily_summary = (
        policy_daily.groupby("tax_policy_phase", as_index=False)
        .agg(
            policy_days=("order_date", "nunique"),
            avg_daily_sales=("daily_net_sales", "mean"),
            avg_daily_orders=("daily_orders", "mean"),
        )
    )
    tax_policy_summary = policy_sales_summary.merge(policy_daily_summary, on="tax_policy_phase", how="left")
    baseline = tax_policy_summary.loc[
        tax_policy_summary["tax_policy_phase"] == "Pre-2026 19% VAT", "avg_unit_price"
    ]
    baseline_value = float(baseline.iloc[0]) if not baseline.empty else float(tax_policy_summary["avg_unit_price"].mean())
    tax_policy_summary["avg_unit_price_change_pct_vs_pre_2026"] = (
        ((tax_policy_summary["avg_unit_price"] / baseline_value) - 1) * 100
    ).round(1)
    for column in ["avg_unit_price", "avg_base_unit_price", "avg_vat_rate_pct", "avg_daily_sales", "avg_daily_orders"]:
        tax_policy_summary[column] = tax_policy_summary[column].round(2)
    tax_policy_summary["avg_pass_through_pct"] = (tax_policy_summary["avg_pass_through_pct"] * 100).round(1)
    return tax_policy_summary.sort_values("avg_daily_sales", ascending=False)


def build_new_poutine_summary(sales: pd.DataFrame) -> pd.DataFrame:
    launch_sales = sales[sales["new_poutine_flag"]].copy()
    if launch_sales.empty:
        return pd.DataFrame(
            columns=[
                "launch_name",
                "launch_sales_band",
                "launch_days",
                "total_net_sales",
                "total_orders",
                "avg_order_value",
                "avg_daily_sales",
            ]
        )

    launch_daily = (
        launch_sales.groupby(["order_date", "launch_name"], as_index=False)
        .agg(daily_net_sales=("net_sales", "sum"))
    )
    launch_summary = (
        launch_sales.groupby(["launch_name", "launch_sales_band"], as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_orders=("order_id", "nunique"),
            avg_order_value=("net_sales", "mean"),
        )
    )
    daily_summary = (
        launch_daily.groupby("launch_name", as_index=False)
        .agg(
            launch_days=("order_date", "nunique"),
            avg_daily_sales=("daily_net_sales", "mean"),
        )
    )
    launch_summary = launch_summary.merge(daily_summary, on="launch_name", how="left")
    launch_summary["avg_order_value"] = launch_summary["avg_order_value"].round(2)
    launch_summary["avg_daily_sales"] = launch_summary["avg_daily_sales"].round(2)
    return launch_summary.sort_values("total_net_sales", ascending=False)


def build_daily_sales_profile(sales: pd.DataFrame) -> pd.DataFrame:
    daily_sales = (
        sales.groupby("order_date", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            dominant_festival=("festival_name", lambda values: values.mode().iloc[0] if not values.mode().empty else "No Festival"),
        )
        .sort_values("order_date")
    )
    daily_sales["day_num"] = daily_sales["order_date"].dt.weekday
    daily_sales["profile_name"] = np.select(
        [
            (daily_sales["dominant_festival"] == "Christmas Market") & (daily_sales["day_num"] == 5),
            (daily_sales["dominant_festival"] == "Christmas Market") & (daily_sales["day_num"] < 5),
            (daily_sales["dominant_festival"] != "No Festival") & (daily_sales["day_num"] == 5),
            (daily_sales["dominant_festival"] != "No Festival")
            & (daily_sales["dominant_festival"] != "Christmas Market")
            & (daily_sales["day_num"] < 5),
            (daily_sales["dominant_festival"] == "No Festival") & (daily_sales["day_num"] >= 4),
        ],
        [
            "Christmas Market Saturday",
            "Christmas Market Weekday",
            "Festival Saturday",
            "Festival Weekday",
            "Normal Weekend",
        ],
        default="Normal Weekday",
    )
    profile_summary = (
        daily_sales.groupby("profile_name", as_index=False)["total_net_sales"]
        .agg(
            profile_days="count",
            p25_daily_sales=lambda values: values.quantile(0.25),
            median_daily_sales="median",
            p75_daily_sales=lambda values: values.quantile(0.75),
        )
    )
    profile_order = [
        "Normal Weekday",
        "Normal Weekend",
        "Festival Weekday",
        "Festival Saturday",
        "Christmas Market Weekday",
        "Christmas Market Saturday",
    ]
    profile_summary["profile_name"] = pd.Categorical(
        profile_summary["profile_name"],
        categories=profile_order,
        ordered=True,
    )
    profile_summary = profile_summary.sort_values("profile_name")
    for column in ["p25_daily_sales", "median_daily_sales", "p75_daily_sales"]:
        profile_summary[column] = profile_summary[column].round(2)
    return profile_summary


def build_food_trend_summary(sales: pd.DataFrame) -> pd.DataFrame:
    food_trend_summary = (
        sales.groupby("food_trend_theme", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_orders=("order_id", "nunique"),
            avg_order_value=("net_sales", "mean"),
        )
        .sort_values("total_net_sales", ascending=False)
    )
    food_trend_summary["avg_order_value"] = food_trend_summary["avg_order_value"].round(2)
    return food_trend_summary


def detect_daily_anomalies(sales: pd.DataFrame) -> pd.DataFrame:
    daily_sales = (
        sales.groupby("order_date", as_index=False)
        .agg(
            total_net_sales=("net_sales", "sum"),
            total_orders=("order_id", "nunique"),
            promotion_share=("promotion_applied_flag", "mean"),
            local_event_share=("local_event_flag", "mean"),
            dominant_festival=(
                "festival_name",
                lambda values: values.mode().iloc[0] if not values.mode().empty else "No Festival",
            ),
            dominant_holiday=(
                "school_holiday_name",
                lambda values: values.mode().iloc[0] if not values.mode().empty else "No School Holiday",
            ),
        )
        .sort_values("order_date")
    )
    daily_sales["rolling_mean"] = daily_sales["total_net_sales"].rolling(28, min_periods=14).mean().shift(1)
    daily_sales["rolling_std"] = daily_sales["total_net_sales"].rolling(28, min_periods=14).std().shift(1)
    daily_sales["anomaly_z_score"] = (
        (daily_sales["total_net_sales"] - daily_sales["rolling_mean"]) / daily_sales["rolling_std"]
    ).replace([np.inf, -np.inf], np.nan)
    daily_sales["is_anomaly"] = daily_sales["anomaly_z_score"].abs() >= 2.2

    anomaly_reason = np.where(
        daily_sales["dominant_festival"] != "No Festival",
        "Festival-driven spike",
        np.where(
            daily_sales["dominant_holiday"] != "No School Holiday",
            "School holiday shift",
            np.where(
                daily_sales["local_event_share"] >= 0.5,
                "Local event pressure",
                np.where(
                    daily_sales["promotion_share"] >= 0.4,
                    "Promotion-heavy day",
                    "Unexpected volume change",
                ),
            ),
        ),
    )
    daily_sales["anomaly_reason"] = np.where(daily_sales["is_anomaly"], anomaly_reason, "Normal range")
    return daily_sales


def create_charts(
    raw_sales: pd.DataFrame,
    clean_sales: pd.DataFrame,
    funnel: pd.DataFrame,
    missing_summary: pd.DataFrame,
    skewness_summary: pd.DataFrame,
    monthly_sales: pd.DataFrame,
    anomalies: pd.DataFrame,
    promotion_summary: pd.DataFrame,
    festival_summary: pd.DataFrame,
    holiday_summary: pd.DataFrame,
    tax_policy_summary: pd.DataFrame,
    new_poutine_summary: pd.DataFrame,
    daily_profile: pd.DataFrame,
    food_trend_summary: pd.DataFrame,
) -> None:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 5))
    funnel_plot = funnel.copy()
    sns.barplot(data=funnel_plot, x="row_count", y="stage", color="#5b8e7d")
    plt.title("Data Cleaning Funnel")
    plt.xlabel("Row Count")
    plt.ylabel("")
    for index, row in funnel_plot.reset_index(drop=True).iterrows():
        plt.text(row["row_count"] + 150, index, f"{int(row['row_count']):,}", va="center")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "data_cleaning_funnel.png", dpi=180)
    plt.close()

    missing_plot = missing_summary[
        (missing_summary["stage"] == "raw") & (missing_summary["missing_count"] > 0)
    ].sort_values("missing_count", ascending=False)
    if not missing_plot.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(data=missing_plot.head(10), x="missing_count", y="column", color="#c65b7c")
        plt.title("Missing Values in Raw Data")
        plt.xlabel("Missing Count")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "missing_values_overview.png", dpi=180)
        plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=skewness_summary, x="metric", y="skewness", hue="stage", palette="mako")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Numeric Skewness Profile")
    plt.xlabel("")
    plt.ylabel("Skewness")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "skewness_profile.png", dpi=180)
    plt.close()

    plt.figure(figsize=(13, 6))
    sns.lineplot(data=monthly_sales, x="year_month", y="total_net_sales", marker="o")
    plt.title("Monthly Net Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Net Sales")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "monthly_sales_trend.png", dpi=180)
    plt.close()

    plt.figure(figsize=(13, 6))
    sns.lineplot(data=anomalies, x="order_date", y="total_net_sales", color="#2b6777")
    anomaly_points = anomalies[anomalies["is_anomaly"]]
    if not anomaly_points.empty:
        plt.scatter(
            anomaly_points["order_date"],
            anomaly_points["total_net_sales"],
            color="#c44536",
            label="Anomaly",
            zorder=3,
        )
        plt.legend()
    plt.title("Daily Sales Anomalies")
    plt.xlabel("Date")
    plt.ylabel("Daily Net Sales")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "daily_sales_anomalies.png", dpi=180)
    plt.close()

    promotion_plot = promotion_summary[promotion_summary["promotion_group"] != "No Promotion"].copy()
    if not promotion_plot.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=promotion_plot.sort_values("avg_daily_sales_lift_pct", ascending=False),
            x="avg_daily_sales_lift_pct",
            y="promotion_group",
            color="#4c72b0",
        )
        plt.title("Promotion Lift vs No Promotion")
        plt.xlabel("Average Daily Sales Lift %")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "promotion_impact.png", dpi=180)
        plt.close()

    festival_plot = festival_summary.copy()
    if not festival_plot.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=festival_plot.head(6),
            x="avg_daily_sales",
            y="festival_name",
            color="#dd8452",
        )
        plt.title("Festival Impact on Average Daily Sales")
        plt.xlabel("Average Daily Sales")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "festival_impact.png", dpi=180)
        plt.close()

    holiday_plot = holiday_summary[holiday_summary["school_holiday_name"] != "No School Holiday"].copy()
    if not holiday_plot.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=holiday_plot.sort_values("avg_daily_sales", ascending=False),
            x="avg_daily_sales",
            y="school_holiday_name",
            color="#55a868",
        )
        plt.title("NRW School Holiday Impact")
        plt.xlabel("Average Daily Sales")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "school_holiday_impact.png", dpi=180)
        plt.close()

    tax_plot = tax_policy_summary.copy()
    if not tax_plot.empty:
        plt.figure(figsize=(9, 5))
        sns.barplot(
            data=tax_plot.sort_values("avg_unit_price_change_pct_vs_pre_2026"),
            x="avg_unit_price_change_pct_vs_pre_2026",
            y="tax_policy_phase",
            color="#937860",
        )
        plt.axvline(0, color="black", linewidth=0.8)
        plt.title("Food Price Shift After VAT Policy Change")
        plt.xlabel("Average Unit Price Change vs Pre-2026 %")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "tax_policy_impact.png", dpi=180)
        plt.close()

    if not new_poutine_summary.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=new_poutine_summary.sort_values("total_net_sales", ascending=False),
            x="total_net_sales",
            y="launch_name",
            color="#8172b2",
        )
        plt.title("New Poutine Launch Performance")
        plt.xlabel("Total Net Sales")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "new_poutine_performance.png", dpi=180)
        plt.close()

    if not daily_profile.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(
            data=daily_profile,
            x="median_daily_sales",
            y="profile_name",
            color="#4c9f70",
        )
        plt.title("Daily Sales Profile by Day Type")
        plt.xlabel("Median Daily Sales")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "day_type_sales_profile.png", dpi=180)
        plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=food_trend_summary.head(8),
        x="total_net_sales",
        y="food_trend_theme",
        color="#64b5cd",
    )
    plt.title("Food Trend Contribution to Sales")
    plt.xlabel("Total Net Sales")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "food_trend_sales_mix.png", dpi=180)
    plt.close()

    boxplot_data = pd.concat(
        [
            raw_sales.assign(stage="Raw"),
            clean_sales.assign(stage="Clean"),
        ],
        ignore_index=True,
    )
    boxplot_data["net_sales"] = pd.to_numeric(boxplot_data["net_sales"], errors="coerce")
    boxplot_data = boxplot_data.dropna(subset=["net_sales"])
    upper_cap = boxplot_data["net_sales"].quantile(0.99)
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=boxplot_data, x="stage", y="net_sales", hue="stage", dodge=False, palette="Set2")
    legend = plt.gca().get_legend()
    if legend is not None:
        legend.remove()
    plt.ylim(boxplot_data["net_sales"].min(), upper_cap)
    plt.title("Order Value Distribution Before and After Cleaning")
    plt.xlabel("")
    plt.ylabel("Net Sales")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "order_value_boxplot.png", dpi=180)
    plt.close()


def save_outputs(
    clean_sales: pd.DataFrame,
    funnel: pd.DataFrame,
    missing_summary: pd.DataFrame,
    skewness_summary: pd.DataFrame,
    quality_checks: pd.DataFrame,
    outlier_orders: pd.DataFrame,
    anomalies: pd.DataFrame,
    monthly_sales: pd.DataFrame,
    seasonality: pd.DataFrame,
    promotion_summary: pd.DataFrame,
    festival_summary: pd.DataFrame,
    external_factors: pd.DataFrame,
    holiday_summary: pd.DataFrame,
    tax_policy_summary: pd.DataFrame,
    new_poutine_summary: pd.DataFrame,
    daily_profile: pd.DataFrame,
    food_trend_summary: pd.DataFrame,
) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean_sales.to_csv(CLEAN_DATA_PATH, index=False)
    funnel.to_csv(FUNNEL_PATH, index=False)
    missing_summary.to_csv(MISSING_PATH, index=False)
    skewness_summary.to_csv(SKEWNESS_PATH, index=False)
    quality_checks.to_csv(QUALITY_CHECKS_PATH, index=False)
    outlier_orders.to_csv(OUTLIERS_PATH, index=False)
    anomalies.to_csv(ANOMALIES_PATH, index=False)
    monthly_sales.to_csv(MONTHLY_PATH, index=False)
    seasonality.to_csv(SEASONALITY_PATH, index=False)
    promotion_summary.to_csv(PROMOTION_PATH, index=False)
    festival_summary.to_csv(FESTIVAL_PATH, index=False)
    external_factors.to_csv(EXTERNAL_FACTORS_PATH, index=False)
    holiday_summary.to_csv(HOLIDAY_PATH, index=False)
    tax_policy_summary.to_csv(TAX_POLICY_PATH, index=False)
    new_poutine_summary.to_csv(NEW_POUTINE_PATH, index=False)
    daily_profile.to_csv(DAILY_PROFILE_PATH, index=False)
    food_trend_summary.to_csv(FOOD_TREND_PATH, index=False)


def write_summary(
    raw_sales: pd.DataFrame,
    clean_sales: pd.DataFrame,
    funnel: pd.DataFrame,
    missing_summary: pd.DataFrame,
    skewness_summary: pd.DataFrame,
    anomalies: pd.DataFrame,
    seasonality: pd.DataFrame,
    promotion_summary: pd.DataFrame,
    festival_summary: pd.DataFrame,
    external_factors: pd.DataFrame,
    holiday_summary: pd.DataFrame,
    tax_policy_summary: pd.DataFrame,
    new_poutine_summary: pd.DataFrame,
    daily_profile: pd.DataFrame,
    food_trend_summary: pd.DataFrame,
) -> None:
    top_missing = (
        missing_summary[(missing_summary["stage"] == "raw") & (missing_summary["missing_count"] > 0)]
        .sort_values("missing_count", ascending=False)
        .head(3)
    )
    top_missing_text = ", ".join(
        f"{row['column']} ({int(row['missing_count'])})" for _, row in top_missing.iterrows()
    ) or "No material missingness"

    peak_month = seasonality.sort_values("seasonality_index", ascending=False).iloc[0]
    weak_month = seasonality.sort_values("seasonality_index", ascending=True).iloc[0]
    anomaly_days = anomalies[anomalies["is_anomaly"]]
    top_promotion = promotion_summary[
        promotion_summary["promotion_group"] != "No Promotion"
    ].sort_values("avg_daily_sales_lift_pct", ascending=False).iloc[0]
    top_festival = festival_summary.sort_values("avg_daily_sales", ascending=False).iloc[0]
    top_food_trend = food_trend_summary.sort_values("total_net_sales", ascending=False).iloc[0]
    top_weather_factor = external_factors[
        external_factors["factor_group"] == "Weather"
    ].sort_values("total_net_sales", ascending=False).iloc[0]
    holiday_focus = holiday_summary[holiday_summary["school_holiday_name"] != "No School Holiday"]
    top_holiday = holiday_focus.sort_values("avg_daily_sales", ascending=False).iloc[0]
    tax_policy_row = tax_policy_summary[
        tax_policy_summary["tax_policy_phase"] == "Food VAT 7% from 2026-01-01"
    ].iloc[0]
    top_launch = new_poutine_summary.sort_values("total_net_sales", ascending=False).iloc[0]
    profile_lookup = daily_profile.set_index("profile_name")
    most_skewed = skewness_summary[skewness_summary["stage"] == "raw"].iloc[
        skewness_summary[skewness_summary["stage"] == "raw"]["skewness"].abs().argmax()
    ]

    summary_lines = [
        "# Frittenwerk Sales Seasonality Summary",
        "",
        "## Business context",
        (
            "A manager expectation that the following week would be busier was translated into a structured "
            "analytics workflow using restaurant sales, NRW school holidays, German festival windows, menu launches, "
            "and the January 1, 2026 gastronomy VAT change."
        ),
        "",
        "## Data quality workflow",
        f"- Raw rows analysed: {len(raw_sales):,}",
        f"- Final clean rows used for analysis: {len(clean_sales):,}",
        f"- Rows excluded from the primary analysis dataset: {len(raw_sales) - len(clean_sales):,}",
        f"- Outlier orders flagged separately: {int((funnel.iloc[2]['row_count'] - funnel.iloc[3]['row_count'])):,}",
        f"- Main raw missing-value pressure points: {top_missing_text}",
        f"- Most skewed raw metric: {most_skewed['metric']} ({most_skewed['skewness']:+.3f})",
        "",
        "## Demand and seasonality findings",
        f"- Strongest seasonal month: {peak_month['month_name']} (index {peak_month['seasonality_index']:.3f})",
        f"- Weakest seasonal month: {weak_month['month_name']} (index {weak_month['seasonality_index']:.3f})",
        (
            f"- Normal weekdays typically land around {profile_lookup.loc['Normal Weekday', 'p25_daily_sales']:,.0f}-"
            f"{profile_lookup.loc['Normal Weekday', 'p75_daily_sales']:,.0f} in daily sales."
        ),
        (
            f"- Normal weekends typically land around {profile_lookup.loc['Normal Weekend', 'p25_daily_sales']:,.0f}-"
            f"{profile_lookup.loc['Normal Weekend', 'p75_daily_sales']:,.0f} in daily sales."
        ),
        (
            f"- Festival weekdays typically land around {profile_lookup.loc['Festival Weekday', 'p25_daily_sales']:,.0f}-"
            f"{profile_lookup.loc['Festival Weekday', 'p75_daily_sales']:,.0f} in daily sales."
        ),
        (
            f"- Festival Saturdays typically land around {profile_lookup.loc['Festival Saturday', 'p25_daily_sales']:,.0f}-"
            f"{profile_lookup.loc['Festival Saturday', 'p75_daily_sales']:,.0f} in daily sales."
        ),
        (
            f"- Christmas Market Saturdays typically land around "
            f"{profile_lookup.loc['Christmas Market Saturday', 'p25_daily_sales']:,.0f}-"
            f"{profile_lookup.loc['Christmas Market Saturday', 'p75_daily_sales']:,.0f} in daily sales."
        ),
        f"- Promotion with strongest daily-sales lift: {top_promotion['promotion_group']} ({top_promotion['avg_daily_sales_lift_pct']:.1f}%)",
        f"- Highest average festival sales: {top_festival['festival_name']} ({top_festival['avg_daily_sales']:,.2f} per day)",
        f"- Strongest NRW school holiday window: {top_holiday['school_holiday_name']} ({top_holiday['avg_daily_sales']:,.2f} per day)",
        f"- Highest-selling food trend: {top_food_trend['food_trend_theme']} ({top_food_trend['total_net_sales']:,.2f})",
        f"- Strongest weather factor by total sales: {top_weather_factor['factor_label']} ({top_weather_factor['total_net_sales']:,.2f})",
        f"- Anomalous sales days flagged: {len(anomaly_days):,}",
        "",
        "## Pricing and menu changes",
        (
            f"- From January 1, 2026, the food VAT relief phase lowered the average food-item price by "
            f"{abs(tax_policy_row['avg_unit_price_change_pct_vs_pre_2026']):.1f}% versus the pre-2026 period."
        ),
        (
            f"- Top new poutine launch: {top_launch['launch_name']} with {top_launch['total_net_sales']:,.2f} "
            f"in total net sales and a '{top_launch['launch_sales_band']}' sales label."
        ),
        "",
        "## Operational recommendation",
        (
            "Staffing, prep volume, and promo coordination should be increased ahead of late-Q4 weeks, Karneval, "
            "Christmas-market periods, and high-footfall holiday windows. The price-reset from the 2026 VAT change "
            "should also be monitored because it lowered menu prices while keeping demand resilient."
        ),
    ]
    SUMMARY_PATH.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def write_linkedin_note(
    seasonality: pd.DataFrame,
    promotion_summary: pd.DataFrame,
    festival_summary: pd.DataFrame,
    holiday_summary: pd.DataFrame,
    tax_policy_summary: pd.DataFrame,
    new_poutine_summary: pd.DataFrame,
    daily_profile: pd.DataFrame,
) -> None:
    peak_month = seasonality.sort_values("seasonality_index", ascending=False).iloc[0]
    top_promotion = promotion_summary[
        promotion_summary["promotion_group"] != "No Promotion"
    ].sort_values("avg_daily_sales_lift_pct", ascending=False).iloc[0]
    top_festival = festival_summary.sort_values("avg_daily_sales", ascending=False).iloc[0]
    top_holiday = holiday_summary[holiday_summary["school_holiday_name"] != "No School Holiday"].sort_values(
        "avg_daily_sales",
        ascending=False,
    ).iloc[0]
    tax_policy_row = tax_policy_summary[
        tax_policy_summary["tax_policy_phase"] == "Food VAT 7% from 2026-01-01"
    ].iloc[0]
    top_launch = new_poutine_summary.sort_values("total_net_sales", ascending=False).iloc[0]
    weekend_profile = daily_profile.set_index("profile_name").loc["Normal Weekend"]

    linkedin_lines = [
        "# LinkedIn Case Study Draft",
        "",
        "Project: Sales seasonality and demand-driver analysis for a Frittenwerk-style restaurant operation",
        "",
        "Suggested wording:",
        (
            "I built an end-to-end restaurant analytics case study inspired by my operations experience. Using "
            "anonymized transaction data, I cleaned inconsistent records, checked missing values, outliers, skewness, "
            "and anomalies, then measured how NRW school holidays, German festival periods, promotions, new poutine "
            "launches, and the January 1, 2026 gastronomy VAT change shaped sales."
        ),
        "",
        "Highlights to mention:",
        f"- Peak seasonal month in the dataset: {peak_month['month_name']}",
        f"- Strongest promotion lift: {top_promotion['promotion_group']} ({top_promotion['avg_daily_sales_lift_pct']:.1f}%)",
        f"- Strongest festival period: {top_festival['festival_name']}",
        f"- Strongest NRW holiday window: {top_holiday['school_holiday_name']}",
        (
            f"- Normal weekend sales were calibrated to roughly "
            f"{weekend_profile['p25_daily_sales']:,.0f}-{weekend_profile['p75_daily_sales']:,.0f} per day."
        ),
        (
            f"- Average food-item price moved {tax_policy_row['avg_unit_price_change_pct_vs_pre_2026']:.1f}% "
            "after the VAT policy shift."
        ),
        f"- New poutine launch tracked in the analysis: {top_launch['launch_name']} ({top_launch['launch_sales_band']})",
        "- Delivered outputs included a cleaning funnel, data-quality reports, anomaly checks, and business charts.",
        "",
        "Public-safe note:",
        "Use 'anonymized' or 'simulated' wording if you are sharing the project outside the company.",
    ]
    LINKEDIN_PATH.write_text("\n".join(linkedin_lines) + "\n", encoding="utf-8")


def main() -> None:
    raw_sales = load_raw_sales()
    clean_sales_df, outlier_orders, funnel, quality_checks = run_cleaning_pipeline(raw_sales)
    missing_summary = pd.concat(
        [
            summarize_missing_values(raw_sales, "raw"),
            summarize_missing_values(clean_sales_df, "clean"),
        ],
        ignore_index=True,
    )
    skewness_summary = pd.concat(
        [
            summarize_numeric_skewness(raw_sales, "raw"),
            summarize_numeric_skewness(clean_sales_df, "clean"),
        ],
        ignore_index=True,
    )
    anomalies = detect_daily_anomalies(clean_sales_df)
    monthly_sales = build_monthly_sales_summary(clean_sales_df)
    seasonality = build_seasonality_index(monthly_sales)
    promotion_summary = build_promotion_impact(clean_sales_df)
    festival_summary = build_festival_impact(clean_sales_df)
    external_factors = build_external_factor_summary(clean_sales_df)
    holiday_summary = build_school_holiday_summary(clean_sales_df)
    tax_policy_summary = build_tax_policy_summary(clean_sales_df)
    new_poutine_summary = build_new_poutine_summary(clean_sales_df)
    daily_profile = build_daily_sales_profile(clean_sales_df)
    food_trend_summary = build_food_trend_summary(clean_sales_df)

    save_outputs(
        clean_sales_df,
        funnel,
        missing_summary,
        skewness_summary,
        quality_checks,
        outlier_orders,
        anomalies,
        monthly_sales,
        seasonality,
        promotion_summary,
        festival_summary,
        external_factors,
        holiday_summary,
        tax_policy_summary,
        new_poutine_summary,
        daily_profile,
        food_trend_summary,
    )
    create_charts(
        raw_sales,
        clean_sales_df,
        funnel,
        missing_summary,
        skewness_summary,
        monthly_sales,
        anomalies,
        promotion_summary,
        festival_summary,
        holiday_summary,
        tax_policy_summary,
        new_poutine_summary,
        daily_profile,
        food_trend_summary,
    )
    write_summary(
        raw_sales,
        clean_sales_df,
        funnel,
        missing_summary,
        skewness_summary,
        anomalies,
        seasonality,
        promotion_summary,
        festival_summary,
        external_factors,
        holiday_summary,
        tax_policy_summary,
        new_poutine_summary,
        daily_profile,
        food_trend_summary,
    )
    write_linkedin_note(
        seasonality,
        promotion_summary,
        festival_summary,
        holiday_summary,
        tax_policy_summary,
        new_poutine_summary,
        daily_profile,
    )

    print(f"Saved clean dataset to {CLEAN_DATA_PATH}")
    print(f"Saved processed outputs to {PROCESSED_DIR}")
    print(f"Saved charts to {CHARTS_DIR}")
    print(f"Saved summary to {SUMMARY_PATH}")
    print(f"Saved LinkedIn draft to {LINKEDIN_PATH}")


if __name__ == "__main__":
    main()
