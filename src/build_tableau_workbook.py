from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
TABLEAU_DIR = BASE_DIR / "outputs" / "tableau"
CSV_PATH = TABLEAU_DIR / "frittenwerk_dashboard_data.csv"
WORKBOOK_PATHS = [
    TABLEAU_DIR / "frittenwerk_analytics_dashboard.twb",
    TABLEAU_DIR / "frittenwerk_analytics_dashboard_fixed.twb",
    TABLEAU_DIR / "frittenwerk_analytics_dashboard_enhanced.twb",
]
GUIDE_PATH = TABLEAU_DIR / "tableau_desktop_guide.md"

USER_NS = "http://www.tableausoftware.com/xml/user"
ET.register_namespace("user", USER_NS)

WORKBOOK_NAME = "Frittenwerk Analytics Overview"
DATASOURCE_NAME = "DashboardData"
DATASOURCE_CAPTION = "Frittenwerk Dashboard Data"
CONNECTION_NAME = "textscan.dashboard"
TABLE_NAME = "frittenwerk_dashboard_data#csv"

SECTION_COLORS = {
    "Monthly Sales": "#0F766E",
    "Seasonality Index": "#D97706",
    "Festival Impact": "#DB2777",
    "Inventory Wastage Drivers": "#2563EB",
}

FESTIVAL_COLORS = ["#E11D48", "#F97316", "#F59E0B", "#14B8A6", "#6366F1", "#8B5CF6"]
DRIVER_COLORS = ["#7C3AED", "#EF4444", "#0EA5E9", "#F59E0B"]


@dataclass(frozen=True)
class WorksheetSpec:
    name: str
    section: str
    mark_class: str
    rows_expr: str
    cols_expr: str
    color_field: str
    show_text_labels: bool
    title_color: str
    axis_title: str
    number_format: str
    size_field: str | None = None


WORKSHEET_SPECS = [
    WorksheetSpec(
        name="Monthly Sales Trend",
        section="Monthly Sales",
        mark_class="Line",
        rows_expr=f"[{DATASOURCE_NAME}].[sum:Value:qk]",
        cols_expr=f"[{DATASOURCE_NAME}].[Category]",
        color_field="Chart Section",
        show_text_labels=False,
        title_color=SECTION_COLORS["Monthly Sales"],
        axis_title="Monthly Net Sales",
        number_format="*#,##0",
    ),
    WorksheetSpec(
        name="Seasonality Wave",
        section="Seasonality Index",
        mark_class="Area",
        rows_expr=f"[{DATASOURCE_NAME}].[sum:Value:qk]",
        cols_expr=f"[{DATASOURCE_NAME}].[Category]",
        color_field="Chart Section",
        show_text_labels=True,
        title_color=SECTION_COLORS["Seasonality Index"],
        axis_title="Seasonality Index",
        number_format="0.000",
    ),
    WorksheetSpec(
        name="Festival Demand Lift",
        section="Festival Impact",
        mark_class="Bar",
        rows_expr=f"[{DATASOURCE_NAME}].[Category]",
        cols_expr=f"[{DATASOURCE_NAME}].[sum:Value:qk]",
        color_field="Category",
        show_text_labels=True,
        title_color=SECTION_COLORS["Festival Impact"],
        axis_title="Average Daily Sales",
        number_format="*#,##0",
    ),
    WorksheetSpec(
        name="Inventory Risk Bubbles",
        section="Inventory Wastage Drivers",
        mark_class="Circle",
        rows_expr=f"[{DATASOURCE_NAME}].[Category]",
        cols_expr=f"[{DATASOURCE_NAME}].[sum:Value:qk]",
        color_field="Category",
        show_text_labels=True,
        title_color=SECTION_COLORS["Inventory Wastage Drivers"],
        axis_title="Estimated Waste Units",
        number_format="*#,##0",
        size_field=f"[{DATASOURCE_NAME}].[sum:Value:qk]",
    ),
]


def qname(local_name: str) -> str:
    return f"{{{USER_NS}}}{local_name}"


def build_dashboard_assets() -> tuple[pd.DataFrame, dict[str, str], dict[str, str], list[dict[str, str]]]:
    monthly = pd.read_csv(PROCESSED_DIR / "monthly_sales_summary.csv")
    seasonality = pd.read_csv(PROCESSED_DIR / "monthly_seasonality_index.csv")
    festivals = pd.read_csv(PROCESSED_DIR / "festival_impact_summary.csv")
    promotions = pd.read_csv(PROCESSED_DIR / "promotion_impact_summary.csv")
    inventory = pd.read_csv(PROCESSED_DIR / "inventory_cycle_summary.csv")

    frames: list[pd.DataFrame] = []
    aliases: dict[str, str] = {}
    category_palette: dict[str, str] = {}

    def add_section(section: str, labels: list[str], values: list[float], palette: list[str] | None = None) -> None:
        keys = [f"{index:02d} | {label}" for index, label in enumerate(labels, start=1)]
        frames.append(
            pd.DataFrame(
                {
                    "Chart Section": section,
                    "Category": keys,
                    "Value": values,
                }
            )
        )
        aliases.update(dict(zip(keys, labels)))
        if palette:
            for index, key in enumerate(keys):
                category_palette[key] = palette[index % len(palette)]

    monthly = monthly.sort_values("year_month").reset_index(drop=True)
    add_section("Monthly Sales", monthly["year_month"].tolist(), monthly["total_net_sales"].astype(float).tolist())

    seasonality = seasonality.sort_values("month").reset_index(drop=True)
    add_section("Seasonality Index", seasonality["month_name"].tolist(), seasonality["seasonality_index"].astype(float).tolist())

    festivals = festivals.sort_values("avg_daily_sales", ascending=False).reset_index(drop=True)
    add_section("Festival Impact", festivals["festival_name"].tolist(), festivals["avg_daily_sales"].astype(float).tolist(), FESTIVAL_COLORS)

    drivers = (
        inventory.loc[inventory["estimated_waste_units"] > 0, ["primary_wastage_driver", "estimated_waste_units"]]
        .groupby("primary_wastage_driver", as_index=False)["estimated_waste_units"]
        .sum()
        .sort_values("estimated_waste_units", ascending=False)
        .reset_index(drop=True)
    )
    add_section(
        "Inventory Wastage Drivers",
        drivers["primary_wastage_driver"].tolist(),
        drivers["estimated_waste_units"].astype(float).tolist(),
        DRIVER_COLORS,
    )

    total_sales = monthly["total_net_sales"].sum()
    total_orders = int(monthly["total_orders"].sum())
    avg_order_value = monthly["avg_order_value"].mean()
    peak_month = monthly.sort_values("total_net_sales", ascending=False).iloc[0]
    peak_seasonality = seasonality.sort_values("seasonality_index", ascending=False).iloc[0]
    top_promotion = promotions[promotions["promotion_group"] != "No Promotion"].sort_values(
        "avg_daily_sales_lift_pct",
        ascending=False,
    ).iloc[0]
    top_festival = festivals.sort_values("avg_daily_sales", ascending=False).iloc[0]
    top_driver = drivers.iloc[0]
    wastage_rate = inventory["estimated_waste_units"].sum() / inventory["observed_stock_order_units"].sum() * 100

    kpis = [
        {
            "title": "Total Sales",
            "value": f"{total_sales:,.0f}",
            "subtitle": f"Avg order value {avg_order_value:.2f}",
            "accent": SECTION_COLORS["Monthly Sales"],
        },
        {
            "title": "Total Orders",
            "value": f"{total_orders:,}",
            "subtitle": f"Top promo {top_promotion['promotion_group']}",
            "accent": "#B45309",
        },
        {
            "title": "Peak Month",
            "value": str(peak_month["month_name"]),
            "subtitle": f"{peak_month['total_net_sales']:,.0f} sales | seasonality peak {peak_seasonality['month_name']}",
            "accent": SECTION_COLORS["Festival Impact"],
        },
        {
            "title": "Wastage Rate",
            "value": f"{wastage_rate:.1f}%",
            "subtitle": f"Top festival {top_festival['festival_name']} | driver {top_driver['primary_wastage_driver']}",
            "accent": SECTION_COLORS["Inventory Wastage Drivers"],
        },
    ]

    return pd.concat(frames, ignore_index=True), aliases, category_palette, kpis


def write_dashboard_csv(frame: pd.DataFrame) -> None:
    TABLEAU_DIR.mkdir(parents=True, exist_ok=True)
    frame.to_csv(CSV_PATH, index=False)


def add_metadata_record(parent: ET.Element, remote_name: str, ordinal: int, datatype: str) -> None:
    metadata_record = ET.SubElement(parent, "metadata-record", {"class": "column"})
    ET.SubElement(metadata_record, "remote-name").text = remote_name
    ET.SubElement(metadata_record, "remote-type").text = {"string": "129", "real": "5"}[datatype]
    ET.SubElement(metadata_record, "local-name").text = f"[{remote_name}]"
    ET.SubElement(metadata_record, "parent-name").text = f"[{TABLE_NAME}]"
    ET.SubElement(metadata_record, "remote-alias").text = remote_name
    ET.SubElement(metadata_record, "ordinal").text = str(ordinal)
    ET.SubElement(metadata_record, "local-type").text = datatype
    ET.SubElement(metadata_record, "aggregation").text = "Count" if datatype == "string" else "Sum"
    ET.SubElement(metadata_record, "contains-null").text = "true"

    if datatype == "string":
        ET.SubElement(metadata_record, "scale").text = "1"
        ET.SubElement(metadata_record, "width").text = "1073741823"
        ET.SubElement(metadata_record, "collation", {"flag": "0", "name": "LEN_RUS"})

    attributes = ET.SubElement(metadata_record, "attributes")
    if datatype == "string":
        ET.SubElement(attributes, "attribute", {"datatype": "string", "name": "DebugRemoteCollation"}).text = '"en_US"'
        ET.SubElement(attributes, "attribute", {"datatype": "string", "name": "DebugRemoteMetadata (compression)"}).text = '"heap"'
        ET.SubElement(attributes, "attribute", {"datatype": "integer", "name": "DebugRemoteMetadata (size)"}).text = "4294967292"
        ET.SubElement(attributes, "attribute", {"datatype": "integer", "name": "DebugRemoteMetadata (storagewidth)"}).text = "8"
        ET.SubElement(attributes, "attribute", {"datatype": "string", "name": "DebugRemoteType"}).text = '"str"'
    else:
        ET.SubElement(attributes, "attribute", {"datatype": "integer", "name": "DebugRemoteMetadata (size)"}).text = "8"
        ET.SubElement(attributes, "attribute", {"datatype": "string", "name": "DebugRemoteType"}).text = '"double"'


def add_palette_encoding(parent: ET.Element, field_name: str, mapping: dict[str, str]) -> None:
    encoding = ET.SubElement(parent, "encoding", {"attr": "color", "field": field_name, "type": "palette"})
    for bucket, color in mapping.items():
        color_map = ET.SubElement(encoding, "map", {"to": color})
        ET.SubElement(color_map, "bucket").text = f'"{bucket}"'


def build_datasource(parent: ET.Element, aliases: dict[str, str], category_palette: dict[str, str]) -> None:
    datasource = ET.SubElement(
        parent,
        "datasource",
        {
            "caption": DATASOURCE_CAPTION,
            "inline": "true",
            "name": DATASOURCE_NAME,
            "version": "18.1",
        },
    )
    connection = ET.SubElement(datasource, "connection", {"class": "federated"})
    named_connections = ET.SubElement(connection, "named-connections")
    named_connection = ET.SubElement(
        named_connections,
        "named-connection",
        {"caption": DATASOURCE_CAPTION, "name": CONNECTION_NAME},
    )
    ET.SubElement(
        named_connection,
        "connection",
        {
            "auto-extract": "yes",
            "character-set": "UTF-8",
            "class": "textscan",
            "directory": str(CSV_PATH.parent),
            "driver": "",
            "filename": CSV_PATH.name,
            "force-character-set": "no",
            "force-header": "no",
            "force-separator": "no",
            "header": "yes",
            "separator": ",",
            "text-qualifier": '"',
        },
    )

    relation = ET.SubElement(
        connection,
        "relation",
        {
            "connection": CONNECTION_NAME,
            "name": TABLE_NAME,
            "table": f"[{TABLE_NAME}]",
            "type": "table",
        },
    )
    columns = ET.SubElement(
        relation,
        "columns",
        {
            "character-set": "UTF-8",
            "header": "yes",
            "locale": "en_US",
            "separator": ",",
            "text-qualifier": '"',
        },
    )
    ET.SubElement(columns, "column", {"datatype": "string", "name": "Chart Section", "ordinal": "0"})
    ET.SubElement(columns, "column", {"datatype": "string", "name": "Category", "ordinal": "1"})
    ET.SubElement(columns, "column", {"datatype": "real", "name": "Value", "ordinal": "2"})
    ET.SubElement(connection, "refresh", {"increment-key": "", "incremental-updates": "false"})

    metadata_records = ET.SubElement(connection, "metadata-records")
    add_metadata_record(metadata_records, "Chart Section", 0, "string")
    add_metadata_record(metadata_records, "Category", 1, "string")
    add_metadata_record(metadata_records, "Value", 2, "real")

    capability = ET.SubElement(metadata_records, "metadata-record", {"class": "capability"})
    ET.SubElement(capability, "remote-name")
    ET.SubElement(capability, "remote-type").text = "0"
    ET.SubElement(capability, "parent-name").text = f"[{TABLE_NAME}]"
    ET.SubElement(capability, "remote-alias")
    ET.SubElement(capability, "aggregation").text = "Count"
    ET.SubElement(capability, "contains-null").text = "true"
    capability_attributes = ET.SubElement(capability, "attributes")
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "character-set"}).text = '"UTF-8"'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "collation"}).text = '"en_US"'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "field-delimiter"}).text = '","'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "header-row"}).text = '"true"'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "locale"}).text = '"en_US"'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "quote-char"}).text = '"\\""'
    ET.SubElement(capability_attributes, "attribute", {"datatype": "string", "name": "single-char"}).text = '""'

    ET.SubElement(datasource, "aliases", {"enabled": "yes"})
    ET.SubElement(datasource, "column", {"datatype": "string", "name": "[Chart Section]", "role": "dimension", "type": "nominal"})
    category_column = ET.SubElement(datasource, "column", {"datatype": "string", "name": "[Category]", "role": "dimension", "type": "nominal"})
    category_aliases = ET.SubElement(category_column, "aliases")
    for key, label in aliases.items():
        ET.SubElement(category_aliases, "alias", {"key": f'"{key}"', "value": label})
    ET.SubElement(datasource, "column", {"aggregation": "Sum", "datatype": "real", "name": "[Value]", "role": "measure", "type": "quantitative"})
    number_of_records = ET.SubElement(
        datasource,
        "column",
        {
            "datatype": "integer",
            "hidden": "true",
            "name": "[Number of Records]",
            "role": "measure",
            "type": "quantitative",
            qname("auto-column"): "numrec",
        },
    )
    ET.SubElement(number_of_records, "calculation", {"class": "tableau", "formula": "1"})

    ET.SubElement(datasource, "column-instance", {"column": "[Chart Section]", "derivation": "None", "name": "[none:Chart Section:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(datasource, "column-instance", {"column": "[Category]", "derivation": "None", "name": "[none:Category:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(datasource, "column-instance", {"column": "[Category]", "derivation": "Attribute", "name": "[attr:Category:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(datasource, "column-instance", {"column": "[Value]", "derivation": "Sum", "name": "[sum:Value:qk]", "pivot": "key", "type": "quantitative"})
    ET.SubElement(datasource, "column-instance", {"column": "[Number of Records]", "derivation": "Sum", "name": "[sum:Number of Records:qk]", "pivot": "key", "type": "quantitative"})

    ET.SubElement(
        datasource,
        "layout",
        {
            "dim-ordering": "alphabetic",
            "dim-percentage": "0.5",
            "measure-ordering": "alphabetic",
            "measure-percentage": "0.4",
            "show-structure": "true",
        },
    )

    style = ET.SubElement(datasource, "style")
    mark_rule = ET.SubElement(style, "style-rule", {"element": "mark"})
    add_palette_encoding(mark_rule, "[Chart Section]", SECTION_COLORS)
    add_palette_encoding(mark_rule, "[Category]", category_palette)


def add_datasource_dependencies(parent: ET.Element) -> None:
    dependencies = ET.SubElement(parent, "datasource-dependencies", {"datasource": DATASOURCE_NAME})
    ET.SubElement(dependencies, "column", {"datatype": "string", "name": "[Chart Section]", "role": "dimension", "type": "nominal"})
    ET.SubElement(dependencies, "column", {"datatype": "string", "name": "[Category]", "role": "dimension", "type": "nominal"})
    ET.SubElement(dependencies, "column", {"aggregation": "Sum", "datatype": "real", "name": "[Value]", "role": "measure", "type": "quantitative"})
    ET.SubElement(dependencies, "column-instance", {"column": "[Chart Section]", "derivation": "None", "name": "[none:Chart Section:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(dependencies, "column-instance", {"column": "[Category]", "derivation": "None", "name": "[none:Category:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(dependencies, "column-instance", {"column": "[Category]", "derivation": "Attribute", "name": "[attr:Category:nk]", "pivot": "key", "type": "nominal"})
    ET.SubElement(dependencies, "column-instance", {"column": "[Value]", "derivation": "Sum", "name": "[sum:Value:qk]", "pivot": "key", "type": "quantitative"})


def add_custom_tooltip(parent: ET.Element) -> None:
    customized_tooltip = ET.SubElement(parent, "customized-tooltip")
    formatted_text = ET.SubElement(customized_tooltip, "formatted-text")
    ET.SubElement(formatted_text, "run", {"fontcolor": "#64748B"}).text = "Category:\t"
    ET.SubElement(formatted_text, "run", {"bold": "true"}).text = f"<[{DATASOURCE_NAME}].[attr:Category:nk]>\n"
    ET.SubElement(formatted_text, "run", {"fontcolor": "#64748B"}).text = "Value:\t"
    ET.SubElement(formatted_text, "run", {"bold": "true"}).text = f"<[{DATASOURCE_NAME}].[sum:Value:qk]>"


def build_worksheet(parent: ET.Element, spec: WorksheetSpec) -> None:
    worksheet = ET.SubElement(parent, "worksheet", {"name": spec.name})

    layout_options = ET.SubElement(worksheet, "layout-options")
    title = ET.SubElement(layout_options, "title")
    formatted_text = ET.SubElement(title, "formatted-text")
    ET.SubElement(formatted_text, "run", {"bold": "true", "fontcolor": spec.title_color, "fontsize": "12"}).text = spec.name

    table = ET.SubElement(worksheet, "table")
    view = ET.SubElement(table, "view")
    datasources = ET.SubElement(view, "datasources")
    ET.SubElement(datasources, "datasource", {"caption": DATASOURCE_CAPTION, "name": DATASOURCE_NAME})
    add_datasource_dependencies(view)

    filter_element = ET.SubElement(view, "filter", {"class": "categorical", "column": f"[{DATASOURCE_NAME}].[Chart Section]"})
    ET.SubElement(
        filter_element,
        "groupfilter",
        {
            "function": "member",
            "level": "[Chart Section]",
            "member": f'"{spec.section}"',
            qname("ui-domain"): "database",
            qname("ui-enumeration"): "inclusive",
            qname("ui-marker"): "enumerate",
        },
    )

    slices = ET.SubElement(view, "slices")
    ET.SubElement(slices, "column").text = f"[{DATASOURCE_NAME}].[Category]"
    ET.SubElement(slices, "column").text = f"[{DATASOURCE_NAME}].[sum:Value:qk]"
    ET.SubElement(view, "aggregation", {"value": "true"})

    style = ET.SubElement(table, "style")
    axis_rule = ET.SubElement(style, "style-rule", {"element": "axis"})
    ET.SubElement(axis_rule, "format", {"attr": "title", "class": "0", "field": f"[{DATASOURCE_NAME}].[sum:Value:qk]", "scope": "cols", "value": spec.axis_title})
    ET.SubElement(axis_rule, "format", {"attr": "auto-subtitle", "class": "0", "field": f"[{DATASOURCE_NAME}].[sum:Value:qk]", "scope": "cols", "value": "true"})

    worksheet_rule = ET.SubElement(style, "style-rule", {"element": "worksheet"})
    ET.SubElement(worksheet_rule, "format", {"attr": "display-field-labels", "scope": "rows", "value": "false"})
    ET.SubElement(worksheet_rule, "format", {"attr": "color", "value": "#1F2937"})

    label_rule = ET.SubElement(style, "style-rule", {"element": "label"})
    ET.SubElement(label_rule, "format", {"attr": "color", "field": f"[{DATASOURCE_NAME}].[sum:Value:qk]", "value": "#1F2937"})
    ET.SubElement(label_rule, "format", {"attr": "font-size", "field": f"[{DATASOURCE_NAME}].[sum:Value:qk]", "value": "9"})

    cell_rule = ET.SubElement(style, "style-rule", {"element": "cell"})
    ET.SubElement(cell_rule, "format", {"attr": "text-format", "field": f"[{DATASOURCE_NAME}].[sum:Value:qk]", "value": spec.number_format})

    tooltip_rule = ET.SubElement(style, "style-rule", {"element": "tooltip"})
    ET.SubElement(tooltip_rule, "format", {"attr": "font-size", "value": "11"})
    ET.SubElement(tooltip_rule, "format", {"attr": "color", "value": "#334155"})

    panes = ET.SubElement(table, "panes")
    pane = ET.SubElement(panes, "pane")
    pane_view = ET.SubElement(pane, "view")
    ET.SubElement(pane_view, "breakdown", {"value": "auto"})
    ET.SubElement(pane, "mark", {"class": spec.mark_class})

    encodings = ET.SubElement(pane, "encodings")
    ET.SubElement(encodings, "color", {"column": f"[{DATASOURCE_NAME}].[{spec.color_field}]"})
    if spec.size_field:
        ET.SubElement(encodings, "size", {"column": spec.size_field})
    if spec.show_text_labels:
        ET.SubElement(encodings, "text", {"column": f"[{DATASOURCE_NAME}].[sum:Value:qk]"})
    ET.SubElement(encodings, "tooltip", {"column": f"[{DATASOURCE_NAME}].[attr:Category:nk]"})
    add_custom_tooltip(pane)

    pane_style = ET.SubElement(pane, "style")
    datalabel_rule = ET.SubElement(pane_style, "style-rule", {"element": "datalabel"})
    ET.SubElement(datalabel_rule, "format", {"attr": "font-size", "value": "9"})
    ET.SubElement(datalabel_rule, "format", {"attr": "font-family", "value": "Arial"})
    ET.SubElement(datalabel_rule, "format", {"attr": "color", "value": "#111827"})

    mark_rule = ET.SubElement(pane_style, "style-rule", {"element": "mark"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-show", "value": "true" if spec.show_text_labels else "false"})
    ET.SubElement(mark_rule, "format", {"attr": "mark-labels-cull", "value": "true"})
    ET.SubElement(mark_rule, "format", {"attr": "has-stroke", "value": "true"})
    ET.SubElement(mark_rule, "format", {"attr": "stroke-color", "value": "#E5E7EB"})
    ET.SubElement(mark_rule, "format", {"attr": "stroke-size", "value": "1"})

    ET.SubElement(table, "rows").text = spec.rows_expr
    ET.SubElement(table, "cols").text = spec.cols_expr


def add_dashboard_text_zone(parent: ET.Element, zone_id: int, x: int, y: int, w: int, h: int, runs: list[tuple[dict[str, str], str]], fixed_size: int | None = None) -> None:
    attributes = {"h": str(h), "id": str(zone_id), "type": "text", "w": str(w), "x": str(x), "y": str(y)}
    if fixed_size is not None:
        attributes["fixed-size"] = str(fixed_size)
        attributes["is-fixed"] = "true"
    zone = ET.SubElement(parent, "zone", attributes)
    formatted_text = ET.SubElement(zone, "formatted-text")
    for run_attrs, text in runs:
        ET.SubElement(formatted_text, "run", run_attrs).text = text


def build_dashboard(parent: ET.Element, kpis: list[dict[str, str]]) -> None:
    dashboard = ET.SubElement(parent, "dashboard", {"name": WORKBOOK_NAME})
    layout_options = ET.SubElement(dashboard, "layout-options")
    title = ET.SubElement(layout_options, "title")
    formatted_text = ET.SubElement(title, "formatted-text")
    ET.SubElement(formatted_text, "run", {"fontcolor": "#111827", "fontname": "Arial", "fontsize": "17"}).text = WORKBOOK_NAME

    style = ET.SubElement(dashboard, "style")
    dash_text_rule = ET.SubElement(style, "style-rule", {"element": "dash-text"})
    ET.SubElement(dash_text_rule, "format", {"attr": "wrap", "id": "dash-text_intro", "value": "on"})

    ET.SubElement(dashboard, "size", {"maxheight": "920", "maxwidth": "1280", "minheight": "920", "minwidth": "1280"})
    datasources = ET.SubElement(dashboard, "datasources")
    ET.SubElement(datasources, "datasource", {"caption": DATASOURCE_CAPTION, "name": DATASOURCE_NAME})

    zones = ET.SubElement(dashboard, "zones")
    root = ET.SubElement(zones, "zone", {"h": "100000", "id": "1", "type": "layout-basic", "w": "100000", "x": "0", "y": "0"})
    ET.SubElement(root, "zone", {"h": "5000", "id": "2", "type": "title", "w": "100000", "x": "0", "y": "0"})

    add_dashboard_text_zone(
        root,
        zone_id=3,
        x=0,
        y=5600,
        w=100000,
        h=4200,
        runs=[
            ({"fontcolor": "#475569", "fontsize": "10"}, "Restaurant performance snapshot across "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Monthly Sales"], "fontsize": "10"}, "sales"),
            ({"fontcolor": "#475569", "fontsize": "10"}, ", "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Seasonality Index"], "fontsize": "10"}, "seasonality"),
            ({"fontcolor": "#475569", "fontsize": "10"}, ", "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Festival Impact"], "fontsize": "10"}, "festival demand"),
            ({"fontcolor": "#475569", "fontsize": "10"}, ", and "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Inventory Wastage Drivers"], "fontsize": "10"}, "inventory risk"),
            ({"fontcolor": "#475569", "fontsize": "10"}, " for the 2024-01 to 2026-03 portfolio window."),
        ],
    )

    kpi_container = ET.SubElement(root, "zone", {"h": "9500", "id": "4", "param": "horz", "type": "layout-flow", "w": "100000", "x": "0", "y": "11200"})
    kpi_widths = [24500, 25500, 25000, 25000]
    kpi_x = 0
    for index, (kpi, width) in enumerate(zip(kpis, kpi_widths), start=5):
        add_dashboard_text_zone(
            kpi_container,
            zone_id=index,
            x=kpi_x,
            y=11200,
            w=width,
            h=9500,
            fixed_size=280,
            runs=[
                ({"bold": "true", "fontcolor": "#64748B", "fontsize": "10"}, f"{kpi['title']}\n"),
                ({"bold": "true", "fontcolor": kpi["accent"], "fontsize": "20"}, f"{kpi['value']}\n"),
                ({"fontcolor": "#334155", "fontsize": "9"}, kpi["subtitle"]),
            ],
        )
        kpi_x += width

    chart_zones = [
        (9, "Monthly Sales Trend", 0, 24500, 50000, 30500),
        (10, "Seasonality Wave", 50000, 24500, 50000, 30500),
        (11, "Festival Demand Lift", 0, 58500, 50000, 27000),
        (12, "Inventory Risk Bubbles", 50000, 58500, 50000, 27000),
    ]
    for zone_id, name, x, y, width, height in chart_zones:
        ET.SubElement(root, "zone", {"h": str(height), "id": str(zone_id), "name": name, "show-title": "true", "w": str(width), "x": str(x), "y": str(y)})

    add_dashboard_text_zone(
        root,
        zone_id=13,
        x=0,
        y=89500,
        w=100000,
        h=4000,
        runs=[
            ({"fontcolor": "#64748B", "fontsize": "9"}, "Chart mix: "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Monthly Sales"], "fontsize": "9"}, "trend line"),
            ({"fontcolor": "#64748B", "fontsize": "9"}, " for sales, "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Seasonality Index"], "fontsize": "9"}, "filled area"),
            ({"fontcolor": "#64748B", "fontsize": "9"}, " for seasonality, "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Festival Impact"], "fontsize": "9"}, "ranked bars"),
            ({"fontcolor": "#64748B", "fontsize": "9"}, " for demand lift, and "),
            ({"bold": "true", "fontcolor": SECTION_COLORS["Inventory Wastage Drivers"], "fontsize": "9"}, "bubble marks"),
            ({"fontcolor": "#64748B", "fontsize": "9"}, " for wastage drivers."),
        ],
    )


def add_cards(parent: ET.Element) -> None:
    cards = ET.SubElement(parent, "cards")
    left_edge = ET.SubElement(cards, "edge", {"name": "left"})
    left_strip = ET.SubElement(left_edge, "strip", {"size": "195"})
    ET.SubElement(left_strip, "card", {"type": "pages"})
    ET.SubElement(left_strip, "card", {"type": "filters"})
    ET.SubElement(left_strip, "card", {"type": "marks"})
    ET.SubElement(left_strip, "card", {"type": "color"})

    top_edge = ET.SubElement(cards, "edge", {"name": "top"})
    for card_type in ["columns", "rows", "title"]:
        strip = ET.SubElement(top_edge, "strip", {"size": "2147483647"})
        ET.SubElement(strip, "card", {"type": card_type})


def build_windows(parent: ET.Element) -> None:
    windows = ET.SubElement(parent, "windows", {"source-height": "32"})
    dashboard_window = ET.SubElement(windows, "window", {"class": "dashboard", "maximized": "true", "name": WORKBOOK_NAME})
    viewpoints = ET.SubElement(dashboard_window, "viewpoints")
    for spec in WORKSHEET_SPECS:
        ET.SubElement(viewpoints, "viewpoint", {"name": spec.name})
    ET.SubElement(dashboard_window, "active", {"id": "-1"})

    for spec in WORKSHEET_SPECS:
        worksheet_window = ET.SubElement(windows, "window", {"class": "worksheet", "name": spec.name})
        add_cards(worksheet_window)
        ET.SubElement(worksheet_window, "viewpoint")


def build_workbook(aliases: dict[str, str], category_palette: dict[str, str], kpis: list[dict[str, str]]) -> None:
    workbook = ET.Element(
        "workbook",
        {
            "locale": "en_US",
            "source-build": "2026.1.0",
            "source-platform": "mac",
            "version": "18.1",
        },
    )

    preferences = ET.SubElement(workbook, "preferences")
    ET.SubElement(preferences, "preference", {"name": "ui.encoding.shelf.height", "value": "24"})
    ET.SubElement(preferences, "preference", {"name": "ui.shelf.height", "value": "26"})
    ET.SubElement(workbook, "style-theme", {"name": "smooth"})

    datasources = ET.SubElement(workbook, "datasources")
    build_datasource(datasources, aliases, category_palette)

    worksheets = ET.SubElement(workbook, "worksheets")
    for spec in WORKSHEET_SPECS:
        build_worksheet(worksheets, spec)

    dashboards = ET.SubElement(workbook, "dashboards")
    build_dashboard(dashboards, kpis)
    build_windows(workbook)

    tree = ET.ElementTree(workbook)
    ET.indent(tree, space="  ")
    for path in WORKBOOK_PATHS:
        tree.write(path, encoding="utf-8", xml_declaration=True)


def write_guide() -> None:
    workbook_names = ", ".join(path.name for path in WORKBOOK_PATHS)
    guide = f"""# Tableau Desktop Guide

This folder contains a Tableau-ready CSV plus multiple workbook copies of the same enhanced dashboard.

## Files
- `{CSV_PATH.name}`: backing text source used by the Tableau workbook
- `{workbook_names}`: native Tableau workbooks with KPI cards, mixed chart types, and the colorful dashboard layout

## Rebuild
```bash
./.venv/bin/python src/build_tableau_workbook.py
```

## Open in Tableau Desktop
Open `{WORKBOOK_PATHS[-1].name}` for the most explicit enhanced copy, or reuse `{WORKBOOK_PATHS[0].name}` if you want to keep the original file name.
"""
    GUIDE_PATH.write_text(guide, encoding="utf-8")


def main() -> None:
    frame, aliases, category_palette, kpis = build_dashboard_assets()
    write_dashboard_csv(frame)
    build_workbook(aliases, category_palette, kpis)
    write_guide()
    print(f"Saved dashboard CSV to {CSV_PATH}")
    for path in WORKBOOK_PATHS:
        print(f"Saved Tableau workbook to {path}")
    print(f"Saved guide to {GUIDE_PATH}")


if __name__ == "__main__":
    main()
