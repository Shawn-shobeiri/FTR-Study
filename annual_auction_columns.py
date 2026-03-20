"""
Class to ensure AuctionBidsAndOffers and MarketResults tables in auction_results/annual
and auction_results/monthly have NumberOfHours and MWh columns. If the check fails,
adds them using CRR Time of Use.
"""
from pathlib import Path
from typing import Optional

import pandas as pd

# Default paths (relative to this file)
DEFAULT_ANNUAL_DIR = (Path(__file__).parent / "auction_results" / "annual").resolve()
DEFAULT_MONTHLY_DIR = (Path(__file__).parent / "auction_results" / "monthly").resolve()
DEFAULT_ASSET_DIR = Path(__file__).parent / "asset"
DEFAULT_TOU_FILENAME = "CRR-Time-of-Use-Hours_2024-2028.xlsx"

PATTERNS = ("AuctionBidsAndOffers", "MarketResults")

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


def _col(df: pd.DataFrame, *candidates: str) -> Optional[str]:
    """Return first column name in df that is in candidates, or None."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


class AnnualAuctionColumnsEnsurer:
    """
    If AuctionBidsAndOffers and MarketResults tables in auction_results/annual and
    auction_results/monthly do not have NumberOfHours and MWh columns, add them
    using StartDate, EndDate, TimeOfUse and the CRR Time of Use Excel file.
    MWh = MW * NumberOfHours.
    """

    def __init__(
        self,
        annual_dir: Optional[Path] = None,
        monthly_dir: Optional[Path] = None,
        asset_dir: Optional[Path] = None,
        tou_filename: str = DEFAULT_TOU_FILENAME,
    ) -> None:
        self.annual_dir = Path(annual_dir) if annual_dir is not None else DEFAULT_ANNUAL_DIR
        self.monthly_dir = Path(monthly_dir) if monthly_dir is not None else DEFAULT_MONTHLY_DIR
        self.asset_dir = Path(asset_dir) if asset_dir is not None else DEFAULT_ASSET_DIR
        self.tou_path = self.asset_dir / tou_filename

    def _data_dirs(self) -> list[Path]:
        """Return list of data directories to process (annual, monthly)."""
        return [self.annual_dir, self.monthly_dir]

    def check(self) -> bool:
        """
        Return True if every AuctionBidsAndOffers and MarketResults CSV in each
        subfolder of annual_dir and monthly_dir already has NumberOfHours and MWh.
        Returns True if there are no such files in either directory.
        """
        for data_dir in self._data_dirs():
            if not data_dir.is_dir():
                continue
            for folder in data_dir.iterdir():
                if not folder.is_dir() or folder.name == "combined":
                    continue
                for csv_path in folder.glob("*.csv"):
                    if not any(p in csv_path.name for p in PATTERNS):
                        continue
                    try:
                        df = pd.read_csv(csv_path, nrows=0)
                    except Exception:
                        return False
                    if "NumberOfHours" not in df.columns or "MWh" not in df.columns:
                        return False
        return True

    def run(self) -> None:
        """
        If check() is False, add NumberOfHours and MWh to each AuctionBidsAndOffers
        and MarketResults CSV in auction_results/annual and auction_results/monthly
        subfolders.
        """
        if self.check():
            return
        tou_df = self._load_tou_df()
        if tou_df is None:
            raise FileNotFoundError(
                f"CRR Time of Use file not found or invalid: {self.tou_path}"
            )
        for data_dir in self._data_dirs():
            if not data_dir.is_dir():
                continue
            for folder in sorted(data_dir.iterdir()):
                if not folder.is_dir() or folder.name == "combined":
                    continue
                for csv_path in sorted(folder.glob("*.csv")):
                    if not any(p in csv_path.name for p in PATTERNS):
                        continue
                    self._add_columns_to_csv(csv_path, tou_df)

    def _load_tou_df(self) -> Optional[pd.DataFrame]:
        """Load CRR Time of Use table from asset Excel."""
        if not self.tou_path.exists():
            return None
        need = {"Year", "Month", "OffPeak", "PeakWD", "PeakWE", "Total"}
        try:
            xl = pd.ExcelFile(self.tou_path)
            for sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, header=1)
                if not df.empty and need.issubset(df.columns):
                    return df
        except Exception:
            pass
        return None

    def _compute_number_of_hours(
        self, df: pd.DataFrame, tou_df: pd.DataFrame
    ) -> pd.Series:
        """Compute NumberOfHours for each row using StartDate, EndDate, TimeOfUse and TOU table."""
        start_col = _col(df, "StartDate", "Start Date")
        end_col = _col(df, "EndDate", "End Date")
        tou_val_col = _col(df, "TimeOfUse", "Time Of Use", "TOU")
        if not start_col or not end_col or not tou_val_col:
            return pd.Series(index=df.index, dtype=float)
        tou_lookup = tou_df.set_index(["Year", "Month"])
        starts = pd.to_datetime(df[start_col], errors="coerce")
        ends = pd.to_datetime(df[end_col], errors="coerce")

        def norm_tou(val: str) -> str:
            s = str(val).strip().lower().replace(" ", "")
            if "-" in s and "peak" in s:
                s = "offpeak"
            return TOU_TO_COL.get(s) or TOU_TO_COL.get(s.replace("-", ""), "Total")

        tou_cols = df[tou_val_col].map(norm_tou)
        rows_meta: list[tuple[int, pd.Timestamp, pd.Timestamp, str]] = []
        for i in df.index:
            start, end = starts.loc[i], ends.loc[i]
            if pd.isna(start) or pd.isna(end) or start > end:
                continue
            rows_meta.append((i, start, end, tou_cols.loc[i]))
        if not rows_meta:
            return pd.Series(index=df.index, dtype=float)

        expanded: list[tuple[int, int, str, float]] = []
        for i, start, end, tcol in rows_meta:
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
                        hrs = float(tou_lookup.loc[(year, month_name), tcol])
                    except (KeyError, TypeError):
                        hrs = 0.0
                    expanded.append((i, year, month_name, (overlap_days / days_in_month) * hrs))
                cur = month_end + pd.Timedelta(days=1)

        if not expanded:
            return pd.Series(index=df.index, dtype=float)
        exp_df = pd.DataFrame(expanded, columns=["_idx", "Year", "Month", "_hours"])
        hours_by_row = exp_df.groupby("_idx", as_index=False)["_hours"].sum()
        out = hours_by_row.set_index("_idx")["_hours"].reindex(df.index).astype(float)
        return out

    def _add_columns_to_csv(self, csv_path: Path, tou_df: pd.DataFrame) -> bool:
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
            return False
        start_col = _col(df, "StartDate", "Start Date")
        end_col = _col(df, "EndDate", "End Date")
        tou_col = _col(df, "TimeOfUse", "Time Of Use", "TOU")
        mw_col = _col(df, "MW", "mw_amount", "MWAmount", "mw")
        if not start_col or not end_col or not tou_col:
            return False
        df["NumberOfHours"] = self._compute_number_of_hours(df, tou_df)
        if mw_col:
            df["MWh"] = pd.to_numeric(df[mw_col], errors="coerce") * df["NumberOfHours"]
        else:
            df["MWh"] = float("nan")
        try:
            df.to_csv(csv_path, index=False)
            return True
        except Exception:
            return False

    def recompute_csv(self, csv_path: Path) -> bool:
        """
        Recompute NumberOfHours and MWh for a CSV and overwrite it (e.g. when values were wrong).
        Returns True if the file was updated.
        """
        csv_path = Path(csv_path)
        try:
            df = pd.read_csv(csv_path)
        except Exception:
            return False
        if df.empty:
            return False
        df = df.drop(columns=["NumberOfHours", "MWh"], errors="ignore")
        tou_df = self._load_tou_df()
        if tou_df is None:
            return False
        start_col = _col(df, "StartDate", "Start Date")
        end_col = _col(df, "EndDate", "End Date")
        tou_col = _col(df, "TimeOfUse", "Time Of Use", "TOU")
        mw_col = _col(df, "MW", "mw_amount", "MWAmount", "mw")
        if not start_col or not end_col or not tou_col:
            return False
        df["NumberOfHours"] = self._compute_number_of_hours(df, tou_df)
        if mw_col:
            df["MWh"] = pd.to_numeric(df[mw_col], errors="coerce") * df["NumberOfHours"]
        else:
            df["MWh"] = float("nan")
        try:
            df.to_csv(csv_path, index=False)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    ensurer = AnnualAuctionColumnsEnsurer()
    if ensurer.check():
        print("Check passed: all tables already have NumberOfHours and MWh.")
    else:
        print("Check failed: adding NumberOfHours and MWh to tables...")
        ensurer.run()
        print("Done.")
