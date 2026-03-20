"""
One-time script: add NumberOfHours and MWh to AuctionBidsAndOffers and MarketResults
CSVs in each folder under auction_results/annual. Uses asset/CRR-Time-of-Use-Hours_2025-2028.xlsx
for the hours lookup.
"""
from pathlib import Path

import pandas as pd

ASSET_DIR = Path(__file__).parent / "asset"
ANNUAL_AUCTION_DIR = (Path(__file__).parent / "auction_results" / "annual").resolve()
TOU_XLSX = ASSET_DIR / "CRR-Time-of-Use-Hours_2025-2028.xlsx"

PATTERNS = ("AuctionBidsAndOffers", "MarketResults")


def _col(df: pd.DataFrame, *candidates: str) -> str | None:
    """Return first column name in df that is in candidates, or None."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def load_tou_df() -> pd.DataFrame | None:
    """Load CRR Time of Use table from asset Excel. First sheet with Year, Month, OffPeak, PeakWD, PeakWE, Total."""
    if not TOU_XLSX.exists():
        return None
    need = {"Year", "Month", "OffPeak", "PeakWD", "PeakWE", "Total"}
    try:
        xl = pd.ExcelFile(TOU_XLSX)
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet, header=1)
            if not df.empty and need.issubset(df.columns):
                return df
    except Exception:
        pass
    return None


MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
TOU_TO_COL = {
    "offpeak": "OffPeak", "off-peak": "OffPeak", "off_peak": "OffPeak",
    "peakwd": "PeakWD", "peak_wd": "PeakWD",
    "peakwe": "PeakWE", "peak_we": "PeakWE",
    "total": "Total", "24 hour": "Total", "all": "Total",
}


def _normalize_tou(tou_val: str) -> str:
    s = str(tou_val).strip().lower().replace(" ", "")
    if "-" in s and "peak" in s:
        s = "offpeak"
    return TOU_TO_COL.get(s) or TOU_TO_COL.get(s.replace("-", ""), "Total")


def compute_number_of_hours(df: pd.DataFrame, tou_df: pd.DataFrame) -> pd.Series:
    """
    Compute NumberOfHours for each row using StartDate, EndDate, TimeOfUse
    and the CRR Time of Use table.
    """
    start_col = _col(df, "StartDate", "Start Date")
    end_col = _col(df, "EndDate", "End Date")
    tou_val_col = _col(df, "TimeOfUse", "Time Of Use", "TOU")
    if not start_col or not end_col or not tou_val_col:
        return pd.Series(index=df.index, dtype=float)
    tou_lookup = tou_df.set_index(["Year", "Month"])
    idx_start = df.columns.get_loc(start_col)
    idx_end = df.columns.get_loc(end_col)
    idx_tou = df.columns.get_loc(tou_val_col)
    results = []
    for row in df.itertuples(index=True):
        i = row.Index
        try:
            start = pd.to_datetime(row[idx_start + 1], errors="coerce")  # +1 because Index is first
            end = pd.to_datetime(row[idx_end + 1], errors="coerce")
        except Exception:
            results.append((i, float("nan")))
            continue
        if pd.isna(start) or pd.isna(end) or start > end:
            results.append((i, float("nan")))
            continue
        tou_val = str(row[idx_tou + 1]).strip().lower().replace(" ", "")
        if "-" in tou_val and "peak" in tou_val:
            tou_val = "offpeak"
        tcol = TOU_TO_COL.get(tou_val) or TOU_TO_COL.get(tou_val.replace("-", ""), "Total")
        total_hours = 0.0
        cur = start
        while cur <= end:
            year, month = cur.year, cur.month
            month_name = MONTH_NAMES[month - 1]
            month_start = pd.Timestamp(year=year, month=month, day=1)
            month_end = month_start + pd.offsets.MonthEnd(0)
            overlap_start = max(start, month_start)
            overlap_end = min(end, month_end)
            if overlap_start <= overlap_end:
                overlap_days = (overlap_end - overlap_start).days + 1
                days_in_month = (month_end - month_start).days + 1
                try:
                    hrs = tou_lookup.loc[(year, month_name), tcol]
                except (KeyError, TypeError):
                    hrs = 0.0
                total_hours += (overlap_days / days_in_month) * float(hrs)
            cur = month_end + pd.Timedelta(days=1)
        results.append((i, total_hours))
    out = pd.Series(index=df.index, dtype=float)
    for i, h in results:
        out.loc[i] = h
    return out


def process_csv(csv_path: Path, tou_df: pd.DataFrame) -> bool:
    """
    Add NumberOfHours and MWh to the CSV if missing. Returns True if file was modified.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return False
    if df.empty:
        return False
    if "NumberOfHours" in df.columns and "MWh" in df.columns:
        return False  # already done
    start_col = _col(df, "StartDate", "Start Date")
    end_col = _col(df, "EndDate", "End Date")
    tou_col = _col(df, "TimeOfUse", "Time Of Use", "TOU")
    mw_col = _col(df, "MW", "mw_amount", "MWAmount", "mw")
    if not start_col or not end_col or not tou_col:
        return False
    df["NumberOfHours"] = compute_number_of_hours(df, tou_df)
    if mw_col:
        df["MWh"] = pd.to_numeric(df[mw_col], errors="coerce") * df["NumberOfHours"]
    else:
        df["MWh"] = float("nan")
    try:
        df.to_csv(csv_path, index=False)
        return True
    except Exception:
        return False


def main() -> None:
    tou_df = load_tou_df()
    if tou_df is None:
        print("ERROR: Could not load CRR Time of Use from", TOU_XLSX)
        return
    print("Loaded TOU table:", list(tou_df.columns))
    if not ANNUAL_AUCTION_DIR.is_dir():
        print("ERROR: annual dir not found:", ANNUAL_AUCTION_DIR)
        return
    modified = 0
    skipped = 0
    for folder in sorted(ANNUAL_AUCTION_DIR.iterdir()):
        if not folder.is_dir() or folder.name == "combined":
            continue
        for csv_path in sorted(folder.glob("*.csv")):
            if not any(p in csv_path.name for p in PATTERNS):
                continue
            if process_csv(csv_path, tou_df):
                modified += 1
                print("  Modified:", csv_path.relative_to(ANNUAL_AUCTION_DIR))
            else:
                skipped += 1
    print("Done. Modified:", modified, "Skipped or unchanged:", skipped)


if __name__ == "__main__":
    main()
