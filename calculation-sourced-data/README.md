# Calculation File - Sourced Data Extraction

## Overview
Extracts all hardcoded/sourced data from MineSpans calculation files into a single machine-readable `SourcedData` worksheet, then rewires the original calculation sheets to reference it.

## File
- `20191231_CalculationAngloAmerican_Company.xlsx` — Anglo American Coal example

## SourcedData Sheet Structure

### Metadata Columns (A-I)
| Column | Field | Description |
|--------|-------|-------------|
| A | `data_key` | Unique ID: `section::item` |
| B | `sheet` | Originating worksheet name |
| C | `orig_row` | Original row number for traceability |
| D | `section` | Section name (e.g., "Coal production - Mine Level") |
| E | `item` | Mine or metric name |
| F | `unit` | Mt, %, etc. |
| G | `anglo_share_pct` | Ownership percentage |
| H | `source_ref` | MLCCI reference IDs |
| I | `comment` | Notes from original file |

### Time-Period Columns (J onwards)
| Range | Format | Count |
|-------|--------|-------|
| J-BS | `Q1_2012` ... `Q4_2025` | 56 quarterly |
| BT-CG | `FY2012_2013` ... `FY2025_2026` | 14 fiscal year |
| CH-CT | `CY2012` ... `CY2024` | 13 calendar year |

## How It Works
- **1,661 cells** across both original sheets now contain `=SourcedData!XX` references instead of hardcoded values
- Formula-embedded literals (e.g., `=1.1514/$C$10%`) became `=SourcedData!N2/$C$10%`
- Pure hardcodes became `=SourcedData!J15` references
- All calculation formulas remain untouched

## Automation Use
To update data programmatically, write values to the SourcedData sheet's time-period columns. The original calculation sheets will automatically pick up changes through the references.

```python
from openpyxl import load_workbook
wb = load_workbook('20191231_CalculationAngloAmerican_Company.xlsx')
ws = wb['SourcedData']
# Find row by data_key, write value to appropriate time column
# Save — original sheets auto-update via references
```
