"""
Extract ERCOT auction result ZIPs into per-ZIP subfolders for combined parquet build.

AnnualAuctionResultsExtractor and MonthlyAuctionResultsExtractor unzip any .zip in the
given directory into a subfolder (named from the ZIP stem or the single top-level folder
inside the ZIP), so the app can find CSVs in each folder and build combined parquets.
"""

import zipfile
from pathlib import Path


def _extract_zip(zip_path: Path, base_dir: Path) -> Path | None:
    """
    Unzip zip_path into base_dir. If the ZIP has a single top-level folder, extract
    to base_dir so that folder becomes base_dir/<name>; otherwise extract to base_dir/<zip_stem>.
    Returns the path to the extracted folder, or None on failure.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            if not names:
                return None
            top = set()
            for n in names:
                n = n.replace("\\", "/").strip("/")
                if not n:
                    continue
                first = n.split("/")[0]
                top.add(first)
            if len(top) == 1:
                first_name = list(top)[0].rstrip("/")
                if any(n.startswith(first_name + "/") or n == first_name for n in names):
                    zf.extractall(base_dir)
                    return base_dir / first_name
            out_folder_name = zip_path.stem
            out_path = base_dir / out_folder_name
            out_path.mkdir(parents=True, exist_ok=True)
            zf.extractall(out_path)
            return out_path
    except Exception:
        return None


class AnnualAuctionResultsExtractor:
    """Unzip annual auction result ZIPs in the given directory into subfolders."""

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)

    def run(self) -> None:
        for zip_path in sorted(self.directory.glob("*.zip")):
            _extract_zip(zip_path, self.directory)


class MonthlyAuctionResultsExtractor:
    """Unzip monthly auction result ZIPs in the given directory into subfolders."""

    def __init__(self, directory: Path) -> None:
        self.directory = Path(directory)

    def run(self) -> None:
        for zip_path in sorted(self.directory.glob("*.zip")):
            _extract_zip(zip_path, self.directory)
