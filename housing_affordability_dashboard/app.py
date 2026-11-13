from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Housing Affordability | Singapore & Hong Kong",
    layout="wide",
)


# Consistent visual styling: restrained research / editorial palette.
# CSS changes presentation only; all calculations and source data remain unchanged.
st.markdown("""
<style>
    :root {
        --ink: #172B3A;
        --muted: #647681;
        --forest: #246B58;
        --mint: #EAF2EE;
        --sand: #F5F3ED;
        --line: #DCE4E0;
    }
    .block-container {padding-top: 1.7rem; padding-bottom: 3.2rem; max-width: 1320px;}
    [data-testid="stAppViewContainer"] {background: #FBFCFA;}
    [data-testid="stHeader"] {background: rgba(251,252,250,0.85);}
    [data-testid="stSidebar"] {background: #F3F6F3; border-right: 1px solid var(--line);}
    [data-testid="stSidebar"] > div:first-child {padding-top: 1.5rem;}
    /* Streamlit headings: force a strong, readable ink colour. */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stHeading"] h1,
    [data-testid="stHeading"] h2,
    [data-testid="stHeading"] h3,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #172B3A !important;
        opacity: 1 !important;
        letter-spacing: -0.035em;
    }
    h1 {font-weight: 750;}
    h2 {font-weight: 700; margin-top: 1.2rem;}
    h3 {font-weight: 650;}
    p, li {color: #344955; line-height: 1.65;}
    [data-testid="stCaptionContainer"] p {color: var(--muted);}
    [data-testid="stMetric"] {
        background: #FFFFFF; padding: 17px 18px; border-radius: 13px;
        border: 1px solid var(--line); box-shadow: 0 2px 8px rgba(23,43,58,0.035);
    }
    [data-testid="stMetricLabel"] p {color: var(--muted); font-size: 0.82rem; font-weight: 600;}
    [data-testid="stMetricValue"] {color: var(--ink); font-weight: 750;}
    [data-testid="stMetricDelta"] {
        font-size: 0.78rem;
        color: #FFFFFF !important;
    }
    [data-testid="stMetricDelta"] p,
    [data-testid="stMetricDelta"] span {
        color: #FFFFFF !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricDelta"] svg {
        fill: #A7E6C8 !important;
        color: #A7E6C8 !important;
    }
    [data-testid="stDataFrame"] {border: 1px solid var(--line); border-radius: 10px; overflow: hidden;}
    [data-testid="stExpander"] {border: 1px solid var(--line); border-radius: 10px; background: #FFFFFF;}
    [data-testid="stAlert"] {border-radius: 10px;}
    [data-testid="stRadio"] label, [data-testid="stSelectbox"] label,
    [data-testid="stSelectSlider"] label {font-weight: 600; color: var(--ink);}
    div.stButton > button {border-radius: 8px; font-weight: 600;}
    hr {border-color: var(--line);}
    .hero {
        background: linear-gradient(115deg, #173B3A 0%, #246B58 68%, #4D8874 100%);
        border-radius: 18px; padding: 30px 34px; margin: 0.4rem 0 1.5rem 0;
        color: #FFFFFF; box-shadow: 0 8px 24px rgba(23,59,58,0.12);
    }
    .hero-kicker {font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: #D3E6DC; margin-bottom: 9px;}
    .hero-title {font-size: clamp(1.8rem, 4vw, 2.65rem); line-height: 1.1;
        font-weight: 760; letter-spacing: -0.045em; color: #FFFFFF; margin: 0;}
    .hero-subtitle {font-size: 0.98rem; color: #E3EEE8; margin-top: 10px; max-width: 820px;}
    .hero-meta {display: flex; flex-wrap: wrap; gap: 9px; margin-top: 20px;}
    .hero-pill {font-size: 0.74rem; color: #F3F8F5; border: 1px solid rgba(255,255,255,0.28);
        border-radius: 30px; padding: 5px 11px; background: rgba(255,255,255,0.08);}
    .sidebar-brand {font-size: 1.05rem; font-weight: 750; color: var(--ink); margin-bottom: 2px;}
    .sidebar-note {font-size: 0.78rem; color: var(--muted); line-height: 1.45;}
    .section-note {background: var(--sand); border-left: 3px solid var(--forest);
        border-radius: 0 8px 8px 0; padding: 10px 14px; color: #40545D; font-size: 0.9rem;}
    @media (max-width: 700px) {
        .block-container {padding-left: 1rem; padding-right: 1rem;}
        .hero {padding: 23px 21px;}
    }
</style>
""", unsafe_allow_html=True)

# Plotly defaults keep every chart visually consistent.
px.defaults.template = "plotly_white"
pio.templates.default = "plotly_white"
px.defaults.color_discrete_sequence = ["#176B55", "#B96516", "#356A91", "#875477", "#657C35"]


def render_plotly_chart(fig, **kwargs):
    """Apply an explicit, high-contrast Plotly theme and visible trace styling."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", size=13, color="#24343B"),
        title_font=dict(color="#24343B", size=18),
        legend=dict(font=dict(color="#24343B", size=12), bgcolor="rgba(255,255,255,0.88)"),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#AAB8B1",
            font=dict(family="Arial, sans-serif", size=13, color="#172B32"),
            align="left",
        ),
        hovermode=fig.layout.hovermode or "closest",
    )
    fig.update_xaxes(
        color="#24343B",
        title_font=dict(color="#24343B"),
        tickfont=dict(color="#24343B"),
        gridcolor="#E5EAE7",
        zerolinecolor="#AAB8B1",
        linecolor="#AAB8B1",
        showline=True,
        showgrid=True,
    )
    fig.update_yaxes(
        color="#24343B",
        title_font=dict(color="#24343B"),
        tickfont=dict(color="#24343B"),
        gridcolor="#E5EAE7",
        zerolinecolor="#AAB8B1",
        linecolor="#AAB8B1",
        showline=True,
        showgrid=True,
    )
    # Explicitly prevent traces/markers from inheriting invisible or transparent styling.
    fig.update_traces(selector=dict(type="scatter"), opacity=1)
    fig.update_traces(
        selector=dict(type="scatter", mode="lines+markers"),
        line=dict(width=3),
        marker=dict(size=7, opacity=1, line=dict(width=1, color="#FFFFFF")),
    )
    fig.update_traces(
        selector=dict(type="scatter", mode="lines"),
        line=dict(width=3),
    )
    st.plotly_chart(fig, use_container_width=True, **{k: v for k, v in kwargs.items() if k != "use_container_width"})

st.markdown("""
<div class="hero">
  <div class="hero-kicker">Comparative economic research · Interactive dashboard</div>
  <div class="hero-title">Housing Affordability</div>
  <div class="hero-subtitle">What changed in Singapore and Hong Kong — and how well can economic indicators predict housing-price growth?</div>
  <div class="hero-meta">
    <span class="hero-pill">Singapore</span>
    <span class="hero-pill">Hong Kong</span>
    <span class="hero-pill">2017Q1 — 2025Q4</span>
    <span class="hero-pill">36 quarterly observations each</span>
  </div>
</div>
""", unsafe_allow_html=True)

# The app.py file should be inside:
# Housing Affordability/housing_affordability_dashboard/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA_DIR = PROJECT_ROOT / "data" / "clean"

SINGAPORE_FILE = CLEAN_DATA_DIR / "singapore_merged.csv"
HONGKONG_FILE = CLEAN_DATA_DIR / "hongkong_merged.csv"

START_QUARTER = "2017Q1"
END_QUARTER = "2025Q4"


# ============================================================
# 2. LOAD AND PREPARE THE EXISTING CLEANED DATA
# ============================================================

@st.cache_data
def load_data():
    singapore = pd.read_csv(SINGAPORE_FILE)
    hongkong = pd.read_csv(HONGKONG_FILE)

    required_sg = {
        "quarter", "resale_price_index", "cpi", "gdp",
        "income_avg", "income_median", "resale_volume"
    }
    required_hk = {
        "quarter", "hk_price_index", "hk_cpi", "hk_gdp",
        "hk_income_median", "hk_lending_rate"
    }

    missing_sg = required_sg - set(singapore.columns)
    missing_hk = required_hk - set(hongkong.columns)

    if missing_sg:
        raise ValueError(
            f"Singapore CSV is missing columns: {sorted(missing_sg)}"
        )
    if missing_hk:
        raise ValueError(
            f"Hong Kong CSV is missing columns: {sorted(missing_hk)}"
        )

    singapore["quarter"] = pd.PeriodIndex(
        singapore["quarter"].astype(str), freq="Q"
    )
    hongkong["quarter"] = pd.PeriodIndex(
        hongkong["quarter"].astype(str), freq="Q"
    )

    start = pd.Period(START_QUARTER, freq="Q")
    end = pd.Period(END_QUARTER, freq="Q")

    singapore = singapore[
        singapore["quarter"].between(start, end)
    ].copy()

    hongkong = hongkong[
        hongkong["quarter"].between(start, end)
    ].copy()

    singapore = singapore.sort_values("quarter").reset_index(drop=True)
    hongkong = hongkong.sort_values("quarter").reset_index(drop=True)

    if len(singapore) != 36 or len(hongkong) != 36:
        raise ValueError(
            "Expected exactly 36 observations per country from "
            "2017Q1 to 2025Q4. Check the quarter values in the CSV files."
        )

    # Rebase prices and median incomes to 100 in 2017Q1.
    singapore["price_index"] = (
        singapore["resale_price_index"]
        / singapore["resale_price_index"].iloc[0]
    ) * 100

    singapore["income_index"] = (
        singapore["income_median"]
        / singapore["income_median"].iloc[0]
    ) * 100

    hongkong["price_index"] = (
        hongkong["hk_price_index"]
        / hongkong["hk_price_index"].iloc[0]
    ) * 100

    hongkong["income_index"] = (
        hongkong["hk_income_median"]
        / hongkong["hk_income_median"].iloc[0]
    ) * 100

    # Relative affordability index:
    # (price index / income index) * 100.
    singapore["affordability_index"] = (
        singapore["price_index"] / singapore["income_index"]
    ) * 100

    hongkong["affordability_index"] = (
        hongkong["price_index"] / hongkong["income_index"]
    ) * 100

    return singapore, hongkong


try:
    singapore, hongkong = load_data()
except Exception as error:
    st.error(f"Could not load the project data: {error}")
    st.write("Expected data files:")
    st.code(
        "Housing Affordability/\n"
        "├── data/\n"
        "│   └── clean/\n"
        "│       ├── singapore_merged.csv\n"
        "│       └── hongkong_merged.csv\n"
        "└── housing_affordability_dashboard/\n"
        "    └── app.py"
    )
    st.stop()


# ============================================================
# 3. SUMMARY METRICS
# ============================================================

def percentage_change(series):
    return (series.iloc[-1] / series.iloc[0] - 1) * 100


sg_price_growth = percentage_change(singapore["resale_price_index"])
sg_income_growth = percentage_change(singapore["income_median"])
hk_price_growth = percentage_change(hongkong["hk_price_index"])
hk_income_growth = percentage_change(hongkong["hk_income_median"])

sg_final_affordability = singapore["affordability_index"].iloc[-1]
hk_final_affordability = hongkong["affordability_index"].iloc[-1]


# ============================================================
# 4. MODEL RESULTS FROM THE EXISTING NOTEBOOK EXPERIMENTS
# ============================================================

MODEL_ORDER = ["Naive", "OLS", "Ridge (scaled)", "Random Forest"]

# Main experiment: four-fold rolling-origin validation.
four_fold_means = pd.DataFrame(
    {
        "Model": MODEL_ORDER,
        "Singapore": [4.26, 3.65, 3.07, 3.03],
        "Hong Kong": [9.64, 5.35, 4.79, 7.80],
    }
)

four_fold_details = {
    "Singapore": pd.DataFrame(
        {
            "Fold": [1, 2, 3, 4],
            "Naive": [8.67, 2.68, 2.96, 2.72],
            "OLS": [3.30, 2.78, 4.97, 3.56],
            "Ridge (scaled)": [2.07, 2.05, 4.84, 3.33],
            "Random Forest": [1.26, 2.51, 5.40, 2.94],
        }
    ),
    "Hong Kong": pd.DataFrame(
        {
            "Fold": [1, 2, 3, 4],
            "Naive": [11.40, 11.03, 12.00, 4.11],
            "OLS": [7.59, 6.18, 4.23, 3.40],
            "Ridge (scaled)": [6.48, 5.02, 4.31, 3.34],
            "Random Forest": [8.87, 14.26, 6.22, 1.83],
        }
    ),
}

# Separate five-fold experiment. These are not pooled with the
# four-fold experiment because the validation windows differ.
five_fold_means = pd.DataFrame(
    {
        "Model": MODEL_ORDER,
        "Singapore": [5.26, 6.36, 5.02, 4.50],
        "Hong Kong": [8.12, 18.68, 10.08, 7.20],
    }
)

# Regression diagnostics reported by the existing notebook.
diagnostics = pd.DataFrame(
    [
        ["Singapore", "Durbin-Watson", 1.06],
        ["Hong Kong", "Durbin-Watson", 1.46],
        ["Singapore", "VIF: CPI", 22.4],
        ["Singapore", "VIF: GDP", 1.2],
        ["Singapore", "VIF: Median income", 22.1],
        ["Singapore", "VIF: COVID", 1.2],
        ["Hong Kong", "VIF: CPI", 6.0],
        ["Hong Kong", "VIF: GDP", 1.3],
        ["Hong Kong", "VIF: Median income", 2.4],
        ["Hong Kong", "VIF: Lending rate", 5.2],
        ["Hong Kong", "VIF: COVID", 4.5],
    ],
    columns=["Country", "Diagnostic", "Value"],
)

# Full-sample standardised Ridge coefficients supplied in the notebook.
ridge_coefficients = {
    "Singapore": pd.DataFrame(
        {
            "Feature": ["GDP", "COVID", "CPI YoY", "Income YoY"],
            "Standardised coefficient": [1.03, 1.52, 1.60, 2.11],
        }
    ),
    "Hong Kong": pd.DataFrame(
        {
            "Feature": [
                "Lending rate", "Income YoY", "COVID", "GDP", "CPI YoY"
            ],
            "Standardised coefficient": [-5.26, 1.16, 1.19, 3.52, 3.56],
        }
    ),
}

# Separate holdout OLS outputs from the notebook.
# These are NOT the rolling-origin cross-validation results.
holdout_results = pd.DataFrame(
    [
        ["Singapore", "Price index level", 0.987, 8.39, 28, 8],
        ["Hong Kong", "Price index level", 0.732, 100.70, 28, 8],
        ["Singapore", "YoY price growth", 0.945, 4.82, 24, 8],
        ["Hong Kong", "YoY price growth", 0.776, 4.55, 24, 8],
    ],
    columns=[
        "Country", "Target", "Train R²", "Test RMSE",
        "Training observations", "Test observations"
    ],
)


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    "<div class='sidebar-brand'>HOUSING / DATA</div>"
    "<div class='sidebar-note'>Singapore × Hong Kong<br>Research dashboard</div>",
    unsafe_allow_html=True,
)
st.sidebar.divider()
st.sidebar.markdown("**Explore the research**")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Affordability Analysis",
        "Predictive Model Lab",
        "Data & Methodology",
    ],
)

st.sidebar.divider()
st.sidebar.caption("**Study period**  ·  2017Q1–2025Q4")
st.sidebar.caption("**Frequency**  ·  Quarterly")
st.sidebar.caption("**Sample**  ·  36 observations per market")
st.sidebar.caption("Built with Python · Streamlit · Plotly")


# ============================================================
# 6. OVERVIEW
# ============================================================

if page == "Overview":

    st.header("Overview")

    st.write(
        "This project examines whether public economic indicators "
        "help explain and predict housing price movements in Singapore "
        "and Hong Kong, and compares the relative affordability trends "
        "of the two housing markets."
    )

    st.subheader("Housing market changes")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Singapore price growth", f"{sg_price_growth:.1f}%")
    c2.metric("Singapore income growth", f"{sg_income_growth:.1f}%")
    c3.metric("Hong Kong price growth", f"{hk_price_growth:.1f}%")
    c4.metric("Hong Kong income growth", f"{hk_income_growth:.1f}%")

    st.subheader("Final relative affordability index")

    a1, a2 = st.columns(2)
    a1.metric(
        "Singapore",
        f"{sg_final_affordability:.1f}",
        delta=f"{sg_final_affordability - 100:+.1f} vs baseline",
    )
    a2.metric(
        "Hong Kong",
        f"{hk_final_affordability:.1f}",
        delta=f"{hk_final_affordability - 100:+.1f} vs baseline",
    )

    st.info(
        "The affordability index compares the growth of housing prices "
        "with the growth of median income, with 2017Q1 = 100. An index "
        "above 100 means prices have grown faster than median income. "
        "It is not a direct measure of the share of household income "
        "spent on housing."
    )

    st.subheader("Main findings")

    left, right = st.columns(2)

    with left:
        st.markdown("**Singapore**")
        st.write(
            "Housing prices increased by 52.1%, while median income "
            "increased by 37.9%. The final relative affordability index "
            "of 110.3 indicates that prices outpaced median income "
            "relative to the 2017Q1 baseline."
        )

    with right:
        st.markdown("**Hong Kong**")
        st.write(
            "Housing prices declined by 5.5%, while median income "
            "increased by 14.1%. The final index of 82.9 indicates an "
            "improvement in relative affordability on this measure. "
            "This does not mean housing became affordable in absolute terms."
        )

    st.subheader("Predictive modelling: headline result")

    best_sg = four_fold_means.loc[
        four_fold_means["Singapore"].idxmin()
    ]
    best_hk = four_fold_means.loc[
        four_fold_means["Hong Kong"].idxmin()
    ]

    b1, b2 = st.columns(2)
    b1.metric(
        "Lowest Singapore RMSE",
        f"{best_sg['Singapore']:.2f} pp",
        best_sg["Model"],
    )
    b2.metric(
        "Lowest Hong Kong RMSE",
        f"{best_hk['Hong Kong']:.2f} pp",
        best_hk["Model"],
    )

    st.caption(
        "Model results are from the four-fold rolling-origin experiment. "
        "Lower RMSE indicates lower average prediction error."
    )


# ============================================================
# 7. AFFORDABILITY ANALYSIS
# ============================================================

elif page == "Affordability Analysis":

    st.header("Affordability Analysis")
    st.write(
        "Compare housing prices, median income and their relative "
        "movement over the same 36-quarter period."
    )

    sg = singapore[
        ["quarter", "price_index", "income_index", "affordability_index"]
    ].copy()
    hk = hongkong[
        ["quarter", "price_index", "income_index", "affordability_index"]
    ].copy()

    sg["Country"] = "Singapore"
    hk["Country"] = "Hong Kong"

    combined = pd.concat([sg, hk], ignore_index=True)
    combined["Quarter"] = combined["quarter"].astype(str)

    quarters = sorted(combined["Quarter"].unique())

    selected_range = st.select_slider(
        "Select period",
        options=quarters,
        value=(quarters[0], quarters[-1]),
    )

    filtered = combined[
        combined["Quarter"].between(
            selected_range[0], selected_range[1]
        )
    ].copy()

    indicator_label = st.selectbox(
        "Select indicator",
        [
            "Relative affordability index",
            "Housing price index",
            "Median income index",
        ],
    )

    indicator_map = {
        "Relative affordability index": "affordability_index",
        "Housing price index": "price_index",
        "Median income index": "income_index",
    }
    y_col = indicator_map[indicator_label]

    fig = px.line(
        filtered,
        x="Quarter",
        y=y_col,
        color="Country",
        markers=True,
        title=indicator_label,
        labels={
            y_col: "Index (2017Q1 = 100)",
            "Quarter": "Quarter",
        },
    )

    fig.add_hline(
        y=100,
        line_dash="dash",
        annotation_text="2017Q1 baseline",
    )
    fig.update_layout(hovermode="x unified")
    render_plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Housing prices versus median income")

    comparison = filtered.melt(
        id_vars=["Quarter", "Country"],
        value_vars=["price_index", "income_index"],
        var_name="Measure",
        value_name="Index",
    )
    comparison["Measure"] = comparison["Measure"].map(
        {
            "price_index": "Housing prices",
            "income_index": "Median income",
        }
    )

    fig2 = px.line(
        comparison,
        x="Quarter",
        y="Index",
        color="Measure",
        facet_col="Country",
        markers=True,
        title="Price growth and median income growth",
    )
    fig2.add_hline(y=100, line_dash="dash")
    fig2.update_layout(hovermode="x unified")
    render_plotly_chart(fig2, use_container_width=True)

    st.subheader("Price growth minus income growth")
    gap_data = filtered.copy()
    gap_data["Price-income gap"] = gap_data["price_index"] - gap_data["income_index"]
    gap_fig = px.line(
        gap_data, x="Quarter", y="Price-income gap", color="Country",
        markers=True, title="Cumulative price-index gap relative to median income",
        labels={"Price-income gap": "Index-point difference"},
    )
    gap_fig.add_hline(y=0, line_dash="dash", annotation_text="Prices and income grew equally")
    gap_fig.update_layout(hovermode="x unified")
    render_plotly_chart(gap_fig, use_container_width=True)
    st.caption("A positive gap means the rebased housing price index is above the rebased median income index. This is a relative index comparison, not a household expenditure measure.")

    with st.expander("View quarterly data"):
        display_data = filtered[
            [
                "Quarter", "Country", "price_index",
                "income_index", "affordability_index"
            ]
        ].copy()
        display_data.columns = [
            "Quarter", "Country", "Price index",
            "Income index", "Affordability index"
        ]
        st.dataframe(display_data, use_container_width=True, hide_index=True)


# ============================================================
# 8. PREDICTIVE MODEL LAB
# ============================================================

elif page == "Predictive Model Lab":

    st.header("Predictive Model Lab")
    st.write(
        "This section compares models used to predict year-on-year "
        "housing price growth. The main comparison uses four-fold "
        "rolling-origin validation."
    )

    st.info(
        "RMSE is measured in percentage points (pp). Lower values "
        "indicate better predictive performance. The four-fold and "
        "five-fold experiments are shown separately because their "
        "validation designs differ."
    )

    # --------------------------------------------------------
    # A. Main four-fold experiment
    # --------------------------------------------------------

    st.subheader("1. Main experiment: four-fold rolling-origin validation")

    country_choice = st.radio(
        "Choose country",
        ["Compare both", "Singapore", "Hong Kong"],
        horizontal=True,
        key="fourfold_country",
    )

    if country_choice == "Compare both":
        model_plot = four_fold_means.melt(
            id_vars="Model",
            value_vars=["Singapore", "Hong Kong"],
            var_name="Country",
            value_name="Mean test RMSE",
        )

        fig = px.bar(
            model_plot,
            x="Model",
            y="Mean test RMSE",
            color="Country",
            barmode="group",
            title="Mean test RMSE by model and country",
            text_auto=".2f",
        )
        fig.update_layout(yaxis_title="RMSE (percentage points)")
        render_plotly_chart(fig, use_container_width=True)

        st.dataframe(
            four_fold_means,
            use_container_width=True,
            hide_index=True,
        )

    else:
        selected_mean = four_fold_means[
            ["Model", country_choice]
        ].rename(columns={country_choice: "Mean test RMSE"})

        fig = px.bar(
            selected_mean,
            x="Model",
            y="Mean test RMSE",
            title=f"{country_choice}: mean test RMSE",
            text_auto=".2f",
        )
        fig.update_layout(yaxis_title="RMSE (percentage points)")
        render_plotly_chart(fig, use_container_width=True)

        st.dataframe(
            selected_mean,
            use_container_width=True,
            hide_index=True,
        )

    # Best model metrics
    sg_best_idx = four_fold_means["Singapore"].idxmin()
    hk_best_idx = four_fold_means["Hong Kong"].idxmin()

    sg_best_model = four_fold_means.loc[sg_best_idx, "Model"]
    hk_best_model = four_fold_means.loc[hk_best_idx, "Model"]
    sg_best_rmse = four_fold_means.loc[sg_best_idx, "Singapore"]
    hk_best_rmse = four_fold_means.loc[hk_best_idx, "Hong Kong"]

    m1, m2 = st.columns(2)
    m1.metric(
        "Best Singapore model",
        sg_best_model,
        f"{sg_best_rmse:.2f} pp RMSE",
    )
    m2.metric(
        "Best Hong Kong model",
        hk_best_model,
        f"{hk_best_rmse:.2f} pp RMSE",
    )

    st.markdown(
        """
        **Interpretation**

        - In Singapore, Random Forest has the lowest mean RMSE at 3.03,
          closely followed by scaled Ridge at 3.07.
        - In Hong Kong, scaled Ridge performs best at 4.79, followed
          by OLS at 5.35.
        - The best-performing model differs between the two markets.
        - The small difference between Random Forest and Ridge in
          Singapore should not be treated as strong evidence that one
          model is definitively superior.
        """
    )

    st.subheader("Model improvement over the naive baseline")
    improvement_rows = []
    for country in ["Singapore", "Hong Kong"]:
        baseline = float(four_fold_means.loc[four_fold_means["Model"] == "Naive", country].iloc[0])
        for _, row in four_fold_means[four_fold_means["Model"] != "Naive"].iterrows():
            improvement = (baseline - float(row[country])) / baseline * 100
            improvement_rows.append([country, row["Model"], baseline, float(row[country]), improvement])
    improvement_df = pd.DataFrame(improvement_rows, columns=["Country", "Model", "Naive RMSE", "Model RMSE", "RMSE reduction (%)"])
    improvement_plot = px.bar(
        improvement_df, x="Model", y="RMSE reduction (%)", color="Country",
        barmode="group", text_auto=".1f",
        title="Reduction in RMSE relative to the naive baseline",
    )
    improvement_plot.add_hline(y=0, line_dash="dash")
    improvement_plot.update_layout(yaxis_title="RMSE reduction (%)")
    render_plotly_chart(improvement_plot, use_container_width=True)
    st.dataframe(improvement_df.round(2), use_container_width=True, hide_index=True)
    st.caption("Positive values indicate lower RMSE than the naive baseline. These percentages describe this validation experiment only; they are not percentage increases in prediction accuracy.")

    # --------------------------------------------------------
    # B. Fold-by-fold results
    # --------------------------------------------------------

    st.divider()
    st.subheader("2. Fold-by-fold validation results")

    fold_country = st.selectbox(
        "Select country for fold details",
        ["Singapore", "Hong Kong"],
        key="fold_country",
    )

    fold_df = four_fold_details[fold_country].copy()

    consistency_df = pd.DataFrame({
        "Model": [c for c in fold_df.columns if c != "Fold"],
        "Mean RMSE": [fold_df[c].mean() for c in fold_df.columns if c != "Fold"],
        "Standard deviation": [fold_df[c].std(ddof=1) for c in fold_df.columns if c != "Fold"],
        "Minimum": [fold_df[c].min() for c in fold_df.columns if c != "Fold"],
        "Maximum": [fold_df[c].max() for c in fold_df.columns if c != "Fold"],
    })
    st.markdown("**Consistency across the four folds**")
    st.dataframe(consistency_df.round(2), use_container_width=True, hide_index=True)
    st.caption("The standard deviation and range describe variation across only four validation folds. They are useful diagnostics, not precise estimates of future uncertainty.")

    fold_long = fold_df.melt(
        id_vars="Fold",
        var_name="Model",
        value_name="Test RMSE",
    )

    fold_fig = px.line(
        fold_long,
        x="Fold",
        y="Test RMSE",
        color="Model",
        markers=True,
        title=f"{fold_country}: RMSE across validation folds",
    )
    fold_fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3, 4],
        ),
        yaxis_title="Test RMSE (percentage points)",
        hovermode="x unified",
    )
    render_plotly_chart(fold_fig, use_container_width=True)

    st.dataframe(
        fold_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Fold scores show how model performance changes across "
        "different validation windows. A low mean can still conceal "
        "large errors in individual folds."
    )

    # --------------------------------------------------------
    # C. Alternative five-fold experiment
    # --------------------------------------------------------

    st.divider()
    st.subheader("3. Alternative experiment: five-fold validation")

    st.write(
        "This is a separate experiment from the four-fold comparison. "
        "It is included for transparency, not combined with the main results."
    )

    five_long = five_fold_means.melt(
        id_vars="Model",
        value_vars=["Singapore", "Hong Kong"],
        var_name="Country",
        value_name="Mean test RMSE",
    )

    five_fig = px.bar(
        five_long,
        x="Model",
        y="Mean test RMSE",
        color="Country",
        barmode="group",
        title="Five-fold experiment: mean test RMSE",
        text_auto=".2f",
    )
    five_fig.update_layout(yaxis_title="RMSE (percentage points)")
    render_plotly_chart(five_fig, use_container_width=True)

    st.dataframe(
        five_fold_means,
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "The five-fold and four-fold results should not be compared "
        "as if they were generated by an identical validation design. "
        "Confirm the feature sets, target construction, preprocessing, "
        "fold windows and tuning procedure before drawing conclusions "
        "about why their scores differ."
    )

    # --------------------------------------------------------
    # D. Regression analysis and diagnostics
    # --------------------------------------------------------

    st.divider()
    st.subheader("4. Regression analysis and diagnostics")

    st.write(
        "These statistics come from separate regression and diagnostic "
        "outputs in the research notebook. They are not the same as "
        "the rolling-origin model scores above."
    )

    with st.expander("Holdout OLS regression results"):
        st.dataframe(
            holdout_results,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "The level-based and YoY-growth regressions have different "
            "dependent variables. Their RMSE values should not be "
            "compared directly."
        )

    with st.expander("Regression diagnostics: VIF and Durbin-Watson"):
        st.dataframe(
            diagnostics,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            """
            **How to interpret these diagnostics**

            - VIF measures how strongly a predictor is linearly related
              to the other predictors in the regression. High values
              can make individual OLS coefficients unstable.
            - Singapore's CPI and median income VIF values are high,
              suggesting substantial multicollinearity.
            - Durbin-Watson values below 2 can indicate positive
              residual autocorrelation. The reported values warrant
              further investigation.
            """
        )

    with st.expander("Standardised Ridge coefficients"):
        coefficient_country = st.radio(
            "Select coefficient set",
            ["Singapore", "Hong Kong"],
            horizontal=True,
            key="coefficient_country",
        )

        coef_df = ridge_coefficients[coefficient_country].copy()

        coef_fig = px.bar(
            coef_df,
            x="Feature",
            y="Standardised coefficient",
            title=f"{coefficient_country}: full-sample standardised Ridge coefficients",
            text_auto=".2f",
        )
        coef_fig.add_hline(y=0, line_dash="dash")
        render_plotly_chart(coef_fig, use_container_width=True)

        st.dataframe(
            coef_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "These are full-sample standardised coefficients reported "
            "by the notebook. They are descriptive and should not be "
            "interpreted as causal effects or as fold-independent "
            "feature importance."
        )

    # --------------------------------------------------------
    # E. YoY OLS coefficients and statistical associations
    # --------------------------------------------------------

    st.divider()
    st.subheader("5. YoY OLS coefficients and p-values")
    st.write("These are the reported YoY OLS regression estimates from the notebook. Coefficients describe conditional associations in the fitted models; they do not establish causation.")
    yoy_ols = pd.DataFrame([
        ["Singapore", "CPI YoY", 1.2355, 0.001, "<0.001"],
        ["Singapore", "GDP", 0.0450, 0.143, "0.143"],
        ["Singapore", "Income YoY", 0.4358, 0.005, "0.005"],
        ["Singapore", "COVID", 5.3755, 0.001, "<0.001"],
        ["Hong Kong", "CPI YoY", 3.2476, 0.048, "0.048"],
        ["Hong Kong", "GDP", 0.9105, 0.004, "0.004"],
        ["Hong Kong", "Income YoY", 0.1039, 0.673, "0.673"],
        ["Hong Kong", "Lending rate", -20.1130, 0.001, "<0.001"],
        ["Hong Kong", "COVID", -0.6450, 0.841, "0.841"],
    ], columns=["Country", "Predictor", "Coefficient", "P-value numeric", "P-value"])
    yoy_ols["Significant at 5%"] = yoy_ols["P-value numeric"] < 0.05
    ols_country = st.radio("Select OLS results", ["Singapore", "Hong Kong"], horizontal=True, key="yoy_ols_country")
    ols_view = yoy_ols[yoy_ols["Country"] == ols_country].copy()
    ols_fig = px.bar(ols_view, x="Predictor", y="Coefficient", color="Significant at 5%",
                     title=f"{ols_country}: YoY OLS coefficients", text_auto=".2f")
    ols_fig.add_hline(y=0, line_dash="dash")
    render_plotly_chart(ols_fig, use_container_width=True)
    st.dataframe(ols_view[["Predictor", "Coefficient", "P-value", "Significant at 5%"]].round(4), use_container_width=True, hide_index=True)
    st.caption("P-values are shown as reported/rounded in the notebook. Statistical significance at 5% does not imply a large effect or a causal relationship. Coefficient units depend on the units of each predictor.")

    # --------------------------------------------------------
    # F. Model limitations
    # --------------------------------------------------------

    st.divider()
    st.subheader("6. Model limitations")

    st.markdown(
        """
        - **Small sample:** Each country has only 36 quarterly observations.
          Results can be sensitive to the choice of validation windows.
        - **Time dependence:** Housing markets are time series. Validation
          must preserve chronological order and avoid random shuffling.
        - **Model instability:** Individual fold scores vary, particularly
          for Hong Kong Random Forest.
        - **Multicollinearity:** Some predictors, particularly Singapore's
          CPI and median income, are strongly related.
        - **Prediction is not causation:** A predictor's coefficient or
          predictive contribution does not establish a causal relationship.
        - **Experiment consistency:** Differences between validation
          experiments need to be checked against their features,
          preprocessing, target definitions and fold construction.
        """
    )


# ============================================================
# 9. DATA AND METHODOLOGY
# ============================================================

elif page == "Data & Methodology":

    st.header("Data & Methodology")

    st.subheader("Study design")

    st.write(
        "The study uses quarterly observations from 2017Q1 to 2025Q4 "
        "for Singapore and Hong Kong. Each country contributes 36 "
        "observations to the common comparison period."
    )

    st.subheader("Data variables")

    data_dictionary = pd.DataFrame(
        [
            ["Singapore", "resale_price_index", "Housing resale price index"],
            ["Singapore", "cpi", "Consumer price index"],
            ["Singapore", "gdp", "GDP growth indicator"],
            ["Singapore", "income_avg", "Average income"],
            ["Singapore", "income_median", "Median income"],
            ["Singapore", "resale_volume", "Resale transaction volume"],
            ["Hong Kong", "hk_price_index", "Housing price index"],
            ["Hong Kong", "hk_cpi", "Consumer price index"],
            ["Hong Kong", "hk_gdp", "GDP growth indicator"],
            ["Hong Kong", "hk_income_median", "Median income"],
            ["Hong Kong", "hk_lending_rate", "Lending rate"],
        ],
        columns=["Country", "Variable", "Description"],
    )

    st.dataframe(
        data_dictionary,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Affordability calculation")

    st.latex(
        r"Price\ Index_t = "
        r"\frac{Price_t}{Price_{2017Q1}} \times 100"
    )
    st.latex(
        r"Income\ Index_t = "
        r"\frac{Income_t}{Income_{2017Q1}} \times 100"
    )
    st.latex(
        r"Affordability\ Index_t = "
        r"\frac{Price\ Index_t}{Income\ Index_t} \times 100"
    )

    st.write(
        "An index above 100 indicates that housing prices have grown "
        "faster than median income relative to the 2017Q1 baseline."
    )

    st.subheader("Predictive validation")

    st.write(
        "The main model comparison uses rolling-origin validation. "
        "Training observations precede the test observations in time. "
        "RMSE is reported in percentage points, and lower values "
        "indicate better predictive accuracy."
    )

    st.subheader("Limitations")

    st.markdown(
        """
        - The study uses a relatively small quarterly sample.
        - The affordability index is a relative comparison, not a
          complete household affordability measure.
        - The two countries have different housing systems and
          economic structures.
        - Predictive relationships do not establish causation.
        - Model performance may change with different validation
          windows, predictor sets or preprocessing choices.
        """
    )

    st.subheader("Data quality checks")

    q1, q2 = st.columns(2)
    q1.metric("Singapore observations", len(singapore))
    q2.metric("Hong Kong observations", len(hongkong))

    st.write(
        f"Singapore missing values: **{int(singapore.isna().sum().sum())}**"
    )
    st.write(
        f"Hong Kong missing values: **{int(hongkong.isna().sum().sum())}**"
    )

    st.caption(
        "The dashboard reads the existing cleaned CSV files. "
        "It does not modify the original datasets or notebooks."
    )


# ============================================================
# 10. FOOTER
# ============================================================

st.divider()
st.markdown(
    "<div style='text-align:center; padding:12px 0 4px 0; color:#71818A; "
    "font-size:0.78rem;'>HOUSING AFFORDABILITY RESEARCH &nbsp;·&nbsp; "
    "SINGAPORE × HONG KONG &nbsp;·&nbsp; 2017Q1–2025Q4</div>",
    unsafe_allow_html=True,
)



# ============================================================
# FINAL COLOUR SYSTEM — DARK, HIGH-CONTRAST, CONSISTENT
# All dashboard surfaces are dark; all readable text is light.
# ============================================================
st.markdown("""
<style>
:root {
    color-scheme: dark;
    --page: #101719;
    --surface: #182326;
    --surface-raised: #202E32;
    --surface-soft: #1B292C;
    --surface-warm: #26302D;
    --ink: #F2F6F4;
    --body: #E0E9E5;
    --muted: #B3C2BC;
    --forest: #4FA889;
    --forest-hover: #67BE9E;
    --border: #3B4B4D;
    --focus: #E5B66A;
}
html, body, [data-testid="stApp"],
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], .main {
    background: var(--page) !important;
    color: var(--body) !important;
    color-scheme: dark !important;
}
.block-container { background: transparent !important; }
[data-testid="stHeader"] { background: rgba(16,23,25,.96) !important; }
[data-testid="stSidebar"], section[data-testid="stSidebar"],
[data-testid="stSidebar"] > div, [data-testid="stSidebarContent"] {
    background: #172225 !important;
    color: var(--body) !important;
    border-right: 1px solid var(--border) !important;
}

/* Main copy, labels and headings */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"], [data-testid="stText"] p,
[data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
[data-testid="stMain"] label, [data-testid="stMain"] small,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em {
    color: var(--body) !important;
    opacity: 1 !important;
}
[data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"] *,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: var(--ink) !important;
    opacity: 1 !important;
}

/* Hero panel */
.hero {
    background: linear-gradient(115deg, #102D2B 0%, #174A3D 72%, #286A55 100%) !important;
    border: 1px solid #38685A !important;
}
.hero .hero-kicker, .hero .hero-subtitle { color: #DCEBE4 !important; }
.hero .hero-title, .hero .hero-pill { color: #FFFFFF !important; }
.hero .hero-pill { border-color: rgba(255,255,255,.32) !important; }
.sidebar-brand { color: var(--ink) !important; }
.sidebar-note { color: var(--muted) !important; }

/* Cards, metric panels, expanders, containers */
[data-testid="stMetric"], [data-testid="stExpander"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stDataFrame"], [data-testid="stTable"],
[data-testid="stForm"], [data-testid="stPopover"] {
    background: var(--surface) !important;
    color: var(--body) !important;
    border-color: var(--border) !important;
}
[data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"] *,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
    color: var(--body) !important;
    opacity: 1 !important;
}
[data-testid="stMetricValue"] * { color: var(--ink) !important; }
[data-testid="stMetricDelta"] svg { color: #75D6AE !important; fill: #75D6AE !important; }
.section-note {
    background: var(--surface-warm) !important;
    color: var(--body) !important;
    border-left-color: var(--forest) !important;
}

/* Alerts and status messages */
[data-testid="stAlert"], [data-testid="stNotification"] {
    background: #24332F !important;
    border: 1px solid #49685B !important;
}
[data-testid="stAlert"] *, [data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stNotification"] * {
    color: #E5F1EA !important;
    opacity: 1 !important;
}

/* Tabs and form controls */
[data-testid="stTabs"] button, [data-testid="stTab"] {
    color: var(--body) !important; opacity: 1 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #83D8B6 !important;
    font-weight: 750 !important;
    border-bottom-color: #65C39D !important;
}
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label,
[data-testid="stToggle"] label, [data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label, [data-testid="stSlider"] label,
[data-testid="stSelectSlider"] label, [data-testid="stDateInput"] label {
    color: var(--ink) !important; opacity: 1 !important;
}
input, textarea, [data-baseweb="select"] > div,
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div,
[data-testid="stDateInput"] input {
    color: var(--ink) !important;
    background: #202D31 !important;
    border-color: #526568 !important;
}
input::placeholder, textarea::placeholder {
    color: #AFC0B9 !important; opacity: 1 !important;
}
[data-baseweb="select"] *, [data-baseweb="popover"] *,
[role="listbox"] *, [role="option"] {
    color: var(--ink) !important;
    background-color: #202D31 !important;
}
[data-baseweb="popover"] { background: #202D31 !important; }
[data-baseweb="tag"] { background: #315B4D !important; }
[data-baseweb="tag"] * { color: #FFFFFF !important; }

/* Tables and code areas */
[data-testid="stDataFrame"] *, [data-testid="stTable"] * {
    color: var(--body) !important;
}
[data-testid="stDataFrame"] [role="grid"],
[data-testid="stDataFrame"] canvas {
    background: #182326 !important;
}
[data-testid="stCodeBlock"], [data-testid="stCodeBlock"] pre,
[data-testid="stCodeBlock"] code, pre, code {
    background: #202D31 !important;
    color: #E3ECE7 !important;
    border-color: var(--border) !important;
}
[data-testid="stLatex"] *, .katex, .katex * { color: var(--body) !important; }

/* Buttons */
div.stButton > button, [data-testid="stDownloadButton"] button {
    color: #FFFFFF !important;
    background: #286B55 !important;
    border: 1px solid #4C987A !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
}
div.stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
    color: #FFFFFF !important;
    background: #347E65 !important;
    border-color: #75C7A5 !important;
}
button:focus-visible, input:focus-visible, textarea:focus-visible {
    outline: 3px solid var(--focus) !important;
    outline-offset: 2px !important;
}
a, a:visited { color: #8AD9B8 !important; }
hr, [data-testid="stDivider"] { border-color: var(--border) !important; }

/* Keep only the chart's outer frame styled here. Plotly itself controls its SVG. */
[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)
