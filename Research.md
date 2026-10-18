GDP year-on-year growth rate, quarterly, [earliest]–[latest]. Source: SingStat Table Builder. Saved as singapore_gdp.csv.

Consumer Price Index (headline, all items), annual/monthly [whichever it turns out to be], [earliest]–[latest]. Source: SingStat Table Builder. Saved as singapore_cpi.csv.

Merged Singapore dataset (price_index, cpi, gdp, income, resale_volume), quarterly, 2017Q1–2025Q4. Merge method: inner join on standardized quarter column; annual income expanded via forward-repeat across quarters; CPI/GDP filtered to headline series ("All Items" / "GDP At Current Market Prices") and reshaped from wide to long. Saved as singapore_merged_draft.csv (draft — final clean pass Sunday).

Final cleaned Singapore dataset: quarterly, 2017Q1–2025Q4 (36 quarters), columns [quarter, resale_price_index, cpi, gdp, income_avg, income_median, resale_volume]. Checked for nulls (none), duplicate quarters (none), and gaps in quarter sequence (none — fully continuous). Saved as singapore_merged.csv.

HK private domestic price index (All Classes, territory-wide), quarterly, 1979Q4–2026Q2. Source: data.gov.hk (Rating and Valuation Department, Property Market Statistics). Converted quarter format from "MM-MM/YYYY" to "YYYYQ#". Saved as hongkong_price_index.csv.

HK Composite CPI (Underlying, All items), monthly pulled from C&SD web table (510-60002A), aggregated to quarterly via mean. 2015Q1–2026Q3 (2026Q3 partial — only July data available). Base period: Oct 2019–Sep 2020=100. Saved as hongkong_cpi.csv.

HK GDP, year-on-year % change (real terms, chained 2024 dollars), quarterly, 2014Q1–2026Q2. Source: C&SD web table 310-30001 ("Percentage change of GDP and selected major expenditure components in real terms"). Filtered to headline GDP row (excluding component breakdowns). Saved as hongkong_gdp.csv.

HK median monthly household income (Overall, all household sizes), quarterly, 2014Q1–2026Q2. Source: C&SD web table 130-06606 ("Median monthly household income by household size"). Note: recent quarters marked "r" (revised) in source — stripped marker during cleaning, values otherwise unchanged. Saved as hongkong_income.csv.

HK Best Lending Rate, quarterly (forward-filled from effective-date changes), 1987Q4–2026Q3. Source: HKMA API (er-ir/hkd-ir-effdates). Used as mortgage-rate proxy since HKMA's direct mortgage rate data (Residential Mortgage Survey) only provides rate-type composition shares, not rate levels. Method: took quarter-end effective rate, forward-filled across quarters with no rate change. Saved as hongkong_lending_rate.csv.

Final cleaned Hong Kong dataset: quarterly, 2015Q1–2026Q2 (46 quarters), columns [quarter, hk_price_index, hk_cpi, hk_gdp, hk_income_median, hk_lending_rate]. Checked for nulls (none), duplicate quarters (none), and gaps in quarter sequence (none — fully continuous). Merge method: inner join on standardized quarter column across five sources with differing native formats (data.gov.hk quarterly, C&SD monthly aggregated to quarterly, HKMA forward-filled from effective-date changes). Saved as hongkong_merged.csv.

## Data Quality Notes — Sanity Check (Week 4 prep)

**Date:** September 20, 2026

### Merge validation
- Singapore merged dataset: 36 rows (2017Q1–2025Q4), 7 columns, no nulls, no duplicate quarters, sorted correctly.
- Hong Kong merged dataset: originally 46 rows (2015Q1–2026Q2) — wider range than expected because
  source variables were pulled independently at different date ranges. Trimmed to 2017Q1–2025Q4
  to align with Singapore's window → 36 rows, 6 columns, no nulls post-trim.
- Both datasets confirmed clean: matching quarterly frequency, no missing quarters within range,
  plausible value ranges for all variables (price indices, CPI, income, GDP YoY, HK lending rate).

### Known anomaly: Singapore GDP YoY, 2021Q2–2022Q2
- GDP YoY growth spikes to 33.7% (2021Q2), with elevated values continuing through 2022Q2
  (27.5%, 24.4%, 24.3%, 23.3%).
- Root cause: base-effect distortion — these quarters are compared against suppressed 2020
  "Circuit Breaker" (COVID lockdown) quarters, inflating YoY % growth. Not a data entry or
  parsing error; confirmed by checking underlying dates.
- Decision: retained in dataset as-is (reflects real economic conditions). Will consider adding
  a COVID-period dummy variable at the modeling stage so regression/ML models don't misread
  this period as representative "normal" GDP behavior.

### Variable note
- Hong Kong dataset includes `hk_lending_rate` as a fifth variable (not in original four-variable
  plan of price index, CPI, GDP, income). Confirmed intentional inclusion.

  ## EDA — Time Series Visualization (Week 4)

**Date:** September 20, 2026

Plotted all merged variables for both cities, 2017Q1–2025Q4, to visually inspect trends
before cross-city comparison and modeling.

### Charts produced
1. Housing price index: Singapore (HDB resale) vs Hong Kong (private domestic) — combined chart
2. CPI: Singapore vs Hong Kong — combined chart
3. GDP YoY growth: Singapore vs Hong Kong — combined chart
4. Household income: Singapore (avg vs median) — combined chart, SG only
5. Household income: Hong Kong (median) — standalone chart
6. Resale transaction volume — Singapore only, standalone chart
7. Lending rate — Hong Kong only, standalone chart

### Observations / caveats to carry into next phase
- **Base-year mismatch (price index & CPI):** Singapore and Hong Kong indices don't start
  at the same level in 2017Q1, suggesting different base years for each source's indexing
  methodology. Absolute levels aren't directly comparable between cities — only trends/rates
  of change should be compared, or values should be re-indexed to a common base (e.g., both
  set to 100 at 2017Q1) before any cross-city ratio or regression work.
- **GDP outlier (Singapore, 2021Q2–2022Q2):** Confirmed base-effect distortion from 2020
  COVID lockdown comparisons (see earlier log entry). Visible as a sharp spike in the GDP
  chart — expected, not an error.
- **Income asymmetry:** Singapore has both average and median household income (enabling
  an inequality/skew check via the avg-median gap); Hong Kong has median only. Cross-city
  income comparison will be median-to-median; SG's avg-median gap is an SG-only analysis.
- **Currency non-comparability:** Income figures are in local currency (SGD vs HKD) and
  were kept on separate charts — no FX conversion applied yet. Decide before modeling
  whether income needs FX-normalizing or whether it's used only within-city (e.g., as a
  ratio to local price index, which sidesteps the FX issue entirely).
- **Hong Kong lending rate:** No Singapore equivalent in current dataset — remains a
  Hong Kong-only variable, standalone chart, not used in cross-city comparison.
