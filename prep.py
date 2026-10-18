import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if not os.path.exists('Data/Clean/singapore_merged.csv'):
    raise FileNotFoundError(f'Run from the project folder that contains Data/. Current folder: {os.getcwd()}')
os.makedirs('Figures', exist_ok=True)

# --- Load and trim HK to the Singapore window ---
sg = pd.read_csv('Data/Clean/singapore_merged.csv')
hk = pd.read_csv('Data/Clean/hongkong_merged.csv')
hk = hk[(hk['quarter'] >= '2017Q1') & (hk['quarter'] <= '2025Q4')].copy().reset_index(drop=True)
sg['quarter_period'] = pd.PeriodIndex(sg['quarter'], freq='Q')
hk['quarter_period'] = pd.PeriodIndex(hk['quarter'], freq='Q')

# --- Re-index to 2017Q1 = 100, affordability index ---
def rebase(s):
    return s / s.iloc[0] * 100

sg['price_idx'], sg['cpi_idx'], sg['income_idx'] = (rebase(sg['resale_price_index']),
                                                    rebase(sg['cpi']), rebase(sg['income_median']))
hk['price_idx'], hk['cpi_idx'], hk['income_idx'] = (rebase(hk['hk_price_index']),
                                                    rebase(hk['hk_cpi']), rebase(hk['hk_income_median']))
for df in (sg, hk):
    df['afford_idx'] = df['price_idx'] / df['income_idx'] * 100   # higher = less affordable

# --- YoY growth rates ---
for df, p, i, c in [(sg, 'resale_price_index', 'income_median', 'cpi'),
                    (hk, 'hk_price_index', 'hk_income_median', 'hk_cpi')]:
    df['price_yoy']  = df[p].pct_change(4) * 100
    df['income_yoy'] = df[i].pct_change(4) * 100
    df['cpi_yoy']    = df[c].pct_change(4) * 100

# --- COVID dummy (2020Q1-2022Q2) ---
for df in (sg, hk):
    df['covid'] = df['quarter_period'].between(pd.Period('2020Q1', 'Q'),
                                               pd.Period('2022Q2', 'Q')).astype(int)

# --- Feature lists ---
sg_feats_yoy = ['cpi_yoy', 'gdp', 'income_yoy', 'covid']
hk_feats_yoy = ['cpi_yoy', 'hk_gdp', 'income_yoy', 'hk_lending_rate', 'covid']

# --- Save model-ready datasets ---
sg.drop(columns='quarter_period').to_csv('Data/Clean/sg_model_ready.csv', index=False)
hk.drop(columns='quarter_period').to_csv('Data/Clean/hk_model_ready.csv', index=False)