# Tableau Desktop Guide

This folder contains a Tableau-ready CSV plus multiple workbook copies of the same enhanced dashboard.

## Files
- `frittenwerk_dashboard_data.csv`: backing text source used by the Tableau workbook
- `frittenwerk_analytics_dashboard.twb, frittenwerk_analytics_dashboard_fixed.twb, frittenwerk_analytics_dashboard_enhanced.twb`: native Tableau workbooks with KPI cards, mixed chart types, and the colorful dashboard layout

## Rebuild
```bash
./.venv/bin/python src/build_tableau_workbook.py
```

## Open in Tableau Desktop
Open `frittenwerk_analytics_dashboard_enhanced.twb` for the most explicit enhanced copy, or reuse `frittenwerk_analytics_dashboard.twb` if you want to keep the original file name.
