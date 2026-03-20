"""
Build master parquet tables by combining all CSVs of the same report type from
auction_results/annual and auction_results/monthly. Each row gets a report_date
column derived from the folder name (part after last '_' as YYYY-MM-DD).
"""
from pathlib import Path
from typing import Optional

import pandas as pd

# Default paths
DEFAULT_ANNUAL_DIR = (Path(__file__).parent / "auction_results" / "annual").resolve()
DEFAULT_MONTHLY_DIR = (Path(__file__).parent / "auction_results" / "monthly").resolve()

REPORT_TYPES = [
    "Auction Bids and Offers",
    "Base Loading",
    "Binding Constraint",
    "Auction Results",
    "Shadow Prices",
]
REPORT_TYPE_FILE_PATTERNS = {
    "Auction Bids and Offers": "AuctionBidsAndOffers",
    "Base Loading": "BaseLoading",
    "Binding Constraint": "BindingConstraint",
    "Auction Results": "MarketResults",
    "Shadow Prices": "SourceAndSinkShadowPrices",
}


def _report_date_from_folder_name(folder_name: str) -> str:
    """
    Extract report date from folder name (part after last '_') as YYYY-MM-DD.
    E.g. 20241st6_20230601 -> 2023-06-01, 20252nd6_20230406 -> 2023-04-06.
    """
    if "_" not in folder_name:
        return ""
    suffix = folder_name.split("_")[-1]
    if len(suffix) == 8 and suffix.isdigit():
        y, m, d = suffix[:4], suffix[4:6], suffix[6:8]
        return f"{y}-{m}-{d}"
    return suffix


def _report_type_to_parquet_name(report_type: str) -> str:
    """Convert report type label to parquet filename (e.g. 'Auction Bids and Offers' -> 'Auction_Bids_and_Offers.parquet')."""
    safe = report_type.replace(" ", "_") + ".parquet"
    return safe


class MasterParquetBuilder:
    """
    Combines all CSVs of the same report type (from annual or monthly subfolders)
    into one master parquet per report type, with a report_date column for each row.
    """

    def __init__(
        self,
        annual_dir: Optional[Path] = None,
        monthly_dir: Optional[Path] = None,
    ) -> None:
        self.annual_dir = Path(annual_dir) if annual_dir is not None else DEFAULT_ANNUAL_DIR
        self.monthly_dir = Path(monthly_dir) if monthly_dir is not None else DEFAULT_MONTHLY_DIR

    def _data_dirs(self) -> list[tuple[str, Path]]:
        """Return [(source_label, path), ...] for annual and monthly."""
        return [("annual", self.annual_dir), ("monthly", self.monthly_dir)]

    def _build_one_report_type(
        self, source: str, base_dir: Path, report_type: str
    ) -> Optional[pd.DataFrame]:
        """
        Load all CSVs for this report type from all subfolders of base_dir,
        add report_date, and return one combined DataFrame. Returns None if no data.
        """
        pattern = REPORT_TYPE_FILE_PATTERNS.get(report_type, "")
        if not pattern:
            return None
        if not base_dir.is_dir():
            return None
        folders = sorted(
            d.name for d in base_dir.iterdir() if d.is_dir() and d.name != "combined"
        )
        frames = []
        for folder_name in folders:
            folder_path = base_dir / folder_name
            report_date = _report_date_from_folder_name(folder_name)
            for csv_path in sorted(folder_path.glob("*.csv")):
                if pattern not in csv_path.name:
                    continue
                try:
                    df = pd.read_csv(csv_path)
                    if df.empty:
                        continue
                    df = df.copy()
                    df["report_date"] = report_date
                    frames.append(df)
                except Exception:
                    continue
        if not frames:
            return None
        return pd.concat(frames, ignore_index=True)

    def build(self) -> None:
        """
        For each (annual, monthly) and each report type, build one master parquet
        in <source>/combined/<ReportType>.parquet with report_date on every row.
        """
        for source, base_dir in self._data_dirs():
            if not base_dir.is_dir():
                continue
            combined_dir = base_dir / "combined"
            combined_dir.mkdir(parents=True, exist_ok=True)
            for report_type in REPORT_TYPES:
                df = self._build_one_report_type(source, base_dir, report_type)
                if df is None:
                    continue
                out_path = combined_dir / _report_type_to_parquet_name(report_type)
                try:
                    df.to_parquet(out_path, index=False)
                except Exception:
                    pass

    def get_master_path(self, report_type: str, source: str = "annual") -> Path:
        """Return the path to the master parquet for this report type and source."""
        base = self.annual_dir if source == "annual" else self.monthly_dir
        return base / "combined" / _report_type_to_parquet_name(report_type)


if __name__ == "__main__":
    builder = MasterParquetBuilder()
    builder.build()
    print("Master parquet tables written to auction_results/annual/combined/ and auction_results/monthly/combined/")
