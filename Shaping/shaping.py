"""
Shaping: hourly price forward curves (HPFC), arbitrage freedom, and price structure.
Theory (markdown) and application: off-peak formula, forward curve granularity, daily/hourly weighting, HPFC preview.
"""
import re
from pathlib import Path

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

_shaping_dir = Path(__file__).resolve().parent
_shaping_md = _shaping_dir / "markdown-shaping.md"

# Default day-of-week weights (% of weekly average): weekdays > 100%, weekends < 100%
_DEFAULT_DAY_WEIGHTS = {"Mon": 108, "Tue": 110, "Wed": 111, "Thu": 110, "Fri": 109, "Sat": 81, "Sun": 71}
# Default hourly weights (% of daily average): higher during day, lower at night (24 values)
_DEFAULT_HOURLY_WEIGHTS = [
    72, 68, 65, 64, 66, 72, 85, 98, 108, 112, 110, 108, 105, 104, 106, 108, 112, 118, 115, 105, 95, 88, 80, 75,
]
# Days per month (non–leap year)
_DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# ERCOT ERN typical peak hours: 7–22 (16 hours) — 6:00–22:00 in some definitions; use 7–22 as default
_ERN_PEAK_START = 7
_ERN_PEAK_END = 23  # inclusive 7..22


def _render_markdown_with_latex(markdown_path: Path) -> None:
    """Render markdown; split on $$...$$ and use st.latex() for formulas."""
    try:
        content = markdown_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.info("Shaping content not found.")
        return
    except Exception as e:
        st.error(f"Error reading markdown: {e}")
        return
    parts = re.split(r"\$\$([^$]+)\$\$", content)
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if i % 2 == 1:
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.latex(part)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(part, unsafe_allow_html=False)


def _run_offpeak_tab() -> None:
    """Off-peak price from base and peak: H_peak*P_peak + H_off*P_off = H_base*P_base."""
    st.markdown("#### Off-peak from base and peak")
    st.caption(
        "Volume-weighted average of peak and off-peak prices must equal the base price. "
        "Solve for $P_{\\mathrm{off}}$: $H_{\\mathrm{peak}} P_{\\mathrm{peak}} + H_{\\mathrm{off}} P_{\\mathrm{off}} = H_{\\mathrm{base}} P_{\\mathrm{base}}$."
    )
    col1, col2 = st.columns(2)
    with col1:
        P_base = st.number_input("Base price $P_{\\mathrm{base}}$ ($/MWh)", value=93.27, min_value=0.0, step=1.0, format="%.2f", key="hpfc_pbase")
        P_peak = st.number_input("Peak price $P_{\\mathrm{peak}}$ ($/MWh)", value=101.0, min_value=0.0, step=1.0, format="%.2f", key="hpfc_ppeak")
    with col2:
        H_base = st.number_input("Total base hours $H_{\\mathrm{base}}$", value=720, min_value=1, step=24, key="hpfc_hbase")
        H_peak = st.number_input("Peak hours $H_{\\mathrm{peak}}$", value=168, min_value=0, max_value=int(H_base), step=24, key="hpfc_hpeak")
    H_off = H_base - H_peak
    if H_off <= 0:
        st.warning("Off-peak hours must be positive (peak hours < base hours).")
        return
    P_off = (H_base * P_base - H_peak * P_peak) / H_off
    st.markdown("**Result**")
    st.latex(r"P_{\mathrm{off}} = \frac{H_{\mathrm{base}}\, P_{\mathrm{base}} - H_{\mathrm{peak}}\, P_{\mathrm{peak}}}{H_{\mathrm{off}}}")
    st.metric("Off-peak price $P_{\\mathrm{off}}$ ($/MWh)", f"{P_off:.2f}")
    st.caption(
        f"Check: {H_peak}×{P_peak:.2f} + {H_off}×{P_off:.2f} = {H_peak * P_peak + H_off * P_off:.2f}; "
        f"$H_{{\\mathrm{{base}}}} P_{{\\mathrm{{base}}}}$ = {H_base * P_base:.2f}."
    )


def _run_forward_curve_tab() -> None:
    """Forward curve: cal year and quarters; volume-weighted average of quarters = cal year."""
    st.markdown("#### Forward curve (calendar year and quarters)")
    st.caption(
        "Quarterly prices (Q1–Q4) and calendar-year price. The volume-weighted average of the four quarterly prices equals the calendar-year price when quarters do not overlap."
    )
    cal_price = st.number_input("Calendar year price ($/MWh)", value=133.29, min_value=0.0, step=1.0, format="%.2f", key="hpfc_cal")
    q1 = st.number_input("Q1 price ($/MWh)", value=137.65, min_value=0.0, step=1.0, format="%.2f", key="hpfc_q1")
    q2 = st.number_input("Q2 price ($/MWh)", value=121.07, min_value=0.0, step=1.0, format="%.2f", key="hpfc_q2")
    q3 = st.number_input("Q3 price ($/MWh)", value=129.06, min_value=0.0, step=1.0, format="%.2f", key="hpfc_q3")
    q4 = st.number_input("Q4 price ($/MWh)", value=145.28, min_value=0.0, step=1.0, format="%.2f", key="hpfc_q4")
    # Equal weight for simplicity (or use actual hours per quarter)
    hours_q = np.array([90, 91, 92, 92]) * 24  # approximate hours per quarter
    vol_weighted = np.average([q1, q2, q3, q4], weights=hours_q)
    st.markdown("**Volume-weighted average of Q1–Q4** (using approximate hours per quarter)")
    st.metric("(Q1×h1 + Q2×h2 + Q3×h3 + Q4×h4) / (h1+h2+h3+h4)", f"{vol_weighted:.2f} $/MWh")
    st.metric("Calendar year price", f"{cal_price:.2f} $/MWh")
    diff = abs(vol_weighted - cal_price)
    if diff < 0.01:
        st.success("Arbitrage-free: weighted quarterly average matches calendar year.")
    else:
        st.info(f"Difference: {diff:.2f} $/MWh. In practice, weights are set so the curve is arbitrage-free.")
    df = pd.DataFrame({"Period": ["Cal-y", "Q1", "Q2", "Q3", "Q4"], "Price ($/MWh)": [cal_price, q1, q2, q3, q4]})
    st.dataframe(df.set_index("Period"), use_container_width=True)


def _run_daily_hourly_tab() -> None:
    """Daily and hourly weighting matrices; build HPFC for one week and check arbitrage."""
    st.markdown("#### Daily and hourly shaping")
    st.caption(
        "Apply day-of-week weights (% of weekly average) and hourly weights (% of daily average) to a weekly base price to get hourly prices. "
        "The average of the 168 hourly prices should equal the weekly price (arbitrage freedom)."
    )
    weekly_price = st.number_input("Weekly average price ($/MWh)", value=85.0, min_value=0.0, step=1.0, format="%.2f", key="hpfc_weekly")
    day_names = list(_DEFAULT_DAY_WEIGHTS.keys())
    day_weights = []
    cols = st.columns(7)
    for i, (name, default) in enumerate(_DEFAULT_DAY_WEIGHTS.items()):
        with cols[i]:
            w = st.number_input(name, value=default, min_value=50, max_value=150, step=1, key=f"hpfc_dw_{name}")
            day_weights.append(w)
    day_weights = np.array(day_weights) / 100.0  # as fraction of weekly avg
    # Normalize so that mean of daily prices = weekly_price: daily_i = weekly * weight_i, and mean(daily) = weekly * mean(weights).
    # So we want mean(daily) = weekly => mean(weights) should be 1. Normalize:
    day_weights = day_weights / np.mean(day_weights)
    hourly_weights = []
    st.markdown("**Hourly weights** (% of daily average; 24 hours)")
    use_default_hourly = st.checkbox("Use default hourly profile", value=True, key="hpfc_use_def_h")
    if use_default_hourly:
        hourly_weights = np.array(_DEFAULT_HOURLY_WEIGHTS, dtype=float) / 100.0
        hourly_weights = hourly_weights / np.mean(hourly_weights)
    else:
        for h in range(24):
            v = st.number_input(f"Hour {h}", value=_DEFAULT_HOURLY_WEIGHTS[h], min_value=30, max_value=150, step=1, key=f"hpfc_hw_{h}")
            hourly_weights.append(v)
        hourly_weights = np.array(hourly_weights) / 100.0
        hourly_weights = hourly_weights / np.mean(hourly_weights)
    # Build 7 days × 24 hours: for day d, daily_price_d = weekly_price * day_weights[d]; hour h price = daily_price_d * hourly_weights[h]
    hourly_prices = np.zeros(7 * 24)
    for d in range(7):
        daily_price = weekly_price * day_weights[d]
        for h in range(24):
            hourly_prices[d * 24 + h] = daily_price * hourly_weights[h]
    avg_hourly = np.mean(hourly_prices)
    st.markdown("**Arbitrage check**")
    st.metric("Average of 168 hourly prices ($/MWh)", f"{avg_hourly:.2f}")
    st.metric("Target weekly price ($/MWh)", f"{weekly_price:.2f}")
    if abs(avg_hourly - weekly_price) < 0.01:
        st.success("Arbitrage-free: average of hourly prices equals weekly price.")
    else:
        st.caption("Small differences can occur due to normalization. In practice, weights are chosen so the curve is arbitrage-free.")
    # Table: 7 rows (days), 24 cols (hours) or show as long table
    df_week = pd.DataFrame(
        hourly_prices.reshape(7, 24),
        index=day_names,
        columns=[f"H{h}" for h in range(24)],
    )
    st.markdown("**Hourly prices ($/MWh) for the week**")
    st.dataframe(df_week.style.format("{:.2f}"), use_container_width=True, height=280)


def _run_hpfc_chart_tab() -> None:
    """HPFC bar chart: hourly forward prices over a period with peak/off-peak shape."""
    st.markdown("#### HPFC preview (hourly price structure)")
    st.caption(
        "Build a simple HPFC for a chosen number of days using base and peak prices, with daily and hourly shape. "
        "Peak hours (e.g. 8–20) get peak price; off-peak get off-peak price; then apply hourly weights for within-day shape."
    )
    P_base = st.number_input("Base price ($/MWh)", value=93.27, min_value=0.0, step=1.0, format="%.2f", key="hpfc_chart_base")
    P_peak = st.number_input("Peak price ($/MWh)", value=101.0, min_value=0.0, step=1.0, format="%.2f", key="hpfc_chart_peak")
    H_peak_per_day = st.slider("Peak hours per day (e.g. 8–20 = 12)", value=12, min_value=0, max_value=24, key="hpfc_chart_hpeak")
    num_days = st.slider("Number of days to show", value=14, min_value=1, max_value=31, key="hpfc_chart_days")
    H_off_per_day = 24 - H_peak_per_day
    H_off_total = num_days * H_off_per_day
    H_peak_total = num_days * H_peak_per_day
    H_base_total = num_days * 24
    if H_off_total <= 0:
        P_off = P_base
    else:
        P_off = (H_base_total * P_base - H_peak_total * P_peak) / H_off_total
    hourly_weights = np.array(_DEFAULT_HOURLY_WEIGHTS, dtype=float) / 100.0
    peak_start = (24 - H_peak_per_day) // 2
    peak_end = min(24, peak_start + H_peak_per_day)
    # One day template: each hour gets peak or off-peak level scaled by hourly weight
    prices_one_day = np.zeros(24)
    for h in range(24):
        if peak_start <= h < peak_end and H_peak_per_day > 0:
            prices_one_day[h] = P_peak * hourly_weights[h]
        else:
            prices_one_day[h] = P_off * hourly_weights[h]
    # Normalize single day so that (H_peak * P_peak + H_off * P_off) / 24 = implied daily avg; then scale so period avg = P_base
    day_avg_target = (H_peak_per_day * P_peak + H_off_per_day * P_off) / 24.0
    if np.sum(prices_one_day) > 1e-10:
        prices_one_day = prices_one_day / np.mean(prices_one_day) * day_avg_target
    prices_flat = np.tile(prices_one_day, num_days)
    prices_flat = prices_flat * (H_base_total * P_base) / np.sum(prices_flat)
    fig = go.Figure(data=[go.Bar(x=list(range(len(prices_flat))), y=prices_flat, marker_color="steelblue")])
    fig.update_layout(
        title="Hourly forward prices (HPFC)",
        xaxis_title="Hour index",
        yaxis_title="Price ($/MWh)",
        template="plotly_white",
        height=400,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key="hpfc_bar")
    avg_plot = float(np.mean(prices_flat))
    st.caption(f"Average of {len(prices_flat)} hourly prices: {avg_plot:.2f} $/MWh (target base: {P_base:.2f}). Seasonality and peak/off-peak are reflected in the shape.")


def _build_ern_simulated_year(
    base_level: float = 50.0,
    monthly_factors: list[float] | None = None,
) -> np.ndarray:
    """Simulate 8760 hourly prices for a year (hub ERN, ERCOT). Shape from day-of-week and hourly weights; monthly seasonality."""
    if monthly_factors is None:
        # ERCOT: higher in summer (Jun–Sep), lower in shoulder/spring/fall
        monthly_factors = [0.92, 0.88, 0.90, 0.95, 1.00, 1.15, 1.25, 1.22, 1.10, 0.98, 0.92, 0.95]
    day_weights = np.array(list(_DEFAULT_DAY_WEIGHTS.values()), dtype=float) / 100.0
    hourly_weights = np.array(_DEFAULT_HOURLY_WEIGHTS, dtype=float) / 100.0
    # Normalize so that a flat day would give 1.0
    day_weights = day_weights / np.mean(day_weights)
    hourly_weights = hourly_weights / np.mean(hourly_weights)
    prices = []
    hour_of_year = 0
    for month in range(12):
        days = _DAYS_PER_MONTH[month]
        mf = monthly_factors[month]
        for day_in_month in range(days):
            day_of_week = (hour_of_year // 24) % 7
            dw = day_weights[day_of_week]
            for h in range(24):
                hw = hourly_weights[h]
                p = base_level * mf * dw * hw
                prices.append(p)
                hour_of_year += 1
    return np.array(prices)


def _run_ern_monthly_tab() -> None:
    """ERCOT ERN: simulated year of hourly prices; then hourly profile for a month from peak/off-peak futures (arbitrage-free, shape from history)."""
    st.markdown("#### ERCOT ERN — Monthly hourly profile from peak/off-peak futures")
    st.caption(
        "A **simulated year** (8760 hours) of hourly prices for hub **ERN** (ERCOT) is used as **historical shape**. "
        "You choose a **month**, the **peak** and **off-peak** futures prices for that month. "
        "The app builds an **arbitrage-free** hourly profile for the month: the average over peak hours equals the peak futures price, "
        "and the average over off-peak hours equals the off-peak futures price. The **relative shape** (hourly and daily pattern) follows the simulated historical structure."
    )
    with st.expander("Simulation methodology"):
        st.markdown("""
**How the three weight sets are obtained**

- **Monthly factors:** In this app they are **fixed default values** (one per month Jan–Dec) chosen to reflect typical ERCOT seasonality—e.g. higher in summer (Jun–Sep), lower in spring/fall. In practice you would derive them from **historical data**: e.g. average realized or forward price in each month divided by the annual average, so each factor is that month’s relative level.  
- **Day-of-week weights:** In this app they are **fixed default values** (Mon–Sun), e.g. weekdays ~108–111% and weekends ~71–81% of the weekly average. In practice you would derive them from **historical data**: for each weekday, take the average price over all hours on that day (across many weeks) and divide by the average price over the full week; that gives the relative level for each day.  
- **Hourly weights:** In this app they are **fixed default values** (24 values, one per hour 0–23) giving within-day shape—e.g. higher during daytime, lower at night. In practice you would derive them from **historical data**: for each hour of the day, take the average price in that hour (across many days) and divide by the daily average; that gives the relative level for each hour.

All three sets are **normalized** so that (in the product used below) they preserve the intended structure without rescaling the base level. Here, day and hourly weights are normalized so their mean is 1.

**1. Simulated year (8760 hours)**  
- Each hourly price is: **base level × monthly factor × day-of-week weight × hourly weight**.  
- **Monthly factors** reflect seasonality (e.g. higher in summer for ERCOT); they are fixed relative weights by month (Jan–Dec).  
- **Day-of-week weights** (Mon–Sun) are normalized so their mean is 1; weekdays are above 1, weekends below.  
- **Hourly weights** (0–23) are normalized so their mean is 1; they give within-day shape (e.g. higher during daytime, lower at night).  
- No stochastic component: the same inputs produce the same 8760 values. The result is a deterministic “historical” shape for the year.

**2. Monthly slice and peak/off-peak**  
- For the chosen **month**, we take the corresponding slice of the simulated year (e.g. January = first 31×24 hours).  
- **Peak hours** are those with hour-of-day in [peak start, peak end) (e.g. 7–22). All other hours are **off-peak**.  
- Every day in the month uses the same peak/off-peak definition.

**3. Arbitrage-free hourly profile for the month**  
- Let *hist* be the simulated hourly prices for the month (historical shape).  
- Compute the average of *hist* over **peak hours**, *avg_peak_hist*, and over **off-peak hours**, *avg_off_hist*.  
- **Scaling (preserve shape):**  
  - For each **peak** hour: *shaped* = *P_peak* × (*hist* / *avg_peak_hist*).  
  - For each **off-peak** hour: *shaped* = *P_off* × (*hist* / *avg_off_hist*).  
- By construction, the average of *shaped* over peak hours equals *P_peak* and over off-peak hours equals *P_off*, so the profile is **arbitrage-free** with respect to the peak and off-peak futures. The **relative** pattern (hourly and daily) is unchanged from the simulated shape.

**4. Shaping factors**  
- For each hour of the day *h* (0–23), the **shaping factor** = (average of *shaped* at that hour across all days in the month) / (overall average of *shaped*).  
- A factor of 1 means that hour is at the period average; >1 above average, <1 below average. The bar plot shows these 24 values.
        """)
    # Simulated year (8760)
    base_level = st.number_input("Simulated year base level ($/MWh)", value=50.0, min_value=1.0, step=5.0, format="%.1f", key="ern_base")
    year_prices = _build_ern_simulated_year(base_level=base_level)
    st.markdown("**Simulated year** — 8760 hourly prices (ERN-style structure: day-of-week and hourly weights, monthly seasonality).")
    with st.expander("Show simulated year summary"):
        st.metric("Year average ($/MWh)", f"{np.mean(year_prices):.2f}")
        st.metric("Min / Max ($/MWh)", f"{np.min(year_prices):.2f} / {np.max(year_prices):.2f}")
        fig_year = go.Figure(data=[go.Scatter(x=list(range(8760)), y=year_prices, mode="lines", line=dict(width=1, color="steelblue"))])
        fig_year.update_layout(title="Simulated ERN hourly prices (full year)", xaxis_title="Hour of year", yaxis_title="Price ($/MWh)", template="plotly_white", height=250)
        st.plotly_chart(fig_year, use_container_width=True, key="ern_year_plot")

    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_ix = st.selectbox("Month", options=list(range(12)), format_func=lambda i: month_names[i], key="ern_month")
    P_peak = st.number_input("Peak futures price for month ($/MWh)", value=95.0, min_value=0.0, step=1.0, format="%.2f", key="ern_ppeak")
    P_off = st.number_input("Off-peak futures price for month ($/MWh)", value=78.0, min_value=0.0, step=1.0, format="%.2f", key="ern_poff")
    peak_start = st.number_input("Peak start hour (0–23)", value=_ERN_PEAK_START, min_value=0, max_value=23, step=1, key="ern_peak_start")
    peak_end = st.number_input("Peak end hour (exclusive, 1–24)", value=_ERN_PEAK_END, min_value=1, max_value=24, step=1, key="ern_peak_end")
    if peak_end <= peak_start:
        st.warning("Peak end hour must be greater than peak start hour.")
        return

    # Extract month from simulated year (same month index)
    start_hour = sum(_DAYS_PER_MONTH[m] * 24 for m in range(month_ix))
    days_in_month = _DAYS_PER_MONTH[month_ix]
    n_hours = days_in_month * 24
    hist = year_prices[start_hour : start_hour + n_hours].copy()

    # Which hours are peak (0..23)
    def is_peak(h: int) -> bool:
        return peak_start <= h < peak_end

    peak_mask = np.array([is_peak(h) for _ in range(days_in_month) for h in range(24)], dtype=bool)
    off_mask = ~peak_mask
    n_peak = int(np.sum(peak_mask))
    n_off = int(np.sum(off_mask))
    if n_peak == 0 or n_off == 0:
        st.warning("Need both peak and off-peak hours in the day.")
        return

    avg_peak_hist = float(np.mean(hist[peak_mask]))
    avg_off_hist = float(np.mean(hist[off_mask]))
    if avg_peak_hist < 1e-10 or avg_off_hist < 1e-10:
        st.warning("Historical shape has zero average in peak or off-peak; cannot scale.")
        return

    # Scale: preserve shape, set averages to P_peak and P_off
    shaped = np.zeros_like(hist)
    shaped[peak_mask] = P_peak * (hist[peak_mask] / avg_peak_hist)
    shaped[off_mask] = P_off * (hist[off_mask] / avg_off_hist)

    st.markdown("**Arbitrage check**")
    avg_peak_out = float(np.mean(shaped[peak_mask]))
    avg_off_out = float(np.mean(shaped[off_mask]))
    base_implied = float(np.mean(shaped))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg peak hours ($/MWh)", f"{avg_peak_out:.2f}")
    with col2:
        st.metric("Avg off-peak hours ($/MWh)", f"{avg_off_out:.2f}")
    with col3:
        st.metric("Implied base (avg all hours) ($/MWh)", f"{base_implied:.2f}")
    if abs(avg_peak_out - P_peak) < 0.02 and abs(avg_off_out - P_off) < 0.02:
        st.success("Arbitrage-free: average over peak hours = peak futures; average over off-peak = off-peak futures.")
    st.caption(f"Peak hours: {n_peak} (hours {peak_start}–{peak_end - 1}); off-peak: {n_off}. Shape from simulated historical ERN prices.")

    st.markdown("**Shaping factors (shapers) by hour of day**")
    # For each hour 0..23: shaping factor = avg price at that hour / overall avg (1 = at average)
    hour_of_day = np.arange(n_hours) % 24
    shapers = np.array([np.mean(shaped[hour_of_day == h]) / base_implied for h in range(24)])
    fig_shapers = go.Figure(
        data=[go.Bar(x=list(range(24)), y=shapers, marker_color="steelblue", text=[f"{s:.3f}" for s in shapers], textposition="outside")]
    )
    fig_shapers.update_layout(
        title="Hourly shaping factors (price at hour / period average)",
        xaxis_title="Hour of day",
        yaxis_title="Shaping factor",
        template="plotly_white",
        height=360,
        showlegend=False,
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        yaxis=dict(rangemode="tozero"),
    )
    st.plotly_chart(fig_shapers, use_container_width=True, key="ern_shapers_bar")
    st.caption("Factor = 1 at period average; >1 above average, <1 below average. Averaged across all days in the month.")

    st.markdown("**Hourly price profile for the month**")
    fig = go.Figure(data=[go.Bar(x=list(range(len(shaped))), y=shaped, marker_color="steelblue")])
    fig.update_layout(
        title=f"{month_names[month_ix]} — ERN hourly profile ($/MWh)",
        xaxis_title="Hour of month",
        yaxis_title="Price ($/MWh)",
        template="plotly_white",
        height=400,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key="ern_month_bar")

    df_month = pd.DataFrame(
        shaped.reshape(days_in_month, 24),
        index=[f"Day {d+1}" for d in range(days_in_month)],
        columns=[f"H{h}" for h in range(24)],
    )
    st.dataframe(df_month.style.format("{:.2f}"), use_container_width=True, height=min(400, 50 + days_in_month * 22))

    with st.expander("How the hourly price profile is calculated (example)"):
        st.markdown("**Formulas used to build the monthly profile**")
        st.latex(
            r"\text{For a peak hour } i:\quad \text{shaped}_i = P_{\mathrm{peak}} \times "
            r"\frac{\text{hist}_i}{\overline{\text{hist}}_{\mathrm{peak}}}"
        )
        st.latex(
            r"\text{For an off-peak hour } j:\quad \text{shaped}_j = P_{\mathrm{off}} \times "
            r"\frac{\text{hist}_j}{\overline{\text{hist}}_{\mathrm{off}}}"
        )
        st.markdown(
            "- $\\text{hist}_i$ / $\\text{hist}_j$: simulated \"historical\" hourly prices for the chosen month.\n"
            "- $\\overline{\\text{hist}}_{\\mathrm{peak}}$: average of $\\text{hist}$ over all peak hours in the month.\n"
            "- $\\overline{\\text{hist}}_{\\mathrm{off}}$: average of $\\text{hist}$ over all off-peak hours in the month.\n"
            "- $P_{\\mathrm{peak}}$, $P_{\\mathrm{off}}$: peak and off-peak futures prices you entered."
        )

        # Simple numeric example using the first peak and first off-peak hour in the month
        ex_peak_idx = int(np.flatnonzero(peak_mask)[0]) if n_peak > 0 else None
        ex_off_idx = int(np.flatnonzero(off_mask)[0]) if n_off > 0 else None
        if ex_peak_idx is not None and ex_off_idx is not None:
            hist_peak_ex = float(hist[ex_peak_idx])
            shaped_peak_ex = float(shaped[ex_peak_idx])
            hist_off_ex = float(hist[ex_off_idx])
            shaped_off_ex = float(shaped[ex_off_idx])

            # Map flat indices back to (day, hour-of-day) within the month
            peak_day = ex_peak_idx // 24
            peak_hour = ex_peak_idx % 24
            off_day = ex_off_idx // 24
            off_hour = ex_off_idx % 24

            st.markdown("**Example peak hour (within the selected month)**")
            st.markdown(
                f"- Day {peak_day + 1}, hour {peak_hour}  \n"
                f"- Historical price at this **peak hour in the selected month** = {hist_peak_ex:.2f} $/MWh  \n"
                f"- Average historical price over **all peak hours of the selected month** = {avg_peak_hist:.2f} $/MWh  \n"
                f"- Peak futures price $P_{{\\mathrm{{peak}}}}$ = {P_peak:.2f} $/MWh"
            )
            st.markdown(
                "Computed shaped peak price (numbers substituted into the formula above):  \n"
                f"- {P_peak:.2f} × {hist_peak_ex:.2f} / {avg_peak_hist:.2f} ≈ **{shaped_peak_ex:.2f} $/MWh**"
            )

            st.markdown("**Example off-peak hour (within the selected month)**")
            st.markdown(
                f"- Day {off_day + 1}, hour {off_hour}  \n"
                f"- Historical price at this **off-peak hour in the selected month** = {hist_off_ex:.2f} $/MWh  \n"
                f"- Average historical price over **all off-peak hours of the selected month** = {avg_off_hist:.2f} $/MWh  \n"
                f"- Off-peak futures price $P_{{\\mathrm{{off}}}}$ = {P_off:.2f} $/MWh"
            )
            st.markdown(
                "Computed shaped off-peak price (numbers substituted into the formula above):  \n"
                f"- {P_off:.2f} × {hist_off_ex:.2f} / {avg_off_hist:.2f} ≈ **{shaped_off_ex:.2f} $/MWh**"
            )

    st.markdown("---")
    st.markdown("**Arbitrage freedom check**")
    st.caption("Verify that the profile is arbitrage-free: the average over **peak hours** must equal the **peak futures price**, and the average over **off-peak hours** must equal the **off-peak futures price**. Enter the futures prices to check against.")
    tol = 0.02
    target_peak_check = st.number_input("Peak futures price to check ($/MWh)", value=P_peak, min_value=0.0, step=1.0, format="%.2f", key="ern_arb_target_peak")
    target_off_check = st.number_input("Off-peak futures price to check ($/MWh)", value=P_off, min_value=0.0, step=1.0, format="%.2f", key="ern_arb_target_off")
    peak_ok = abs(avg_peak_out - target_peak_check) <= tol
    off_ok = abs(avg_off_out - target_off_check) <= tol
    sum_peak = float(np.sum(shaped[peak_mask]))
    sum_off = float(np.sum(shaped[off_mask]))
    with st.expander("Show calculation"):
        st.markdown("**Peak hours**")
        st.latex(r"\text{Profile avg (peak)} = \frac{\sum \text{(prices at peak hours)}}{n_{\mathrm{peak}}}")
        st.markdown(f"- Sum of profile prices at peak hours = **{sum_peak:.2f}** (sum over {n_peak} hours, in $/MWh)")
        st.markdown(f"- $n_{{peak}}$ = {n_peak} hours")
        st.markdown(f"- Profile average (peak) = {sum_peak:.2f} / {n_peak} = **{avg_peak_out:.2f}** $/MWh")
        st.markdown(f"- Peak futures price = **{target_peak_check:.2f}** $/MWh → difference = {avg_peak_out - target_peak_check:+.2f} $/MWh")
        st.markdown("---")
        st.markdown("**Off-peak hours**")
        st.latex(r"\text{Profile avg (off-peak)} = \frac{\sum \text{(prices at off-peak hours)}}{n_{\mathrm{off}}}")
        st.markdown(f"- Sum of profile prices at off-peak hours = **{sum_off:.2f}** (sum over {n_off} hours, in $/MWh)")
        st.markdown(f"- $n_{{off}}$ = {n_off} hours")
        st.markdown(f"- Profile average (off-peak) = {sum_off:.2f} / {n_off} = **{avg_off_out:.2f}** $/MWh")
        st.markdown(f"- Off-peak futures price = **{target_off_check:.2f}** $/MWh → difference = {avg_off_out - target_off_check:+.2f} $/MWh")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Peak hours**")
        st.metric("Profile average ($/MWh)", f"{avg_peak_out:.2f}")
        st.metric("Peak futures price ($/MWh)", f"{target_peak_check:.2f}")
        st.metric("Difference ($/MWh)", f"{avg_peak_out - target_peak_check:+.2f}")
        if peak_ok:
            st.success("Arbitrage-free: profile avg matches peak futures.")
        else:
            st.warning(f"Violation: differs from peak futures by {abs(avg_peak_out - target_peak_check):.2f} $/MWh.")
    with c2:
        st.markdown("**Off-peak hours**")
        st.metric("Profile average ($/MWh)", f"{avg_off_out:.2f}")
        st.metric("Off-peak futures price ($/MWh)", f"{target_off_check:.2f}")
        st.metric("Difference ($/MWh)", f"{avg_off_out - target_off_check:+.2f}")
        if off_ok:
            st.success("Arbitrage-free: profile avg matches off-peak futures.")
        else:
            st.warning(f"Violation: differs from off-peak futures by {abs(avg_off_out - target_off_check):.2f} $/MWh.")


# ---------- Page layout: theory column + application tabs ----------
def run() -> None:
    """Entry point for the Shaping section (HPFC, arbitrage freedom, ERN profile)."""
    st.markdown(
        """
        <style>
        .stColumn, div[data-testid="column"] { max-height: none !important; }
        .stColumn:nth-of-type(2), div[data-testid="column"]:nth-of-type(2) {
            position: sticky !important; top: 0 !important; align-self: flex-start !important;
            max-height: 100vh !important; overflow-y: auto !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    theory_col, app_col = st.columns([1, 1], gap="large")

    with theory_col:
        st.markdown("<h3 align='center'>Theory</h3>", unsafe_allow_html=True)
        if _shaping_md.exists():
            _render_markdown_with_latex(_shaping_md)
        else:
            st.info("Shaping content not found.")

    with app_col:
        st.markdown("<h3 align='center'>Application</h3>", unsafe_allow_html=True)
        tab_offpeak, tab_daily, tab_chart, tab_ern = st.tabs([
            "Off-peak formula",
            "Daily & hourly shaping",
            "HPFC chart",
            "ERCOT ERN monthly profile",
        ])
        with tab_offpeak:
            _run_offpeak_tab()
        with tab_daily:
            _run_daily_hourly_tab()
        with tab_chart:
            _run_hpfc_chart_tab()
        with tab_ern:
            _run_ern_monthly_tab()


if __name__ == "__main__":
    run()
