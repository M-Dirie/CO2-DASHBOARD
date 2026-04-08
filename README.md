# Task 2 – Global Fossil CO2 Emissions Interactive Dashboard

## Overview
This project presents an interactive dashboard built for Task 2 of the Data Visualisation assessment. The dashboard explores the EDGAR fossil CO2 dataset and allows users to compare countries, trends, sectors, per-capita emissions, and GDP intensity in one interface.

The goal of the dashboard is to turn a complex workbook into a clear and useful analytical tool that supports exploration and comparison.

## Main Goal
The main story of the dashboard is that global fossil CO2 emissions are highly concentrated, but countries differ in more than total emissions alone. The dashboard shows differences in:
- overall emission scale
- historical trends
- sector contribution
- emissions per person
- emissions relative to GDP

This makes it possible to look beyond simple rankings and understand emissions from different perspectives.

## Questions the Dashboard Helps Answer
The dashboard supports questions such as:

- Which countries are the largest contributors to fossil CO2 emissions?
- How have emissions changed over time for major countries?
- Which sectors contribute most to emissions in a selected country?
- Which countries have high per-capita emissions?
- Which countries have high GDP intensity?
- Are there clear outliers or unusual patterns in the data?

## Audience
The dashboard is designed for:
- course assessors
- students
- general users interested in climate data
- people who want a simple but meaningful emissions comparison tool

The design aims to keep the dashboard professional, readable, and easy to navigate.

## Design Approach
The dashboard was built in **Streamlit** using **Python**, **Pandas**, and **Plotly**.

These tools were selected because they allow:
- interactive filtering
- multiple coordinated charts
- clean online deployment
- easy exploration by year and country

The layout was designed to move from overview to deeper analysis. This helps users understand the main message first and then explore details.

## Main Dashboard Features
The dashboard includes:
- summary KPI cards
- country comparison views
- time-series trend analysis
- sector composition analysis
- per-capita and GDP intensity comparison
- supporting contextual views
- shared filters for year and country selection

## Data Cleaning Summary
The EDGAR workbook needed preparation before it could be used in the dashboard.

The main cleaning steps were:
- loading data from multiple sheets
- reshaping wide year columns into long format
- creating a clean `Year` field
- removing aggregate rows such as `GLOBAL TOTAL`, `WORLD`, and `EU27` from country-level analysis
- dropping missing values where necessary
- merging totals, per-capita, and GDP-intensity data for combined analysis
- keeping LULUCF as supporting context rather than mixing it directly into country fossil CO2 comparisons

These steps were important because they made the dashboard more accurate and improved the quality of country comparisons.

## Public Dashboard Link
Add your deployed Streamlit link here:

https://co2-dashboard-h88x5nwev8gwwtdg4rlsif.streamlit.app/

## Software Used
- Python
- Streamlit
- Pandas
- Plotly
- VS Code

## Files Included
This task submission usually includes:
- `app.py`
- `requirements.txt`
- the EDGAR Excel workbook
- dashboard screenshots
- written report in the final PDF

## Notes
The dashboard was designed to remain understandable without the report. The written report explains the goal, design choices, visual encodings, communication approach, and limitations.

## Author
**Mursal Abdidahir Dirie**
