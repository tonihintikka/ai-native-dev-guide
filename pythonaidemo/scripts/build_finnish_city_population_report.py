#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px

API_TABLE_URL = "https://pxdata.stat.fi/PXWeb/api/v1/en/StatFin/vaerak/statfin_vaerak_pxt_11ra.px"

METRICS = {
    "vaesto": "population",
    "vaesto_alle15_p": "share_under_15",
    "vaesto_yli64_p": "share_over_65",
    "vaesto_keski_ika": "avg_age",
    "vaesto_kieli_ulk_p": "share_foreign_language",
}


def _http_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    request = urllib.request.Request(url=url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _ordered_codes(dimension: dict[str, Any]) -> list[str]:
    index = dimension["category"]["index"]
    if isinstance(index, list):
        return index
    return [code for code, _ in sorted(index.items(), key=lambda item: item[1])]


def _label_lookup(dimension: dict[str, Any]) -> dict[str, str]:
    labels = dimension["category"].get("label", {})
    return {str(code): str(label) for code, label in labels.items()}


def _jsonstat_value(values: list[Any] | dict[str, Any], flat_index: int) -> Any:
    if isinstance(values, list):
        return values[flat_index] if flat_index < len(values) else None
    return values.get(str(flat_index))


def fetch_population_rows(api_table_url: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    table_meta = _http_json(api_table_url)

    query_payload = {
        "query": [
            {"code": "Alue", "selection": {"filter": "all", "values": ["*"]}},
            {"code": "Tiedot", "selection": {"filter": "item", "values": list(METRICS.keys())}},
            {"code": "Vuosi", "selection": {"filter": "all", "values": ["*"]}},
        ],
        "response": {"format": "json-stat2"},
    }
    dataset = _http_json(api_table_url, query_payload)

    area_dimension = dataset["dimension"]["Alue"]
    metric_dimension = dataset["dimension"]["Tiedot"]
    year_dimension = dataset["dimension"]["Vuosi"]

    area_codes = _ordered_codes(area_dimension)
    metric_codes = _ordered_codes(metric_dimension)
    year_values = _ordered_codes(year_dimension)

    area_labels = _label_lookup(area_dimension)
    metric_labels = _label_lookup(metric_dimension)

    area_count = len(area_codes)
    metric_count = len(metric_codes)
    year_count = len(year_values)

    values = dataset["value"]
    records: list[dict[str, Any]] = []
    for area_idx, area_code in enumerate(area_codes):
        for metric_idx, metric_code in enumerate(metric_codes):
            for year_idx, year in enumerate(year_values):
                flat_index = (area_idx * metric_count * year_count) + (metric_idx * year_count) + year_idx
                value = _jsonstat_value(values, flat_index)
                records.append(
                    {
                        "area_code": area_code,
                        "area_name": area_labels.get(area_code, area_code),
                        "metric_code": metric_code,
                        "metric_name": metric_labels.get(metric_code, metric_code),
                        "year": int(year),
                        "value": value,
                    }
                )

    expected_cells = area_count * metric_count * year_count
    meta = {
        "table_title": dataset.get("label", table_meta.get("title", "")),
        "source": dataset.get("source", "Statistics Finland"),
        "table_updated": dataset.get("updated", ""),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "api_table_url": api_table_url,
        "expected_cells": expected_cells,
    }

    return pd.DataFrame.from_records(records), meta


def transform_for_municipalities(df_long: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    municipal = df_long[df_long["area_code"].str.startswith("KU")].copy()
    municipal = municipal[municipal["metric_code"].isin(METRICS.keys())]

    wide = (
        municipal.pivot_table(
            index=["area_code", "area_name", "year"],
            columns="metric_code",
            values="value",
            aggfunc="first",
        )
        .rename(columns=METRICS)
        .reset_index()
    )

    for column in METRICS.values():
        wide[column] = pd.to_numeric(wide[column], errors="coerce")

    municipalities = (
        wide[["area_code", "area_name"]]
        .drop_duplicates()
        .sort_values("area_name")
        .reset_index(drop=True)
    )

    wide = wide.sort_values(["year", "population"], ascending=[True, False]).reset_index(drop=True)
    return municipalities, wide


def write_sqlite(db_path: Path, municipalities: pd.DataFrame, population_metrics: pd.DataFrame, source_meta: dict[str, Any]) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")

        municipalities.to_sql("municipalities", conn, if_exists="replace", index=False)
        population_metrics.to_sql("population_metrics", conn, if_exists="replace", index=False)

        conn.execute("DROP TABLE IF EXISTS source_meta;")
        conn.execute(
            """
            CREATE TABLE source_meta (
                table_title TEXT,
                source TEXT,
                table_updated TEXT,
                fetched_at TEXT,
                api_table_url TEXT,
                expected_cells INTEGER
            );
            """
        )
        conn.execute(
            """
            INSERT INTO source_meta (
                table_title, source, table_updated, fetched_at, api_table_url, expected_cells
            ) VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                source_meta["table_title"],
                source_meta["source"],
                source_meta["table_updated"],
                source_meta["fetched_at"],
                source_meta["api_table_url"],
                source_meta["expected_cells"],
            ),
        )

        conn.execute("CREATE INDEX IF NOT EXISTS idx_population_metrics_area ON population_metrics(area_code);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_population_metrics_year ON population_metrics(year);")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_municipalities_area ON municipalities(area_code);")


def _format_int(value: float) -> str:
    return f"{int(round(value)):,}"


def build_html_report(report_path: Path, df_population: pd.DataFrame) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    latest_year = int(df_population["year"].max())
    df_latest = df_population[df_population["year"] == latest_year].copy()
    df_latest = df_latest.dropna(subset=["population"])

    top_n = df_latest.nlargest(20, "population").sort_values("population")
    top_codes = df_latest.nlargest(8, "population")["area_code"].tolist()
    trend_df = df_population[df_population["area_code"].isin(top_codes)].copy()

    fig_top = px.bar(
        top_n,
        x="population",
        y="area_name",
        orientation="h",
        color="population",
        color_continuous_scale="Blues",
        text=top_n["population"].map(_format_int),
        title=f"Top 20 municipalities by population ({latest_year})",
        labels={"population": "Population", "area_name": "Municipality"},
    )
    fig_top.update_layout(
        template="plotly_white",
        height=700,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=70, b=20),
    )

    fig_trend = px.line(
        trend_df,
        x="year",
        y="population",
        color="area_name",
        title="Population trend for the 8 largest municipalities",
        labels={"year": "Year", "population": "Population", "area_name": "Municipality"},
    )
    fig_trend.update_layout(template="plotly_white", height=520, margin=dict(l=20, r=20, t=70, b=20))

    fig_demographics = px.scatter(
        df_latest,
        x="avg_age",
        y="share_over_65",
        size="population",
        color="share_foreign_language",
        hover_name="area_name",
        color_continuous_scale="Viridis",
        title="Demographics by municipality (size=population, color=foreign-language share)",
        labels={
            "avg_age": "Average age",
            "share_over_65": "Share age 65+ (%)",
            "share_foreign_language": "Foreign-language share (%)",
        },
    )
    fig_demographics.update_layout(template="plotly_white", height=520, margin=dict(l=20, r=20, t=70, b=20))

    fig_age_profile = px.scatter(
        df_latest,
        x="share_under_15",
        y="share_over_65",
        size="population",
        color="population",
        hover_name="area_name",
        color_continuous_scale="Tealgrn",
        title="Age profile: under 15% vs over 65%",
        labels={
            "share_under_15": "Share under 15 (%)",
            "share_over_65": "Share age 65+ (%)",
            "population": "Population",
        },
    )
    fig_age_profile.update_layout(template="plotly_white", height=520, margin=dict(l=20, r=20, t=70, b=20))

    chart_top = fig_top.to_html(full_html=False, include_plotlyjs="cdn", config={"displaylogo": False})
    chart_trend = fig_trend.to_html(full_html=False, include_plotlyjs=False, config={"displaylogo": False})
    chart_demo = fig_demographics.to_html(full_html=False, include_plotlyjs=False, config={"displaylogo": False})
    chart_age = fig_age_profile.to_html(full_html=False, include_plotlyjs=False, config={"displaylogo": False})

    total_population = int(round(df_latest["population"].sum()))
    median_age = float(df_latest["avg_age"].median())
    foreign_share_avg = float(df_latest["share_foreign_language"].mean())
    largest_city = df_latest.nlargest(1, "population").iloc[0]

    top_table_df = (
        df_latest.nlargest(15, "population")[
            ["area_name", "population", "avg_age", "share_foreign_language", "share_over_65"]
        ]
        .rename(
            columns={
                "area_name": "Municipality",
                "population": "Population",
                "avg_age": "Average age",
                "share_foreign_language": "Foreign-language share %",
                "share_over_65": "Age 65+ share %",
            }
        )
        .copy()
    )
    top_table_df["Population"] = top_table_df["Population"].map(_format_int)
    top_table_df["Average age"] = top_table_df["Average age"].map(lambda x: f"{x:.1f}")
    top_table_df["Foreign-language share %"] = top_table_df["Foreign-language share %"].map(lambda x: f"{x:.1f}")
    top_table_df["Age 65+ share %"] = top_table_df["Age 65+ share %"].map(lambda x: f"{x:.1f}")
    top_table_html = top_table_df.to_html(index=False, classes="table", border=0)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Finnish Municipality Population Report</title>
  <style>
    :root {{
      --bg: #f4f8fb;
      --card: #ffffff;
      --ink: #0f172a;
      --muted: #475569;
      --accent: #0f766e;
      --accent-2: #0ea5e9;
      --border: #dbe5ef;
    }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", Arial, sans-serif;
      background:
        radial-gradient(900px 300px at 90% -10%, #cffafe 0%, transparent 70%),
        radial-gradient(900px 300px at -10% -20%, #e0f2fe 0%, transparent 75%),
        var(--bg);
      color: var(--ink);
    }}
    .wrap {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}
    .hero {{
      background: linear-gradient(120deg, #0f766e 0%, #0ea5e9 100%);
      color: #fff;
      border-radius: 20px;
      padding: 28px;
      box-shadow: 0 16px 30px rgba(15, 118, 110, 0.22);
    }}
    .hero h1 {{
      margin: 0 0 8px 0;
      font-size: 2rem;
      letter-spacing: 0.2px;
    }}
    .hero p {{
      margin: 0;
      opacity: 0.95;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}
    .metric {{
      background: rgba(255, 255, 255, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.28);
      padding: 14px;
      border-radius: 14px;
      backdrop-filter: blur(6px);
    }}
    .metric h2 {{
      margin: 0;
      font-size: 1.3rem;
    }}
    .metric p {{
      margin: 4px 0 0 0;
      font-size: 0.86rem;
      opacity: 0.95;
    }}
    .card {{
      margin-top: 18px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 12px 16px;
      box-shadow: 0 7px 16px rgba(2, 6, 23, 0.06);
    }}
    .table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    .table th, .table td {{
      border-bottom: 1px solid var(--border);
      text-align: left;
      padding: 10px 8px;
    }}
    .table th {{
      background: #f8fafc;
      color: #1e293b;
      font-weight: 700;
    }}
    .footnote {{
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.86rem;
    }}
    a {{
      color: var(--accent);
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <h1>Finnish Municipality Population Analytics</h1>
      <p>Interactive report generated from Statistics Finland PXWeb table 11ra. Latest year: {latest_year}.</p>
      <div class="metrics">
        <div class="metric">
          <h2>{_format_int(total_population)}</h2>
          <p>Total population across municipalities ({latest_year})</p>
        </div>
        <div class="metric">
          <h2>{len(df_latest)}</h2>
          <p>Municipalities in dataset</p>
        </div>
        <div class="metric">
          <h2>{largest_city['area_name']}</h2>
          <p>Largest municipality ({_format_int(largest_city['population'])} inhabitants)</p>
        </div>
        <div class="metric">
          <h2>{median_age:.1f}</h2>
          <p>Median municipal average age</p>
        </div>
        <div class="metric">
          <h2>{foreign_share_avg:.1f}%</h2>
          <p>Mean foreign-language share</p>
        </div>
      </div>
    </section>
    <section class="card">{chart_top}</section>
    <section class="card">{chart_trend}</section>
    <section class="card">{chart_demo}</section>
    <section class="card">{chart_age}</section>
    <section class="card">
      <h3>Top 15 municipalities snapshot ({latest_year})</h3>
      {top_table_html}
      <p class="footnote">
        Source: Statistics Finland, population structure table 11ra via PXWeb API.
      </p>
    </section>
  </main>
</body>
</html>"""

    report_path.write_text(html, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Finnish municipality population SQLite DB and HTML analytics report.")
    parser.add_argument("--db-path", type=Path, default=Path("data/finnish_city_population.sqlite"))
    parser.add_argument("--report-path", type=Path, default=Path("output/finnish_city_population_report.html"))
    parser.add_argument("--api-table-url", default=API_TABLE_URL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    df_long, source_meta = fetch_population_rows(args.api_table_url)
    municipalities, population_metrics = transform_for_municipalities(df_long)

    write_sqlite(args.db_path, municipalities, population_metrics, source_meta)
    build_html_report(args.report_path, population_metrics)

    latest_year = int(population_metrics["year"].max())
    print(f"Municipalities: {len(municipalities)}")
    print(f"Rows in population_metrics: {len(population_metrics)}")
    print(f"Latest year: {latest_year}")
    print(f"SQLite database: {args.db_path}")
    print(f"HTML report: {args.report_path}")


if __name__ == "__main__":
    main()
