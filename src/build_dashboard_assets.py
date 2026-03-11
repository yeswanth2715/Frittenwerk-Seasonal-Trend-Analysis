from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MPLCONFIG_DIR = BASE_DIR / ".matplotlib"
MPLCONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIG_DIR))

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")

PROCESSED_DIR = BASE_DIR / "data" / "processed"
DASHBOARD_DIR = BASE_DIR / "outputs" / "dashboards"

MONTHLY_PATH = PROCESSED_DIR / "monthly_sales_summary.csv"
SEASONALITY_PATH = PROCESSED_DIR / "monthly_seasonality_index.csv"
PROMOTION_PATH = PROCESSED_DIR / "promotion_impact_summary.csv"
FESTIVAL_PATH = PROCESSED_DIR / "festival_impact_summary.csv"
HOLIDAY_PATH = PROCESSED_DIR / "school_holiday_impact_summary.csv"
PROFILE_PATH = PROCESSED_DIR / "daily_sales_profile.csv"
FOOD_TREND_PATH = PROCESSED_DIR / "food_trend_summary.csv"
INVENTORY_PATH = PROCESSED_DIR / "inventory_cycle_summary.csv"

SEASONAL_DASHBOARD_PATH = DASHBOARD_DIR / "seasonal_trends_dashboard.png"
INVENTORY_DASHBOARD_PATH = DASHBOARD_DIR / "inventory_management_dashboard.png"
GUIDE_PATH = DASHBOARD_DIR / "powerbi_tableau_dashboard_guide.md"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run the analysis pipeline first.")
    return pd.read_csv(path, parse_dates=["stock_delivery_date"] if "inventory_cycle" in path.name else None)


def format_currency_compact(value: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"


def add_kpi_card(ax: plt.Axes, title: str, value: str, subtitle: str, color: str) -> None:
    ax.set_facecolor(color)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.04, 0.80, title, fontsize=11, fontweight="bold", color="#1F2933", transform=ax.transAxes)
    ax.text(0.04, 0.44, value, fontsize=20, fontweight="bold", color="#0B1320", transform=ax.transAxes)
    ax.text(0.04, 0.15, subtitle, fontsize=9, color="#425466", transform=ax.transAxes)


def create_seasonal_dashboard(
    monthly_sales: pd.DataFrame,
    seasonality: pd.DataFrame,
    promotions: pd.DataFrame,
    festivals: pd.DataFrame,
    holidays: pd.DataFrame,
    profiles: pd.DataFrame,
    food_trends: pd.DataFrame,
) -> None:
    sns.set_theme(style="whitegrid")
    peak_month = seasonality.sort_values("seasonality_index", ascending=False).iloc[0]
    weak_month = seasonality.sort_values("seasonality_index", ascending=True).iloc[0]
    top_promotion = promotions[promotions["promotion_group"] != "No Promotion"].sort_values(
        "avg_daily_sales_lift_pct",
        ascending=False,
    ).iloc[0]
    top_food_trend = food_trends.sort_values("total_net_sales", ascending=False).iloc[0]

    fig = plt.figure(figsize=(18, 11), facecolor="#F5F1E8")
    gs = fig.add_gridspec(3, 12, height_ratios=[1.2, 3.2, 3.2], hspace=0.42, wspace=0.55)

    card_axes = [fig.add_subplot(gs[0, 0:3]), fig.add_subplot(gs[0, 3:6]), fig.add_subplot(gs[0, 6:9]), fig.add_subplot(gs[0, 9:12])]
    add_kpi_card(card_axes[0], "Peak Month", str(peak_month["month_name"]), f"Seasonality index {peak_month['seasonality_index']:.3f}", "#D9E7FF")
    add_kpi_card(card_axes[1], "Weakest Month", str(weak_month["month_name"]), f"Seasonality index {weak_month['seasonality_index']:.3f}", "#FDE7D8")
    add_kpi_card(card_axes[2], "Top Promotion", str(top_promotion["promotion_group"]), f"Lift {top_promotion['avg_daily_sales_lift_pct']:.1f}%", "#E2F4E8")
    add_kpi_card(card_axes[3], "Top Food Trend", str(top_food_trend["food_trend_theme"]), format_currency_compact(float(top_food_trend["total_net_sales"])), "#FBE5F4")

    ax_monthly = fig.add_subplot(gs[1, 0:7])
    monthly_plot = monthly_sales.copy()
    sns.lineplot(
        data=monthly_plot,
        x="year_month",
        y="total_net_sales",
        marker="o",
        linewidth=2.5,
        color="#0F766E",
        ax=ax_monthly,
    )
    ax_monthly.set_title("Uncovering Seasonal Trends", fontsize=16, fontweight="bold", loc="left")
    ax_monthly.set_xlabel("")
    ax_monthly.set_ylabel("Net Sales")
    ax_monthly.tick_params(axis="x", rotation=45)

    ax_seasonality = fig.add_subplot(gs[1, 7:12])
    seasonality_plot = seasonality.sort_values("month")
    sns.barplot(
        data=seasonality_plot,
        x="month_name",
        y="seasonality_index",
        color="#D97706",
        ax=ax_seasonality,
    )
    ax_seasonality.axhline(1.0, color="#4B5563", linewidth=1, linestyle="--")
    ax_seasonality.set_title("Seasonality Index by Month", fontsize=13, fontweight="bold", loc="left")
    ax_seasonality.set_xlabel("")
    ax_seasonality.set_ylabel("Index")

    ax_profiles = fig.add_subplot(gs[2, 0:4])
    sns.barplot(
        data=profiles,
        x="median_daily_sales",
        y="profile_name",
        color="#1D4ED8",
        ax=ax_profiles,
    )
    ax_profiles.set_title("Daily Sales Profile", fontsize=13, fontweight="bold", loc="left")
    ax_profiles.set_xlabel("Median Daily Sales")
    ax_profiles.set_ylabel("")

    ax_festivals = fig.add_subplot(gs[2, 4:8])
    festival_plot = festivals[festivals["festival_name"] != "No Festival"].head(5)
    sns.barplot(
        data=festival_plot,
        x="avg_daily_sales",
        y="festival_name",
        color="#BE185D",
        ax=ax_festivals,
    )
    ax_festivals.set_title("Festival Demand Impact", fontsize=13, fontweight="bold", loc="left")
    ax_festivals.set_xlabel("Avg Daily Sales")
    ax_festivals.set_ylabel("")

    ax_food = fig.add_subplot(gs[2, 8:12])
    food_plot = food_trends.head(6)
    sns.barplot(
        data=food_plot,
        x="total_net_sales",
        y="food_trend_theme",
        color="#7C3AED",
        ax=ax_food,
    )
    ax_food.set_title("Food Trends Driving Sales", fontsize=13, fontweight="bold", loc="left")
    ax_food.set_xlabel("Total Net Sales")
    ax_food.set_ylabel("")

    fig.suptitle("Sheet 1: Seasonal Trends", fontsize=24, fontweight="bold", x=0.03, y=0.98, ha="left")
    fig.text(
        0.03,
        0.94,
        "Monthly demand, day-type ranges, promotion lift, festival pressure, and menu trends.",
        fontsize=11,
        color="#425466",
    )
    fig.savefig(SEASONAL_DASHBOARD_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)


def create_inventory_dashboard(inventory_cycles: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")
    waste_cycles = inventory_cycles[inventory_cycles["estimated_waste_units"] > 0].copy()
    top_driver = (
        waste_cycles.groupby("primary_wastage_driver", as_index=False)["estimated_waste_units"]
        .sum()
        .sort_values("estimated_waste_units", ascending=False)
        .iloc[0]
    )
    top_cycle = waste_cycles.sort_values("estimated_waste_units", ascending=False).iloc[0]
    waste_rate = (
        inventory_cycles["estimated_waste_units"].sum() / inventory_cycles["observed_stock_order_units"].sum() * 100
    )

    fig = plt.figure(figsize=(18, 11), facecolor="#EEF4F0")
    gs = fig.add_gridspec(3, 12, height_ratios=[1.2, 3.1, 3.4], hspace=0.42, wspace=0.55)

    card_axes = [fig.add_subplot(gs[0, 0:3]), fig.add_subplot(gs[0, 3:6]), fig.add_subplot(gs[0, 6:9]), fig.add_subplot(gs[0, 9:12])]
    add_kpi_card(card_axes[0], "Excess Stock", f"{inventory_cycles['estimated_waste_units'].sum():,.0f}", "Estimated extra units", "#D8F3DC")
    add_kpi_card(card_axes[1], "Wastage Rate", f"{waste_rate:.1f}%", "Observed stock vs recommended stock", "#DDEAFE")
    add_kpi_card(card_axes[2], "Top Driver", str(top_driver["primary_wastage_driver"]), f"{top_driver['estimated_waste_units']:,.0f} units", "#FEE2E2")
    add_kpi_card(card_axes[3], "High-Risk Cycle", top_cycle["stock_delivery_date"].strftime("%Y-%m-%d"), f"{top_cycle['estimated_waste_units']:,.1f} units", "#FDF3C7")

    ax_stock = fig.add_subplot(gs[1, 0:7])
    line_plot = inventory_cycles.tail(24).copy()
    sns.lineplot(
        data=line_plot,
        x="stock_delivery_date",
        y="recommended_stock_units",
        linewidth=2.5,
        color="#0F766E",
        label="Recommended Stock",
        ax=ax_stock,
    )
    sns.lineplot(
        data=line_plot,
        x="stock_delivery_date",
        y="observed_stock_order_units",
        linewidth=2.5,
        color="#B91C1C",
        label="Observed Stock Order",
        ax=ax_stock,
    )
    ax_stock.set_title("Recommended vs Observed Stock Orders", fontsize=16, fontweight="bold", loc="left")
    ax_stock.set_xlabel("")
    ax_stock.set_ylabel("Stock Units")
    ax_stock.tick_params(axis="x", rotation=45)

    ax_driver = fig.add_subplot(gs[1, 7:12])
    driver_plot = waste_cycles.groupby("primary_wastage_driver", as_index=False)["estimated_waste_units"].sum()
    driver_plot = driver_plot.sort_values("estimated_waste_units", ascending=False)
    sns.barplot(
        data=driver_plot,
        x="estimated_waste_units",
        y="primary_wastage_driver",
        color="#B45309",
        ax=ax_driver,
    )
    ax_driver.set_title("Wastage by Driver", fontsize=13, fontweight="bold", loc="left")
    ax_driver.set_xlabel("Estimated Excess Stock Units")
    ax_driver.set_ylabel("")

    ax_scatter = fig.add_subplot(gs[2, 0:7])
    palette = {
        "Festival stock uplift": "#C2410C",
        "Low-sales order value inconsistency": "#7C2D12",
        "Product-mix volatility": "#1D4ED8",
        "No excess stock": "#6B7280",
    }
    for driver, group in waste_cycles.groupby("primary_wastage_driver"):
        ax_scatter.scatter(
            group["cycle_total_sales"],
            group["estimated_waste_units"],
            s=np.clip(group["observed_stock_order_units"] / 4, 25, 220),
            alpha=0.75,
            label=driver,
            color=palette.get(driver, "#475569"),
            edgecolor="white",
            linewidth=0.6,
        )
    ax_scatter.set_title("Sales vs Wastage Risk", fontsize=13, fontweight="bold", loc="left")
    ax_scatter.set_xlabel("Cycle Total Sales")
    ax_scatter.set_ylabel("Estimated Excess Stock Units")
    ax_scatter.legend(frameon=False, loc="upper left")

    ax_table = fig.add_subplot(gs[2, 7:12])
    ax_table.axis("off")
    top_cases = waste_cycles.sort_values("estimated_waste_units", ascending=False).head(6).copy()
    top_cases["stock_delivery_date"] = top_cases["stock_delivery_date"].dt.strftime("%Y-%m-%d")
    table_values = top_cases[
        ["stock_delivery_date", "inventory_cycle", "primary_wastage_driver", "estimated_waste_units"]
    ].copy()
    table_values["estimated_waste_units"] = table_values["estimated_waste_units"].map(lambda value: f"{value:,.1f}")
    table = ax_table.table(
        cellText=table_values.values,
        colLabels=["Cycle Date", "Cycle", "Driver", "Waste Units"],
        cellLoc="left",
        colLoc="left",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.6)
    ax_table.set_title("Top Risk Cycles", fontsize=13, fontweight="bold", loc="left", pad=12)

    fig.suptitle("Sheet 2: Inventory Management", fontsize=24, fontweight="bold", x=0.03, y=0.98, ha="left")
    fig.text(
        0.03,
        0.94,
        "Monday/Thursday stock cycles, estimated wastage, driver mix, and the highest-risk inventory periods.",
        fontsize=11,
        color="#425466",
    )
    fig.savefig(INVENTORY_DASHBOARD_PATH, dpi=180, bbox_inches="tight")
    plt.close(fig)


def write_dashboard_guide(
    seasonality: pd.DataFrame,
    promotions: pd.DataFrame,
    festivals: pd.DataFrame,
    holidays: pd.DataFrame,
    food_trends: pd.DataFrame,
    inventory_cycles: pd.DataFrame,
) -> None:
    peak_month = seasonality.sort_values("seasonality_index", ascending=False).iloc[0]
    top_promotion = promotions[promotions["promotion_group"] != "No Promotion"].sort_values(
        "avg_daily_sales_lift_pct",
        ascending=False,
    ).iloc[0]
    top_festival = festivals[festivals["festival_name"] != "No Festival"].sort_values(
        "avg_daily_sales",
        ascending=False,
    ).iloc[0]
    top_holiday = holidays[holidays["school_holiday_name"] != "No School Holiday"].sort_values(
        "avg_daily_sales",
        ascending=False,
    ).iloc[0]
    top_food_trend = food_trends.sort_values("total_net_sales", ascending=False).iloc[0]
    waste_cycles = inventory_cycles[inventory_cycles["estimated_waste_units"] > 0]
    top_driver = waste_cycles.groupby("primary_wastage_driver", as_index=False)["estimated_waste_units"].sum().sort_values(
        "estimated_waste_units",
        ascending=False,
    ).iloc[0]
    top_cycle = waste_cycles.sort_values("estimated_waste_units", ascending=False).iloc[0]

    guide_lines = [
        "# Power BI / Tableau Dashboard Guide",
        "",
        "This package gives you two dashboard sheets built from the processed CSV outputs in this repository.",
        "",
        "## Sheet 1: Uncovering Seasonal Trends",
        "- KPI cards: Peak Month, Weakest Month, Top Promotion Lift, Top Food Trend",
        "- Main line chart: `monthly_sales_summary.csv` using `year_month` vs `total_net_sales`",
        "- Bar chart: `monthly_seasonality_index.csv` using `month_name` vs `seasonality_index`",
        "- Bar chart: `daily_sales_profile.csv` using `profile_name` vs `median_daily_sales`",
        "- Bar chart: `festival_impact_summary.csv` using `festival_name` vs `avg_daily_sales`",
        "- Bar chart: `food_trend_summary.csv` using `food_trend_theme` vs `total_net_sales`",
        "- Suggested slicers: `year`, `month_name`, `festival_name`, `promotion_group`, `school_holiday_name`",
        "",
        "Recommended headline metrics:",
        f"- Peak month: {peak_month['month_name']} ({peak_month['seasonality_index']:.3f})",
        f"- Strongest promotion lift: {top_promotion['promotion_group']} ({top_promotion['avg_daily_sales_lift_pct']:.1f}%)",
        f"- Strongest festival period: {top_festival['festival_name']}",
        f"- Strongest NRW holiday window: {top_holiday['school_holiday_name']}",
        f"- Top food trend: {top_food_trend['food_trend_theme']}",
        "",
        "## Sheet 2: Inventory Management",
        "- KPI cards: Excess Stock Units, Wastage Rate, Top Wastage Driver, Highest-Risk Cycle",
        "- Dual-line chart: `inventory_cycle_summary.csv` using `stock_delivery_date` vs `recommended_stock_units` and `observed_stock_order_units`",
        "- Bar chart: `primary_wastage_driver` vs `estimated_waste_units`",
        "- Scatter chart: `cycle_total_sales` vs `estimated_waste_units`, sized by `observed_stock_order_units`, colored by `primary_wastage_driver`",
        "- Detail table: `stock_delivery_date`, `inventory_cycle`, `dominant_festival`, `primary_wastage_driver`, `estimated_waste_units`",
        "- Suggested slicers: `inventory_cycle`, `coverage_window`, `dominant_festival`, `dominant_holiday`, `cycle_sales_band`",
        "",
        "Recommended headline metrics:",
        f"- Top wastage driver: {top_driver['primary_wastage_driver']} ({top_driver['estimated_waste_units']:,.1f} units)",
        f"- Highest-risk cycle: {top_cycle['stock_delivery_date']:%Y-%m-%d}",
        f"- Overall wastage rate: {inventory_cycles['estimated_waste_units'].sum() / inventory_cycles['observed_stock_order_units'].sum() * 100:.1f}%",
        "",
        "## Files to use",
        f"- [seasonal_trends_dashboard.png]({SEASONAL_DASHBOARD_PATH})",
        f"- [inventory_management_dashboard.png]({INVENTORY_DASHBOARD_PATH})",
        f"- [monthly_sales_summary.csv]({MONTHLY_PATH})",
        f"- [monthly_seasonality_index.csv]({SEASONALITY_PATH})",
        f"- [promotion_impact_summary.csv]({PROMOTION_PATH})",
        f"- [festival_impact_summary.csv]({FESTIVAL_PATH})",
        f"- [school_holiday_impact_summary.csv]({HOLIDAY_PATH})",
        f"- [daily_sales_profile.csv]({PROFILE_PATH})",
        f"- [food_trend_summary.csv]({FOOD_TREND_PATH})",
        f"- [inventory_cycle_summary.csv]({INVENTORY_PATH})",
    ]
    GUIDE_PATH.write_text("\n".join(guide_lines) + "\n", encoding="utf-8")


def main() -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    monthly_sales = pd.read_csv(MONTHLY_PATH)
    seasonality = pd.read_csv(SEASONALITY_PATH)
    promotions = pd.read_csv(PROMOTION_PATH)
    festivals = pd.read_csv(FESTIVAL_PATH)
    holidays = pd.read_csv(HOLIDAY_PATH)
    profiles = pd.read_csv(PROFILE_PATH)
    food_trends = pd.read_csv(FOOD_TREND_PATH)
    inventory_cycles = pd.read_csv(INVENTORY_PATH, parse_dates=["stock_delivery_date"])

    create_seasonal_dashboard(monthly_sales, seasonality, promotions, festivals, holidays, profiles, food_trends)
    create_inventory_dashboard(inventory_cycles)
    write_dashboard_guide(seasonality, promotions, festivals, holidays, food_trends, inventory_cycles)

    print(f"Saved seasonal dashboard mockup to {SEASONAL_DASHBOARD_PATH}")
    print(f"Saved inventory dashboard mockup to {INVENTORY_DASHBOARD_PATH}")
    print(f"Saved dashboard guide to {GUIDE_PATH}")


if __name__ == "__main__":
    main()
