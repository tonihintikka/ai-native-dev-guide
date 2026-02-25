# Finnish City Inhabitants Analytics

This project fetches official municipality-level population data for Finland from **Statistics Finland (StatFin) PXWeb API**, stores it in SQLite, and generates an interactive HTML analytics report with Plotly charts.

## Data source

- Primary source: Statistics Finland PXWeb API (Population structure, table `11ra`)
  - API table endpoint: `https://pxdata.stat.fi/PXWeb/api/v1/en/StatFin/vaerak/statfin_vaerak_pxt_11ra.px`
  - Dataset title: *Key figures on population by region, 1990-2024*

## What the script produces

- SQLite database: `data/finnish_city_population.sqlite`
  - `municipalities` table
  - `population_metrics` table (population, age structure, avg age, foreign-language share by municipality/year)
  - `source_meta` table
- HTML report: `output/finnish_city_population_report.html`
  - Top municipalities by population
  - Multi-year trend for largest municipalities
  - Demographic scatter charts
  - Snapshot table for latest year

## Use with venv

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/build_finnish_city_population_report.py
```

Optional custom paths:

```bash
python scripts/build_finnish_city_population_report.py \
  --db-path data/my_population.sqlite \
  --report-path output/my_report.html
```
