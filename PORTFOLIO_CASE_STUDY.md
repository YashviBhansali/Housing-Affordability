# Housing Affordability in Singapore and Hong Kong

## Project overview

This independent research and data-science project examines how housing prices have changed relative to median income in Singapore and Hong Kong, and tests whether selected economic indicators can help predict year-on-year housing-price growth.

The analysis covers quarterly observations from **2017 Q1 to 2025 Q4** (36 observations per market). The work combines public economic data, descriptive analysis, predictive modelling, and an interactive Streamlit dashboard.

## Research question

How have housing affordability trends changed in Singapore and Hong Kong since 2017, and how well can economic indicators predict housing-price growth in each market?

## Data

The project uses public data from:

- data.gov.sg and the Singapore Department of Statistics (SingStat)
- data.gov.hk and the Hong Kong Census and Statistics Department (C&SD)
- Hong Kong Monetary Authority (HKMA)

The cleaned country datasets are stored in `Data/Clean/`. The dashboard reads these files directly.

## Method

1. Prepared quarterly datasets for both markets over the common 2017Q1–2025Q4 period.
2. Rebased housing-price and median-income series to 100 in 2017Q1.
3. Calculated a relative affordability indicator: price index divided by median-income index, multiplied by 100.
4. Used year-on-year housing-price growth as the predictive modelling target.
5. Compared a naive baseline, Ordinary Least Squares (OLS), scaled Ridge Regression, and Random Forest.
6. Evaluated the models using four-fold rolling-origin cross-validation and RMSE, measured in percentage points.

## Findings

### Relative affordability

| Measure | Singapore | Hong Kong |
|---|---:|---:|
| Housing-price change | +52.1% | -5.5% |
| Median-income change | +37.9% | +14.1% |
| Final relative affordability indicator | 110.3 | 82.9 |

The indicator suggests that housing prices outpaced median-income growth in Singapore relative to the 2017Q1 base. Hong Kong's indicator improved over the period because prices declined while median income increased.

This is a comparison of relative index movements. It is not an absolute ranking of affordability between the two cities, nor does it measure the share of an individual household's income spent on housing.

### Predictive modelling

Four-fold rolling-origin cross-validation results (RMSE in percentage points; lower is better):

| Model | Singapore | Hong Kong |
|---|---:|---:|
| Naive baseline | 4.26 | 9.64 |
| OLS | 3.65 | 5.35 |
| Ridge (scaled) | 3.07 | 4.79 |
| Random Forest | 3.03 | 7.80 |

Random Forest recorded the lowest mean RMSE in Singapore at 3.03, narrowly ahead of Ridge at 3.07. Ridge performed best in Hong Kong at 4.79. All three model approaches improved on the naive baseline on average in this experiment.

The 0.04 percentage-point difference between the two leading Singapore models is very small and should not be interpreted as a decisive performance advantage. Results also varied across validation folds.

## Interactive dashboard

The Streamlit dashboard presents the work in four sections:

- **Overview:** research context and headline findings.
- **Affordability Analysis:** price, income, and relative affordability trends.
- **Predictive Model Lab:** model comparisons and validation results.
- **Data & Methodology:** dataset context and analytical choices.

The application is built with Streamlit and Plotly, using pandas and NumPy for data handling and scikit-learn for modelling.

## Limitations and interpretation

- Each market has only 36 quarterly observations, which limits the reliability and generalisability of predictive models.
- Model performance can vary with the selected features, preprocessing, training windows, and validation design.
- Economic indicators that move alongside housing prices are not necessarily causal drivers.
- The relative index measure does not account for housing quality, household composition, mortgage terms, taxes, transaction costs, or differences across property segments.
- Cross-validation RMSE describes performance on the selected historical folds; it does not guarantee future forecasting accuracy.

## Tools

Python · pandas · NumPy · scikit-learn · Streamlit · Plotly · GitHub

## What I developed

This project involved collecting and preparing public datasets, constructing comparable indicators across two markets, implementing and evaluating predictive models, and translating the analysis into an interactive dashboard. It strengthened my experience in data cleaning, exploratory analysis, time-aware model validation, visual communication, and building a deployable data application.

## Repository

[View the source code and datasets](https://github.com/YashviBhansali/Housing-Affordability)
