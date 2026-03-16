"""
Steel Financials Extractor
Extracts quarterly financial data from Financials_from_reports_by_quarter_v3.xlsx
Usage: python extractor.py --input queries.json --output results.json
"""

import json
import re
import argparse
import pandas as pd

FILE_PATH = (
    "/Users/Dawid_Lipus/Library/CloudStorage/"
    "OneDrive-McKinsey&Company/Attachments/"
    "Financials_from_reports_by_quarter_v3.xlsx"
)

COMPANY_SHEET_MAP = {
    "nucor": [("NUCORbis", "2016+"), ("NUCOR", "2013-2015")],
    "sdi": [("SDInew", "2015+"), ("SDI", "older")],
    "steel dynamics": [("SDInew", "2015+"), ("SDI", "older")],
    "us steel": [("USS", "main")],
    "uss": [("USS", "main")],
    "salzgitter": [("SALn", "newer"), ("SAL", "older")],
    "arcelormittal europe": [("AMn", "current"), ("AMo2", "older"), ("AMo", "oldest")],
    "am europe": [("AMn", "current"), ("AMo2", "older")],
    "arcelormittal nafta": [("A_AMc", "current"), ("A_AMb", "older")],
    "thyssenkrupp": [("TKS", "main")],
    "tks": [("TKS", "main")],
    "voestalpine": [("05_VAbis", "newer"), ("05_VA", "older")],
    "va steel": [("05_VAbis", "newer"), ("05_VA", "older")],
    "ssab": [("SSAB", "main")],
    "gerdau": [("Gerdau new", "newer"), ("Gerdau", "older")],
    "stelco": [("Stelco", "main")],
    "algoma": [("Algoma", "main")],
    "bluescope": [("Bluescope", "main")],
    "tata steel": [("Tata", "current"), ("TATA_old", "older")],
    "tata": [("Tata", "current")],
    "jsw steel": [("JSW_Q", "quarterly"), ("JSW", "older")],
    "jsw": [("JSW_Q", "quarterly"), ("JSW", "older")],
    "sail": [("SAIL_Q", "quarterly"), ("SAIL", "older")],
    "aperam": [("APERAM", "main")],
    "acerinox": [("Acerinox", "main")],
    "outokumpu": [("OUTokumpu", "main")],
    "cmc": [("CMC", "main")],
    "metinvest": [("Metinvest", "main")],
}

METRIC_ALIASES = {
    "revenue": ["net sales", "sales", "revenu", "net sales to external customers", "revenue"],
    "ebitda": ["ebitda"],
    "ebitda_margin": ["ebitda margin", "ebitda %", "ebitda%"],
    "gross_margin": ["gross margin"],
    "net_earnings": ["net earnings attributable", "net earnings", "net income"],
    "shipments": ["shipments (net ton)", "shipments (kt)", "shipments", "steel shipments"],
    "capex": ["capex/investment", "capex"],
}


def load_workbook(path=FILE_PATH):
    return pd.read_excel(path, sheet_name=None, header=None)


def parse_period(period_str):
    """Parse 'Q1 2022' → (1, 2022)"""
    m = re.match(r"Q(\d)\s+(\d{4})", period_str.strip(), re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2))
    raise ValueError(f"Cannot parse period: {period_str}")


def build_time_axis_format_a(df):
    """
    Format A: find year-row and quarter-row, return dict {(quarter, year): col_index}
    """
    year_row = None
    quarter_row = None

    for i in range(min(10, len(df))):
        row = df.iloc[i]
        years = [v for v in row if isinstance(v, (int, float)) and not pd.isna(v) and 2000 < v < 2030]
        quarters = [v for v in row if isinstance(v, str) and re.match(r"^Q[1-4]$", v.strip())]
        if len(years) >= 1 and year_row is None:
            year_row = i
        if len(quarters) >= 2 and quarter_row is None:
            quarter_row = i

    if year_row is None or quarter_row is None:
        return {}

    time_axis = {}
    current_year = None
    for col in range(len(df.columns)):
        yr_val = df.iloc[year_row, col]
        if isinstance(yr_val, (int, float)) and not pd.isna(yr_val) and 2000 < yr_val < 2030:
            current_year = int(yr_val)
        q_val = df.iloc[quarter_row, col]
        if isinstance(q_val, str) and re.match(r"^Q[1-4]$", q_val.strip()) and current_year:
            q_num = int(q_val.strip()[1])
            time_axis[(q_num, current_year)] = col

    return time_axis


def build_time_axis_format_b(df):
    """
    Format B: row 1 has "Q1 16", "2Q 2015" style labels.
    Returns dict {(quarter, year): col_index}
    """
    time_axis = {}
    header_row = df.iloc[1]

    for col, val in enumerate(header_row):
        if not isinstance(val, str):
            continue
        # Match "Q1 16", "Q2 22", "Q3 23"
        m = re.match(r"Q(\d)\s+(\d{2})$", val.strip())
        if m:
            q = int(m.group(1))
            yr = 2000 + int(m.group(2))
            time_axis[(q, yr)] = col
            continue
        # Match "1Q 2015", "2Q 2022"
        m = re.match(r"(\d)Q\s+(\d{4})$", val.strip())
        if m:
            q = int(m.group(1))
            yr = int(m.group(2))
            time_axis[(q, yr)] = col

    return time_axis


def detect_format(df):
    """Returns 'A' or 'B'"""
    if len(df) < 2:
        return "A"
    header_row = df.iloc[1]
    format_b_count = sum(
        1 for v in header_row
        if isinstance(v, str) and (
            re.match(r"Q\d\s+\d{2}$", v.strip()) or
            re.match(r"\dQ\s+\d{4}$", v.strip())
        )
    )
    return "B" if format_b_count >= 2 else "A"


def find_metric_row(df, metric_key, fmt):
    """Find row index for a given metric. Returns (row_index, matched_label) or (None, None)"""
    aliases = METRIC_ALIASES.get(metric_key, [metric_key])
    search_cols = [2] if fmt == "B" else [0, 1]

    for i in range(len(df)):
        for col in search_cols:
            if col >= len(df.columns):
                continue
            cell = df.iloc[i, col]
            if not isinstance(cell, str):
                continue
            cell_lower = cell.lower().strip()
            for alias in aliases:
                if alias.lower() in cell_lower:
                    return i, cell.strip()

    return None, None


def extract_from_summary(df, company_name, period_str):
    """Extract EBITDA margin from SUMMARY sheet."""
    q, yr = parse_period(period_str)

    # Build time axis
    time_axis = {}
    year_row = df.iloc[3]
    quarter_row = df.iloc[4]
    current_year = None

    for col in range(len(year_row)):
        yr_val = year_row.iloc[col]
        if isinstance(yr_val, (int, float)) and not pd.isna(yr_val) and yr_val > 2000:
            current_year = int(yr_val)
        q_val = quarter_row.iloc[col]
        if isinstance(q_val, str) and re.match(r"^Q[1-4]$", q_val.strip()) and current_year:
            q_num = int(q_val.strip()[1])
            time_axis[(q_num, current_year)] = col

    col_idx = time_axis.get((q, yr))
    if col_idx is None:
        return None, "period out of range"

    # Find company row
    for i in range(5, len(df)):
        cell = df.iloc[i, 0]
        if isinstance(cell, str) and company_name.lower() in cell.lower():
            val = df.iloc[i, col_idx]
            if pd.isna(val):
                return None, "no data"
            return float(val), None

    return None, "company not found in SUMMARY"


def extract_from_company_sheet(df, metric_key, period_str):
    """Extract a metric from a company sheet (Format A or B)."""
    q, yr = parse_period(period_str)
    fmt = detect_format(df)

    time_axis = build_time_axis_format_b(df) if fmt == "B" else build_time_axis_format_a(df)
    col_idx = time_axis.get((q, yr))
    if col_idx is None:
        return None, None, "period out of range"

    row_idx, matched_label = find_metric_row(df, metric_key, fmt)
    if row_idx is None:
        return None, None, f"metric '{metric_key}' not found"

    val = df.iloc[row_idx, col_idx]
    if pd.isna(val):
        return None, matched_label, "no data"

    return val, matched_label, None


def process_queries(queries, all_sheets):
    results = []

    for query in queries:
        company = query["company"]
        metrics = query["metrics"]
        periods = query["periods"]

        company_key = company.lower().strip()
        sheet_options = COMPANY_SHEET_MAP.get(company_key)

        if sheet_options is None:
            results.append({"company": company, "error": "company_not_found"})
            continue

        # Find first available sheet
        sheet_name = None
        for s, _ in sheet_options:
            if s in all_sheets:
                sheet_name = s
                break

        if sheet_name is None:
            results.append({"company": company, "error": "sheet_not_found"})
            continue

        df = all_sheets[sheet_name]
        summary_df = all_sheets.get("SUMMARY")

        for period in periods:
            period_result = {
                "company": company,
                "sheet_used": sheet_name,
                "period": period,
                "metrics": {}
            }

            for metric in metrics:
                if metric == "ebitda_margin" and summary_df is not None:
                    val, err = extract_from_summary(summary_df, company, period)
                    if val is not None:
                        period_result["metrics"][metric] = {"value": val, "unit": "decimal"}
                    else:
                        # fallback to company sheet
                        val, label, err = extract_from_company_sheet(df, metric, period)
                        period_result["metrics"][metric] = {
                            "value": float(val) if val is not None else None,
                            "unit": "decimal",
                            "note": err
                        }
                else:
                    val, label, err = extract_from_company_sheet(df, metric, period)
                    period_result["metrics"][metric] = {
                        "value": float(val) if val is not None and not isinstance(val, str) else val,
                        "unit": "see source sheet",
                        "matched_label": label,
                        "note": err
                    }

            results.append(period_result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Extract steel financials from Excel")
    parser.add_argument("--input", required=True, help="Path to JSON file with queries")
    parser.add_argument("--output", required=True, help="Path to write results JSON")
    parser.add_argument("--file", default=FILE_PATH, help="Path to the Excel file")
    args = parser.parse_args()

    print(f"Loading workbook from: {args.file}")
    all_sheets = load_workbook(args.file)
    print(f"Loaded {len(all_sheets)} sheets")

    with open(args.input) as f:
        queries = json.load(f)

    print(f"Processing {len(queries)} queries...")
    results = process_queries(queries, all_sheets)

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
