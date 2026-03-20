"""
ERCOT CRR Auction Results.

Streamlit app for Activity Calendar, Auction Results, and Shaping.
Uses OOP structure with data loaders, views, and a main app controller.
"""

import re

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Callable, Optional

from auction_results_extractor import (
    AnnualAuctionResultsExtractor,
    MonthlyAuctionResultsExtractor,
)
from annual_auction_columns import AnnualAuctionColumnsEnsurer

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

ASSET_DIR = Path(__file__).parent / "asset"
ANNUAL_AUCTION_DIR = (Path(__file__).parent / "auction_results" / "annual").resolve()
MONTHLY_AUCTION_DIR = (Path(__file__).parent / "auction_results" / "monthly").resolve()
PATH_SPECIFIC_ADDERS_ANNUAL_DIR = (
    Path(__file__).parent / "auction_results" / "path_specific_adders" / "annual"
).resolve()
PATH_SPECIFIC_ADDERS_MONTHLY_DIR = (
    Path(__file__).parent / "auction_results" / "path_specific_adders" / "monthly"
).resolve()
AUCTION_SOURCE_OPTIONS = ["Annual", "Monthly"]
REPORT_TYPES = [
    "Auction Bids and Offers",
    "Base Loading",
    "Binding Constraint",
    "Auction Results",
    "Shadow Prices",
]
# Map report type label to substring to match in CSV filenames (e.g. Common_MarketResults_...)
REPORT_TYPE_FILE_PATTERNS = {
    "Auction Bids and Offers": "AuctionBidsAndOffers",
    "Base Loading": "BaseLoading",
    "Binding Constraint": "BindingConstraint",
    "Auction Results": "MarketResults",
    "Shadow Prices": "SourceAndSinkShadowPrices",
}
ACTIVITY_CALENDAR_SHEETS = [
    "CRR Activity Calendar",
    "Calendar Protocol References",
]
CRR_CSV_COLUMN_MAP = {
    "auction_date": ["auction_date", "AuctionDate", "auction date", "date"],
    "auction_type": ["auction_type", "AuctionType", "auction type"],
    "source_node": ["source_node", "SourceNode", "Source", "source", "source node"],
    "sink_node": ["sink_node", "SinkNode", "Sink", "sink", "sink node"],
    "path_name": ["path_name", "PathName", "path", "path name"],
    "mw_amount": ["mw_amount", "MW", "mw", "MWAmount", "mw amount"],
    "clearing_price": [
        "clearing_price",
        "ClearingPrice",
        "price",
        "clearing price",
    ],
    "time_of_use": ["time_of_use", "TimeOfUse", "TOU", "time of use"],
    "crr_type": ["crr_type", "CRRType", "type", "crr type"],
}
CHART_HEIGHT_LINE = 450
CHART_HEIGHT_BAR = 450
CHART_HEIGHT_TREEMAP = 500
CHART_HEIGHT_PIE = 400

# -----------------------------------------------------------------------------
# Page config and styling (run once at import)
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="ERCOT CRR Auction Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
<style>
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Data loaders
# -----------------------------------------------------------------------------


class ActivityCalendarLoader:
    """Loads CRR Activity Calendar xlsx from the asset folder."""

    def __init__(self, asset_dir: Path, sheet_names: list[str]) -> None:
        """
        Initialize the loader.

        Args:
            asset_dir: Directory containing CRRActivityCalendar*.xlsx files.
            sheet_names: List of sheet names to read (header assumed at row 3).
        """
        self._asset_dir = asset_dir
        self._sheet_names = sheet_names

    @st.cache_data
    def load(_self) -> Optional[dict[str, pd.DataFrame]]:
        """
        Load all configured sheets from the first matching xlsx in asset dir.

        Returns:
            Dict mapping sheet name to DataFrame, or None if no file found.
        """
        xlsx_files = list(_self._asset_dir.glob("CRRActivityCalendar*.xlsx"))
        if not xlsx_files:
            return None
        result = {}
        for name in _self._sheet_names:
            try:
                df = pd.read_excel(xlsx_files[0], sheet_name=name, header=3)
                result[name] = df
            except Exception:
                result[name] = pd.DataFrame()
        return result

    @st.cache_data
    def load_tou(_self) -> Optional[dict[str, pd.DataFrame]]:
        """
        Load CRR-Time-of-Use*.xlsx from asset dir.
        If 2024 is missing, fills it using the same data as 2025.

        Returns:
            Dict mapping sheet name to DataFrame, or None if no file found.
        """
        xlsx_files = list(_self._asset_dir.glob("CRR-Time-of-Use*.xlsx"))
        if not xlsx_files:
            return None
        result = {}
        try:
            xl = pd.ExcelFile(xlsx_files[0])
            for sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, header=1)
                if not df.empty and "Year" in df.columns and "Month" in df.columns:
                    if 2024 not in df["Year"].values and 2025 in df["Year"].values:
                        df_2024 = df.loc[df["Year"] == 2025].copy()
                        df_2024["Year"] = 2024
                        df = pd.concat([df, df_2024], ignore_index=True).sort_values(
                            "Year", ignore_index=True
                        )
                result[sheet] = df
        except Exception:
            return None
        return result if result else None


class AuctionDataLoader:
    """Loads and normalizes CRR auction results from uploaded CSV."""

    def __init__(self, column_map: dict[str, list[str]]) -> None:
        """
        Initialize the loader.

        Args:
            column_map: Map from standard column name to list of possible CSV names.
        """
        self._column_map = column_map

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply column mapping and derived columns to a DataFrame."""
        for std_col, variants in self._column_map.items():
            if std_col not in df.columns:
                for v in variants:
                    if v in df.columns:
                        df = df.rename(columns={v: std_col})
                        break
        if "auction_date" in df.columns:
            df["auction_date"] = pd.to_datetime(df["auction_date"], errors="coerce")
            df["year"] = df["auction_date"].dt.year
        if "mw_amount" in df.columns and "clearing_price" in df.columns:
            df["total_value"] = df["mw_amount"] * df["clearing_price"]
        return df

    def load(self, uploaded_file) -> pd.DataFrame:
        """
        Read CSV from Streamlit UploadedFile and normalize.

        Args:
            uploaded_file: Streamlit UploadedFile (CSV).

        Returns:
            DataFrame with standardized columns and total_value, year if applicable.
        """
        df = pd.read_csv(uploaded_file)
        return self._normalize(df)

    def load_from_path(self, path: Path) -> pd.DataFrame:
        """
        Read CSV from file path and normalize.

        Args:
            path: Path to a CSV file.

        Returns:
            DataFrame with standardized columns and total_value, year if applicable.
        """
        df = pd.read_csv(path)
        return self._normalize(df)


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------


class ActivityCalendarView:
    """Renders the Activity Calendar section (three sheets stacked)."""

    def __init__(
        self,
        loader: ActivityCalendarLoader,
        sheet_names: list[str],
    ) -> None:
        """
        Initialize the view.

        Args:
            loader: Loader that returns dict of sheet name -> DataFrame.
            sheet_names: Order of sheets to display.
        """
        self._loader = loader
        self._sheet_names = sheet_names

    def _render_auction_capacity_charts(self, calendar_df: pd.DataFrame) -> None:
        """
        Render bar charts of Auction Capacity % for Monthly and Annual auctions.

        Args:
            calendar_df: CRR Activity Calendar DataFrame with Auction Type and Capacity %.
        """
        capacity_col = self._find_column(calendar_df, "Auction Capacity %")
        name_col = self._find_column(calendar_df, "Auction Name")
        type_col = self._find_column(calendar_df, "Auction Type")
        if not capacity_col or not name_col or not type_col:
            return
        monthly = calendar_df[calendar_df[type_col].str.strip().str.lower() == "monthly"].copy()
        annual = calendar_df[calendar_df[type_col].str.strip().str.lower() == "annual"].copy()
        x_col = "Date"
        monthly[x_col] = monthly[name_col].apply(
            lambda n: self._auction_name_to_date_label(n, False)[0]
        )
        monthly["_sort"] = monthly[name_col].apply(
            lambda n: self._auction_name_to_date_label(n, False)[1]
        )
        monthly = monthly.sort_values("_sort")
        annual[x_col] = annual[name_col].apply(
            lambda n: self._auction_name_to_date_label(n, True)[0]
        )
        annual["_sort"] = annual[name_col].apply(
            lambda n: self._auction_name_to_date_label(n, True)[1]
        )
        annual = annual.sort_values("_sort")
        col1, col2 = st.columns(2)
        with col1:
            if not monthly.empty:
                fig_m = px.bar(
                    monthly,
                    x=x_col,
                    y=capacity_col,
                    title="Monthly Auction Capacity %",
                    labels={capacity_col: "Auction Capacity %", x_col: "Date"},
                )
                fig_m.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_m, use_container_width=True)
            else:
                st.caption("No monthly auctions in calendar.")
        with col2:
            if not annual.empty:
                fig_a = px.bar(
                    annual,
                    x=x_col,
                    y=capacity_col,
                    title="Semiannual (Annual) Auction Capacity %",
                    labels={capacity_col: "Auction Capacity %", x_col: "Date"},
                )
                fig_a.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_a, use_container_width=True)
            else:
                st.caption("No annual auctions in calendar.")

    @staticmethod
    def _find_column(df: pd.DataFrame, substring: str) -> Optional[str]:
        """Return first column name containing substring, or None."""
        for c in df.columns:
            if substring.lower() in str(c).lower():
                return c
        return None

    @staticmethod
    def _auction_name_to_date_label(name: str, is_annual: bool) -> tuple[str, tuple]:
        """
        Convert auction name to a date-style x-axis label and sort key.

        Monthly: "2026.JAN.Monthly.Auction" -> ("2026-01", (2026, 1)).
        Annual 1st6: "2026.1st6.AnnualAuction.Seq1" -> ("2026-Jan-Jul-Seq1", (2026, 0, 1)).
        Annual 2nd6: "2026.2nd6.AnnualAuction.Seq1" -> ("2026-Jul-Dec-Seq1", (2026, 1, 1)).

        Args:
            name: Raw auction name from calendar.
            is_annual: True if Auction Type is Annual.

        Returns:
            (display_label, sort_key) for ordering and x-axis.
        """
        name = str(name).strip()
        if is_annual:
            m = re.match(r"(\d{4})\.(1st6|2nd6)\.AnnualAuction\.Seq(\d+)", name, re.I)
            if m:
                year, half, seq = m.group(1), m.group(2).lower(), m.group(3)
                if "1st" in half:
                    label = f"{year}-Jan-Jul-Seq{seq}"
                    sort_key = (int(year), 0, int(seq))
                else:
                    label = f"{year}-Jul-Dec-Seq{seq}"
                    sort_key = (int(year), 1, int(seq))
                return label, sort_key
            return name, (0, 0, 0)
        # Monthly: 2026.JAN.Monthly.Auction -> 2026-01
        months = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06",
                  "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
        m = re.match(r"(\d{4})\.([A-Z]{3})\.Monthly", name, re.I)
        if m:
            year, mon = m.group(1), m.group(2).upper()
            mm = months.get(mon, "00")
            return f"{year}-{mm}", (int(year), int(mm))
        return name, (0, 0)

    def render(self) -> None:
        """Render all sheets as stacked tables with subheaders and dividers."""
        st.markdown("<h2 style='text-align: center'>Activity Calendar</h2>", unsafe_allow_html=True)
        sheets = self._loader.load()
        if sheets is None:
            st.warning("No CRR Activity Calendar xlsx found in the `asset` folder.")
            return
        for name in self._sheet_names:
            df = sheets.get(name, pd.DataFrame())
            st.subheader(name)
            if name == "Calendar Protocol References":
                st.markdown(
                    "[ERCOT Nodal Protocol](https://www.ercot.com/mktrules/nprotocols/current)"
                )
            if df.empty:
                st.caption("No data.")
            else:
                if name == "Calendar Protocol References":
                    df = df.T.reset_index()
                    df.columns = ["Column", "Protocol Reference"]
                st.dataframe(df, use_container_width=True, hide_index=True)
                if name == "CRR Activity Calendar":
                    self._render_auction_capacity_charts(df)
            st.divider()
        # CRR Time of Use table(s) from asset Excel at the end
        tou_sheets = self._loader.load_tou()
        if tou_sheets:
            st.subheader("CRR Time of Use (Hours)")
            for sheet_name, df in tou_sheets.items():
                if not df.empty:
                    st.caption(sheet_name)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.divider()


class AuctionResultsView:
    """Renders the Auction Results section: filters, metrics, and analysis tabs."""

    def __init__(
        self,
        df: pd.DataFrame,
        folder_names: Optional[list[str]] = None,
        source_folders: Optional[dict[str, list[str]]] = None,
        load_report_fn: Optional[Callable[[str, str, str], pd.DataFrame]] = None,
        load_path_specific_adders_fn: Optional[
            Callable[[str, str], list[tuple[str, pd.DataFrame]]]
        ] = None,
    ) -> None:
        """
        Initialize the view with the loaded auction DataFrame.

        Args:
            df: Normalized CRR auction results.
            folder_names: Names of annual subfolders that contributed data (for display).
            source_folders: Map "Annual" / "Monthly" to list of folder names for dropdowns.
            load_report_fn: Callable(source, folder_name, report_type) -> DataFrame for selected report.
            load_path_specific_adders_fn: Callable(source, folder_name) -> list of (label, DataFrame) for path specific adders.
        """
        self._df = df
        self._folder_names = folder_names or []
        self._source_folders = source_folders or {}
        self._load_report_fn = load_report_fn
        self._load_path_specific_adders_fn = load_path_specific_adders_fn

    def _render_available_auction_data_dropdowns(self) -> None:
        """Render source and folder dropdowns, then show all report-type tables for the selected folder."""
        st.subheader("Available auction data")
        st.caption(
            "In each folder name, the part after _ is the report production date."
        )
        if not self._source_folders or not self._load_report_fn:
            st.warning("No auction folders or loader available.")
            return
        source = st.selectbox(
            "Auction",
            AUCTION_SOURCE_OPTIONS,
            key="auction_source",
            help="Annual or Monthly auction data (so far only annual has data).",
        )
        folders = self._source_folders.get(source, [])
        if not folders:
            st.caption(f"No folders in {source}.")
            return

        folder_name = st.selectbox(
            "Auction data",
            folders,
            key="auction_folder",
            format_func=lambda x: x,
        )
        for report_type in REPORT_TYPES:
            report_df = self._load_report_fn(source, folder_name, report_type)
            if report_df is not None and not report_df.empty:
                st.subheader(report_type)
                st.dataframe(report_df, use_container_width=True, hide_index=True)
                st.divider()
        if self._load_path_specific_adders_fn:
            adders_list = self._load_path_specific_adders_fn(source, folder_name)
            if adders_list:
                st.subheader("Path Specific Adders")
                for label, adder_df in adders_list:
                    if adder_df is not None and not adder_df.empty:
                        # st.caption(label)
                        st.dataframe(adder_df, use_container_width=True, hide_index=True)
                        st.divider()

    def _render_metrics(self, df: pd.DataFrame) -> None:
        """Render summary metric cards."""
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total MW Awarded", f"{df['mw_amount'].sum():,.0f}")
        with col2:
            avg = df["clearing_price"].mean()
            st.metric("Avg Clearing Price ($/MW)", f"${avg:.2f}")
        with col3:
            total = df["total_value"].sum() if "total_value" in df.columns else 0
            st.metric("Total Auction Value ($)", f"${total:,.0f}")
        with col4:
            n = df["path_name"].nunique() if "path_name" in df.columns else 0
            st.metric("Unique Paths", n)

    def _render_price_trends_tab(self, df: pd.DataFrame) -> None:
        """Render Price Trends tab."""
        st.subheader("Clearing Price Trends Over Time")
        if "auction_date" not in df.columns or "clearing_price" not in df.columns:
            st.warning("Required columns (auction_date, clearing_price) not found.")
            return
        agg = df.groupby(["auction_date", "path_name"], as_index=False).agg(
            {"clearing_price": "mean", "mw_amount": "sum", "total_value": "sum"}
        )
        fig = px.line(
            agg,
            x="auction_date",
            y="clearing_price",
            color="path_name",
            title="Average Clearing Price by Path Over Time",
            labels={"clearing_price": "Avg Price ($/MW)", "auction_date": "Auction Date"},
        )
        fig.update_layout(
            height=CHART_HEIGHT_LINE,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig, use_container_width=True)
        if "time_of_use" in df.columns:
            st.subheader("Price by Time of Use Block")
            tou_agg = df.groupby(["year", "time_of_use"], as_index=False)["clearing_price"].mean()
            fig2 = px.bar(
                tou_agg,
                x="year",
                y="clearing_price",
                color="time_of_use",
                barmode="group",
                title="Average Clearing Price by Time of Use",
                labels={"clearing_price": "Avg Price ($/MW)"},
            )
            fig2.update_layout(height=CHART_HEIGHT_PIE)
            st.plotly_chart(fig2, use_container_width=True)

    def _render_path_analysis_tab(self, df: pd.DataFrame) -> None:
        """Render Path Analysis tab."""
        st.subheader("Path-Level Analysis")
        if "path_name" not in df.columns:
            st.warning("Path column not found in data.")
            return
        path_stats = (
            df.groupby("path_name")
            .agg(
                total_mw=("mw_amount", "sum"),
                avg_price=("clearing_price", "mean"),
                total_value=("total_value", "sum"),
                num_awards=("mw_amount", "count"),
            )
            .reset_index()
            .sort_values("total_value", ascending=False)
        )
        fig = px.bar(
            path_stats,
            x="path_name",
            y="total_value",
            color="avg_price",
            color_continuous_scale="Viridis",
            title="Total Auction Value by Path",
            labels={"total_value": "Total Value ($)", "path_name": "Path", "avg_price": "Avg Price"},
        )
        fig.update_layout(height=CHART_HEIGHT_BAR, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            path_stats.style.format({"avg_price": "${:.2f}", "total_value": "${:,.0f}"}),
            use_container_width=True,
        )

    def _render_market_overview_tab(self, df: pd.DataFrame) -> None:
        """Render Market Overview tab."""
        st.subheader("Market Overview")
        if "source_node" not in df.columns or "sink_node" not in df.columns:
            st.warning("Source/sink columns not found for flow analysis.")
            return
        df = df.copy()
        df["source_sink"] = df["source_node"] + " -> " + df["sink_node"]
        flow = (
            df.groupby("source_sink")
            .agg({"mw_amount": "sum", "total_value": "sum"})
            .reset_index()
            .sort_values("mw_amount", ascending=False)
            .head(15)
        )
        fig = px.treemap(
            flow,
            path=["source_sink"],
            values="mw_amount",
            color="total_value",
            color_continuous_scale="Blues",
            title="MW Flow by Source-Sink Pair",
        )
        fig.update_layout(height=CHART_HEIGHT_TREEMAP)
        st.plotly_chart(fig, use_container_width=True)
        if "crr_type" in df.columns:
            type_agg = df.groupby("crr_type").agg(
                {"mw_amount": "sum", "total_value": "sum"}
            ).reset_index()
            col_a, col_b = st.columns(2)
            with col_a:
                fig_a = px.pie(
                    type_agg,
                    values="mw_amount",
                    names="crr_type",
                    title="MW by CRR Type",
                )
                st.plotly_chart(fig_a, use_container_width=True)
            with col_b:
                fig_b = px.pie(
                    type_agg,
                    values="total_value",
                    names="crr_type",
                    title="Value by CRR Type",
                )
                st.plotly_chart(fig_b, use_container_width=True)

    def _render_raw_data_tab(self, df: pd.DataFrame) -> None:
        """Render Raw Data tab."""
        st.subheader("Raw Auction Data")
        st.dataframe(df, use_container_width=True)

    def render(self) -> None:
        """Render metrics and analysis tabs, or available data if expected columns missing."""
        df = self._df
        if "clearing_price" not in df.columns or "mw_amount" not in df.columns:
            self._render_available_auction_data_dropdowns()
            return
        self._render_metrics(df)
        st.divider()
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Price Trends", "Path Analysis", "Market Overview", "Raw Data"]
        )
        with tab1:
            self._render_price_trends_tab(df)
        with tab2:
            self._render_path_analysis_tab(df)
        with tab3:
            self._render_market_overview_tab(df)
        with tab4:
            self._render_raw_data_tab(df)


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------


class ERCOTCRRApp:
    """
    Main app controller: sidebar navigation and section dispatch.

    Displays either Activity Calendar (xlsx from asset folder) or
    Auction Results (uploaded CSV with filters and analysis tabs).
    """

    SECTIONS = ["Activity Calendar", "Auction Results", "Bid & Offer", "Base Loading", "Binding Constraints", "Shadow Prices", "Cleared Results", "Shaping", "Optimized FTR Portfolio"]

    def __init__(self) -> None:
        """Initialize loaders and views (views receive data at render time)."""
        self._calendar_loader = ActivityCalendarLoader(
            ASSET_DIR,
            ACTIVITY_CALENDAR_SHEETS,
        )
        self._calendar_view = ActivityCalendarView(
            self._calendar_loader,
            ACTIVITY_CALENDAR_SHEETS,
        )
        self._auction_loader = AuctionDataLoader(CRR_CSV_COLUMN_MAP)

    def _render_sidebar(self) -> str:
        """Render sidebar title and section selector. Returns selected section."""
        st.sidebar.markdown("**ERCOT CRR Auction Historical Analysis**")
        st.sidebar.divider()
        section = st.sidebar.selectbox(
            "Select section",
            self.SECTIONS,
            index=0,
        )
        return section

    def _run_activity_calendar(self) -> None:
        """Run the Activity Calendar section."""
        self._calendar_view.render()

    def _run_bid_offer(self) -> None:
        """Run the Bid & Offer section (inputs and analysis on combined data)."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Bid & Offer")
        source = st.sidebar.selectbox(
            "Source",
            options=["Annual", "Monthly"],
            key="bid_offer_source",
            help="Choose Annual or Monthly combined Bid & Offer data.",
        )
        source_key = source.lower()
        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        report_type = "Auction Bids and Offers"
        path = builder.get_master_path(report_type, source_key)
        if not path.exists():
            st.info(f"No {source} Bid & Offer master data. Run build_master_parquets.py to build.")
            return
        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in selected Bid & Offer master table.")
            return
        need = ["report_date", "BidPricePerMWH", "ShadowPricePerMWH", "MWh"]
        missing = [c for c in need if c not in df.columns]
        if missing:
            st.warning(f"Missing columns for price analysis: {missing}")
            return

        st.markdown("<h2 style='text-align: center'>Bid & Offer</h2>", unsafe_allow_html=True)
        # Build filter options from data
        def _options(col: str) -> list[str]:
            if col not in df.columns:
                return ["All"]
            vals = sorted(df[col].dropna().astype(str).unique().tolist())
            return ["All"] + [v for v in vals if v and str(v).strip()]

        bid_type_options = _options("BidType")
        hedge_type_options = _options("HedgeType")
        path_source_options = _options("Source")
        path_sink_options = _options("Sink")

        def _idx(opts: list[str], key: str) -> int:
            val = st.session_state.get(key, "All")
            if val in opts:
                return opts.index(val)
            return 0

        with st.sidebar.form("bid_offer_filters_form"):
            bid_type_filter = st.selectbox(
                "Bid Type",
                options=bid_type_options,
                index=_idx(bid_type_options, "bid_offer_bid_type"),
                key="bid_offer_bid_type_in",
                help="Filter by Bid Type (e.g. BUY, SELL).",
            )
            hedge_type_filter = st.selectbox(
                "Hedge Type",
                options=hedge_type_options,
                index=_idx(hedge_type_options, "bid_offer_hedge_type"),
                key="bid_offer_hedge_type_in",
                help="Filter by Hedge Type.",
            )
            path_source_filter = st.selectbox(
                "Path Source",
                options=path_source_options,
                index=_idx(path_source_options, "bid_offer_path_source"),
                key="bid_offer_path_source_in",
                help="Filter by path source node.",
            )
            path_sink_filter = st.selectbox(
                "Path Sink",
                options=path_sink_options,
                index=_idx(path_sink_options, "bid_offer_path_sink"),
                key="bid_offer_path_sink_in",
                help="Filter by path sink node.",
            )
            submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state["bid_offer_bid_type"] = bid_type_filter
            st.session_state["bid_offer_hedge_type"] = hedge_type_filter
            st.session_state["bid_offer_path_source"] = path_source_filter
            st.session_state["bid_offer_path_sink"] = path_sink_filter

        bid_type_filter = st.session_state.get("bid_offer_bid_type", "All")
        hedge_type_filter = st.session_state.get("bid_offer_hedge_type", "All")
        path_source_filter = st.session_state.get("bid_offer_path_source", "All")
        path_sink_filter = st.session_state.get("bid_offer_path_sink", "All")

        # Apply filters
        if "BidType" in df.columns and bid_type_filter != "All":
            df = df[df["BidType"].astype(str) == bid_type_filter].copy()
        if "HedgeType" in df.columns and hedge_type_filter != "All":
            df = df[df["HedgeType"].astype(str) == hedge_type_filter].copy()
        if "Source" in df.columns and path_source_filter != "All":
            df = df[df["Source"].astype(str) == path_source_filter].copy()
        if "Sink" in df.columns and path_sink_filter != "All":
            df = df[df["Sink"].astype(str) == path_sink_filter].copy()

        if df.empty:
            st.info("No rows after applying filters.")
            return
        if "TimeOfUse" not in df.columns:
            st.warning("TimeOfUse column missing; cannot plot by Time of Use.")
            return
        title_parts = [f"Auction: {source}"]
        if bid_type_filter != "All":
            title_parts.append(f"Bid Type: {bid_type_filter}")
        if hedge_type_filter != "All":
            title_parts.append(f"Hedge Type: {hedge_type_filter}")
        if path_source_filter != "All":
            title_parts.append(f"Path Source: {path_source_filter}")
        if path_sink_filter != "All":
            title_parts.append(f"Path Sink: {path_sink_filter}")
        title_suffix = " · ".join(title_parts)
        df["_bid_vw"] = pd.to_numeric(df["BidPricePerMWH"], errors="coerce") * pd.to_numeric(df["MWh"], errors="coerce")
        df["_shadow_vw"] = pd.to_numeric(df["ShadowPricePerMWH"], errors="coerce") * pd.to_numeric(df["MWh"], errors="coerce")
        agg = df.groupby(["report_date", "TimeOfUse"], as_index=False).agg(
            _bid_vw=("_bid_vw", "sum"),
            _shadow_vw=("_shadow_vw", "sum"),
            mwh_sum=("MWh", "sum"),
        )
        agg["mwh_sum"] = pd.to_numeric(agg["mwh_sum"], errors="coerce").replace(0, float("nan"))
        agg["Bid"] = agg["_bid_vw"] / agg["mwh_sum"]
        agg["Shadow"] = agg["_shadow_vw"] / agg["mwh_sum"]
        agg = agg.sort_values(["report_date", "TimeOfUse"])
        long = agg.melt(
            id_vars=["report_date", "TimeOfUse"],
            value_vars=["Bid", "Shadow"],
            var_name="price_type",
            value_name="$/MW",
        )
        long["series"] = long["TimeOfUse"].astype(str) + " · " + long["price_type"]
        fig = px.line(
            long,
            x="report_date",
            y="$/MW",
            color="series",
            title=f"Volume-weighted ($/MW) Bid and Shadow prices<br><sub>{title_suffix}</sub>",
            labels={"report_date": "Report date", "$/MW": "Vol-weighted $/MW"},
        )
        fig.update_layout(
            height=CHART_HEIGHT_LINE,
            legend_title="Time of Use · Price",
            legend=dict(orientation="h", yanchor="top", y=-0.15),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Per-series histograms and statistics (mean, quantiles, skewness, kurtosis, IQR)
        with st.expander("Distribution by series"):
            vals_col = "$/MW"
            for series_name in sorted(long["series"].dropna().unique()):
                ser = long.loc[long["series"] == series_name, vals_col].dropna()
                if ser.empty or ser.size < 2:
                    st.caption(f"{series_name}: not enough data for histogram.")
                continue
                st.markdown(f"**{series_name}**")
                col_hist, col_tab = st.columns([2, 1])
                with col_hist:
                    fig_hist = px.histogram(
                        ser,
                        x=vals_col,
                        nbins=min(30, max(10, ser.size // 3)),
                        title=f"Distribution of {vals_col}",
                        labels={"x": vals_col, "y": "Count"},
                    )
                    fig_hist.update_layout(height=280, showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
                with col_tab:
                    qs = [0.01, 0.05, 0.10, 0.90, 0.95, 0.99]
                    quant = ser.quantile(qs)
                    iqr = ser.quantile(0.75) - ser.quantile(0.25)
                stats = {
                    "Statistic": [
                        "Count",
                        "Mean",
                        "Median",
                        "1st %",
                        "5th %",
                        "10th %",
                        "90th %",
                        "95th %",
                        "99th %",
                        "IQR",
                        "Skewness",
                        "Kurtosis",
                    ],
                    "Value": [
                        int(ser.size),
                        round(ser.mean(), 4),
                        round(ser.median(), 4),
                        round(quant.iloc[0], 4),
                        round(quant.iloc[1], 4),
                        round(quant.iloc[2], 4),
                        round(quant.iloc[3], 4),
                        round(quant.iloc[4], 4),
                        round(quant.iloc[5], 4),
                        round(iqr, 4),
                        round(ser.skew(), 4),
                        round(ser.kurtosis(), 4),
                    ],
                }
                st.dataframe(
                    pd.DataFrame(stats),
                    use_container_width=True,
                    hide_index=True,
                )
                st.divider()

        # Volume over time: total MW by report_date and Time of Use
        if "MW" not in df.columns:
            st.caption("Volume over time skipped: no MW column.")
        else:
            df["_vol_mw"] = pd.to_numeric(df["MW"], errors="coerce")
            vol_agg = df.groupby(["report_date", "TimeOfUse"], as_index=False)["_vol_mw"].sum()
            vol_agg = vol_agg.sort_values(["report_date", "TimeOfUse"])
            fig_vol = px.line(
                vol_agg,
                x="report_date",
                y="_vol_mw",
                color="TimeOfUse",
                title=f"Total MW by report date and Time of Use<br><sub>{title_suffix}</sub>",
                labels={"report_date": "Report date", "_vol_mw": "Total MW", "TimeOfUse": "Time of Use"},
            )
            fig_vol.update_layout(
                height=CHART_HEIGHT_LINE,
                legend_title="Time of Use",
                legend=dict(orientation="h", yanchor="top", y=-0.15),
            )
            st.plotly_chart(fig_vol, use_container_width=True)

            # Total MW: distribution by Time of Use (histogram + stats in expander)
            with st.expander("Total MW — distribution by Time of Use"):
                mw_col = "_vol_mw"
                for tou_name in sorted(vol_agg["TimeOfUse"].dropna().astype(str).unique()):
                    ser = vol_agg.loc[vol_agg["TimeOfUse"].astype(str) == tou_name, mw_col].dropna()
                    if ser.empty or ser.size < 2:
                        st.caption(f"{tou_name}: not enough data for histogram.")
                        continue
                    st.markdown(f"**{tou_name}**")
                    col_hist, col_tab = st.columns([2, 1])
                    with col_hist:
                        fig_mw_hist = px.histogram(
                            ser,
                            x=mw_col,
                            nbins=min(30, max(10, ser.size // 3)),
                            title="Distribution of Total MW",
                            labels={"x": "Total MW", "y": "Count"},
                        )
                        fig_mw_hist.update_layout(height=280, showlegend=False)
                        st.plotly_chart(fig_mw_hist, use_container_width=True)
                    with col_tab:
                        qs = [0.01, 0.05, 0.10, 0.90, 0.95, 0.99]
                        quant = ser.quantile(qs)
                        iqr = ser.quantile(0.75) - ser.quantile(0.25)
                        stats_mw = {
                            "Statistic": [
                                "Count",
                                "Mean",
                                "Median",
                                "1st %",
                                "5th %",
                                "10th %",
                                "90th %",
                                "95th %",
                                "99th %",
                                "IQR",
                                "Skewness",
                                "Kurtosis",
                            ],
                            "Value": [
                                int(ser.size),
                                round(ser.mean(), 4),
                                round(ser.median(), 4),
                                round(quant.iloc[0], 4),
                                round(quant.iloc[1], 4),
                                round(quant.iloc[2], 4),
                                round(quant.iloc[3], 4),
                                round(quant.iloc[4], 4),
                                round(quant.iloc[5], 4),
                                round(iqr, 4),
                                round(ser.skew(), 4),
                                round(ser.kurtosis(), 4),
                            ],
                        }
                        st.dataframe(
                            pd.DataFrame(stats_mw),
                            use_container_width=True,
                            hide_index=True,
                        )
        st.divider()

        # Stacked bar: MW by report_date, stacked by Time of Use with percentage
        if "MW" in df.columns and "TimeOfUse" in df.columns:
            df["_mw"] = pd.to_numeric(df["MW"], errors="coerce")
            bar_agg = df.groupby(["report_date", "TimeOfUse"], as_index=False)["_mw"].sum()
            tot_per_date = bar_agg.groupby("report_date", as_index=False)["_mw"].sum().rename(columns={"_mw": "_total"})
            bar_agg = bar_agg.merge(tot_per_date, on="report_date")
            bar_agg["pct"] = (bar_agg["_mw"] / bar_agg["_total"].replace(0, float("nan")) * 100).round(1)
            bar_agg["_text"] = bar_agg["pct"].astype(str) + "%"
            fig_bar = px.bar(
                bar_agg,
                x="report_date",
                y="_mw",
                color="TimeOfUse",
                barmode="stack",
                title=f"MW by report date <br><sub>{title_suffix}</sub>",
                labels={"report_date": "Report date", "_mw": "MW", "TimeOfUse": "Time of Use"},
                text="_text",
            )
            fig_bar.update_traces(textposition="inside", textfont_size=10)
            fig_bar.update_layout(
                height=CHART_HEIGHT_BAR,
                legend_title="Time of Use",
                legend=dict(orientation="h", yanchor="top", y=-0.15),
                xaxis_tickangle=-45,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Bid vs Shadow price: scatter (vol-weighted by report_date and Time of Use) + OLS trendline
        scatter_df = agg[["report_date", "TimeOfUse", "Bid", "Shadow"]].dropna(subset=["Bid", "Shadow"])
        if not scatter_df.empty:
            fig_scatter = px.scatter(
                scatter_df,
                x="Bid",
                y="Shadow",
                color="TimeOfUse",
                hover_data=["report_date"],
                trendline="ols",
                title=f"Bid vs Shadow price (vol-weighted $/MW)<br><sub>{title_suffix}</sub>",
                labels={"Bid": "Bid price ($/MW)", "Shadow": "Shadow price ($/MW)", "TimeOfUse": "Time of Use"},
            )
            lim = max(scatter_df["Bid"].max(), scatter_df["Shadow"].max()) * 1.05
            fig_scatter.add_trace(
                go.Scatter(
                    x=[0, lim],
                    y=[0, lim],
                    mode="lines",
                    line=dict(dash="dash", color="gray"),
                    name="Bid = Shadow",
                )
            )
            fig_scatter.update_layout(
                height=CHART_HEIGHT_LINE,
                legend_title="Time of Use",
                legend=dict(orientation="h", yanchor="top", y=-0.15),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            # Bid–Shadow correlation: overall and by Time of Use
            r_overall = scatter_df["Bid"].corr(scatter_df["Shadow"])
            st.caption(f"**Bid–Shadow correlation (overall):** r = {r_overall:.4f}")
            with st.expander("Correlation by Time of Use"):
                corr_tou = (
                    scatter_df.groupby("TimeOfUse")
                    .apply(lambda g: g["Bid"].corr(g["Shadow"]) if len(g) >= 2 else float("nan"))
                    .reset_index()
                )
                corr_tou.columns = ["Time of Use", "Correlation"]
                st.dataframe(corr_tou, use_container_width=True, hide_index=True)

        # Path-level view: top paths by MW or by premium (Bid − Shadow)
        if "Source" in df.columns and "Sink" in df.columns:
            df_path = df.copy()
            df_path["_path"] = (
                df_path["Source"].astype(str).fillna("") + " → " + df_path["Sink"].astype(str).fillna("")
            ).str.strip(" → ")
            df_path["_bid_vw"] = pd.to_numeric(df_path["BidPricePerMWH"], errors="coerce") * pd.to_numeric(
                df_path["MWh"], errors="coerce"
            )
            df_path["_shadow_vw"] = pd.to_numeric(df_path["ShadowPricePerMWH"], errors="coerce") * pd.to_numeric(
                df_path["MWh"], errors="coerce"
            )
            path_agg = (
                df_path.groupby(["report_date", "_path"], as_index=False)
                .agg(
                    MWh=("MWh", lambda s: pd.to_numeric(s, errors="coerce").sum()),
                    _bid_vw=("_bid_vw", "sum"),
                    _shadow_vw=("_shadow_vw", "sum"),
                )
            )
            mwh_pos = path_agg["MWh"] > 0
            path_agg["Bid"] = (path_agg["_bid_vw"] / path_agg["MWh"]).where(mwh_pos)
            path_agg["Shadow"] = (path_agg["_shadow_vw"] / path_agg["MWh"]).where(mwh_pos)
            path_agg["Premium"] = path_agg["Bid"] - path_agg["Shadow"]

            # with st.expander("Bid–Shadow correlation by path"):
            #     path_corr = (
            #         path_agg.dropna(subset=["Bid", "Shadow"])
            #         .groupby("_path")
            #         .apply(lambda g: g["Bid"].corr(g["Shadow"]) if len(g) >= 2 else float("nan"))
            #         .reset_index()
            #     )
            #     path_corr.columns = ["Path", "Correlation"]
            #     path_corr = path_corr.dropna(subset=["Correlation"]).sort_values(
            #         "Correlation", key=lambda s: s.abs(), ascending=False
            #     )
            #     if path_corr.empty:
            #         st.caption("No path-level correlation (need at least 2 report dates per path).")
            #     else:
            #         st.dataframe(path_corr, use_container_width=True, hide_index=True)

            st.subheader("Path-level view")
            rank_by = st.radio(
                "Rank paths by",
                ["MW", "Premium (Bid − Shadow)"],
                key="path_rank_by",
                horizontal=True,
                help="Top paths by total MW or by volume-weighted premium.",
            )
            view_mode = st.radio(
                "View",
                ["Over time", "Single report date"],
                key="path_view_mode",
                horizontal=True,
            )
            report_dates = sorted(path_agg["report_date"].dropna().unique().tolist())
            single_date = None
            if view_mode == "Single report date" and report_dates:
                single_date = st.selectbox(
                    "Report date",
                    options=report_dates,
                    key="path_single_date",
                )
            top_n = st.slider("Top N paths", 5, 50, 15, key="path_top_n")

            if rank_by == "MW":
                path_totals = path_agg.groupby("_path", as_index=False)["MWh"].sum()
                top_paths = path_totals.nlargest(top_n, "MWh")["_path"].tolist()
                metric_col = "MWh"
                y_title = "MW"
            else:
                path_agg["_premium_contrib"] = path_agg["Premium"] * path_agg["MWh"]
                path_totals = path_agg.groupby("_path", as_index=False)["_premium_contrib"].sum()
                top_paths = path_totals.reindex(
                    path_totals["_premium_contrib"].abs().sort_values(ascending=False).index
                )["_path"].head(top_n).tolist()
                metric_col = "Premium"
                y_title = "Premium ($/MW)"

            path_agg_top = path_agg[path_agg["_path"].isin(top_paths)].copy()

            if path_agg_top.empty:
                st.caption("No path-level data after filters.")
            elif view_mode == "Single report date" and single_date is not None:
                one = path_agg_top[path_agg_top["report_date"] == single_date].copy()
                one = one.sort_values(metric_col, ascending=False)
                fig_path = px.bar(
                    one,
                    x="_path",
                    y=metric_col,
                    title=f"Top {top_n} paths by {y_title} on {single_date}<br><sub>{title_suffix}</sub>",
                    labels={"_path": "Path", metric_col: y_title},
                )
                fig_path.update_layout(
                    height=max(400, min(800, 25 * len(one))),
                    xaxis_tickangle=-45,
                    margin=dict(b=120),
                )
                st.plotly_chart(fig_path, use_container_width=True)
                with st.expander("Path-level table"):
                    st.dataframe(
                        one[["_path", "report_date", "MWh", "Bid", "Shadow", "Premium"]].rename(
                            columns={"_path": "Path"}
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )
            else:
                fig_path = px.line(
                    path_agg_top,
                    x="report_date",
                    y=metric_col,
                    color="_path",
                    title=f"Top {top_n} paths by {y_title} over time<br><sub>{title_suffix}</sub>",
                    labels={"report_date": "Report date", "_path": "Path", metric_col: y_title},
                )
                fig_path.update_layout(
                    height=CHART_HEIGHT_LINE,
                    legend_title="Path",
                    legend=dict(orientation="h", yanchor="top", y=-0.2),
                )
                st.plotly_chart(fig_path, use_container_width=True)
                with st.expander("Path-level table (top paths over time)"):
                    tab_df = path_agg_top[["_path", "report_date", "MWh", "Bid", "Shadow", "Premium"]].sort_values(
                        ["report_date", "_path"]
                    )
                    st.dataframe(
                        tab_df.rename(columns={"_path": "Path"}),
                        use_container_width=True,
                        hide_index=True,
                    )
        else:
            st.caption("Path-level view requires Source and Sink columns in the data.")

    def _run_base_loading(self) -> None:
        """Run the Base Loading section (combined Base Loading parquet)."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Base Loading")

        # Applied values (updated only on form Submit)
        bl_defaults = {
            "bl_applied_source": "Annual",
            "bl_applied_view": "Overall",
            "bl_applied_report_date": None,
            "bl_applied_share_mw_view": "Overall",
            "bl_applied_top_n_share": 10,
            "bl_applied_share_val_view": "Overall",
            "bl_applied_top_n_val": 10,
            "bl_applied_conc_metric": "MW",
            "bl_applied_top_n_paths": 10,
            "bl_applied_part_ts_metric": "MW",
            "bl_applied_top_n_ts": 10,
            "bl_applied_period_size": 3,
            "bl_applied_growth_metric": "MW",
        }
        for k, v in bl_defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v
        applied_source = st.session_state["bl_applied_source"]
        applied_view = st.session_state["bl_applied_view"]
        applied_report_date = st.session_state["bl_applied_report_date"]
        applied_share_mw_view = st.session_state["bl_applied_share_mw_view"]
        applied_top_n_share = st.session_state["bl_applied_top_n_share"]
        applied_share_val_view = st.session_state["bl_applied_share_val_view"]
        applied_top_n_val = st.session_state["bl_applied_top_n_val"]
        applied_conc_metric = st.session_state["bl_applied_conc_metric"]
        applied_top_n_paths = st.session_state["bl_applied_top_n_paths"]
        applied_part_ts_metric = st.session_state["bl_applied_part_ts_metric"]
        applied_top_n_ts = st.session_state["bl_applied_top_n_ts"]
        applied_period_size = st.session_state["bl_applied_period_size"]
        applied_growth_metric = st.session_state["bl_applied_growth_metric"]

        source_key = applied_source.lower()
        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        report_type = "Base Loading"
        path = builder.get_master_path(report_type, source_key)
        if not path.exists():
            st.info(f"No {applied_source} Base Loading master data. Run build_master_parquets.py to build.")
            return
        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in selected Base Loading master table.")
            return
        st.markdown("<h2 style='text-align: center'>Base Loading</h2>", unsafe_allow_html=True)

        account_col = "AccountHolder" if "AccountHolder" in df.columns else None
        has_report_date = "report_date" in df.columns
        report_dates = sorted(df["report_date"].dropna().unique().tolist()) if has_report_date else []
        if report_dates and applied_report_date not in report_dates:
            st.session_state["bl_applied_report_date"] = report_dates[0]
            applied_report_date = report_dates[0]

        # All inputs in a form (applied on Submit)
        with st.sidebar.form(key="base_loading_form"):
            source = st.selectbox(
                "Data source",
                options=["Annual", "Monthly"],
                index=0 if applied_source == "Annual" else 1,
                help="Annual or Monthly Base Loading data.",
            )
            view_over_time = st.radio(
                "Volume & value view",
                ["Overall", "By report date"],
                index=0 if applied_view == "Overall" else 1,
                horizontal=True,
                help="Overall or filter by report date.",
            )
            selected_date = None
            if has_report_date and report_dates:
                idx = report_dates.index(applied_report_date) if applied_report_date in report_dates else 0
                selected_date = st.selectbox("Report date", options=report_dates, index=idx)
            share_mw_view = st.radio(
                "Share of MW view",
                ["Overall", "Over time"],
                index=0 if applied_share_mw_view == "Overall" else 1,
                horizontal=True,
            )
            top_n_share = st.slider("Top N participants (MW over time)", 3, 25, applied_top_n_share)
            share_val_view = st.radio(
                "Share of value view",
                ["Overall", "Over time"],
                index=0 if applied_share_val_view == "Overall" else 1,
                horizontal=True,
            )
            top_n_val = st.slider("Top N participants (value over time)", 3, 25, applied_top_n_val)
            conc_metric = st.radio(
                "Concentration metric",
                ["MW", "Value"],
                index=0 if applied_conc_metric == "MW" else 1,
                horizontal=True,
            )
            top_n_paths = st.slider("Top N paths per participant", 1, 30, applied_top_n_paths)
            part_ts_metric = st.radio(
                "Participation over time metric",
                ["MW", "Value"],
                index=0 if applied_part_ts_metric == "MW" else 1,
                horizontal=True,
            )
            top_n_ts = st.slider("Top N participants (time series)", 3, 25, applied_top_n_ts)
            period_size = st.slider("Period size (growth/decline)", 1, 10, applied_period_size)
            growth_metric = st.radio(
                "Growth metric",
                ["MW", "Value"],
                index=0 if applied_growth_metric == "MW" else 1,
                horizontal=True,
            )
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["bl_applied_source"] = source
            st.session_state["bl_applied_view"] = view_over_time
            if view_over_time == "By report date":
                st.session_state["bl_applied_report_date"] = selected_date if selected_date is not None else (report_dates[0] if report_dates else None)
            st.session_state["bl_applied_share_mw_view"] = share_mw_view
            st.session_state["bl_applied_top_n_share"] = top_n_share
            st.session_state["bl_applied_share_val_view"] = share_val_view
            st.session_state["bl_applied_top_n_val"] = top_n_val
            st.session_state["bl_applied_conc_metric"] = conc_metric
            st.session_state["bl_applied_top_n_paths"] = top_n_paths
            st.session_state["bl_applied_part_ts_metric"] = part_ts_metric
            st.session_state["bl_applied_top_n_ts"] = top_n_ts
            st.session_state["bl_applied_period_size"] = period_size
            st.session_state["bl_applied_growth_metric"] = growth_metric
            st.rerun()

        # Participation over time: distinct AccountHolders and CRR count by report_date
        if "report_date" not in df.columns:
            st.caption("Participation over time requires a report_date column in the data.")
        elif account_col is None:
            st.caption("Participation over time requires an AccountHolder column in the data.")
        else:
            part = (
                df.groupby("report_date", as_index=False)
                .agg(distinct_participants=(account_col, "nunique"))
            )
            part["crr_count"] = part["report_date"].map(df.groupby("report_date").size())
            part = part.sort_values("report_date")

            fig_part = go.Figure()
            fig_part.add_trace(
                go.Scatter(
                    x=part["report_date"],
                    y=part["distinct_participants"],
                    mode="lines+markers",
                    name="Distinct participants",
                    line=dict(width=2),
                )
            )
            fig_part.add_trace(
                go.Scatter(
                    x=part["report_date"],
                    y=part["crr_count"],
                    mode="lines+markers",
                    name="CRR count",
                    yaxis="y2",
                    line=dict(width=2, dash="dot"),
                )
            )
            fig_part.update_layout(
                title="Participation over time",
                xaxis_title="Report date",
                yaxis_title="Distinct participants",
                height=400,
                legend=dict(orientation="h", yanchor="top", y=-0.12),
                yaxis2=dict(
                    title="CRR count",
                    overlaying="y",
                    side="right",
                ),
            )
            st.plotly_chart(fig_part, use_container_width=True)

        # Participant-level: Volume, Value, CRR count / path count (require AccountHolder)
        if account_col is not None:
            df_part = df[df[account_col].notna()].copy()
            if applied_view == "By report date" and applied_report_date is not None:
                df_part = df_part[df_part["report_date"] == applied_report_date]
            part_grp = df_part.groupby(account_col, as_index=False)

            # 1. Volume by participant (Total MW)
            if "MW" in df.columns:
                st.subheader("Volume by participant")
                vol = part_grp.agg(total_mw=("MW", lambda s: pd.to_numeric(s, errors="coerce").sum()))
                vol = vol.sort_values("total_mw", ascending=False).reset_index(drop=True)
                fig_vol = px.bar(
                    vol,
                    x=account_col,
                    y="total_mw",
                    title="Total MW per AccountHolder",
                    labels={account_col: "Account holder", "total_mw": "Total MW"},
                )
                fig_vol.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_vol, use_container_width=True)
                st.dataframe(
                    vol.rename(columns={account_col: "Account holder", "total_mw": "Total MW"}),
                    use_container_width=True,
                    hide_index=True,
                )

            # 2. Value by participant (MW × ShadowPricePerMWH)
            if "MW" in df.columns and "ShadowPricePerMWH" in df.columns:
                st.subheader("Value by participant")
                df_part["_value"] = (
                    pd.to_numeric(df_part["MW"], errors="coerce")
                    * pd.to_numeric(df_part["ShadowPricePerMWH"], errors="coerce")
                )
                val = df_part.groupby(account_col, as_index=False)["_value"].sum()
                val = val.rename(columns={"_value": "total_value"}).sort_values(
                    "total_value", ascending=False
                ).reset_index(drop=True)
                fig_val = px.bar(
                    val,
                    x=account_col,
                    y="total_value",
                    title="Total value (MW × $/MW) per AccountHolder",
                    labels={account_col: "Account holder", "total_value": "Total value"},
                )
                fig_val.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_val, use_container_width=True)
                st.dataframe(
                    val.rename(columns={account_col: "Account holder", "total_value": "Total value"}),
                    use_container_width=True,
                    hide_index=True,
                )

            # 3. CRR count / path count per AccountHolder
            st.subheader("Breadth of activity (CRR count / path count)")
            crr_count = part_grp.size().reset_index()
            crr_count = crr_count.rename(columns={crr_count.columns[-1]: "CRR count"})
            if "Source" in df.columns and "Sink" in df.columns:
                path_count = (
                    df_part.groupby(account_col)
                    .apply(lambda g: g.drop_duplicates(subset=["Source", "Sink"]).shape[0])
                    .reset_index()
                )
                path_count = path_count.rename(columns={path_count.columns[-1]: "Path count"})
                breadth = crr_count.merge(path_count, on=account_col, how="left")
            else:
                breadth = crr_count.copy()
                breadth["Path count"] = None
            breadth = breadth.sort_values("CRR count", ascending=False).reset_index(drop=True)
            fig_crr = px.bar(
                breadth,
                x=account_col,
                y="CRR count",
                title="CRR count per AccountHolder",
                labels={account_col: "Account holder"},
            )
            fig_crr.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_crr, use_container_width=True)
            if "Path count" in breadth.columns and breadth["Path count"].notna().any():
                fig_path = px.bar(
                    breadth,
                    x=account_col,
                    y="Path count",
                    title="Distinct path count per AccountHolder",
                    labels={account_col: "Account holder", "Path count": "Path count"},
                )
                fig_path.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_path, use_container_width=True)
            display_breadth = breadth.rename(columns={account_col: "Account holder"})
            if "Path count" in display_breadth.columns and display_breadth["Path count"].isna().all():
                display_breadth = display_breadth.drop(columns=["Path count"])
            st.dataframe(display_breadth, use_container_width=True, hide_index=True)

            # 4. Share of MW
            if "MW" in df.columns and account_col is not None:
                st.subheader("Share of MW")
                df_share = df[df[account_col].notna()].copy()
                df_share["_mw"] = pd.to_numeric(df_share["MW"], errors="coerce")
                if applied_share_mw_view == "Overall" or not has_report_date:
                    mw_tot = df_share["_mw"].sum()
                    share_mw = (
                        df_share.groupby(account_col, as_index=False)["_mw"]
                        .sum()
                        .assign(pct_mw=lambda x: (x["_mw"] / mw_tot * 100) if mw_tot else 0)
                        .sort_values("pct_mw", ascending=False)
                    )
                    share_mw = share_mw.rename(columns={account_col: "Account holder", "pct_mw": "% of total MW"})
                    fig_share_mw = px.bar(
                        share_mw,
                        x="Account holder",
                        y="% of total MW",
                        title="Share of total MW by participant",
                    )
                    fig_share_mw.update_layout(height=400, xaxis_tickangle=-45)
                    st.plotly_chart(fig_share_mw, use_container_width=True)
                    with st.expander("Share of MW table"):
                        st.dataframe(share_mw[["Account holder", "% of total MW"]], use_container_width=True, hide_index=True)
                elif has_report_date:
                    mw_by_date = df_share.groupby(["report_date", account_col], as_index=False)["_mw"].sum()
                    tot_by_date = mw_by_date.groupby("report_date", as_index=False)["_mw"].sum().rename(columns={"_mw": "_tot"})
                    mw_by_date = mw_by_date.merge(tot_by_date, on="report_date")
                    mw_by_date["pct"] = (mw_by_date["_mw"] / mw_by_date["_tot"].replace(0, float("nan")) * 100)
                    top_participants = (
                        df_share.groupby(account_col)["_mw"].sum().nlargest(applied_top_n_share).index.tolist()
                    )
                    mw_top = mw_by_date[mw_by_date[account_col].isin(top_participants)]
                    fig_share_mw = px.area(
                        mw_top,
                        x="report_date",
                        y="pct",
                        color=account_col,
                        title=f"Share of MW over time (top {applied_top_n_share} participants)",
                        labels={"report_date": "Report date", "pct": "% of total MW", account_col: "Account holder"},
                    )
                    fig_share_mw.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12))
                    st.plotly_chart(fig_share_mw, use_container_width=True)

            # 5. Share of value
            if "MW" in df.columns and "ShadowPricePerMWH" in df.columns and account_col is not None:
                st.subheader("Share of value")
                df_val = df[df[account_col].notna()].copy()
                df_val["_mw"] = pd.to_numeric(df_val["MW"], errors="coerce")
                df_val["_price"] = pd.to_numeric(df_val["ShadowPricePerMWH"], errors="coerce")
                df_val["_value"] = df_val["_mw"] * df_val["_price"]
                if applied_share_val_view == "Overall" or not has_report_date:
                    val_tot = df_val["_value"].sum()
                    share_val = (
                        df_val.groupby(account_col, as_index=False)["_value"]
                        .sum()
                        .assign(pct_val=lambda x: (x["_value"] / val_tot * 100) if val_tot else 0)
                        .sort_values("pct_val", ascending=False)
                    )
                    share_val = share_val.rename(columns={account_col: "Account holder", "pct_val": "% of total value"})
                    fig_share_val = px.bar(
                        share_val,
                        x="Account holder",
                        y="% of total value",
                        title="Share of total value by participant",
                    )
                    fig_share_val.update_layout(height=400, xaxis_tickangle=-45)
                    st.plotly_chart(fig_share_val, use_container_width=True)
                    with st.expander("Share of value table"):
                        st.dataframe(share_val[["Account holder", "% of total value"]], use_container_width=True, hide_index=True)
                elif has_report_date:
                    val_by_date = df_val.groupby(["report_date", account_col], as_index=False)["_value"].sum()
                    tot_val_date = val_by_date.groupby("report_date", as_index=False)["_value"].sum().rename(columns={"_value": "_tot"})
                    val_by_date = val_by_date.merge(tot_val_date, on="report_date")
                    val_by_date["pct"] = (val_by_date["_value"] / val_by_date["_tot"].replace(0, float("nan")) * 100)
                    top_val = df_val.groupby(account_col)["_value"].sum().nlargest(applied_top_n_val).index.tolist()
                    val_top = val_by_date[val_by_date[account_col].isin(top_val)]
                    fig_share_val = px.area(
                        val_top,
                        x="report_date",
                        y="pct",
                        color=account_col,
                        title=f"Share of value over time (top {applied_top_n_val} participants)",
                        labels={"report_date": "Report date", "pct": "% of total value", account_col: "Account holder"},
                    )
                    fig_share_val.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12))
                    st.plotly_chart(fig_share_val, use_container_width=True)

            # 6. Concentration metrics (Top 5 / Top 10 share, HHI by report_date)
            if has_report_date and account_col is not None:
                st.subheader("Concentration metrics")
                df_conc = df[df[account_col].notna()].copy()
                if applied_conc_metric == "MW" and "MW" in df_conc.columns:
                    df_conc["_conc"] = pd.to_numeric(df_conc["MW"], errors="coerce")
                elif applied_conc_metric == "Value" and "MW" in df_conc.columns and "ShadowPricePerMWH" in df_conc.columns:
                    df_conc["_conc"] = (
                        pd.to_numeric(df_conc["MW"], errors="coerce")
                        * pd.to_numeric(df_conc["ShadowPricePerMWH"], errors="coerce")
                    )
                else:
                    df_conc["_conc"] = 0
                by_date = df_conc.groupby("report_date", as_index=False)["_conc"].sum().rename(columns={"_conc": "_tot"})
                by_date_part = df_conc.groupby(["report_date", account_col], as_index=False)["_conc"].sum()
                by_date_part = by_date_part.merge(by_date[["report_date", "_tot"]], on="report_date")
                by_date_part["share_pct"] = (by_date_part["_conc"] / by_date_part["_tot"].replace(0, float("nan")) * 100)
                def top_share(g, n):
                    return g.nlargest(n, "_conc")["share_pct"].sum()
                conc_ts = (
                    by_date_part.groupby("report_date")
                    .apply(lambda g: pd.Series({"top5": top_share(g, 5), "top10": top_share(g, 10), "hhi": ((g["share_pct"] / 100) ** 2).sum() * 10000}))
                    .reset_index()
                )
                conc_ts = conc_ts.sort_values("report_date")
                fig_conc = go.Figure()
                fig_conc.add_trace(
                    go.Scatter(x=conc_ts["report_date"], y=conc_ts["top5"], mode="lines+markers", name="Top 5 share (%)")
                )
                fig_conc.add_trace(
                    go.Scatter(x=conc_ts["report_date"], y=conc_ts["top10"], mode="lines+markers", name="Top 10 share (%)")
                )
                fig_conc.add_trace(
                    go.Scatter(x=conc_ts["report_date"], y=conc_ts["hhi"], mode="lines+markers", name="HHI (×10000)", yaxis="y2")
                )
                fig_conc.update_layout(
                    title=f"Concentration by report date ({applied_conc_metric})",
                    xaxis_title="Report date",
                    yaxis_title="Share (%)",
                    yaxis2=dict(title="HHI", overlaying="y", side="right"),
                    height=400,
                    legend=dict(orientation="h", yanchor="top", y=-0.12),
                )
                st.plotly_chart(fig_conc, use_container_width=True)
                with st.expander("Concentration table"):
                    st.dataframe(
                        conc_ts.rename(columns={"top5": "Top 5 share (%)", "top10": "Top 10 share (%)", "hhi": "HHI"}),
                        use_container_width=True,
                        hide_index=True,
                    )

            # 7. Paths per participant (Source → Sink)
            if "Source" in df.columns and "Sink" in df.columns and account_col is not None:
                st.subheader("Paths per participant")
                df_paths = df[df[account_col].notna()].copy()
                df_paths["_path"] = (
                    df_paths["Source"].astype(str).fillna("") + " → " + df_paths["Sink"].astype(str).fillna("")
                ).str.strip(" → ")
                df_paths["_mw"] = pd.to_numeric(df_paths["MW"], errors="coerce")
                path_part = (
                    df_paths.groupby([account_col, "_path"], as_index=False)["_mw"]
                    .sum()
                )
                part_tot = path_part.groupby(account_col, as_index=False)["_mw"].sum().rename(columns={"_mw": "_tot"})
                path_part = path_part.merge(part_tot, on=account_col)
                path_part["pct_of_participant"] = (path_part["_mw"] / path_part["_tot"].replace(0, float("nan")) * 100).round(2)
                path_part_sorted = path_part.sort_values([account_col, "_mw"], ascending=[True, False])
                path_top = (
                    path_part_sorted.groupby(account_col, as_index=False)
                    .head(applied_top_n_paths)
                )
                path_display = path_top.rename(
                    columns={account_col: "Account holder", "_path": "Path", "_mw": "MW", "pct_of_participant": "% of participant MW"}
                )[["Account holder", "Path", "MW", "% of participant MW"]]
                st.dataframe(path_display, use_container_width=True, hide_index=True)

            # 8. Participation over time (MW or value by report_date for top N participants)
            if has_report_date and account_col is not None and "MW" in df.columns:
                st.subheader("Participation over time (per participant)")
                df_ts = df[df[account_col].notna()].copy()
                df_ts["_mw"] = pd.to_numeric(df_ts["MW"], errors="coerce")
                if applied_part_ts_metric == "Value" and "ShadowPricePerMWH" in df_ts.columns:
                    df_ts["_val"] = df_ts["_mw"] * pd.to_numeric(df_ts["ShadowPricePerMWH"], errors="coerce")
                    ts_col = "_val"
                    ts_label = "Value"
                else:
                    ts_col = "_mw"
                    ts_label = "MW"
                ts_by_part = df_ts.groupby([account_col, "report_date"], as_index=False)[ts_col].sum()
                part_totals = ts_by_part.groupby(account_col, as_index=False)[ts_col].sum()
                top_parts = part_totals.nlargest(applied_top_n_ts, ts_col)[account_col].tolist()
                ts_top = ts_by_part[ts_by_part[account_col].isin(top_parts)].sort_values("report_date")
                fig_ts = px.line(
                    ts_top,
                    x="report_date",
                    y=ts_col,
                    color=account_col,
                    title=f"{ts_label} by report date (top {applied_top_n_ts} participants)",
                    labels={"report_date": "Report date", ts_col: ts_label, account_col: "Account holder"},
                )
                fig_ts.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12))
                st.plotly_chart(fig_ts, use_container_width=True)

            # 9. Entry/exit (first and last report_date per AccountHolder)
            if has_report_date and account_col is not None:
                st.subheader("Entry / exit")
                df_ee = df[df[account_col].notna()][[account_col, "report_date"]].copy()
                entry_exit = (
                    df_ee.groupby(account_col)
                    .agg(first_date=("report_date", "min"), last_date=("report_date", "max"))
                    .reset_index()
                )
                nunique = df_ee.groupby(account_col)["report_date"].nunique().reset_index()
                nunique.columns = [account_col, "report_dates_count"]
                entry_exit = entry_exit.merge(nunique, on=account_col)
                entry_exit = entry_exit.sort_values("first_date")
                st.dataframe(
                    entry_exit.rename(columns={
                        account_col: "Account holder",
                        "first_date": "First report date",
                        "last_date": "Last report date",
                        "report_dates_count": "Report dates (count)",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

            # 10. Growth/decline (early vs late period by participant)
            if has_report_date and account_col is not None and "MW" in df.columns:
                st.subheader("Growth / decline (early vs late period)")
                report_dates_sorted = sorted(df["report_date"].dropna().unique().tolist())
                if len(report_dates_sorted) >= 2 * applied_period_size:
                    early_dates = report_dates_sorted[:applied_period_size]
                    late_dates = report_dates_sorted[-applied_period_size:]
                    df_g = df[df[account_col].notna()].copy()
                    df_g["_mw"] = pd.to_numeric(df_g["MW"], errors="coerce")
                    if applied_growth_metric == "Value" and "ShadowPricePerMWH" in df_g.columns:
                        df_g["_v"] = df_g["_mw"] * pd.to_numeric(df_g["ShadowPricePerMWH"], errors="coerce")
                        g_col = "_v"
                        g_label = "Value"
                    else:
                        g_col = "_mw"
                        g_label = "MW"
                    early_agg = df_g[df_g["report_date"].isin(early_dates)].groupby(account_col, as_index=False)[g_col].sum().rename(columns={g_col: "early"})
                    late_agg = df_g[df_g["report_date"].isin(late_dates)].groupby(account_col, as_index=False)[g_col].sum().rename(columns={g_col: "late"})
                    growth = early_agg.merge(late_agg, on=account_col, how="outer").fillna(0)
                    growth["change"] = growth["late"] - growth["early"]
                    growth["pct_change"] = (growth["change"] / growth["early"].replace(0, float("nan")) * 100).round(2)
                    growth = growth.sort_values("change", ascending=False).reset_index(drop=True)
                    growth_display = growth.rename(columns={
                        account_col: "Account holder",
                        "early": f"Early {g_label}",
                        "late": f"Late {g_label}",
                        "change": f"Change ({g_label})",
                        "pct_change": "% change",
                    })
                    st.caption(f"Early = first {applied_period_size} report dates; Late = last {applied_period_size} report dates.")
                    st.dataframe(growth_display, use_container_width=True, hide_index=True)
                else:
                    st.caption("Need at least twice the period size in report dates to compare early vs late.")

    def _run_binding_constraints(self) -> None:
        """Run the Binding Constraints section (binding count by device, contingency, time, TOU)."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Binding Constraints")

        # Applied values (used for loading and analysis; updated only on Submit)
        defaults = {
            "binding_applied_source": "Annual",
            "binding_applied_device": "All",
            "binding_applied_contingency": "All",
            "binding_applied_top_n_devices": 15,
            "binding_applied_top_n_cont": 15,
            "binding_applied_top_n_shadow": 15,
            "binding_applied_top_n_hot": 15,
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v
        applied_source = st.session_state["binding_applied_source"]
        applied_device = st.session_state["binding_applied_device"]
        applied_contingency = st.session_state["binding_applied_contingency"]
        applied_top_n_devices = st.session_state["binding_applied_top_n_devices"]
        applied_top_n_cont = st.session_state["binding_applied_top_n_cont"]
        applied_top_n_sp = st.session_state["binding_applied_top_n_shadow"]
        applied_top_n_hot = st.session_state["binding_applied_top_n_hot"]

        # Load data using applied source (so options can be built from current data)
        source_key = applied_source.lower()
        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        report_type = "Binding Constraint"
        path = builder.get_master_path(report_type, source_key)
        if not path.exists():
            st.info(f"No {applied_source} Binding Constraint master data. Run build_master_parquets.py to build.")
            return
        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in selected Binding Constraint table.")
            return
        st.markdown("<h2 style='text-align: center'>Binding Constraints</h2>", unsafe_allow_html=True)

        device_col = "DeviceName" if "DeviceName" in df.columns else None
        contingency_col = "Contingency" if "Contingency" in df.columns else None
        period_col = "CalendarPeriod" if "CalendarPeriod" in df.columns else ("report_date" if "report_date" in df.columns else None)
        tou_col = "TimeOfUse" if "TimeOfUse" in df.columns else None
        shadow_col = "ShadowPrice" if "ShadowPrice" in df.columns else None
        if shadow_col:
            df["_shadow_num"] = pd.to_numeric(df[shadow_col], errors="coerce")

        # All inputs in a form (applied on Submit)
        with st.sidebar.form(key="binding_constraints_form"):
            source_options = ["Annual", "Monthly"]
            source_index = source_options.index(applied_source) if applied_source in source_options else 0
            source = st.selectbox(
                "Data source",
                options=source_options,
                index=source_index,
                help="Annual or Monthly Binding Constraint data.",
            )
            device_options = ["All"]
            if device_col:
                device_options = ["All"] + sorted(df[device_col].dropna().astype(str).unique().tolist())
            filter_device = st.selectbox(
                "Device Name",
                options=device_options,
                index=device_options.index(applied_device) if applied_device in device_options else 0,
                help="Filter by device / path.",
            )
            contingency_options = ["All"]
            if contingency_col and not df.empty:
                contingency_options = ["All"] + sorted(df[contingency_col].dropna().astype(str).unique().tolist())
            filter_contingency = st.selectbox(
                "Contingency",
                options=contingency_options,
                index=contingency_options.index(applied_contingency) if applied_contingency in contingency_options else 0,
                help="Filter by contingency.",
            )
            st.caption("Device Name and Contingency cannot both have a value — one must be **All** when the other is chosen.")
            top_n_devices = st.slider(
                "Top N devices (binding count)",
                5, 50, applied_top_n_devices,
            )
            top_n_cont = st.slider(
                "Top N contingencies",
                5, 50, applied_top_n_cont,
            )
            top_n_sp = st.slider(
                "Top N devices (by shadow price)",
                5, 50, applied_top_n_sp,
            )
            top_hot = st.slider(
                "Top N hot flowgates (shadow)",
                5, 40, applied_top_n_hot,
            )
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["binding_applied_source"] = source
            st.session_state["binding_applied_device"] = filter_device
            st.session_state["binding_applied_contingency"] = filter_contingency
            st.session_state["binding_applied_top_n_devices"] = top_n_devices
            st.session_state["binding_applied_top_n_cont"] = top_n_cont
            st.session_state["binding_applied_top_n_shadow"] = top_n_sp
            st.session_state["binding_applied_top_n_hot"] = top_hot
            st.rerun()

        if device_col and applied_device != "All":
            df = df[df[device_col].astype(str) == applied_device].copy()
        if contingency_col and applied_contingency != "All":
            df = df[df[contingency_col].astype(str) == applied_contingency].copy()
        if df.empty:
            st.info("No rows after filtering by Device Name and Contingency.")
            return

        # 1. Binding count by device/path
        if device_col:
            st.subheader("Binding count by device / path")
            by_device = df.groupby(device_col).size().reset_index()
            by_device = by_device.rename(columns={by_device.columns[-1]: "Binding count"})
            by_device = by_device.sort_values("Binding count", ascending=False).reset_index(drop=True)
            top_devices = by_device.head(applied_top_n_devices)
            fig_dev = px.bar(
                top_devices,
                x=device_col,
                y="Binding count",
                title=f"Top {applied_top_n_devices} flowgates by number of binding events",
                labels={device_col: "Device / path"},
            )
            fig_dev.update_layout(height=max(350, min(600, 22 * len(top_devices))), xaxis_tickangle=-45, margin=dict(b=100))
            st.plotly_chart(fig_dev, use_container_width=True)
            with st.expander("Table: binding count by device"):
                st.dataframe(by_device, use_container_width=True, hide_index=True)
        else:
            st.caption("Binding count by device requires a DeviceName column in the data.")

        # 2. Binding count by contingency
        if contingency_col:
            st.subheader("Binding count by contingency")
            by_cont = df.groupby(contingency_col).size().reset_index()
            by_cont = by_cont.rename(columns={by_cont.columns[-1]: "Binding count"})
            by_cont = by_cont.sort_values("Binding count", ascending=False).reset_index(drop=True)
            top_cont = by_cont.head(applied_top_n_cont)
            fig_cont = px.bar(
                top_cont,
                x=contingency_col,
                y="Binding count",
                title=f"Top {applied_top_n_cont} contingencies by number of binding events",
                labels={contingency_col: "Contingency"},
            )
            fig_cont.update_layout(height=max(350, min(600, 22 * len(top_cont))), xaxis_tickangle=-45, margin=dict(b=80))
            st.plotly_chart(fig_cont, use_container_width=True)
            with st.expander("Table: binding count by contingency"):
                st.dataframe(by_cont, use_container_width=True, hide_index=True)
        else:
            st.caption("Binding count by contingency requires a Contingency column in the data.")

        # 3. Binding over time (by CalendarPeriod or report_date)
        if period_col:
            st.subheader("Binding over time")
            by_period = df.groupby(period_col).size().reset_index()
            by_period = by_period.rename(columns={by_period.columns[-1]: "Binding count"})
            by_period = by_period.sort_values(period_col).reset_index(drop=True)
            fig_period = px.bar(
                by_period,
                x=period_col,
                y="Binding count",
                title="Number of binding events by period",
                labels={period_col: "Period", "Binding count": "Binding count"},
            )
            fig_period.update_layout(height=400, xaxis_tickangle=-45, margin=dict(b=80))
            st.plotly_chart(fig_period, use_container_width=True)
            with st.expander("Table: binding count by period"):
                st.dataframe(by_period, use_container_width=True, hide_index=True)
        else:
            st.caption("Binding over time requires CalendarPeriod or report_date in the data.")

        # 4. Binding by TimeOfUse
        if tou_col:
            st.subheader("Binding by Time of Use")
            by_tou = df.groupby(tou_col).size().reset_index()
            by_tou = by_tou.rename(columns={by_tou.columns[-1]: "Binding count"})
            by_tou = by_tou.sort_values("Binding count", ascending=False).reset_index(drop=True)
            col_pie, col_bar = st.columns(2)
            with col_pie:
                fig_tou_pie = px.pie(
                    by_tou,
                    names=tou_col,
                    values="Binding count",
                    title="Share of binding events by Time of Use",
                )
                fig_tou_pie.update_layout(height=CHART_HEIGHT_PIE)
                st.plotly_chart(fig_tou_pie, use_container_width=True)
            with col_bar:
                fig_tou_bar = px.bar(
                    by_tou,
                    x=tou_col,
                    y="Binding count",
                    title="Count of binding events by Time of Use",
                    labels={tou_col: "Time of Use"},
                )
                fig_tou_bar.update_layout(height=CHART_HEIGHT_PIE, xaxis_tickangle=-30)
                st.plotly_chart(fig_tou_bar, use_container_width=True)
            with st.expander("Table: binding count by Time of Use"):
                st.dataframe(by_tou, use_container_width=True, hide_index=True)
        else:
            st.caption("Binding by Time of Use requires a TimeOfUse column in the data.")

        # 4b. Binding and shadow price over time (line: count and/or avg/sum shadow by period)
        if period_col:
            st.subheader("Binding and shadow price over time")
            over_time = df.groupby(period_col).size().reset_index(name="Binding count")
            over_time = over_time.sort_values(period_col).reset_index(drop=True)
            if shadow_col and "_shadow_num" in df.columns:
                sp_over = (
                    df.groupby(period_col)["_shadow_num"]
                    .agg(["mean", lambda s: s.abs().sum()])
                    .reset_index()
                )
                sp_over.columns = [period_col, "Avg shadow price ($/MW)", "Sum |shadow| ($/MW)"]
                over_time = over_time.merge(sp_over, on=period_col, how="left")
            fig_ot = go.Figure()
            fig_ot.add_trace(
                go.Scatter(
                    x=over_time[period_col].astype(str),
                    y=over_time["Binding count"],
                    mode="lines+markers",
                    name="Binding count",
                    line=dict(width=2),
                )
            )
            if shadow_col and "Avg shadow price ($/MW)" in over_time.columns:
                fig_ot.add_trace(
                    go.Scatter(
                        x=over_time[period_col].astype(str),
                        y=over_time["Avg shadow price ($/MW)"],
                        mode="lines+markers",
                        name="Avg shadow price ($/MW)",
                        yaxis="y2",
                        line=dict(width=2, dash="dot"),
                    )
                )
            layout_kw = dict(
                title="Binding count and average shadow price by period",
                xaxis_title="Period",
                yaxis_title="Binding count",
                height=400,
                legend=dict(orientation="h", yanchor="top", y=-0.12),
            )
            if shadow_col and "Avg shadow price ($/MW)" in over_time.columns:
                layout_kw["yaxis2"] = dict(title="Avg shadow price ($/MW)", overlaying="y", side="right")
            fig_ot.update_layout(**layout_kw)
            st.plotly_chart(fig_ot, use_container_width=True)
            with st.expander("Table: binding and shadow price by period"):
                st.dataframe(over_time, use_container_width=True, hide_index=True)

        # 4c. Seasonality (month-of-year or season: count and shadow price)
        if period_col:
            st.subheader("Seasonality (month / season)")
            _df_season = df.copy()
            _df_season["_period_str"] = _df_season[period_col].astype(str)
            def _month_from_period(s):
                out = []
                for v in s:
                    v = str(v)
                    if len(v) >= 7 and v[4] == "-" and v[7] == "-":
                        out.append(int(v[5:7]))
                    elif "_" in v and len(v) >= 3:
                        mon = v[:3].upper()
                        months = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
                        out.append(months.get(mon, 0))
                    else:
                        out.append(0)
                return pd.Series(out, index=s.index)
            _df_season["_month"] = _month_from_period(_df_season[period_col])
            def _season(m):
                if m in (12, 1, 2): return "Winter"
                if m in (3, 4, 5): return "Spring"
                if m in (6, 7, 8): return "Summer"
                if m in (9, 10, 11): return "Fall"
                return "Other"
            _df_season["_season"] = _df_season["_month"].map(_season)
            _df_season = _df_season[_df_season["_month"] > 0]
            if len(_df_season) > 0:
                by_season = _df_season.groupby("_season", as_index=False).size()
                by_season = by_season.rename(columns={by_season.columns[-1]: "Binding count"})
                if shadow_col and "_shadow_num" in _df_season.columns:
                    sp_season = _df_season.groupby("_season")["_shadow_num"].agg(["mean", lambda s: s.abs().sum()]).reset_index()
                    sp_season.columns = ["_season", "Avg shadow price ($/MW)", "Sum |shadow| ($/MW)"]
                    by_season = by_season.merge(sp_season, on="_season", how="left")
                order = ["Winter", "Spring", "Summer", "Fall", "Other"]
                by_season["_season"] = pd.Categorical(by_season["_season"], categories=order, ordered=True)
                by_season = by_season.sort_values("_season")
                col_s_count, col_s_sp = st.columns(2)
                with col_s_count:
                    fig_season = px.bar(
                        by_season,
                        x="_season",
                        y="Binding count",
                        title="Binding count by season",
                        labels={"_season": "Season"},
                    )
                    fig_season.update_layout(height=350)
                    st.plotly_chart(fig_season, use_container_width=True)
                if shadow_col and "Avg shadow price ($/MW)" in by_season.columns:
                    with col_s_sp:
                        fig_season_sp = px.bar(
                            by_season,
                            x="_season",
                            y="Avg shadow price ($/MW)",
                            title="Avg shadow price by season",
                            labels={"_season": "Season"},
                        )
                        fig_season_sp.update_layout(height=350)
                        st.plotly_chart(fig_season_sp, use_container_width=True)
                with st.expander("Table: count and shadow price by season"):
                    st.dataframe(by_season.rename(columns={"_season": "Season"}), use_container_width=True, hide_index=True)
            else:
                st.caption("Could not parse month/season from period column.")

        # 4d. TimeOfUse over time (stacked area or grouped bar by period, split by TOU)
        if period_col and tou_col:
            st.subheader("Time of Use over time")
            tou_over = df.groupby([period_col, tou_col]).size().reset_index(name="Binding count")
            tou_over = tou_over.sort_values([period_col, tou_col])
            if shadow_col and "_shadow_num" in df.columns:
                sp_tou_over = (
                    df.groupby([period_col, tou_col])["_shadow_num"]
                    .apply(lambda s: s.abs().sum())
                    .reset_index(name="Sum |shadow| ($/MW)")
                )
                tou_over = tou_over.merge(sp_tou_over, on=[period_col, tou_col], how="left")
            fig_tou_stacked = px.area(
                tou_over,
                x=period_col,
                y="Binding count",
                color=tou_col,
                title="Binding count by period (stacked by Time of Use)",
                labels={period_col: "Period", "Binding count": "Binding count", tou_col: "Time of Use"},
            )
            fig_tou_stacked.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12))
            st.plotly_chart(fig_tou_stacked, use_container_width=True)
            fig_tou_grouped = px.bar(
                tou_over,
                x=period_col,
                y="Binding count",
                color=tou_col,
                barmode="group",
                title="Binding count by period (grouped by Time of Use)",
                labels={period_col: "Period", "Binding count": "Binding count", tou_col: "Time of Use"},
            )
            fig_tou_grouped.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12), xaxis_tickangle=-45)
            st.plotly_chart(fig_tou_grouped, use_container_width=True)
            if shadow_col and "Sum |shadow| ($/MW)" in tou_over.columns:
                fig_tou_sp = px.area(
                    tou_over,
                    x=period_col,
                    y="Sum |shadow| ($/MW)",
                    color=tou_col,
                    title="Shadow price impact by period (stacked by Time of Use)",
                    labels={period_col: "Period", "Sum |shadow| ($/MW)": "Sum |shadow| ($/MW)", tou_col: "Time of Use"},
                )
                fig_tou_sp.update_layout(height=400, legend=dict(orientation="h", yanchor="top", y=-0.12))
                st.plotly_chart(fig_tou_sp, use_container_width=True)
            with st.expander("Table: binding count and shadow by period and Time of Use"):
                st.dataframe(tou_over, use_container_width=True, hide_index=True)
        elif period_col and not tou_col:
            st.caption("Time of Use over time requires a TimeOfUse column in the data.")

        # Shadow price analyses (require ShadowPrice column)
        if shadow_col:
            df_shadow = df[df["_shadow_num"].notna()].copy()
        else:
            df_shadow = pd.DataFrame()

        if shadow_col and not df_shadow.empty:
            # 5. Distribution of shadow prices
            st.subheader("Distribution of shadow prices")
            ser = df_shadow["_shadow_num"]
            col_hist_sp, col_stats_sp = st.columns([2, 1])
            with col_hist_sp:
                fig_sp_hist = px.histogram(
                    df_shadow,
                    x="_shadow_num",
                    nbins=min(40, max(15, len(df_shadow) // 20)),
                    title="Histogram of shadow price ($/MW)",
                    labels={"_shadow_num": "Shadow price ($/MW)", "y": "Count"},
                )
                fig_sp_hist.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_sp_hist, use_container_width=True)
            with col_stats_sp:
                qs = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
                quant = ser.quantile(qs)
                iqr = ser.quantile(0.75) - ser.quantile(0.25)
                stats_df = pd.DataFrame({
                    "Statistic": [
                        "Count", "Mean", "Median", "Min", "Max",
                        "1st %", "5th %", "10th %", "90th %", "95th %", "99th %", "IQR",
                    ],
                    "Value": [
                        int(ser.size),
                        round(ser.mean(), 4),
                        round(ser.median(), 4),
                        round(ser.min(), 4),
                        round(ser.max(), 4),
                        round(quant.iloc[0], 4),
                        round(quant.iloc[1], 4),
                        round(quant.iloc[2], 4),
                        round(quant.iloc[6], 4),
                        round(quant.iloc[7], 4),
                        round(quant.iloc[8], 4),
                        round(iqr, 4),
                    ],
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
                st.caption("All values above are in $/MW.")
            with st.expander("Full summary stats (skewness, kurtosis)"):
                st.dataframe(
                    pd.DataFrame({
                        "Statistic": ["Skewness", "Kurtosis"],
                        "Value": [round(ser.skew(), 4), round(ser.kurtosis(), 4)],
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

            # 6. Top constraints by shadow price (by device)
            if device_col:
                st.subheader("Top constraints by shadow price")
                by_dev_sp = (
                    df_shadow.groupby(device_col, as_index=False)
                    .agg(
                        binding_count=("_shadow_num", "count"),
                        avg_shadow=("_shadow_num", "mean"),
                        max_shadow=("_shadow_num", "max"),
                        max_abs_shadow=("_shadow_num", lambda s: s.abs().max()),
                    )
                )
                by_dev_sp = by_dev_sp.rename(columns={
                    "binding_count": "Binding count",
                    "avg_shadow": "Avg shadow price ($/MW)",
                    "max_shadow": "Max shadow price ($/MW)",
                    "max_abs_shadow": "Max |shadow price| ($/MW)",
                })
                by_dev_sp = by_dev_sp.sort_values("Max |shadow price| ($/MW)", ascending=False).reset_index(drop=True)
                top_dev_sp = by_dev_sp.head(applied_top_n_sp)
                fig_top_sp = px.bar(
                    top_dev_sp,
                    x=device_col,
                    y="Max |shadow price| ($/MW)",
                    title=f"Top {applied_top_n_sp} flowgates by max |shadow price| ($/MW)",
                    labels={device_col: "Device / path", "Max |shadow price| ($/MW)": "Max |Shadow price| ($/MW)"},
                )
                fig_top_sp.update_layout(height=max(350, min(600, 22 * len(top_dev_sp))), xaxis_tickangle=-45, margin=dict(b=100))
                st.plotly_chart(fig_top_sp, use_container_width=True)
                with st.expander("Table: top constraints by shadow price (per device)"):
                    st.dataframe(by_dev_sp, use_container_width=True, hide_index=True)

            # 7. Shadow price by device/path (count, avg, max)
            if device_col:
                st.subheader("Shadow price by device / path")
                sp_dev_agg = (
                    df_shadow.groupby(device_col, as_index=False)
                    .agg(
                        binding_count=("_shadow_num", "count"),
                        avg_shadow_price=("_shadow_num", "mean"),
                        max_shadow_price=("_shadow_num", "max"),
                    )
                )
                sp_dev_agg = sp_dev_agg.rename(columns={
                    "binding_count": "Binding count",
                    "avg_shadow_price": "Avg shadow price ($/MW)",
                    "max_shadow_price": "Max shadow price ($/MW)",
                })
                sp_dev_agg = sp_dev_agg.sort_values("Max shadow price ($/MW)", ascending=False).reset_index(drop=True)
                sp_hot = sp_dev_agg.head(applied_top_n_hot)
                fig_hot = px.bar(
                    sp_hot,
                    x=device_col,
                    y=["Avg shadow price ($/MW)", "Max shadow price ($/MW)"],
                    barmode="group",
                    title=f"Hot flowgates: avg and max shadow price (top {applied_top_n_hot})",
                    labels={device_col: "Device / path", "value": "$/MW"},
                )
                fig_hot.update_layout(height=max(350, min(550, 22 * len(sp_hot))), xaxis_tickangle=-45, margin=dict(b=100))
                st.plotly_chart(fig_hot, use_container_width=True)
                with st.expander("Table: shadow price by device (count, avg, max)"):
                    st.dataframe(sp_dev_agg, use_container_width=True, hide_index=True)

            # 8. Shadow price by contingency
            if contingency_col:
                st.subheader("Shadow price by contingency")
                sp_cont_agg = (
                    df_shadow.groupby(contingency_col, as_index=False)
                    .agg(
                        binding_count=("_shadow_num", "count"),
                        avg_shadow_price=("_shadow_num", "mean"),
                        max_shadow_price=("_shadow_num", "max"),
                    )
                )
                sp_cont_agg = sp_cont_agg.rename(columns={
                    "binding_count": "Binding count",
                    "avg_shadow_price": "Avg shadow price ($/MW)",
                    "max_shadow_price": "Max shadow price ($/MW)",
                })
                sp_cont_agg = sp_cont_agg.sort_values("Max shadow price ($/MW)", ascending=False).reset_index(drop=True)
                top_cont_sp = sp_cont_agg.head(20)
                fig_cont_sp = px.bar(
                    top_cont_sp,
                    x=contingency_col,
                    y=["Avg shadow price ($/MW)", "Max shadow price ($/MW)"],
                    barmode="group",
                    title="Shadow price by contingency (top 20 by max shadow price)",
                    labels={contingency_col: "Contingency", "value": "$/MW"},
                )
                fig_cont_sp.update_layout(height=400, xaxis_tickangle=-45, margin=dict(b=80))
                st.plotly_chart(fig_cont_sp, use_container_width=True)
                with st.expander("Table: shadow price by contingency"):
                    st.dataframe(sp_cont_agg, use_container_width=True, hide_index=True)

            # 9. Shadow price by TimeOfUse
            if tou_col:
                st.subheader("Shadow price by Time of Use")
                sp_tou_agg = (
                    df_shadow.groupby(tou_col, as_index=False)
                    .agg(
                        binding_count=("_shadow_num", "count"),
                        avg_shadow_price=("_shadow_num", "mean"),
                        total_shadow_exposure=("_shadow_num", lambda s: s.abs().sum()),
                    )
                )
                sp_tou_agg = sp_tou_agg.rename(columns={
                    "binding_count": "Binding count",
                    "avg_shadow_price": "Avg shadow price ($/MW)",
                    "total_shadow_exposure": "Sum |shadow price| ($/MW)",
                })
                sp_tou_agg = sp_tou_agg.sort_values("Avg shadow price ($/MW)", ascending=False).reset_index(drop=True)
                fig_tou_sp = px.bar(
                    sp_tou_agg,
                    x=tou_col,
                    y=["Avg shadow price ($/MW)", "Sum |shadow price| ($/MW)"],
                    barmode="group",
                    title="Average and total |shadow price| by Time of Use ($/MW)",
                    labels={tou_col: "Time of Use", "value": "Shadow price ($/MW)"},
                )
                fig_tou_sp.update_layout(height=400, xaxis_tickangle=-30)
                st.plotly_chart(fig_tou_sp, use_container_width=True)
                with st.expander("Table: shadow price by Time of Use"):
                    st.dataframe(sp_tou_agg, use_container_width=True, hide_index=True)

        # 10. Path summary table (binding count, avg/max shadow price, typical TimeOfUse per path)
        direction_col = "Direction" if "Direction" in df.columns else None
        if device_col:
            st.subheader("Path summary table")
            path_group_cols = [device_col]
            if direction_col:
                path_group_cols.append(direction_col)
                df_path_sum = df.copy()
                df_path_sum["_path_label"] = (
                    df_path_sum[device_col].astype(str) + " (" + df_path_sum[direction_col].astype(str) + ")"
                )
            else:
                df_path_sum = df.copy()
                df_path_sum["_path_label"] = df_path_sum[device_col].astype(str)
            path_sum = df_path_sum.groupby("_path_label").size().reset_index()
            path_sum = path_sum.rename(columns={path_sum.columns[-1]: "Binding count"})
            if shadow_col and "_shadow_num" in df_path_sum.columns:
                sh_agg = df_path_sum.groupby("_path_label")["_shadow_num"].agg(["mean", "max"]).reset_index()
                sh_agg.columns = ["_path_label", "Avg shadow price ($/MW)", "Max shadow price ($/MW)"]
                path_sum = path_sum.merge(sh_agg, on="_path_label")
            if tou_col and tou_col in df_path_sum.columns:
                def mode_tou(s):
                    m = s.mode()
                    return m.iloc[0] if len(m) > 0 else None
                tou_mode = df_path_sum.groupby("_path_label")[tou_col].apply(mode_tou).reset_index()
                tou_mode.columns = ["_path_label", "Typical Time of Use"]
                path_sum = path_sum.merge(tou_mode, on="_path_label")
            path_sum = path_sum.sort_values("Binding count", ascending=False).reset_index(drop=True)
            path_display = path_sum.rename(columns={"_path_label": "Path"})
            st.dataframe(path_display, use_container_width=True, hide_index=True)

        # 11. Direction (From - To vs To - From: frequency and shadow price)
        if direction_col:
            st.subheader("Direction (From - To vs To - From)")
            by_dir = df.groupby(direction_col).size().reset_index()
            by_dir = by_dir.rename(columns={by_dir.columns[-1]: "Binding count"})
            by_dir = by_dir.sort_values("Binding count", ascending=False)
            if shadow_col and "_shadow_num" in df.columns:
                sp_dir = df.groupby(direction_col)["_shadow_num"].agg(["mean", "max"]).reset_index()
                sp_dir.columns = [direction_col, "Avg shadow price ($/MW)", "Max shadow price ($/MW)"]
                by_dir = by_dir.merge(sp_dir, on=direction_col)
            col_dir_count, col_dir_sp = st.columns(2)
            with col_dir_count:
                fig_dir = px.bar(
                    by_dir,
                    x=direction_col,
                    y="Binding count",
                    title="Binding count by direction",
                    labels={direction_col: "Direction"},
                )
                fig_dir.update_layout(height=350, xaxis_tickangle=-30)
                st.plotly_chart(fig_dir, use_container_width=True)
            if shadow_col and "Avg shadow price ($/MW)" in by_dir.columns:
                with col_dir_sp:
                    fig_dir_sp = px.bar(
                        by_dir,
                        x=direction_col,
                        y=["Avg shadow price ($/MW)", "Max shadow price ($/MW)"],
                        barmode="group",
                        title="Shadow price by direction",
                        labels={direction_col: "Direction", "value": "$/MW"},
                    )
                    fig_dir_sp.update_layout(height=350, xaxis_tickangle=-30)
                    st.plotly_chart(fig_dir_sp, use_container_width=True)
            with st.expander("Table: direction (count and shadow price)"):
                st.dataframe(by_dir.rename(columns={direction_col: "Direction"}), use_container_width=True, hide_index=True)
        else:
            st.caption("Direction analysis requires a Direction column in the data.")

        # 12. Flow vs limit (utilization when binding)
        if "Flow" in df.columns and "Limit" in df.columns:
            st.subheader("Flow vs limit (constraint tightness)")
            _flow = pd.to_numeric(df["Flow"], errors="coerce")
            _limit = pd.to_numeric(df["Limit"], errors="coerce")
            valid = _limit != 0
            utilization = (_flow / _limit).where(valid)
            utilization_abs = (_flow.abs() / _limit).where(valid)
            u_clean = utilization_abs.dropna()
            u_clean = u_clean[u_clean < 10]
            if len(u_clean) > 0:
                col_hist_util, col_scatter = st.columns(2)
                with col_hist_util:
                    fig_util = px.histogram(
                        x=u_clean,
                        nbins=min(40, max(15, len(u_clean) // 20)),
                        title="Histogram of utilization |Flow|/Limit when binding",
                        labels={"x": "|Flow| / Limit", "y": "Count"},
                    )
                    fig_util.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig_util, use_container_width=True)
                with col_scatter:
                    scat_df = df.loc[valid].copy()
                    scat_df["_flow_num"] = pd.to_numeric(scat_df["Flow"], errors="coerce")
                    scat_df["_limit_num"] = pd.to_numeric(scat_df["Limit"], errors="coerce")
                    scat_df = scat_df.dropna(subset=["_flow_num", "_limit_num"])
                    if len(scat_df) > 0:
                        fig_scatter_fl = px.scatter(
                            scat_df.head(2000),
                            x="_limit_num",
                            y="_flow_num",
                            title="Flow vs Limit (sample)",
                            labels={"_limit_num": "Limit", "_flow_num": "Flow"},
                        )
                        fig_scatter_fl.update_layout(height=400)
                        st.plotly_chart(fig_scatter_fl, use_container_width=True)
                with st.expander("Utilization stats (|Flow|/Limit)"):
                    u_stats = pd.DataFrame({
                        "Statistic": ["Count", "Mean", "Median", "Min", "Max", "Std"],
                        "Value": [
                            int(u_clean.size),
                            round(u_clean.mean(), 4),
                            round(u_clean.median(), 4),
                            round(u_clean.min(), 4),
                            round(u_clean.max(), 4),
                            round(u_clean.std(), 4),
                        ],
                    })
                    st.dataframe(u_stats, use_container_width=True, hide_index=True)
            else:
                st.caption("No valid utilization (Flow/Limit) values after filtering.")
        else:
            st.caption("Flow vs limit analysis requires Flow and Limit columns in the data.")

        # 13. Contingency × device (pairs that bind most or have highest shadow prices)
        if contingency_col and device_col:
            st.subheader("Contingency × device")
            cont_dev_count = df.groupby([contingency_col, device_col]).size().reset_index(name="Binding count")
            if shadow_col and "_shadow_num" in df.columns:
                cont_dev_sp = (
                    df.groupby([contingency_col, device_col])["_shadow_num"]
                    .agg(["mean", "max", lambda s: s.abs().sum()])
                    .reset_index()
                )
                cont_dev_sp.columns = [contingency_col, device_col, "Avg shadow price ($/MW)", "Max shadow price ($/MW)", "Sum |shadow| ($/MW)"]
                cont_dev = cont_dev_count.merge(
                    cont_dev_sp,
                    on=[contingency_col, device_col],
                    how="left",
                )
            else:
                cont_dev = cont_dev_count
            cont_dev = cont_dev.sort_values("Binding count", ascending=False).reset_index(drop=True)
            with st.expander("Table: (Contingency, Device) pairs by binding count and shadow price"):
                st.dataframe(
                    cont_dev.rename(columns={contingency_col: "Contingency", device_col: "Device / path"}),
                    use_container_width=True,
                    hide_index=True,
                )
            # Heatmap: top contingencies × top devices by binding count
            top_cont_n = min(15, cont_dev[contingency_col].nunique())
            top_dev_n = min(15, cont_dev[device_col].nunique())
            top_cont_list = cont_dev.groupby(contingency_col)["Binding count"].sum().nlargest(top_cont_n).index.tolist()
            top_dev_list = cont_dev.groupby(device_col)["Binding count"].sum().nlargest(top_dev_n).index.tolist()
            cont_dev_sub = cont_dev[
                cont_dev[contingency_col].isin(top_cont_list) & cont_dev[device_col].isin(top_dev_list)
            ]
            if not cont_dev_sub.empty:
                pivot_count = cont_dev_sub.pivot_table(
                    index=contingency_col,
                    columns=device_col,
                    values="Binding count",
                    aggfunc="sum",
                    fill_value=0,
                )
                fig_heat = go.Figure(
                    data=go.Heatmap(
                        z=pivot_count.values,
                        x=pivot_count.columns.tolist(),
                        y=pivot_count.index.tolist(),
                        colorscale="Blues",
                        colorbar=dict(title="Binding count"),
                    )
                )
                fig_heat.update_layout(
                    title=f"Contingency × device: binding count (top {top_cont_n} contingencies × top {top_dev_n} devices)",
                    xaxis_title="Device / path",
                    yaxis_title="Contingency",
                    height=max(400, 25 * len(pivot_count.index)),
                        xaxis_tickangle=-45,
                )
                st.plotly_chart(fig_heat, use_container_width=True)

        # 14. Top contingencies (rank by count and by total/max shadow price)
        if contingency_col:
            st.subheader("Top contingencies")
            top_cont_by_count = df.groupby(contingency_col).size().reset_index(name="Binding count")
            top_cont_by_count = top_cont_by_count.sort_values("Binding count", ascending=False).reset_index(drop=True)
            if shadow_col and "_shadow_num" in df.columns:
                top_cont_sp = (
                    df.groupby(contingency_col)["_shadow_num"]
                    .agg(["mean", "max", lambda s: s.abs().sum()])
                    .reset_index()
                )
                top_cont_sp.columns = [contingency_col, "Avg shadow price ($/MW)", "Max shadow price ($/MW)", "Sum |shadow| ($/MW)"]
                top_cont = top_cont_by_count.merge(
                    top_cont_sp,
                    on=contingency_col,
                    how="left",
                )
            else:
                top_cont = top_cont_by_count
            top_cont = top_cont.sort_values("Binding count", ascending=False).reset_index(drop=True)
            st.dataframe(
                top_cont.rename(columns={contingency_col: "Contingency"}),
                use_container_width=True,
                hide_index=True,
            )
            col_tc_count, col_tc_sp = st.columns(2)
            top_n_tc = min(15, len(top_cont))
            with col_tc_count:
                fig_tc_count = px.bar(
                    top_cont.head(top_n_tc),
                    x=contingency_col,
                    y="Binding count",
                    title=f"Top {top_n_tc} contingencies by binding count",
                    labels={contingency_col: "Contingency"},
                )
                fig_tc_count.update_layout(height=350, xaxis_tickangle=-45)
                st.plotly_chart(fig_tc_count, use_container_width=True)
            if shadow_col and "Max shadow price ($/MW)" in top_cont.columns:
                with col_tc_sp:
                    top_cont_by_max = top_cont.sort_values("Max shadow price ($/MW)", ascending=False).head(top_n_tc)
                    fig_tc_sp = px.bar(
                        top_cont_by_max,
                        x=contingency_col,
                        y="Max shadow price ($/MW)",
                        title=f"Top {top_n_tc} contingencies by max shadow price",
                        labels={contingency_col: "Contingency"},
                    )
                    fig_tc_sp.update_layout(height=350, xaxis_tickangle=-45)
                    st.plotly_chart(fig_tc_sp, use_container_width=True)

        if not shadow_col:
            st.caption("Shadow price analyses require a ShadowPrice column in the data.")
        elif shadow_col and df_shadow.empty:
            st.caption("Shadow price distribution and analyses require non-null ShadowPrice values.")

    def _run_shadow_prices(self) -> None:
        """Run the Shadow Prices section (SourceSink shadow prices: distribution, FTR/CRR targets, temporal patterns)."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Shadow Prices")
        if "sp_applied_source" not in st.session_state:
            st.session_state["sp_applied_source"] = "Annual"
        if "sp_applied_period" not in st.session_state:
            st.session_state["sp_applied_period"] = "All"
        if "sp_applied_tou" not in st.session_state:
            st.session_state["sp_applied_tou"] = "All"
        if "sp_applied_path" not in st.session_state:
            st.session_state["sp_applied_path"] = "All"
        applied_source = st.session_state["sp_applied_source"]
        applied_period = st.session_state["sp_applied_period"]
        applied_tou = st.session_state["sp_applied_tou"]
        applied_path = st.session_state["sp_applied_path"]

        source_key = applied_source.lower()
        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        path = builder.get_master_path("Shadow Prices", source_key)
        if not path.exists():
            st.info("No Shadow Prices master data. Run build_master_parquets.py to build.")
            return
        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in Shadow Prices table.")
            return
        st.markdown("<h2 style='text-align: center'>Shadow Prices</h2>", unsafe_allow_html=True)

        path_col = "SourceSink" if "SourceSink" in df.columns else ("Source" if "Source" in df.columns else None)
        period_col = "CalendarPeriod" if "CalendarPeriod" in df.columns else ("report_date" if "report_date" in df.columns else None)
        tou_col = "TimeOfUse" if "TimeOfUse" in df.columns else None
        price_col = "ShadowPricePerMWH" if "ShadowPricePerMWH" in df.columns else ("ShadowPrice" if "ShadowPrice" in df.columns else None)
        if not price_col:
            st.caption("Shadow price column (ShadowPricePerMWH or ShadowPrice) not found.")
            return
        df["_price_num"] = pd.to_numeric(df[price_col], errors="coerce")
        df = df[df["_price_num"].notna()].copy()

        period_options = ["All"]
        if period_col:
            period_options += sorted(df[period_col].dropna().astype(str).unique().tolist())
        tou_options = ["All"]
        if tou_col:
            tou_options += sorted(df[tou_col].dropna().astype(str).unique().tolist())
        path_options = ["All"]
        if path_col:
            path_options += sorted(df[path_col].dropna().astype(str).unique().tolist())

        with st.sidebar.form(key="shadow_prices_form"):
            source = st.selectbox("Data source", ["Annual", "Monthly"], index=0 if applied_source == "Annual" else 1)
            path_sel = st.selectbox(
                "Source / Sink",
                path_options,
                index=path_options.index(applied_path) if applied_path in path_options else 0,
                help="Filter by path (SourceSink).",
            )
            period_sel = st.selectbox("Calendar period", period_options, index=period_options.index(applied_period) if applied_period in period_options else 0)
            tou_sel = st.selectbox("Time of Use", tou_options, index=tou_options.index(applied_tou) if applied_tou in tou_options else 0)
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["sp_applied_source"] = source
            st.session_state["sp_applied_path"] = path_sel
            st.session_state["sp_applied_period"] = period_sel
            st.session_state["sp_applied_tou"] = tou_sel
            st.rerun()
        if applied_path != "All" and path_col:
            df = df[df[path_col].astype(str) == applied_path].copy()
        if applied_period != "All" and period_col:
            df = df[df[period_col].astype(str) == applied_period].copy()
        if applied_tou != "All" and tou_col:
            df = df[df[tou_col].astype(str) == applied_tou].copy()
        if df.empty:
            st.info("No rows after filters.")
            return

        # 1. Distribution of shadow prices (positive vs negative, histogram, stats)
        st.subheader("Distribution of shadow prices")
        st.caption("Positive shadow prices: binding constraint; relaxing by 1 MWh reduces system cost. Negative: constraint binding in opposite sense.")
        ser = df["_price_num"]
        col_hist, col_stats = st.columns([2, 1])
        with col_hist:
            fig_sp = px.histogram(
                df,
                x="_price_num",
                nbins=min(50, max(20, len(df) // 30)),
                title="Shadow price ($/MW) distribution",
                labels={"_price_num": "Shadow price ($/MW)", "y": "Count"},
            )
            fig_sp.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_sp, use_container_width=True)
        with col_stats:
            pos = ser[ser > 0]
            neg = ser[ser < 0]
            stats_list = [
                ("Count", int(ser.size)),
                ("Mean", round(ser.mean(), 4)),
                ("Median", round(ser.median(), 4)),
                ("Min", round(ser.min(), 4)),
                ("Max", round(ser.max(), 4)),
                ("Positive count", int(pos.size)),
                ("Negative count", int(neg.size)),
            ]
            st.dataframe(pd.DataFrame(stats_list, columns=["Statistic", "Value"]), use_container_width=True, hide_index=True)
        with st.expander("Full stats (percentiles, IQR)"):
            qs = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
            qv = ser.quantile(qs)
            st.dataframe(pd.DataFrame({"Quantile": [f"{int(q*100)}%" for q in qs], "Value": qv.tolist()}), use_container_width=True, hide_index=True)

        # 2. Top paths for FTR/CRR (highest positive, most negative)
        if path_col:
            st.subheader("Top paths by shadow price (FTR/CRR targeting)")
            path_agg = (
                df.groupby(path_col)["_price_num"]
                .agg(["count", "mean", "max", "min"])
                .reset_index()
            )
            path_agg.columns = [path_col, "Count", "Avg ($/MW)", "Max ($/MW)", "Min ($/MW)"]
            top_pos = path_agg.nlargest(15, "Max ($/MW)")
            top_neg = path_agg.nsmallest(15, "Min ($/MW)")
            col_pos, col_neg = st.columns(2)
            with col_pos:
                fig_pos = px.bar(
                    top_pos,
                    x=path_col,
                    y="Max ($/MW)",
                    title="Top 15 paths by max shadow price (FTR/CRR long)",
                    labels={path_col: "Path", "Max ($/MW)": "Max shadow ($/MW)"},
                )
                fig_pos.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_pos, use_container_width=True)
            with col_neg:
                fig_neg = px.bar(
                    top_neg,
                    x=path_col,
                    y="Min ($/MW)",
                    title="Top 15 paths by min shadow price (reverse / short)",
                    labels={path_col: "Path", "Min ($/MW)": "Min shadow ($/MW)"},
                )
                fig_neg.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_neg, use_container_width=True)
            with st.expander("Table: path summary (count, avg, max, min)"):
                path_agg_sorted = path_agg.sort_values("Max ($/MW)", ascending=False)
                st.dataframe(path_agg_sorted.rename(columns={path_col: "Path"}), use_container_width=True, hide_index=True)

        # 3. Path summary with typical CalendarPeriod and TimeOfUse
        if path_col:
            st.subheader("Path summary (typical period and TOU)")
            def _mode(s):
                m = s.mode()
                return m.iloc[0] if len(m) > 0 else None
            path_summary = df.groupby(path_col).agg(
                count=("_price_num", "count"),
                avg_price=("_price_num", "mean"),
                max_price=("_price_num", "max"),
                min_price=("_price_num", "min"),
            ).reset_index()
            path_summary.columns = [path_col, "Count", "Avg ($/MW)", "Max ($/MW)", "Min ($/MW)"]
            if period_col:
                pmode = df.groupby(path_col)[period_col].apply(_mode).reset_index()
                pmode.columns = [path_col, "Typical period"]
                path_summary = path_summary.merge(pmode, on=path_col, how="left")
            if tou_col:
                tmode = df.groupby(path_col)[tou_col].apply(_mode).reset_index()
                tmode.columns = [path_col, "Typical TOU"]
                path_summary = path_summary.merge(tmode, on=path_col, how="left")
            path_summary = path_summary.sort_values("Max ($/MW)", ascending=False)
            st.dataframe(path_summary.rename(columns={path_col: "Path"}), use_container_width=True, hide_index=True)

        # 4. Shadow price by CalendarPeriod / time
        if period_col:
            st.subheader("Shadow price by period")
            by_period = df.groupby(period_col)["_price_num"].agg(["count", "mean", "max"]).reset_index()
            by_period.columns = [period_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
            by_period = by_period.sort_values(period_col)
            fig_per = go.Figure()
            fig_per.add_trace(go.Scatter(x=by_period[period_col].astype(str), y=by_period["Count"], mode="lines+markers", name="Count"))
            fig_per.add_trace(go.Scatter(x=by_period[period_col].astype(str), y=by_period["Avg ($/MW)"], mode="lines+markers", name="Avg ($/MW)", yaxis="y2"))
            fig_per.update_layout(
                title="Binding count and avg shadow price by period",
                xaxis_title="Period",
                yaxis_title="Count",
                yaxis2=dict(title="Avg shadow ($/MW)", overlaying="y", side="right"),
                height=400,
                legend=dict(orientation="h", yanchor="top", y=-0.12),
            )
            st.plotly_chart(fig_per, use_container_width=True)
            with st.expander("Table: by period"):
                st.dataframe(by_period, use_container_width=True, hide_index=True)

        # 5. Shadow price by TimeOfUse
        if tou_col:
            st.subheader("Shadow price by Time of Use")
            by_tou = df.groupby(tou_col)["_price_num"].agg(["count", "mean", "max"]).reset_index()
            by_tou.columns = [tou_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
            by_tou = by_tou.sort_values("Avg ($/MW)", ascending=False)
            fig_tou = px.bar(
                by_tou,
                x=tou_col,
                y=["Count", "Avg ($/MW)", "Max ($/MW)"],
                        barmode="group",
                title="Count and shadow price by Time of Use",
                labels={tou_col: "Time of Use", "value": "Value"},
            )
            fig_tou.update_layout(height=400, xaxis_tickangle=-30)
            st.plotly_chart(fig_tou, use_container_width=True)
            with st.expander("Table: by Time of Use"):
                st.dataframe(by_tou, use_container_width=True, hide_index=True)

        # 6. Seasonality (month/season from CalendarPeriod or report_date)
        if period_col:
            st.subheader("Seasonality (month / season)")
            _df = df.copy()
            def _month_from(s):
                out = []
                for v in s:
                    v = str(v)
                    if len(v) >= 7 and v[4] == "-" and v[7] == "-":
                        out.append(int(v[5:7]))
                    elif "_" in v and len(v) >= 3:
                        mon = v[:3].upper()
                        months = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}
                        out.append(months.get(mon, 0))
                    else:
                        out.append(0)
                return pd.Series(out, index=s.index)
            _df["_month"] = _month_from(_df[period_col])
            def _season(m):
                if m in (12, 1, 2): return "Winter"
                if m in (3, 4, 5): return "Spring"
                if m in (6, 7, 8): return "Summer"
                if m in (9, 10, 11): return "Fall"
                return "Other"
            _df["_season"] = _df["_month"].map(_season)
            _df = _df[_df["_month"] > 0]
            if len(_df) > 0:
                by_season = _df.groupby("_season")["_price_num"].agg(["count", "mean", "max"]).reset_index()
                by_season.columns = ["Season", "Count", "Avg ($/MW)", "Max ($/MW)"]
                order = ["Winter", "Spring", "Summer", "Fall", "Other"]
                by_season["Season"] = pd.Categorical(by_season["Season"], categories=order, ordered=True)
                by_season = by_season.sort_values("Season")
                fig_season = px.bar(
                    by_season,
                    x="Season",
                    y=["Count", "Avg ($/MW)"],
                        barmode="group",
                    title="Count and avg shadow price by season",
                )
                fig_season.update_layout(height=350)
                st.plotly_chart(fig_season, use_container_width=True)
                with st.expander("Table: by season"):
                    st.dataframe(by_season, use_container_width=True, hide_index=True)
            else:
                st.caption("Could not parse month/season from period.")

        # 7. Data table (sort by |shadow price|)
        st.subheader("Shadow price table")
        df_display = df.copy()
        df_display["|Shadow price|"] = df_display["_price_num"].abs()
        df_display = df_display.sort_values("|Shadow price|", ascending=False)
        cols_show = [path_col, period_col, tou_col, price_col, "|Shadow price|"]
        cols_show = [c for c in cols_show if c and c in df_display.columns]
        st.dataframe(df_display[cols_show].head(500), use_container_width=True, hide_index=True)
        with st.expander("All rows (export)"):
            st.dataframe(df_display[cols_show], use_container_width=True, hide_index=True)

    def _run_cleared_results(self) -> None:
        """Run the Cleared Results section: CRR trader insights and practical checklist."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Cleared Results")
        if "cr_applied_source" not in st.session_state:
            st.session_state["cr_applied_source"] = "Annual"
        if "cr_applied_path" not in st.session_state:
            st.session_state["cr_applied_path"] = "All"
        if "cr_applied_period" not in st.session_state:
            st.session_state["cr_applied_period"] = "All"
        if "cr_applied_tou" not in st.session_state:
            st.session_state["cr_applied_tou"] = "All"
        applied_source = st.session_state["cr_applied_source"]
        applied_path = st.session_state["cr_applied_path"]
        applied_period = st.session_state["cr_applied_period"]
        applied_tou = st.session_state["cr_applied_tou"]

        source_key = applied_source.lower()
        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        path = builder.get_master_path("Auction Results", source_key)
        if not path.exists():
            st.info("No Cleared Results (Auction Results) master data. Run build_master_parquets.py to build.")
            return
        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in Cleared Results table.")
            return
        st.markdown("<h2 style='text-align: center'>Cleared Results</h2>", unsafe_allow_html=True)
        st.caption("Cleared CRR awards: path value, temporal patterns, hedge type, volume vs price, pre-award signal, and practical checklist for the next auction.")

        # Normalize column names for parquet (may have Source, Sink, ShadowPricePerMWH, report_date, etc.)
        if "report_date" in df.columns and "auction_date" not in df.columns:
            df = df.rename(columns={"report_date": "auction_date"})
        if "ShadowPricePerMWH" in df.columns and "clearing_price" not in df.columns:
            df = df.rename(columns={"ShadowPricePerMWH": "clearing_price"})
        if "MW" in df.columns and "mw_amount" not in df.columns:
            df = df.rename(columns={"MW": "mw_amount"})
        if "TimeOfUse" in df.columns and "time_of_use" not in df.columns:
            df = df.rename(columns={"TimeOfUse": "time_of_use"})
        if "HedgeType" in df.columns and "hedge_type" not in df.columns:
            df = df.rename(columns={"HedgeType": "hedge_type"})
        if "CRRType" in df.columns and "crr_type" not in df.columns:
            df = df.rename(columns={"CRRType": "crr_type"})
        path_col = "path_name" if "path_name" in df.columns else None
        if not path_col and "Source" in df.columns and "Sink" in df.columns:
            df["_path"] = df["Source"].astype(str) + " → " + df["Sink"].astype(str)
            path_col = "_path"
        if not path_col and "source_node" in df.columns and "sink_node" in df.columns:
            df["_path"] = df["source_node"].astype(str) + " → " + df["sink_node"].astype(str)
            path_col = "_path"
        price_col = "clearing_price" if "clearing_price" in df.columns else "ShadowPricePerMWH"
        if price_col not in df.columns:
            st.warning("No clearing/shadow price column found.")
            return
        df["_price_num"] = pd.to_numeric(df[price_col], errors="coerce")
        df = df[df["_price_num"].notna()].copy()
        if df.empty:
            st.info("No rows with valid price.")
            return

        # Sidebar filters
        period_col = "auction_date" if "auction_date" in df.columns else ("CalendarPeriod" if "CalendarPeriod" in df.columns else None)
        tou_col = "time_of_use" if "time_of_use" in df.columns else None
        period_options = ["All"]
        if period_col:
            period_options += sorted(df[period_col].dropna().astype(str).unique().tolist())
        tou_options = ["All"]
        if tou_col:
            tou_options += sorted(df[tou_col].dropna().astype(str).unique().tolist())
        path_options = ["All"]
        if path_col:
            path_options += sorted(df[path_col].dropna().astype(str).unique().tolist())
        with st.sidebar.form(key="cleared_results_form"):
            source = st.selectbox("Data source", ["Annual", "Monthly"], index=0 if applied_source == "Annual" else 1)
            path_sel = st.selectbox("Source / Sink", path_options, index=path_options.index(applied_path) if applied_path in path_options else 0, help="Filter by path.")
            period_sel = st.selectbox("Period", period_options, index=period_options.index(applied_period) if applied_period in period_options else 0)
            tou_sel = st.selectbox("Time of Use", tou_options, index=tou_options.index(applied_tou) if applied_tou in tou_options else 0)
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["cr_applied_source"] = source
            st.session_state["cr_applied_path"] = path_sel
            st.session_state["cr_applied_period"] = period_sel
            st.session_state["cr_applied_tou"] = tou_sel
            st.rerun()
        if applied_path != "All" and path_col:
            df = df[df[path_col].astype(str) == applied_path].copy()
        if applied_period != "All" and period_col:
            df = df[df[period_col].astype(str) == applied_period].copy()
        if applied_tou != "All" and tou_col:
            df = df[df[tou_col].astype(str) == applied_tou].copy()
        if df.empty:
            st.info("No rows after filters.")
            return

        # ----- 1. Path value (buy vs avoid/sell) -----
        st.subheader("Path value (Source–Sink)")
        st.caption("High clearing price → buy CRR candidates; low → avoid or sell.")
        path_agg = df.groupby(path_col)["_price_num"].agg(["count", "mean", "max", "min"]).reset_index()
        path_agg.columns = [path_col, "Count", "Avg ($/MW)", "Max ($/MW)", "Min ($/MW)"]
        path_agg = path_agg.sort_values("Max ($/MW)", ascending=False)
        top_n = 15
        col_buy, col_avoid = st.columns(2)
        with col_buy:
            st.markdown("**Top paths by max price (buy candidates)**")
            st.dataframe(path_agg.head(top_n).rename(columns={path_col: "Path"}), use_container_width=True, hide_index=True)
        with col_avoid:
            st.markdown("**Lowest-price paths (avoid / sell candidates)**")
            st.dataframe(path_agg.tail(top_n).rename(columns={path_col: "Path"}), use_container_width=True, hide_index=True)
        fig_buy = px.bar(
            path_agg.head(top_n),
            x=path_col,
            y="Max ($/MW)",
            title="Top paths by max clearing price (buy candidates)",
            labels={path_col: "Path", "Max ($/MW)": "Max price ($/MW)"},
        )
        fig_buy.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_buy, use_container_width=True)

        # ----- 2. Temporal -----
        st.subheader("Temporal patterns")
        if tou_col:
            by_tou = df.groupby(tou_col)["_price_num"].agg(["count", "mean", "max"]).reset_index()
            by_tou.columns = [tou_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
            by_tou = by_tou.sort_values("Avg ($/MW)", ascending=False)
            fig_tou = px.bar(by_tou, x=tou_col, y=["Avg ($/MW)", "Max ($/MW)"], barmode="group", title="Clearing price by Time of Use", labels={tou_col: "Time of Use", "value": "$/MW"})
            fig_tou.update_layout(height=350)
            st.plotly_chart(fig_tou, use_container_width=True)
            with st.expander("Table: by Time of Use"):
                st.dataframe(by_tou, use_container_width=True, hide_index=True)
        date_col = "auction_date" if "auction_date" in df.columns else ("StartDate" if "StartDate" in df.columns else None)
        if date_col:
            df_date = df.copy()
            df_date["_dt"] = pd.to_datetime(df_date[date_col], errors="coerce")
            df_date = df_date[df_date["_dt"].notna()].copy()
            if not df_date.empty:
                df_date["_month"] = df_date["_dt"].dt.month
                by_month = df_date.groupby("_month")["_price_num"].agg(["count", "mean", "max"]).reset_index()
                by_month.columns = ["Month", "Count", "Avg ($/MW)", "Max ($/MW)"]
                fig_mon = px.bar(by_month, x="Month", y=["Count", "Avg ($/MW)"], barmode="group", title="Clearing price by month (seasonality)")
                fig_mon.update_layout(height=350)
                st.plotly_chart(fig_mon, use_container_width=True)

        # ----- 3. Hedge type (OBL vs OPT) -----
        st.subheader("Hedge type (OBL vs OPT)")
        hedge_col = "hedge_type" if "hedge_type" in df.columns else ("HedgeType" if "HedgeType" in df.columns else None)
        if hedge_col:
            by_hedge = df.groupby(hedge_col)["_price_num"].agg(["count", "mean", "max"]).reset_index()
            by_hedge.columns = [hedge_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
            st.caption("OBL = obligation (two-way risk); OPT = option (upside only).")
            st.dataframe(by_hedge.rename(columns={hedge_col: "Hedge Type"}), use_container_width=True, hide_index=True)
            fig_hedge = px.bar(by_hedge, x=hedge_col, y="Avg ($/MW)", title="Average clearing price by hedge type", labels={hedge_col: "Hedge Type", "Avg ($/MW)": "Avg ($/MW)"})
            st.plotly_chart(fig_hedge, use_container_width=True)
        else:
            st.caption("HedgeType column not found in data.")

        # ----- 4. Volume vs price -----
        st.subheader("Volume vs price")
        mw_col = "mw_amount" if "mw_amount" in df.columns else ("MW" if "MW" in df.columns else None)
        if mw_col:
            df["_mw_num"] = pd.to_numeric(df[mw_col], errors="coerce")
            df_vol = df[df["_mw_num"].notna()].copy()
            if not df_vol.empty:
                p50 = df_vol["_price_num"].quantile(0.5)
                m50 = df_vol["_mw_num"].quantile(0.5)
                df_vol["_price_hi"] = df_vol["_price_num"] >= p50
                df_vol["_mw_hi"] = df_vol["_mw_num"] >= m50
                df_vol["_bucket"] = "Low MW / Low price"
                df_vol.loc[df_vol["_mw_hi"] & ~df_vol["_price_hi"], "_bucket"] = "High MW / Low price"
                df_vol.loc[~df_vol["_mw_hi"] & df_vol["_price_hi"], "_bucket"] = "Low MW / High price"
                df_vol.loc[df_vol["_mw_hi"] & df_vol["_price_hi"], "_bucket"] = "High MW / High price"
                bucket_counts = df_vol.groupby("_bucket", as_index=False).agg(count=("_price_num", "count"), avg_price=("_price_num", "mean"), total_mw=("_mw_num", "sum"))
                st.caption("High shadow + high MW = strong demand; low price + high MW = surplus.")
                st.dataframe(bucket_counts.rename(columns={"_bucket": "Bucket", "count": "Count", "avg_price": "Avg price ($/MW)", "total_mw": "Total MW"}), use_container_width=True, hide_index=True)
                fig_scatter = px.scatter(df_vol.head(500), x="_mw_num", y="_price_num", title="MW vs clearing price (sample)", labels={"_mw_num": "MW", "_price_num": "Price ($/MW)"})
                fig_scatter.update_layout(height=400)
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.caption("MW column not found.")

        # ----- 5. Pre-award as signal -----
        st.subheader("Pre-award as signal")
        crr_col = "crr_type" if "crr_type" in df.columns else ("CRRType" if "CRRType" in df.columns else None)
        if crr_col:
            pre = df[df[crr_col].astype(str).str.upper().str.contains("PREAWARD", na=False)]
            if not pre.empty:
                st.caption("PREAWARD results are an early signal for main auction demand and price levels.")
                st.metric("PREAWARD rows", len(pre))
                pre_agg = pre.groupby(path_col)["_price_num"].agg(["count", "mean", "max"]).reset_index()
                pre_agg.columns = [path_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
                pre_agg = pre_agg.sort_values("Max ($/MW)", ascending=False).head(15)
                st.dataframe(pre_agg.rename(columns={path_col: "Path"}), use_container_width=True, hide_index=True)
            else:
                st.caption("No PREAWARD rows in this dataset.")
        else:
            st.caption("CRRType column not found.")

        # ----- 6. Practical checklist for the next auction -----
        st.subheader("Practical checklist for the next auction")
        path_agg_sorted = path_agg.sort_values("Max ($/MW)", ascending=False)
        top_paths_list = path_agg_sorted.head(10)[path_col].tolist()
        low_paths_list = path_agg_sorted.tail(5)[path_col].tolist()
        checklist_items = [
            ("**Prioritize bids**", f"Rank paths by clearing price; focus on top paths: {', '.join(str(p) for p in top_paths_list[:5])}{'...' if len(top_paths_list) > 5 else ''}."),
            ("**Avoid overpaying**", "Use historical clearing prices as a reference; avoid bidding far above recent clears unless fundamentals justify it."),
            ("**Season / Time of Use**", "Filter by period and TOU; do not assume PeakWE patterns apply to PeakWD or OffPeak."),
            ("**Size and value**", "Combine MW, NumberOfHours, and MWh with clearing price to gauge total exposure and whether size is available at acceptable levels."),
            ("**Low-value paths**", f"Avoid bidding for speculation on very low clearing paths; consider selling or skipping: {', '.join(str(p) for p in low_paths_list)}."),
        ]
        for title, body in checklist_items:
            st.markdown(f"- {title}: {body}")

        st.caption("Top 15 rows per checklist point (data-driven analysis).")
        # 1. Prioritize bids — top 15 rows by clearing price
        st.markdown("**Prioritize bids** — top 15 rows by clearing price")
        cols_prio = [path_col, price_col]
        if period_col and period_col in df.columns:
            cols_prio.append(period_col)
        if tou_col and tou_col in df.columns:
            cols_prio.append(tou_col)
        if mw_col and mw_col in df.columns:
            cols_prio.append(mw_col)
        cols_prio = [c for c in cols_prio if c in df.columns]
        top15_prio = df.nlargest(15, "_price_num")[cols_prio].copy()
        top15_prio = top15_prio.rename(columns={path_col: "Path", price_col: "Clearing price ($/MW)"})
        st.dataframe(top15_prio, use_container_width=True, hide_index=True)

        # 2. Avoid overpaying — top 15 path-level reference (max clearing price by path)
        st.markdown("**Avoid overpaying** — top 15 paths by max clearing price (reference)")
        top15_ref = path_agg_sorted.head(15).rename(columns={path_col: "Path"})
        st.dataframe(top15_ref[["Path", "Count", "Avg ($/MW)", "Max ($/MW)"]], use_container_width=True, hide_index=True)

        # 3. Season / Time of Use — top 15 period-TOU combinations by avg clearing price
        if period_col and period_col in df.columns and tou_col and tou_col in df.columns:
            st.markdown("**Season / Time of Use** — top 15 period × TOU by avg clearing price")
            by_period_tou = (
                df.groupby([period_col, tou_col])["_price_num"]
                .agg(["count", "mean", "max"])
                .reset_index()
            )
            by_period_tou.columns = [period_col, tou_col, "Count", "Avg ($/MW)", "Max ($/MW)"]
            by_period_tou = by_period_tou.sort_values("Avg ($/MW)", ascending=False).head(15)
            st.dataframe(by_period_tou.rename(columns={period_col: "Period", tou_col: "Time of Use"}), use_container_width=True, hide_index=True)
        else:
            st.markdown("**Season / Time of Use** — period or TOU column missing; filter by period and TOU in the sidebar.")

        # 4. Size and value — top 15 rows by value (MW × price)
        mw_col_check = "mw_amount" if "mw_amount" in df.columns else ("MW" if "MW" in df.columns else None)
        if mw_col_check and "_mw_num" in df.columns:
            st.markdown("**Size and value** — top 15 rows by value (MW × clearing price)")
            df_val = df.copy()
            df_val["_value"] = df_val["_mw_num"] * df_val["_price_num"]
            cols_val = [path_col, "_value", "_mw_num", "_price_num"]
            if period_col and period_col in df_val.columns:
                cols_val.insert(1, period_col)
            if tou_col and tou_col in df_val.columns:
                cols_val.insert(2, tou_col)
            cols_val = [c for c in cols_val if c in df_val.columns]
            top15_val = df_val.nlargest(15, "_value")[cols_val].copy()
            top15_val = top15_val.rename(columns={path_col: "Path", "_value": "Value ($)", "_mw_num": "MW", "_price_num": "Clearing price ($/MW)"})
            if period_col in top15_val.columns:
                top15_val = top15_val.rename(columns={period_col: "Period"})
            if tou_col in top15_val.columns:
                top15_val = top15_val.rename(columns={tou_col: "Time of Use"})
            st.dataframe(top15_val, use_container_width=True, hide_index=True)
        else:
            st.markdown("**Size and value** — MW column missing; combine MW × price for exposure.")

        # 5. Low-value paths — bottom 15 rows by clearing price
        st.markdown("**Low-value paths** — bottom 15 rows by clearing price (avoid / sell)")
        top15_low = df.nsmallest(15, "_price_num")[cols_prio].copy()
        top15_low = top15_low.rename(columns={path_col: "Path", price_col: "Clearing price ($/MW)"})
        st.dataframe(top15_low, use_container_width=True, hide_index=True)

    def _run_optimized_ftr_portfolio(self) -> None:
        """Run the Optimized FTR Portfolio section: top contingencies and devices by shadow price."""
        from build_master_parquets import MasterParquetBuilder

        st.sidebar.subheader("Optimized FTR Portfolio")

        st.markdown(
            "<h2 style='text-align: center'>Optimized FTR Portfolio</h2>",
            unsafe_allow_html=True,
        )

        # Use applied 'Interested in' from form (Monthly vs Annual) for Binding Constraint parquet
        applied_interested_in = st.session_state.get("optimized_ftr_applied_interested_in", "Monthly")
        source_key = applied_interested_in.lower()

        builder = MasterParquetBuilder(
            annual_dir=ANNUAL_AUCTION_DIR,
            monthly_dir=MONTHLY_AUCTION_DIR,
        )
        report_type = "Binding Constraint"
        path = builder.get_master_path(report_type, source_key)
        if not path.exists():
            st.info(f"No {applied_interested_in} Binding Constraint master data. Run build_master_parquets.py to build.")
            return

        df = pd.read_parquet(path)
        if df.empty:
            st.info("No data in selected Binding Constraint table.")
            return

        device_col = "DeviceName" if "DeviceName" in df.columns else None
        contingency_col = "Contingency" if "Contingency" in df.columns else None
        shadow_col = "ShadowPrice" if "ShadowPrice" in df.columns else None
        tou_col = "TimeOfUse" if "TimeOfUse" in df.columns else None
        direction_col = "Direction" if "Direction" in df.columns else None
        device_type_col = None
        for cand in ["DeviceType", "DeviceTypeName", "ConstraintType", "Device_Category"]:
            if cand in df.columns:
                device_type_col = cand
                break
        if not (device_col and contingency_col and shadow_col):
            st.info("Binding Constraint data must have DeviceName, Contingency, and ShadowPrice columns.")
            return

        df["_shadow_num"] = pd.to_numeric(df[shadow_col], errors="coerce")
        df = df.dropna(subset=["_shadow_num"])
        if df.empty:
            st.info("No non-null ShadowPrice values in Binding Constraint data.")
            return

        # Slider value (applied) determines how many top contingencies appear in the Contingency dropdown
        max_cont_pre = min(50, df[contingency_col].nunique())
        applied_top_n = st.session_state.get("optimized_ftr_applied_top_n", min(10, max_cont_pre))
        applied_top_n = max(1, min(max_cont_pre, applied_top_n))

        # Contingency options = top applied_top_n contingencies by binding count (descending)
        by_cont_options = (
            df.groupby(contingency_col).size().sort_values(ascending=False).head(applied_top_n)
        )
        contingency_options = ["All"] + by_cont_options.index.astype(str).tolist()
        tou_options = ["All"] + sorted(df[tou_col].dropna().astype(str).unique().tolist()) if tou_col else ["All"]
        direction_options = ["All"] + sorted(df[direction_col].dropna().astype(str).unique().tolist()) if direction_col else ["All"]
        device_type_options = ["All"] + sorted(df[device_type_col].dropna().astype(str).unique().tolist()) if device_type_col else ["All"]

        applied_contingency = st.session_state.get("optimized_ftr_applied_contingency", "All")
        applied_device = st.session_state.get("optimized_ftr_applied_device", "All")
        applied_tou = st.session_state.get("optimized_ftr_applied_tou", "All")
        applied_direction = st.session_state.get("optimized_ftr_applied_direction", "All")
        applied_device_type = st.session_state.get("optimized_ftr_applied_device_type", "All")
        if applied_contingency not in contingency_options:
            applied_contingency = "All"
        # DeviceName options = devices that appear for the chosen Contingency (or all devices if Contingency is All)
        if applied_contingency == "All":
            device_options = ["All"] + sorted(df[device_col].dropna().astype(str).unique().tolist())
        else:
            df_for_devices = df[df[contingency_col].astype(str) == applied_contingency]
            device_options = ["All"] + sorted(df_for_devices[device_col].dropna().astype(str).unique().tolist())
        if applied_device not in device_options:
            applied_device = "All"
        if applied_tou not in tou_options:
            applied_tou = "All"
        if applied_direction not in direction_options:
            applied_direction = "All"
        if applied_device_type not in device_type_options:
            applied_device_type = "All"

        with st.sidebar.form(key="optimized_ftr_portfolio_form"):
            top_n = st.slider(
                "Top N contingencies (by binding count)",
                min_value=1,
                max_value=max_cont_pre,
                value=applied_top_n,
                key="optimized_ftr_top_n_contingencies",
                help="Submit this number first to determine the available options for the Contingency input below.",
            )
            st.caption("Submit the value above first to set the list of contingencies available in **Contingency**.")
            interested_in = st.selectbox(
                "Interested in",
                options=["Monthly", "Annual"],
                index=0 if applied_interested_in == "Monthly" else 1,
                key="optimized_ftr_interested_in",
            )
            filter_contingency = st.selectbox(
                "Contingency",
                options=contingency_options,
                index=contingency_options.index(applied_contingency),
                key="optimized_ftr_contingency",
            )
            st.caption("**DeviceName** options below are based on the chosen Contingency.")
            filter_device = st.selectbox(
                "DeviceName",
                options=device_options,
                index=device_options.index(applied_device),
                key="optimized_ftr_device",
            )
            filter_tou = st.selectbox(
                "TOU",
                options=tou_options,
                index=tou_options.index(applied_tou),
                key="optimized_ftr_tou",
            )
            filter_direction = st.selectbox(
                "Direction",
                options=direction_options,
                index=direction_options.index(applied_direction),
                key="optimized_ftr_direction",
            )
            filter_device_type = st.selectbox(
                "Device Type",
                options=device_type_options,
                index=device_type_options.index(applied_device_type),
                key="optimized_ftr_device_type",
            )
            applied_min_obs_sf = st.session_state.get("optimized_ftr_min_obs_sf", 5)
            min_obs_sf_input = st.number_input(
                "Min observations (ΔSF regression)",
                min_value=2,
                max_value=50,
                value=applied_min_obs_sf,
                key="optimized_ftr_min_obs_sf",
                help="Paths need at least this many (report_date, TOU) rows after merging with constraints. Lower values allow more paths but estimates are less reliable.",
            )
            submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["optimized_ftr_applied_interested_in"] = interested_in
            st.session_state["optimized_ftr_applied_contingency"] = filter_contingency
            st.session_state["optimized_ftr_applied_device"] = filter_device
            st.session_state["optimized_ftr_applied_tou"] = filter_tou
            st.session_state["optimized_ftr_applied_direction"] = filter_direction
            st.session_state["optimized_ftr_applied_device_type"] = filter_device_type
            st.session_state["optimized_ftr_applied_top_n"] = top_n
            st.rerun()

        # Bar plots: use full data and Top N slider only (no Contingency/DeviceName/TOU filter)
        max_cont = min(50, df[contingency_col].nunique())
        if max_cont == 0:
            st.info("No contingencies found in Binding Constraint data.")
            return
        applied_top_n = st.session_state.get("optimized_ftr_applied_top_n", min(10, max_cont))
        applied_top_n = max(1, min(max_cont, applied_top_n))
        by_cont = df.groupby(contingency_col).size().sort_values(ascending=False).head(applied_top_n)
        if by_cont.empty:
            st.info("No contingencies found in Binding Constraint data.")
            return

        st.subheader(f"Top {len(by_cont)} contingencies by binding count")
        st.caption(f"Data source: **{applied_interested_in}** combined Binding Constraint parquet. Plots use full data; filters below are for analysis only.")

        top_contingencies = by_cont.index.tolist()

        # Build one bar plot per contingency: DeviceName vs number of bindings (count)
        cols = st.columns(2)
        for idx, cont in enumerate(top_contingencies):
            sub = df[df[contingency_col].astype(str) == str(cont)]
            if sub.empty:
                continue
            device_counts = (
                sub.groupby(device_col, dropna=False)
                .size()
                .reset_index(name="Binding count")
            )
            device_counts = device_counts.rename(columns={device_col: "DeviceName"})
            if device_counts.empty:
                continue
            device_counts = device_counts.sort_values(
                "Binding count", ascending=False
            )

            col = cols[idx % 2]
            with col:
                fig = px.bar(
                    device_counts,
                    x="DeviceName",
                    y="Binding count",
                    title=str(cont),
                )
                fig.update_layout(
                    height=350,
                    xaxis_tickangle=-45,
                    margin=dict(b=120),
                )
                st.plotly_chart(fig, use_container_width=True)

        # Analysis: filtered by Contingency / DeviceName / TOU (for analysis after the bar plots)
        st.divider()
        st.subheader("Analysis (by selected filters)")
        df_analysis = df.copy()
        if applied_contingency != "All":
            df_analysis = df_analysis[df_analysis[contingency_col].astype(str) == applied_contingency]
        if applied_device != "All":
            df_analysis = df_analysis[df_analysis[device_col].astype(str) == applied_device]
        if applied_tou != "All" and tou_col:
            df_analysis = df_analysis[df_analysis[tou_col].astype(str) == applied_tou]
        if applied_direction != "All" and direction_col:
            df_analysis = df_analysis[df_analysis[direction_col].astype(str) == applied_direction]
        if applied_device_type != "All" and device_type_col:
            df_analysis = df_analysis[df_analysis[device_type_col].astype(str) == applied_device_type]
        no_filters = (
            applied_contingency == "All" and applied_device == "All"
            and (applied_tou == "All" or not tou_col)
            and (applied_direction == "All" or not direction_col)
            and (applied_device_type == "All" or not device_type_col)
        )
        if no_filters:
            st.caption("Select **Contingency**, **DeviceName**, **TOU**, **Direction**, and/or **Device Type** in the sidebar and submit to see filtered data below.")
        elif df_analysis.empty:
            st.info("No rows match the selected filters.")
        else:
            st.caption(f"**{len(df_analysis)}** rows match Contingency={applied_contingency}, DeviceName={applied_device}, TOU={applied_tou}, Direction={applied_direction}, Device Type={applied_device_type}.")

            # If a specific DeviceName is selected, show its device type (when available)
            if applied_device != "All":
                device_type_col = None
                for cand in ["DeviceType", "DeviceTypeName", "ConstraintType", "Device_Category"]:
                    if cand in df_analysis.columns:
                        device_type_col = cand
                        break
                if device_type_col:
                    type_vals = (
                        df_analysis[df_analysis[device_col].astype(str) == applied_device][device_type_col]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )
                    if type_vals:
                        st.caption(
                            f"Selected **DeviceName** '{applied_device}' is a: "
                            + ", ".join(f"**{v}**" for v in type_vals)
                            + f"."
                        )
                    else:
                        st.caption(
                            f"No non-null device type found for **DeviceName** `{applied_device}` "
                            f"in column `{device_type_col}`."
                        )
            display_cols = [contingency_col, device_col, shadow_col]
            if tou_col and tou_col in df_analysis.columns:
                display_cols.insert(2, tou_col)
            if direction_col and direction_col in df_analysis.columns:
                display_cols.append(direction_col)
            if device_type_col and device_type_col in df_analysis.columns:
                display_cols.append(device_type_col)
            if "report_date" in df_analysis.columns:
                display_cols.insert(0, "report_date")
            elif "CalendarPeriod" in df_analysis.columns:
                display_cols.insert(0, "CalendarPeriod")
            display_cols = [c for c in display_cols if c in df_analysis.columns]
            st.dataframe(
                df_analysis[display_cols].sort_values(contingency_col),
                use_container_width=True,
                hide_index=True,
            )

            # Historical shadow prices: grouped bar plot per report date (Plotly)
            # First, average over duplicate rows for each unique (Contingency, DeviceName, TOU, date) combo.
            x_col = "report_date" if "report_date" in df_analysis.columns else ("CalendarPeriod" if "CalendarPeriod" in df_analysis.columns else None)
            if x_col:
                base = df_analysis.copy()
                group_keys = [x_col, contingency_col, device_col]
                if tou_col and tou_col in base.columns:
                    group_keys.append(tou_col)
                base = (
                    base.groupby(group_keys, dropna=False)["_shadow_num"]
                    .mean()
                    .reset_index()
                )
                # Then aggregate by (date, TOU) for plotting
                if tou_col and tou_col in base.columns:
                    plot_df = (
                        base.groupby([x_col, tou_col], dropna=False)["_shadow_num"]
                        .mean()
                        .reset_index()
                    )
                else:
                    plot_df = (
                        base.groupby(x_col, dropna=False)["_shadow_num"]
                        .mean()
                        .reset_index()
                    )
                    if tou_col:
                        plot_df[tou_col] = "All"
                # Keep x as categorical for grouped bars (sort by date for order)
                if x_col == "report_date":
                    plot_df["_x_plot"] = pd.to_datetime(plot_df[x_col], errors="coerce")
                    plot_df = plot_df.dropna(subset=["_x_plot"])
                    plot_df["_x_label"] = plot_df["_x_plot"].dt.strftime("%Y-%m-%d")
                    plot_df = plot_df.sort_values("_x_plot")
                else:
                    plot_df["_x_plot"] = plot_df[x_col]
                    plot_df["_x_label"] = plot_df[x_col].astype(str)
                    plot_df = plot_df.sort_values("_x_label")
                if tou_col and tou_col in plot_df.columns:
                    fig_hist = px.bar(
                        plot_df,
                        x="_x_label",
                        y="_shadow_num",
                        color=tou_col,
                        title="Historical shadow prices by report date (all Time of Use)",
                        labels={"_shadow_num": "Shadow price ($/MW)", "_x_label": "Report date", tou_col: "Time of Use"},
                        barmode="group",
                    )
                else:
                    fig_hist = px.bar(
                        plot_df,
                        x="_x_label",
                        y="_shadow_num",
                        title="Historical shadow prices by report date",
                        labels={"_shadow_num": "Shadow price ($/MW)", "_x_label": "Report date"},
                    )
                fig_hist.update_layout(
                    height=450,
                    margin=dict(b=100, t=50, l=60, r=40),
                    xaxis=dict(
                        tickangle=-45,
                        title="Report date",
                        categoryorder="array",
                        categoryarray=plot_df["_x_label"].drop_duplicates().tolist(),
                    ),
                    yaxis=dict(title="Shadow price ($/MW)"),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.caption("No report date or period column available for historical chart.")

            # Path–constraint shift factor differences (ΔSF) from path + constraint shadow prices
            st.divider()
            st.subheader("Path–constraint shift factor differences (ΔSF)")
            st.caption(
                "Auction tables do not contain node-level PTDFs. We have path shadow prices (SourceAndSinkShadowPrices) "
                "and constraint shadow prices (Binding Constraint). Theory: path spread $= \\sum_k \\mu_k \\cdot \\Delta\\mathrm{SF}_{\\mathrm{path},k}$. "
                "We estimate $\\Delta\\mathrm{SF}$ by regressing path spread on constraint $\\mu_k$ across (report_date, TOU). "
                "**Dependent variable:** path spread ($y$), from the **Shadow Prices (path)** table (SourceAndSinkShadowPrices), column **ShadowPricePerMWH**. "
                "**Independent variables:** constraint shadow prices $\\mu_k$, from the **Binding Constraint** table, column **ShadowPrice**, one per constraint (DeviceName | Contingency). "
                "Results depend on sidebar inputs: **Interested in** (data source), **Contingency**, **DeviceName**, **TOU**, and **Direction** — only data matching these filters is used."
            )
            with st.expander("How this is calculated (step-by-step and example)"):
                st.markdown(
                    "**Regression variables**\n\n"
                    "- **Dependent variable ($y_t$):** Path spread (shadow price of the path in \$/MWh). "
                    "Source: **Shadow Prices (path)** table (SourceAndSinkShadowPrices), column **ShadowPricePerMWH**. "
                    "One observation per (path, report_date, TimeOfUse).\n\n"
                    "- **Independent variables ($\\mu_{1,t}, \\ldots, \\mu_{K,t}$):** Constraint shadow prices in \$/MW. "
                    "Source: **Binding Constraint** table, column **ShadowPrice**, with each constraint identified by **DeviceName** and **Contingency** (label: DeviceName | Contingency). "
                    "After pivoting, one column per constraint.\n\n"
                    "**Tables used**\n\n"
                    "1. **Binding Constraint** (combined parquet for the selected Monthly/Annual source). "
                    "Columns used: `report_date`, `TimeOfUse`, `DeviceName`, `Contingency`, `ShadowPrice`. "
                    "Each row is one constraint (device + contingency) in one (report_date, TOU) with its shadow price $\\mu_k$.\n\n"
                    "2. **Shadow Prices** (path) — **SourceAndSinkShadowPrices** (combined parquet). "
                    "Columns used: `SourceSink` (path id), `report_date`, `TimeOfUse`, `ShadowPricePerMWH`. "
                    "Each row is one path in one (report_date, TOU) with the path spread (congestion component of LMP_sink − LMP_source). "
                    "The **path** column in the output table is exactly **SourceSink** from this table (one row per unique path that had enough observations).\n\n"
                    "**Calculation steps**\n\n"
                    "1. **Filter constraints:** From Binding Constraint, keep only rows for the **chosen Contingency** (if not \"All\"). "
                    "Build a constraint label: $\\textit{DeviceName} \\mid \\textit{Contingency}$.\n\n"
                    "2. **Pivot constraints:** For each (report_date, TimeOfUse), take the (mean) shadow price for each constraint. "
                    "Result: one row per (report_date, TimeOfUse) with columns $\\mu_1, \\mu_2, \\ldots, \\mu_K$ for the top K constraints (K ≤ 20).\n\n"
                    "3. **Merge:** Join path Shadow Prices with this pivot on (report_date, TimeOfUse). "
                    "Each path observation now has: path spread $y$ and constraint shadow prices $\\mu_1, \\ldots, \\mu_K$.\n\n"
                    "4. **Regression per path:** For each path that has at least 5 observations, run OLS with **no intercept**. "
                    "The estimated coefficients are the **ΔSF** for that path for each constraint.\n\n"
                    "**Complete regression equation (for each path, e.g. first row):** For observation $t$ (each report_date × TimeOfUse), let $y_t$ = path spread for that path and $\\mu_{k,t}$ = shadow price of constraint $k$. The model is\n\n"
                    "$$ y_t = \\mu_{1,t}\\,\\Delta\\mathrm{SF}_1 + \\mu_{2,t}\\,\\Delta\\mathrm{SF}_2 + \\cdots + \\mu_{K,t}\\,\\Delta\\mathrm{SF}_K \\quad (\\text{no intercept}) $$ \n\n"
                    "5. **Output table:** Each row is one path. The **path** column is copied from the **SourceSink** column of the Shadow Prices (path) table — i.e. the path identifier as reported in SourceAndSinkShadowPrices (e.g. a path name or code). Each other column is one constraint; the value is the estimated ΔSF (SF_sink − SF_source) for that path and constraint.\n\n"
                )
            path_shadow = builder.get_master_path("Shadow Prices", source_key)
            if path_shadow.exists():
                import numpy as np

                df_path = pd.read_parquet(path_shadow)
                path_spread_col = "ShadowPricePerMWH" if "ShadowPricePerMWH" in df_path.columns else None
                path_id_col = "SourceSink" if "SourceSink" in df_path.columns else None
                if path_spread_col and path_id_col and "report_date" in df_path.columns and "TimeOfUse" in df_path.columns:
                    max_constraints_sf = 20
                    min_obs_sf = max(2, min(50, st.session_state.get("optimized_ftr_min_obs_sf", 5)))
                    df_bind_sf = df.copy()
                    if applied_contingency != "All":
                        df_bind_sf = df_bind_sf[df_bind_sf[contingency_col].astype(str) == applied_contingency]
                    if applied_device != "All" and device_col:
                        df_bind_sf = df_bind_sf[df_bind_sf[device_col].astype(str) == applied_device]
                    if applied_tou != "All" and tou_col and tou_col in df_bind_sf.columns:
                        df_bind_sf = df_bind_sf[df_bind_sf[tou_col].astype(str) == applied_tou]
                    if applied_direction != "All" and direction_col and direction_col in df_bind_sf.columns:
                        df_bind_sf = df_bind_sf[df_bind_sf[direction_col].astype(str) == applied_direction]
                    if df_bind_sf.empty:
                        st.caption("No binding constraint data for the chosen filters (Contingency / DeviceName / TOU / Direction); cannot estimate ΔSF.")
                    else:
                        df_bind_sf["_mu"] = pd.to_numeric(df_bind_sf[shadow_col], errors="coerce")
                        df_bind_sf = df_bind_sf.dropna(subset=["_mu"])
                        df_bind_sf["_constraint"] = (
                            df_bind_sf[device_col].astype(str) + " | " + df_bind_sf[contingency_col].astype(str)
                        )
                        constraint_counts_sf = df_bind_sf["_constraint"].value_counts()
                        top_constraints_sf = constraint_counts_sf.head(max_constraints_sf).index.tolist()
                        df_bind_sf = df_bind_sf[df_bind_sf["_constraint"].isin(top_constraints_sf)]
                        constraint_cols_sf_global = top_constraints_sf

                        calendar_period_col_sf = "CalendarPeriod" if "CalendarPeriod" in df_bind_sf.columns else None
                        if calendar_period_col_sf:
                            calendar_periods_sf = sorted(df_bind_sf[calendar_period_col_sf].dropna().astype(str).unique().tolist())
                        else:
                            calendar_periods_sf = ["All"]

                        df_path["_spread"] = pd.to_numeric(df_path[path_spread_col], errors="coerce")
                        df_path_clean = df_path.dropna(subset=["_spread"])
                        if applied_tou != "All" and "TimeOfUse" in df_path_clean.columns:
                            df_path_clean = df_path_clean[df_path_clean["TimeOfUse"].astype(str) == applied_tou]

                        results_sf = []
                        merged_sf_any = None
                        paths_ok_sf_any = []
                        constraint_cols_sf = None

                        for period in calendar_periods_sf:
                            if calendar_period_col_sf and period != "All":
                                df_bind_per = df_bind_sf[df_bind_sf[calendar_period_col_sf].astype(str) == period]
                            else:
                                df_bind_per = df_bind_sf
                            if df_bind_per.empty:
                                continue
                            pivot_sf = df_bind_per.groupby(["report_date", "TimeOfUse", "_constraint"], as_index=False)["_mu"].mean()
                            pivot_sf = pivot_sf.pivot_table(
                                index=["report_date", "TimeOfUse"],
                                columns="_constraint",
                                values="_mu",
                                aggfunc="first",
                            ).reset_index()
                            constraint_cols_per = [c for c in constraint_cols_sf_global if c in pivot_sf.columns]
                            if len(constraint_cols_per) < 1:
                                continue
                            if constraint_cols_sf is None:
                                constraint_cols_sf = constraint_cols_per

                            path_cols_merge = [path_id_col, "report_date", "TimeOfUse", "_spread"]
                            if calendar_period_col_sf and "CalendarPeriod" in df_path_clean.columns:
                                df_path_per = df_path_clean[df_path_clean["CalendarPeriod"].astype(str) == period]
                            else:
                                df_path_per = df_path_clean
                            if df_path_per.empty:
                                continue
                            merged_sf = df_path_per[[c for c in path_cols_merge if c in df_path_per.columns]].merge(
                                pivot_sf, on=["report_date", "TimeOfUse"], how="inner"
                            )
                            if merged_sf.empty:
                                continue
                            path_counts_sf = merged_sf.groupby(path_id_col).size()
                            paths_ok_sf = path_counts_sf[path_counts_sf >= min_obs_sf].index.tolist()
                            merged_sf = merged_sf[merged_sf[path_id_col].isin(paths_ok_sf)]
                            if merged_sf.empty:
                                continue
                            if merged_sf_any is None:
                                merged_sf_any = merged_sf
                                paths_ok_sf_any = paths_ok_sf

                            X_sf = merged_sf[constraint_cols_per].fillna(0).values
                            y_all_sf = merged_sf["_spread"].values
                            path_ids_sf = merged_sf[path_id_col].values
                            for pid in paths_ok_sf:
                                mask_sf = path_ids_sf == pid
                                y_sf = y_all_sf[mask_sf]
                                X_path_sf = X_sf[mask_sf]
                                if y_sf.size < min_obs_sf or np.linalg.matrix_rank(X_path_sf) < len(constraint_cols_per):
                                    continue
                                try:
                                    coefs_sf, *_ = np.linalg.lstsq(X_path_sf, y_sf, rcond=None)
                                except Exception:
                                    continue
                                row_sf = {"path": pid, "calendar_period": period}
                                for c in constraint_cols_sf_global:
                                    row_sf[c] = np.nan
                                for i, c in enumerate(constraint_cols_per):
                                    row_sf[c] = float(coefs_sf[i]) if i < len(coefs_sf) else np.nan
                                results_sf.append(row_sf)

                        # Fallback: if no results from per-period regressions, try one pooled regression (all periods combined)
                        if not results_sf and constraint_cols_sf_global and not df_bind_sf.empty and not df_path_clean.empty:
                            pivot_pooled = df_bind_sf.groupby(["report_date", "TimeOfUse", "_constraint"], as_index=False)["_mu"].mean()
                            pivot_pooled = pivot_pooled.pivot_table(
                                index=["report_date", "TimeOfUse"],
                                columns="_constraint",
                                values="_mu",
                                aggfunc="first",
                            ).reset_index()
                            constraint_cols_per = [c for c in constraint_cols_sf_global if c in pivot_pooled.columns]
                            if len(constraint_cols_per) >= 1:
                                if constraint_cols_sf is None:
                                    constraint_cols_sf = constraint_cols_per
                                path_cols_merge = [path_id_col, "report_date", "TimeOfUse", "_spread"]
                                merged_pooled = df_path_clean[[c for c in path_cols_merge if c in df_path_clean.columns]].merge(
                                    pivot_pooled, on=["report_date", "TimeOfUse"], how="inner"
                                )
                                if not merged_pooled.empty:
                                    path_counts_pooled = merged_pooled.groupby(path_id_col).size()
                                    paths_ok_pooled = path_counts_pooled[path_counts_pooled >= min_obs_sf].index.tolist()
                                    merged_pooled = merged_pooled[merged_pooled[path_id_col].isin(paths_ok_pooled)]
                                    if not merged_pooled.empty:
                                        merged_sf_any = merged_pooled
                                        paths_ok_sf_any = paths_ok_pooled
                                        X_sf = merged_pooled[constraint_cols_per].fillna(0).values
                                        y_all_sf = merged_pooled["_spread"].values
                                        path_ids_sf = merged_pooled[path_id_col].values
                                        for pid in paths_ok_pooled:
                                            mask_sf = path_ids_sf == pid
                                            y_sf = y_all_sf[mask_sf]
                                            X_path_sf = X_sf[mask_sf]
                                            if y_sf.size < min_obs_sf or np.linalg.matrix_rank(X_path_sf) < len(constraint_cols_per):
                                                continue
                                            try:
                                                coefs_sf, *_ = np.linalg.lstsq(X_path_sf, y_sf, rcond=None)
                                            except Exception:
                                                continue
                                            row_sf = {"path": pid, "calendar_period": "Pooled"}
                                            for c in constraint_cols_sf_global:
                                                row_sf[c] = np.nan
                                            for i, c in enumerate(constraint_cols_per):
                                                row_sf[c] = float(coefs_sf[i]) if i < len(coefs_sf) else np.nan
                                            results_sf.append(row_sf)

                        if constraint_cols_sf is None:
                            constraint_cols_sf = list(constraint_cols_sf_global)
                        if len(constraint_cols_sf) >= 1 and results_sf:
                            result_df_sf = pd.DataFrame(results_sf)
                            merged_sf = merged_sf_any
                            paths_ok_sf = paths_ok_sf_any
                            st.caption(
                                "**Sensitivities:** This result depends on sidebar inputs: **Interested in** (data source), "
                                "**Contingency**, **DeviceName**, **TOU**, and **Direction**. ΔSF is estimated **per calendar period** when data has CalendarPeriod."
                            )
                            if "calendar_period" in result_df_sf.columns and (result_df_sf["calendar_period"] == "Pooled").any():
                                st.caption("Results include **Pooled** (all periods combined) where no path had enough observations in any single calendar period.")
                            report_dates_used = merged_sf["report_date"].dropna().unique() if merged_sf is not None else []
                            report_dates_used = sorted(
                                pd.to_datetime(report_dates_used, errors="coerce").dropna()
                            )
                            if len(report_dates_used) > 0:
                                dates_fmt = [d.strftime("%Y-%m-%d") for d in report_dates_used]
                                if len(dates_fmt) <= 10:
                                    dates_str = ", ".join(dates_fmt)
                                else:
                                    dates_str = ", ".join(dates_fmt[:4]) + ", … , " + ", ".join(dates_fmt[-2:]) + f" ({len(dates_fmt)} total)"
                                st.caption("**Report dates used in regression:** " + dates_str)
                            st.caption("**Filtered Binding Constraint**")
                            bind_display_cols = [c for c in ["report_date", "TimeOfUse", contingency_col, device_col, shadow_col, direction_col] if c in df_bind_sf.columns]
                            if bind_display_cols:
                                st.dataframe(df_bind_sf[bind_display_cols], use_container_width=True, hide_index=True)
                            st.caption("**Shadow Prices (path)**")
                            path_display_cols = [path_id_col, "report_date", "TimeOfUse", "_spread"]
                            path_display_cols = [c for c in path_display_cols if c in df_path_clean.columns]
                            if path_display_cols:
                                path_display = df_path_clean[path_display_cols].copy()
                                path_display = path_display.rename(columns={"_spread": "ShadowPricePerMWH"})
                                st.dataframe(path_display, use_container_width=True, hide_index=True)
                            st.caption("**Estimated path–constraint shift factor differences (ΔSF)** — one row per (path, calendar period); each path has multiple shift factors per constraint by calendar period.")
                            st.dataframe(result_df_sf, use_container_width=True, hide_index=True)
                            st.markdown(
                                "**How to interpret the numbers**  \n"
                                "Each cell is the **estimated ΔSF** (shift factor difference = SF_sink − SF_source) for that **path** and that **constraint** (column = device/contingency). "
                                "**Both interpretations below are correct** — they describe the same coefficient in two equivalent ways.\n\n"
                                "**1. Physical (flow):** Injecting **1 MW at the path source** and withdrawing **1 MW at the path sink** results in **(this number) MW** of flow on that constraint's device. "
                                "E.g. **0.5** → 1 MW path flow adds 0.5 MW on that constraint; **−0.3** → 1 MW path flow reduces flow on that constraint by 0.3 MW.\n\n"
                                "**2. Price (shadow price):** Path spread = Σ μₖ × ΔSFₖ, so a **1 \$/MW** change in that constraint's shadow price μ is associated with a **(this number) \$/MWh** change in the path spread. "
                                "So the same **0.5** means: 1 \$/MW higher μ on that constraint → 0.5 \$/MWh higher path spread.\n\n"
                                "**Sign:** positive = path flow adds to constraint flow (and path spread moves with μ); negative = path flow relieves constraint flow (path spread moves opposite to μ)."
                            )
                            # Dynamic example using the first row of the result table
                            row0 = result_df_sf.iloc[0]
                            ex_path = row0.get("path", "—")
                            ex_period = row0.get("calendar_period", None)
                            first_constraint_col = next((c for c in constraint_cols_sf if c in row0.index), None)
                            if first_constraint_col is not None:
                                ex_val = row0[first_constraint_col]
                                if pd.notna(ex_val) and isinstance(ex_val, (int, float)):
                                    ex_val_rounded = round(float(ex_val), 4)
                                    period_txt = f" (calendar period **{ex_period}**)" if ex_period and str(ex_period) not in ("All", "Pooled") else ""
                                    st.markdown(
                                        f"**Example (first row):** For path **{ex_path}**{period_txt}, the estimated ΔSF for constraint **{first_constraint_col}** is **{ex_val_rounded}**. "
                                        f"Injecting 1 MW at the path source and withdrawing 1 MW at the path sink would result in **{ex_val_rounded} MW** flow on that constraint's device."
                                    )
                            if len(constraint_cols_sf) <= 15 and len(results_sf) <= 50:
                                try:
                                    if "calendar_period" in result_df_sf.columns:
                                        plot_df_sf = result_df_sf.set_index(["path", "calendar_period"])[constraint_cols_sf]
                                    else:
                                        plot_df_sf = result_df_sf.set_index("path")[constraint_cols_sf]
                                    y_labels = [f"{p} | {cp}" for (p, cp) in plot_df_sf.index] if isinstance(plot_df_sf.index, pd.MultiIndex) else plot_df_sf.index.tolist()
                                    fig_sf = go.Figure(
                                        data=go.Heatmap(
                                            z=plot_df_sf.values,
                                            x=constraint_cols_sf,
                                            y=y_labels,
                                            colorscale="RdBu",
                                            zmid=0,
                                        )
                                    )
                                    fig_sf.update_layout(
                                        title="ΔSF by path and constraint",
                                        xaxis_title="Constraint",
                                        yaxis_title="Path | Calendar period",
                                        height=400 + 12 * plot_df_sf.shape[0],
                                    )
                                    st.plotly_chart(fig_sf, use_container_width=True)
                                except Exception:
                                    pass
                            first_path_id = result_df_sf.iloc[0]["path"]
                            first_period = result_df_sf.iloc[0].get("calendar_period", "All")
                            if calendar_period_col_sf and first_period != "All":
                                df_bind_first = df_bind_sf[df_bind_sf[calendar_period_col_sf].astype(str) == first_period]
                                df_path_first = df_path_clean[df_path_clean["CalendarPeriod"].astype(str) == first_period] if "CalendarPeriod" in df_path_clean.columns else df_path_clean
                                pivot_first = df_bind_first.groupby(["report_date", "TimeOfUse", "_constraint"], as_index=False)["_mu"].mean().pivot_table(index=["report_date", "TimeOfUse"], columns="_constraint", values="_mu", aggfunc="first").reset_index()
                                cols_per = [c for c in constraint_cols_sf if c in pivot_first.columns]
                                if cols_per:
                                    m_first = df_path_first[[path_id_col, "report_date", "TimeOfUse", "_spread"]].merge(pivot_first, on=["report_date", "TimeOfUse"], how="inner")
                                    merged_first = m_first[m_first[path_id_col] == first_path_id].copy()
                                else:
                                    merged_first = pd.DataFrame()
                            else:
                                merged_first = merged_sf[merged_sf[path_id_col] == first_path_id].copy() if merged_sf is not None else pd.DataFrame()
                            if not merged_first.empty:
                                st.subheader("OLS inputs (first path)")
                                st.caption(
                                    f"Path = **{first_path_id}**" + (f", calendar period = **{first_period}**." if first_period != "All" else ".")
                                    + " Regression: $A \\mathbf{{x}} = \\mathbf{{b}}$ (no intercept); $\\mathbf{{x}}$ = estimated ΔSF. "
                                    + "**b** = dependent variable (path spread) from **Shadow Prices (path)** (ShadowPricePerMWH). "
                                    + "**A** = independent variables (constraint shadow prices) from **Binding Constraint** (ShadowPrice by constraint)."
                                )
                                idx_cols = ["report_date", "TimeOfUse"] if "report_date" in merged_first.columns and "TimeOfUse" in merged_first.columns else []
                                constraint_cols_first = [c for c in constraint_cols_sf if c in merged_first.columns]
                                A_display = merged_first[idx_cols + constraint_cols_first].copy() if idx_cols else merged_first[constraint_cols_first].copy()
                                st.caption("**Matrix A** (independent variables: constraint shadow prices $\\mu_{k,t}$ from Binding Constraint)")
                                st.dataframe(A_display, use_container_width=True, hide_index=True)
                                b_display = merged_first[["report_date", "TimeOfUse", "_spread"]].copy() if idx_cols else merged_first[["_spread"]].copy()
                                b_display = b_display.rename(columns={"_spread": "b (path spread)"})
                                st.caption("**Vector b** (dependent variable: path spread $y_t$ from Shadow Prices (path), ShadowPricePerMWH)")
                                st.dataframe(b_display, use_container_width=True, hide_index=True)
                        else:
                            if not results_sf and len(constraint_cols_sf or []) >= 1:
                                st.caption("No path had enough observations for a valid regression (in any calendar period).")
                                with st.expander("Why no results? (diagnostics)"):
                                    # Build pooled pivot and merge to report counts
                                    try:
                                        pivot_diag = df_bind_sf.groupby(["report_date", "TimeOfUse", "_constraint"], as_index=False)["_mu"].mean()
                                        pivot_diag = pivot_diag.pivot_table(
                                            index=["report_date", "TimeOfUse"],
                                            columns="_constraint",
                                            values="_mu",
                                            aggfunc="first",
                                        ).reset_index()
                                        n_pivot = len(pivot_diag)
                                        path_pairs = df_path_clean[["report_date", "TimeOfUse"]].drop_duplicates()
                                        n_path_pairs = len(path_pairs)
                                        path_cols_merge = [path_id_col, "report_date", "TimeOfUse", "_spread"]
                                        merged_diag = df_path_clean[[c for c in path_cols_merge if c in df_path_clean.columns]].merge(
                                            pivot_diag[["report_date", "TimeOfUse"]], on=["report_date", "TimeOfUse"], how="inner"
                                        )
                                        n_overlap = len(merged_diag)
                                        path_counts_diag = merged_diag.groupby(path_id_col).size()
                                        n_paths = len(path_counts_diag)
                                        if path_counts_diag.size > 0:
                                            min_obs = int(path_counts_diag.min())
                                            max_obs = int(path_counts_diag.max())
                                            med_obs = float(path_counts_diag.median())
                                            n_above = int((path_counts_diag >= min_obs_sf).sum())
                                            st.markdown(
                                                f"- **Constraint pivot:** {n_pivot} (report_date, TimeOfUse) rows  \n"
                                                f"- **Path data:** {n_path_pairs} unique (report_date, TimeOfUse) pairs  \n"
                                                f"- **After inner merge:** {n_overlap} rows across {n_paths} paths  \n"
                                                f"- **Per-path observations:** min = {min_obs}, max = {max_obs}, median = {med_obs:.0f}  \n"
                                                f"- **Paths with ≥ {min_obs_sf} observations:** {n_above} (need full column rank for OLS)"
                                            )
                                            if n_above == 0 and max_obs >= 2:
                                                st.caption(f"Try lowering **Min observations** in the sidebar to **{max(2, max_obs)}** to include paths that have at most {max_obs} observations (estimates may be less reliable).")
                                            elif n_above > 0:
                                                st.caption("Some paths have enough rows; failure may be due to **collinearity** (constraint shadow prices not full rank for that path). Try fewer constraints or different filters.")
                                        else:
                                            st.markdown(
                                                f"- **Constraint pivot:** {n_pivot} (report_date, TimeOfUse) rows  \n"
                                                f"- **Path data:** {n_path_pairs} unique (report_date, TimeOfUse) pairs  \n"
                                                f"- **After inner merge:** 0 rows — no (report_date, TimeOfUse) overlap between path and constraint data."
                                            )
                                            st.caption("Check that path and constraint data share the same report_date and TimeOfUse values (e.g. same date range and TOU encoding).")
                                    except Exception as e:
                                        st.caption(f"Could not compute diagnostics: {e}")
                            elif not constraint_cols_sf:
                                st.caption("No (report_date, TimeOfUse) overlap between path and constraint data, or no constraint with data for the chosen filters.")
                            else:
                                st.caption("Need at least one constraint with data to estimate ΔSF for the chosen filters.")
                else:
                    st.caption("Shadow Prices (path) table must have SourceSink, ShadowPricePerMWH, report_date, TimeOfUse.")
            else:
                st.caption("Shadow Prices (path) parquet not found for this source; run build_master_parquets.py to enable ΔSF estimation.")

            # Path lookup: Source & Sink for a given path name (from Auction Results / Bids)
            st.divider()
            st.subheader("Path lookup: Source & Sink")
            st.caption(
                "Path names in the app (e.g. in the ΔSF table) come from the **Shadow Prices (path)** table (SourceSink). "
                "Here we look up **Source** and **Sink** settlement points for a path name using tables that have (Source, Sink): **Auction Results** and **Auction Bids and Offers**."
            )
            path_lookup_options = []
            if path_shadow.exists():
                try:
                    df_path_lookup = pd.read_parquet(path_shadow)
                    if "SourceSink" in df_path_lookup.columns:
                        path_lookup_options = sorted(df_path_lookup["SourceSink"].dropna().astype(str).unique().tolist())
                except Exception:
                    pass
            path_lookup_name = st.selectbox(
                "Path name",
                options=[""] + path_lookup_options,
                index=0,
                key="optimized_ftr_path_lookup_name",
                help="Select a path (SourceSink from Shadow Prices) to see Source and Sink from Auction Results / Bids.",
            )
            if path_lookup_name:
                # Load tables that have Source, Sink (same source: Monthly/Annual)
                lookup_sources = []
                for report_label, report_type in [("Auction Results", "Auction Results"), ("Auction Bids and Offers", "Auction Bids and Offers")]:
                    p = builder.get_master_path(report_type, source_key)
                    if not p.exists():
                        continue
                    try:
                        df_lu = pd.read_parquet(p)
                        if "Source" in df_lu.columns and "Sink" in df_lu.columns:
                            df_lu = df_lu[["Source", "Sink"]].drop_duplicates()
                            df_lu["_table"] = report_label
                            lookup_sources.append(df_lu)
                    except Exception:
                        continue
                if lookup_sources:
                    df_lu_all = pd.concat(lookup_sources, ignore_index=True).drop_duplicates(subset=["Source", "Sink"])
                    path_name_str = str(path_lookup_name).strip()
                    # Exact match: path name equals "Source_Sink" or "Source → Sink"
                    exact = df_lu_all[
                        (df_lu_all["Source"].astype(str) + "_" + df_lu_all["Sink"].astype(str) == path_name_str)
                        | (df_lu_all["Source"].astype(str) + " → " + df_lu_all["Sink"].astype(str) == path_name_str)
                    ]
                    as_source = df_lu_all[df_lu_all["Source"].astype(str) == path_name_str][["Source", "Sink"]].drop_duplicates()
                    as_sink = df_lu_all[df_lu_all["Sink"].astype(str) == path_name_str][["Source", "Sink"]].drop_duplicates()
                    if not exact.empty:
                        st.markdown(f"**Exact match:** Path name **{path_name_str}** = **Source** → **Sink**: **{exact.iloc[0]['Source']}** → **{exact.iloc[0]['Sink']}**.")
                    if not as_source.empty:
                        st.markdown(f"**When used as Source:** {path_name_str} appears as **Source** in these paths (Source → Sink):")
                        st.dataframe(as_source, use_container_width=True, hide_index=True)
                    if not as_sink.empty:
                        st.markdown(f"**When used as Sink:** {path_name_str} appears as **Sink** in these paths (Source → Sink):")
                        st.dataframe(as_sink, use_container_width=True, hide_index=True)
                    if exact.empty and as_source.empty and as_sink.empty:
                        st.caption(f"No (Source, Sink) pair found in Auction Results or Auction Bids and Offers where the path name **{path_name_str}** appears as Source or Sink, or as exact \"Source_Sink\" / \"Source → Sink\".")
                else:
                    st.caption("Auction Results and Auction Bids and Offers parquets not found or do not have Source/Sink columns; cannot look up path.")
            else:
                st.caption("Select a path name above to see Source and Sink from the auction tables.")

    def _run_shaping(self) -> None:
        """Run the Shaping section (HPFC, arbitrage-free curves, ERN profile)."""
        st.markdown("<h2 style='text-align: center'>Shaping</h2>", unsafe_allow_html=True)
        from Shaping.shaping import run as run_shaping
        run_shaping()

    def _get_folders_by_source(self) -> dict[str, list[str]]:
        """Return map of source name ('Annual'/'Monthly') to sorted list of folder names."""
        out = {}
        if ANNUAL_AUCTION_DIR.is_dir():
            out["Annual"] = sorted(
                d.name for d in ANNUAL_AUCTION_DIR.iterdir()
                if d.is_dir() and d.name != "combined"
            )
        else:
            out["Annual"] = []
        if MONTHLY_AUCTION_DIR.is_dir():
            out["Monthly"] = sorted(
                d.name for d in MONTHLY_AUCTION_DIR.iterdir()
                if d.is_dir() and d.name != "combined"
            )
        else:
            out["Monthly"] = []
        return out

    def _load_report_for_folder(
        self, source: str, folder_name: str, report_type: str
    ) -> pd.DataFrame:
        """
        Load CSV(s) for the selected folder and report type.

        Args:
            source: 'Annual' or 'Monthly'.
            folder_name: Name of the subfolder (e.g. 20281st6_20260305).
            report_type: One of REPORT_TYPES (e.g. 'Auction Results').

        Returns:
            DataFrame of the matching file(s); concatenated if multiple (e.g. Base Loading).
        """
        base = ANNUAL_AUCTION_DIR if source == "Annual" else MONTHLY_AUCTION_DIR
        folder_path = base / folder_name
        if not folder_path.is_dir():
            return pd.DataFrame()
        pattern = REPORT_TYPE_FILE_PATTERNS.get(report_type, "")
        if not pattern:
            return pd.DataFrame()
        frames = []
        for csv_path in sorted(folder_path.glob("*.csv")):
            if pattern in csv_path.name:
                try:
                    frames.append(pd.read_csv(csv_path))
                except Exception:
                    continue
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    @staticmethod
    def _date_from_folder_name(folder_name: str) -> Optional[int]:
        """
        Extract date as integer YYYYMMDD from folder name (part after last '_').
        E.g. 20261st6_20250605 -> 20250605, APR2025_20250306 -> 20250306.
        """
        if "_" not in folder_name:
            return None
        suffix = folder_name.split("_")[-1]
        if len(suffix) == 8 and suffix.isdigit():
            return int(suffix)
        return None

    def _load_path_specific_adders_for_folder(
        self, source: str, folder_name: str
    ) -> list[tuple[str, pd.DataFrame]]:
        """
        Load Path Specific Adders for the selected auction folder. Adders are produced
        before auction results, so we match by auction id (first 8 chars) and pick the
        adders folder whose date is the latest that is still before the auction folder date.
        E.g. adders in 20261st6_20250515 are for auction 20261st6_20250605.
        """
        base = (
            PATH_SPECIFIC_ADDERS_ANNUAL_DIR
            if source == "Annual"
            else PATH_SPECIFIC_ADDERS_MONTHLY_DIR
        )
        if not base.is_dir():
            return []
        prefix = folder_name[:8] if len(folder_name) >= 8 else folder_name
        auction_date = self._date_from_folder_name(folder_name)
        candidates: list[tuple[Path, int]] = []
        for d in base.iterdir():
            if not d.is_dir() or d.name == "combined":
                continue
            if len(d.name) < len(prefix) or d.name[: len(prefix)] != prefix:
                continue
            adders_date = self._date_from_folder_name(d.name)
            if adders_date is None or auction_date is None:
                continue
            if adders_date < auction_date:
                candidates.append((d, adders_date))
        if not candidates:
            return []
        folder_path = max(candidates, key=lambda x: x[1])[0]
        out: list[tuple[str, pd.DataFrame]] = []
        for csv_path in sorted(folder_path.glob("*.csv")):
            if "pathspecificadders" not in csv_path.name.lower():
                continue
            try:
                df = pd.read_csv(csv_path)
                out.append((csv_path.name, df))
            except Exception:
                continue
        return out

    def _load_auction_results_from_annual(self) -> tuple[Optional[pd.DataFrame], list[str]]:
        """
        Load and concatenate all CSV auction results from extracted annual folders.

        Returns:
            (DataFrame or None, list of folder names that contributed data).
        """
        if not ANNUAL_AUCTION_DIR.is_dir():
            return None, []
        frames = []
        folder_names = []
        for subdir in sorted(ANNUAL_AUCTION_DIR.iterdir()):
            if not subdir.is_dir() or subdir.name == "combined":
                continue
            for csv_path in subdir.glob("*.csv"):
                try:
                    frames.append(self._auction_loader.load_from_path(csv_path))
                    if subdir.name not in folder_names:
                        folder_names.append(subdir.name)
                except Exception:
                    continue
        if not frames:
            return None, []
        return pd.concat(frames, ignore_index=True), folder_names

    def _run_auction_results(self) -> None:
        """Run the Auction Results section (data from auction_results/annual and /monthly)."""
        ANNUAL_AUCTION_DIR.mkdir(parents=True, exist_ok=True)
        MONTHLY_AUCTION_DIR.mkdir(parents=True, exist_ok=True)
        PATH_SPECIFIC_ADDERS_ANNUAL_DIR.mkdir(parents=True, exist_ok=True)
        PATH_SPECIFIC_ADDERS_MONTHLY_DIR.mkdir(parents=True, exist_ok=True)

        source_folders = self._get_folders_by_source()
        has_any_folders = any(source_folders.get(s) for s in AUCTION_SOURCE_OPTIONS)
        if not has_any_folders:
            st.info(
                "No auction results data found. Place data in auction_results/annual or auction_results/monthly."
            )
            return
        df, folder_names = self._load_auction_results_from_annual()
        if df is None or df.empty:
            df = pd.DataFrame()
        view = AuctionResultsView(
            df,
            folder_names=folder_names,
            source_folders=source_folders,
            load_report_fn=self._load_report_for_folder,
            load_path_specific_adders_fn=self._load_path_specific_adders_for_folder,
        )
        st.markdown("<h2 style='text-align: center'>Auction Results</h2>", unsafe_allow_html=True)
        view.render()
        st.sidebar.divider()


    def run(self) -> None:
        """Render sidebar, then the content for the selected section."""
        self._extract_pending_zips_if_any()
        self._ensure_auction_columns_on_startup()
        section = self._render_sidebar()
        if section == self.SECTIONS[0]:
            self._run_activity_calendar()
        elif section == self.SECTIONS[1]:
            self._run_auction_results()
        elif section == "Bid & Offer":
            self._run_bid_offer()
        elif section == "Base Loading":
            self._run_base_loading()
        elif section == "Binding Constraints":
            self._run_binding_constraints()
        elif section == "Shadow Prices":
            self._run_shadow_prices()
        elif section == "Cleared Results":
            self._run_cleared_results()
        elif section == "Optimized FTR Portfolio":
            self._run_optimized_ftr_portfolio()
        else:
            self._run_shaping()

    def _ensure_auction_columns_on_startup(self) -> None:
        """Once per session: ensure AuctionBidsAndOffers and MarketResults have NumberOfHours and MWh."""
        if st.session_state.get("_auction_columns_ensured"):
            return
        try:
            ensurer = AnnualAuctionColumnsEnsurer(
                annual_dir=ANNUAL_AUCTION_DIR,
                monthly_dir=MONTHLY_AUCTION_DIR,
                asset_dir=ASSET_DIR,
            )
            ensurer.run()
        except Exception:
            pass
        st.session_state["_auction_columns_ensured"] = True

    def _extract_pending_zips_if_any(self) -> None:
        """On app run: unzip any ZIPs in auction_results/annual, monthly, and path_specific_adders/annual and /monthly."""
        ANNUAL_AUCTION_DIR.mkdir(parents=True, exist_ok=True)
        MONTHLY_AUCTION_DIR.mkdir(parents=True, exist_ok=True)
        PATH_SPECIFIC_ADDERS_ANNUAL_DIR.mkdir(parents=True, exist_ok=True)
        PATH_SPECIFIC_ADDERS_MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
        if list(ANNUAL_AUCTION_DIR.glob("*.zip")):
            AnnualAuctionResultsExtractor(ANNUAL_AUCTION_DIR).run()
        if list(MONTHLY_AUCTION_DIR.glob("*.zip")):
            MonthlyAuctionResultsExtractor(MONTHLY_AUCTION_DIR).run()
        if list(PATH_SPECIFIC_ADDERS_ANNUAL_DIR.glob("*.zip")):
            AnnualAuctionResultsExtractor(PATH_SPECIFIC_ADDERS_ANNUAL_DIR).run()
        if list(PATH_SPECIFIC_ADDERS_MONTHLY_DIR.glob("*.zip")):
            MonthlyAuctionResultsExtractor(PATH_SPECIFIC_ADDERS_MONTHLY_DIR).run()


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------


def main() -> None:
    """Entry point: create app and run."""
    app = ERCOTCRRApp()
    app.run()


if __name__ == "__main__":
    main()
