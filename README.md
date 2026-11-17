# Housing Affordability Research in Singapore and Hong Kong

An independent data analysis and machine-learning project examining how housing prices have evolved relative to median income in Singapore and Hong Kong, and whether selected economic indicators help predict year-on-year housing price growth.

**Project status:** Research complete; interactive Streamlit dashboard deployed.

## Live dashboard

[Open the Housing Affordability Dashboard](https://housing-affordability-27j4jzsrtskaqvfn4otn8t.streamlit.app/)

The dashboard contains four sections:
- **Overview** — project context and headline findings.
- **Affordability Analysis** — housing-price and median-income index trends.
- **Predictive Model Lab** — comparison of predictive models and validation results.
- **Data & Methodology** — data context and analytical approach.

## Research question

How have housing affordability trends changed in Singapore and Hong Kong since 2017, and how well can economic indicators help predict housing-price movements in each market?

The project uses quarterly data from **2017 Q1 to 2025 Q4**.

## Key findings

### Relative affordability

Housing-price and median-income indices are each rebased to 100 in 2017 Q1. The relative affordability indicator is the price index divided by the median-income index, multiplied by 100. A value above 100 indicates that prices have grown faster than median income relative to the base period.

| Measure | Singapore | Hong Kong |
|---|---:|---:|
| Housing-price index change | +52.1% | -5.5% |
| Median-income index change | +37.9% | +14.1% |
| Final relative affordability indicator | 110.3 | 82.9 |

On this index-based measure, Singapore became less affordable relative to 2017 Q1, while Hong Kong's indicator improved. Hong Kong's improvement reflects falling prices alongside income growth; it does **not** mean Hong Kong became more affordable than Singapore in absolute terms.

This is a relative index comparison, not a measure of the proportion of household income spent on housing. It does not capture differences between individual households, dwelling types, or financing arrangements.

### Predictive model comparison

Mean RMSE from the main four-fold rolling-origin cross-validation experiment predicting year-on-year housing-price growth. RMSE is measured in percentage points; lower values indicate lower prediction error.

| Model | Singapore | Hong Kong |
|---|---:|---:|
| Naive baseline | 4.26 | 9.64 |
| Ordinary Least Squares (OLS) | 3.65 | 5.35 |
| Ridge Regression (scaled) | 3.07 | 4.79 |
| Random Forest | 3.03 | 7.80 |

Random Forest recorded the lowest mean RMSE in Singapore (3.03), narrowly ahead of Ridge Regression (3.07). Ridge Regression performed best in Hong Kong (4.79). All three model approaches improved on the naive baseline on average in this experiment.

The difference between the leading Singapore models is only 0.04 percentage points and should not be treated as evidence of a decisive advantage. Results also varied across validation folds.

**Validation note:** The dashboard may also show a separate five-fold experiment. Its results are presented separately because the validation designs differ. The four-fold and five-fold scores should not be combined or treated as directly interchangeable.

## Data sources

The analysis draws on public statistical and economic data from:
- [data.gov.sg](https://data.gov.sg/)
- [Singapore Department of Statistics (SingStat)](https://www.singstat.gov.sg/)
- [data.gov.hk](https://data.gov.hk/)
- [Hong Kong Census and Statistics Department (C&SD)](https://www.censtatd.gov.hk/)
- [Hong Kong Monetary Authority (HKMA)](https://www.hkma.gov.hk/)

Raw and cleaned datasets are stored in `Data/Raw/` and `Data/Clean/`. Dataset definitions, transformations, and analytical decisions should be checked alongside the notebooks and research notes.

## Methodology

1. Assemble quarterly housing-price and economic-indicator data for both markets.
2. Prepare and merge the country datasets.
3. Rebase housing-price and median-income indices to 100 in 2017 Q1.
4. Compare the relative growth of prices and median income.
5. Use year-on-year housing-price growth as the predictive target.
6. Compare a naive baseline, OLS, scaled Ridge Regression, and Random Forest using rolling-origin cross-validation.
7. Evaluate predictive performance using root mean squared error (RMSE).

## Repository structure

```text
Housing-Affordability/
├── Data/
│   ├── Raw/
│   └── Clean/
├── Figures/
├── housing_affordability_dashboard/
│   ├── app.py
│   └── requirements.txt
├── eda.ipynb
├── final_analysis.ipynb
├── hk_raw&clean.ipynb
├── sg_raw&clean.ipynb
├── prep.py
├── Research.md
├── PORTFOLIO_CASE_STUDY.md
└── README.md
```

## Run locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r housing_affordability_dashboard/requirements.txt
streamlit run housing_affordability_dashboard/app.py
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Tools and technologies

Python · pandas · NumPy · scikit-learn · Streamlit · Plotly · Jupyter Notebook · GitHub

## Limitations and interpretation

- Each market has approximately 36 quarterly observations, a small sample for predictive modelling.
- The underlying housing-price indicators differ in market coverage and methodology between Singapore and Hong Kong. The comparison is therefore most informative as an examination of relative trends within each market, rather than a direct comparison of absolute housing affordability.
- Results can be sensitive to the selected features, preprocessing, time windows, and validation design.
- The four-fold and five-fold experiments use different validation designs and should be interpreted separately.
- Economic indicators may be associated with housing-price movements without causing them.
- The index-based affordability measure does not represent the full range of household circumstances or housing costs.
- Cross-validation results describe performance on selected historical folds; they do not guarantee future forecasting accuracy or prove that a model will generalise to unseen periods.

## Portfolio documentation

See [PORTFOLIO_CASE_STUDY.md](PORTFOLIO_CASE_STUDY.md) for a concise project case study, including the research question, methods, findings, limitations, and skills developed.

## Author

**Yashvi Bhansali**

This project was developed as an independent research and data-science project exploring housing affordability and predictive modelling in Singapore and Hong Kong.
