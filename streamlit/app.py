import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

# ── Uber brand palette ───────────────────────────────────────────────────────
UBER_BLACK = "#000000"
UBER_WHITE = "#FFFFFF"
UBER_GREEN = "#06C167"
UBER_GREEN_DARK = "#048848"
UBER_BLUE = "#276EF1"
UBER_ORANGE = "#FF6937"
UBER_RED = "#E54B4B"
UBER_GREY_50 = "#F6F6F6"
UBER_GREY_100 = "#EEEEEE"
UBER_GREY_300 = "#B0B0B0"
UBER_GREY_500 = "#757575"
UBER_GREY_700 = "#545454"

BOROUGH_COLORS = {
    "Manhattan": UBER_GREEN,
    "Brooklyn": UBER_BLUE,
    "Queens": UBER_ORANGE,
    "Bronx": "#8B5CF6",
    "Staten Island": UBER_GREY_500,
}

FONT_FAMILY = "'UberMove', 'UberMoveText', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
PLOTLY_FONT = "UberMove, UberMoveText, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"

# ── Load logo ────────────────────────────────────────────────────────────────
LOGO_PATH = Path(__file__).parent / "uber_eats_frony.svg"
LOGO_B64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UberEats NYC – Postal Code Prioritization",
    page_icon="🗽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS – Uber Move font + white background ──────────────────────────
st.markdown(f"""
<style>
/* ── Uber Move font (CDN fallback to system sans-serif) ─────────────────── */
@font-face {{
    font-family: 'UberMove';
    src: url('https://d1a3f4spazzrp4.cloudfront.net/dotcom-assets/fonts/UberMove-Medium.woff2') format('woff2');
    font-weight: 500;
    font-style: normal;
    font-display: swap;
}}
@font-face {{
    font-family: 'UberMove';
    src: url('https://d1a3f4spazzrp4.cloudfront.net/dotcom-assets/fonts/UberMove-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}}
@font-face {{
    font-family: 'UberMoveText';
    src: url('https://d1a3f4spazzrp4.cloudfront.net/dotcom-assets/fonts/UberMoveText-Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}}
@font-face {{
    font-family: 'UberMoveText';
    src: url('https://d1a3f4spazzrp4.cloudfront.net/dotcom-assets/fonts/UberMoveText-Medium.woff2') format('woff2');
    font-weight: 500;
    font-style: normal;
    font-display: swap;
}}

/* ── Global ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: {FONT_FAMILY};
    background-color: #FFFFFF;
}}
.stApp {{
    background-color: #FFFFFF;
}}
.block-container {{
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}}

/* Remove default Streamlit header bar */
header[data-testid="stHeader"] {{
    background-color: #FFFFFF;
    border-bottom: 1px solid #EEEEEE;
}}

/* ── Header ─────────────────────────────────────────────────────────────── */
.uber-header {{
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1rem 0 1.25rem 0;
    border-bottom: 2px solid {UBER_GREEN};
    margin-bottom: 1.5rem;
}}
.uber-header img {{
    height: 44px;
    border-radius: 8px;
}}
.uber-header-text h1 {{
    font-family: {FONT_FAMILY};
    font-size: 1.5rem;
    font-weight: 700;
    color: {UBER_BLACK};
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.3px;
}}
.uber-header-text p {{
    font-family: {FONT_FAMILY};
    font-size: 0.85rem;
    color: {UBER_GREY_500};
    margin: 0.15rem 0 0 0;
}}

/* ── KPI cards ──────────────────────────────────────────────────────────── */
div[data-testid="stMetric"] {{
    background: {UBER_WHITE};
    border: 1px solid {UBER_GREY_100};
    border-radius: 8px;
    padding: 0.9rem 1rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}}
div[data-testid="stMetric"] label {{
    font-family: {FONT_FAMILY} !important;
    color: {UBER_GREY_500} !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    font-family: {FONT_FAMILY} !important;
    color: {UBER_BLACK} !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}}

/* ── Section headers ────────────────────────────────────────────────────── */
.section-header {{
    font-family: {FONT_FAMILY};
    font-size: 1.05rem;
    font-weight: 700;
    color: {UBER_BLACK};
    border-left: 3px solid {UBER_GREEN};
    padding-left: 0.65rem;
    margin: 1.75rem 0 0.75rem 0;
    letter-spacing: -0.2px;
}}

/* ── Filter bar ─────────────────────────────────────────────────────────── */
.filter-strip {{
    background: {UBER_GREY_50};
    border: 1px solid {UBER_GREY_100};
    border-radius: 8px;
    padding: 0.5rem 0.75rem 0.1rem 0.75rem;
    margin-bottom: 1.25rem;
}}

/* ── Multiselect pills ──────────────────────────────────────────────────── */
span[data-baseweb="tag"] {{
    background-color: {UBER_BLACK} !important;
    color: {UBER_WHITE} !important;
    border-radius: 4px !important;
    font-family: {FONT_FAMILY} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}

/* ── Selectbox ──────────────────────────────────────────────────────────── */
div[data-baseweb="select"] > div {{
    border-radius: 6px !important;
    border-color: {UBER_GREY_100} !important;
    font-family: {FONT_FAMILY} !important;
}}

/* ── Dataframe ──────────────────────────────────────────────────────────── */
.stDataFrame {{ border-radius: 6px; overflow: hidden; }}

/* ── Expander ───────────────────────────────────────────────────────────── */
div[data-testid="stExpander"] {{
    border: 1px solid {UBER_GREY_100};
    border-radius: 8px;
    background: {UBER_WHITE};
}}
div[data-testid="stExpander"] summary {{
    font-family: {FONT_FAMILY} !important;
    font-weight: 600 !important;
    color: {UBER_BLACK} !important;
}}
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] li,
div[data-testid="stExpander"] td,
div[data-testid="stExpander"] th,
div[data-testid="stExpander"] strong,
div[data-testid="stExpander"] .stMarkdown {{
    color: {UBER_BLACK} !important;
    font-family: {FONT_FAMILY} !important;
}}

/* ── Dividers ───────────────────────────────────────────────────────────── */
hr {{ border-color: {UBER_GREY_100} !important; }}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background-color: {UBER_GREY_50};
    border-right: 1px solid {UBER_GREY_100};
}}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    font-family: {FONT_FAMILY} !important;
}}
</style>
""", unsafe_allow_html=True)


# ── Load & merge data ────────────────────────────────────────────────────────
@st.cache_data
def load_internal_data():
    raw = pd.read_csv("internal_data_exercise.csv", parse_dates=["order_timestamp", "dropoff_timestamp"])
    raw["order_week"] = raw["order_timestamp"].dt.to_period("W").dt.start_time
    raw["order_month"] = raw["order_timestamp"].dt.to_period("M").dt.start_time
    raw["order_hour"] = raw["order_timestamp"].dt.hour
    raw["order_dow"] = raw["order_timestamp"].dt.day_name()
    raw["merchant_activation_date"] = pd.to_datetime(raw["merchant_activation_date"])
    raw["eater_account_creation_date"] = pd.to_datetime(raw["eater_account_creation_date"])
    return raw


@st.cache_data
def load_data():
    agg = pd.read_csv("agg_zip_statistics.csv")
    dim = pd.read_csv("dim_zipcode.csv")

    agg = agg.rename(columns={"zipcode": "zip_code"})
    dim = dim.rename(columns={"boro": "borough_dim"})

    # Deduplicate both sources to avoid inflated counts
    # For agg: prefer rows with a real borough name over "0"/NaN
    agg["borough"] = agg["borough"].replace("0", np.nan)
    agg = agg.sort_values("borough", na_position="last").drop_duplicates(subset="zip_code", keep="first")
    dim["borough_dim"] = dim["borough_dim"].replace("0", np.nan)
    dim = dim.sort_values("borough_dim", na_position="last").drop_duplicates(subset="zip_code", keep="first")

    df = agg.merge(dim, on="zip_code", how="left")

    df["borough"] = df["borough"].fillna(df["borough_dim"])
    df.drop(columns=["borough_dim"], inplace=True)
    df = df.dropna(subset=["order_volume"])

    # Normalized scores (0-100)
    dt_min, dt_max = df["avg_delivery_time"].min(), df["avg_delivery_time"].max()
    df["delivery_speed_score"] = 100 * (dt_max - df["avg_delivery_time"]) / (dt_max - dt_min)

    qi_min, qi_max = df["avg_quality_index"].min(), df["avg_quality_index"].max()
    df["quality_score_norm"] = 100 * (qi_max - df["avg_quality_index"]) / (qi_max - qi_min)

    for col, new, invert in [
        ("orders_per_1k_residents", "penetration_norm", True),  # invert: low penetration = high opportunity
        ("growth_rate", "growth_norm", False),
        ("coverage_gap", "coverage_gap_norm", False),  # high gap = more room to acquire merchants = high score
    ]:
        cmin, cmax = df[col].min(), df[col].max()
        df[new] = 100 * ((cmax - df[col]) if invert else (df[col] - cmin)) / (cmax - cmin)

    return df


df = load_data()
raw = load_internal_data()

# Map zip codes to boroughs on raw data early so filters work everywhere
zip_borough = df[["zip_code", "borough"]].dropna().drop_duplicates().set_index("zip_code")["borough"].to_dict()
raw["borough"] = raw["delivery_zip_code"].map(zip_borough)

# Header with logo
st.markdown(f"""
<div class="uber-header">
    <img src="data:image/svg+xml;base64,{LOGO_B64}" alt="Uber Eats">
    <div class="uber-header-text">
        <h1>NYC Postal Code Prioritization</h1>
        <p>Growth Strategy & Planning &mdash; Food delivery expansion analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Filter strip (top of page)
st.markdown('<div class="filter-strip">', unsafe_allow_html=True)
fc1, fc2, fc3, fc4 = st.columns([2.5, 3, 1.5, 2])

with fc1:
    boroughs = sorted(df["borough"].dropna().unique())
    sel_boroughs = st.multiselect(
        "Borough", boroughs, default=boroughs, placeholder="All boroughs",
    )
    # If nothing selected, treat as all selected
    if not sel_boroughs:
        sel_boroughs = boroughs

with fc2:
    available_zips = sorted(
        df[df["borough"].isin(sel_boroughs)]["zip_code"].dropna().unique()
    )
    sel_zips = st.multiselect(
        "Zip Code",
        options=[str(z) for z in available_zips],
        default=[],
        placeholder="All zip codes",
    )

with fc3:
    top_n = st.selectbox("Show Top", [10, 15, 20, 30, 50], index=2)

with fc4:
    sort_metric = st.selectbox(
        "Sort By",
        ["Composite Score", "Market Penetration", "Growth Rate", "Coverage Gap", "Delivery Speed"],
    )
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar – Composite weights
with st.sidebar:
    st.markdown("### Composite Weights")
    st.caption("Adjust metric importance. Auto-normalizes to 100 %.")
    w_penetration = st.slider("Orders per Capita", 0, 100, 25, 1, format="%d %%") # Weight for market penetration (inverted orders per capita)
    w_growth = st.slider("Growth Rate", 0, 100, 20, 1, format="%d %%") # Weight for growth rate (HoH % change in orders)
    w_volume = st.slider("Order Volume", 0, 100, 8, 1, format="%d %%") # Weight for absolute order volume (anchors opportunity but kept low to avoid favoring already-served markets)
    w_coverage = st.slider("Coverage Gap", 0, 100, 15, 1, format="%d %%") # Weight for supply gap (potential supply from restaurants not currently on platform)
    w_quality = st.slider("Quality Index", 0, 100, 15, 1, format="%d %%") # Weight for quality index (customer satisfaction)
    w_repeat = st.slider("Repeat Rate", 0, 100, 10, 1, format="%d %%") # Weight for repeat order rate (customer loyalty)
    w_speed = st.slider("Delivery Speed", 0, 100, 7, 1, format="%d %%") # Weight for delivery speed (customer satisfaction)
    total_w = max(w_penetration + w_growth + w_volume + w_coverage + w_quality + w_repeat + w_speed, 1)
    wn_pen = w_penetration / total_w
    wn_gro = w_growth / total_w
    wn_vol = w_volume / total_w
    wn_cov = w_coverage / total_w
    wn_qua = w_quality / total_w
    wn_rep = w_repeat / total_w
    wn_spd = w_speed / total_w
    st.markdown(
        f"**Effective:**  \n"
        f"Penetration `{wn_pen:.0%}` · Growth `{wn_gro:.0%}`  \n"
        f"Volume `{wn_vol:.0%}` · Coverage `{wn_cov:.0%}`  \n"
        f"Quality `{wn_qua:.0%}` · Repeat `{wn_rep:.0%}`  \n"
        f"Speed `{wn_spd:.0%}`"
    )

# Compute composite score — individual metric weights
ror_min, ror_max = df["repeat_order_rate"].min(), df["repeat_order_rate"].max()
df["repeat_rate_norm"] = 100 * (df["repeat_order_rate"] - ror_min) / (ror_max - ror_min)

ov_min, ov_max = df["order_volume"].min(), df["order_volume"].max()
df["volume_norm"] = 100 * (df["order_volume"] - ov_min) / (ov_max - ov_min)

df["composite_score"] = (
    wn_pen * df["penetration_norm"]
    + wn_gro * df["growth_norm"]
    + wn_vol * df["volume_norm"]
    + wn_cov * df["coverage_gap_norm"]
    + wn_qua * df["quality_score_norm"]
    + wn_rep * df["repeat_rate_norm"]
    + wn_spd * df["delivery_speed_score"]
)

# Pillar aggregates for borough chart
df["demand_pillar"] = (wn_pen * df["penetration_norm"] + wn_gro * df["growth_norm"] + wn_vol * df["volume_norm"]) / max(wn_pen + wn_gro + wn_vol, 0.01)
df["supply_pillar"] = (wn_cov * df["coverage_gap_norm"] + wn_qua * df["quality_score_norm"]) / max(wn_cov + wn_qua, 0.01)
df["ops_pillar"] = (wn_rep * df["repeat_rate_norm"] + wn_spd * df["delivery_speed_score"]) / max(wn_rep + wn_spd, 0.01)
df["rank"] = df["composite_score"].rank(ascending=False, method="min", na_option="bottom").astype("Int64")


filt = df[df["borough"].isin(sel_boroughs)].copy()
if sel_zips:
    filt = filt[filt["zip_code"].isin([int(z) for z in sel_zips])]

# 3-tier segmentation using composite score percentiles
p66 = filt["composite_score"].quantile(0.66)
p33 = filt["composite_score"].quantile(0.33)

def classify(row):
    score = row["composite_score"]
    if pd.isna(score):
        return "Low Priority"
    if score >= p66:
        return "High Potential"
    elif score >= p33:
        return "Saturated"
    return "Low Priority"

sort_map = {
    "Composite Score": "composite_score",
    "Market Penetration": "orders_per_1k_residents",
    "Growth Rate": "growth_rate",
    "Coverage Gap": "coverage_gap",
    "Delivery Speed": "delivery_speed_score",
}
filt = filt.sort_values(sort_map[sort_metric], ascending=False)

# Plotly defaults
def uber_layout(**overrides):
    """Return a dict of Plotly layout defaults, merged with overrides."""
    base = dict(
        template="plotly_white",
        font=dict(family=PLOTLY_FONT, color=UBER_BLACK),
        paper_bgcolor=UBER_WHITE,
        plot_bgcolor=UBER_WHITE,
        margin=dict(l=0, r=0, t=35, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    base.update(overrides)
    return base

# KPI cards — sourced from internal order-level data
# Include ALL orders (even unmapped boroughs) when no specific filter is applied
if sel_zips:
    raw_kpi = raw[raw["delivery_zip_code"].isin([int(z) for z in sel_zips])].copy()
elif set(sel_boroughs) == set(boroughs):
    # All boroughs selected → show everything including unmapped zips
    raw_kpi = raw.copy()
else:
    raw_kpi = raw[raw["borough"].isin(sel_boroughs)].copy()

k1, k2, k5, k6, k7 = st.columns(5)
k1.metric("Zip Codes", f"{raw_kpi['delivery_zip_code'].nunique()}")
k2.metric("Total Orders", f"{len(raw_kpi):,}")
k5.metric("Med. Penetration", f"{filt['orders_per_1k_residents'].median():.1f} / 1K")
k6.metric("Avg Growth", f"{filt['growth_rate'].mean():.1f} %")
k7.metric("Avg Delivery", f"{raw_kpi['delivery_time_mins'].mean():.1f} min")

# Framework expander
with st.expander("Prioritization Framework & Core Metrics"):
    st.markdown("""
**Composite score ranks each postal code across seven weighted metrics:**

| Metric | Default Weight | Rationale |
|--------|---------------|-----------|
| **Orders per Capita** | 25 % | Inverted — low penetration in a dense zip = biggest untapped opportunity |
| **Growth Rate** | 20 % | Half-on-half order growth — momentum signal for expansion |
| **Order Volume** | 8 % | Absolute demand — anchor only, kept low to avoid favoring already-served markets |
| **Coverage Gap** | 15 % | Gap between potential supply and current merchants — high gap = acquisition opportunity |
| **Quality Index** | 15 % | Avg inspection score — better restaurants support premium positioning & retention |
| **Repeat Rate** | 10 % | Retention health — loyal customers drive LTV |
| **Delivery Speed** | 7 % | Inverted avg delivery time — fast deliveries sustain the retention flywheel |

*Weights are adjustable in the sidebar and auto-normalize to 100 %.*
    """)

# Top-N Ranking
st.markdown(f'<p class="section-header">Top {top_n} Postal Codes</p>', unsafe_allow_html=True)

top = filt.head(top_n)

display_cols = {
    "rank": "Rank", "zip_code": "Zip Code", "borough": "Borough",
    "composite_score": "Score", "orders_per_1k_residents": "Penetration",
    "growth_rate": "Growth %", "coverage_gap": "Coverage Gap",
    "avg_quality_index": "Quality", "avg_delivery_time": "Delivery (min)",
    "order_volume": "Orders", "population": "Population",
}

st.dataframe(
    top[list(display_cols.keys())]
    .rename(columns=display_cols)
    .style.format({
        "Score": "{:.1f}", "Penetration": "{:.1f}", "Growth %": "{:.1f}",
        "Coverage Gap": "{:.1f}", "Quality": "{:.1f}", "Delivery (min)": "{:.1f}",
        "Orders": "{:,.0f}", "Population": "{:,.0f}",
    })
    .background_gradient(subset=["Score"], cmap="Greens"),
    use_container_width=True, hide_index=True,
    height=min(len(top) * 38 + 40, 500),
)

filt["segment"] = filt.apply(classify, axis=1)

# Segment Summary
st.markdown('<p class="section-header">Segment Summary</p>', unsafe_allow_html=True)

seg_col1, seg_col2 = st.columns([3, 2])

with seg_col1:
    seg_summary = (
        filt.groupby("segment")
        .agg(
            zip_count=("zip_code", "count"),
            avg_composite=("composite_score", "mean"),
            total_orders=("order_volume", "sum"),
            avg_penetration=("orders_per_1k_residents", "mean"),
            avg_growth=("growth_rate", "mean"),
        )
        .reset_index()
        .sort_values("avg_composite", ascending=False)
    )
    st.dataframe(
        seg_summary.rename(columns={
            "segment": "Segment", "zip_count": "Zips",
            "avg_composite": "Avg Score", "total_orders": "Orders",
            "avg_penetration": "Penetration", "avg_growth": "Growth %",
        }).style.format({
            "Avg Score": "{:.1f}", "Orders": "{:,.0f}",
            "Penetration": "{:.1f}", "Growth %": "{:.1f}",
        }),
        use_container_width=True, hide_index=True,
    )

with seg_col2:
    st.markdown("""
**Reading the segments**
- **High Potential** — Top third by composite score. Low penetration, strong growth, room to acquire merchants. Prioritize investment.
- **Saturated** — Middle third. Established markets with limited upside. Maintain current operations, optimize selectively.
- **Low Priority** — Bottom third. High penetration, low growth, supply already covered. Monitor but limit new investment.
    """)

# Score Breakdown & Quadrant
st.markdown('<p class="section-header">Score Breakdown & Market Quadrant</p>', unsafe_allow_html=True)

col_bar, col_scatter = st.columns(2)

with col_bar:
    bar_data = top.dropna(subset=["composite_score"]).sort_values("composite_score", ascending=True).copy()
    bar_data["zip_str"] = bar_data["zip_code"].astype(int).astype(str)
    if not bar_data.empty:
        fig_bar = px.bar(
            bar_data, x="composite_score", y="zip_str", orientation="h",
            color="borough", text="composite_score",
            color_discrete_map=BOROUGH_COLORS,
            labels={"composite_score": "Composite Score", "zip_str": ""},
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside", marker_line_width=0)
        fig_bar.update_layout(
            **uber_layout(height=480, yaxis=dict(type="category"),
            margin=dict(l=0, r=30, t=35, b=0),
            title=dict(text=f"Composite Score - Top {top_n}", font=dict(size=13, color=UBER_BLACK))),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with col_scatter:
    vol_by_boro = (
        filt.groupby("borough")["order_volume"].sum()
        .reset_index().sort_values("order_volume", ascending=False)
    )
    fig_vol_boro = px.bar(
        vol_by_boro, x="borough", y="order_volume", color="borough",
        text="order_volume", color_discrete_map=BOROUGH_COLORS,
        labels={"order_volume": "Total Orders", "borough": ""},
    )
    fig_vol_boro.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
    fig_vol_boro.update_layout(**uber_layout(height=400, showlegend=False,
                               title=dict(text="Total Order Volume by Borough", font=dict(size=13, color=UBER_BLACK))))
    st.plotly_chart(fig_vol_boro, use_container_width=True)


# Pillar Performance by Borough
st.markdown('<p class="section-header">Pillar Performance by Borough</p>', unsafe_allow_html=True)

borough_agg = (
    filt.groupby("borough")[["demand_pillar", "supply_pillar", "ops_pillar", "composite_score"]]
    .mean().reset_index().sort_values("composite_score", ascending=False)
)

fig_pillars = go.Figure()
for pillar, color, label in [
    ("demand_pillar", UBER_GREEN, "Demand"),
    ("supply_pillar", UBER_BLUE, "Supply"),
    ("ops_pillar", UBER_ORANGE, "Operations"),
]:
    fig_pillars.add_trace(go.Bar(
        name=label, x=borough_agg["borough"], y=borough_agg[pillar],
        marker_color=color, marker_line_width=0,
    ))
fig_pillars.update_layout(
    **uber_layout(barmode="group", height=380,
    yaxis_title="Avg Score (0-100)",
    margin=dict(l=0, r=0, t=10, b=0)),
)
st.plotly_chart(fig_pillars, use_container_width=True)


# Apply same borough / zip filters to raw data
raw_filt = raw[raw["borough"].isin(sel_boroughs)].copy()
if sel_zips:
    raw_filt = raw_filt[raw_filt["delivery_zip_code"].isin([int(z) for z in sel_zips])]

    
# Merchant & Supply Analysis
st.markdown('<p class="section-header">Merchant & Supply Analysis</p>', unsafe_allow_html=True)

mc1, mc2 = st.columns(2)

with mc1:
    fig_sd = px.scatter(
        filt, x="total_restaurants", y="order_volume",
        color="borough", hover_name="zip_code", trendline="ols",
        color_discrete_map=BOROUGH_COLORS,
        labels={"total_restaurants": "Total Restaurants", "order_volume": "Order Volume"},
    )
    fig_sd.update_layout(**uber_layout(height=420,
                         title=dict(text="Restaurant Count vs Order Volume", font=dict(size=13, color=UBER_BLACK))))
    st.plotly_chart(fig_sd, use_container_width=True)

# Merchant density by borough
merch_boro = (
    filt.groupby("borough").agg(
        total_restaurants=("total_restaurants", "sum"),
        avg_coverage_gap=("coverage_gap", "mean"),
        avg_quality=("avg_quality_index", "mean"),
    ).reset_index().sort_values("total_restaurants", ascending=False)
)

with mc2:
    fig_merch = px.bar(
        merch_boro, x="borough", y="total_restaurants", color="borough",
        text="total_restaurants", color_discrete_map=BOROUGH_COLORS,
        labels={"total_restaurants": "Restaurants", "borough": ""},
    )
    fig_merch.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
    fig_merch.update_layout(**uber_layout(height=380, showlegend=False,
                            title=dict(text="Total Restaurants by Borough", font=dict(size=13, color=UBER_BLACK))))
    st.plotly_chart(fig_merch, use_container_width=True)


# Eater Cohort Analysis
st.markdown('<p class="section-header">Eater Acquisition & Retention</p>', unsafe_allow_html=True)

ea1, ea2 = st.columns(2)

with ea1:
    eaters = raw_filt.drop_duplicates(subset="eater_id")[["eater_id", "eater_account_creation_date", "borough"]].copy()
    eaters["signup_month"] = eaters["eater_account_creation_date"].dt.to_period("M").dt.start_time
    monthly_eaters = eaters.groupby("signup_month").size().reset_index(name="new_eaters")
    monthly_eaters["cumulative"] = monthly_eaters["new_eaters"].cumsum()
    fig_eater = go.Figure()
    fig_eater.add_trace(go.Bar(
        x=monthly_eaters["signup_month"], y=monthly_eaters["new_eaters"],
        name="New Eaters", marker_color=UBER_BLUE, marker_line_width=0,
    ))
    fig_eater.add_trace(go.Scatter(
        x=monthly_eaters["signup_month"], y=monthly_eaters["cumulative"],
        name="Cumulative", line=dict(color=UBER_BLACK, width=2), yaxis="y2",
    ))
    fig_eater.update_layout(
        **uber_layout(height=420,
        title=dict(text="Eater Signups Over Time", font=dict(size=13, color=UBER_BLACK)),
        yaxis=dict(title="New Eaters / Month"),
        yaxis2=dict(title="Cumulative", overlaying="y", side="right", showgrid=False)),
    )
    st.plotly_chart(fig_eater, use_container_width=True)

with ea2:
    orders_per_eater = raw_filt.groupby("eater_id").size().reset_index(name="order_count")
    freq_bins = [1, 2, 3, 5, 10, 50, orders_per_eater["order_count"].max() + 1]
    freq_labels = ["1", "2", "3-4", "5-9", "10-49", "50+"]
    orders_per_eater["frequency"] = pd.cut(orders_per_eater["order_count"], bins=freq_bins, labels=freq_labels, right=False)
    freq_dist = orders_per_eater["frequency"].value_counts().reset_index()
    freq_dist.columns = ["frequency", "eater_count"]
    freq_dist["frequency"] = pd.Categorical(freq_dist["frequency"], categories=freq_labels, ordered=True)
    freq_dist = freq_dist.sort_values("frequency")
    fig_freq = px.bar(
        freq_dist, x="frequency", y="eater_count", text="eater_count",
        labels={"frequency": "Orders per Eater", "eater_count": "Eaters"},
    )
    fig_freq.update_traces(marker_color=UBER_ORANGE, texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
    fig_freq.update_layout(**uber_layout(height=420,
                           title=dict(text="Eater Order Frequency Distribution", font=dict(size=13, color=UBER_BLACK))))
    st.plotly_chart(fig_freq, use_container_width=True)