# Steel Financials Extractor

Extracts quarterly financial data from the McKinsey steel industry Excel database
(`Financials_from_reports_by_quarter_v3.xlsx`) and returns structured JSON.

## Files

| File | Purpose |
|---|---|
| `prompt.md` | System prompt for use in agentic workflows |
| `extractor.py` | Python implementation of the extraction logic |
| `example_queries.json` | Example batch input format |

## Usage

```bash
python extractor.py --input example_queries.json --output results.json
```

## Input format

```json
[
  {
    "company": "Nucor",
    "metrics": ["revenue", "ebitda_margin", "net_earnings", "shipments"],
    "periods": ["Q1 2022", "Q2 2022"]
  }
]
```

Supported metrics: `revenue`, `ebitda`, `ebitda_margin`, `gross_margin`, `net_earnings`, `shipments`, `capex`

## Source file

`/Users/Dawid_Lipus/Library/CloudStorage/OneDrive-McKinsey&Company/Attachments/Financials_from_reports_by_quarter_v3.xlsx`
- 113 sheets, 20+ companies, quarterly data 2007–2023
