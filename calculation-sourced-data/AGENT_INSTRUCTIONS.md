# Agent Instructions: Coal Mine Calculation Data Sourcing

## Objective

Given a company name (e.g., "Anglo American") and a list of its coal mines, find and extract the data needed to populate the `SourcedData` worksheet. The calculation worksheets derive all results from this sourced data — no other inputs are needed.

---

## Data Categories to Source

There are **6 data categories**, each with a distinct source type and extraction method.

### 1. Quarterly Saleable Production (attributable)

- **What**: Saleable coal production per mine per quarter, on an **attributable basis** (= Anglo's ownership share × 100% production)
- **Unit**: Mt (million tonnes)
- **Granularity**: Per mine, per quarter (Q1–Q4), per year (2012–2025)
- **Mines**: Callide, Capcoal, Dawson, Drayton, Foxleigh, Jellinbah Group, Moranbah North, Grosvenor
- **Also needed**: Thermal Export and Thermal Domestic subtotals (not per-mine — these are aggregate)

#### Where to find
- **Primary**: Company quarterly production reports (published on investor relations page)
  - Anglo American: "Production Report" released ~2 weeks after each quarter end
  - URL pattern: `anglo-american.com/investors/results-and-reports`
- **Secondary**: ASX/LSE regulatory filings, annual reports (production tables)
- **Identifier pattern**: Values appear in tables titled "Production summary", "Coal — Australia" or "Metallurgical Coal"

#### How to extract
1. Download the quarterly production report PDF for the target quarter
2. Find the table for "Coal" or "Metallurgical Coal" operations
3. For each mine, extract the "Saleable production" row in the "Attributable" column
4. Values are typically reported in Mt to 1-3 decimal places
5. **Watch for**: Rounding differences (report may show 1.2 Mt, model needs 1.1514 Mt — prefer the more precise figure if available in supplementary data)

#### Validation
- Each mine should produce 0.5–5.0 Mt/quarter typically
- Total across mines: ~10–25 Mt/quarter
- Compare against prior quarter (±30% is normal, >50% change needs flagging)

---

### 2. Anglo's Ownership Share (%)

- **What**: Anglo American's equity interest in each mine, by quarter
- **Unit**: % (e.g., 51, 70, 88, 100)
- **Granularity**: Per mine, per quarter (changes infrequently — often stable for years, but can change on divestment/acquisition)
- **Mines**: Aquila, Callide, Dawson, Drayton, Foxleigh, Grasstree, Grosvenor, Jellinbah East, Lake Lindsay, Lake Vermont, Moranbah North

#### Where to find
- **Primary**: Annual report → "Operations at a glance" or "Principal subsidiaries and associates" table
- **Secondary**: Quarterly production report footnotes (ownership changes noted)
- **Also**: Company announcements for M&A transactions changing ownership

#### How to extract
1. In the annual report, find the table listing mines with ownership percentages
2. Check quarterly report footnotes for any mid-year changes
3. If a mine is 100% owned, it's often not explicitly listed — assume 100% unless stated otherwise
4. For JV mines (Jellinbah, Foxleigh), track the specific % — these change on partner transactions

#### Validation
- Values must be 0–100%
- Cross-check: attributable production ÷ ownership% should equal 100% production reported elsewhere
- Flag any quarter-over-quarter change >0% — these should correspond to announced transactions

---

### 3. ROM (Run-of-Mine) Production

- **What**: Total raw coal extracted from each mine before washing/processing
- **Unit**: Mt (million tonnes)
- **Granularity**: Per mine, **fiscal year** (Anglo's FY = Jan–Dec for coal; some older years July–June)
- **Mines**: Dawson, Moranbah North, Foxleigh, Callide & Boundary Hill, German Creek East, German Creek – Lake Lindsay, German Creek – Aquila, German Creek – Grasstree, Jellinbah East, Lake Vermont, Grosvenor

#### Where to find
- **Primary**: Annual report → "Ore Reserves and Mineral Resources" section, or operational review tables
- **Secondary**: Sustainability reports (often include ROM for emissions intensity calculations)
- **Also**: JORC/NI 43-101 technical reports for specific mines

#### How to extract
1. ROM is sometimes labelled "Total material mined", "Run of mine", or "Raw coal produced"
2. Check both the operational review AND the reserves section — ROM appears in different contexts
3. Some mines report in tonnes (not Mt) — convert: `Mt = tonnes / 1,000,000`
4. German Creek complex mines may be reported individually or as "Capcoal" aggregate — if aggregate, need the production split (see category 6)

#### Calendarisation note
The calculation model converts FY to CY using: `CY = FY_prev × 0.5 + FY_current × 0.5`. The agent only needs to provide FY values; the formula handles conversion.

#### Validation
- ROM > Saleable production (always — mass recovery is typically 60-85%)
- Typical range: 2–15 Mt/year per mine
- Mass recovery = Saleable / ROM should be 55–90%

---

### 4. Emissions (Scope 1)

- **What**: Greenhouse gas emissions (Scope 1 direct) per mine
- **Unit**: t CO2 eq. (tonnes of CO2 equivalent)
- **Granularity**: Per mine, **fiscal year**
- **Mines**: Capcoal, Dawson, Grosvenor, Moranbah North, Jellinbah, Lake Vermont

#### Where to find
- **Primary**: Sustainability report / ESG report → "Climate" or "Emissions" chapter
  - Anglo American publishes annual sustainability reports with mine-level GHG data
- **Secondary**: CDP (Carbon Disclosure Project) submissions
- **Also**: NGER (National Greenhouse and Energy Reporting) data for Australian mines (publicly available from Clean Energy Regulator)

#### How to extract
1. Find the emissions table broken down by operation
2. Extract Scope 1 (direct) emissions — NOT Scope 2 or Scope 3
3. Values are typically in t CO2-e (tonnes)
4. **GWP conversion**: Older reports may use GWP of 25 for methane; newer reports use 28. The model applies: `(old_value / 25) × 28` for Grosvenor and Moranbah North. Check which GWP the source uses.
5. Underground mines (Grosvenor, Moranbah North) have significantly higher emissions due to fugitive methane

#### Calendarisation note
The model calendarises emissions using quarterly production weighting: `CY_emissions = FY_prev × (Q3+Q4_prod/annual_prod) + FY_current × (Q1+Q2_prod/annual_prod)`. Agent provides FY values only.

#### Validation
- Underground mines: 500,000–5,000,000 t CO2-e/year
- Open cut mines: 50,000–500,000 t CO2-e/year
- Emissions intensity: 0.01–0.15 t CO2-e per tonne ROM

---

### 5. Pricing

- **What**: Two price series:
  - **Realised prices**: Average selling price achieved by Anglo American for PHCC (premium hard coking coal) and PCI (pulverised coal injection)
  - **Reference prices**: MineSpans benchmark prices for the same products
- **Unit**: USD/mt
- **Granularity**: Calendar year (2015–2024)

#### Where to find
- **Realised prices**: Annual report → "Financial review" or "Revenue" section, often in a table "Average realised prices"
- **Reference prices (MineSpans)**: Internal MineSpans database. If unavailable, use:
  - Platts Premium Low Vol HCC (TSI) as PHCC proxy
  - Platts PCI CFR China as PCI proxy

#### How to extract
1. Realised prices: Look for "Average realised price" table in the annual report, coal section
2. Prices are USD/mt (sometimes shown as US$/t or $/t — same thing)
3. May need to convert from other currencies if reported in ZAR or AUD

#### Validation
- PHCC: typically $100–$400/mt (volatile, was $500+ in 2022)
- PCI: typically $80–$250/mt
- Price differential (realised/reference) should be 0.7–1.1 (±30% of benchmark)

---

### 6. Product Splits & Supplementary Data

- **What**: Various percentage splits and supplementary production data:
  - Jellinbah washing share (% of raw coal that goes through wash plant vs bypass)
  - PCI share in Jellinbah East washing stream
  - Lake Vermont product split (HCC/PCI/Thermal %)
  - Lake Lindsay product split (HCC/PCI/Thermal volumes in Mt)
  - Total Jellinbah East resources (Mt)
- **Unit**: % or Mt
- **Granularity**: Calendar year

#### Where to find
- **Primary**: Internal mine operating data / mine planning documents
- **Secondary**: JORC resource statements (for total resources)
- **If unavailable**: Some splits can be inferred:
  - Washing share: stable at ~60-80% for most years
  - PCI share: typically 30–50% of washed product
  - Product splits: check if quarterly production reports break out by product type

#### Validation
- All percentage splits must sum to 100% across categories
- Product volumes must reconcile: HCC + PCI + Thermal = Total saleable

---

### 7. Employee Headcount

- **What**: Number of employees per mine per quarter
- **Unit**: Headcount (integer)
- **Granularity**: Per mine, per quarter (Q1 2012 – Q4 2024)
- **Mines**: Dawson, Jellinbah East, Jellinbah Plains, Lake Vermont, Grasstree, Grosvenor, Moranbah North, Aquila, Capcoal Surface
- **Also**: Permanent vs Contractor split for Jellinbah East and Lake Vermont (annual, ~2020)

#### Where to find
- **Primary**: Annual report → "Our people" or "Workforce" section
- **Secondary**: Sustainability report → social/workforce metrics
- **Also**: State mining authority workforce statistics (QLD Mines Inspectorate publishes census data)
- **Note**: Quarterly granularity may only be available from internal HR systems or mine-site reports

#### How to extract
1. Annual reports typically give year-end headcount, not quarterly
2. For quarterly estimates, check if the sustainability report provides quarterly averages
3. Permanent vs Contractor split: look in the workforce section or safety report (contractors are tracked separately for safety metrics)

#### Validation
- Range: 200–2,000 employees per mine
- Large mines (Dawson, Lake Vermont): 800–2,000
- Smaller/UG mines: 200–900
- Contractor share: typically 30–60%

---

## Extraction Workflow

For each company + mine combination:

```
1. IDENTIFY which years need data (check SourcedData for gaps)
2. LOCATE the source documents:
   a. Annual reports (production, ownership, prices, employees)
   b. Quarterly production reports (quarterly production data)
   c. Sustainability reports (emissions, workforce)
   d. MineSpans database (reference prices, internal data)
3. EXTRACT values into a staging format:
   {
     "company": "Anglo American",
     "mine": "Dawson",
     "data_key": "Coal production - Mine Level::Dawson",
     "period": "Q1_2018",
     "value": 2.3456,
     "unit": "Mt",
     "source_document": "Anglo American Q1 2018 Production Report",
     "source_page": 4,
     "source_table": "Coal Australia - Metallurgical Coal",
     "confidence": "high",  // high | medium | low
     "notes": ""
   }
4. VALIDATE each value against expected ranges (see per-category validation above)
5. CROSS-CHECK: attributable × (1/ownership%) should match 100% figures
6. WRITE to SourcedData sheet at the correct row (match data_key) and column (match period)
```

## Source Document Priority

When multiple sources have the same datapoint:

1. **Quarterly production report** (most timely, highest precision for production)
2. **Annual report** (audited, most reliable for financial and ownership data)
3. **Sustainability report** (best for emissions and workforce)
4. **MineSpans internal database** (reference prices, product splits)
5. **Regulatory filings** (NGER for emissions, JORC for resources)

## Error Handling

- **Missing data**: Leave cell blank, add note in `comment` column: `"No data found for [period] in [sources checked]"`
- **Conflicting sources**: Use the audited/primary source, note the discrepancy
- **Unit mismatch**: Always convert to the target unit (Mt, %, t CO2 eq., USD/mt, headcount)
- **Fiscal vs Calendar year**: Store FY values in FY columns. The calculation formulas handle calendarisation.

## Output Format

Write directly to the `SourcedData` worksheet:
- Match row by `data_key` column (A)
- Match column by period header (row 1)
- Values only — no formulas
- Update `source_ref` column (H) with document identifier
