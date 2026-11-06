import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Charlotte-Mecklenburg Crime Dashboard",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "dashboard_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["incident_date"])
    df["offense_type"] = df["offense_type"].fillna("Unknown").astype(str)
    df["area"] = df["area"].astype("Int64").astype(str)
    df = df.dropna(subset=["incident_date"])
    return df

df = load_data()

st.title("Charlotte-Mecklenburg Crime Data Dashboard")
st.markdown(
    """
    Explore reported CMPD incident patterns over time, by offense type, and
    across Neighborhood Profile Areas (NPAs). Use the filters to focus on a
    date range, selected offenses, or specific neighborhoods.

    **Intended audience:** Charlotte-Mecklenburg residents, community groups,
    and people interested in local public safety.
    """
)

st.info(
    "This dashboard counts reported incidents in the selected dataset. "
    "Counts are not crime rates and do not adjust for population, visitors, "
    "or differences in reporting."
)

# Sidebar controls
st.sidebar.header("Explore the data")
min_date = df["incident_date"].min().date()
max_date = df["incident_date"].max().date()

date_range = st.sidebar.date_input(
    "Report date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Choose the beginning and ending report dates.",
)

offense_options = sorted(df["offense_type"].unique().tolist())
selected_offenses = st.sidebar.multiselect(
    "Offense type",
    options=offense_options,
    default=[],
    help="Leave empty to include every offense type.",
)

area_options = sorted(df["area"].unique().tolist(), key=lambda x: int(x))
selected_areas = st.sidebar.multiselect(
    "Neighborhood Profile Area (NPA)",
    options=area_options,
    default=[],
    help="Leave empty to include every NPA.",
)

top_n = st.sidebar.slider(
    "Number of categories shown in ranking charts",
    min_value=5,
    max_value=20,
    value=12,
)

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.warning("Select both a start date and an end date to display the dashboard.")
    st.stop()

start_date, end_date = date_range
if start_date > end_date:
    st.error("The start date must be on or before the end date.")
    st.stop()

filtered = df[
    (df["incident_date"].dt.date >= start_date)
    & (df["incident_date"].dt.date <= end_date)
].copy()

if selected_offenses:
    filtered = filtered[filtered["offense_type"].isin(selected_offenses)]
if selected_areas:
    filtered = filtered[filtered["area"].isin(selected_areas)]

st.caption(
    f"Showing {len(filtered):,} reported incidents from "
    f"{start_date:%b %d, %Y} through {end_date:%b %d, %Y}."
)

# Summary metrics update with the filters.
total_incidents = len(filtered)
offense_count = filtered["offense_type"].nunique()
area_count = filtered["area"].nunique()
top_offense = (
    filtered["offense_type"].value_counts().index[0]
    if total_incidents else "—"
)

m1, m2, m3 = st.columns(3)
m1.metric("Reported incidents", f"{total_incidents:,}")
m2.metric("Offense types represented", f"{offense_count:,}")
m3.metric("Neighborhood areas represented", f"{area_count:,}")

if filtered.empty:
    st.warning("No incidents match these filters. Try widening the date range or clearing a filter.")
    st.stop()

st.subheader("1. How do reported incident counts change over time?")
monthly = (
    filtered.assign(month=filtered["incident_date"].dt.to_period("M").dt.to_timestamp())
    .groupby("month")
    .size()
    .reset_index(name="Reported incidents")
    .sort_values("month")
)
fig_month = px.line(
    monthly,
    x="month",
    y="Reported incidents",
    markers=True,
    title="Reported CMPD Incidents by Month",
    labels={"month": "Month reported", "Reported incidents": "Number of incidents"},
)
fig_month.update_layout(hovermode="x unified")
st.plotly_chart(fig_month, use_container_width=True)
st.caption(
    "Each point represents the number of incidents reported during that month. "
    "The trend reflects report dates, not necessarily the dates when incidents began."
)

left, right = st.columns(2)

with left:
    st.subheader("2. Which offense types are reported most often?")
    offense_counts = (
        filtered.groupby("offense_type")
        .size()
        .reset_index(name="Reported incidents")
        .sort_values("Reported incidents", ascending=False)
        .head(top_n)
        .sort_values("Reported incidents", ascending=True)
    )
    fig_offense = px.bar(
        offense_counts,
        x="Reported incidents",
        y="offense_type",
        orientation="h",
        title=f"Top {min(top_n, len(offense_counts))} Offense Types",
        labels={"offense_type": "Offense type"},
    )
    st.plotly_chart(fig_offense, use_container_width=True)
    st.caption(
        f"The most common offense in the current selection is **{top_offense}**. "
        "These are report counts, not measures of individual risk."
    )

with right:
    st.subheader("3. Which neighborhoods have the most reports?")
    area_counts = (
        filtered.groupby("area")
        .size()
        .reset_index(name="Reported incidents")
        .sort_values("Reported incidents", ascending=False)
        .head(top_n)
        .sort_values("Reported incidents", ascending=True)
    )
    area_counts["NPA"] = "NPA " + area_counts["area"]
    fig_area = px.bar(
        area_counts,
        x="Reported incidents",
        y="NPA",
        orientation="h",
        title=f"Top {min(top_n, len(area_counts))} Neighborhood Profile Areas",
        labels={"NPA": "Neighborhood Profile Area"},
    )
    st.plotly_chart(fig_area, use_container_width=True)
    st.caption(
        "Areas with more reports have higher totals in this dataset. "
        "Population, business activity, and visitors can affect these totals."
    )

with st.expander("About the data and its limitations"):
    st.markdown(
        """
        - **Source:** City of Charlotte, CMPD Incidents open-data dataset.
        - **Date field:** The dashboard uses the date the incident was reported.
        - **Area field:** Neighborhood Profile Area (NPA).
        - **Preparation:** The supplied analysis notebook removes exact duplicate
          rows, excludes records with 800-series NIBRS codes (identified in the
          notebook as non-criminal report types), removes records without a valid
          report date, and keeps one row per incident report ID where available.
        - **Interpretation:** Incident counts are not population-adjusted crime
          rates. They do not explain why incidents happen and may reflect
          reporting patterns as well as underlying events.
        """
    )

st.markdown("---")
st.caption("CIS 3400 • Project 1 • Charlotte-Mecklenburg Crime Data Dashboard")
