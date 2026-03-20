# Shaping and the Hourly Price Forward Curve (HPFC)

A practical guide from a power-market quant: what shaping is, how to build an HPFC, methods with pros and cons, and real examples using ICE indices in ERCOT and CAISO.

---

## 1. What is shaping?

**Shaping** is the process of turning **block** (or period-average) forward prices into **hourly** (or sub-hourly) price profiles. Markets trade **blocks** — e.g. monthly base, monthly peak, quarterly, calendar year — not individual hours. To value hourly exposure (load, generation, storage, contracts), we need a **forward price for every hour**. Shaping is the step that **distributes** the block prices over time while preserving their **average** and imposing a **plausible intra-period profile**.

**Hourly Price Forward Curve (HPFC):** An HPFC is a **forward curve of hourly prices** over a delivery horizon (e.g. next 12 months, 24 months). It is not directly observable; it is **derived** from:

- Traded **block** prices (base, peak, off-peak, monthly, quarterly, calendar).
- **Structural** information: seasonality, weekday/weekend, peak/off-peak hours, typical hourly shape.
- Optionally: **fundamentals** (load, renewables, outages) or **weather** for short horizons.

**Why it matters:** Valuation (hourly volume × hourly price), supply contracts, plant dispatch, storage optionality, risk (VaR, P&amp;L attribution), and trading all need an **hourly** view consistent with **market** block prices.

---

## 2. Two necessary properties of an HPFC

Any serious HPFC must satisfy:

1. **Arbitrage freedom (consistency with blocks):** The **average** of the HPFC over any traded period must equal the **market price** for that block. Examples:
   - Average of all 8,760 hours in a calendar year = **calendar base** price for that year.
   - Average of all **peak** hours in a month = **monthly peak** price for that month.
   - Average of all **off-peak** hours in a month = **monthly off-peak** (or implied from base and peak).
   So shaping is **constrained**: we choose the **profile**, but the **level** over each block is fixed by the market.

2. **Reasonable shape:** The **profile** (hour-of-day, day-of-week, season) should reflect **expected** structure: higher prices in peak hours, weekday vs weekend, summer/winter seasonality, and (if used) historical or fundamental hourly patterns. The curve should not introduce implausible jumps or one-off spikes unless justified.

---

## 3. Block products and definitions (context for shaping)

Before shaping, we need **block prices** and **definitions** of peak/off-peak and delivery periods. These differ by market.

**Typical blocks:**

- **Base (around-the-clock, ATC):** All hours in the period (e.g. 24/7 for a month).
- **Peak:** Only peak hours (e.g. HE 7–22 or HE 8–23 in local time, depending on ISO).
- **Off-peak:** All hours that are not peak; can be quoted or implied from base and peak.

**Relationship:** If $H_{\mathrm{peak}}$ and $H_{\mathrm{off}}$ are the number of peak and off-peak hours in the period, and $P_{\mathrm{base}}$, $P_{\mathrm{peak}}$, $P_{\mathrm{off}}$ are the average prices:

$$
H_{\mathrm{peak}} P_{\mathrm{peak}} + H_{\mathrm{off}} P_{\mathrm{off}} = H_{\mathrm{base}} P_{\mathrm{base}}.
$$

So given **base** and **peak** market quotes, we can solve for the implied **off-peak** price: $P_{\mathrm{off}} = (H_{\mathrm{base}} P_{\mathrm{base}} - H_{\mathrm{peak}} P_{\mathrm{peak}}) / H_{\mathrm{off}}$.

---

## 4. Methods of shaping to get an HPFC

Below are the main **methods**, with pros and cons. In practice, shops often combine them (e.g. use historical shape for the profile, then scale to match block prices).

---

### 4.1 Peak/off-peak split then flat or simple hourly shape

**Idea:** For each period (e.g. month), assign a **single price** to every peak hour (the monthly peak price) and a **single price** to every off-peak hour (implied off-peak from base and peak). Optionally apply a **fixed hourly multiplier** (e.g. hour 18 = 110% of peak, hour 3 = 90% of off-peak) so the average over peak hours still equals the peak block and over off-peak equals off-peak block.

**Pros:** Simple; exactly matches block averages by construction; no historical data required.  
**Cons:** No weekday/weekend or day-of-week structure; no within-day variation beyond a fixed template; can look too flat and unrealistic for valuation of flexible assets.

**Best for:** Quick HPFC, back office checks, or when only base and peak are available and no shape data exists.

---

### 4.2 Historical hourly shape (daily and hourly weight matrices)

**Idea:** Use **historical** (e.g. trailing 12–24 months) hourly prices to build **weights**:

- **Day-of-week weights:** For each weekday (Mon–Sun), compute the ratio of that day’s average price to the **weekly** average (e.g. Monday = 105%, Saturday = 92%). So each day gets a multiplier relative to the week.
- **Hourly weights:** For each hour of the day (0–23), compute the ratio of that hour’s average price to the **daily** (or peak/off-peak) average. These can be **separate** for peak days vs weekend, or a single profile.

Then: (1) Start from **block** prices (e.g. monthly base and peak). (2) Derive **weekly** or **daily** prices from the monthly so that averages match. (3) For each day, apply the day-of-week weight to get that day’s level. (4) For each hour, apply the hourly weight so that the **average** over the relevant block (e.g. all hours in the month, all peak hours in the month) still equals the market block price. This usually requires a **normalization** step so that the shaped hourly series averages exactly to the block (arbitrage freedom).

**Pros:** Uses observable structure; captures weekday/weekend and typical hourly pattern; relatively robust.  
**Cons:** Assumes the future **shape** is like the past; can miss **structural change** (e.g. more solar flattening midday, new load from EVs); sensitive to the choice of history (length, period); overlapping blocks (e.g. week + month) require iterative or constrained optimization to satisfy all averages.

**Best for:** Standard HPFC for valuation and risk when no proprietary fundamental model is used; widely used in industry.

---

### 4.3 Fundamental / supply–demand–based shaping

**Idea:** Use a **fundamental model** (load forecast, unit commitment, renewable availability, transmission) to simulate **hourly** prices (or LMPs) over the delivery period. The **level** of the simulated path is then **scaled** or **adjusted** so that the average over each traded block (month base, month peak, etc.) matches the **market** block price. So the **shape** comes from the fundamental run; the **level** is anchored to the forward curve.

**Pros:** Can capture **structural changes** (new plants, renewables, demand shifts); hourly profile is consistent with physics and constraints; useful for medium/long-term and for “what-if” views.  
**Cons:** Data- and model-intensive; requires UC/ED or similar; scaling to match all blocks (month base, month peak, quarter, year) without arbitrage can be complex; slower to run and maintain.

**Best for:** Strategic valuation, long-dated HPFC, and when the shop has a fundamental team and wants shape driven by supply/demand rather than history alone.

---

### 4.4 Short-term weather-driven shaping (days ahead)

**Idea:** For the **next few days to a few weeks**, use **forecasts** of load and **weather-dependent generation** (wind, solar) to build an hourly profile. Temperature drives load; wind speed and irradiance drive renewable output. The hourly profile is then **scaled** so that the average over any overlapping block (e.g. balance-of-month) matches the **forward** block price.

**Pros:** Captures **near-term** variation (heat waves, wind lulls, cloud cover); better for trading and dispatch in the prompt window.  
**Cons:** Only applicable to **short** horizons (forecast quality decays); need reliable load and renewable forecasts; block consistency still required where blocks overlap.

**Best for:** Next-day to two-week HPFC; trading and operational scheduling.

---

### 4.5 Optimization-based / constrained spline or regression

**Idea:** Parameterize the hourly curve (e.g. by splines, or by a set of basis functions over hour-of-day and day-of-year), and **optimize** the parameters subject to **constraints** that the average over each traded block equals the market price. Smoothness or prior (e.g. close to historical shape) can be added to the objective.

**Pros:** Arbitrage freedom is **hard-constrained**; can blend historical shape with smoothness; flexible (can add peak/off-peak, weekday, etc. as constraints).  
**Cons:** Implementation is more involved; need to define blocks and constraints carefully (overlapping weeks/months); can be underdetermined (many feasible shapes) so the objective drives the choice.

**Best for:** Production HPFC systems where many blocks (month, quarter, year, peak, off-peak, weekend) must be satisfied exactly and a unique, smooth shape is desired.

---

### 4.6 Summary table: shaping methods

| Method | Pros | Cons | Typical use |
|--------|------|------|-------------|
| Peak/off-peak flat | Simple; exact block match | No intraday/week structure | Quick HPFC, checks |
| Historical daily + hourly weights | Uses real structure; robust | Past ≠ future; structural change | Standard valuation/risk HPFC |
| Fundamental (UC/ED + scale) | Structure from supply/demand | Heavy; scaling to blocks complex | Long-term, strategic |
| Weather-driven (short-term) | Good for prompt | Only short horizon; needs forecasts | Next days/weeks |
| Optimization / constrained | Exact block match; smooth | More complex; need all block defs | Production, multi-block |

---

## 5. Real-world examples: ICE indices in ERCOT and CAISO

Block **definitions** and **traded products** differ by hub and ISO. Below we use **ICE**-traded products as the source of **block prices**; shaping then turns these into an HPFC.

---

### 5.1 ERCOT (ICE)

**Hubs / locations:** ERCOT North 345kV is a key financial hub; ICE lists products that settle against ERCOT real-time **settlement point prices (SPPs)** for that hub.

**Nx16 notation:** The “**Nx16**” convention means **N days per week** × **16 hours per day** (peak window). The 16 hours are typically **HE 7–22** (7:00–22:00) in **CPT** (Central Prevailing Time), i.e. 16 on-peak hours per day. Which **days** are included depends on the product.

**Block products (ICE) — ERCOT North 345kV:**

- **Around-the-clock (ATC):** All hours (e.g. 0100–2400 CPT). Examples:
  - **ICE NGX ERCOT North 345kV Financial ATC** — ticker **EXA**: Monthly, cash-settled; reference = average of real-time SPPs over all hours for the contract month.
  - **ERCOT North 345kV Physical Daily ATC** — ticker **YDY**: Daily ATC; all hours 0100–2400 CPT.
- **5x16 (weekday peak):** **5 days** (Monday–Friday) × **16 hours** (e.g. 7–22 CPT). “On-peak” weekdays only; excludes weekends and usually NERC holidays. Liquid monthly and calendar products; often the **primary** peak block for financial and physical deals. Ticker **ERN** (ERCOT North 345kV Real-Time Peak) for **monthly** 5x16; **NDB** for Day-Ahead Peak Daily where listed.
- **2x16 (weekend peak):** **2 days** (Saturday–Sunday) × **16 hours** (same 7–22 CPT). Weekend-only peak; ticker for Real-Time 2x16 (e.g. **ERCOT North 345kV Hub Real-Time Peak 2x16**) — check ICE product list for current symbol.
- **7x16 (all-days peak):** **7 days** × **16 hours** (every day, 7–22 CPT). No weekend discount; one price for all peak hours in the period. Used when the deal does not distinguish weekday vs weekend. Monthly 7x16 peak products listed on ICE; symbol may be product-specific (e.g. 7x Peak).
- **Off-peak:** Can be **7x8** (all days, remaining 8 hours) or **5x8** (weekday nights) etc., or implied from ATC and the relevant peak block via $H_{\mathrm{peak}} P_{\mathrm{peak}} + H_{\mathrm{off}} P_{\mathrm{off}} = H_{\mathrm{base}} P_{\mathrm{base}}$. **NZD** = ERCOT North Load Zone Day-Ahead Off-Peak (where listed).
- **Other:** **ERG** = Real-Time **TB4 (7x)** (spread between 4 highest and 4 lowest hours); ancillary products (e.g. Responsive Reserve **ECR**); daily peak/ATC.

**ERCOT North 345kV — ticker reference (ICE):**

| Block / product       | Ticker(s) | Notes                                      |
|-----------------------|-----------|--------------------------------------------|
| ATC, monthly financial| **EXA**   | NGX Financial ATC, monthly                 |
| ATC, daily physical   | **YDY**   | Physical Daily ATC                         |
| 5x16 Real-Time Peak   | **ERN**   | Monthly RT peak (Mon–Fri 7–22 CPT)         |
| 5x16 Day-Ahead Peak   | **NDB**   | DA Peak Daily (where listed)               |
| 2x16 Real-Time Peak   | (ICE)     | Check ICE for “Real-Time Peak 2x16”       |
| 7x16 / 7x peak        | (ICE)     | Product-specific; see ICE product list      |
| Off-peak (Load Zone)  | **NZD**   | North Load Zone DA Off-Peak                |
| TB4 (7x)              | **ERG**   | 4 high − 4 low hours, 7x                    |
| Responsive Reserve    | **ECR**   | Ancillary                                  |

**Shaping with 5x16, 2x16, 7x16:**  
If the curve has **5x16**, **2x16**, and **7x16** (and optionally ATC) quotes:

- **7x16** fixes the average over **all** peak hours (Mon–Sun, 7–22 CPT).
- **5x16** fixes the average over **weekday** peak hours; **2x16** over **weekend** peak hours. So you have two sub-blocks that together must be consistent with 7x16 (volume-weighted: $5/7 \cdot P_{5\times16} + 2/7 \cdot P_{2\times16} = P_{7\times16}$ for the same 16-hour window).
- Build the HPFC so that: (1) average over all hours = ATC, (2) average over 7x16 hours = 7x16 price, (3) average over 5x16 hours = 5x16 price, (4) average over 2x16 hours = 2x16 price. Use historical hourly shape (weekday vs weekend, hour-of-day) and normalize so all these block constraints hold.

---

### 5.2 CAISO (ICE)

**Hubs:** **NP-15** (Northern California) and **SP-15** (Southern California) are the main ICE hubs; settlement is against CAISO **LMPs** (day-ahead or real-time per contract). **PPT** = Pacific Prevailing Time; peak is usually **HE 0700–2200 PPT** (16 hours).

**Nx16 and block notation:** As in ERCOT, **Nx16** = N days per week × 16 peak hours. CAISO also has **1x16** (single-day 16h) and **6x16** (e.g. Mon–Sat) in addition to 5x16, 2x16, 7x16. Product symbols and exact day definitions are in the ICE (and CME) product specs; below is a compact overview of **available product types** for NP-15 and SP-15.

**Block products (ICE) — NP-15 and SP-15:**

- **1x16 (daily peak):** **1 day** × **16 hours** (HE 0700–2200 PPT). One price per **calendar day** for the 16 peak hours. Traded as **daily** contracts. Tickers: **NRP** = NP-15 Real-Time Peak Daily; **SRP** = SP-15 Real-Time Peak Daily; Day-Ahead Peak Daily symbols vary — check ICE.
- **5x16 (weekday peak):** Monday–Friday × 16 hours. **NPM** = NP-15 Day-Ahead Peak (monthly); SP-15 Day-Ahead Peak monthly; Real-Time Peak monthly/calendar for 5x16 where listed.
- **6x16 (six-day peak):** **6 days** × 16 hours — typically Monday–Saturday. Available as monthly or calendar where listed; check ICE for exact tickers per hub.
- **7x16 (all-days peak):** 7 days × 16 hours. **2x16** (weekend-only peak) may be quoted; 5x16 and 2x16 together consistent with 7x16.
- **Day-Ahead vs Real-Time:** Both hubs have **DA** and **RT** products; use the market that matches your exposure.
- **Narrow peak (HE 0900–1600):** **CNG** = SP-15 Day-Ahead Peak HE 0900–1600 (8h “super-peak”); NP-15 Day-Ahead Peak Daily HE 0900–1600 — check ICE for symbol.
- **Off-peak:** **ONP** = NP-15 Day-Ahead Off-Peak (monthly); **OFP** = SP-15 Day-Ahead Off-Peak (monthly); Real-Time Off-Peak where listed; often implied from ATC and peak.
- **Contract sizes:** Commonly **400 MWh** or **1 MW**; min tick **$0.01/MWh**; listing up to 365 days (daily) or monthly/quarterly/calendar.

**CAISO NP-15 / SP-15 — ticker reference (ICE):**

| Hub   | Product                     | Ticker | Notes                          |
|-------|-----------------------------|--------|--------------------------------|
| NP-15 | Real-Time Peak Daily        | **NRP**| 1x16, HE 0700–2200 PPT         |
| SP-15 | Real-Time Peak Daily        | **SRP**| 1x16, HE 0700–2200 PPT         |
| NP-15 | Day-Ahead Peak (monthly)    | **NPM**| 5x16 monthly                   |
| NP-15 | Day-Ahead Off-Peak (monthly) | **ONP**| Off-peak monthly               |
| SP-15 | Day-Ahead Off-Peak (monthly)| **OFP**| Off-peak monthly               |
| SP-15 | Day-Ahead Peak HE 0900–1600 | **CNG**| 8h super-peak                  |
| NP-15 | Day-Ahead Peak Daily HE 0900–1600 | (ICE) | Check ICE for symbol   |
| SP-15 | Day-Ahead Peak (monthly)    | (ICE)  | 5x16; see ICE product list     |

**Summary of available product types (CAISO):**

| Block   | Description              | Typical use / note                    |
|---------|--------------------------|---------------------------------------|
| **1x16** | One day, 16 peak hours   | Daily peak; **NRP**, **SRP**; prompt HPFC |
| **5x16** | Mon–Fri, 16h             | Standard weekday peak; **NPM** (NP-15) |
| **6x16** | Mon–Sat, 16h             | Six-day peak (Sunday off)             |
| **2x16** | Sat–Sun, 16h             | Weekend peak (with 5x16 → 7x16)      |
| **7x16** | All days, 16h            | Undifferentiated peak                 |
| **Off-peak** | Remaining hours       | **ONP**, **OFP** (DA monthly)         |
| **HE 0900–1600** | 8h strip           | Super-peak; **CNG** (SP-15)           |

**Shaping in practice:**  
Use the **block prices** you have (e.g. monthly 5x16, 7x16, 1x16 daily for prompt, off-peak, and optionally 6x16, 2x16, or HE 0900–1600). For each month (and each day where 1x16 is used):

1. Anchor **level** to ATC (or base), **7x16**, **5x16**, **2x16**, **6x16** as available; imply off-peak where needed.
2. Apply **historical** NP-15 or SP-15 hourly shape (day-of-week + hour-of-day; separate weekend if 2x16 is used).
3. **Normalize** so the average over every traded block (month ATC, month 5x16, month 2x16, daily 1x16, etc.) equals the market price for that block.
4. Result: **HPFC** for NP-15 or SP-15 consistent with ICE (and, if used, CME) block prices. Use **DA** blocks for day-ahead exposure and **RT** blocks for real-time.

---

## 6. One formula to remember

**Off-peak from base and peak (same period):**

$$
P_{\mathrm{off}} = \frac{H_{\mathrm{base}}\, P_{\mathrm{base}} - H_{\mathrm{peak}}\, P_{\mathrm{peak}}}{H_{\mathrm{off}}}.
$$

**Shaping** = choose an **hourly profile** (from history, fundamentals, or a template) and **scale/normalize** so that the **average** over every traded block equals the **market** block price. That gives you an **HPFC** that is arbitrage-free and usable for valuation, risk, and trading.
