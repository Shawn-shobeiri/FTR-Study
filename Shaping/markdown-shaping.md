# Shaping and hourly price forward curves (HPFC)

- **What HPFC is:** An **hourly price forward curve** (HPFC) is an estimate of future **hourly** (or quarter-hourly) prices over a delivery period. The same ideas apply to quarter-hourly curves; the abbreviation HPFC is commonly used.

- **Why HPFCs are needed:** Hourly electricity products are **not** traded directly on wholesale futures markets, so there are no observable hourly forward prices. An HPFC must be **derived** from available market prices (e.g. baseload futures) and from **structural information** (e.g. monthly, weekly, daily, and hourly price patterns).

- **Uses of HPFCs:**
  - Valuing **open positions** (hourly volumes × hourly prices).
  - Pricing **electricity supply contracts** and **consumer-specific load profiles**.
  - Evaluating **load profiles** and **power plants**.
  - Supporting **investment and divestment** decisions and **trading strategies**.
  - **Risk management** and **performance measurement**.
  - Input to **power plant optimisation** (e.g. dispatch, valuation of flexibility).

- **Two necessary properties of any HPFC:**
  1. **Arbitrage freedom:** The **average** of the HPFC hourly prices over any period must match the corresponding **market future price** for that period (e.g. the 8760 hourly prices for a year must average to the base future for that year; the average over all peak hours must equal the peak future for that year).
  2. **Shape:** The **profile** of hourly prices should reflect the **expected structure** (seasonality, weekday/weekend, peak/off-peak, typical hourly pattern).

- **What “shape” implies:** An HPFC should exhibit a **seasonal** profile, a **weekly** profile (e.g. higher weekdays, lower weekends), **smooth** price evolution over time, and should not be driven by **historical one-off extremes** unless they are expected to recur.

- **Forecast errors and time horizon:** Forecast errors generally **increase with time to delivery**. Short-term HPFCs (e.g. a few days) can use detailed inputs (e.g. wind feed-in forecasts); for weeks or months ahead, such granular information is usually not available. HPFCs can be purchased from vendors, but understanding the **underlying concept** is useful.

- **Factors that drive the methodology:**
  - **Application:** The way the HPFC is built can depend on how it will be used (e.g. for a power plant with many running hours, average levels and “in-the-money” periods may matter more than short spikes; for storage or flexible assets, **hourly volatility** and peak/off-peak spread matter more).
  - **Time horizon:** Methodology differs for a curve over the next few days versus months or years; longer horizons imply less granular information.

- **Information used to build an HPFC:**
  - **Load structure** (seasonal, monthly, weekly, daily, hourly).
  - **Generation mix** and **power plant park** (including renewables).
  - **Hourly feed-in** from weather-dependent sources (e.g. wind, solar).
  - **Current market prices** for the delivery period’s futures (base, peak, etc.).
  - **Historical** (quarter-)hourly price structure and other historical data.
  - **Expert knowledge** about future developments (e.g. technology phase-outs, electromobility, hydrogen, new PV capacity).

- **Formation process (high level):** An HPFC is formed by combining (1) **current market prices** for the relevant futures, (2) **historical hourly (or quarter-hourly) price structure** and other information, and (3) **expert knowledge** about relevant future developments, to produce a **current estimate** of the (quarter-)hourly price forward curve.

---

# Price quotes and forward curve granularity

- **Available price quotes:** Exchanges (e.g. EEX, Nord Pool) offer prices for **yearly** contracts and for **finer granularities**: quarters, months, weeks, and sometimes weekends. These quotes are for **base** (and often **peak**) products.

- **Why use granular quotes:** Including **monthly, quarterly, weekly**, and **weekend** prices improves the **quality** and **realism** of the forward curve and helps capture **seasonality**.

- **Liquidity by tenor:** **Quarterly** prices are typically liquid for the next few years; **monthly** prices are liquid for a shorter period (often only the next few months). For **long-term** horizons (several years), **yearly** futures are the main building blocks.

- **Building the curve:** The **short end** of the curve is shaped mainly by **monthly** (and weekly) quotes where available; as monthly quotes drop off, **quarterly** quotes take over; the **long end** is driven by **yearly** quotes. The **volume-weighted average** of the four quarterly prices equals the calendar-year price when quarters and years do not overlap.

- **Arbitrage and overlapping periods:** All available quotes (including **weekly** and **weekend**) should be used so that the curve is **arbitrage-free** and has a plausible shape. Ensuring arbitrage freedom is relatively straightforward for **monthly, quarterly, and yearly** prices (typically from exchanges). It becomes **more complex** for **weekly** and **weekend** prices because they **overlap** with each other and with calendar months; satisfying all constraints at once requires care.

- **Example of overlap:** A week that straddles two months (e.g. days in August and September) contributes to both the **month** and the **week** averages. Changing an hourly price in that week affects both the monthly and the weekly average, so achieving arbitrage freedom for the month and the week simultaneously can require iterative adjustment (e.g. shifting prices within the week). The same applies when incorporating **peak** and **weekend** definitions; further adjustments may be needed in practice.

---

# From monthly to weekly and hourly structure

- **First step:** Convert **monthly** average data (e.g. for base and peak) into **weekly** data so that the forward curve has a **weekly** structure. A simple approach is to assign the same average price to every week in the month, with **adjustments** for weeks that span two months so that the curve remains **arbitrage-free**.

- **Peak and off-peak:** For each period (e.g. a month), **peak** and **off-peak** prices can be derived from **base** (and **peak**) market quotes. An hour is assigned the **peak** value if it falls in the peak window; otherwise the **off-peak** price. The **volume-weighted average** of peak and off-peak prices over the period must equal the **base** price for that period.

- **Off-peak formula:** If $H_{\mathrm{peak}}$ is the number of peak hours, $H_{\mathrm{off}}$ the number of off-peak hours, $P_{\mathrm{peak}}$ and $P_{\mathrm{off}}$ their prices, and $P_{\mathrm{base}}$ the base price over $H_{\mathrm{base}} = H_{\mathrm{peak}} + H_{\mathrm{off}}$ hours, then

$$H_{\mathrm{peak}}\, P_{\mathrm{peak}} + H_{\mathrm{off}}\, P_{\mathrm{off}} = H_{\mathrm{base}}\, P_{\mathrm{base}}$$

  so $P_{\mathrm{off}}$ can be solved from the base and peak quotes and hour counts (e.g. for a month with 720 base hours and 168 peak hours, given base and peak prices in dollars per MWh).

- **Hourly shaping:** A simple approach is to use **historical hourly** price structure: future hourly prices are assumed to have a **similar shape** to history, even if the **level** (e.g. monthly or weekly average) differs. Historic hourly data are applied under the constraint that **averages** over each week and each month match the respective **forward prices** (arbitrage freedom).

- **Daily and hourly weighting matrices:**
  - **Daily:** From history, the **relative price level** for each **day of the week** (e.g. Monday, Tuesday, …, Sunday) can be expressed as a **percentage of the weekly average** (e.g. weekdays above 100%, weekends below).
  - **Hourly:** An **hourly** structure gives the price in each **hour** as a **percentage of the daily** (or base) price. These percentages can vary by **day of the week** (e.g. hour 6 on a Thursday might be 85% of that day’s base). Together, **daily** and **hourly** matrices from history are applied to **daily** (or weekly) forward prices to build the HPFC.

- **Assumptions and limitations:** The approach assumes that the **shape** of hourly prices in the future will be **similar** to the past. This can ignore **structural changes** (e.g. new PV capacity lowering midday prices, or changes in demand from electromobility or hydrogen). For the **short term**, more specific information (e.g. weather-driven wind/solar) may be available. Despite that, using recent historical behaviour as the **shape** often gives a **robust** and practical estimator for the HPFC; refinements (e.g. arbitrage checks, peak/weekend definitions) may be needed in implementation.

---

# Price structure and HPFC output

- **Seasonality and peak/off-peak:** An HPFC typically shows **seasonality** and **higher prices in peak hours** than in off-peak hours. A bar chart of hourly forward prices over a delivery period (e.g. September–December) illustrates this: levels around a base range with **spikes** at peak times.

- **Refining the hourly profile:** Beyond a simple peak/off-peak split, a more refined hourly structure uses **historical hourly** price development, **fundamental** views on the future (e.g. technology, demand shifts), and **expert** assessments. The result is a **current estimate** of the (quarter-)hourly price forward curve used for valuation, optimisation, and risk.
