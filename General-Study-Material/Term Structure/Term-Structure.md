# Term Structure and Curve Building in Energy Commodities

A beginner-oriented guide with formulas, methods, pros/cons, and how they support portfolio managers and traders.

---

## 1. What is term structure?

**Term structure** is the relationship between **price** and **time to delivery** for a commodity. In energy (power, gas, oil), you don’t have a single “price” — you have prices for different delivery periods: next hour, next day, next month, next quarter, next year, etc. Term structure is the **curve** that links those prices.

- **Spot / prompt:** Delivery soon (e.g. next day or next month).
- **Forward / deferred:** Delivery further out (e.g. next quarter, next calendar year).

So “curve building” means **constructing a consistent set of forward prices** (and sometimes volatilities) across all relevant delivery dates, using whatever inputs you have (quotes, historical data, models).

---

## 2. Why it matters

- **Valuation:** Any contract with future delivery (forwards, futures, options, FTRs/CRRs) is valued off the forward curve.
- **Hedging:** Hedging future exposure requires knowing forward prices and their relationships (spreads, basis).
- **Trading:** Term structure shows **contango** (forward > spot) vs **backwardation** (forward < spot) and where the curve is steep or flat — that drives spread and calendar trades.
- **Risk:** Mark-to-market, P&amp;L attribution, and risk limits all depend on a proper curve.

---

## 3. Core concepts (step by step)

### 3.1 Spot vs forward

- **Spot price** $S_t$: price for immediate (or very prompt) delivery at time $t$.
- **Forward price** $F_{t,T}$: price agreed today for delivery at time $T$, with $T > t$.

No-arbitrage (simplified, no convenience yield) gives:

$$
F_{t,T} = S_t \, e^{(r - q)(T - t)}
$$

where $r$ = risk-free rate, $q$ = convenience yield (or net cost of carry). In power, storage is limited, so the “cost of carry” story is less clean than in oil; curves are driven more by **expected scarcity** and **seasonality**.

### 3.2 What do we mean by no-arbitrage?

**No-arbitrage** means the curve does not allow a **risk-free profit** with zero net investment. If such an opportunity existed, market participants would trade it until prices moved and the opportunity disappeared. So we **build and assume** curves that rule out these profits.

**In term structure, no-arbitrage usually means:**

- **Spot–forward consistency (cost of carry):** You cannot lock in a risk-free gain by buying spot and selling forward (or the reverse) and holding to delivery. The forward $F_{t,T}$ must equal the cost of "buy spot today and carry to $T$" — i.e. $F_{t,T} = S_t e^{(r-q)(T-t)}$ (or the appropriate variant with storage and convenience). If $F_{t,T}$ were too high relative to $S_t$ and carry, you could sell the forward, buy spot, finance and store, deliver at $T$, and pocket the difference with no risk; that would be an arbitrage. So "no arbitrage" pins the **level** of the forward relative to spot and carry.

- **Calendar spread consistency:** You cannot lock in a risk-free gain from the **spreads between** delivery dates. For example, the price for delivery in month $T_2$ should not be **lower** than the price for delivery in the earlier month $T_1$ (assuming the same product and no storage cost that could justify a negative spread). If the curve said $F_{T_2} < F_{T_1}$ with $T_2 > T_1$, you could buy $T_2$ and sell $T_1$, take delivery in $T_1$ and "carry" to $T_2$ (or deliver against the $T_2$ contract), and earn a risk-free spread. So we require that **calendar spreads** implied by the curve are consistent with storage and carry: no **negative** carry (unless storage is costly enough to justify it in the model). In practice, "no-arbitrage" curve building often means **non-negative forward spreads** between adjacent tenors (or spreads within bounds set by storage cost).

- **Rates curve:** For interest rates, no-arbitrage means **discount factors** are positive and **decreasing** in maturity (so forward rates are non-negative, or within allowed bounds). Otherwise you could borrow at a lower rate and lend at a higher rate for the same period with no risk.

**Why it matters for curve building:** If we **interpolate** or **extrapolate** without constraints, we can accidentally produce a curve that implies an arbitrage (e.g. a later delivery cheaper than an earlier one with no economic reason). **No-arbitrage methods** (e.g. monotone splines, constrained bootstrap) build curves that **by construction** satisfy these consistency conditions, so valuation and risk metrics are not distorted by "impossible" prices.

### 3.3 Where do we get $q$ (cost of carry)?

In theory, $q$ is the **net convenience yield**: benefit of holding physical (e.g. optionality, supply assurance) minus storage cost. In practice we rarely observe $q$ directly; we **imply** it from the curve or treat it as absent for non-storable products.

- **Oil (and other storable commodities):**  
  - **Implied from the curve:** Given liquid spot $S_t$ and forward $F_{t,T}$, and risk-free rate $r$, we can back out $q$ from $F_{t,T} = S_t e^{(r-q)(T-t)}$, i.e. $q = r - \frac{1}{T-t}\ln(F_{t,T}/S_t)$. So $q$ is the **implied convenience yield** (or net carry) that makes the no-arbitrage formula hold.  
  - **Storage market:** In some markets, storage is traded (e.g. pipeline capacity, tank storage). The spread between prompt and deferred, after financing, reflects the marginal cost/benefit of carry and can inform $q$ or validate the implied value.  
  - **Typical use:** Curve builders often use $r$ from rates markets and then **let the liquid forward quotes define the curve**; the implied $q$ is then implicit in the built curve rather than input explicitly.

- **Gas:**  
  - **Storage exists** (salt caverns, aquifers, LNG), so a carry story applies over seasonal horizons. $q$ can be **implied** from winter vs summer strips (e.g. winter premium vs financing) or from storage spread quotes.  
  - **Short-dated:** Prompt gas is often driven by weather and balance; the "$q$" that would fit $F = S e^{(r-q)\tau}$ is time-varying and can be **negative** (backwardation when prompt is tight).  
  - **Practical:** Many shops build the gas curve from **liquid forwards** and interpolate; the implied carry is embedded in those quotes rather than estimated as a separate input.

- **Power:**  
  - **Storage is limited** (batteries, pumped hydro); bulk energy is not storable like oil or gas. So there is **no meaningful tradable cost of carry** for "energy" across months in the same way.  
  - The relationship $F_{t,T} = S_t e^{(r-q)(T-t)}$ is **not used to define** power curves in practice. Instead, curves are built from **liquid forward quotes** (prompt month, balance of month, calendar months, quarters, seasons) and **seasonality/fundamentals**.  
  - If one insisted on an "implied $q$" from observed $F$ and $S$, it would be **highly seasonal and volatile** (e.g. large and negative into peak summer/winter), reflecting expected scarcity, not carry. So for power, **we don't source $q$** — we treat the forward curve as the primitive and build it from quotes and seasonal/fundamental models.

**Takeaway:** For **oil (and storable commodities)**, $q$ is implied from spot vs forward or inferred from storage markets. For **gas**, $q$ can be implied from seasonal spreads and storage, but curve building often uses liquid forwards directly. For **power**, $q$ is not a practical input; the curve is built from forwards and seasonality, and the cost-of-carry formula is a **reference** rather than an operational source of $q$.

### 3.4 Contango and backwardation

- **Contango:** $F_{t,T} > S_t$ — forward above spot (common when storage is cheap and supply is ample).
- **Backwardation:** $F_{t,T} < S_t$ — forward below spot (often when prompt is tight or storage is full).

In power, **seasonality** is strong (summer/winter peaks), so you see backwardation into peak months and contango into off-peak.

### 3.5 Calendar spreads and basis

- **Calendar spread:** difference between two forward prices, e.g. $F_{t,T_2} - F_{t,T_1}$. Traded explicitly in many markets (e.g. power: next month vs next quarter).
- **Basis:** price difference between two **locations** or **products** (e.g. hub A vs hub B, or gas at Henry Hub vs at a power hub). Basis is often quoted as a spread to a benchmark curve.

Curve building must be **internally consistent** so that calendar spreads and basis relationships are coherent.

### 3.6 Storage and storage spread quotes

For **storable** commodities (oil, gas, and to a limited extent NGLs/products), **storage** is a link between prompt and deferred prices. When storage is **traded** or **quoted**, those quotes inform the curve and the implied cost of carry.

**What is "storage" in markets?**

- **Physical storage:** Tanks (oil), salt caverns / aquifers / LNG (gas). The owner can **inject** when prompt is cheap and **withdraw** when prompt is expensive, earning the **spread** between delivery dates minus **storage cost** (rent, operating cost, fuel, losses).
- **Storage as optionality:** The right to inject/withdraw is an option on the calendar spread; value depends on volatility and convenience yield. So storage value is not just the current spread but the option to use the spread over time.

**What are "storage spread quotes"?**

- **Gas:**  
  - **Spread quotes** are often the **price difference** between two delivery periods (e.g. winter strip vs summer strip, or month $T_1$ vs $T_2$). Example: "Winter '25 vs Summer '25 at +0.80 $/MMBtu" means winter is 0.80 above summer.  
  - The **storage spread** is the calendar spread a storage operator can capture: buy summer, store, sell winter. The **quoted spread** (winter − summer) is the market's implied value of that trade; after subtracting **storage cost** (in $/MMBtu or $/unit of capacity), the remainder is related to **convenience yield** or scarcity.  
  - **Where you see them:** Brokers and OTC markets quote **strip spreads** (e.g. balance-of-winter vs balance-of-summer, or month-on-month). Some venues quote **storage capacity** (injection/withdrawal rates, working gas) and the implied **spread** to fill that capacity.

- **Oil:**  
  - **Spread quotes** are calendar spreads (e.g. front month vs 6th month, or prompt vs 12-month forward). The **contango** (forward − spot) must at least cover **storage cost** (tank rent, insurance, financing) or arbitrage would exist.  
  - **Storage spread** here is the spread needed to **cover the cost of storing** for a period. When the market quotes "M1–M6 spread" or "front–back," that spread is compared to **storage cost** for that period; if spread > storage cost, it can be profitable to store (and the implied $q$ is lower or negative).  
  - **Floating storage:** For crude, "floating storage" (tankers) is sometimes quoted as a **spread** (e.g. forward minus spot minus shipping and time charter) that makes it economic to hold oil on water.

**How storage spread quotes help curve building**

- **Consistency check:** A built forward curve implies **calendar spreads** (e.g. winter − summer). If the curve's implied spread is far from **observed storage spread quotes**, the curve may be mispriced or the market is implying a different storage/carry value.  
- **Input to $q$:** For gas, the **winter–summer spread** (after adjusting for financing and storage cost) is a direct input to the **implied convenience yield** over that horizon. Large winter premium → high convenience to holding winter gas → backwardation into winter.  
- **Valuation of storage:** Traders and quants value **storage contracts** (e.g. salt cavern for a season) by using the **forward curve** and **spread quotes** to estimate inject/withdraw optionality and spread capture; the curve and storage quotes must be consistent.

**Takeaway:** **Storage spread quotes** are market quotes for the **calendar spread** between delivery periods (e.g. winter vs summer gas, front vs deferred oil). They reflect the value of moving commodity across time via storage. Curve builders use them to **validate** implied carry, to **inform** $q$ (especially in gas), and to keep the curve consistent with the **marginal cost/benefit of storage** observed in the market.

---

## 4. Building the curve: what you have and what you want

**Inputs (typically):**

- **Liquid points:** exchange or OTC quotes for specific delivery periods (e.g. prompt month, next month, balance of month, calendar months, quarters, seasons, calendar years).
- **Few or no quotes:** for many delivery months or hours (e.g. individual months 3 years out). Those have to be **interpolated** or **extrapolated**.

**Output:**

- A **continuous** (or granular) forward curve: a price (and optionally volatility) for every delivery period you need for valuation and risk.

So “curve building” = **blend liquid quotes + fill gaps with a consistent method**.

---

## 5. Main methods for curve building

Below we outline common approaches, with formulas, pros/cons, and how they help PMs and traders.

---

### 5.1 Linear interpolation (in time)

**Idea:** Between two quoted tenors $T_1$ and $T_2$ with prices $F_1$ and $F_2$, set:

$$
F(T) = F_1 + \frac{F_2 - F_1}{T_2 - T_1}(T - T_1), \qquad T_1 \leq T \leq T_2.
$$

**Pros:** Simple, no extra data, fast; exactly matches quoted points.  
**Cons:** Kinks at every quote; no smoothness; can produce unrealistic spikes or flat segments; no guarantee of no-arbitrage (e.g. negative spreads between adjacent months).  
**For PMs/traders:** Good for a quick first pass; not ideal for risk or for valuing options (rough curve → rough Greeks).

---

### 5.2 Cubic spline interpolation

**Idea:** Fit a piecewise cubic polynomial through quoted points so that the curve is **continuous** and has **continuous first derivative** (and often second). So $F(T)$ is smooth between quotes.

**Formula:** Given **knots** (quoted tenors) $T_0 < T_1 < \cdots < T_n$ with prices $F_0, F_1, \ldots, F_n$, on each segment $[T_i, T_{i+1}]$ the curve is a cubic:

$$
F(T) = a_i + b_i (T - T_i) + c_i (T - T_i)^2 + d_i (T - T_i)^3, \qquad T \in [T_i, T_{i+1}].
$$

The coefficients $a_i, b_i, c_i, d_i$ are chosen so that:
- **Value match:** $F(T_i) = F_i$ and $F(T_{i+1}) = F_{i+1}$ (the curve passes through the quoted points).
- **Smoothness:** At each **internal** knot $T_i$ ($i = 1, \ldots, n-1$), the **first derivative** $F'(T)$ and (usually) the **second derivative** $F''(T)$ from the left and right segments are equal. So $F$ and $F'$ (and $F''$) are continuous everywhere.
- **Boundary conditions:** At the ends $T_0$ and $T_n$, one imposes an extra condition (e.g. **natural spline:** $F''(T_0) = F''(T_n) = 0$; or **clamped:** fix $F'(T_0)$ and $F'(T_n)$ from data or assumption). These close the system so the $a_i, b_i, c_i, d_i$ are uniquely determined.

So there are $4n$ coefficients ($4$ per segment) and the value + smoothness + boundary conditions give exactly $4n$ linear equations, yielding a unique cubic spline.

**Pros:** Smooth curve; no kinks at quotes; often looks more realistic than linear.  
**Cons:** Can still **oscillate** (overshoot) between points, especially with few points or big gaps; no built-in no-arbitrage; not necessarily stable when one quote moves.  
**For PMs/traders:** Better for presentation and for stable Greeks than linear; still need to check for arbitrage (e.g. negative calendar spreads) and fix by hand or with constraints.

---

### 5.3 Monotone / no-arbitrage splines

**Idea:** Use splines with **constraints** so that forward prices (or discount factors / cumulative costs) satisfy no-arbitrage. For example, require that **calendar spreads** between adjacent delivery periods are non-negative (or within known bounds), so the curve cannot imply negative carry.

**Pros:** Curve is both smooth and arbitrage-free; suitable for marking and risk.  
**Cons:** More complex to implement; may need to relax some quotes (e.g. allow small violations) if the input quotes themselves are inconsistent.  
**For PMs/traders:** Preferred for **official** curves used in valuation and risk limits; gives confidence that P&amp;L and hedges are not distorted by arbitrage in the curve.

---

### 5.4 Seasonal decomposition (e.g. power / gas)

**Idea:** Model the forward curve as **trend + seasonality**:

$$
F(T) = \mu(T) + \sum_k \bigl( a_k \cos(\omega_k T) + b_k \sin(\omega_k T) \bigr),
$$

where $\mu(T)$ is a slow-moving level (e.g. linear or low-order polynomial) and the sum captures seasonal cycles (e.g. annual, semi-annual). Fit to history and/or to liquid quotes.

**Pros:** Reflects known seasonality (summer/winter in power and gas); can fill many months with few parameters; good for long-dated strips where quotes are sparse.  
**Cons:** Assumes a fixed seasonal pattern; can be wrong in regime shifts (e.g. new renewables, demand changes); usually need to **blend** with liquid quotes so short end is not distorted.  
**For PMs/traders:** Helps value long-dated positions and assess whether the market is cheap or rich relative to “normal” seasonality; supports strategic calendar and seasonal trades.

---

### 5.5 Bootstrapping (from liquid to illiquid)

**Idea:** Build the curve **chronologically**: start from the most prompt liquid point, then use the next liquid point to imply the **forward** (or average price) for the period in between, then move to the next, and so on. So you “bootstrap” from known to unknown tenors.

**Example:** You have quotes for Month 1 ($F_1$) and Month 3 ($F_3$). You need Month 2. If the curve is in “average price per month” space, you might set $F_2$ so that a no-arbitrage condition holds (e.g. cost of holding across 1→2→3 is consistent). In a simple form:

$$
F_2 \approx 2 F_{1,3} - F_1 \quad \text{(e.g. if } F_{1,3} \text{ is the 2-month average)},
$$

or use a proper bootstrap that respects day counts and compounding.

**Pros:** Uses liquid information first; avoids arbitrary interpolation in the most traded tenors.  
**Cons:** Depends on having a clear ordering and a model for how tenors relate (e.g. average vs prompt); can be sensitive to a single bad quote.  
**For PMs/traders:** Aligns the curve with where the market actually trades; good for marking and for understanding which tenors are “implied” vs “quoted.”

---

### 5.6 Model-based curves (e.g. mean-reversion + seasonality)

**Idea:** Assume spot (or prompt price) follows a stochastic process (e.g. mean-reverting with seasonal level):

$$
dS_t = \kappa\bigl(\theta(t) - S_t\bigr) dt + \sigma(t) dW_t,
$$

with $\theta(t)$ seasonal. Then **forward price** is the expected spot under the risk-neutral measure:

$$
F_{t,T} = \mathbb{E}^\mathbb{Q}[S_T \mid \mathcal{F}_t].
$$

You calibrate $\kappa$, $\theta(\cdot)$, $\sigma(\cdot)$ to liquid options and/or historical data, then build $F_{t,T}$ for all $T$.

**Pros:** Theoretically consistent; can price options and exotics; forward curve and volatility term structure come from the same model.  
**Cons:** More complex; model risk; may not fit every liquid quote exactly.  
**For PMs/traders:** Used for **options books** and structured products; helps with delta-hedging and volatility trading; less often the single source for “plain” forward curves in power unless the desk is options-focused.

---

## 6. Interest rate curves: what they are, what is available, how they are built

Commodity valuation and risk use **interest rates** for discounting (NPV of forward curves, FTR payouts, options) and in cost-of-carry ($r$ in $F = S e^{(r-q)(T-t)}$). The **rates curve** is the term structure of risk-free (or funding) rates — we build it from liquid rates instruments so we can compute **discount factors** and **forward rates** for any tenor.

### 6.1 What we mean by "rates curve"

- **Discount factor** $D(T)$: today's value of 1 unit paid at time $T$. So $D(T) = e^{-r(T) \cdot T}$ if $r(T)$ is the **zero rate** (continuously compounded) for maturity $T$, or $D(T) = 1/(1 + y(T))^T$ in simple yield terms depending on convention.
- **Zero rate** $r(T)$: the constant rate (out to $T$) that gives $D(T)$; $D(T) = e^{-r(T) T}$.
- **Forward rate** $f(t,T_1,T_2)$: rate implied today for borrowing/lending from $T_1$ to $T_2$; no-arbitrage gives $e^{-r(T_1)T_1} e^{-f \cdot (T_2-T_1)} = e^{-r(T_2)T_2}$, so forwards are implied by the zero (or discount) curve.

The **curve** is the function $T \mapsto D(T)$ (or $T \mapsto r(T)$). We build it from liquid quotes and interpolate so we can discount any cash flow and compute forward rates.

### 6.2 What is available (instruments and data)

Liquid rates instruments differ by currency and jurisdiction. Typical building blocks:

- **Money market / short end (e.g. 0–2 years):**  
  - **Deposits:** Cash deposits (O/N, T/N, 1w, 1m, 2m, 3m, 6m, 12m) — give **spot** or **forward-start** rates.  
  - **OIS (overnight index swap):** Fixed leg vs geometric average of overnight rate (Fed Funds, **SOFR** — Secured Overnight Financing Rate — EONIA, etc.). OIS is the standard **discounting** curve for collateralized derivatives in many jurisdictions (USD: SOFR; EUR: ESTR).  
  - **Futures:** Short-term rate futures (e.g. Fed Funds futures, SOFR futures) — imply **forward** overnight or 3m rates; often used for the first 2–3 years before switching to swaps.

- **Swap curve (e.g. 2–30+ years):**  
  - **Interest rate swaps (IRS):** Fixed leg vs floating (e.g. 3m SOFR, 6m LIBOR legacy). Par swaps (fixed rate such that NPV = 0) give **par rates** at standard tenors (2y, 3y, 4y, 5y, 7y, 10y, 15y, 20y, 30y). From par rates we **bootstrap** or **solve** for zero rates (or discount factors).  
  - **Basis:** In multi-curve settings, there is a **discount curve** (e.g. OIS) and **forward curves** (e.g. 3m SOFR for floating leg). Basis swaps (e.g. 3m vs overnight) inform the spread between them.

- **Government bonds (optional):** In some currencies, government bonds are used for the long end or for a "risk-free" reference; they are often converted to a zero-coupon curve via **bootstrap** from the shortest maturity upward.

**In practice (e.g. USD):** Use **SOFR OIS** for discounting; **SOFR futures** and **SOFR-based swaps** (or legacy LIBOR until transition) for the curve. Data comes from **brokers**, **clearing houses** (e.g. LCH), and **vendors** (Bloomberg, Refinitiv). For a commodity shop, the rates desk or risk often provides a **single discount curve** (e.g. OIS) and possibly a **funding spread** on top for uncollateralized exposure.

### 6.3 Methods of building the rates curve

**Step 1: Choose the "pillar" instruments.**  
Order them by maturity (e.g. deposits 1m, 3m, 6m; futures for 1–2 years; par swaps 2y, 3y, 5y, 7y, 10y, 20y, 30y). Each pillar gives a **constraint** (e.g. the present value of the fixed leg of a par swap must equal the present value of the floating leg, so the swap has zero NPV).

**Step 2: Bootstrap discount factors (or zero rates).**  
- Start at $T=0$ with $D(0)=1$.  
- Use the **shortest** instrument to get $D(T_1)$ (e.g. from a deposit or OIS).  
- Move to the next: use the next instrument's cash flows and **already known** $D(\cdot)$ to solve for the **next** $D(T)$ at the instrument's maturity.  
- Repeat so that every pillar is exactly repriced. This gives $D(T)$ at **discrete** pillar dates.

**Step 3: Interpolate between (and beyond) pillars.**  
We need $D(T)$ for every $T$, not just at pillars. Common choices:

| Method | What is interpolated | Pros | Cons |
|--------|----------------------|------|------|
| **Linear in discount factor** | $D(T)$ linear between pillars | Simple; no-arbitrage (positive $D$, decreasing in $T$ if rates positive) | Kinks at pillars; forward rates can jump |
| **Linear in log discount** | $\ln D(T)$ linear | Smoother forwards than linear $D$; still no-arbitrage | Forwards not continuous at pillars |
| **Cubic spline in discount** | $D(T)$ as cubic spline | Smooth curve and forwards | Can oscillate; need monotonicity constraints to avoid negative forwards |
| **Cubic spline in zero rate** | $r(T)$ as cubic spline | Intuitive (direct zero curve) | Risk of negative forwards or arbitrage if unconstrained |
| **Monotone / no-arbitrage spline** | $D(T)$ or $r(T)$ with constraints | Smooth and no negative forwards; suitable for risk and valuation | More implementation work |

**No-arbitrage:** For the curve to be arbitrage-free, **discount factors** must be positive and **decreasing** in $T$ (for positive rates), and **forward rates** must be non-negative (or bounded below by a floor) if we want to avoid arbitrage. So in practice, **linear in $D$** or **monotone spline in $D$** are safe choices; unconstrained splines in $r$ or $D$ can violate this and need checking.

### 6.4 Single vs multi-curve

- **Single-curve (legacy):** One curve used for both discounting and forwarding. Simpler but no longer standard for cleared/collateralized derivatives.
- **Multi-curve:** Separate **discount curve** (e.g. OIS) and **forward curves** (e.g. 3m SOFR for floating leg). Swap valuation: discount fixed and floating cash flows with the discount curve; floating leg uses forward rates from the relevant forward curve. Basis between tenors (e.g. 3m vs 1m) is then part of the construction.

For a **commodity shop**, risk and valuation typically take the **discount curve** as given (from treasury or a rates vendor) and use it to:
- Discount commodity forward curves and option payoffs.
- Plug $r$ into cost-of-carry formulas where applicable (e.g. oil).
- Value FTR/CRR payouts (often a stream of spread × quantity over time) at NPV.

### 6.5 Summary: rates curve in one paragraph

The **interest rate curve** is built from **liquid instruments** (deposits, OIS, futures, par swaps) by **bootstrapping** discount factors at pillar maturities, then **interpolating** (e.g. linear in $D$, or monotone spline) so that discount factors and forward rates exist for any tenor. **OIS** (e.g. SOFR OIS in USD) is typically used for **discounting** collateralized positions. Methods that preserve **positive, decreasing discount factors** and **non-negative forwards** keep the curve arbitrage-free and suitable for marking and risk.

---

## 7. Summary: how methods help PMs and traders

| Method              | Best for                          | PM/Trader use                                                                 |
|---------------------|-----------------------------------|-------------------------------------------------------------------------------|
| Linear interp       | Quick checks, ad hoc              | Fast sanity check; not for official marks or risk.                            |
| Cubic spline        | Smooth curves, reporting          | Smoother Greeks and reports; still need arbitrage checks.                     |
| No-arbitrage spline | Official marks, risk, limits      | Reliable valuation and risk; no “phantom” arbitrage in the curve.              |
| Seasonal decomp     | Long-dated, sparse quotes         | Strategic calendar/seasonal views; long-dated fair value.                      |
| Bootstrapping       | Aligning with liquid tenors       | Curve that matches where the market trades; clear implied vs quoted.          |
| Model-based         | Options, exotics, vol term struct | Options pricing, hedging, vol surface; consistent curve + vol.                |

---

## 8. Practical example (power)

- **Liquid:** Prompt month 50 $/MWh, next month 48, Q2 45, Cal 24 44.  
- **Goal:** Build a monthly curve for the next 12 months.

**Steps:**

1. **Anchor** on the four quotes (they are your “pillars”).
2. **Between pillars:** Use cubic or no-arbitrage spline so that:
   - You get smooth monthly prices.
   - No adjacent month has a negative spread (or you fix with constraints).
3. **Seasonality:** If you have historical monthly patterns, you can use them to **adjust** the spline so that summer/winter look reasonable relative to history; or use a seasonal model for months beyond the last liquid point.
4. **Check:** Compare implied calendar spreads (e.g. Jul vs Aug) to any OTC or broker quotes; if your curve implies a spread that no one would trade, revisit inputs or method.

**For a trader:** The curve gives fair value for each month; they can trade calendar spreads when the market deviates from that fair value.  
**For a PM:** The curve is the reference for marking positions and measuring P&amp;L; a no-arbitrage method avoids misstating risk and attribution.

---

## 9. One formula to remember

**No-arbitrage forward (cost of carry):**

$$
F_{t,T} = S_t \, e^{(r - q)(T - t)}.
$$

In power, this is a **reference** more than a literal formula (storage is limited, so $q$ is not like in oil). The real takeaway: **term structure ties together spot, forwards, and time** — and curve building is the process of making that tie consistent and usable for valuation, hedging, and trading.
