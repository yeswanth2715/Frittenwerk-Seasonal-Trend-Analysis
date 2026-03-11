from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "frittenwerk_sales_raw.csv"
LEGACY_RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "customer_sales.csv"
VAT_RELIEF_START = pd.Timestamp("2026-01-01")

STORE_PROFILES = [
    {"store_id": "FWK-01", "store_city": "Cologne", "base_orders": 52},
    {"store_id": "FWK-02", "store_city": "Dusseldorf", "base_orders": 46},
    {"store_id": "FWK-03", "store_city": "Bonn", "base_orders": 41},
    {"store_id": "FWK-04", "store_city": "Essen", "base_orders": 42},
]

CATEGORY_DETAILS = {
    "Loaded Fries": {
        "base_weight": 0.30,
        "unit_price_mean": 9.8,
        "unit_price_std": 1.2,
        "items": ["Classic Fries", "Cheese Fries", "Truffle Fries"],
    },
    "Poutine": {
        "base_weight": 0.18,
        "unit_price_mean": 11.3,
        "unit_price_std": 1.4,
        "items": ["Classic Poutine", "BBQ Poutine"],
    },
    "Vegan Bowl": {
        "base_weight": 0.14,
        "unit_price_mean": 10.4,
        "unit_price_std": 1.1,
        "items": ["Falafel Bowl", "Green Power Bowl"],
    },
    "Wraps": {
        "base_weight": 0.15,
        "unit_price_mean": 8.6,
        "unit_price_std": 1.0,
        "items": ["Crispy Chicken Wrap", "Veggie Wrap"],
    },
    "Snacks": {
        "base_weight": 0.11,
        "unit_price_mean": 5.4,
        "unit_price_std": 0.8,
        "items": ["Croquettes", "Curry Bites"],
    },
    "Drinks": {
        "base_weight": 0.12,
        "unit_price_mean": 3.6,
        "unit_price_std": 0.5,
        "items": ["Soft Drink", "Iced Tea"],
    },
}

MONTHLY_SEASONALITY = {
    1: 1.03,
    2: 1.07,
    3: 0.98,
    4: 1.01,
    5: 1.06,
    6: 1.08,
    7: 1.02,
    8: 0.94,
    9: 0.99,
    10: 1.10,
    11: 1.08,
    12: 1.12,
}

WEATHER_PROFILES = {
    1: (["Cold", "Rainy", "Mild"], [0.58, 0.26, 0.16]),
    2: (["Cold", "Rainy", "Mild"], [0.48, 0.30, 0.22]),
    3: (["Cold", "Rainy", "Mild"], [0.26, 0.34, 0.40]),
    4: (["Rainy", "Mild", "Warm"], [0.30, 0.48, 0.22]),
    5: (["Rainy", "Warm", "Mild"], [0.20, 0.48, 0.32]),
    6: (["Warm", "Hot", "Rainy"], [0.44, 0.38, 0.18]),
    7: (["Warm", "Hot", "Rainy"], [0.40, 0.42, 0.18]),
    8: (["Warm", "Hot", "Rainy"], [0.36, 0.36, 0.28]),
    9: (["Mild", "Rainy", "Warm"], [0.38, 0.34, 0.28]),
    10: (["Mild", "Rainy", "Cold"], [0.28, 0.36, 0.36]),
    11: (["Cold", "Rainy", "Mild"], [0.42, 0.38, 0.20]),
    12: (["Cold", "Rainy", "Mild"], [0.56, 0.28, 0.16]),
}

NRW_SCHOOL_HOLIDAYS = [
    {"name": "Christmas Holiday", "start": "2023-12-21", "end": "2024-01-05"},
    {"name": "Easter Holiday", "start": "2024-03-25", "end": "2024-04-06"},
    {"name": "Pentecost Holiday", "start": "2024-05-21", "end": "2024-05-21"},
    {"name": "Summer Holiday", "start": "2024-07-08", "end": "2024-08-20"},
    {"name": "Autumn Holiday", "start": "2024-10-14", "end": "2024-10-26"},
    {"name": "Christmas Holiday", "start": "2024-12-23", "end": "2025-01-06"},
    {"name": "Easter Holiday", "start": "2025-04-14", "end": "2025-04-26"},
    {"name": "Pentecost Holiday", "start": "2025-06-10", "end": "2025-06-10"},
    {"name": "Summer Holiday", "start": "2025-07-14", "end": "2025-08-26"},
    {"name": "Autumn Holiday", "start": "2025-10-13", "end": "2025-10-25"},
    {"name": "Christmas Holiday", "start": "2025-12-22", "end": "2026-01-06"},
    {"name": "Easter Holiday", "start": "2026-03-30", "end": "2026-03-31"},
]

FESTIVAL_WINDOWS = [
    {
        "name": "Karneval",
        "start": "2024-02-08",
        "end": "2024-02-14",
        "cities": {"Cologne", "Dusseldorf", "Bonn"},
        "multiplier": 2.10,
    },
    {
        "name": "Karneval",
        "start": "2025-02-27",
        "end": "2025-03-05",
        "cities": {"Cologne", "Dusseldorf", "Bonn"},
        "multiplier": 2.12,
    },
    {
        "name": "Karneval",
        "start": "2026-02-12",
        "end": "2026-02-18",
        "cities": {"Cologne", "Dusseldorf", "Bonn"},
        "multiplier": 2.14,
    },
    {
        "name": "Easter Weekend",
        "start": "2024-03-29",
        "end": "2024-04-01",
        "cities": None,
        "multiplier": 1.86,
    },
    {
        "name": "Easter Weekend",
        "start": "2025-04-18",
        "end": "2025-04-21",
        "cities": None,
        "multiplier": 1.88,
    },
    {
        "name": "Summer Festival",
        "start": "2024-07-12",
        "end": "2024-07-21",
        "cities": None,
        "multiplier": 1.98,
    },
    {
        "name": "Summer Festival",
        "start": "2025-07-11",
        "end": "2025-07-20",
        "cities": None,
        "multiplier": 1.96,
    },
    {
        "name": "Christmas Market",
        "start": "2024-11-28",
        "end": "2024-12-23",
        "cities": None,
        "multiplier": 1.00,
    },
    {
        "name": "Christmas Market",
        "start": "2025-11-27",
        "end": "2025-12-23",
        "cities": None,
        "multiplier": 1.02,
    },
]

POUTINE_LAUNCHES = [
    {
        "name": "Chicken BBQ Poutine",
        "start": "2025-05-02",
        "end": "2025-12-31",
        "selection_weight": 0.18,
        "unit_price_delta": 1.2,
        "sales_band": "Medium",
    },
    {
        "name": "Chicken Shawarma Poutine",
        "start": "2026-01-08",
        "end": "2026-03-31",
        "selection_weight": 0.22,
        "unit_price_delta": 1.35,
        "sales_band": "Medium",
    },
]


def get_festival_context(order_date: pd.Timestamp, store_city: str) -> tuple[str, float]:
    for festival in FESTIVAL_WINDOWS:
        start = pd.Timestamp(festival["start"])
        end = pd.Timestamp(festival["end"])
        valid_city = festival["cities"] is None or store_city in festival["cities"]
        if start <= order_date <= end and valid_city:
            return str(festival["name"]), float(festival["multiplier"])
    return "No Festival", 1.0


def get_school_holiday_context(order_date: pd.Timestamp) -> tuple[str, bool, float]:
    holiday_multiplier_map = {
        "No School Holiday": 1.0,
        "Christmas Holiday": 1.06,
        "Easter Holiday": 1.02,
        "Pentecost Holiday": 1.01,
        "Summer Holiday": 0.92,
        "Autumn Holiday": 0.96,
    }
    for holiday in NRW_SCHOOL_HOLIDAYS:
        start = pd.Timestamp(holiday["start"])
        end = pd.Timestamp(holiday["end"])
        if start <= order_date <= end:
            holiday_name = str(holiday["name"])
            return holiday_name, True, holiday_multiplier_map[holiday_name]
    return "No School Holiday", False, holiday_multiplier_map["No School Holiday"]


def get_weather_condition(month: int, rng: np.random.Generator) -> str:
    conditions, probabilities = WEATHER_PROFILES[month]
    return str(rng.choice(conditions, p=probabilities))


def get_day_type_multiplier(order_date: pd.Timestamp) -> float:
    weekday = order_date.weekday()
    if weekday <= 3:
        return 0.95
    if weekday == 4:
        return 1.80
    if weekday == 5:
        return 2.50
    return 2.10


def adjust_festival_multiplier(
    festival_name: str,
    base_multiplier: float,
    order_date: pd.Timestamp,
) -> float:
    if festival_name == "No Festival":
        return 1.0

    weekday = order_date.weekday()
    default_adjustment = {
        0: 1.00,
        1: 1.00,
        2: 1.00,
        3: 1.00,
        4: 0.76,
        5: 0.58,
        6: 0.66,
    }
    christmas_adjustment = {
        0: 1.08,
        1: 1.08,
        2: 1.08,
        3: 1.08,
        4: 1.04,
        5: 1.00,
        6: 1.00,
    }
    adjustment_map = christmas_adjustment if festival_name == "Christmas Market" else default_adjustment
    return base_multiplier * adjustment_map[weekday]


def get_food_trend_theme(order_date: pd.Timestamp, rng: np.random.Generator) -> str:
    month = order_date.month
    if month == 1:
        themes = ["Vegan Focus", "Avocado Chicken Bowl", "Tijuana Street Fries"]
        probabilities = [0.46, 0.26, 0.28]
    elif month in (6, 7, 8):
        themes = ["Sweet Cheese Fire Fries", "BBQ Pulled Pork", "Tijuana Street Fries"]
        probabilities = [0.36, 0.28, 0.36]
    elif month in (10, 11, 12):
        themes = ["Chili Cheese Fries", "Truffle Craze", "Tijuana Street Fries"]
        probabilities = [0.40, 0.25, 0.35]
    else:
        themes = ["Tijuana Street Fries", "Avocado Chicken Bowl", "Chili Cheese Fries"]
        probabilities = [0.46, 0.26, 0.28]
    return str(rng.choice(themes, p=probabilities))


def get_active_poutine_launches(order_date: pd.Timestamp) -> list[dict[str, object]]:
    active_launches: list[dict[str, object]] = []
    for launch in POUTINE_LAUNCHES:
        start = pd.Timestamp(launch["start"])
        end = pd.Timestamp(launch["end"])
        if start <= order_date <= end:
            active_launches.append(launch)
    return active_launches


def get_day_promotion(
    order_date: pd.Timestamp,
    festival_name: str,
    school_holiday_name: str,
    new_poutine_active: bool,
) -> str:
    if festival_name == "Karneval":
        return "Karneval Combo"
    if festival_name == "Christmas Market":
        return "Holiday Bundle"
    if new_poutine_active and order_date.weekday() in (0, 2, 3):
        return "Poutine Trial Deal"
    if school_holiday_name == "Summer Holiday" and order_date.weekday() in (4, 5):
        return "Family Holiday Deal"
    if order_date.weekday() in (1, 2) and school_holiday_name == "No School Holiday":
        return "Student Deal"
    if order_date.day <= 7 and order_date.weekday() <= 3:
        return "Lunch Combo"
    if order_date.month in (10, 11):
        return "Truffle Special"
    return "No Promotion"


def get_promotion_usage_rate(promotion_name: str) -> float:
    usage_rates = {
        "Karneval Combo": 0.74,
        "Holiday Bundle": 0.58,
        "Poutine Trial Deal": 0.31,
        "Family Holiday Deal": 0.27,
        "Student Deal": 0.39,
        "Lunch Combo": 0.33,
        "Truffle Special": 0.27,
        "No Promotion": 0.0,
    }
    return usage_rates[promotion_name]


def get_discount_rate(promotion_name: str) -> float:
    discount_rates = {
        "Karneval Combo": 0.14,
        "Holiday Bundle": 0.12,
        "Poutine Trial Deal": 0.09,
        "Family Holiday Deal": 0.11,
        "Student Deal": 0.15,
        "Lunch Combo": 0.10,
        "Truffle Special": 0.08,
        "No Promotion": 0.0,
    }
    return discount_rates[promotion_name]


def pick_sales_channel(
    weather_condition: str,
    weekend_flag: bool,
    rng: np.random.Generator,
) -> str:
    channel_weights = {
        "Dine-In": 0.38,
        "Takeaway": 0.39,
        "Delivery": 0.23,
    }
    if weather_condition == "Rainy":
        channel_weights["Delivery"] += 0.12
        channel_weights["Dine-In"] -= 0.06
        channel_weights["Takeaway"] -= 0.06
    if weather_condition == "Hot":
        channel_weights["Takeaway"] += 0.05
        channel_weights["Delivery"] -= 0.02
        channel_weights["Dine-In"] -= 0.03
    if weekend_flag:
        channel_weights["Dine-In"] += 0.06
        channel_weights["Takeaway"] -= 0.03
        channel_weights["Delivery"] -= 0.03

    channels = list(channel_weights)
    probabilities = np.array([max(channel_weights[channel], 0.05) for channel in channels])
    probabilities = probabilities / probabilities.sum()
    return str(rng.choice(channels, p=probabilities))


def pick_meal_period(weekend_flag: bool, rng: np.random.Generator) -> str:
    periods = ["Lunch", "Dinner", "Late"]
    probabilities = [0.45, 0.43, 0.12] if not weekend_flag else [0.34, 0.48, 0.18]
    return str(rng.choice(periods, p=probabilities))


def pick_category(
    food_trend_theme: str,
    weather_condition: str,
    new_poutine_active: bool,
    rng: np.random.Generator,
) -> str:
    weights = {
        category: details["base_weight"] for category, details in CATEGORY_DETAILS.items()
    }

    if food_trend_theme == "Vegan Focus":
        weights["Vegan Bowl"] += 0.12
        weights["Wraps"] += 0.03
        weights["Loaded Fries"] -= 0.05
    elif food_trend_theme == "Avocado Chicken Bowl":
        weights["Vegan Bowl"] += 0.07
        weights["Wraps"] += 0.05
        weights["Loaded Fries"] -= 0.04
    elif food_trend_theme == "Chili Cheese Fries":
        weights["Loaded Fries"] += 0.08
        weights["Poutine"] += 0.07
        weights["Drinks"] -= 0.04
    elif food_trend_theme == "Truffle Craze":
        weights["Loaded Fries"] += 0.07
        weights["Poutine"] += 0.03
        weights["Snacks"] += 0.02
    elif food_trend_theme == "Sweet Cheese Fire Fries":
        weights["Wraps"] += 0.05
        weights["Snacks"] += 0.04
        weights["Drinks"] += 0.02
    elif food_trend_theme == "BBQ Pulled Pork":
        weights["Drinks"] += 0.10
        weights["Loaded Fries"] -= 0.04
        weights["Poutine"] -= 0.03

    if new_poutine_active:
        weights["Poutine"] += 0.03

    if weather_condition in {"Cold", "Rainy"}:
        weights["Loaded Fries"] += 0.04
        weights["Poutine"] += 0.03
    if weather_condition == "Hot":
        weights["Drinks"] += 0.08
        weights["Poutine"] -= 0.04

    categories = list(weights)
    probabilities = np.array([max(weights[category], 0.03) for category in categories])
    probabilities = probabilities / probabilities.sum()
    return str(rng.choice(categories, p=probabilities))


def pick_menu_item(
    category: str,
    order_date: pd.Timestamp,
    rng: np.random.Generator,
) -> dict[str, object]:
    if category != "Poutine":
        return {
            "menu_item": str(rng.choice(CATEGORY_DETAILS[category]["items"])),
            "new_poutine_flag": False,
            "launch_name": "Core Menu",
            "launch_sales_band": "Core",
            "unit_price_delta": 0.0,
        }

    active_launches = get_active_poutine_launches(order_date)
    choice_pool = [
        {
            "menu_item": "Classic Poutine",
            "selection_weight": 0.46,
            "new_poutine_flag": False,
            "launch_name": "Core Menu",
            "launch_sales_band": "Core",
            "unit_price_delta": 0.0,
        },
        {
            "menu_item": "BBQ Poutine",
            "selection_weight": 0.36,
            "new_poutine_flag": False,
            "launch_name": "Core Menu",
            "launch_sales_band": "Core",
            "unit_price_delta": 0.2,
        },
    ]

    for launch in active_launches:
        choice_pool.append(
            {
                "menu_item": str(launch["name"]),
                "selection_weight": float(launch["selection_weight"]),
                "new_poutine_flag": True,
                "launch_name": str(launch["name"]),
                "launch_sales_band": str(launch["sales_band"]),
                "unit_price_delta": float(launch["unit_price_delta"]),
            }
        )

    weights = np.array([entry["selection_weight"] for entry in choice_pool])
    weights = weights / weights.sum()
    selected_index = int(rng.choice(np.arange(len(choice_pool)), p=weights))
    return choice_pool[selected_index]


def get_tax_policy_context(order_date: pd.Timestamp, menu_category: str) -> dict[str, object]:
    if order_date >= VAT_RELIEF_START and menu_category != "Drinks":
        return {
            "vat_rate_pct": 7.0,
            "vat_relief_eligible_flag": True,
            "tax_policy_phase": "Food VAT 7% from 2026-01-01",
            "vat_relief_pass_through_pct": 0.05,
        }
    if order_date >= VAT_RELIEF_START and menu_category == "Drinks":
        return {
            "vat_rate_pct": 19.0,
            "vat_relief_eligible_flag": False,
            "tax_policy_phase": "Drinks stayed at 19% VAT",
            "vat_relief_pass_through_pct": 0.0,
        }
    return {
        "vat_rate_pct": 19.0,
        "vat_relief_eligible_flag": False,
        "tax_policy_phase": "Pre-2026 19% VAT",
        "vat_relief_pass_through_pct": 0.0,
    }


def inject_quality_issues(
    sales: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    messy_sales = sales.copy()

    missing_promotion_idx = rng.choice(messy_sales.index, size=max(60, len(messy_sales) // 1800), replace=False)
    missing_weather_idx = rng.choice(messy_sales.index, size=max(45, len(messy_sales) // 2200), replace=False)
    missing_trend_idx = rng.choice(messy_sales.index, size=max(45, len(messy_sales) // 2200), replace=False)
    inconsistent_channel_idx = rng.choice(
        messy_sales.index,
        size=max(80, len(messy_sales) // 1500),
        replace=False,
    )
    inconsistent_category_idx = rng.choice(
        messy_sales.index,
        size=max(80, len(messy_sales) // 1500),
        replace=False,
    )
    invalid_numeric_idx = rng.choice(messy_sales.index, size=max(40, len(messy_sales) // 3000), replace=False)
    outlier_idx = rng.choice(messy_sales.index, size=max(32, len(messy_sales) // 3800), replace=False)

    messy_sales.loc[missing_promotion_idx, "promotion_name"] = None
    messy_sales.loc[missing_weather_idx, "weather_condition"] = None
    messy_sales.loc[missing_trend_idx, "food_trend_theme"] = None

    half_channel = len(inconsistent_channel_idx) // 2
    messy_sales.loc[inconsistent_channel_idx[:half_channel], "sales_channel"] = "dine in"
    messy_sales.loc[inconsistent_channel_idx[half_channel:], "sales_channel"] = "delivery "

    half_category = len(inconsistent_category_idx) // 2
    messy_sales.loc[inconsistent_category_idx[:half_category], "menu_category"] = "loaded fries "
    messy_sales.loc[inconsistent_category_idx[half_category:], "menu_category"] = "vegan bowl"

    invalid_split = len(invalid_numeric_idx) // 2
    messy_sales.loc[invalid_numeric_idx[:invalid_split], "quantity"] = 0
    messy_sales.loc[invalid_numeric_idx[invalid_split:], "net_sales"] = -abs(
        messy_sales.loc[invalid_numeric_idx[invalid_split:], "net_sales"]
    )
    messy_sales.loc[invalid_numeric_idx[invalid_split:], "discount_eur"] = (
        messy_sales.loc[invalid_numeric_idx[invalid_split:], "gross_sales"] * 1.12
    )

    outlier_factors = rng.uniform(3.5, 5.4, size=len(outlier_idx))
    messy_sales.loc[outlier_idx, "quantity"] = (
        messy_sales.loc[outlier_idx, "quantity"].to_numpy() * rng.integers(4, 7, size=len(outlier_idx))
    )
    messy_sales.loc[outlier_idx, "gross_sales"] = (
        messy_sales.loc[outlier_idx, "gross_sales"].to_numpy() * outlier_factors
    )
    messy_sales.loc[outlier_idx, "net_sales"] = (
        messy_sales.loc[outlier_idx, "net_sales"].to_numpy() * outlier_factors
    )

    duplicates = messy_sales.loc[
        rng.choice(messy_sales.index, size=max(120, len(messy_sales) // 900), replace=False)
    ].copy()

    messy_sales = pd.concat([messy_sales, duplicates], ignore_index=True)
    messy_sales = messy_sales.sample(frac=1, random_state=42).reset_index(drop=True)

    numeric_columns = [
        "base_unit_price",
        "unit_price",
        "gross_sales",
        "discount_eur",
        "net_sales",
        "vat_rate_pct",
        "vat_relief_pass_through_pct",
    ]
    for column in numeric_columns:
        messy_sales[column] = messy_sales[column].round(2)

    return messy_sales


def generate_sales() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", "2026-03-31", freq="D")

    records: list[dict[str, object]] = []
    order_sequence = 1

    for store in STORE_PROFILES:
        for order_date in dates:
            festival_name, festival_multiplier = get_festival_context(order_date, store["store_city"])
            school_holiday_name, school_holiday_flag, school_holiday_multiplier = get_school_holiday_context(
                order_date
            )
            weather_condition = get_weather_condition(order_date.month, rng)
            food_trend_theme = get_food_trend_theme(order_date, rng)
            active_launches = get_active_poutine_launches(order_date)
            new_poutine_active = bool(active_launches)

            weekend_flag = bool(order_date.weekday() >= 4)
            day_type_multiplier = get_day_type_multiplier(order_date)
            local_event_probability = 0.08 if weekend_flag else 0.03
            if festival_name != "No Festival":
                local_event_probability += 0.12
            local_event_flag = bool(rng.random() < local_event_probability)

            promotion_name = get_day_promotion(
                order_date,
                festival_name,
                school_holiday_name,
                new_poutine_active,
            )

            weather_multiplier = {
                "Cold": 1.05,
                "Rainy": 1.04,
                "Mild": 1.0,
                "Warm": 0.99,
                "Hot": 0.94,
            }[weather_condition]
            festival_multiplier = adjust_festival_multiplier(festival_name, festival_multiplier, order_date)
            promotion_multiplier = 1.06 if promotion_name != "No Promotion" else 1.0
            local_event_multiplier = 1.08 if local_event_flag else 1.0
            tax_policy_multiplier = 1.05 if order_date >= VAT_RELIEF_START else 1.0

            expected_orders = (
                store["base_orders"]
                * MONTHLY_SEASONALITY[order_date.month]
                * festival_multiplier
                * school_holiday_multiplier
                * weather_multiplier
                * day_type_multiplier
                * promotion_multiplier
                * local_event_multiplier
                * tax_policy_multiplier
            )
            daily_order_count = int(max(18, rng.poisson(expected_orders)))

            for _ in range(daily_order_count):
                order_food_trend = food_trend_theme if rng.random() < 0.75 else get_food_trend_theme(order_date, rng)
                menu_category = pick_category(order_food_trend, weather_condition, new_poutine_active, rng)
                menu_selection = pick_menu_item(menu_category, order_date, rng)
                sales_channel = pick_sales_channel(weather_condition, weekend_flag, rng)
                meal_period = pick_meal_period(weekend_flag, rng)

                promotion_applied_flag = bool(
                    promotion_name != "No Promotion" and rng.random() < get_promotion_usage_rate(promotion_name)
                )

                quantity_lambda = 1.10
                if menu_category == "Drinks":
                    quantity_lambda += 0.30
                if sales_channel == "Delivery":
                    quantity_lambda += 0.22
                if meal_period == "Dinner":
                    quantity_lambda += 0.18
                if festival_name != "No Festival":
                    quantity_lambda += 0.20
                if local_event_flag:
                    quantity_lambda += 0.10
                if order_date >= VAT_RELIEF_START and menu_category != "Drinks":
                    quantity_lambda += 0.05
                quantity = int(max(1, rng.poisson(quantity_lambda) + 1))

                price_mean = (
                    CATEGORY_DETAILS[menu_category]["unit_price_mean"] + float(menu_selection["unit_price_delta"])
                )
                price_std = CATEGORY_DETAILS[menu_category]["unit_price_std"]
                base_unit_price = float(max(2.4, rng.normal(price_mean, price_std)))

                tax_policy_context = get_tax_policy_context(order_date, menu_category)
                launch_trial_discount_pct = (
                    0.04 if bool(menu_selection["new_poutine_flag"]) and rng.random() < 0.24 else 0.0
                )
                unit_price = base_unit_price
                unit_price *= 1 - float(tax_policy_context["vat_relief_pass_through_pct"])
                unit_price *= 1 - launch_trial_discount_pct

                gross_sales = quantity * unit_price
                discount_eur = 0.0
                if promotion_applied_flag:
                    discount_eur = gross_sales * get_discount_rate(promotion_name)
                net_sales = gross_sales - discount_eur

                price_adjustment_reasons = []
                if float(tax_policy_context["vat_relief_pass_through_pct"]) > 0:
                    price_adjustment_reasons.append("VAT Pass-Through")
                if launch_trial_discount_pct > 0:
                    price_adjustment_reasons.append("Launch Trial Price")
                price_adjustment_reason = (
                    " + ".join(price_adjustment_reasons) if price_adjustment_reasons else "No Base Price Reduction"
                )

                records.append(
                    {
                        "order_id": f"FWK-ORD-{order_sequence:07d}",
                        "order_date": order_date,
                        "store_id": store["store_id"],
                        "store_city": store["store_city"],
                        "sales_channel": sales_channel,
                        "meal_period": meal_period,
                        "menu_category": menu_category,
                        "menu_item": menu_selection["menu_item"],
                        "new_poutine_flag": bool(menu_selection["new_poutine_flag"]),
                        "launch_name": menu_selection["launch_name"],
                        "launch_sales_band": menu_selection["launch_sales_band"],
                        "quantity": quantity,
                        "base_unit_price": round(base_unit_price, 2),
                        "unit_price": round(unit_price, 2),
                        "gross_sales": round(gross_sales, 2),
                        "discount_eur": round(discount_eur, 2),
                        "net_sales": round(net_sales, 2),
                        "promotion_name": promotion_name,
                        "promotion_applied_flag": promotion_applied_flag,
                        "festival_name": festival_name,
                        "weather_condition": weather_condition,
                        "school_holiday_name": school_holiday_name,
                        "school_holiday_flag": school_holiday_flag,
                        "local_event_flag": local_event_flag,
                        "food_trend_theme": order_food_trend,
                        "vat_rate_pct": float(tax_policy_context["vat_rate_pct"]),
                        "vat_relief_eligible_flag": bool(tax_policy_context["vat_relief_eligible_flag"]),
                        "tax_policy_phase": tax_policy_context["tax_policy_phase"],
                        "vat_relief_pass_through_pct": round(
                            float(tax_policy_context["vat_relief_pass_through_pct"]) + launch_trial_discount_pct,
                            4,
                        ),
                        "price_adjustment_reason": price_adjustment_reason,
                    }
                )
                order_sequence += 1

    sales = pd.DataFrame.from_records(records)
    return inject_quality_issues(sales, rng)


def main() -> None:
    sales = generate_sales()
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    sales.to_csv(RAW_DATA_PATH, index=False)
    sales.to_csv(LEGACY_RAW_DATA_PATH, index=False)
    print(f"Wrote {len(sales):,} rows to {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()
