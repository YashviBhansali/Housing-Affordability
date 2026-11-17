# Housing Affordability Research in Singapore and Hong Kong

An interactive data analysis and machine-learning project examining how housing prices have evolved relative to median income in Singapore and Hong Kong, and whether selected economic indicators help predict year-on-year housing price growth.

> **Project status:** Research and Streamlit dashboard developed locally. Repository setup and public deployment are in progress.

## Research question

How have housing affordability trends changed in Singapore and Hong Kong since 2017, and how well can economic indicators explain or predict housing price movements in each market?

The project compares two high-cost housing markets using quarterly data from **2017 Q1 to 2025 Q4**.

## Dashboard

The project includes an interactive Streamlit dashboard with four sections:

- **Overview** — introduces the project and summarises the comparison.
- **Affordability Analysis** — explores the relationship between housing price and median-income indices.
- **Predictive Model Lab** — compares forecasting models for year-on-year housing price growth.
- **Data & Methodology** — describes the data and analytical approach.

The dashboard is designed with a dark interface and light Plotly chart panels to make the visualisations easier to read.

## Key findings

### Housing affordability index

Housing prices and median income are each rebased to 100 in 2017 Q1. The affordability indicator is the price index divided by the median-income index, multiplied by 100. A value above 100 indicates that prices have grown faster than median income relative to the base period.

| Measure | Singapore | Hong Kong |
|---|---:|---:|
| Housing price index change | +52.1% | -5.5% |
| Median income index change | +37.9% | +14.1% |
| Final affordability indicator | 110.3 | 82.9 |

On this index-based measure, Singapore became less affordable relative to 2017 Q1, while Hong Kong's indicator improved. Hong Kong's improvement reflects falling prices alongside income growth; it does **not** mean that Hong Kong became more affordable than Singapore in absolute terms.

**Important interpretation note:** This is a relative index comparison, not a measure of the proportion of household income spent on housing, and it does not capture differences between individual households, dwelling types, or financing arrangements.

### Predictive model comparison

The following results are the mean RMSE from a four-fold rolling-origin cross-validation experiment predicting year-on-year housing price growth. RMSE is measured in percentage points; lower values indicate lower prediction error.

| Model | Singapore | Hong Kong |
|---|---:|---:|
| Naive baseline | 4.26 | 9.64 |
| Ordinary Least Squares (OLS) | 3.65 | 5.35 |
| Ridge Regression (scaled) | 3.07 | 4.79 |
| Random Forest | 3.03 | 7.80 |

In this experiment, Random Forest had the lowest mean RMSE in Singapore (3.03), narrowly ahead of Ridge Regression (3.07). Ridge Regression performed best in Hong Kong (4.79). All three model approaches improved on the naive baseline on average in this experiment.

The difference between the Singapore Random Forest and Ridge results is small, and the limited number of observations means it should not be treated as evidence of a decisive advantage. Performance also varied across validation folds, particularly for Hong Kong's Random Forest model.

## Data sources

The research draws on public statistical and economic data from:

- Singapore Government data portal — [data.gov.sg](https://data.gov.sg/)
- Singapore Department of Statistics — [SingStat](https://www.singstat.gov.sg/)
- Hong Kong Government data portal — [data.gov.hk](https://data.gov.hk/)
- Hong Kong Census and Statistics Department — [C&SD](https://www.censtatd.gov.hk/)
- Hong Kong Monetary Authority — [HKMA](https://www.hkma.gov.hk/)

The precise dataset definitions, series, transformations, and source references should be documented alongside the project's data and methodology files.

## Methodology

The project combines descriptive analysis with predictive modelling:

1. Assemble quarterly housing-price and economic-indicator data for Singapore and Hong Kong.
2. Prepare and merge the country datasets.
3. Rebase housing-price and median-income indices to 100 in 2017 Q1.
4. Compare the relative growth of prices and median income.
5. Construct year-on-year housing-price growth as the predictive target.
6. Compare a naive baseline, OLS, scaled Ridge Regression, and Random Forest using rolling-origin cross-validation.
7. Evaluate models using root mean squared error (RMSE).

## Limitations

- The analysis uses approximately 36 quarterly observations per market, which is a small sample for predictive modelling.
- Model results can be sensitive to the selected time periods, features, preprocessing, and validation design.
- Economic indicators may be associated with housing-price movements without causing them.
- The index-based affordability measure does not represent the full range of household circumstances or housing costs.
- Cross-validation results are estimates of performance on the specified folds, not a guarantee of future forecasting accuracy.

## Project structure

The intended project layout is:

```text
Housing-Affordability/
├── README.md
├── requirements.txt
├── .gitignore
└── Housing Affordability/
    ├── data/
    │   ├── raw/
    │   └── clean/
    ├── figures/
    ├── notebooks/
    └── housing_affordability_dashboard/
        └── app.py
```

This layout will be updated to match the final repository contents as the project files are added.

## Run the dashboard locally

After the project files and dependency list have been added to the repository:

```bash
git clone https://github.com/YashviBhansali/Housing-Affordability.git
cd Housing-Affordability
```

Create and activate a virtual environment, install the project dependencies, then run the dashboard from its application directory. The exact commands will be finalised once the repository's dependency file and folder structure are committed.

## Tools and technologies

- Python
- pandas
- Streamlit
- Plotly
- scikit-learn

## Future work

- Publish the interactive dashboard online.
- Add reproducible setup instructions and a verified dependency file.
- Document dataset definitions and source links in detail.
- Add project screenshots and a concise portfolio case study.
- Continue testing model robustness with clearly separated validation experiments.

## Author

**Yashvi Bhansali**

This project was developed as an independent research and data-science project exploring housing affordability and predictive modelling in Singapore and Hong Kong.
