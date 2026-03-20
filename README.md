# ERCOT CRR Auction Historical Analysis

A Streamlit app for analyzing historical Congestion Revenue Rights (CRR) auction results from ERCOT.

## Overview

CRRs are financial instruments that hedge or speculate on transmission congestion in the ERCOT Day-Ahead Market. This app provides:

- **Price trends** – Clearing price evolution over time by path and Time of Use
- **Path analysis** – Total MW, average prices, and auction value by path
- **Market overview** – Source–sink flow visualization, Obligation vs Option breakdown
- **Raw data** – Full dataset with filters

## Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Data

Upload your own CRR auction results as CSV (from ERCOT Annual or Monthly Auction Results).

### Expected CSV Columns

| Column        | Description                    |
|---------------|--------------------------------|
| auction_date  | Date of auction (YYYY-MM-DD)   |
| auction_type  | Annual or Monthly              |
| source_node   | Source settlement point        |
| sink_node     | Sink settlement point          |
| path_name     | Path identifier                |
| mw_amount     | Awarded MW                     |
| clearing_price| Clearing price ($/MW)          |
| time_of_use   | 24Hour, PeakWD, PeakWE, OffPeak|
| crr_type      | Obligation or Option           |

The app will try to map common column name variations (e.g., `SourceNode` → `source_node`).

### ERCOT Data Products

- [Annual Auction Results](https://www.ercot.com/mp/data-products/data-product-details?id=NP7-802-M) (NP7-802-M)
- [Monthly Auction Results](https://www.ercot.com/mp/data-products/data-product-details?id=NP7-803-M) (NP7-803-M)

Download CSV/XML from the ERCOT Market Participant Data portal.

## Project Structure

```
FTR/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```
