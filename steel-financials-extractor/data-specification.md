# Steel Financials — Data Specification for Collection Agent

## Purpose

This document specifies the exact data to be collected quarterly from public company filings to populate the McKinsey steel industry financial database (`Financials_from_reports_by_quarter_v3.xlsx`).

---

## Companies (21 total)

### North America (7)
| Company | Ticker/ID | Reporting Currency | Typical Source |
|---|---|---|---|
| Nucor | NUE | USD (thousands) | 10-Q / Earnings release |
| Steel Dynamics (SDI) | STLD | USD (thousands) | 10-Q / Earnings release |
| US Steel | X | USD (millions) | 10-Q / Supplemental data |
| Gerdau (North America segment) | GGB | BRL → USD | 6-K / Earnings release |
| Stelco | STLC (TSX) | CAD (millions) | Quarterly report |
| Algoma Steel | ASTL | CAD (millions) | Quarterly report |
| CMC (Commercial Metals) | CMC | USD (millions) | 10-Q / Earnings release |

### Europe (8)
| Company | Ticker/ID | Reporting Currency | Typical Source |
|---|---|---|---|
| Salzgitter (Strip steel) | SZG (XETRA) | EUR (millions) | Quarterly report |
| ArcelorMittal (Europe segment) | MT | USD (millions) | 6-K / Earnings release |
| ThyssenKrupp Steel (TKS) | TKA (XETRA) | EUR (millions) | Quarterly report |
| voestalpine (Steel Division) | VOE (VIE) | EUR (millions) | Quarterly report |
| SSAB | SSAB (OMX) | SEK (millions) | Quarterly report |
| APERAM | APAM (AMS) | EUR (millions) | Earnings release |
| Acerinox | ACX (BME) | EUR (millions) | Quarterly report |
| Outokumpu | OUT1V (HEL) | EUR (millions) | Quarterly report |

### Asia / Other (6)
| Company | Ticker/ID | Reporting Currency | Typical Source |
|---|---|---|---|
| Tata Steel (Consolidated + India standalone + Europe) | TATASTEEL (NSE) | INR (crores) | Quarterly report |
| JSW Steel | JSWSTEEL (NSE) | INR (crores) | Quarterly report |
| SAIL | SAIL (NSE) | INR (crores) | Quarterly report |
| Bluescope Steel | BSL (ASX) | AUD (millions) | Half-year / Annual only |
| Metinvest | — (private) | USD (millions) | Annual report / Press release |
| RINL / Vizag Steel | — (state-owned) | INR (crores) | Annual only |

---

## Metrics to Collect

### Core metrics (required for every company & quarter)

| # | Metric | Aliases in DB | Unit | Notes |
|---|---|---|---|---|
| 1 | **Revenue / Net Sales** | `Net sales`, `Sales`, `Revenue`, `Total revenue from operations`, `Net Sales to External Customers` | Currency | Total quarterly net sales. For multi-segment companies, collect **both** consolidated and segment-level |
| 2 | **COGS** | `COGS`, `Cost of goods sold`, `RM cost` | Currency | Cost of goods sold |
| 3 | **Gross Margin** | `Gross margin`, `Gross Profit` | Currency | Revenue minus COGS |
| 4 | **EBITDA** | `EBITDA`, `Adj. EBITDA`, `EBITDA Adjusted`, `Reported EBITDA` | Currency | Prefer reported EBITDA; note if adjusted |
| 5 | **EBITDA Margin** | (calculated) | Decimal (e.g. 0.082 = 8.2%) | EBITDA ÷ Revenue. Calculate if not directly stated |
| 6 | **EBIT / Operating Income** | `EBIT`, `Operating Income`, `Operating profit EBIT`, `Income (loss) from oper.` | Currency | |
| 7 | **Net Earnings** | `Net earnings`, `Net income`, `Net earinings` [sic] | Currency | Attributable to shareholders |
| 8 | **Depreciation & Amortization** | `Depreciation`, `Depreciation and amortisation` | Currency | Needed for EBITDA reconstruction |
| 9 | **Steel Shipments** | `Shipments`, `Shipments (net ton)`, `Shipments (Mtons)`, `Deliveries`, `Sales volumes shipments` | Volume (kt or Mtons) | Net tons (US) or metric tons (EU/Asia). Always specify unit |
| 10 | **Average Selling Price** | `Average Price per net ton`, `Selling price (EUR/t)`, `Average steel price` | Currency/ton | Revenue ÷ Shipments if not directly reported |
| 11 | **CAPEX** | `CAPEX`, `Capital Expenditures`, `Capex` | Currency | Quarterly where available; annual for EU companies |

### Extended metrics (collect when available)

| # | Metric | Notes |
|---|---|---|
| 12 | **Raw Steel Production** | Production volume (vs. shipment volume) |
| 13 | **Capacity Utilization** | As decimal or percentage |
| 14 | **Interest Expense** | Net interest expense |
| 15 | **Income Tax** | Provision for income taxes |
| 16 | **Employee Costs** | Employee benefits expenses |
| 17 | **Inventory Changes** | Change in inventories |
| 18 | **Operating Cash Flow (OCF)** | |
| 19 | **Free Cash Flow (FCF)** | |
| 20 | **Headcount** | Number of employees |

---

## Segment Breakdown (where applicable)

Some companies report by business segment. Collect segment-level data when available:

| Company | Segments in DB |
|---|---|
| US Steel | `Europe flat rolled`, `US flat rolled`, `US minimill Big River` |
| SSAB | `SSAB Special Steels`, `SSAB Europe`, `SSAB Americas`, `Tibnor`, `Ruuki construction` |
| Tata Steel | `Consolidated`, `TATA Steel stand alone` (India), `TATA Steel Europe` |
| Bluescope | `Australian Steel Products`, `Buildings & Coated Products North America`, `New Zealand and Pacific Steel Products`, `Coated Products Asia` |
| Nucor | `Steel mills`, `Steel products`, `Metals Recycling` (from newer filings) |
| SDI | `Steel`, `Metals Recycling`, `Fabrication` |
| APERAM | `Stainless and Electrical Steel (S&E)`, `Recycling & Renewables` |
| ArcelorMittal | `Europe`, `NAFTA`, `Brazil BD`, `South America BD`, `North America BD` |

For each segment, collect: Revenue, EBITDA, Shipments, and Average Price where reported.

---

## Time Format

- **Granularity:** Quarterly (Q1, Q2, Q3, Q4)
- **Period format:** `Q1 2024`, `Q2 2024`, etc.
- **Indian fiscal year:** Tata/JSW/SAIL use April–March FY. Map to calendar quarters:
  - Q1 FY25 (Apr–Jun 2024) → Q2 2024
  - Q2 FY25 (Jul–Sep 2024) → Q3 2024
  - Q3 FY25 (Oct–Dec 2024) → Q4 2024
  - Q4 FY25 (Jan–Mar 2025) → Q1 2025
- **Historical range in DB:** 2006–2023 (varies by company)
- **Target:** Collect from Q1 2024 onwards (continuing quarterly)

---

## Units & Conventions

| Convention | Rule |
|---|---|
| **Currency values** | Record in the company's reporting currency. Always specify unit (thousands, millions, crores) |
| **Margins** | Store as decimal (0.082 not 8.2%) |
| **Volumes** | ktonnes or Mtons. Always specify net tons vs metric tons |
| **Nulls** | If a metric is not reported for a quarter, return `null` — never estimate |
| **Adjusted vs Reported** | Prefer reported/GAAP. If only adjusted available, flag with `"adjusted": true` |
| **Exchange rates** | Do NOT convert currencies. Store in original reporting currency. The DB has a separate `Exchange rates` / `Xrate Q` sheet |
| **Footnotes** | Capture material footnotes (e.g. LIFO adjustments, impairments, one-time charges) as metadata |

---

## Data Quality Rules

1. **Quarterly only** — never derive a quarter by subtracting from annual/H1 totals
2. **Source required** — every data point must have a traceable source (URL, filing reference)
3. **Raw text** — include the exact sentence or table cell the value came from
4. **No estimation** — if data is not explicitly stated, return null
5. **Consistency check** — EBITDA margin should approximately equal EBITDA ÷ Revenue
6. **Segment sum check** — segment revenues should approximately sum to consolidated revenue

---

## Output Schema

```json
{
  "company": "Nucor",
  "period": "Q4 2024",
  "reporting_currency": "USD",
  "unit_scale": "thousands",
  "source": {
    "type": "earnings press release",
    "url": "https://...",
    "filing_date": "2025-01-28",
    "raw_document": "Q4 2024 Earnings Release"
  },
  "consolidated": {
    "revenue": {"value": 7827000, "raw_text": "Net sales of $7.83 billion"},
    "cogs": {"value": null, "note": "not separately reported"},
    "gross_margin": {"value": null},
    "ebitda": {"value": 1150000, "raw_text": "EBITDA of $1.15 billion"},
    "ebitda_margin": {"value": 0.147, "calculated": true},
    "ebit": {"value": 812000},
    "net_earnings": {"value": 567000, "raw_text": "Net earnings of $567 million"},
    "depreciation": {"value": 338000},
    "shipments": {"value": 6200, "unit": "net tons (thousands)"},
    "avg_selling_price": {"value": 1263, "unit": "USD/net ton", "calculated": true},
    "capex": {"value": 520000}
  },
  "segments": [
    {
      "name": "Steel mills",
      "revenue": {"value": 5200000},
      "ebitda": {"value": 850000},
      "shipments": {"value": 5100, "unit": "net tons (thousands)"}
    }
  ],
  "notes": ["Q4 includes $45M LIFO charge"],
  "extended": {
    "raw_steel_production": null,
    "capacity_utilization": null,
    "employees": 31400
  }
}
```

---

## Priority Order

When collecting data, prioritize in this order:
1. **Tier 1 (always):** Revenue, EBITDA, EBITDA margin, Shipments, Net earnings
2. **Tier 2 (important):** COGS, EBIT, D&A, CAPEX, Average selling price
3. **Tier 3 (when available):** Production, utilization, OCF/FCF, headcount, interest, tax
