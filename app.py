import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Fossil CO₂ Emissions Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  .main {
    background: linear-gradient(180deg, #07101d 0%, #091729 100%);
  }

  .block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
  }

  [data-testid="stSidebar"] {
    background: #0b1626;
    border-right: 1px solid rgba(120, 160, 200, 0.15);
  }

  [data-testid="stSidebar"] * {
    color: #d7e7f6 !important;
  }

  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label,
  [data-testid="stSidebar"] .stSlider label,
  [data-testid="stSidebar"] .stCheckbox label {
    color: #9ab7d2 !important;
    font-size: 0.82rem;
    font-weight: 600;
  }

  .hero-block {
    background: linear-gradient(135deg, #0c1a2d 0%, #0f2743 55%, #10324f 100%);
    border: 1px solid rgba(88, 155, 220, 0.22);
    border-radius: 24px;
    padding: 1.7rem 2rem 1.4rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.18);
  }

  .hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.35rem;
    line-height: 1.1;
    color: #f2f7ff;
    margin: 0 0 0.45rem 0;
  }

  .hero-sub {
    font-size: 0.98rem;
    color: #b6d1ea;
    margin: 0.2rem 0 0.35rem 0;
  }

  .hero-meta {
    font-size: 0.95rem;
    color: #d7e7f6;
    margin: 0;
  }

  .metric-card {
    background: linear-gradient(180deg, rgba(12, 24, 42, 0.92) 0%, rgba(10, 20, 36, 0.95) 100%);
    border: 1px solid rgba(88, 155, 220, 0.18);
    border-radius: 22px;
    padding: 1.15rem 1.35rem;
    min-height: 136px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
  }

  .metric-label {
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #88aacc;
    margin-bottom: 0.65rem;
    font-weight: 600;
  }

  .metric-value {
    font-size: 2rem;
    line-height: 1.05;
    font-weight: 700;
    color: #39bdfc;
    margin-bottom: 0.45rem;
  }

  .metric-unit {
    font-size: 0.95rem;
    color: #b6d1ea;
  }

  .section-box {
    background: rgba(12, 24, 42, 0.72);
    border: 1px solid rgba(88, 155, 220, 0.15);
    border-radius: 22px;
    padding: 1.15rem 1.4rem;
    margin-bottom: 1rem;
  }

  .section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.45rem;
    color: #f2f7ff;
    margin: 0 0 0.25rem 0;
  }

  .section-sub {
    font-size: 0.95rem;
    color: #a9c5de;
    margin: 0;
  }

  .insight-box {
    background: rgba(11, 23, 38, 0.82);
    border: 1px solid rgba(88, 155, 220, 0.12);
    border-radius: 18px;
    padding: 0.95rem 1.1rem;
    color: #d7e7f6;
  }

  .footer {
    text-align: center;
    color: #6d8aa8;
    font-size: 0.78rem;
    padding-top: 0.6rem;
  }

  .stTabs [data-baseweb="tab-list"] {
    gap: 0.45rem;
    background: rgba(11, 23, 38, 0.7);
    border-radius: 18px;
    padding: 0.3rem;
    border: 1px solid rgba(88, 155, 220, 0.12);
  }

  .stTabs [data-baseweb="tab"] {
    border-radius: 14px;
    color: #9dbad4;
    padding: 0.6rem 1rem;
    font-weight: 600;
  }

  .stTabs [aria-selected="true"] {
    background: rgba(28, 78, 130, 0.65) !important;
    color: #46c3ff !important;
  }

  hr {
    border: none;
    border-top: 1px solid rgba(88, 155, 220, 0.15);
    margin: 1rem 0 1.15rem 0;
  }

  .stMultiSelect > div > div,
  .stSelectbox > div > div {
    background: #0b1320 !important;
    border: 1px solid rgba(88, 155, 220, 0.16) !important;
    border-radius: 12px !important;
  }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
DATA_FILE = "EDGARv7.0_FT2021_fossil_CO2_booklet_2022.xlsx"
AGGREGATES = {"EU27", "EU28", "GLOBAL TOTAL", "ANNEXI", "NONANNEXI", "AIR", "SEA"}

SECTOR_COLORS = {
    "Power Industry": "#4fc3f7",
    "Transport": "#81d4fa",
    "Buildings": "#0288d1",
    "Other industrial combustion": "#26c6da",
    "Other sectors": "#80cbc4",
}

REGION_COLORS = {
    "East Asia": "#4fc3f7",
    "North America": "#ef9a9a",
    "Europe": "#80cbc4",
    "South Asia": "#ffcc80",
    "Latin America": "#ce93d8",
    "Middle East": "#ff8a65",
    "Oceania": "#a5d6a7",
    "Africa": "#f48fb1",
    "Southeast Asia": "#b39ddb",
    "Other": "#708090",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#d7e7f6", size=12),
    xaxis=dict(gridcolor="rgba(120,160,200,0.12)", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="rgba(120,160,200,0.12)", showgrid=True, zeroline=False),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#d7e7f6"),
        title_font=dict(color="#d7e7f6"),
    ),
)

REGION_MAP = {
    "CHN": "East Asia",
    "JPN": "East Asia",
    "KOR": "East Asia",
    "TWN": "East Asia",
    "USA": "North America",
    "CAN": "North America",
    "MEX": "North America",
    "DEU": "Europe",
    "GBR": "Europe",
    "FRA": "Europe",
    "ITA": "Europe",
    "RUS": "Europe",
    "ESP": "Europe",
    "POL": "Europe",
    "NLD": "Europe",
    "TUR": "Europe",
    "UKR": "Europe",
    "IND": "South Asia",
    "PAK": "South Asia",
    "BGD": "South Asia",
    "BRA": "Latin America",
    "ARG": "Latin America",
    "COL": "Latin America",
    "SAU": "Middle East",
    "IRN": "Middle East",
    "IRQ": "Middle East",
    "AUS": "Oceania",
    "NZL": "Oceania",
    "ZAF": "Africa",
    "NGA": "Africa",
    "EGY": "Africa",
    "IDN": "Southeast Asia",
    "THA": "Southeast Asia",
    "VNM": "Southeast Asia",
    "MYS": "Southeast Asia",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def show_section_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="section-box">
            <div class="section-title">{title}</div>
            <p class="section-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_chart_layout(fig, title=None, height=420, margin=None, **extra_layout):
    layout = CHART_LAYOUT.copy()
    layout.update(
        dict(
            title=title,
            height=height,
            margin=margin if margin is not None else dict(l=8, r=8, t=52, b=8),
        )
    )
    layout.update(extra_layout)
    fig.update_layout(**layout)
    return fig


def melt_years(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    year_cols = [c for c in df.columns if str(c).isdigit()]
    id_cols = [c for c in df.columns if not str(c).isdigit()]
    out = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="Year", value_name=value_name)
    out["Year"] = pd.to_numeric(out["Year"], errors="coerce")
    out = out.dropna(subset=["Year"])
    out["Year"] = out["Year"].astype(int)
    return out


def filter_countries(df: pd.DataFrame) -> pd.DataFrame:
    code_col = "EDGAR Country Code"
    country_col = "Country"
    if code_col not in df.columns or country_col not in df.columns:
        return df.copy()

    filtered = df.copy()
    filtered[code_col] = filtered[code_col].astype(str).str.strip()
    filtered[country_col] = filtered[country_col].astype(str).str.strip()

    mask = (
        filtered[code_col].str.len() == 3
    ) & (~filtered[code_col].isin(AGGREGATES)) & (filtered[country_col].str.lower() != "nan")
    return filtered.loc[mask].copy()


def safe_top_row(df: pd.DataFrame, value_col: str):
    df2 = df.dropna(subset=[value_col]).copy()
    if df2.empty:
        return None
    return df2.loc[df2[value_col].idxmax()]


def safe_bottom_row(df: pd.DataFrame, value_col: str):
    df2 = df.dropna(subset=[value_col]).copy()
    if df2.empty:
        return None
    return df2.loc[df2[value_col].idxmin()]



# DATA LOADING
@st.cache_data
def load_data():
    try:
        totals = pd.read_excel(DATA_FILE, sheet_name="fossil_CO2_totals_by_country")
        sectors = pd.read_excel(DATA_FILE, sheet_name="fossil_CO2_by_sector_and_countr")
        gdp = pd.read_excel(DATA_FILE, sheet_name="fossil_CO2_per_GDP_by_country")
        capita = pd.read_excel(DATA_FILE, sheet_name="fossil_CO2_per_capita_by_countr")
        lulucf = pd.read_excel(DATA_FILE, sheet_name="LULUCF by macro regions")
        return totals, sectors, gdp, capita, lulucf
    except FileNotFoundError:
        st.error(
            f"Data file '{DATA_FILE}' was not found. Place the Excel file in the same folder as app.py."
        )
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


totals, sectors, gdp, capita, lulucf = load_data()

totals_m = filter_countries(melt_years(totals, "CO2_Mt"))
capita_m = filter_countries(melt_years(capita, "CO2_cap"))
gdp_m = filter_countries(melt_years(gdp, "CO2_GDP"))
sectors_m = filter_countries(melt_years(sectors, "CO2_Mt"))

YEAR_RANGE = (int(totals_m["Year"].min()), int(totals_m["Year"].max()))
DEFAULT_YEAR = 2021 if 2021 in totals_m["Year"].unique() else YEAR_RANGE[1]

global_total = totals_m.groupby("Year", as_index=False)["CO2_Mt"].sum()

all_countries = sorted(totals_m["Country"].dropna().astype(str).unique().tolist())

# SIDEBAR

with st.sidebar:
    st.markdown("## Dashboard Controls")
    st.markdown(
        """
        <div style="color:#9ab7d2; font-size:0.96rem; line-height:1.65; margin-bottom:0.9rem;">
        Explore emissions trends, geography, sectors, and intensity metrics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_year = st.slider(
        "Reference year",
        min_value=YEAR_RANGE[0],
        max_value=YEAR_RANGE[1],
        value=DEFAULT_YEAR,
        step=1,
    )

    top_n = st.selectbox("Top emitters to show", [5, 10, 15, 20], index=1)

    default_countries = ["China", "United States", "India", "Russia", "Germany"]
    trend_countries = st.multiselect(
        "Countries for trend comparison",
        options=all_countries,
        default=[c for c in default_countries if c in all_countries],
    )

    sector_country = st.selectbox(
        "Country for sector view",
        options=all_countries,
        index=all_countries.index("China") if "China" in all_countries else 0,
    )

    show_preview = st.checkbox("Show filtered data preview", value=False)


# HEADER

st.markdown(
    """
    <div class="hero-block">
        <div class="hero-title">Global Fossil CO₂ Emissions Dashboard</div>
        <p class="hero-sub">
            A professional analytical dashboard built with Streamlit and Plotly for country-level emissions exploration.
        </p>
        <p class="hero-meta">
            Coverage: 1970–2021 &nbsp;•&nbsp; Country-level totals, sector composition, per-capita footprint, GDP intensity, and LULUCF context
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# KPI ROW

yr_data = totals_m[totals_m["Year"] == selected_year].copy()
cap_yr = capita_m[capita_m["Year"] == selected_year].copy()
gdp_yr = gdp_m[gdp_m["Year"] == selected_year].copy()

total_yr = yr_data["CO2_Mt"].sum()

top_emitter_row = safe_top_row(yr_data, "CO2_Mt")
top_cap_row = safe_top_row(cap_yr, "CO2_cap")

gdp_positive = gdp_yr[gdp_yr["CO2_GDP"] > 0].copy()
best_eff_row = safe_bottom_row(gdp_positive, "CO2_GDP")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Global Emissions</div>
            <div class="metric-value">{total_yr:,.0f}</div>
            <div class="metric-unit">Mt CO₂ in {selected_year}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    largest_country = top_emitter_row["Country"] if top_emitter_row is not None else "N/A"
    largest_value = top_emitter_row["CO2_Mt"] if top_emitter_row is not None else 0
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Largest Emitter</div>
            <div class="metric-value" style="font-size:1.75rem;">{largest_country}</div>
            <div class="metric-unit">{largest_value:,.1f} Mt CO₂</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    cap_country = top_cap_row["Country"] if top_cap_row is not None else "N/A"
    cap_value = top_cap_row["CO2_cap"] if top_cap_row is not None else 0
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Highest Per Capita</div>
            <div class="metric-value" style="font-size:1.75rem;">{cap_country}</div>
            <div class="metric-unit">{cap_value:,.2f} t CO₂/person</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    eff_country = best_eff_row["Country"] if best_eff_row is not None else "N/A"
    eff_value = best_eff_row["CO2_GDP"] if best_eff_row is not None else 0
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Lowest GDP Intensity</div>
            <div class="metric-value" style="font-size:1.75rem;">{eff_country}</div>
            <div class="metric-unit">{eff_value:,.3f} t CO₂/kUSD GDP</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# TABS
tab1, tab2, tab3, tab4 = st.tabs(
    ["🗺️ Overview", "📈 Trends", "🏭 Sectors", "⚖️ Intensity & Footprint"]
)


# TAB 1: OVERVIEW

with tab1:
    show_section_header(
        "Global overview",
        f"Spatial distribution and rankings for {selected_year}. Total countries shown: {yr_data['Country'].nunique()}",
    )

    map_data = yr_data.dropna(subset=["EDGAR Country Code", "Country", "CO2_Mt"]).copy()
    map_data = map_data[map_data["EDGAR Country Code"].astype(str).str.len() == 3]

    if map_data.empty:
        st.warning("No map data available for the selected year.")
    else:
        fig_map = px.choropleth(
            map_data,
            locations="EDGAR Country Code",
            color="CO2_Mt",
            hover_name="Country",
            hover_data={"CO2_Mt": ":,.1f", "EDGAR Country Code": False},
            color_continuous_scale=[
                [0.00, "#0d2137"],
                [0.10, "#0c3a60"],
                [0.30, "#0071a4"],
                [0.60, "#00a0d1"],
                [0.80, "#4fc3f7"],
                [1.00, "#e0f7ff"],
            ],
            labels={"CO2_Mt": "Mt CO₂"},
        )

        apply_chart_layout(
            fig_map,
            title=f"Fossil CO₂ Emissions by Country — {selected_year}",
            height=460,
            margin=dict(l=0, r=0, t=56, b=0),
            coloraxis_colorbar=dict(
                title="Mt CO₂",
                tickfont=dict(color="#d7e7f6"),
                title_font=dict(color="#d7e7f6"),
                bgcolor="rgba(0,0,0,0)",
            ),
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                landcolor="#132a3e",
                oceancolor="#091522",
                showocean=True,
                showframe=False,
                coastlinecolor="#1e3a55",
                countrycolor="#1e3a55",
                showlakes=False,
                projection_type="natural earth",
            ),
        )

        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    col_a, col_b = st.columns([1.65, 1])

    with col_a:
        top_data = map_data.nlargest(top_n, "CO2_Mt").sort_values("CO2_Mt", ascending=True)

        if top_data.empty:
            st.warning("No ranking data available for the selected year.")
        else:
            fig_bar = go.Figure(
                go.Bar(
                    x=top_data["CO2_Mt"],
                    y=top_data["Country"],
                    orientation="h",
                    marker=dict(
                        color=top_data["CO2_Mt"],
                        colorscale=[[0, "#0d5b8a"], [1, "#45c4ff"]],
                        showscale=False,
                    ),
                    text=top_data["CO2_Mt"].round(0).astype(int).astype(str) + " Mt",
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>%{x:,.1f} Mt CO₂<extra></extra>",
                )
            )

            apply_chart_layout(
                fig_bar,
                title=f"Top {top_n} Emitters in {selected_year}",
                height=max(340, top_n * 36),
                margin=dict(l=8, r=50, t=56, b=8),
                xaxis_title="Mt CO₂ per year",
                yaxis_title=None,
            )

            st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        top3 = map_data.nlargest(3, "CO2_Mt")[["Country", "CO2_Mt"]].copy()
        share_top10 = (
            map_data.nlargest(10, "CO2_Mt")["CO2_Mt"].sum() / map_data["CO2_Mt"].sum() * 100
            if map_data["CO2_Mt"].sum() > 0
            else 0
        )
        avg_country = map_data["CO2_Mt"].mean()

        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### Key observations")
        if not top3.empty:
            st.write(
                f"• The largest emitter in {selected_year} is **{top3.iloc[0]['Country']}**, contributing **{top3.iloc[0]['CO2_Mt']:,.1f} Mt CO₂**."
            )
        st.write(f"• The **top 10 countries** account for approximately **{share_top10:.1f}%** of total emissions shown.")
        st.write(f"• The **average country-level total** in the selected year is **{avg_country:,.1f} Mt CO₂**.")
        if len(top3) == 3:
            st.write(
                f"• The top three emitters are **{top3.iloc[0]['Country']}**, **{top3.iloc[1]['Country']}**, and **{top3.iloc[2]['Country']}**."
            )
        st.markdown("</div>", unsafe_allow_html=True)


# TAB 2: TRENDS
with tab2:
    show_section_header(
        "Emissions over time",
        "Track long-term emissions trajectories for selected countries and compare them with the global total.",
    )

    col_a, col_b = st.columns([1.7, 1])

    with col_a:
        if trend_countries:
            trend_df = totals_m[totals_m["Country"].isin(trend_countries)].copy()
            fig_line = px.line(
                trend_df,
                x="Year",
                y="CO2_Mt",
                color="Country",
                labels={"CO2_Mt": "Mt CO₂ per year", "Year": "Year"},
                color_discrete_sequence=[
                    "#4fc3f7",
                    "#81d4fa",
                    "#0288d1",
                    "#26c6da",
                    "#80cbc4",
                    "#b3e5fc",
                    "#e0f7ff",
                    "#006064",
                ],
            )
            fig_line.update_traces(line_width=2.4)
            fig_line.add_vline(
                x=selected_year,
                line_dash="dot",
                line_color="#46c3ff",
                opacity=0.6,
                annotation_text=str(selected_year),
                annotation_font_color="#46c3ff",
            )

            apply_chart_layout(
                fig_line,
                title="Country Emissions Trend Comparison",
                height=430,
                xaxis_title="Year",
                yaxis_title="Mt CO₂ per year",
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Select at least one country in the sidebar to view trend comparisons.")

    with col_b:
        fig_global = go.Figure(
            go.Scatter(
                x=global_total["Year"],
                y=global_total["CO2_Mt"],
                fill="tozeroy",
                mode="lines",
                line=dict(color="#4fc3f7", width=2.4),
                fillcolor="rgba(79,195,247,0.16)",
                hovertemplate="<b>%{x}</b><br>%{y:,.0f} Mt CO₂<extra></extra>",
                name="Global total",
            )
        )
        fig_global.add_vline(
            x=selected_year,
            line_dash="dot",
            line_color="#ff8a80",
            opacity=0.7,
        )

        apply_chart_layout(
            fig_global,
            title="Global Emissions Trajectory",
            height=430,
            xaxis_title="Year",
            yaxis_title="Mt CO₂ per year",
        )
        st.plotly_chart(fig_global, use_container_width=True)

    st.markdown("---")

    if trend_countries:
        rows = []
        for country in trend_countries:
            cdf = totals_m[totals_m["Country"] == country].sort_values("Year")
            val_1990 = cdf.loc[cdf["Year"] == 1990, "CO2_Mt"]
            val_sel = cdf.loc[cdf["Year"] == selected_year, "CO2_Mt"]

            if not val_1990.empty and not val_sel.empty and float(val_1990.iloc[0]) > 0:
                pct_change = (float(val_sel.iloc[0]) - float(val_1990.iloc[0])) / float(val_1990.iloc[0]) * 100
                rows.append(
                    {
                        "Country": country,
                        "1990 (Mt)": round(float(val_1990.iloc[0]), 1),
                        f"{selected_year} (Mt)": round(float(val_sel.iloc[0]), 1),
                        "Change vs 1990 (%)": round(pct_change, 1),
                    }
                )

        if rows:
            summary_df = pd.DataFrame(rows).sort_values("Change vs 1990 (%)", ascending=False)
            st.subheader("Change summary")
            st.dataframe(summary_df, use_container_width=True, hide_index=True)


# TAB 3: SECTORS

with tab3:
    show_section_header(
        "Sector breakdown",
        f"Understand which sectors drive emissions in {sector_country}, and compare sector composition across leading emitters.",
    )

    sc_df = sectors_m[sectors_m["Country"] == sector_country].copy()
    sc_df = sc_df.dropna(subset=["Sector", "Year", "CO2_Mt"])

    col_left, col_right = st.columns([1.7, 1])

    with col_left:
        if sc_df.empty:
            st.warning("No sector data available for the selected country.")
        else:
            fig_stack = go.Figure()
            sector_list = [s for s in sc_df["Sector"].dropna().unique().tolist()]

            for i, sec in enumerate(sector_list):
                sdata = sc_df[sc_df["Sector"] == sec].sort_values("Year")
                fig_stack.add_trace(
                    go.Scatter(
                        x=sdata["Year"],
                        y=sdata["CO2_Mt"],
                        mode="lines",
                        name=sec,
                        stackgroup="one",
                        line=dict(width=0.6),
                        fillcolor=list(SECTOR_COLORS.values())[i % len(SECTOR_COLORS)],
                        hovertemplate=f"<b>{sec}</b><br>%{{x}}: %{{y:,.2f}} Mt CO₂<extra></extra>",
                    )
                )

            fig_stack.add_vline(
                x=selected_year,
                line_dash="dot",
                line_color="#ff8a80",
                opacity=0.7,
                annotation_text=str(selected_year),
                annotation_font_color="#ff8a80",
            )

            apply_chart_layout(
                fig_stack,
                title=f"{sector_country}: Emissions by Sector Over Time",
                height=430,
                xaxis_title="Year",
                yaxis_title="Mt CO₂ per year",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(size=11, color="#d7e7f6"),
                ),
            )
            st.plotly_chart(fig_stack, use_container_width=True)

    with col_right:
        sc_year = sc_df[sc_df["Year"] == selected_year].copy()
        sc_year = sc_year.sort_values("CO2_Mt", ascending=False)

        if sc_year.empty:
            st.warning("No sector share data available for the selected year.")
        else:
            fig_pie = go.Figure(
                go.Pie(
                    labels=sc_year["Sector"],
                    values=sc_year["CO2_Mt"],
                    hole=0.54,
                    marker=dict(colors=[SECTOR_COLORS.get(s, "#4fc3f7") for s in sc_year["Sector"]]),
                    hovertemplate="<b>%{label}</b><br>%{value:,.2f} Mt CO₂<br>%{percent}<extra></extra>",
                    textinfo="percent",
                )
            )

            apply_chart_layout(
                fig_pie,
                title=f"{sector_country}: Sector Share in {selected_year}",
                height=430,
                showlegend=True,
            )

            fig_pie.add_annotation(
                text=f"<b>{sc_year['CO2_Mt'].sum():,.1f}</b><br><span style='font-size:10px'>Mt CO₂</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=14, color="#d7e7f6"),
                xref="paper",
                yref="paper",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    top10_countries = (
        totals_m[totals_m["Year"] == selected_year]
        .nlargest(10, "CO2_Mt")["Country"]
        .dropna()
        .tolist()
    )

    sec_top10 = sectors_m[
        (sectors_m["Year"] == selected_year) & (sectors_m["Country"].isin(top10_countries))
    ].copy()

    if not sec_top10.empty:
        fig_grouped = px.bar(
            sec_top10,
            x="Country",
            y="CO2_Mt",
            color="Sector",
            barmode="stack",
            color_discrete_map=SECTOR_COLORS,
            labels={"CO2_Mt": "Mt CO₂", "Country": "Country"},
        )

        apply_chart_layout(
            fig_grouped,
            title=f"Sector Composition of Top 10 Emitters — {selected_year}",
            height=390,
            xaxis_title=None,
            yaxis_title="Mt CO₂ per year",
        )
        st.plotly_chart(fig_grouped, use_container_width=True)


# TAB 4: INTENSITY & FOOTPRINT

with tab4:
    show_section_header(
        "Intensity and footprint analysis",
        f"Bubble size represents total emissions in {selected_year}. This view compares economic carbon intensity with per-capita emissions.",
    )

    t = totals_m[totals_m["Year"] == selected_year][["Country", "EDGAR Country Code", "CO2_Mt"]].copy()
    cp = capita_m[capita_m["Year"] == selected_year][["Country", "CO2_cap"]].copy()
    gp = gdp_m[gdp_m["Year"] == selected_year][["Country", "CO2_GDP"]].copy()

    merged = t.merge(cp, on="Country", how="inner").merge(gp, on="Country", how="inner")
    merged = merged.dropna(subset=["CO2_Mt", "CO2_cap", "CO2_GDP"])
    merged = merged[(merged["CO2_Mt"] > 0) & (merged["CO2_GDP"] > 0)]
    merged["Region"] = merged["EDGAR Country Code"].map(REGION_MAP).fillna("Other")

    if merged.empty:
        st.warning("No merged intensity data available for the selected year.")
    else:
        fig_bubble = px.scatter(
            merged,
            x="CO2_GDP",
            y="CO2_cap",
            size="CO2_Mt",
            color="Region",
            color_discrete_map=REGION_COLORS,
            hover_name="Country",
            hover_data={
                "CO2_Mt": ":,.1f",
                "CO2_cap": ":,.2f",
                "CO2_GDP": ":,.3f",
                "EDGAR Country Code": False,
            },
            labels={
                "CO2_GDP": "Carbon Intensity (t CO₂ / kUSD GDP)",
                "CO2_cap": "Per-Capita Emissions (t CO₂ / person)",
                "CO2_Mt": "Total Emissions (Mt)",
            },
            log_x=True,
            size_max=55,
        )

        med_x = merged["CO2_GDP"].median()
        med_y = merged["CO2_cap"].median()

        fig_bubble.add_vline(
            x=med_x,
            line_dash="dot",
            line_color="#7d8ea3",
            opacity=0.7,
            annotation_text="Median intensity",
            annotation_font_color="#7d8ea3",
        )
        fig_bubble.add_hline(
            y=med_y,
            line_dash="dot",
            line_color="#7d8ea3",
            opacity=0.7,
            annotation_text="Median per capita",
            annotation_font_color="#7d8ea3",
        )

        apply_chart_layout(
            fig_bubble,
            title=f"Carbon Intensity vs Per-Capita Emissions — {selected_year}",
            height=520,
            xaxis_title="Carbon Intensity (t CO₂ / kUSD GDP) — log scale",
            yaxis_title="Per-Capita Emissions (t CO₂ / person)",
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")

    st.subheader("LULUCF regional context")
    st.caption("Negative values indicate land-use carbon sinks, while positive values indicate net emissions from land use.")

    try:
        lulucf_long = lulucf.copy()
        year_cols = [c for c in lulucf_long.columns if str(c).isdigit()]
        lulucf_long = lulucf_long.melt(
            id_vars=["Sector", "region", "substance"],
            value_vars=year_cols,
            var_name="Year",
            value_name="CO2_Mt",
        )
        lulucf_long["Year"] = pd.to_numeric(lulucf_long["Year"], errors="coerce")
        lulucf_long = lulucf_long.dropna(subset=["Year", "CO2_Mt"])
        lulucf_long["Year"] = lulucf_long["Year"].astype(int)

        lulucf_year = min(selected_year, int(lulucf_long["Year"].max()))
        lulucf_sel = lulucf_long[lulucf_long["Year"] == lulucf_year].copy()

        if not lulucf_sel.empty:
            fig_lu = px.bar(
                lulucf_sel.sort_values("CO2_Mt"),
                x="CO2_Mt",
                y="region",
                orientation="h",
                color="CO2_Mt",
                color_continuous_scale=[[0, "#ef9a9a"], [0.5, "#b0bec5"], [1, "#80cbc4"]],
                labels={"CO2_Mt": "Net CO₂ (Mt)", "region": "Region"},
            )

            apply_chart_layout(
                fig_lu,
                title=f"Net LULUCF Emissions by Region — {lulucf_year}",
                height=360,
                xaxis_title="Mt CO₂ (negative = carbon sink)",
                yaxis_title=None,
                coloraxis_showscale=False,
            )

            fig_lu.add_vline(x=0, line_color="#7d8ea3", line_width=1)
            st.plotly_chart(fig_lu, use_container_width=True)
        else:
            st.info("No LULUCF data available for the selected year.")
    except Exception as e:
        st.warning(f"LULUCF view could not be rendered: {e}")


#DATA PREVIEW (i did it optional, to be compatible)

if show_preview:
    st.markdown("---")
    st.subheader("Filtered data preview")
    preview_df = totals_m[totals_m["Year"] == selected_year][
        ["Country", "EDGAR Country Code", "CO2_Mt"]
    ].sort_values("CO2_Mt", ascending=False)
    st.dataframe(preview_df, use_container_width=True, hide_index=True)


# FOOTER

st.markdown("---")
st.markdown(
    """
    <div class="footer">
        EDGAR v7.0 · Crippa et al. (2022) · European Commission Joint Research Centre · Dashboard built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)