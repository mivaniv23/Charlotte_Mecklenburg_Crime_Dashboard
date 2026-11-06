# Charlotte-Mecklenburg Crime Data Dashboard

An interactive Streamlit dashboard exploring reported CMPD incident patterns over time, by offense type, and across Neighborhood Profile Areas (NPAs).

## Published application

**Streamlit app URL:** https://charlottemecklenburgcrimedashboard-75dtpuhvt7clyicjsqtdxv.streamlit.app

## Project purpose

This project makes public CMPD incident data easier for Charlotte-Mecklenburg residents, community groups, and people interested in local public safety to explore. Users can filter the report date range, offense type, and neighborhood area.

## Dataset and source

- **Dataset:** CMPD Incidents
- **Publisher:** City of Charlotte open data
- **Source page:** https://data.charlottenc.gov/datasets/charlotte::cmpd-incidents-1
- **Prepared dashboard data:** `dashboard_data.csv`
- **Records included:** 472,252 cleaned incident records
- **Date range:** January 1, 2017 – October 26, 2026
- **Fields included:** `incident_date`, `offense_type`, and `area` (NPA)

The original source export contained many additional fields. The deployment CSV keeps only the fields required by this dashboard, avoiding unnecessary incident identifiers and location coordinates.

## Data preparation

The supplied analysis notebook:
1. Removes exact duplicate rows.
2. Parses the report date and removes records without a valid report date.
3. Excludes 800-series NIBRS codes, which the notebook identifies as non-criminal report types.
4. Keeps one row per incident report ID when an ID field is available.
5. Prepares the date, offense description, and Neighborhood Profile Area fields for analysis.

## Questions explored

1. How do reported crime counts change over time?
2. Which offense types are reported most often?
3. Which areas have the highest numbers of reported incidents?

## Dashboard features

- Date range filter
- Offense type filter
- Neighborhood Profile Area (NPA) filter
- Adjustable number of categories shown in the ranking charts
- Three summary metrics that respond to the selected filters
- Monthly incident trend line chart
- Offense type ranking bar chart
- NPA ranking bar chart

## Run locally

1. Clone this repository.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Deploy with Streamlit Community Cloud

1. Push these four files to a **public GitHub repository**: `app.py`, `dashboard_data.csv`, `requirements.txt`, and `README.md`.
2. Sign in to https://share.streamlit.io/ using GitHub.
3. Select **Create app**, choose this repository and branch, and set the main file path to `app.py`.
4. Deploy the app.
5. Open the public app URL and test the date, offense, and NPA filters. Confirm the metrics and all three charts update.
6. Replace the placeholder Streamlit app URL near the top of this README with the published URL, then commit the update.

## Important interpretation note

The dashboard displays counts of reported incidents, not population-adjusted crime rates. Higher counts do not automatically mean a neighborhood is more dangerous. Population, business activity, visitors, and reporting patterns can influence totals.

## AI-use statement

ChatGPT assisted with Streamlit application structure, dashboard code, and project documentation. The dataset selection, analysis questions, data preparation, and interpretation are based on the student's project work. The student is responsible for reviewing, understanding, testing, and presenting the final application.
