# US FTR, Gas and Power Risk – Quantitative Researcher (JD prep)

## 1. Risk models for commodity products and derivatives (term structures, volatility surfaces)

**Bullet:** Formulate and implement models for risk analysis of commodity products and derivatives, such as methodologies for constructing term structures and volatility surfaces.

### Models / skills needed (brief)

- **Term structures:** Curve-building for forwards (power, gas): bootstrap from liquid contracts (prompt, balance-of-month, month-ahead, quarters, strips); interpolation (linear, cubic spline, Nelson–Siegel) and extrapolation; seasonality (e.g. monthly/quarterly dummies or sinusoidal); consistency with liquid options if used for discounting/vol.
- **Volatility surfaces:** Implied vol from options (calls/puts, possibly swaptions); strike space (moneyness, delta) and term space; sticky-strike vs sticky-delta vs local vol; power/gas specifics (spikes, mean reversion, seasonality in vol); calibration to market (least-squares, smoothness penalties); arbitrage-free constraints (no calendar/triangle arbitrage).
- **Risk metrics:** Greeks (delta, gamma, vega) on curves and surfaces; VaR/CVaR (historical, parametric, Monte Carlo); scenario and stress tests; PnL explain (curve move, vol move, theta).
- **Implementation:** Numerical methods (root-finding, optimization), stable calibration, code (Python/C++), versioning and backtesting of model changes.

### Formulas (reference)

**Term structure / no-arbitrage**
- Forward (risk-neutral): $F(t,T) = \mathbb{E}^\mathbb{Q}[S_T \mid \mathcal{F}_t]$. With storage/cost of carry: $F(t,T) = S_t e^{(r-q)(T-t)}$ (simplified).
- Discount factor: $P(t,T)$ for time-$T$ cash flow valued at $t$.

**How to get forward rates**

1. **From discount factors (interest-rate curve)**  
   Bootstrap a discount curve $P(t,T)$ from liquid rates (e.g. deposits, futures, swaps). Then:
   - **Zero rate** (continuously compounded): $P(t,T) = e^{-r(t,T)(T-t)}$ $\Rightarrow$ $r(t,T) = -\frac{\ln P(t,T)}{T-t}$.
   - **Simply compounded forward rate** for period $[T_1, T_2]$ (e.g. 3m LIBOR-style):
   $$
   1 + f(t; T_1, T_2)\,\tau = \frac{P(t,T_1)}{P(t,T_2)} \quad \Rightarrow \quad f(t; T_1, T_2) = \frac{1}{\tau}\left( \frac{P(t,T_1)}{P(t,T_2)} - 1 \right),
   $$
   where $\tau = \text{day count}(T_1, T_2)$. No-arbitrage: locking in $f$ via lending from $T_1$ to $T_2$ must match borrowing today to $T_2$ and repaying at $T_1$.

2. **From commodity forwards (power/gas)**  
   Forward *prices* $F(t,T)$ (e.g. \$/MWh or \$/MMBtu) are the tradable objects. Build the curve by:
   - Using **liquid pillars**: prompt, balance-of-month, monthly contracts, quarterly strips. Each quoted price is the forward for that delivery period.
   - **No-arbitrage between periods**: e.g. a quarterly contract must equal a consistent average of the constituent monthly forwards; solve or interpolate so the calendar is consistent (no arbitrage between overlapping products).
   - **Interpolation**: between pillar dates use splines or parametric forms (e.g. Nelson–Siegel on log-prices or on spreads to a reference). **Forward rate** in a commodity context often means the **instantaneous forward price** $F(t,T)$ or the **forward return** $\mu(t,T)$ in a model (e.g. $F(t,T) = F(t,T_0) \exp(\int_{T_0}^T \mu(t,u)\,du)$); these are backed out from the built curve.

**Basis in the context of forward contracts**

**Definition**  
**Basis** = the **difference** between two related prices. In forwards it usually refers to (a) **location basis** (price at location A minus price at a **reference hub**), (b) **calendar basis** (forward for one period minus forward for another), or (c) **spot–forward basis** (cash/spot minus forward). Basis is quoted in **\$/unit** (e.g. \$/MWh, \$/MMBtu) and can be **positive** or **negative**.

**Location basis (power and gas)**  
- **Forward at location:** $F_{\mathrm{loc}}(t,T)$ = forward price at a **specific** location (e.g. a load zone, pipeline hub). The **liquid** contract is often at a **benchmark hub** (e.g. Henry Hub for gas, ERCOT North for power).  
- **Basis forward:** $B(t,T) = F_{\mathrm{loc}}(t,T) - F_{\mathrm{hub}}(t,T)$. Then
$$
F_{\mathrm{loc}}(t,T) = F_{\mathrm{hub}}(t,T) + B(t,T).
$$
- **Use:** A **forward contract** at the **location** is equivalent to **hub forward** + **basis forward**. **Basis risk** = risk that $B(t,T)$ moves (pipeline congestion, local demand, outages). **Basis contracts** (forwards or options on $B$) allow hedging location-specific exposure.

**Calendar basis**  
- **Spread** between two **forward** delivery periods: e.g. $F(t,T_1) - F(t,T_2)$ (e.g. **winter** minus **summer**, or **prompt** minus **next month**).  
- **Use:** **Spread** trades (e.g. long winter, short summer); **storage** value depends on calendar spread. **Calendar basis** can be **backwardation** (near &gt; far) or **contango** (far &gt; near).

**Spot–forward basis (optional)**  
- $S_t - F(t,T)$ = **cash** (or prompt) minus **forward** for $T$. In theory, $F(t,T) = \mathbb{E}^\mathbb{Q}[S_T]$; the **realized** spread $S_T - F(t,T)$ at expiry is the **settlement** P&L of a forward. **Basis risk** for a **physical** position hedged with a **financial** forward = risk that **physical** delivery price differs from the **index** that settles the forward.

**Basis risk in a hedged forward**  
- **Exposure:** You have **physical** or **economic** exposure at **price** $P$ (e.g. price at your location).  
- **Hedge:** You enter a **forward** on **index** $I$ (e.g. hub price) with delivery $T$. At $T$, you receive/pay $I_T - F(t,T)$ on the forward.  
- **Basis:** $P_T - I_T$ = **location basis at settlement**. Your **total** P&L = (exposure on $P$) + (forward P&L on $I$). If $P$ and $I$ don’t move 1:1, **basis** $P - I$ moves and the hedge is **imperfect**. **Basis risk** = variance of $(P_T - I_T)$ (or of the change in basis).  
- **Formula (hedge P&L):** Suppose you are **short** $Q$ units at price $P$ (you sell at $P$) and **long** a forward on $I$ for quantity $Q$ at forward price $F$. At $T$: exposure P&L = $Q(P_T - \ldots)$; forward P&L = $Q(I_T - F)$. Net exposure to **basis** = $Q(P_T - I_T)$.

**Summary**

| Type | Formula | Use |
|------|---------|-----|
| **Location basis** | $B = F_{\mathrm{loc}} - F_{\mathrm{hub}}$; $F_{\mathrm{loc}} = F_{\mathrm{hub}} + B$ | Build **location** curve from **hub** + basis; **basis** forwards/options |
| **Calendar basis** | $F(t,T_1) - F(t,T_2)$ | Spread trades; **storage**; contango/backwardation |
| **Spot–forward** | $S_t - F(t,T)$ | Convergence at expiry; **index** vs **physical** |
| **Basis risk** | Variance of $(P - I)$ or $\Delta B$ | **Hedge** imperfection when exposure price $\neq$ forward index |

**Nelson–Siegel (curve shape)**
$$
y(\tau) = \beta_0 + \beta_1\,\frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} + \beta_2\left( \frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} - e^{-\tau/\lambda} \right)
$$
($y$ = yield or log-price component, $\tau$ = tenor, $\lambda$ = decay; used for smooth curve fitting.)

**Black–Scholes (implied vol)**
$$
C = S_0 N(d_1) - K e^{-rT} N(d_2), \quad d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}.
$$
Solve for $\sigma_{\mathrm{impl}}$ from market $C_{\mathrm{mkt}}$.

**Black-76 (options on forwards) vs Black–Scholes–Merton**

**Black-76** (Black 1976) values options on a **forward/future** $F(t,T)$ with strike $K$ and expiry $T$:
$$
C = P(t,T)\bigl( F_0 N(d_1) - K N(d_2) \bigr), \quad d_1 = \frac{\ln(F_0/K) + \sigma^2 T/2}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}.
$$
Here $F_0 = F(t,T)$ and $P(t,T)$ is the discount factor to $T$. Put: $P = P(t,T)\bigl( K N(-d_2) - F_0 N(-d_1) \bigr)$.

**Why Black-76 is better for commodity portfolios than BSM**
- **Underlying is the forward.** Power and gas options are typically **on forwards or futures** (monthly, quarterly), not on spot. The quoted “underlying” is $F(t,T)$; there is no need to introduce spot $S_t$ and cost of carry.
- **No storage/carry.** BSM assumes the spot asset can be held and has a constant (or known) dividend yield/carry. **Power is non-storable**; gas is storable but with complex constraints. Black-76 bypasses this: the drift of $F$ under the risk-neutral measure is zero (no-arb), so the formula is clean and consistent with how forwards are traded.
- **Market convention.** Brokers and exchanges quote implied vol in **Black-76** (or Black in forward space). Using BSM would require converting spot to forward and modeling carry, which is redundant and error-prone.
- **Consistency with the curve.** The forward curve $F(t,T)$ is already built for risk and pricing; option valuation should use the same $F$ and $P(t,T)$. Black-76 does that directly; BSM would require a separate spot process and a link to the curve.

**When BSM is used:** Equities, FX (with interest-rate diff as “dividend”), or any asset where the **spot** is the liquid underlying and options are spot-referenced. For **commodity options on forwards/futures**, use **Black-76**.

**Why we can use forward/futures prices in Black-76 when there is no basis**

- **At expiry**, the **forward** equals the **settlement price**: $F(T,T) = S_T$ (the spot or the official settlement price at $T$). So the **option payoff** $(F_T - K)^+$ or $(K - F_T)^+$ is exactly **paid on** $S_T$. The **underlying** in Black-76 is therefore the **same** as the **price that settles the option** — no extra variable (spot vs forward) is involved.
- **No basis** means the **forward (or futures) price** we observe is the **same** as (a) the **price that settles the option**, and (b) the **price we are exposed to** (e.g. we have a position at that hub/location). So there is **no mismatch**: the option is written on $F$, and our **economic exposure** is also to $F$ (or to $S_T = F_T$ at expiry). Black-76 with **that** forward is then **correct**: we value an option on the **single** price $F(t,T)$ that will become $S_T$ at $T$, with no spread or second location.
- **When there is basis**, our **exposure** might be at **location** price $P_T$ while the **option** (or futures) settles on **hub** price $I_T = F_{\mathrm{hub}}(T,T)$. Then the option **payoff** is on $I_T$, but our **P&L** is driven by $P_T$ (or by $P_T - I_T$). Using **only** the hub forward $F_{\mathrm{hub}}(t,T)$ in Black-76 gives the **value of the option on the hub**, not the value of hedging our **location** exposure; we would need a **spread option** (on $P - I$) or a **location forward** $F_{\mathrm{loc}} = F_{\mathrm{hub}} + B$ to align underlying and exposure. So **with no basis** (one price, one exposure), forward/futures **is** the right input to Black-76; **with basis**, we must either use the **location** forward (hub + basis) if the option settles at the location, or model the **spread** if the option is on the hub but exposure is at the location.

**Assumptions in option pricing formulas (BSM / Black-76) and their issues**

| Assumption | Issue in practice |
|------------|-------------------|
| **Constant volatility** $\sigma$ | Volatility is **not constant**: it varies with strike (smile/skew), maturity (term structure), and time. Implied vol differs from historical vol; **stochastic vol** and **jumps** are needed to capture market prices and risk. |
| **Constant risk-free rate** $r$ | Interest rates have a **term structure** and are **stochastic**. For long-dated options or when discounting matters (e.g. margin), use a discount curve $P(t,T)$; Rho risk is non-trivial. Black-76 uses $P(t,T)$ but still assumes deterministic rates. |
| **Lognormal distribution** (returns ~ normal) | **Fat tails** and **skew** in empirical returns; **jumps** (e.g. power spikes, oil crashes) violate continuous paths. Lognormal understates OTM option value and tail risk; **jump-diffusion** or **stochastic vol** improve fit. |
| **Continuous trading** / no frictions | **Discrete rehedging** causes **gamma P&L** variance and path-dependence; **transaction costs** (bid-ask, commissions) and **funding/margin** reduce or shift “fair” value. **Short-sale** or **liquidity** constraints can break replication. |
| **No dividends** (or known continuous yield) | **Discrete dividends** and **uncertain timing/size** (e.g. equity dividends) break the simple formula; need **dividend-adjusted** spot or forward. For commodities, Black-76 uses the forward (no explicit dividend). |
| **Underlying follows GBM** (continuous path) | **Mean reversion** (e.g. power, gas) and **spikes** imply non-GBM dynamics. Forward may not be lognormal; **mean-reverting** or **jump** models are used for commodities. |
| **Perfect replication** / complete market | Incomplete markets (e.g. illiquid underlyings, gap risk) → **no unique** risk-neutral measure; **model risk** and **hedging error** matter. Pricing becomes “best estimate” plus reserve. |

**Summary:** The formulas are **tractable benchmarks** and **quoting conventions** (implied vol). In practice, **vol surface**, **stochastic rates**, **jumps**, **frictions**, and **incomplete markets** limit their accuracy; extensions (local vol, SABR, jump-diffusion, stochastic vol) address these at the cost of complexity and calibration.

**Asian options for power**

An **Asian option** has payoff based on the **average** of the underlying over a period (e.g. arithmetic average of daily or hourly prices), not the price at a single expiry. Call payoff: $(A - K)^+$ with $A = \frac{1}{n}\sum_{i=1}^n S_{t_i}$ (or time-weighted); put: $(K - A)^+$.

**Why companies use Asian options to value option contracts on power**
- **Settlement matches delivery.** Power is delivered over a **period** (e.g. a month or quarter). The economic exposure is to the **average price over that period**, not to one snapshot. Asian payoffs align with how volume is settled (MWh × average price over the delivery window).
- **Reduces manipulation and spike risk.** A **vanilla** option on a single fixing is sensitive to one moment—e.g. a spike on the last day. Asian payoffs smooth over many observations, so a single spike has limited impact and gaming the fixing is harder. Regulators and counterparties often prefer this for physical-linked contracts.
- **Lower volatility of the average.** The average of many (even correlated) prices has **lower variance** than a single price. So Asian options are typically **cheaper** than equivalent vanilla options and have **less sensitivity** to short-dated vol; they better reflect “average price” risk that load or generation actually faces.
- **Market practice.** Many power **PPAs**, **structured deals**, and **retail/wholesale hedges** reference average prices (e.g. monthly average of day-ahead or real-time prices). Valuing those embedded options as **Asian** (with appropriate averaging frequency and discounting) is standard; using vanilla would misprice and mis-hedge.

*Valuation:* No closed form for **arithmetic** Asian under Black–Scholes/Black-76; use **numerical methods** (e.g. Monte Carlo, PDE with an auxiliary state for running average) or **approximations** (e.g. moment matching to a lognormal, Lévy). **Geometric** average Asians have a closed form under lognormal assumptions.

**Put–call parity**
$$
C - P = S_0 - K e^{-rT} \quad \text{or} \quad C - P = e^{-rT}(F - K).
$$

**Butterfly / no-arbitrage in strike**
$$
\frac{\partial^2 C}{\partial K^2} = e^{-rT}\,\varphi(K) \geq 0 \quad \text{(risk-neutral density)}.
$$

**Volatility smile and surface: commodities and power**

**Definitions**
- **Volatility smile:** Implied volatility $\sigma_{\mathrm{impl}}(K)$ (from Black or Black-76) **varies with strike** $K$ for a given maturity. A **smile** is U-shaped (OTM puts and OTM calls both higher vol than ATM); a **skew** is a monotonic tilt (e.g. OTM puts &gt; ATM &gt; OTM calls).
- **Volatility surface:** $\sigma_{\mathrm{impl}}(K, T)$ — implied vol as a function of **strike** and **maturity**. The surface is built from liquid option quotes; interpolation and extrapolation must respect no-arbitrage (positive density, no calendar arbitrage).

**Why the smile exists (general)**
- **Fat tails / non-lognormal returns:** Real returns have more extreme moves than lognormal; OTM options are worth more than Black implies, so implied vol is higher away from ATM.
- **Demand:** Hedgers buy OTM puts (downside protection) or OTM calls (upside); flow pushes implied vol up for those strikes.
- **Leverage / correlation:** In equities, as price falls volatility often rises (leverage effect) → **negative skew**. In commodities, supply/demand and storage (or lack of it) drive skew direction.

**Commodity and power specifics**

1. **Direction of skew**
   - **Power:** Often **positive skew** (or **smile**) in **prices**: **OTM calls** (high strikes) can be expensive — upside **spikes** (heat waves, cold snaps, outages) are common, so the right tail is fat. **OTM puts** (low strikes) can also be elevated if participants hedge downside. The **underlying is often the forward** $F$; smile is in **($K/F$ or delta)** space.
   - **Gas:** Similar to power — **winter/summer spikes** → demand for OTM calls; sometimes **smile** or **positive skew** in price. Basis options can show different skew (e.g. location spread).
   - **Oil / refined products:** Often **negative skew** — downside crashes (demand shock, oversupply) are feared; OTM puts trade rich. Storage and contango/backwardation also affect forward vol and skew.

2. **Term structure of volatility**
   - **Short-dated vol** (e.g. prompt month, next week) is **high**: spot and near-term power/gas are very volatile (weather, outages, demand shocks). **Long-dated vol** (e.g. year-ahead, calendar strips) is **lower**: mean reversion and averaging over time reduce effective vol. So the vol surface often **slopes down in maturity** for commodities.
   - **Seasonality in vol:** In power and gas, **summer and winter** delivery months can have **higher implied vol** than shoulder months (demand and weather risk are higher in peak seasons). The surface $\sigma_{\mathrm{impl}}(K, T)$ thus has **seasonal bumps** by delivery month.

3. **Spikes and tails**
   - Power and gas prices can **spike** (positive jumps) and **mean-revert**. That implies **fat right tail** in the risk-neutral distribution. Pure Black-76 understates OTM calls; models with **jumps** (e.g. jump-diffusion, regime-switching) or **stochastic vol** are used to fit the smile and price exotics.
   - **Vol of the average** (for Asian options): The average price over a month has **lower volatility** than the spot. So when building a surface for **Asian-underlying** options, the effective vol is **reduced** (and term structure of “vol of average” vs “vol of spot” matters).

4. **Delta, sticky strike, and sticky delta**
   - **Delta** $\Delta = \partial V/\partial F$ (or $\partial V/\partial S$) is the sensitivity of option value to the **underlying** (forward or spot). Its **numerical value** depends on the **volatility** used (and on how we assume that vol **changes** when $F$ moves). So we must specify a **rule** for the vol surface when we bump $F$ — that rule is the **sticky convention**.
   - **Sticky strike:** Assume that **implied vol is constant in strike** $K$: $\sigma_{\mathrm{impl}}(K)$ does not change when $F$ moves. So when we bump $F$, we **revalue** the option using the **same** $\sigma_{\mathrm{impl}}(K)$ for that strike. Effect: as $F$ moves, the **moneyness** $K/F$ of the option changes, so the option effectively "slides along" the smile to a different point; the **delta** we get includes the effect of that (implicit) vol change and can be **unstable** or **odd** (e.g. delta can jump or have wrong sign in extreme skew). **Vega** (sensitivity to parallel vol shift) is also defined holding strikes fixed; vega by strike can be noisy when the smile is steep.
   - **Sticky delta:** Assume that **implied vol is constant in delta** (or in moneyness $K/F$): as $F$ moves, we **keep the same** $\sigma_{\mathrm{impl}}$ for the **same** moneyness. So the option’s **moneyness** is preserved, and the **delta** is **more stable** and typically closer to a Black-style delta (as if vol were constant). The **surface** is stored and interpolated in **(delta, maturity)** or **(K/F, maturity)**; when $F$ moves, we read off the same vol for the new $(K'/F', T)$. For **power/gas**, **sticky delta** is often used for **risk** and **revaluation** when the forward curve shifts, because price levels move a lot and keeping vol in moneyness avoids artificial delta/vega swings.
   - **Summary:** "Sticky" refers to **how we assume the vol surface moves** when the underlying moves — not to a property of delta itself. **Sticky strike** = vol fixed in $K$; **sticky delta** = vol fixed in delta/moneyness. The **same** option has **different** delta (and vega) under the two conventions; we choose one for reporting and hedging (often sticky delta in commodities).

**Do we have other sticky Greeks?**
   - **No.** The only standard **sticky conventions** are **sticky strike** and **sticky delta**. They are **assumptions about the vol surface**, not different Greeks. Once we choose one convention, we **compute** delta, gamma, vega (and vanna, volga) **under that assumption**: e.g. delta = bump $F$ and revalue with the surface updated according to sticky delta (or sticky strike). There is no separate "sticky gamma" or "sticky vega" — **gamma** is $\partial^2 V/\partial F^2$ (with the same sticky rule when we bump $F$ twice); **vega** is $\partial V/\partial \sigma$ (sensitivity to a shift in the surface, with the surface parameterization fixed in strike or in delta depending on convention). So **all** Greeks are affected by the **one** choice (sticky strike vs sticky delta); we do **not** have a family of "sticky Greeks," just two ways to **evolve** the surface that then determine the numbers we get for every Greek. (Sometimes **"sticky smile"** or **"sticky moneyness"** is used as a synonym for sticky delta.)

**Implied vol surface: key characteristics in energy (power, gas)**

- **Smile shape and moneyness**  
  Energy implied vol is typically quoted and modeled in **moneyness** ($K/F$ or delta), not absolute strike, because the **underlying** is the **forward** $F(t,T)$ and levels move a lot. **Power** and **gas** often show **positive skew in price** (OTM calls rich): upside spikes (heat, cold, outages) fatten the right tail, so $\sigma_{\mathrm{impl}}$ rises with $K/F$ for calls. OTM puts can also be elevated (downside hedging). **Smile** (U-shaped) or **skew** (monotonic) both appear; the **slope** can vary by hub and delivery month.

- **Term structure**  
  **Short-dated** (prompt month, balance-of-month) implied vol is **high**: near-term prices are very sensitive to weather, outages, and demand. **Long-dated** (quarter, calendar strip) implied vol is **lower**: mean reversion and averaging reduce effective volatility. The surface $\sigma_{\mathrm{impl}}(K,T)$ thus **declines with maturity** on average, with **seasonal variation**: **summer and winter** delivery months often have **higher** implied vol than **shoulder** months (April, October), so the surface has **bumps** by delivery period.

- **Illiquidity and proxy vol**  
  Liquid option markets exist mainly at **major hubs** (e.g. ERCOT North, PJM Western, Henry Hub for gas). **Other locations** or **paths** have **no or few** quoted options; implied vol is **transferred** from a liquid hub (e.g. scale by historical vol ratio, or assume same smile in moneyness). That introduces **proxy risk** and **mark uncertainty** for vega.

- **Location and basis vol**  
  **Basis options** (e.g. location A vs hub H) have a **different** smile than hub-only: the **spread** can be less volatile than either leg, or can have its own skew (e.g. congestion spikes). **Vol surface by location** is rarely observable; practitioners often use **hub vol** plus a **spread vol** assumption or historical basis vol.

- **Asian / average-price options**  
  Many power options settle on the **average** of daily prices over a month. The **vol of the average** is **lower** than the vol of the spot (averaging smooths). The implied vol surface for **Asian-underlying** options is therefore **flatter** in strike and **lower** in level than for spot/forward options; **term structure** must distinguish “vol of spot” vs “vol of average” by tenor.

- **Summary**  
  Energy implied vol surfaces are **strike- and maturity-dependent**, **seasonal**, **often positive-skewed in price**, **illiquid** away from major hubs (proxy vol), and **product-specific** (vanilla vs Asian, hub vs basis). Building and maintaining them requires **interpolation** in $(K/F, T)$, **arbitrage-free** constraints, and **conventions** (e.g. sticky delta) for risk and revaluation.

**Modeling the surface**
- **Parametric:** **SABR** $\mathrm{d}F = \sigma F^\beta \mathrm{d}W_1$, $\mathrm{d}\sigma = \nu\sigma\,\mathrm{d}W_2$, correlation $\rho$. Gives an **approximate implied vol** in (forward, strike, expiry); widely used in rates and commodities. Calibrate $\beta$, $\nu$, $\rho$ to market smile per tenor; then interpolate in time.
- **Local vol surface (Dupire / local volatility model)**  
  **Idea:** A **deterministic** function $\sigma_{\mathrm{loc}}(t, F)$ of **time** and **forward (or spot)** such that the one-factor diffusion $\mathrm{d}F_t = \sigma_{\mathrm{loc}}(t, F_t) F_t\,\mathrm{d}W_t$ **reproduces** the market **implied vol surface** (and hence all vanilla prices). **Dupire equation** (in strike and maturity) gives $\sigma_{\mathrm{loc}}^2(T,K)$ from the market **call prices** $C(K,T)$ (or equivalently from $\sigma_{\mathrm{impl}}(K,T)$). So the **local vol surface** is the **same dimensions** as the implied vol surface: $(t, F)$ or $(T, K)$; it is **calibrated** from the implied vol surface (or option prices) and is **unique** given a smooth, arbitrage-free market surface.
  **Use:** **Path-dependent** options (e.g. barriers, lookbacks, some Asians) can be priced by **PDE** or **Monte Carlo** using $\sigma_{\mathrm{loc}}(t,F)$; the model is **complete** (one Brownian motion), so replication is conceptually simple. **Vega** is interpreted as sensitivity to the **implied vol surface** (bump and reprice), not to a single vol parameter.
  **Limitations in energy:** (1) **Forward smile:** When the forward $F$ moves, the **future** implied vol surface in a local vol model is **determined** by $\sigma_{\mathrm{loc}}(t,F)$ at future $(t,F)$; that **future** smile often does **not** match how markets actually move (e.g. sticky delta). So **forward-start** or **cliquet** options can be mispriced. (2) **No vol-of-vol:** Local vol has **no** separate volatility process; vol is a **function** of $(t,F)$ only. So it cannot capture **vega risk** or **smile dynamics** that depend on vol-of-vol (e.g. vol spikes). (3) **Spikes and jumps:** Power and gas have **price spikes** and **jumps**; a **diffusion** with $\sigma_{\mathrm{loc}}(t,F)$ can try to fit the **current** smile by making $\sigma_{\mathrm{loc}}$ very high for certain $F$, but that can be **numerically unstable** and does not model **jump risk** explicitly. (4) **Stability:** Dupire local vol can be **noisy** or **extreme** when implied vol is flat or when extrapolating; **smoothing** and **bounds** are needed. In practice, **local vol** is used in energy for **path-dependent** pricing when a single, consistent surface is needed; for **smile dynamics** and **exotics** with forward vol sensitivity, **stochastic vol** or **SABR** are often preferred.
- **Stochastic vol + jumps:** For power/gas **spikes**, combine **stochastic volatility** (e.g. Heston, SABR) with **jumps** (e.g. Poisson jumps in price or vol) to capture both smile and term structure.

**No-arbitrage on the surface**
- **Butterfly:** $\partial^2 C / \partial K^2 \geq 0$ (positive density) at each maturity.
- **Calendar:** Call values (and implied vols) must be consistent across maturities (no calendar arbitrage). When interpolating in $(K, T)$, preserve these constraints (e.g. use arbitrage-free parameterizations or penalize violations in calibration).

**VaR and CVaR**
$$
\mathrm{VaR}_\alpha(L) = -\inf\bigl\{ x : P(L \leq x) \geq \alpha \bigr\} = -q_\alpha(L), \qquad
\mathrm{CVaR}_\alpha(L) = \mathbb{E}[-L \mid -L \geq \mathrm{VaR}_\alpha].
$$
Here $L$ = **loss** (positive = loss); so $-L$ = P&L (positive = profit). VaR is the **loss** at the $\alpha$-quantile of the loss distribution; CVaR is the **average loss** when the loss **exceeds** VaR. **ES (Expected Shortfall)** = CVaR (same object: expected loss in the tail).

**What 1-day 99% VaR and ES mean**

- **1-day 99% VaR = $X$ (e.g. \$500k)**  
  **Meaning:** Over the **next 1 day**, there is a **1%** chance that the **loss** will be **greater than $X$**. Equivalently: in **99%** of days, the loss will be **at most $X$**. So $X$ is the **threshold** such that **worse** outcomes happen only **1%** of the time (on average, about **2.5 days per year**).  
  **Interpretation:** “We expect that on **99 out of 100** days our loss will not exceed $X$; on **1 in 100** days it can exceed $X$.” VaR **does not** say how bad that 1% of days can be — only that they are **beyond** $X$.

- **1-day 99% ES (Expected Shortfall) = $Y$ (e.g. \$750k)**  
  **Meaning:** When we **are** in that **worst 1%** of days (i.e. when loss **exceeds** 99% VaR), the **average** loss in those days is **$Y$**. So ES answers: “**Conditional on** being in a tail event, what loss do we expect?”  
  **Interpretation:** “On the **worst 1%** of days, our **average** loss is $Y$.” ES is always **≥** VaR (it’s the average of losses **above** the VaR threshold). If the tail is **fat**, ES can be **much larger** than VaR.

**Summary**

| Number | Plain-English meaning |
|--------|------------------------|
| **1-day 99% VaR = \$X** | On **99%** of days, loss ≤ $X$; on **1%** of days, loss **&gt;** $X$. $X$ is the **cutoff** for the worst 1% of days. |
| **1-day 99% ES = \$Y** | **When** we’re in that worst 1%, the **average** loss is $Y$. $Y$ ≥ $X$; $Y$ captures **how bad** the tail is. |

**Greeks**
$$
\Delta = \frac{\partial V}{\partial S}, \qquad \Gamma = \frac{\partial^2 V}{\partial S^2}, \qquad \mathcal{V} = \frac{\partial V}{\partial \sigma}.
$$
Also: **Theta** $\Theta = \partial V/\partial t$ (time decay), **Rho** $\rho = \partial V/\partial r$ (rate sensitivity). **Second-order:** **Vanna** $\partial^2 V/(\partial S\,\partial\sigma)$, **Volga** (vomma) $\partial^2 V/\partial\sigma^2$.

**Signs of Greeks by position (vanilla European; long = buyer, short = seller)**

| Greek | Definition | Buyer of call | Seller of call | Buyer of put | Seller of put |
|-------|------------|---------------|----------------|--------------|---------------|
| **Δ** (Delta) | $\partial V/\partial S$ | + | − | − | + |
| **Γ** (Gamma) | $\partial^2 V/\partial S^2$ | + | − | + | − |
| **$\mathcal{V}$** (Vega) | $\partial V/\partial \sigma$ | + | − | + | − |
| **Θ** (Theta) | $\partial V/\partial t$ | − | + | − | + |
| **ρ** (Rho) | $\partial V/\partial r$ | + | − | − | + |
| **Vanna** | $\partial^2 V/(\partial S\,\partial\sigma)$ | ± | ∓ | ± | ∓ |
| **Volga** (Vomma) | $\partial^2 V/\partial\sigma^2$ | + | − | + | − |

- **Delta:** Call gains value when $S$ rises → buyer +; put gains when $S$ falls → buyer −. Seller has opposite sign.
- **Gamma:** Long option is convex in $S$ → Γ &gt; 0; short option → Γ &lt; 0.
- **Vega:** Long option benefits from higher vol → positive vega; short option → negative.
- **Theta:** Time decay usually hurts long option (Θ &lt; 0) and helps short (Θ &gt; 0); can be positive for deep ITM puts.
- **Rho:** Higher $r$ increases call value (discounting of strike) → call buyer +; decreases put value → put buyer −.
- **Vanna:** Sign depends on moneyness (e.g. ATM vs ITM/OTM); often small; “±” = position-dependent.
- **Volga:** Long options are convex in $\sigma$ (volga &gt; 0); short options have volga &lt; 0.

**Important risk metrics for an FTR / Power / Gas portfolio**

For a **mixed** portfolio of FTR, power, and gas, the following risk metrics are **especially important** — they drive limits, hedging, reporting, and capital.

| Metric | Why it matters for this portfolio |
|--------|-----------------------------------|
| **VaR (e.g. 1-day 99%)** | **Portfolio-level** tail risk in **one number**; used for **limits**, **capital**, and **backtesting**. FTR, power, and gas are **correlated** (e.g. gas → power → congestion); **portfolio VaR** captures diversification and concentration. Must be computed with **joint** factor moves (curves, spreads) and, for FTR, a **proxy** or **MTM-based** series if no liquid prices. |
| **ES (Expected Shortfall)** | **Conditional** tail risk: average loss when we exceed VaR. **Fat tails** (power/gas spikes, FTR realizations) make ES **more informative** than VaR for capital and stress; regulators often prefer ES. Same data and engine as VaR; report both. |
| **Delta (by bucket)** | **First-order** exposure to **curve** moves. **Power:** delta by hub (and location/basis) by tenor. **Gas:** delta by hub and **basis** by tenor. **FTR:** sensitivity to **path spread** curves (or proxy) by path and delivery. Drives **hedging** (forwards, futures) and **limit** design (e.g. delta limit per hub). **Net** delta by bucket shows where the book is long/short; **concentration** (e.g. too much delta in one tenor) is a risk. |
| **Gamma** | **Convexity** from options (power, gas, optional FTR). Large curve moves and **rehedging cost** depend on gamma. **Short** optionality → negative gamma → loss when markets move; **long** optionality → positive gamma but **vega** and **rehedging** matter. Aggregate gamma by book or by underlying for limit and hedging decisions. |
| **Vega** | **Vol** repricing risk. Options (power, gas, FTR options) have vega; **spikes** and **vol surface** moves can materially change MTM and **margin**. Vega by **tenor** (and optionally strike) for limit and hedging; **location/path** vol is often **proxy** → vega is model-dependent. |
| **Limit utilization** | **Current** exposure (VaR, delta, notional, vega) vs **approved limits**. Ensures the book stays within **risk appetite**; **breaches** trigger escalation or reduction. Limits are often set **by book** (FTR, power, gas) and **by factor** (e.g. power delta, gas delta, total VaR). |
| **Concentration** | **Where** risk is concentrated: top paths (FTR), top hubs/tenors (power, gas), single counterparty or venue. **Concentration** = illiquidity risk, **model** risk (one wrong curve affects a large share), and **event** risk (one outage, one path). Metrics: % of VaR or delta in top N paths/hubs; **Herfindahl** or similar. |
| **Stress and scenario P&L** | **What-if** loss under **named** scenarios: e.g. power +$50/MWh, gas winter spike, FTR path spread ±X, **correlation** breakdown. Complements VaR (which is **statistical**); stress answers "how bad if X happens?". Important for **liquidity** and **collateral** (margin calls in stress) and for **management** communication. |
| **Correlation / diversification** | **Correlation** between FTR, power, and gas (and across tenors/locations) drives **portfolio** VaR and **diversification benefit**. **Understated** correlation → understated risk; **overstated** → overstated risk. Report **correlation matrix** (or key pairs) and **standalone vs portfolio** VaR so diversification is visible. |
| **P&L attribution (curve, vol, theta, residual)** | **Explain** realized or hypothetical P&L by **factor** (curve, vol, theta, new trades, residual) and by **book**. Supports **backtesting** (did VaR/Greeks predict P&L?), **trading** review, and **model** validation. **Residual** that is large or systematic suggests missing risk factors or model error. |
| **MTM and mark uncertainty** | Many positions are **Level 2/3** (model + unobservable inputs). **Sensitivity** of MTM to **curve** and **vol** assumptions; **range** of marks under alternative methodologies. Not a single "risk number" but **input risk** — wrong curve or vol → wrong MTM and wrong Greeks. |

**Summary:** **VaR and ES** for tail risk and limits; **delta, gamma, vega** for factor exposure and hedging; **limit utilization** and **concentration** for control and liquidity; **stress** for named scenarios; **correlation/diversification** for portfolio effect; **P&L attribution** for explain and backtest; **mark uncertainty** for model/input risk. Together they give a complete picture of risk for this portfolio.

**Delta–gamma–vega hedging of an FTR / Power / Gas portfolio**

- **Delta hedging**  
  **Goal:** Neutralize first-order P&L to **curve moves** (forward prices). Portfolio value $V$ depends on **power** curves (e.g. hub by tenor), **gas** curves (hub + basis by location/tenor), and **FTR** value (driven by path spreads or proxy curves). **Delta** = sensitivity of $V$ to each risk factor (e.g. $\partial V/\partial F_{\mathrm{power},T}$, $\partial V/\partial F_{\mathrm{gas},T}$, or FTR MTM sensitivity to spread curves). **Hedge:** Take **offsetting** positions in **forwards or futures** (power, gas) and, where possible, in **liquid FTR/CRR** or proxy products so that **net delta** by factor (and ideally by tenor/bucket) is near zero. That way, small parallel or bucketed curve moves do not create large P&L. **Challenges:** FTR and many power/gas locations are **illiquid**; delta is often computed from **models** (curves + optionality); hedging may be done at a **hub** while exposure is at **location** → **basis risk** remains.

- **Gamma hedging**  
  **Goal:** Reduce **convexity** risk — i.e. P&L from **large** curve moves and from **rehedging** delta as the underlying moves. **Gamma** = $\partial^2 V/\partial S^2$ (or second-order sensitivity to curve factors). Options (power, gas, spread options, optional FTR) have **positive gamma** (long) or **negative gamma** (short); forwards have zero gamma. **Hedge:** (1) **Offset** option gamma by trading **other options** (e.g. sell options to reduce long gamma, or buy to cover short gamma); (2) **Rehedge delta** as the curve moves (dynamic hedging). In power/gas/FTR, **liquid option markets** are limited (often to major hubs and standard tenors); **gamma hedging** is therefore **partial** — we hedge what we can and accept **residual gamma** and **rehedging cost** (transaction costs, bid-ask, margin). **Cross-asset:** Portfolio may have power options, gas options, and FTR optionality; gamma is aggregated across underlyings and, if desired, hedged per market where liquidity exists.

- **Vega hedging**  
  **Goal:** Neutralize P&L from **volatility** moves (parallel or term/strike-specific). **Vega** = $\partial V/\partial \sigma$ (sensitivity to implied vol). Options (and optional FTR) have **vega**; forwards do not. **Hedge:** Use **liquid options** (e.g. at power hub, gas hub) to offset **net vega** by tenor (and, if relevant, by strike bucket). In practice, **vol surface** is quoted for a subset of underlyings; **location** or **path** options often have **no liquid vol** → vega is **model-implied** and hedged only at **proxy** hubs, leaving **basis vol** and **location vol** risk.

- **Why delta–gamma–vega is the practical set**  
  These three capture the **dominant** risks: **delta** = direction (curve), **gamma** = convexity (large moves, rehedging), **vega** = vol repricing. Theta is usually **monitored** (time decay) but not "hedged" with another instrument; rho is often **small** for commodity books relative to delta/vega, or hedged via **funding/rates** separately. For a **mixed** FTR/power/gas book, we typically report and hedge **delta by curve** (power, gas, FTR proxies), **gamma** where options are material and hedgeable, and **vega** by vol surface (hub or proxy).

**Why higher-order hedging (vanna, volga, etc.) is not reasonable**

- **Magnitude**  
  **Vanna** $\partial^2 V/(\partial S\,\partial\sigma)$ and **volga** $\partial^2 V/\partial\sigma^2$ are **second-order** in price and vol. For typical **daily or weekly** moves in curves and vol, their **contribution to P&L** is **much smaller** than delta, gamma, and vega. Hedging them would target **noise** rather than the main risk.

- **Liquidity and instruments**  
  There are **no liquid products** that directly and cheaply **target vanna or volga**. Doing so would require **combinations** of options (e.g. ratio spreads, vol swaps) that are **thin or absent** in power, gas, and FTR markets. Trading such combos would be **costly** (wide bid-ask, margin) and **operationally complex**, with limited benefit.

- **Estimation and model risk**  
  Higher-order Greeks are **sensitive** to the **vol surface** (smile, sticky-strike vs sticky-delta) and to **numerical** methods (finite-difference bumps, mixed derivatives). **Noise** and **model choice** can make vanna/volga **unreliable**; a "hedge" based on them might **increase** risk if the Greek is mis-estimated.

- **Transaction costs and rehedging**  
  **Delta–gamma–vega** rehedging is already **costly** (commissions, bid-ask, margin). Adding **vanna/volga** rehedging would **increase** trading and **operational** burden for **marginal** risk reduction. In **illiquid** commodity and FTR markets, the **cost** of hedging higher-order terms typically **exceeds** the benefit.

- **Conclusion**  
  **Delta, gamma, and vega** are the **reasonable** set for an FTR/power/gas portfolio: they capture **first-order** (curve) and the **main second-order** (convexity in price and vol) effects. **Higher-order** (vanna, volga, third-order in $S$ or $\sigma$) is **not reasonable** to hedge: small impact, no liquid instruments, high estimation/model risk, and cost outweigh benefit. Best practice is to **monitor** higher-order terms for **large** moves or **exotic** books, but **not** to run systematic hedges on them.

**Interest rate swap portfolio: main risks**

- **Rate risk (DV01 / PV01)**  
  Value of the portfolio changes when the discount/forward curve moves. **PV01** (or **DV01**) = dollar change in portfolio value for a **1 bp parallel upward shift** in the (relevant) rate curve:
  $$
  \mathrm{PV01} \approx \frac{\partial V}{\partial r}\,\times 0.0001.
  $$
  For a **par swap**, receive-fixed has **negative DV01** (rates up ⇒ fixed leg worth less ⇒ value down). Portfolio DV01 is the sum of individual swap DV01s; **key-rate DV01s** (sensitivity to a single tenor) or **bucket sensitivities** capture **curve** (non-parallel) risk.

- **Curve risk (steepening / flattening)**  
  Rates at different tenors don’t move in lockstep. **Steepening** (long end up more than short) or **flattening** (short end up more) can move P&L even when parallel DV01 is hedged. Hedge with **curve trades** (e.g. 2s10s) or key-rate hedges.

- **Basis risk**  
  Swap legs may reference different rates (e.g. 3m vs 6m, SOFR vs Fed Funds, or different tenors). **Basis** = spread between those rates; it can widen or tighten. Portfolio is exposed if not perfectly matched or if cross-currency (e.g. USD vs EUR curve).

- **Counterparty / credit (CVA)**  
  **Credit Valuation Adjustment**: value of the option to default. Bilateral: CVA (you to counterparty) and DVA (counterparty to you). Net exposure depends on MTM and collateral; risk increases with long-dated, uncollateralized books.

- **Optionality (vol, gamma)**  
  If the book contains **swaptions** or **Bermudan** structures, value is sensitive to **volatility** (vega) and **rate vol** (gamma when rates move). Risk: vol repricing or delta rehedging cost in moving markets.

**Par swap rate** (for reference): with payment dates $T_1,\ldots,T_n$ and day-count fractions $\tau_i$,
$$
R_{\mathrm{par}} = \frac{1 - P(t,T_n)}{\sum_{i=1}^n \tau_i P(t,T_i)}.
$$
Sensitivity of $R_{\mathrm{par}}$ to $P(t,T_i)$ drives swap DV01 by tenor.

**Marking to market: FTR, power, and gas portfolios**

**What MTM is**  
**Marking to market** = valuing positions at **current market or model-derived prices** (daily or at other reporting dates) for P&L, risk, collateral, and reporting. For FTR (Financial Transmission Rights / CRRs), power, and gas, marks depend on **forward curves**, **volatility** (for options), and **discount curves**; many products are **illiquid**, so marks are **model- or proxy-based** and subject to **methodology and input risk**.

---

**FTR (CRR) portfolio**

- **What is marked:** CRRs/FTRs are **path-based** rights that pay (or charge) the **spread between settlement point prices** (e.g. source–sink) in the **Day-Ahead Market** over the life of the right. Value = expected sum of (Sink SPP − Source SPP) × MW × hours (for options, max with zero).
- **Typical mark inputs:** (1) **Forward curve of settlement point price spreads** (or nodal/scenario prices) for each path and delivery period; (2) **discount curve**; (3) for optionality (e.g. spread options), **volatility** of the spread or of the underlying prices.
- **Issues:**
  - **Illiquidity:** Most paths have **no liquid secondary market**. Marks rely on **modeled** or **proxy** spread curves (e.g. from a power flow / congestion model, or from historical DAM spreads). Different models or assumptions → **mark variance** and **disputes** with counterparties or auditors.
  - **Path and product granularity:** CRRs are **path × MW × TOU × month**. Curves may exist for major hubs but not for every path; **mapping** (path → proxy hub spread) and **aggregation** (many small positions) introduce **basis and approximation error**.
  - **Optionality:** PTP **Options** (pay when spread &gt; 0) are **optional**; their value is sensitive to **vol** and **distribution** of spreads. Using a simple forward expectation understates optionality; **option model** (e.g. spread option, Black-76 on spread) and **vol input** are needed, and are often **unobservable** (no traded options on many paths).
  - **Settlement timing and realizations:** CRRs settle on **realized** DAM prices. Mark is **pre-settlement** (expected value); **realized** P&L can differ due to **volume** (forced outages, derates) or **price** (actual DAM vs curve). **Reconciliation** and **reserves** for model vs realization matter.
  - **Concentration and correlation:** Large positions on a few paths or nodes increase **mark uncertainty** (moving the market, or model error on that path). **Correlation** between paths is hard to observe; wrong correlation affects **portfolio-level** risk and MTM variance.

---

**Power portfolio**

- **What is marked:** Forwards (physical or financial), **options** (vanilla, Asian, spread), and sometimes **structured** or **embedded** options (e.g. in PPAs). Each needs a **forward curve** (by hub/delivery) and, for options, a **vol surface** and **discount curve**.
- **Issues:**
  - **Curve availability and consistency:** Curves may be **broker-based**, **internal**, or **mixed**. **Off-peak**, **long-dated**, or **non-standard hubs** can have **thin or no liquidity** → **proxy curves** (e.g. spread to a liquid hub) or **extrapolation**; choice of proxy and methodology drives mark.
  - **Vol surface:** Options need **implied vol** by strike and maturity. Many power options are **Asian** or **path-dependent**; **vol of average** vs **vol of spot**, **term structure**, and **smile** are often **unobservable** (few quoted options). Marks depend on **assumed** or **historical** vol → **vega risk** and **mark uncertainty**.
  - **Basis and location:** **Basis** between hubs (e.g. ERCOT North vs South) and **day-ahead vs real-time** spreads are not always liquid. Marks for **basis positions** or **location-specific** deals rely on **modeled** or **stale** basis curves.
  - **Settlement reference:** Power can settle on **DAM** or **RT** prices; **peak vs off-peak**; **monthly average** vs **single day**. **Wrong settlement specification** in the mark (e.g. using DAM curve for an RT-settled option) causes **systematic mis-mark**.

---

**Gas portfolio**

- **What is marked:** Forwards (by location, e.g. hub or pipe), **basis** (location spread), **options** (e.g. swing, storage-related), and **spread** options (e.g. heat rate in power–gas). Inputs: **gas forward curves** by location, **basis curves**, **vol** (for options), **discount curve**.
- **Issues:**
  - **Location and basis:** **Pipeline and flow** constraints create **location-specific** prices. Many locations are **illiquid**; marks use **basis to a liquid hub** (e.g. Henry Hub). **Basis volatility** and **structural changes** (new pipes, demand shifts) make basis curves **uncertain** and **mark-sensitive**.
  - **Storage and optionality:** **Storage** and **swing** contracts embed **optionality** (flexibility when to inject/withdraw). Valuation needs **storage model** (e.g. dynamic programming, least-squares MC) and **forward curve + vol**. **Model choice** and **calibration** (e.g. to historical spreads) are **subjective** → **mark dispersion**.
  - **Vol by location:** Option marks need **vol** by location and tenor. **Liquid option markets** exist mainly at major hubs; other locations use **proxy vol** (e.g. scaled from hub vol) → **vega and correlation** uncertainty.
  - **Seasonality and prompt:** **Winter/summer** peaks and **prompt** gas can be very volatile. **Curve and vol** for prompt and peak months are more **observable** but still **move fast**; **stale data** or **lagged** curve updates cause **mark lag** and **P&L noise**.

---

**Cross-cutting issues**

| Issue | FTR | Power | Gas |
|-------|-----|-------|-----|
| **Illiquidity** | Most paths untraded; model/proxy marks | Thin options; long-dated/off-peak | Basis and non-hub locations |
| **Curve and vol inputs** | Spread curve, path→proxy, vol for options | Hub curve, Asian vol, smile | Hub + basis curves, location vol |
| **Methodology** | Forward expectation vs option model; path aggregation | Asian vs vanilla; settlement spec | Storage/swing model; basis model |
| **Data and ops** | Congestion model output; DAM history | Broker vs internal curves; timing | Basis quotes; pipeline data |
| **Fair-value hierarchy** | Most marks **Level 2/3** (model + unobservable inputs) | Mix of **Level 1** (liquid) and **2/3** | Similar; hub liquid, rest Level 2/3 |

**Summary:** MTM for FTR, power, and gas is **input- and model-dependent**. Key risks: **illiquidity** (proxy curves and vol), **methodology choice** (option model, Asian, storage), **settlement specification** (DAM vs RT, average vs single fix), and **reconciliation** of mark vs realized settlement. Robust **documentation**, **independent price testing**, and **reserves** for model/realization uncertainty are standard practice.

**Managing collateral: FTR, power, and gas portfolios**

**What collateral management is**  
Collateral (margin) is **cash or eligible securities** posted to **counterparties**, **exchanges**, or **clearing houses** to cover **current exposure** (variation margin / VM) and **potential future exposure** (initial margin / IM). **Managing** collateral means: (1) having **enough** eligible collateral to meet calls; (2) **optimizing** what to post (cost, liquidity, haircuts); (3) **forecasting** and **stressing** future calls; (4) handling **disputes** (MTM disagreements); (5) **funding** and **liquidity** so calls can be met on time.

---

**FTR (CRR) portfolio**

- **Who holds collateral:** In ERCOT, **CRR Account Holders** are subject to **credit limits** and collateral/credit support. ERCOT (and similarly other RTOs for FTRs) may require **collateral or credit facilities** to participate in the **CRR auction** and to support **ongoing CRR exposure**. ERCOT’s **Credit Management System** uses **CRR ownership** and **exposure measures** (e.g. based on CRR value and/or congestion exposure) to compute **available credit** and **margin calls**.
- **What drives calls:** (1) **Auction:** Buying CRRs in the auction consumes **available credit** (bid size × clearing price or similar). (2) **Mark-to-market:** As CRR values or congestion exposure change, **exposure** is re-estimated; if it exceeds the **collateral/credit** already committed, ERCOT may call for more. (3) **Concentration / stress:** Large path or nodal exposure can increase **potential exposure** and thus required collateral.
- **Managing it:** (1) **Pre-auction:** Ensure **credit headroom** for intended bids; understand how ERCOT calculates **available credit** and **credit limit**. (2) **Post-auction:** Monitor **CRR MTM** and **exposure**; maintain **liquidity** (cash or committed lines) to meet **intraday or next-day** calls. (3) **Disputes:** If marks or exposure methodology differ from internal estimates, **reconcile** with ERCOT and escalate; wrong marks can drive **unnecessary** or **insufficient** collateral. (4) **Concentration:** Diversify paths or size positions so that **single-path** moves don’t trigger outsized calls; stress-test **extreme congestion** scenarios.

---

**Power portfolio**

- **Where collateral is posted:** (1) **OTC (bilateral):** Under **ISDA** + **CSA** (Credit Support Annex); **variation margin** (VM) = MTM of the portfolio (often daily); **initial margin** (IM) for **regulated** entities under **UMR** (Uncleared Margin Rules). (2) **Cleared:** Exchange or CCP (e.g. CME, ICE) requires **initial margin** and **variation margin**; margin is typically **daily** and can be **intraday** in stress.
- **What drives calls:** (1) **MTM move:** Power prices (and vol) can **spike**; **VM** increases when the portfolio is **out of the money** (you owe). (2) **IM:** CCPs and CSAs often use **VaR** or **stress-based** models; **vol** and **correlation** spikes increase **IM**. (3) **New trades:** Adding **optionality** or **long-dated** exposure can increase IM.
- **Managing it:** (1) **Liquidity:** Keep **cash or highly liquid** securities to meet **same-day or next-day** VM/IM calls; power **spikes** can cause **large** moves. (2) **Haircuts and eligibility:** CSA/CCP define **eligible collateral** (e.g. cash, govies) and **haircuts**; optimize **which** assets to post (cost vs liquidity). (3) **Netting:** **Netting sets** (e.g. one CSA with a counterparty) reduce **gross** exposure and thus VM/IM; understand **netting** and **rehypothecation** terms. (4) **Disputes:** **MTM disputes** delay or reduce VM exchange; have **resolution** process and **fallback** (e.g. third-party marks, arbitration). (5) **Forecasting:** **Stress** power curves and vol to estimate **peak** VM/IM; ensure **funding** or **credit lines** for tail scenarios.

---

**Gas portfolio**

- **Where collateral is posted:** Same structure as power: **OTC** via **ISDA/CSA** (VM + IM under UMR if applicable); **cleared** gas (e.g. NYMEX/ICE) with **exchange margin**. **Storage** or **swing** deals may have **bilateral** margin terms.
- **What drives calls:** (1) **Price and basis moves:** **Winter/summer** spikes and **basis** moves change **MTM** and thus **VM**. (2) **Vol:** Option-heavy or **storage** books have **vega**; **vol** spikes increase **IM** and **VM**. (3) **Concentration:** Large **location** or **tenor** exposure can increase **potential exposure** and IM.
- **Managing it:** (1) **Seasonal liquidity:** **Peak** seasons (winter) can see **large** margin calls; ensure **liquidity** ahead of **heating season**. (2) **Basis and location:** **Basis** positions can be **illiquid**; **marks** may be disputed; collateral may be called on **model** marks — **document** methodology and agree **dispute** process. (3) **Storage/swing:** Complex **optionality** → **model-dependent** MTM and **potential** for **disputes**; keep **conservative** liquidity buffer. (4) **Rehypothecation and segregation:** Understand whether posted collateral can be **reused** by the counterparty; **segregation** (e.g. for cleared) affects **liquidity** and **default** recovery.

---

**Cross-cutting: collateral management issues**

| Issue | FTR | Power | Gas |
|-------|-----|-------|-----|
| **Volatility of exposure** | CRR value and congestion exposure can move fast | Price and vol spikes → large VM/IM | Winter/summer spikes; basis moves |
| **Liquidity timing** | Calls can be intraday or next-day (ERCOT) | Same-day / next-day VM; intraday in stress | Similar; seasonal peaks |
| **MTM disputes** | ERCOT vs internal marks; methodology | CSA/CCP marks vs internal; curves/vol | Basis and storage marks |
| **Eligibility and cost** | Cash / credit lines; ERCOT-specific rules | Cash, govies; haircuts; UMR IM | Same; exchange vs bilateral |
| **Netting and consolidation** | Single ERCOT credit account; path diversification | Netting set per counterparty; cleared vs OTC | Same; cleared vs OTC |

**Summary:** Collateral management for FTR, power, and gas requires **liquidity** to meet **volatile** VM/IM calls, **alignment** with counterparties (and ERCOT) on **marks and methodology**, **stress testing** for peak exposure, and clear **dispute** and **funding** procedures. FTR is **ERCOT-centric** (credit limit, CRR exposure); power and gas add **CSA/CCP** terms, **UMR** IM where applicable, and **seasonal** and **vol** drivers.

**Capturing correlation in a portfolio of FTR, power, and gas**

**Why correlation matters**  
Portfolio **risk** (VaR, CVaR, P&L variance), **margin** (IM often depends on correlation), **diversification** (negative or low correlation reduces risk), and **hedging** (e.g. gas vs power) all depend on **joint** moves across FTR, power, and gas. **Understated** correlation → **understated** portfolio risk and **overstated** diversification; **overstated** correlation → **overstated** risk. Capturing correlation is also needed for **capital** and **stress** tests.

**Where correlation shows up**
- **FTR–Power:** CRR value is driven by **congestion** (spread between settlement points), which is driven by **load**, **generation**, and **flows** — the same drivers as **power prices**. High demand (e.g. heat wave) → high power prices and often **higher congestion** on import paths → **positive** correlation between power price and many FTR payoffs. Path-specific (export paths can be negatively correlated with power price).
- **Power–Gas:** **Spark spread** (power price minus gas cost) links the two; **gas** is a **marginal fuel** in many regions. **Positive** correlation between power and gas prices (both rise in demand spikes). **Seasonal** (winter: gas heating + power; summer: power cooling, gas for peakers).
- **FTR–Gas:** **Indirect**: gas sets marginal cost in many nodes; gas price affects **LMP** and thus **congestion** and **FTR** value. Can be **positive** when gas-driven nodes set price and congestion.
- **Within asset class:** **Power** across hubs (e.g. ERCOT North vs South); **gas** across locations (hub vs basis); **FTR** across paths (same node, different paths). These **within** correlations matter for **granular** risk and **margin**.

**Ways to capture correlation**

1. **Historical correlation (returns)**  
   Define **return** or **P&L** series for each book or risk factor (e.g. daily P&L of FTR book, power book, gas book; or daily log-returns of key forward prices / congestion proxies). Estimate **sample correlation matrix** $\widehat{\rho}_{ij}$ (and volatilities) from a rolling or expanding window.  
   **Issues:** (1) **FTR** has no liquid price series — use **proxy** (e.g. daily change in mark-to-market of CRR portfolio, or congestion component of a representative LMP spread). (2) **Non-stationarity**: correlation can **change** by season or regime (e.g. summer vs winter). (3) **Horizon alignment**: FTR settles **monthly** (DAM daily, then aggregated); power/gas can be **daily** or **monthly** — decide whether to use **daily** P&L or **monthly** and ensure series are **aligned**. (4) **Tail dependence**: linear correlation understates **joint extremes** (e.g. power and gas spiking together).

2. **Factor model**  
   Assume a few **common factors** drive all three: e.g. **gas price**, **power demand** (or temperature), **congestion index** (or load). Each position or sub-portfolio has **factor loadings** (betas); correlation comes from **factor covariance** + **residual** correlation.  
   **Advantages:** Fewer parameters; **interpretable**; can use **fundamental** or **macro** data. **Implementation:** Regress P&L or returns on factor returns; estimate **factor** cov matrix; $\Sigma = B \Sigma_f B' + \Sigma_{\varepsilon}$ (loadings $B$, factor cov $\Sigma_f$, residual $\Sigma_{\varepsilon}$). **Issues:** Choice of factors; residuals may still be correlated; factors may be **non-stationary**.

3. **Copulas**  
   Model **marginals** (e.g. power P&L distribution, gas P&L distribution, FTR P&L distribution) separately and **dependence** via a **copula** (e.g. Gaussian, t, or empirical). **Tail dependence** (e.g. t-copula) allows **joint spikes** (power and gas both extreme) to be more likely than under Gaussian.  
   **Use:** **Stress** tests and **CVaR** where **tail** correlation matters. **Issues:** More complex; need enough data to fit marginals and copula; **high-dimensional** (many positions) is harder.

4. **Scenario-based / stress correlation**  
   Define **joint scenarios** (e.g. “hot summer”, “cold winter”, “gas supply shock”) and assign **moves** to FTR, power, and gas in each scenario. **Correlation** is implicit in the **joint** scenario; no single correlation matrix.  
   **Use:** **Stress** testing, **liquidity** and **margin** in stress. **Issues:** Scenarios are **subjective**; may miss **regime** or **path** dependence.

5. **Implied correlation (when available)**  
   If **spread** or **basket** options trade (e.g. spark spread options), **implied correlation** between power and gas can be backed out from **spread vol** vs **single-asset** vols: $\sigma_{\mathrm{spread}}^2 \approx \sigma_P^2 + \sigma_G^2 - 2\rho\,\sigma_P\sigma_G$. **Rare** for FTR; more common for power–gas in some markets.

**Implementation choices**

| Choice | Options | Comment |
|--------|---------|--------|
| **Series for FTR** | CRR portfolio P&L change; proxy spread (e.g. key path LMP spread); simulated path value | No liquid FTR price; proxy must be consistent with how CRR is marked |
| **Frequency** | Daily (DAM) vs monthly (settlement) | Align with risk horizon and margin frequency |
| **Power / gas** | Hub-level returns; portfolio P&L; principal components | Portfolio P&L is most relevant for portfolio risk; hub-level for factor model |
| **Estimation window** | Rolling (e.g. 1–2 years) vs expanding; regime-dependent | Balance stability vs responsiveness; seasonality |
| **Positive definiteness** | Shrinkage (e.g. toward diagonal or constant); eigenvalue clamp | Sample matrix may not be PD or stable; shrink or regularize |

**Use in risk**  
Feed **correlation** (and volatilities) into: (1) **Portfolio VaR/CVaR** (e.g. variance–covariance or Monte Carlo with correlated shocks). (2) **Initial margin** approximation (if IM is VaR-based, correlation reduces or increases IM). (3) **Stress**: apply **stressed** correlation (e.g. higher in crisis) or **scenario** moves. (4) **Capital** and **diversification** reporting. **Backtest** by comparing **predicted** portfolio vol vs **realized** P&L vol; adjust correlation (or model) if systematically off.

**Summary:** Correlation in a combined FTR–power–gas book can be captured by **historical** returns (with a **FTR proxy**), **factor** models (common drivers), **copulas** (tail dependence), or **scenarios**. Key challenges: **no liquid FTR series** (use MTM or congestion proxy), **alignment** of horizons and definitions, **non-stationarity** and **seasonality**, and **tail** dependence. Use in **portfolio VaR**, **margin**, and **stress**; validate with **backtests** and **sensitivity** analysis.

**Steps to build a VaR platform (Historical and Monte Carlo) for FTR, Power, and Gas**

**1. Define scope and outputs**
- **Portfolio:** Positions in FTR (path × MW × TOU × month), power (forwards, options by hub/delivery), gas (forwards, options, basis by location).
- **Outputs:** **Historical VaR** and **Monte Carlo VaR** (and optionally **CVaR**) at chosen **confidence** (e.g. 95%, 99%) and **horizon** (e.g. 1-day, 10-day). **Decomposition** by book (FTR / power / gas) or by risk factor. **Backtesting** and **reporting** (daily run, audit trail).

**2. Data layer**
- **Positions:** Static data — FTR path/MW/TOU/dates, power contracts (hub, delivery, MW, optionality), gas contracts (location, delivery, optionality). **Refresh** when trades are booked.
- **Market data (current):**  
  - **FTR:** Forward curves (or proxy) for **settlement-point spreads** (or nodal prices) by path/delivery; **discount curve**; for options, **vol** (if modeled).  
  - **Power:** **Forward curves** by hub and delivery; **vol surface** (strike × tenor) for options; **discount curve**.  
  - **Gas:** **Forward curves** by location; **basis** curves; **vol** for options; **discount curve**.
- **Historical market data:** **Time series** of the same risk factors (or their returns) over a **lookback** (e.g. 1–2 years daily, or monthly if horizon is monthly). For **FTR**, use **proxy** series (e.g. historical CRR portfolio MTM, or congestion/LMP spread series) if no liquid FTR prices.
- **Correlation / covariance:** For **MC VaR**, need **covariance matrix** (or correlation + vols) of **risk-factor returns**; estimate from same historical window (or factor model). Ensure **positive definiteness** (shrinkage, eigenvalue floor).

**3. Valuation and P&L**
- **Valuation engine:**  
  - **FTR:** Mark = expected sum of (Sink − Source) × MW × hours over remaining delivery, discounted; use **spread curves** (or nodal model). For optionality, spread option or simplified option model.  
  - **Power:** Forwards = curve × volume; options = Black-76 or Asian (with curve + vol).  
  - **Gas:** Same idea; storage/swing = dedicated model (e.g. LSMC, dynamic programming).
- **P&L attribution:** For each **historical date** $t$, compute **portfolio value** $V_t$ using **curves/prices as of $t$** (or **scenario** for MC). **1-day P&L** = $V_t - V_{t-1}$ (or **hypothetical** P&L from today’s portfolio revalued at $t$ and $t-1$). For **MC**, simulate **forward** returns and revalue; P&L = $V_{\mathrm{sim}} - V_0$.

**4. Historical VaR — steps**
1. **Build historical P&L series:** For each date $s$ in the lookback window, take **today’s portfolio** (fixed) and value it at **market data as of $s$** and **as of $s-1$**. Compute **1-day P&L** = $V_s - V_{s-1}$ (or use **overlapping** periods if horizon &gt; 1 day). Store the **ordered** P&L series (e.g. 500 daily P&Ls).
2. **Apply horizon (if needed):** For **10-day VaR**, either (a) use **overlapping 10-day** historical P&L (non-overlapping reduces sample size), or (b) scale **1-day VaR** by $\sqrt{10}$ (assumes i.i.d.; often conservative for mean-reverting commodities).
3. **VaR and CVaR:** **Historical VaR** at confidence $\alpha$ (e.g. 95%) = **$\alpha$-quantile** of the P&L distribution (e.g. 5th percentile of 500 P&Ls). **CVaR** = average of P&Ls **worse** than VaR.
4. **Decomposition:** Compute **marginal** or **component** VaR by book (FTR / power / gas) by re-running VaR with only that book, or by **historical** P&L attribution by sub-portfolio.

**Square-root-of-t scaling: when it works and when it doesn’t**

To get **$h$-day VaR** (e.g. 10-day) from **1-day VaR**, a common shortcut is to scale by $\sqrt{h}$:
$$
\mathrm{VaR}_{\alpha}(h\text{-day}) \approx \sqrt{h} \cdot \mathrm{VaR}_{\alpha}(1\text{-day}).
$$
This comes from **parametric (variance–covariance) VaR** under **i.i.d.** assumptions: if 1-day P&L has volatility $\sigma_1$, then $h$-day P&L has volatility $\sigma_h = \sqrt{h}\,\sigma_1$ (variance adds over independent days), and for **elliptic** distributions (e.g. normal) the $\alpha$-quantile scales with $\sigma$, so $\mathrm{VaR}_\alpha(h) = \sqrt{h}\,\mathrm{VaR}_\alpha(1)$.

**When $\sqrt{t}$ is reasonable**
- **I.i.d. returns:** Daily P&L (or returns) are **independent** and **identically distributed**.
- **No autocorrelation:** No mean reversion or momentum in daily moves.
- **Constant volatility:** No time-varying vol (no GARCH, no regime shifts).
- **Parametric VaR:** For **historical** VaR, $\sqrt{t}$ is **not** implied by the method; it is an **extra** assumption if you scale 1-day historical VaR by $\sqrt{h}$ instead of using **overlapping $h$-day** historical P&L.

**When $\sqrt{t}$ fails (the “issue”)**

1. **Mean reversion (commodities, FTR)**  
   Power and gas (and many FTR spreads) are **mean-reverting**. Over **several days**, variance grows **less** than linearly in $h$ (reversion pulls prices back). So **true** $h$-day vol $< \sqrt{h} \times \sigma_1$ ⇒ **scaling 1-day VaR by $\sqrt{h}$ overstates** $h$-day VaR. For **capital** this can be **conservative**; for **risk limit** or **allocation** it can be **too punitive**.

2. **Autocorrelation**  
   **Positive** autocorrelation (momentum) ⇒ variance of $h$-day return **>** $h \times \sigma_1^2$ ⇒ **$\sqrt{h}$ understates** $h$-day VaR. **Negative** (mean reversion) ⇒ **$\sqrt{h}$ overstates** $h$-day VaR.

3. **Time-varying volatility**  
   If vol is **stochastic** (e.g. GARCH) or **regime-dependent**, the **distribution** of $h$-day P&L is **not** the same as “sum of $h$ i.i.d. 1-day” ⇒ $\sqrt{h}$ scaling is **invalid**. Need **multi-day** simulation or **overlapping $h$-day** historical P&L.

4. **Fat tails**  
   For **non-normal** tails, the **quantile** does **not** scale linearly with $\sigma$. **Extreme** percentiles (e.g. 99%) can scale **faster** than $\sqrt{h}$ (tail gets fatter over horizon). **Historical** VaR scaled by $\sqrt{h}$ ignores this; **MC** with correct fat-tailed marginals does not use $\sqrt{h}$ for multi-day.

5. **Liquidity / close-out**  
   If the **holding period** is $h$ days because positions **cannot** be closed in 1 day, the **economic** risk is $h$-day. But **realized** P&L variance over $h$ days may still **not** scale as $h$ (e.g. mean reversion). So $\sqrt{h}$ is a **convention** (e.g. Basel 10-day) not necessarily the **correct** multi-day risk.

**What to do in practice**
- **Preferred:** Compute **$h$-day VaR directly**: (a) **Historical:** use **overlapping** (or non-overlapping) **$h$-day** P&L series and take the $\alpha$-quantile; (b) **MC:** simulate **$h$-day** returns (e.g. $h$ steps of 1-day dynamics, or a joint $h$-day distribution) and revalue; then take quantile. **No** $\sqrt{h}$ scaling.
- **If scaling is used:** Document that it assumes **i.i.d.** and **constant vol**; for **mean-reverting** books (power, gas, FTR), note that $\sqrt{h}$ is likely **conservative**. For **regulatory** 10-day VaR, scaling 1-day by $\sqrt{10}$ is often **allowed** but **conservative** for commodities.
- **Formula (parametric, i.i.d.):** If 1-day P&L $\sim N(\mu_1, \sigma_1^2)$ and i.i.d., then $h$-day P&L $\sim N(h\mu_1, h\sigma_1^2)$, and
$$
\mathrm{VaR}_\alpha(h) = -h\mu_1 + \Phi^{-1}(1-\alpha)\,\sqrt{h}\,\sigma_1 = \sqrt{h}\,\Bigl( \mathrm{VaR}_\alpha(1) + (\sqrt{h}-1)\mu_1 \Bigr) \approx \sqrt{h}\,\mathrm{VaR}_\alpha(1) \quad \text{if } |\mu_1| \ll \sigma_1.
$$

**Better approaches than $\sqrt{t}$ for multi-day VaR**

1. **Historical VaR: use $h$-day P&L directly**  
   Build a series of **$h$-day** P&L (e.g. 10-day): for each date $s$, compute $V_s - V_{s-h}$ (or non-overlapping blocks). Take the **$\alpha$-quantile** of this **$h$-day** P&L distribution. **No scaling**; the distribution naturally reflects **mean reversion**, **autocorrelation**, and **vol clustering** in the data.  
   - **Overlapping** $h$-day windows: more observations, but **serial correlation** in the series (same days appear in many windows).  
   - **Non-overlapping** $h$-day blocks: independent blocks, but **fewer** points (e.g. 252/10 ≈ 25 per year).  
   - **Preferred** when you have enough history and want **model-free** $h$-day risk.

2. **Monte Carlo: simulate over $h$ days**  
   For each scenario, **simulate** the **full $h$-day path** (e.g. $h$ steps of your 1-day dynamics — OU, jump-diffusion, etc.). **Revalue** the portfolio at the **end** of day $h$; P&L = $V_h - V_0$. Take the **$\alpha$-quantile** of the **simulated $h$-day** P&L.  
   - **Mean reversion** and **path dependence** are captured by the **multi-step** simulation.  
   - **Preferred** when you have a **parametric** model and want **consistent** multi-day and 1-day VaR.

3. **Parametric (variance–covariance) with $h$-day variance**  
   If you **insist** on a parametric formula, **estimate** the **$h$-day** variance **directly** (e.g. from overlapping $h$-day returns, or from the model: for OU, $\mathrm{Var}(X_h \mid X_0)$ is known and **not** $h \times \sigma_1^2$). Then $\mathrm{VaR}_\alpha(h) = -h\mu_h + \Phi^{-1}(1-\alpha)\,\sigma_h$, where $\sigma_h$ = **true** $h$-day vol (e.g. from the mean-reverting process), **not** $\sqrt{h}\,\sigma_1$.  
   - **Preferred** when you have a **closed-form** for multi-day variance (e.g. OU, two-factor).

4. **Block bootstrap (historical)**  
   Resample **blocks** of **$h$ consecutive days** (with replacement) to preserve **within-block** dependence; compute P&L over each block; take quantile of the **bootstrap** distribution of $h$-day P&L.  
   - **Preferred** when you want to keep **historical** joint behaviour without a parametric model.

**Recommendation for FTR, power, gas:** Use **$h$-day historical P&L** (overlapping or non-overlapping) for **historical** VaR, and **$h$-day path simulation** for **MC** VaR. Avoid $\sqrt{t}$ unless you explicitly assume i.i.d. and document it; for mean-reverting commodities, $\sqrt{t}$ is conservative and can be replaced by the **direct** $h$-day methods above.

**5. Monte Carlo VaR — steps**
1. **Define risk factors:** Choose a set of **risk factors** whose moves drive P&L: e.g. **power** hub curve (key tenors), **gas** hub curve (key tenors), **FTR** proxy (e.g. key path spreads or CRR sub-portfolio MTM). Optionally **vol** factors if vega is material.
2. **Distribution of factor returns:** Fit **marginal** distributions (e.g. empirical, or normal/t with volatility from history) and **joint** dependence (e.g. **correlation matrix** from historical returns; or **copula** for tail dependence). For **FTR**, use **proxy** returns (e.g. change in CRR MTM or congestion index).
3. **Simulate:** Draw $N$ (e.g. 10k–50k) **scenarios** of **1-day (or horizon)** factor returns. For each scenario, **apply** the shocks to **current** curves/prices to get **simulated** market data.
4. **Revalue:** For each scenario, **revalue** the **full** portfolio (FTR + power + gas) at the **simulated** market data. **Simulated P&L** = $V_{\mathrm{sim}} - V_0$.
5. **VaR and CVaR:** **MC VaR** at confidence $\alpha$ = **$\alpha$-quantile** of the **simulated** P&L distribution. **CVaR** = average of simulated P&Ls below VaR.
6. **Variance reduction (optional):** Use **antithetic** variates or **importance sampling** to reduce MC error for the tail.

**6. Platform and operations**
- **Scheduling:** Run **daily** (e.g. after market data and positions are updated). **Inputs:** positions, current curves/vols, historical series, correlation/covariance.
- **Backtesting:** Compare **predicted** VaR to **realized** 1-day P&L: count **exceptions** (realized loss &gt; VaR). **Traffic light** (e.g. green/amber/red) or **p-value** for exception rate vs expected. **Tune** lookback or model if backtest fails.
- **Reporting:** Output **VaR** (and CVaR) for **total** and **by book**; **contribution** by risk factor or position bucket; **history** of VaR and P&L for trend. **Audit:** store **inputs** (curves, positions, params) and **method** (Historical vs MC) for reproducibility.
- **Governance:** **Document** assumptions (FTR proxy, horizon scaling, correlation estimation). **Review** and **approve** model changes. **Limit** usage (e.g. no VaR for illiquid or model-heavy books without adjustment).

**Backtesting when the portfolio is FTR, power, and gas**

**Goal:** Check whether **1-day VaR** (and, if used, **ES**) is **well calibrated** — i.e. whether **realized** 1-day P&L exceeds VaR with **frequency** consistent with the confidence level (e.g. 99% VaR ⇒ about 1% of days should see loss &gt; VaR). Backtesting is done on the **combined** portfolio and optionally **by book** (FTR, power, gas) to see which book drives exceptions.

**Setup**

- **Realized 1-day P&L:** For each date $t$, the **actual** change in portfolio value from $t-1$ to $t$: $\mathrm{P\&L}_t^{\mathrm{real}} = V_t - V_{t-1}$, where $V_t$ is **mark-to-market** (or **trading P&L**) as of $t$. For a **mixed** book, $V_t$ includes **FTR** (mark from spread curves), **power** (curves + vol), **gas** (curves + vol). So $\mathrm{P\&L}_t^{\mathrm{real}}$ mixes **curve/vol moves**, **new trades**, and **model/mark changes**.
- **Hypothetical 1-day P&L (clean backtest):** To remove **new trades** and **position changes**, use **hypothetical** P&L: fix the **portfolio as of $t-1$** and revalue it at **market data as of $t$** and **as of $t-1$**. Then $\mathrm{P\&L}_t^{\mathrm{hyp}} = V(\text{portfolio}_{t-1}; \text{market}_t) - V(\text{portfolio}_{t-1}; \text{market}_{t-1})$. This is the P&L that **would have occurred** with no trading; it aligns with what **VaR** is predicting (risk of **existing** positions). **Procedure:** Many shops backtest on **hypothetical** P&L for model validation and on **realized** P&L for limit and capital (realized includes new business).
- **VaR as of $t-1$:** 1-day VaR computed **at $t-1$** for the portfolio as of $t-1$, at confidence $\alpha$ (e.g. 99%). So we compare $\mathrm{P\&L}_t$ (realized or hypothetical) to $\mathrm{VaR}_{t-1}$.

**Metrics and formulas**

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Exception (breach)** | $\mathbb{1}\bigl( \mathrm{P\&L}_t < -\mathrm{VaR}_{t-1} \bigr)$ | 1 if **loss** exceeds VaR (i.e. loss &gt; VaR in magnitude), 0 otherwise. |
| **Exception count** | $N = \sum_{t=1}^{T} \mathbb{1}( \mathrm{P\&L}_t < -\mathrm{VaR}_{t-1} )$ | Number of days (over $T$ days) when loss exceeded VaR. |
| **Exception rate** | $\hat{p} = N / T$ | Empirical **frequency** of exceptions. For **99% VaR**, **expected** rate = 1%; for **95% VaR**, expected = 5%. |
| **Binomial test (p-value)** | Under the null that true exception rate = $p_0$ (e.g. 0.01 for 99% VaR), $N \sim \mathrm{Binomial}(T, p_0)$. **p-value** = $P(N \geq n \mid p_0)$ (for too many exceptions) or $P(N \leq n \mid p_0)$ (for too few). **Two-sided:** reject if $\hat{p}$ is far from $p_0$. | **Too many** exceptions ⇒ VaR **understates** risk (model or vol too low). **Too few** ⇒ VaR **overstates** risk (conservative). |
| **Traffic light (Basel-style)** | **Green:** $\hat{p}$ within acceptable range (e.g. $N$ in [expected − buffer, expected + buffer]). **Amber:** $N$ above green. **Red:** $N$ significantly above expected (e.g. &gt; 4 for 99% VaR over 250 days). Exact thresholds depend on regime (e.g. Basel has green/amber/red zones for 99% VaR). | **Regulatory** or **internal** escalation; red may require capital add-on or model change. |
| **Magnitude of exceedances** | For days where $\mathrm{P\&L}_t < -\mathrm{VaR}_{t-1}$, compute **average shortfall**: $\frac{1}{N}\sum_{t \in \text{exceptions}} \bigl( -\mathrm{P\&L}_t - \mathrm{VaR}_{t-1} \bigr)$. | **How much** loss exceeded VaR on exception days; informs **ES** calibration. |
| **Conditional coverage** | Test whether exceptions are **clustered** (e.g. many in a short period) vs **independent**. **Christoffersen** test: independence of exception today vs exception yesterday. | **Clustering** ⇒ model misses **vol regime** or **correlation** in stress. |

**FTR / power / gas specifics**

- **FTR P&L:** **Realized** P&L for FTR includes **mark** change (spread curves, model) and **no** liquid market — so **marks** can jump when curves are rebuilt or when **realized** DAM settles (discrete monthly settlement). **Hypothetical** P&L (portfolio fixed, curves at $t$ vs $t-1$) is **cleaner** for backtest; **realized** is noisier but reflects true P&L. Document whether FTR is **included** in backtest and whether you use **hypothetical** or **realized**.
- **Power and gas:** **Curve** and **vol** updates are daily (or intraday); **realized** P&L is usually **available** and aligned with VaR horizon. **New trades** can create **large** 1-day P&L that has nothing to do with **market** move — so **hypothetical** backtest is often used for **model** validation; **realized** for **limit** and **capital** (with the understanding that exceptions can be due to new business).
- **By book:** Compute **exception count** and **rate** for **total** portfolio and, if desired, **by book** (FTR only, power only, gas only) using **book-level** P&L and **book-level** VaR (or **incremental** VaR for that book). Identifies which book **drives** backtest failures (e.g. FTR proxy too smooth, power vol too low).
- **Correlation:** Portfolio VaR assumes **joint** distribution of FTR, power, gas. If **correlation** is **understated**, **portfolio** VaR can be **too low** in stress (all three lose together) ⇒ **too many** exceptions. **Backtest** does not **directly** estimate correlation; it tests the **combined** effect. If backtest fails, **review** correlation and **marginal** vols (power, gas, FTR proxy).

**Procedure**

1. **Build series:** For a **rolling** window (e.g. last 250 or 500 days), for each $t$: $\mathrm{P\&L}_t$ (realized or hypothetical), $\mathrm{VaR}_{t-1}$ (and optionally $\mathrm{ES}_{t-1}$).
2. **Count exceptions:** $N = \#\{ t : \mathrm{P\&L}_t < -\mathrm{VaR}_{t-1} \}$; $\hat{p} = N/T$.
3. **Test:** Binomial p-value vs $p_0$ (e.g. 0.01); traffic light; magnitude of exceedances; conditional coverage if desired.
4. **Report:** Exception rate, p-value, traffic light, and (if applicable) by-book breakdown. **Trend:** track $\hat{p}$ over **rolling** windows to see if calibration has improved or worsened.
5. **Act:** If **too many** exceptions → review **vol** (power, gas, FTR proxy), **correlation**, **horizon**, or **method** (Historical vs MC). If **too few** → model may be **conservative** (acceptable for limits); or reduce conservatism to free capital.

**Summary**

Backtesting for an FTR/power/gas portfolio: **(1)** Define P&L (realized vs hypothetical) and VaR as of prior day. **(2)** Exception = loss &gt; VaR; exception rate $\hat{p} = N/T$. **(3)** Test $\hat{p}$ vs expected (binomial, traffic light); check magnitude and clustering. **(4)** FTR marks are noisy — prefer hypothetical for model validation; power/gas can use either. **(5)** By-book backtest and correlation review help diagnose failures.

**Summary**
| Step | Historical VaR | Monte Carlo VaR |
|------|----------------|-----------------|
| **Data** | Historical market data + positions | Same + correlation/covariance (or copula) |
| **P&L** | Historical P&L of today’s portfolio | Simulated P&L from simulated factor returns |
| **VaR** | Quantile of historical P&L | Quantile of simulated P&L |
| **Pros** | No distribution assumption; captures realized joint moves | Can impose structure (vol, correlation, tails); scalable to many scenarios |
| **Cons** | Past may not repeat; FTR proxy; limited tail observations | Model risk (distributions, correlation); FTR proxy; compute cost |

**Intramonth VaR for a power book (DAM, RT, DART)**

**What intramonth VaR is**  
**Intramonth** = risk over a horizon **within** the current (or next) month — e.g. **1-day** (tomorrow), **remaining days in month**, or **rolling 7-day**. It applies to power positions that **settle daily** in the **Day-Ahead Market (DAM)** and/or **Real-Time (RT)** market: fixed or variable volume per day, **DART** (Day-Ahead–Real-Time spread) exposure, or any book that has **daily** cash flows and **forward** exposure to DAM/RT prices over the rest of the month.

**Exposure types**

| Type | Description | P&L driver |
|------|-------------|------------|
| **DAM-only** | Volume committed/sold in day-ahead; settles at DAM price | DAM price × volume, per day |
| **RT-only** | Imbalance, deployment, or RT-only volume; settles at RT price | RT price × volume, per day |
| **DART (spread)** | Exposure to **RT − DAM** (e.g. sold DAM, buy RT to cover; or financial DART product) | **(RT − DAM)** × volume, per day (or per hour, then summed) |

**Intramonth P&L structure**  
- **Realized:** Days already **settled** (known cash flows).  
- **Forward:** **Remaining** days in the month: P&L = sum over future days of (price × volume) or (spread × volume). **Intramonth VaR** = risk of the **forward** part (or of **tomorrow’s** P&L, or of **cumulative** P&L over remaining days).  
- **Variable horizon:** “Remaining days” = $h$ depends on **today’s date** (e.g. 15 days left in month). VaR can be **1-day** (next day only), **remaining $h$-day** (to month-end), or **fixed** (e.g. always next 7 days).

**Data needed**  
- **Historical** **DAM** and **RT** prices (and, if hourly, **DART** = RT − DAM by hour) by **hub/zone**, for a long enough history (e.g. 1–2 years).  
- **Volume** profile: fixed MW per day, or **load/volume** shape (to weight prices).  
- For **DART**: historical **spread** (RT − DAM) by hour or daily average; **correlation** between DAM and RT (spread vol is typically **larger** than either alone if they are imperfectly correlated).

**VaR approaches**

1. **Historical intramonth VaR**  
   - **1-day VaR:** For each historical date $s$, compute **next-day** P&L: e.g. (DAM$_{s+1}$ − DAM$_s$) × volume for DAM-only; (Spread$_{s+1}$ − Spread$_s$) × volume for DART; or full revaluation. Take **$\alpha$-quantile** of this **1-day** P&L series.  
   - **Remaining-$h$-day VaR:** For each $s$, compute **cumulative** P&L over days $s+1$ to $s+h$ (same structure: DAM, RT, or DART × volume per day). Take **$\alpha$-quantile** of this **$h$-day** P&L. Use **overlapping** windows if $h$ is fixed (e.g. always 7 days) or **calendar-aligned** windows (e.g. “remaining days in month” so $h$ varies).  
   - **No $\sqrt{t}$:** Use the **actual** 1-day or $h$-day P&L distribution; do **not** scale 1-day VaR by $\sqrt{h}$ (DAM/RT are mean-reverting and volatile).

2. **Monte Carlo intramonth VaR**  
   - **Risk factors:** **DAM** and **RT** (or **DART** spread) by day (or by hour, then aggregate). Model **daily** (or hourly) returns or levels; **correlation** between DAM and RT (or joint distribution of spread).  
   - **Simulate:** For each scenario, simulate **path** of DAM and RT (or DART) over **remaining $h$ days** (or 1 day). Apply **volume** (fixed or stochastic) and compute **P&L** = $\sum_{\text{days}} \text{price}_d \times \text{vol}_d$ or spread × vol.  
   - **VaR:** $\alpha$-quantile of **simulated** intramonth P&L.  
   - **Models:** **OU** or **jump-diffusion** for DAM and RT (or for DART spread); **correlated** shocks (Cholesky). **Hourly** then **sum** if you need hourly granularity (e.g. peak vs off-peak DART).

3. **Parametric (variance–covariance)**  
   If P&L is **linear** in price (or spread) and you assume **normal** returns: estimate **1-day** or **$h$-day** **volatility** of P&L (from historical 1-day or $h$-day P&L, or from model: e.g. OU variance for $h$-day). Then $\mathrm{VaR}_\alpha = -\mu + \Phi^{-1}(1-\alpha)\,\sigma$. Use **true** $h$-day $\sigma$ (e.g. from mean-reverting process), **not** $\sqrt{h}\,\sigma_1$.

**DART-specific**  
- **Spread** RT − DAM is **mean-reverting** (RT and DAM co-move but RT is more volatile); **spread** can **spike** (e.g. congestion, outages).  
- **Volume:** Often **hedged** volume (e.g. load); DART P&L = (RT − DAM) × volume. **Intramonth** = risk of **cumulative** (RT − DAM) × vol over remaining days.  
- **Correlation:** If DAM and RT are **positively correlated**, spread vol $< \sqrt{\sigma_{\mathrm{RT}}^2 + \sigma_{\mathrm{DAM}}^2}$; if **negative** or **low**, spread vol can be **large**. Estimate **joint** (DAM, RT) or **spread** vol from history.  
- **Peak vs off-peak:** DART can be **block-specific** (peak hours vs off-peak); use **hourly** or **block** DAM/RT (or spread) and **weight** by volume in each block.

**Operational choices**  
- **Horizon:** Report **1-day** VaR (next day) and/or **remaining-days** VaR (to month-end). **Remaining-days** changes **daily** (e.g. 20 days left → 19 → … → 1).  
- **Realized vs forward:** VaR can be **forward-only** (remaining days) or **full month** (realized + forward); usually **forward** for risk limit.  
- **Backtesting:** Compare **1-day** VaR to **realized next-day** P&L; or **remaining-$h$-day** VaR to **realized** P&L over the corresponding $h$ days.

**Summary**  
Intramonth VaR for a power book (DAM, RT, DART) = VaR of **daily** or **remaining-days** P&L driven by **DAM**, **RT**, or **DART spread** × volume. Use **historical** (1-day or $h$-day P&L series, no $\sqrt{t}$) or **MC** (simulate DAM/RT or spread over remaining days; mean-reverting/jump models). **Data:** historical DAM/RT (and spread) by hub; **volume** profile. **DART:** model **spread** or **joint** (DAM, RT); capture **correlation** and **block** (peak/off-peak) if needed.

**Stochastic price processes for simulating FTR, power, and gas**

Common choices for **simulating** prices (or risk factors) for VaR, pricing, and stress: **mean-reverting** processes (power and gas are not GBM long-term), **jump-diffusion** for **spikes**, and **correlated** multi-factor processes for **FTR spreads** (difference of nodal or spread prices). Below are standard formulations with formulas.

---

**1. Ornstein–Uhlenbeck (OU) — mean-reverting price or log-price**

Good for **spot** or **spread** that reverts to a long-term level (e.g. power/gas spot, or congestion spread).

$$
\mathrm{d}X_t = \kappa(\theta - X_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t
$$

- $X_t$ = price, log-price, or spread; $\kappa > 0$ = mean-reversion speed; $\theta$ = long-term mean; $\sigma$ = volatility; $W_t$ = Brownian motion.
- **Conditional distribution:** $X_T \mid X_t$ is Gaussian with
$$
\mathbb{E}[X_T \mid X_t] = \theta + (X_t - \theta)e^{-\kappa(T-t)}, \qquad \mathrm{Var}(X_T \mid X_t) = \frac{\sigma^2}{2\kappa}\bigl(1 - e^{-2\kappa(T-t)}\bigr).
$$
- **Euler discretization** (for simulation, step $\Delta t$):
$$
X_{t+\Delta t} = X_t + \kappa(\theta - X_t)\Delta t + \sigma\sqrt{\Delta t}\,Z, \quad Z \sim N(0,1).
$$
- **Seasonality:** Set $\theta = \theta(t)$ (e.g. sinusoidal or monthly dummies) so the mean reverts to a time-dependent level.

---

**2. Geometric mean reversion (Schwartz one-factor) — positive price**

Keeps price **positive** and adds **mean reversion in log-price** (used for commodities).

$$
\mathrm{d}S_t = \kappa(\mu - \ln S_t)S_t\,\mathrm{d}t + \sigma S_t\,\mathrm{d}W_t
$$

Equivalently, for $Y_t = \ln S_t$:
$$
\mathrm{d}Y_t = \kappa(\mu - Y_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t.
$$

- **Closed-form:** $Y_T \mid Y_t$ is Gaussian (same as OU); $S_T = e^{Y_T}$ is **lognormal**.
- **Long-term mean** of $S$ is $e^{\mu + \sigma^2/(4\kappa)}$ (for the stationary distribution).
- **Euler in log:** $Y_{t+\Delta t} = Y_t + \kappa(\mu - Y_t)\Delta t + \sigma\sqrt{\Delta t}\,Z$; then $S_{t+\Delta t} = e^{Y_{t+\Delta t}}$.

---

**3. Jump-diffusion (Merton-style) — spikes**

Add **Poisson jumps** to capture **power/gas spikes**.

$$
\mathrm{d}X_t = \kappa(\theta - X_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t + J_t\,\mathrm{d}N_t
$$

- $N_t$ = Poisson process with intensity $\lambda$; $J_t$ = jump size (e.g. $J \sim N(\mu_J, \sigma_J^2)$ for each jump). Jumps are **independent** of $W$.
- **Simulation:** Over $\Delta t$, (1) draw number of jumps $n \sim \mathrm{Poisson}(\lambda\Delta t)$; (2) sum $n$ i.i.d. jumps $J$; (3) add OU step: $X_{t+\Delta t} = X_t + \kappa(\theta - X_t)\Delta t + \sigma\sqrt{\Delta t}\,Z + \sum_{i=1}^n J_i$.
- **Exponential jumps:** $J > 0$ with $J \sim \mathrm{Exp}(\eta)$ for **upward** spikes (e.g. power).

---

**4. Two-factor (Schwartz–Smith type) — short-term deviation + long-term level**

**Long-term** equilibrium $\xi_t$ and **short-term** deviation $x_t$; spot $S_t = e^{\xi_t + x_t}$.

$$
\mathrm{d}x_t = -\kappa x_t\,\mathrm{d}t + \sigma_x\,\mathrm{d}W_x, \qquad \mathrm{d}\xi_t = \mu_\xi\,\mathrm{d}t + \sigma_\xi\,\mathrm{d}W_\xi
$$

- $\mathrm{Corr}(W_x, W_\xi) = \rho$. **Forward** $F(t,T)$ has a closed form (affine in $x_t$, $\xi_t$). Useful for **curve** simulation and **option** pricing.
- **Simulation:** Euler (or exact for OU $x_t$) for $x$ and $\xi$; then $S_t = \exp(\xi_t + x_t)$.

---

**5. FTR / spread — two correlated OUs (source and sink)**

FTR payoff depends on **spread** = Sink price − Source price (or congestion component). Model **two** mean-reverting prices (or log-prices) with **correlation**; spread = difference.

**Nodal (or hub) prices:**
$$
\mathrm{d}P^{\mathrm{sink}}_t = \kappa_1(\theta_1 - P^{\mathrm{sink}}_t)\,\mathrm{d}t + \sigma_1\,\mathrm{d}W_1, \qquad \mathrm{d}P^{\mathrm{source}}_t = \kappa_2(\theta_2 - P^{\mathrm{source}}_t)\,\mathrm{d}t + \sigma_2\,\mathrm{d}W_2
$$

with $\mathrm{d}W_1\,\mathrm{d}W_2 = \rho\,\mathrm{d}t$. **Spread** $S_t = P^{\mathrm{sink}}_t - P^{\mathrm{source}}_t$ is **mean-reverting** if $\kappa_1 = \kappa_2$ and has a Gaussian distribution; otherwise it is a **sum of two OUs** (still Gaussian, with a known covariance structure).

**Single spread process (reduced form):** Alternatively model the **spread** itself as one OU (or jump-diffusion):
$$
\mathrm{d}S_t = \kappa_S(\theta_S - S_t)\,\mathrm{d}t + \sigma_S\,\mathrm{d}W_S + J_S\,\mathrm{d}N_t.
$$
Calibrate $\kappa_S$, $\theta_S$, $\sigma_S$ (and jump params) to **historical spread** or **CRR MTM** changes.

---

**6. Multi-asset (power, gas, FTR) — correlated shocks**

Simulate **power** $P_t$, **gas** $G_t$, and **FTR** proxy (e.g. spread $S_t$ or CRR subportfolio value $V_t$) with **correlation**:

- **Discretization** (Euler): for each factor $X^i_t$ (e.g. $P$, $G$, $S$),
$$
X^i_{t+\Delta t} = X^i_t + \mu^i(X^i_t)\,\Delta t + \sigma^i(X^i_t)\sqrt{\Delta t}\,\sum_j L_{ij} Z_j, \quad Z_j \sim N(0,1) \text{ i.i.d.}
$$
where $L$ is the **Cholesky** factor of the **correlation matrix** $\rho$ ($LL' = \rho$). Drift $\mu^i$ can be mean-reverting (e.g. OU), and $\sigma^i$ can be constant or level-dependent.
- **Example (three OUs):** $P$, $G$, $S$ each follow OU with their own $\kappa$, $\theta$, $\sigma$; correlate the Brownian motions via $L$ so that $\mathrm{Corr}(\Delta P, \Delta G)$, $\mathrm{Corr}(\Delta P, \Delta S)$, $\mathrm{Corr}(\Delta G, \Delta S)$ match estimates.

---

**7. Forward curve simulation (for multi-tenor VaR)**

To simulate **forward curves** (e.g. power hub by month), either:

- **Factor model:** $F(t,T) = F(0,T) \exp\bigl(\sum_k \beta_k(T) X^k_t\bigr)$ where $X^k_t$ are **few** factors (e.g. level, slope) following OU or jump-diffusion; simulate $X^k$, then rebuild $F(t,T)$.
- **Multi-OU:** One OU per **key tenor** (e.g. prompt, 3 months, 12 months) with **correlation**; interpolate other tenors. Ensures **no-arbitrage** in expectation if drift is chosen consistently (e.g. risk-neutral).

**Summary**

| Process | Use case | Main formula |
|---------|----------|--------------|
| **OU** | Spot, spread, mean-reverting factor | $\mathrm{d}X = \kappa(\theta - X)\,\mathrm{d}t + \sigma\,\mathrm{d}W$ |
| **Schwartz 1-factor** | Positive price, log mean-reversion | $\mathrm{d}S = \kappa(\mu - \ln S)S\,\mathrm{d}t + \sigma S\,\mathrm{d}W$ |
| **Jump-diffusion** | Power/gas spikes | OU + $J\,\mathrm{d}N_t$ (Poisson jumps) |
| **Two-factor** | Curve, short/long term | $x_t$ OU; $\xi_t$ drift + vol; $S = e^{x+\xi}$ |
| **FTR spread** | CRR / congestion | Two OUs (source, sink) or one OU/jump for spread |
| **Multi-asset** | Portfolio (P, G, FTR) | Correlated OUs (Cholesky of $\rho$) |

**Use and selection of copulas for risk analysis (FTR, power, gas portfolio)**

**Why copulas**  
**Copulas** separate **marginal distributions** (how each risk factor or P&L is distributed) from **dependence** (how they move together). For a combined FTR–power–gas book, marginals are often **non-Gaussian** (fat tails, skew, spikes); **linear correlation** is not enough to describe **tail dependence** (e.g. power and gas spiking together, or all three books losing together). A copula models **joint extremes** explicitly and fits well into **VaR/CVaR**, **stress**, and **scenario** generation.

**Sklar’s theorem and definition**

If $F(x_1,\ldots,x_d)$ is the joint CDF of $(X_1,\ldots,X_d)$ with marginals $F_1,\ldots,F_d$, there exists a **copula** $C$ such that
$$
F(x_1,\ldots,x_d) = C\bigl(F_1(x_1),\ldots,F_d(x_d)\bigr).
$$
$C$ is a CDF on $[0,1]^d$ with uniform marginals. So: **marginals** $F_i$ describe each variable; **copula** $C$ describes dependence. For simulation: (1) fit or assume marginals; (2) fit copula to **transformed** data $U_i = F_i(X_i)$ (or rank-based); (3) simulate $(U_1,\ldots,U_d)$ from $C$; (4) transform back: $X_i = F_i^{-1}(U_i)$.

**Tail dependence**

- **Upper tail dependence** $\lambda_U$: probability that one variable is extreme **high** given the other is extreme high (limit of conditional probability). Relevant when **power and gas spike together**.
- **Lower tail dependence** $\lambda_L$: joint **lows** (e.g. **joint losses** in FTR, power, gas). Relevant for **portfolio VaR** and **CVaR**.

**Common copulas (formulas and tail dependence)**

| Copula | Formula / generator | Upper $\lambda_U$ | Lower $\lambda_L$ | Use when |
|--------|---------------------|-------------------|-------------------|----------|
| **Gaussian** | $C(\mathbf{u}) = \Phi_\rho(\Phi^{-1}(u_1),\ldots,\Phi^{-1}(u_d))$ | 0 | 0 | Baseline; no tail dependence |
| **t** | $C(\mathbf{u}) = t_{\rho,\nu}(t_\nu^{-1}(u_1),\ldots,t_\nu^{-1}(u_d))$ | $>0$ if $\rho>0$ | $>0$ if $\rho>0$ | Symmetric tails; joint spikes and crashes |
| **Clayton** | $C(u_1,u_2) = \bigl(\max(u_1^{-\theta}+u_2^{-\theta}-1,0)\bigr)^{-1/\theta}$, $\theta>0$ | 0 | $2^{-1/\theta}$ | **Lower** tail (joint losses) |
| **Gumbel** | $C(u_1,u_2) = \exp\bigl(-\bigl((-\ln u_1)^\theta+(-\ln u_2)^\theta\bigr)^{1/\theta}\bigr)$, $\theta\geq 1$ | $2-2^{1/\theta}$ | 0 | **Upper** tail (joint spikes) |
| **Frank** | $C(u_1,u_2) = -\frac{1}{\theta}\ln\bigl(1+\frac{(e^{-\theta u_1}-1)(e^{-\theta u_2}-1)}{e^{-\theta}-1}\bigr)$ | 0 | 0 | Symmetric; no tail dependence |

- **Gaussian:** $\Phi$ = standard normal CDF; $\Phi_\rho$ = multivariate normal with correlation $\rho$. Simple; **no** tail dependence.
- **t-copula:** $t_{\rho,\nu}$ = multivariate t with correlation $\rho$ and d.f. $\nu$. **Symmetric** upper and lower tail dependence; $\nu \downarrow$ → fatter tails and stronger tail dependence.
- **Clayton:** **Lower** tail only; good for **joint losses** (FTR, power, gas all bad).
- **Gumbel:** **Upper** tail only; good for **joint spikes** (power and gas up).
- **Frank:** Symmetric; stronger dependence in the middle than Gaussian for same correlation; no tail dependence.

**Selection for FTR, power, gas**

1. **Tail behavior:**  
   - **Power–gas:** Often **upper** tail dependence (both spike on demand/weather). → **Gumbel** or **t** (t also allows lower tail).  
   - **Portfolio losses (VaR/CVaR):** **Lower** tail (all books lose). → **Clayton** or **t**.  
   - **Uncertain or both tails:** **t-copula** (symmetric; one parameter $\nu$ controls tail strength).

2. **Fit and parsimony:**  
   - Estimate **rank correlation** (Kendall’s $\tau$ or Spearman’s $\rho_S$) from data; map to copula parameter(s).  
   - **Goodness-of-fit:** Compare empirical joint tail (e.g. tail dependence) to copula-implied; or use **AIC/BIC** if fitting by MLE.  
   - **Dimension:** For $d=3$ (FTR, power, gas), **pair-copula** (vine) or **one** parametric copula (e.g. t with $3\times 3$ correlation + $\nu$) keeps parameters manageable.

3. **Stability and robustness:**  
   - **t** and **Gaussian** are **easy to simulate** (Cholesky + normal or t draws). **Clayton/Gumbel** have closed-form conditional CDFs for **conditional sampling**.  
   - **Empirical copula** (nonparametric) uses data directly but is **noisy in tails**; consider **smoothed** or **parametric** for risk.

**Use in the risk platform**

1. **Data:** Historical **P&L** or **returns** for FTR proxy, power book, gas book (same frequency and horizon as VaR).
2. **Marginals:** Fit **empirical** CDF or **parametric** (e.g. normal, t, skewed-t) to each marginal; transform to $U_i = \widehat{F}_i(X_i)$.
3. **Copula:** Fit **copula** to $(U_1,U_2,U_3)$ (e.g. **t** with $\rho$ and $\nu$ by MLE or Kendall’s $\tau$).
4. **Simulation:** Simulate $N$ draws $(U_1^{(j)},\ldots,U_d^{(j)})$ from the fitted copula; set $X_i^{(j)} = \widehat{F}_i^{-1}(U_i^{(j)})$; compute **portfolio P&L** (or revalue) per scenario.
5. **VaR/CVaR:** Take **quantile** and **tail average** of simulated portfolio P&L.
6. **Stress:** Use **stressed** copula (e.g. higher $\nu^{-1}$ or higher $\theta$ in Clayton) to increase tail dependence in stress tests.

**Summary**

| Step | Action |
|------|--------|
| **Why copula** | Separate marginals from dependence; capture **tail** dependence (joint spikes/losses). |
| **Choose** | **t**: symmetric tails, flexible. **Gumbel**: upper tail (power–gas spikes). **Clayton**: lower tail (joint losses). **Gaussian**: baseline, no tails. |
| **Fit** | Marginals first (empirical or parametric); then copula on $U_i = F_i(X_i)$; MLE or rank correlation. |
| **Simulate** | Draw from copula → invert marginals → get correlated P&L/returns → VaR/CVaR. |
| **FTR/Power/Gas** | t-copula is a robust default; Gumbel if focus on joint spikes; Clayton if focus on joint losses; validate tail dependence against data. |

**Hourly price forward curve (HPFC): shaping methodologies for power**

**Why an hourly curve is needed**  
Liquid power forwards are typically **monthly** or **block** (e.g. peak, off-peak, 7×24). For **valuation** (e.g. hourly optionality, storage, flexible load), **risk** (hourly P&L, VaR), or **dispatch**, an **hourly price forward curve (HPFC)** is required: $P_h$ for each hour $h$ in the delivery period. **Shaping** = turning **block or monthly forwards** into a **consistent** set of **hourly** prices.

**No-arbitrage constraint**  
Whatever the method, the HPFC must be **consistent** with liquid forwards: the **volume-weighted** (or **time-weighted**) average over each **trading period** must match the **forward** for that period. For example:
- **Monthly** forward $F_{\mathrm{month}}$: $\frac{1}{H}\sum_{h \in \mathrm{month}} P_h = F_{\mathrm{month}}$ (or weight by load if needed).
- **Peak block** (e.g. 7–22 weekdays): $\frac{1}{|\mathrm{peak}|}\sum_{h \in \mathrm{peak}} P_h = F_{\mathrm{peak}}$.
- **Off-peak block:** same idea. So shaping is **constrained**: the hourly profile is chosen so that when **aggregated** to each block/month, it **matches** the forward.

**Shaping methodologies**

**1. Proportional (ratio) method**  
Use a **reference shape** (hourly profile) $s_h \geq 0$ (e.g. historical hourly prices or load for the same month, normalized). Set
$$
P_h = F \cdot \frac{s_h}{\bar{s}}, \qquad \bar{s} = \frac{1}{H}\sum_h s_h.
$$
$F$ = forward for the period (e.g. month or block). Then $\frac{1}{H}\sum_h P_h = F$. **Variants:** (a) **Block-specific:** use a **peak** shape for peak hours and **off-peak** shape for off-peak; scale each block so its average = $F_{\mathrm{peak}}$ or $F_{\mathrm{off}}$. (b) **Multiple months:** one shape per month (or season) from historical same month. **Pros:** Simple; no arbitrage by construction. **Cons:** Shape is **backward-looking**; may miss structural change (e.g. solar shifting peak).

**2. Load-based (demand) shaping**  
Use **hourly load** (demand) $L_h$ as the shape: $s_h = L_h$. Rationale: price is often **demand-driven** (high load → high price). Normalize so block/month average = forward. **Pros:** Intuitive; uses fundamental driver. **Cons:** Load is not price; merit order and renewables break a 1:1 link; need **forecast** load for future months.

**3. Temperature-driven adjustment**  
Use **temperature** (or HDD/CDD) to **adjust** the shape. For example: hourly price regression
$$
P_h = \alpha + \beta_{\mathrm{hour}} + \gamma\, T_h + \delta\, T_h^2 + \text{(month/day-type dummies)} + \varepsilon_h.
$$
Fit on history; for HPFC, use **forecast** $T_h$ and **forward** as level (replace intercept or level factor so that block average = forward). **Pros:** Captures **weather**-driven shape (e.g. cooling load). **Cons:** Needs **temperature forecast** by hour; model risk.

**4. Principal components (factor) method**  
Decompose **historical** hourly prices into **factors**: e.g. $P_h = \mu_h + \sum_{k=1}^K \phi_{h,k} Z_k$ where $\mu_h$ = mean profile, $\phi_{h,k}$ = loadings (e.g. from PCA), $Z_k$ = factors. Fit **factor levels** $Z_k$ so that when the reconstructed $P_h$ is **aggregated** to each block/month, it matches **forwards**. Solve a **constrained** optimization (match $F_{\mathrm{peak}}$, $F_{\mathrm{off}}$, $F_{\mathrm{month}}$, etc.). **Pros:** Uses **historical price** structure; flexible. **Cons:** More complex; need enough history; factors may be unstable.

**5. Spline / interpolation between blocks**  
You have **peak** forward $F_P$ and **off-peak** forward $F_O$. Assign **hours** to peak vs off-peak (e.g. 7–22 weekdays = peak). Set $P_h = F_P$ for peak hours and $P_h = F_O$ for off-peak (flat within block). For **smoother** curve: **interpolate** between block boundaries (e.g. spline in time so that **average** over peak = $F_P$ and over off-peak = $F_O$). **Pros:** Simple; exact block match. **Cons:** **No intra-block** shape (flat or smooth only); no hour-of-day nuance (e.g. noon vs 18:00).

**6. Regression with forward as level**  
Regress historical $P_h$ on **hour dummies**, **day type** (weekday/weekend/holiday), **month**, and optionally **temperature**. Get **shape** coefficients. For HPFC: set **level** (intercept or month factor) so that $\frac{1}{H}\sum_h \widehat{P}_h = F$ for the month. **Pros:** Flexible; can include many drivers. **Cons:** Same as (3); need forecasts for regressors; overfitting risk.

**7. Iterative / constrained optimization**  
Define a **target** (e.g. minimize distance to a **prior** shape, or minimize curvature) subject to **linear constraints**: $\sum_{h \in B} w_h P_h = F_B$ for each block $B$. Solve **quadratic program** (QP) or similar. **Pros:** Can combine **prior** (e.g. historical shape) with **exact** match to forwards. **Cons:** More implementation; choice of prior and weights.

**Comparison and selection**

| Method | Data needed | No-arb (block match) | Intra-day shape | Typical use |
|--------|-------------|---------------------|-----------------|-------------|
| **Proportional** | Historical hourly prices or load | Yes (by construction) | From historical profile | Default; simple |
| **Load-based** | Load forecast | Yes (scale to match) | From load | Demand-driven markets |
| **Temperature** | Temp forecast + regression | Yes (level set to forward) | From model | Weather-sensitive shaping |
| **Factor (PCA)** | Historical hourly prices | Yes (solve for factors) | From factors | Rich history; many blocks |
| **Spline / block** | Peak/off-peak forwards | Yes (flat or spline) | Flat or smooth only | Quick; few blocks |
| **Regression** | History + forecast regressors | Yes (level to forward) | From regression | Custom drivers |
| **Constrained QP** | Prior shape + forwards | Yes (constraints) | From solution | Prior + exact match |

**Issues and refinements**
- **Renewables:** **Solar** flattens or shifts the midday peak; **wind** can be uncorrelated with load. Use **renewables-aware** shapes (e.g. net load, or shapes from recent years with high renewables).
- **Holidays and DST:** Use **day-type** (weekday/weekend/holiday) and **hour** (e.g. 1–24 or clock hour) so DST and holidays are treated separately.
- **Multiple blocks:** When you have **month**, **peak**, **off-peak**, and possibly **7×24**, constraints can be **overdetermined** (no exact solution). Use **weighted** fit or **hierarchy** (e.g. match month first, then distribute to peak/off-peak by shape).
- **Validation:** Compare **shaped** HPFC to **realized** hourly prices (backtest); check **block** averages vs forwards; stress **shape** (e.g. use a conservative or stressed profile for risk).

**Summary**  
To build an **hourly price forward curve** from block/month forwards: (1) **No-arbitrage**: hourly curve must average to forwards over each traded block/month. (2) **Proportional** shaping (historical or load-based) is the most common and robust. (3) **Temperature** or **regression** add flexibility for weather. (4) **Factor** or **constrained QP** methods allow a prior shape with exact block match. (5) Account for **renewables**, **day type**, and **multiple blocks**; validate against history and stress shapes for risk.

**Natural gas modeling for portfolio analysis**

**Why model gas**  
A **gas portfolio** (forwards, options, basis, storage, swing) needs **curves** (by location and tenor), **volatility** (for options and risk), and **dynamics** (for VaR, Greeks, and correlation with power). Gas is **storable**, so **inventory** and **seasonality** (winter/summer) drive **contango/backwardation** and **basis**; **spikes** (cold snaps, supply shocks) and **mean reversion** are central. Below are models commonly used for **valuation**, **risk**, and **simulation**.

---

**1. Spot / short-term price: mean reversion and jumps**

**One-factor mean-reverting (OU or Schwartz)**  
Gas spot (or prompt) is often modeled as **mean-reverting** in level or log:

$$
\mathrm{d}S_t = \kappa(\theta_t - S_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t \quad \text{(OU)}, \qquad \text{or} \quad \mathrm{d}\ln S_t = \kappa(\mu - \ln S_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t \quad \text{(Schwartz 1-factor)}.
$$

- **Seasonality:** Set $\theta_t = \theta(t)$ (e.g. winter high, summer low) or add a **seasonal** component to $\mu$.  
- **Use:** Forwards and **vanilla options** (Black-76 on forward); **simulation** for VaR.  
- **Calibration:** $\kappa$, $\theta$ (or $\mu$), $\sigma$ from **historical** spot or from **forward curve** (e.g. fit to observed $F(0,T)$).

**Jump-diffusion (spikes)**  
Add **Poisson jumps** for **cold snaps** or **supply** events:

$$
\mathrm{d}S_t = \kappa(\theta - S_t)\,\mathrm{d}t + \sigma\,\mathrm{d}W_t + (e^J - 1)S_t\,\mathrm{d}N_t, \quad J \sim N(\mu_J, \sigma_J^2), \quad N_t \sim \mathrm{Poisson}(\lambda).
$$

- **Use:** **Tail risk** and **option** pricing when **spikes** matter; **VaR** with fat tails.  
- **Simulation:** Euler for diffusion; add jump component over $\Delta t$ (draw $n \sim \mathrm{Poisson}(\lambda\Delta t)$, then $n$ i.i.d. $J$).

---

**2. Two-factor (Schwartz–Smith): short-term deviation + long-term level**

**State variables:** $x_t$ = short-term deviation (mean-reverting); $\xi_t$ = long-term equilibrium (random walk or drift). **Spot:**
$$
\ln S_t = x_t + \xi_t, \qquad \mathrm{d}x_t = -\kappa x_t\,\mathrm{d}t + \sigma_x\,\mathrm{d}W_x, \qquad \mathrm{d}\xi_t = \mu_\xi\,\mathrm{d}t + \sigma_\xi\,\mathrm{d}W_\xi, \quad \mathrm{Corr}(W_x,W_\xi) = \rho.
$$

- **Forward curve:** Closed-form $F(t,T) = \mathbb{E}[S_T \mid \mathcal{F}_t]$ under risk-neutral measure (affine in $x_t$, $\xi_t$). Useful for **curve** construction and **consistency** with liquid forwards.  
- **Use:** **Curve** simulation; **option** pricing; **correlation** with power (e.g. same $\xi$ or correlated $W$).  
- **Calibration:** Fit to **forward** curve $F(0,T)$ and optionally **option** implied vols; or to **historical** spot and forward data.

---

**3. Basis and multi-location**

**Hub + basis**  
Let $S^{\mathrm{hub}}_t$ = liquid hub price (e.g. Henry Hub); $S^{\mathrm{loc}}_t$ = location price. **Basis** $B_t = S^{\mathrm{loc}}_t - S^{\mathrm{hub}}_t$ (or ratio). Model **basis** as **mean-reverting** (pipeline and flow constraints keep it bounded):

$$
\mathrm{d}B_t = \kappa_B(\theta_B - B_t)\,\mathrm{d}t + \sigma_B\,\mathrm{d}W_B, \qquad \mathrm{Corr}(W_{\mathrm{hub}}, W_B) = \rho.
$$

- **Location price:** $S^{\mathrm{loc}}_t = S^{\mathrm{hub}}_t + B_t$ (additive) or $S^{\mathrm{loc}}_t = S^{\mathrm{hub}}_t \cdot e^{B_t}$ (multiplicative).  
- **Use:** **Basis** options and **location** risk; **portfolio** with multiple hubs/locations.  
- **Alternative:** **Cointegration** between hub and location (long-run relationship); **error-correction** for basis.

**Multi-hub correlation**  
For **portfolio** VaR with **several** locations: model each hub (or hub + basis) with **correlated** Brownian motions (Cholesky of $\rho$). **Joint** simulation of $S^1_t,\ldots,S^d_t$ for delta, VaR, and correlation with **power**.

---

**4. Forward curve dynamics (for risk and VaR)**

**Risk factors** = key **forward** tenors (e.g. prompt, 3-month, 12-month, winter strip). Assume **lognormal** or **normal** returns with **mean reversion**:

$$
\frac{\mathrm{d}F(t,T)}{F(t,T)} = \mu(t,T)\,\mathrm{d}t + \sigma(T)\,\mathrm{d}W_T \quad \text{(lognormal)}, \qquad \text{or} \quad \mathrm{d}F(t,T) = \kappa(\theta(T) - F(t,T))\,\mathrm{d}t + \sigma(T)\,\mathrm{d}W_T.
$$

- **Correlation:** $\mathrm{Corr}(\mathrm{d}W_{T_1}, \mathrm{d}W_{T_2}) = \rho(T_1,T_2)$ (e.g. from **historical** forward returns).  
- **Use:** **Delta** (sensitivity to curve); **VaR** (simulate curve scenarios); **stress** (parallel shift, twist, etc.).  
- **No-arbitrage:** If using **multiple** tenors, ensure **consistency** (e.g. no calendar arbitrage); **factor** models (level, slope) reduce dimension and help keep consistency.

---

**5. Storage and swing (optionality)**

**Storage** = option to **inject** (buy gas, store) and **withdraw** (sell) subject to **capacity**, **injection/withdrawal rates**, and **cycle** limits. **Swing** = flexible **volume** within bounds over the contract period.

- **Valuation:** **Dynamic programming** (backward induction) or **least-squares Monte Carlo (LSMC)**. **State:** inventory level, time; **control:** inject/withdraw/do nothing. **Payoff:** value of gas sold minus cost of gas bought minus **storage cost**.  
- **Model input:** **Forward curve** $F(t,T)$ and **volatility** $\sigma(T)$ (and possibly **spread** vol between injection and withdrawal periods). **Simplified:** **spread option** (spark or storage spread) as proxy.  
- **Portfolio:** Storage value is **convex** in price; **delta** and **vega** matter; **correlation** between **prompt** and **forward** affects value.

**Swing**  
Often modeled as **multiple** (daily or monthly) **options** on volume (take or pay), or as a **compound** option; **LSMC** or **tree** methods.

---

**6. Volatility: term structure and smile**

- **Term structure:** **Short-dated** vol (prompt, winter) is **higher**; **long-dated** (year-ahead) is **lower**. Use **time-dependent** $\sigma(T)$ or **mean-reverting** vol factor.  
- **Smile:** **Options** (calls, puts, spreads) imply **skew** (e.g. OTM calls rich in winter). **Black-76** with **implied vol** by strike; or **SABR** / **jump** model for **smile** and **vega** risk.  
- **Portfolio:** **Vega** by tenor and strike; **stress** vol (e.g. vol + 20%) for risk.

---

**Summary: gas models in portfolio analysis**

| Model | Use | Main idea |
|-------|-----|-----------|
| **OU / Schwartz 1-factor** | Spot, forwards, simple options | Mean reversion (level or log); seasonal $\theta(t)$ |
| **Jump-diffusion** | Spikes, tail risk, options | OU + Poisson jumps (e.g. lognormal jump size) |
| **Two-factor (Schwartz–Smith)** | Curve, consistency, correlation | Short $x_t$ + long $\xi_t$; closed-form $F(t,T)$ |
| **Hub + basis** | Location, basis options | Hub process + mean-reverting basis $B_t$ |
| **Forward curve dynamics** | Delta, VaR, stress | Lognormal or OU per tenor; correlation $\rho(T_1,T_2)$ |
| **Storage / swing** | Physical optionality | DP or LSMC; state = inventory, control = inject/withdraw |

**Portfolio workflow:** Build **forward curves** (hub + basis) → choose **dynamics** (1-factor, 2-factor, or multi-tenor) and **vol** (term structure, smile) → **value** positions (forwards, options, storage) → **simulate** for VaR (correlated with power/FTR if needed) → **Greeks** (delta, vega) and **stress** tests.

**Products available for FTR, Power, and Gas trading in North American markets**

Overview of **tradable products** in North American **FTR** (financial transmission rights), **power**, and **gas** markets — by market, product type, and venue (exchange vs OTC).

---

**FTR / CRR (Financial Transmission Rights / Congestion Revenue Rights)**

| Market | Name | Product types | Tenor | Venue |
|--------|------|---------------|--------|-------|
| **ERCOT** (Texas) | **CRR** | **PTP Option** (pay when spread &gt; 0 only), **PTP Obligation** (pay or receive spread); **with Refund** (NOIE pre-assigned, not tradable) | Monthly, up to ~2 years (long-term auction) | **Auction** (monthly, long-term sequence); **bilateral** (CRR Account Holders) |
| **PJM** | **FTR** | **FTR Obligation**, **FTR Option** (revenue rights); **ARR** (Auction Revenue Rights) for LSEs | Annual, monthly; long-term multi-year | **Auction** (annual, monthly); **secondary** (bilateral, exchange) |
| **MISO** | **FTR** | **FTR** (point-to-point, flow-based); **TLR** (Transmission Loading Relief) for real-time | Annual, monthly | **Auction**; **bilateral** |
| **SPP** (SPP) | **CRR** / **FTR** | Point-to-point financial rights on congestion | Annual, monthly | **Auction**; **bilateral** |
| **CAISO** | **TCC** (Congestion Revenue Rights) | **TCC** (obligation-style); **FTR** in some contexts | Annual, monthly | **Auction**; **bilateral** |
| **NYISO** | **TCC** / **FTR** | **Transmission Congestion Contracts**; point-to-point | Annual, monthly | **Auction**; **bilateral** |
| **ISO-NE** | **FTR** | Point-to-point financial transmission rights | Annual, monthly | **Auction**; **bilateral** |

- **Acquisition:** **Allocation** (e.g. ERCOT PCRRs to NOIEs; PJM ARRs); **auction** (monthly, annual, long-term); **bilateral** (trades between CRR/FTR account holders).  
- **Settlement:** Typically **day-ahead** market (DAM) **congestion** component (LMP spread source–sink); **daily** settlement over contract period.  
- **Products for risk:** Path × MW × TOU (peak/off-peak) × month; **options** vs **obligations**; **tradable** vs **with Refund** (ERCOT).

---

**Power**

| Market | Hub / region | Exchange (e.g. CME, ICE) | OTC | Tenor / shape |
|--------|--------------|---------------------------|-----|----------------|
| **ERCOT** | North, South, West, Houston, etc. | **CME** ERCOT (North, South); **ICE** | Forwards, swaps, options (vanilla, Asian, spread) | **Monthly**, **quarterly**, **calendar**; **peak**, **off-peak**, **7×24**; **daily** (prompt) |
| **PJM** | Western Hub, Eastern Hub, AEP, etc. | **CME** PJM; **ICE** | Same | Monthly, quarterly, calendar; peak, off-peak |
| **MISO** | Indiana Hub, Illinois Hub, etc. | **ICE** MISO | Same | Monthly, seasonal; peak, off-peak |
| **SPP** | SPP North, South, etc. | **ICE** SPP | Same | Monthly, seasonal |
| **CAISO** | SP15, NP15, ZP26 (Palo Verde) | **ICE**; **CME** (limited) | Same | Monthly, quarterly; peak, off-peak |
| **NYISO** | Zone A–J, NYISO hub | **ICE** NYISO | Same | Monthly, seasonal; peak, off-peak |
| **ISO-NE** | Mass Hub, NEPOOL, etc. | **ICE** ISO-NE | Same | Monthly, seasonal; peak, off-peak |

**Product types (power)**  
- **Physical:** Bilateral **physical** contracts (for delivery); **PPAs** (power purchase agreements); **self-schedule** in DAM/RT.  
- **Financial – forwards/swaps:** **Fixed-for-floating** (fixed $/MWh vs floating index, e.g. DAM or RT hub); **monthly**, **quarterly**, **calendar** strips; **peak** (e.g. 7–22 weekdays), **off-peak**, **7×24**.  
- **Financial – options:** **Calls**, **puts** (on price or on spread); **Asian** (average price); **spread options** (e.g. hub A – hub B, or **spark spread** power – gas). **Structured:** Collars, caps, floors.  
- **DAM vs RT:** **Day-ahead** (DAM) and **real-time** (RT) products; **DAM PTP Obligations** (ERCOT) for RT congestion hedge.  
- **Venue:** **Exchange** (CME, ICE) = cleared, standardized; **OTC** = bilateral (ISDA/CSA) or cleared; **brokers** for price discovery.

---

**Natural gas**

| Product / location | Exchange | OTC | Tenor / shape |
|--------------------|----------|-----|----------------|
| **Henry Hub** (benchmark) | **NYMEX** (CME) futures, options; **ICE** | Forwards, swaps, options | **Monthly**, **seasonal** (e.g. Nov–Mar winter, Apr–Oct summer), **calendar**; **daily** (prompt) |
| **Basis** (location vs Henry) | **ICE** basis futures (e.g. Transco Z6, SoCal, Waha, Chicago) | **Basis** swaps, options | Monthly, seasonal; by **location** |
| **Physical** | Pipeline **capacity**, **storage** (injection/withdrawal), **LNG** | **Bilateral** physical; **capacity** releases | Daily, monthly, seasonal; **swing** (flex volume) |
| **Spread / optionality** | **ICE** options; **CME** options on Henry | **Spark spread** (power – heat rate × gas); **storage** optionality; **swing** options | Monthly, seasonal; **heat rate** (power/gas) |

**Product types (gas)**  
- **Futures / forwards:** **Henry Hub** monthly, seasonal strips; **basis** (location – Henry) by pipeline/hub (e.g. Transco Zone 6, SoCal, Waha, Chicago, Appalachia).  
- **Swaps:** **Fixed-for-floating** (fixed $/MMBtu vs index); **basis** swaps (fixed basis vs floating basis).  
- **Options:** **Calls**, **puts** on Henry or basis; **spread options** (e.g. winter – summer); **swing** (volume flexibility).  
- **Physical:** **Pipeline capacity** (firm, interruptible); **storage** (inject/withdraw); **LNG**; **swing** contracts (daily take within min/max).  
- **Venue:** **NYMEX/CME**, **ICE** (cleared); **OTC** (bilateral or cleared); **brokers**.

---

**Summary**

| Asset | Main products | Main markets (NA) | Venue |
|-------|----------------|------------------|-------|
| **FTR/CRR** | Obligations, options; path × MW × TOU × month | ERCOT, PJM, MISO, SPP, CAISO, NYISO, ISO-NE | RTO **auction**; **bilateral** (registered holders) |
| **Power** | Forwards, swaps, options (vanilla, Asian, spread); peak/off-peak/7×24 | ERCOT, PJM, MISO, SPP, CAISO, NYISO, ISO-NE | **CME**, **ICE** (cleared); **OTC** |
| **Gas** | Henry futures/options; basis; physical (capacity, storage, swing) | Henry Hub + regional hubs (SoCal, Waha, Transco, Chicago, etc.) | **NYMEX**, **ICE**; **OTC**; physical pipelines/storage |

For **portfolio** and **risk** work: know **which** products are **liquid** (exchange vs OTC), **tenor** (prompt, monthly, seasonal, calendar), **block** (peak, off-peak, 7×24), and **location** (hub, basis). **FTR** is **path-based** and **RTO-specific**; **power** and **gas** are **hub/location-based** with **exchange** and **OTC** layers.

---

## 2. Risk reporting tools (risk analysis, P&L attribution, portfolio construction)

**Bullet:** Improve and extend existing risk reporting tools, including risk analysis, P&L attribution, and portfolio construction, with focus on both regular periodic reporting and ad-hoc requests.

### Scope (reporting layer; no repetition of modeling above)

- **Reporting layer vs modeling:** Section 1 covers **how** risk is computed (curves, vol surfaces, VaR, Greeks). This bullet is about **delivering** that (and related) information through **tools** and **reports**: dashboards, scheduled packs, and one-off analysis so stakeholders can monitor risk, understand P&L, and support portfolio and business decisions.
- **Improve and extend:** Implies working on **existing** tooling: refactoring for performance and maintainability, adding new views or breakdowns (e.g. by book, region, tenor), improving data pipelines that feed reports, and making outputs easier to interpret and audit. May include **automation** (e.g. scheduled runs, alerts) and **self-serve** capability where possible.

### Risk analysis in reporting

- **What “risk analysis” means here:** Presenting risk metrics (e.g. VaR, ES, Greeks, stress results) in clear, drill-downable form: by **book** (FTR / power / gas), **tenor**, **location**, **factor** (curve, vol). Views might include exposure summaries, limit utilization, scenario comparisons, and time series of risk. Tools should support **filtering**, **comparison across dates or portfolios**, and **export** for further analysis or audit.
- **Extending tools:** Add new risk views (e.g. intramonth VaR, DART vs DAM breakdown), improve run times and refresh frequency, and ensure consistency with the risk engine (same definitions and data as production risk).

### P&L attribution in reporting

- **What to report:** Decomposition of **realized** or **hypothetical** P&L into **contributors**: e.g. curve move (delta), vol move (vega), theta, new trades, and residual. By **book**, **strategy**, or **region** as needed. Period-over-period and cumulative views; reconciliation to trading P&L and to risk (e.g. VaR backtesting).
- **Extending tools:** Richer attribution (e.g. bucket-level curve attribution, vol term-structure), faster availability (e.g. T+0 or intraday), and flexible date ranges and segmentations for ad-hoc questions.

### P&L attribution of an FTR / Power / Gas portfolio (methodology)

**Goal:** Explain **1-day (or period) P&L** = $V_t - V_{t-1}$ for a **mixed** portfolio by **source**: curve moves, vol moves, time decay, new trades, and residual. Attribution is **by book** (FTR, power, gas) and **by factor** within each book so that risk, trading, and management can see *why* P&L moved.

**Generic decomposition (all books)**

- **Curve (delta):** First-order effect of **forward/spread curve** moves. Approximate: $\sum_{\text{buckets}} \Delta_{\text{bucket}} \times \Delta F_{\text{bucket}}$ (or revalue at $t$ with curves from $t-1$ and take the difference). For **power** and **gas**, buckets = hub (and optionally location/basis) by tenor; for **FTR**, buckets = path spread or nodal/spread curve by path and delivery period.
- **Vol (vega):** Effect of **implied vol** (surface) move. Approximate: $\mathcal{V} \times \Delta\sigma$ (parallel) or sum over tenor/strike buckets (vega bucket × Δσ bucket). Relevant for **options** in power, gas, and **optional** FTR (e.g. PTP options).
- **Theta:** Time decay (option value loss as we approach expiry; forward roll). $\Theta \times \Delta t$ or revalue with same curves/vol but time $t$ vs $t-1$.
- **New trades:** P&L from **positions added or removed** in the period. Compare $V_t$ on **portfolio as of $t$** vs $V_t$ on **portfolio as of $t-1$** (or use trade-level P&L from blotter). Ensures we don’t attribute new deal flow to “curve” or “vol.”
- **Residual:** Unexplained P&L = actual P&L − (curve + vol + theta + new trades). Captures **gamma** (second-order curve), **vanna/volga**, **basis** moves not in curve buckets, **model** or **data** changes (e.g. curve rebuild, vol surface update), and **timing** (e.g. settlement, fixings).

**FTR book**

- **Curve:** FTR value depends on **path spread curves** (sink − source by path and delivery month). **Delta attribution** = sensitivity to each path/tenor spread × realized change in that spread (or revalue with prior curves). Curves may be **proxy** (e.g. hub spread, congestion model); document whether attribution uses same curves as MTM.
- **Vol:** Only for **optional** FTR (e.g. spread options, PTP options). Vega × Δσ (spread vol or proxy vol) if the mark uses an option model.
- **Theta:** Optionality decays with time; linear positions have no theta. For path-based rights, **remaining delivery** shortens each day → small “roll” effect even for obligations.
- **New trades:** New FTR from **auctions** or **secondary**; unwinds or adjustments. Often material in attribution (large discrete positions).
- **Residual:** **Volume** or **availability** effects (derates, forced outages) that change **settlement** vs curve assumption; **realized** DAM spread vs **curve** (realization variance); **model** change (e.g. spread curve methodology).

**Power book**

- **Curve:** **Hub** (and **location**) forward curve moves by **tenor** (prompt, monthly, seasonal). Attribution by **bucket** (e.g. ERCOT North Jul, Aug, …) or by **key tenors**. **Basis** (location − hub) can be a separate bucket so location-specific P&L is visible.
- **Vol:** Options (vanilla, Asian, spread) have **vega**; attribute vega × Δσ (parallel or by tenor/strike). **Asian** options: vol of average can have different term structure; attribute using the vol inputs that drive the mark.
- **Theta:** Option decay; forwards have no theta. Often material for short-dated options.
- **New trades:** New power deals (forwards, options) or unwinds in the period.
- **Residual:** **Basis** move not fully in curve buckets (e.g. location vol or correlation); **gamma** (large curve move); **fixing** vs curve (e.g. monthly average realized vs curve); **DAM vs RT** if positions are RT-settled but curve is DAM.

**Gas book**

- **Curve:** **Hub** (e.g. Henry) and **basis** (location − hub) curves by **tenor**. Attribute delta by hub bucket and by **basis bucket** (location/pipe) so that hub move vs basis move are separated.
- **Vol:** Options (e.g. swing, storage-related, basis options) have vega; attribute vega × Δσ by relevant surface (hub or basis vol).
- **Theta:** Option decay; storage optionality (optional exercise over time).
- **New trades:** New gas deals, storage injections/withdrawals, or unwinds.
- **Residual:** **Basis** move (pipeline, weather) not in buckets; **storage** model value change (inventory, spread dynamics); **gamma**; **realized** vs curve.

**Cross-book and total**

- **Total P&L:** Sum of **FTR P&L** + **Power P&L** + **Gas P&L** (each already decomposed into curve, vol, theta, new trades, residual). Report **by book** and **by factor** (e.g. “total curve” = FTR curve + power curve + gas curve) so that both book-level and factor-level stories are clear.
- **Reconciliation:** Attribution P&L (sum of attributed components) should **match** (or be close to) **actual/trading P&L** for the same portfolio and dates. Large **residual** suggests missing factors (e.g. basis, vol bucket granularity, new-trade timing) or model/data changes; investigate and tighten buckets or logic.
- **Correlation:** FTR, power, and gas can be **correlated** (e.g. gas-driven power, congestion). Attribution is **additive by book**; correlation shows up in **portfolio-level** risk (VaR, stress), not in the **attribution formula** itself. For “why did portfolio P&L move?” the additive decomposition by book and factor is the standard.

**Implementation notes**

- **Hypothetical vs realized:** **Hypothetical** P&L = revalue **today’s** portfolio at $t$ and $t-1$ (no new trades). **Realized** P&L = actual P&L from trading (includes new trades, real fixings, realizations). Attribution can be done on either; often **hypothetical** for risk explain and **realized** for trading P&L explain, with new trades explicitly broken out.
- **Bucket granularity:** Finer buckets (e.g. curve by tenor, vol by strike) improve explain but increase data and run time. Balance with **residual** size and stakeholder need; add buckets where residual is large or where drill-down is required.

**Attribution by product type (options, swaps, forwards, …)**

Attribution can be **sliced by product** as well as by book. Each product type has a **natural set of drivers**; reporting by product answers “how much P&L came from our option book vs our linear book?” and supports limit or strategy review.

| Product type | Main drivers | Notes |
|--------------|--------------|--------|
| **Forwards** | **Curve (delta)** only; **new trades**; **residual** (basis, model). | No vega, no theta (or trivial forward roll). Power/gas forwards: delta by hub/tenor (and basis if location). FTR obligations: delta by path spread. |
| **Swaps** (fixed-for-floating on price) | **Curve (delta)** on the floating leg; **new trades**; **residual**. | Financially equivalent to forward; mark = PV of (floating − fixed) flows. Delta = sensitivity to forward curve; no optionality unless embedded. |
| **Options** (vanilla, Asian, spread) | **Curve (delta)**, **vol (vega)**, **theta**; **new trades**; **residual** (gamma, vanna/volga, smile). | Power/gas: calls, puts, Asians, spread options. FTR: PTP options, spread options. All have delta + vega + theta; residual often includes gamma. |
| **FTR obligations** | **Curve** (path spread); **new trades**; **residual** (realization, volume). | Linear in spread; no vol/theta in the mark unless optionality (e.g. capacity) is modeled. |
| **FTR options** (e.g. PTP option) | **Curve**, **vol** (spread vol), **theta**; **new trades**; **residual**. | Optionality → same factor set as other options. |
| **Storage / swing** | **Curve** (forward and spread); **vol** (optionality); **theta** (optional exercise); **new trades**; **residual** (inventory, model). | Hybrid: linear exposure to curve + optional value (vega, theta). |
| **Basis** (location, calendar) | **Curve** (basis curve move); **new trades**; **residual**. If options on basis: add **vega**, **theta**. | Attribute basis delta separately from hub delta so “location P&L” is visible. |

**How to combine with “by book”**

- **Two dimensions:** (1) **Book** = FTR, Power, Gas. (2) **Product** = Forwards, Swaps, Options, (FTR obligations, FTR options), Storage, Basis, etc. Report P&L (and attribution) in a **matrix**: e.g. Power–Forwards (curve, new trades, residual), Power–Options (curve, vol, theta, new trades, residual), Gas–Swaps (curve, new trades, residual), Gas–Options (curve, vol, theta, …), FTR–Obligations (curve, new trades, residual), FTR–Options (curve, vol, theta, …).
- **Roll-up:** **Total curve** = sum of curve attribution across all products (and books). **Total vol** = sum of vega attribution (options only). **Total theta** = sum of theta (options, optional storage). **Total new trades** = sum across products. So you get both “by book” and “by product” views without double-counting.
- **Use cases:** (1) **Risk limits** by product (e.g. option vega limit vs forward delta limit). (2) **Strategy P&L** (e.g. “power options contributed $X from vol”). (3) **Residual drill-down** (e.g. residual concentrated in options → check gamma/smile). (4) **Reconciliation** (e.g. trading desk views by product; risk attribution by product matches).

**Product-level nuances**

- **Swaps vs forwards:** For attribution, treat the same (curve delta). For **reporting**, some shops separate “physical” vs “financial” or “swap” vs “forward” by settlement; attribution logic is identical (curve + new trades + residual).
- **Asian options:** Curve and vol (vol of average); theta. Attribute **vega** using the vol input that drives the Asian mark (may be a single “vol of average” or term structure of average vol).
- **Spread options** (e.g. power spread, gas basis spread): **Delta** to both underlyings (or to spread curve if modeled as single factor); **vega** to spread vol (or to two vols + correlation). Residual can be large if correlation or spread distribution is wrong.
- **Physical vs financial:** **Physical** (e.g. physical power delivery, gas storage) may have **operational** P&L (nominations, imbalance) that sits in **residual** or a separate “physical/operational” bucket if not modeled as curve. **Financial** positions: full attribution as above.

### Portfolio construction in reporting

- **What to report:** Exposure and composition views: **notional** or **sensitivity** by product, hub, tenor, path (FTR); concentration and limits; correlation and diversification; optionality (gamma/vega) by book. Supports answering “what do we own?” and “where is risk concentrated?” for both regular review and strategy decisions.
- **Extending tools:** New aggregation dimensions (e.g. by congestion zone, by counterparty), integration with limits and mandates, and links to pricing/risk so that “portfolio construction” reporting stays aligned with live books.

### Building a platform for portfolio construction (FTR, power, gas)

**Objective:** A **platform** that supports **further portfolio construction** — i.e. decisions on **what to add or reduce** (size, tenor, location, product mix) given the **current** book, **risk**, **constraints**, and **objectives**. It should answer “if we add this trade, how does risk and P&L change?” and “where are we over- or under-exposed relative to our mandate?”

**What to do (practical steps)**

1. **Single source of truth for positions and risk factors**  
   **Positions:** One consolidated view of all **FTR** (path × MW × TOU × delivery), **power** (forwards, options, swaps by hub/location and tenor), and **gas** (hub, basis, options, storage) with consistent **identifiers** (path ID, contract ID, delivery period). **Risk factors:** Forward curves (power hub/location, gas hub/basis), FTR spread curves (or proxy), vol surfaces where needed, discount curve. The platform must **ingest** positions and factors from trading/risk systems (or a data lake) so that “current portfolio” and “current market” are unambiguous. **Versioning** (as-of date, curve version) is critical so scenario and what-if use the same baseline.

2. **Unified valuation and risk engine**  
   **Valuation:** Same **pricing logic** as production risk (curves, vol, models) so that MTM and risk in the platform match official risk reports. FTR = path spread × MW × hours (and optionality if applicable); power = forwards + options (Black-76/Asian); gas = forwards + basis + options + storage model. **Risk:** Greeks (delta by bucket), VaR (historical or MC), stress, and — for construction — **marginal** and **component** risk (e.g. contribution to VaR by position or by book). Without a unified engine, “what-if” and “optimization” would be inconsistent with live risk.

3. **Portfolio construction views**  
   - **Exposure:** Notional and **delta** (sensitivity) by **dimension**: book (FTR / power / gas), product (forwards, options, swaps), **hub/location/path**, **tenor**. Heat maps or tables: e.g. power delta by hub × tenor, FTR notional by path × month.  
   - **Concentration:** Share of risk or notional in top N paths, hubs, or tenors; compare to limits or policy (e.g. “no path &gt; X% of VaR”).  
   - **Marginal contribution to risk:** For each position (or sub-portfolio), **marginal VaR** or **component VaR** — how much does VaR change if we remove or add a unit? Identifies “risk-heavy” positions and **diversifiers** (negative marginal contribution).  
   - **Limit utilization:** Current exposure vs **limits** (VaR, delta by bucket, notional by path, option vega). Flag breaches and “headroom” for new trades.  
   - **Correlation and diversification:** Correlation matrix across books or key factors; diversification benefit (portfolio VaR vs sum of standalone VaRs). Shows where FTR, power, and gas offset or reinforce each other.

4. **Scenario and what-if**  
   - **Hypothetical trades:** “Add +50 MW FTR on path P for month M” or “Sell 100 MW power forward hub H, Jul” → **revalue** and **recompute** VaR, Greeks, and P&L distribution. Compare **before vs after** so the user sees the **incremental** risk and expected P&L of the trade.  
   - **Curve/vol shocks:** “If power curve +$5/MWh” or “if vol +5 points” → impact on current portfolio and on proposed trades. Supports **stress** and **sensitivity** of construction choices.  
   - **Batch what-if:** Evaluate **many** candidate trades (e.g. list of FTR bids or power tenors) and rank by risk-adjusted return, marginal VaR, or fit to target exposure. Enables screening before execution.

5. **Optimization (optional)**  
   - **Objective:** e.g. maximize **expected P&L** or **Sharpe** subject to **VaR limit**, **delta/vega limits**, **notional or position limits**, and **liquidity** (e.g. only liquid paths/hubs). Or minimize **tail risk** (CVaR) for a target return.  
   - **Decision variables:** Size (and possibly tenor/path) of **trades** in a predefined universe (e.g. FTR paths in next auction, power/gas forwards at liquid hubs).  
   - **Constraints:** Hard limits (mandates, regulatory), soft (preferences). **Implementation:** Quadratic or linear program if risk is approximated (e.g. delta-VaR); or **simulation-based** (MC of P&L, then optimize over trial portfolios) if full revaluation is needed.  
   - **Output:** Recommended **trade list** (buy/sell, size) and **resulting** risk/return. Always **review** outputs — optimization can be sensitive to inputs (curves, correlation, constraints) and to misspecified objectives.

6. **Integration with execution and reporting**  
   - **Execution:** Link to **auction** calendars and **trading** (e.g. pre-trade checks: does this trade stay within limits?). Post-trade: new positions flow back into the platform so “current portfolio” updates.  
   - **Reporting:** Portfolio construction views and what-if results should be **auditable** (same definitions as risk reporting) and **distributable** (dashboards, packs) so that strategy and risk committees can see current state and proposed changes.  
   - **Iteration:** As mandates or limits change, the platform should support **re-running** exposure, marginal risk, and optimization so construction stays aligned with policy.

**Challenges**

- **Data:** Positions and curves may live in **multiple** systems (FTR registry, power/gas trading, risk). Deduplication, mapping (e.g. path ID to risk factor), and **refresh frequency** (daily vs intraday) matter.  
- **FTR granularity and illiquidity:** Many **paths** have no liquid market; “universe” for optimization or what-if may be limited to **auction-eligible** or **liquid** paths. Spread curves are often **model-derived** → uncertainty in MTM and risk.  
- **Correlation and joint distribution:** FTR, power, and gas are **correlated** (e.g. gas drives power; congestion links FTR and power). Wrong correlation → wrong diversification and marginal VaR. Estimate and stress-test correlation assumptions.  
- **Constraints:** Some limits are **hard** (regulatory); others **soft** (relationship, capacity). Formalizing all of them in an optimizer can be difficult; use optimization as **input** to human judgment rather than auto-execution.

**Summary**

Build the platform in layers: (1) **Data** — consolidated positions and risk factors, versioned. (2) **Valuation and risk** — same as production, with marginal/component risk. (3) **Views** — exposure, concentration, marginal VaR, limits, correlation. (4) **What-if** — hypothetical trades and shocks; before/after comparison. (5) **Optimization** (optional) — objective + constraints → recommended trades for review. (6) **Integration** — execution and reporting so construction decisions are traceable and the book stays consistent with risk.

### Periodic vs ad-hoc

- **Periodic reporting:** Scheduled, repeatable packs (e.g. daily risk pack, weekly P&L attribution, monthly portfolio summary). Requirements: **reliability** (runs on time, no silent failures), **consistency** (same layout and logic), **versioning** (know which data and code produced each run), and **distribution** (email, portal, or shared drive). Automation (schedulers, DAGs) and clear ownership of data and code paths are important.
- **Ad-hoc requests:** One-off or exploratory analysis: custom date ranges, new slices (e.g. “FTR by path length” or “power by peak vs off-peak”), stress scenarios, or “why did VaR move?”. Requirements: **flexibility** (parameterized reports or modular data/views), **speed** (quick iteration without rebuilding everything), and **traceability** (so one-off logic can be promoted into production reports if it proves useful).

**Possible ad-hoc requests from traders (FTR, power, gas)**

Concrete examples of **one-off or exploratory** questions traders might ask; the platform should support these via **parameterized** views, **custom date ranges**, or **quick** slice/build.

**FTR**

- “What’s our **delta (or MTM sensitivity)** by **path** for next month’s delivery?” — drill into which paths drive P&L if spreads move.
- “**P&L attribution** for the FTR book for **last week** (or **yesterday**): curve vs new trades vs residual.” — explain a specific period.
- “**Concentration**: top 10 paths by notional (or by delta); what % of total FTR risk?” — check concentration before or after an auction.
- “**What-if**: if we add +100 MW on path X for month M, how does **portfolio VaR** and **FTR delta** change?” — pre-trade impact.
- “**Historical** spread (or MTM) for path P over the last 6 months” — support bid/offer or mark debate.
- “**Auction** summary: what we won in the last auction by path and month; **cost** and **current mark** vs cost.” — post-auction review.
- “**Realized** vs **curve** for a specific path/month: how did settlement compare to our curve?” — model vs realization.

**Power**

- “**Delta by hub and tenor** for the power book only (or for a specific strategy).” — hedging or limit check.
- “**Peak vs off-peak** (or 7×24) **exposure** and P&L for last month.” — block-level view.
- “**P&L explain** for power for **date D**: curve move (by bucket), vol move, theta, new trades, residual.” — daily or weekly explain.
- “**What-if**: if ERCOT North Jul forward moves +$10/MWh, what’s the impact on power book and on **total** portfolio?” — scenario.
- “**Vega** by tenor (or by option) for the power options book.” — vol risk and hedging.
- “**Basis** exposure: location A vs hub H by tenor; how much P&L from basis move last week?” — basis risk.
- “**Asian** option marks: what vol of average are we using, and sensitivity to that vol?” — mark/vega detail.
- “**DAM vs RT** exposure or P&L (if we have RT positions); or **monthly average** vs **single-day** fix.” — settlement spec.

**Gas**

- “**Delta by hub and basis** (e.g. Henry vs SoCal) by tenor.” — hub vs location risk.
- “**Storage** position: current inventory, optionality value, **vega** and **theta**.” — storage-specific risk.
- “**P&L attribution** for gas for **last week**: curve (hub + basis), vol, theta, new trades, residual.” — explain.
- “**What-if**: Henry +$1/MMBtu and basis at location X widens by $0.50; impact on gas book and portfolio?” — scenario.
- “**Swing** (or **capacity**) optionality: how much vega and delta; sensitivity to vol?” — structured product detail.
- “**Winter strip** vs **summer strip** exposure and last month’s P&L.” — seasonal view.
- “**Basis** volatility (realized or implied) for location Y; how does it compare to hub?” — basis vol for marks or risk.

**Cross-asset and portfolio**

- “**Why did VaR move** from yesterday to today? Decomposition by book (FTR, power, gas) and by factor (curve, vol, positions).” — VaR explain.
- “**Correlation** between our FTR MTM, power P&L, and gas P&L over the last 3 months (or 1 year).” — diversification and model.
- “**Stress**: if power spikes $100/MWh and gas $5/MMBtu and FTR path Z blows out by $X, what’s **portfolio** P&L and **margin** impact?” — joint scenario.
- “**Limit utilization** as of today (or as of date D) by book and by limit type; any **breaches** or near-breaches?” — limit check.
- “**New trades** in the last 5 days: list and **incremental** VaR (or delta) from those trades.” — new business impact.
- “**Hypothetical** P&L for **today’s** portfolio over the last 30 days (using historical curves): distribution and backtest vs VaR.” — backtest on current book.
- “**Exposure** by **counterparty** (or by **venue**) for power and gas.” — credit or operational view.

**Summary:** Ad-hoc asks are typically **sliced by** (path, hub, tenor, product, date range), **what-if** (add trade, shock curve/vol), **explain** (why did X move, attribution for period), or **one-off** (concentration, correlation, stress, backtest). Keeping **data** and **metrics** modular (same valuation/risk engine, parameterized by book/date/dimension) lets these be answered without rebuilding the whole stack.

### Building a process for regular periodic risk reporting (daily, weekly, monthly, quarterly)

**Objective:** A **repeatable, auditable** process that produces **risk metric** reports at **daily**, **weekly**, **monthly**, and **quarterly** cadences so that risk, trading, and management have consistent, on-time visibility into portfolio risk (FTR, power, gas).

**Cadence and content (what to report when)**

| Cadence | Typical content | Rationale |
|--------|------------------|-----------|
| **Daily** | **Risk pack:** VaR (and ES), Greeks (delta by bucket, gamma, vega), limit utilization, exposure summary by book (FTR / power / gas) and by key dimension (hub, tenor, path). Optionally: 1-day P&L vs VaR (backtest), stress scenario results. | Align with **trading and risk limits** (daily limits, intraday decisions). Data: **T+0** or **T-1** positions and curves; run early morning so pack is available before market open or by agreed cutoff. |
| **Weekly** | **P&L attribution** (curve, vol, theta, new trades, residual) by book and optionally by product; **risk trend** (VaR and key Greeks over the week); **limit utilization** summary; **concentration** (top exposures). Optional: weekly VaR backtest, scenario comparison. | Deeper **explain** than daily; supports **weekly** risk meetings and trading review. Data: week’s position and curve history; run after week close (e.g. Monday AM for prior week). |
| **Monthly** | **Portfolio summary:** exposure and composition (notional, delta) by book and product; **month-end** VaR and Greeks; **monthly P&L attribution** and reconciliation to trading P&L; **stress** and **scenario** summary. Optional: marginal/component VaR, correlation matrix, model or curve change log. | Align with **month-end** close, **margin**, and **management** reporting. Data: month-end positions and curves; run after books and curves are finalized (e.g. first business days of next month). |
| **Quarterly** | **Quarterly risk report:** same as monthly but with **quarterly** P&L attribution, **trend** (VaR, exposure, limits over the quarter), **model/methodology** summary, **limit and mandate** compliance. Optional: capital/regulatory metrics if applicable, longer-horizon stress. | Board, **regulatory**, or **investor** reporting; strategic risk review. Data: quarter-end positions, curves, and history; run after quarter close. |

**Process (data → run → validate → distribute)**

1. **Data readiness**  
   **Inputs:** Positions (FTR, power, gas) as of the **report date**; **curves** (power hub/location, gas hub/basis, FTR spread or proxy); **vol surfaces** (for options); **discount curve**. Define **cutoff** (e.g. positions as of 6pm previous day for daily). Ensure data is **sourced** from agreed systems (risk, trading, data lake) and **versioned** (as-of date, curve ID). **Dependencies:** If curves or positions are late, define **fallback** (e.g. use prior day curve with a flag) and **escalation**.

2. **Run**  
   **Valuation** and **risk** engine: MTM, Greeks, VaR (historical or MC), stress. Use the **same** logic and code as production risk so numbers are **consistent**. For **attribution** (weekly/monthly/quarterly), run P&L decomposition (curve, vol, theta, new trades, residual). **Automation:** Trigger runs via **scheduler** (cron, Airflow, or internal job runner) at a fixed time after data is expected. **Idempotency:** Re-running with same inputs should yield same outputs; log **run ID**, **timestamp**, and **input versions**.

3. **Validate**  
   **Sanity checks:** VaR and Greeks within expected range (e.g. vs previous run or vs limits); no NaN or missing buckets; **reconciliation:** attributed P&L ≈ actual P&L (residual within tolerance). **Alerts:** If checks fail, **notify** owners and **block** or **flag** distribution until resolved. **Audit trail:** Store **run metadata** (inputs, outputs, checks passed/failed) so any report can be reproduced and explained.

4. **Distribute**  
   **Artifacts:** Pack (PDF/Excel), dashboard link, or both. **Recipients:** Risk, trading, management (and compliance/ops if required) per cadence. **Channel:** Email, shared drive, portal (Power BI, internal dashboard). **Versioning:** Report should **state** report date, as-of date, run time, and data versions (e.g. “Curves as of 2025-03-06, positions as of 2025-03-05 18:00”). So readers know exactly what the numbers represent.

**Ownership and SLAs**

- **Owner:** One team or role **owns** each cadence (e.g. Risk owns daily and weekly; Risk + Finance own monthly and quarterly). Owner is responsible for **process** (data, run, validate, distribute), **SLAs**, and **escalation** when data or runs fail.
- **SLAs:** Define **delivery time** (e.g. daily pack by 8am; weekly by Monday 10am; monthly by D+3; quarterly by D+5). Define **data cutoff** and **run window** so that SLA is achievable. Publish SLAs and track **on-time** rate; review misses and improve data or run time.
- **Escalation:** If data is missing or run fails, **notify** data providers and report owner; **fallback** (e.g. prior day) or **delay** with communication to stakeholders. Document **incidents** and **root cause** so the process can be hardened.

**Automation and tooling**

- **Scheduling:** Use a **scheduler** (cron, Airflow, Prefect, or vendor) to trigger **data pull** → **risk run** → **report build** → **validate** → **distribute** in sequence. **Dependencies:** Daily run depends on “positions and curves loaded”; weekly depends on “week-end data finalized.” **Retries:** Auto-retry failed steps (e.g. 2 retries with backoff) and alert on final failure.
- **Report build:** Generate **static** packs (PDF/Excel) from templates with **parameterized** date and run ID; or **refresh** dashboards (Power BI, Dash) from the same output database so that “report” and “dashboard” show the same numbers. **Templates** ensure **consistency** (same layout, same metrics) across runs.
- **Versioning and audit:** **Code** and **config** (e.g. VaR params, bucket definitions) in **version control**; **data** and **outputs** in a **versioned** store (e.g. by report date and run ID). So “daily pack as of 2025-03-06” can be **reproduced** from code + data at that version. Required for **audit** and **dispute** resolution.

**Summary**

Define **what** to report at each cadence (daily: risk pack; weekly: attribution + trend; monthly: portfolio summary + attribution; quarterly: full risk report + trend). Build a **process**: (1) **Data** readiness with cutoff and versioning; (2) **Run** (valuation + risk + attribution) automated and idempotent; (3) **Validate** (checks, reconciliation, alerts); (4) **Distribute** (artifacts + metadata). Assign **ownership** and **SLAs**; use **scheduling** and **templates** for reliability and consistency; keep **versioning** and **audit** so every report is reproducible.

### Tooling experience: Streamlit, Dash, Power BI

- **Streamlit:** Python-based; rapid prototyping of **interactive** apps (dropdowns, date pickers, filters). Good for **ad-hoc** and **internal** risk/P&L views: connect to DataFrames or APIs, add simple caching and reruns. Suits **quant/risk** users who prefer Python and want to iterate quickly; less suited to pixel-perfect, enterprise-wide reporting without extra layout and access control.
- **Dash (Plotly):** Python (or R); **reactive** dashboards with callbacks, more control over layout and interactivity than Streamlit. Good for **periodic** or **shared** dashboards (risk, P&L attribution) that need dropdowns, multi-page structure, and export. Fits into a Python stack; deployment (e.g. Dash Enterprise or internal server) for scheduled refresh and user access.
- **Power BI:** Enterprise **BI** tool; strong for **scheduled** reports, **distribution** to many stakeholders, and **governance** (data models, row-level security, refresh schedules). Good for **portfolio** and **P&L** packs that need a consistent look, drill-through, and integration with Excel/SharePoint/Teams. Data typically fed from warehouses or APIs; less flexible than code-first (Streamlit/Dash) for one-off or highly custom quant logic unless embedded or extended with custom visuals/DAX.
- **How to speak to it:** “I’ve built and extended risk and P&L reporting using **Streamlit** and **Dash** for interactive, Python-based dashboards (risk analysis, attribution, portfolio views) and **Power BI** for periodic, standardized reporting and broader distribution. I’m comfortable supporting both **scheduled** reporting and **ad-hoc** requests by keeping data and metrics modular so we can slice by book, period, or dimension without duplicating logic.”

### Interview angles

- **Improving existing tools:** “I’d start by mapping current data flow and report logic, then identify bottlenecks (run time, manual steps) and gaps (missing breakdowns, hard-to-audit assumptions). I’d extend incrementally—e.g. add a new attribution bucket or a new risk view—and refactor for reuse so ad-hoc and periodic reports share the same definitions.”
- **Periodic vs ad-hoc:** “Periodic reporting needs automation, versioning, and clear SLAs. Ad-hoc needs parameterized or modular design so we can answer new questions quickly; where a one-off view becomes recurring, I’d promote it into the standard tooling and schedule.”
- **Stack choice:** “Streamlit/Dash when the primary users are quants/risk and we need fast iteration and Python-native logic; Power BI when we need enterprise distribution, governance, and a stable, repeatable layout for senior stakeholders.”

---

## 3. Stress testing: methodologies, procedures, and analysis of results

**Bullet:** Develop methodologies and procedures to conduct historical and hypothetical stress testing, as well as analysis of the results using standardized statistical metrics.

### Scope (stress testing only; no repetition of VaR/ES/risk metrics above)

Section 1 defines **risk metrics** (VaR, ES, Greeks, stress as one of them). Here the focus is **how** to design, run, and **analyze** stress tests: **historical** (replay past events on current or past portfolio) and **hypothetical** (defined scenarios). Results are summarized with **standardized statistical metrics** so that scenarios are comparable and auditable.

### Historical stress testing

**What it is:** Apply **past** market moves (or past **realized** factor paths) to the **current** portfolio (or to the portfolio as it was at a past date) and compute **P&L** (and, if needed, margin) that would have occurred. No new scenario design — the scenario **is** history.

**Methodology and procedures**

- **Choice of historical period:** Define **which** dates or events to replay (e.g. Aug 2020 heat wave, Feb 2021 cold snap, a specific congestion event, or a rolling window of worst N days). **Procedure:** Maintain a **library** of named historical periods (start/end date, description, which factors are applied).
- **Factor alignment:** **Risk factors** in the stress must match the **valuation** model: e.g. power hub curves, gas hub and basis curves, FTR path spreads (or proxy). **Procedure:** For each historical date, **reconstruct** or **load** curves and vol as of that date; apply **same** shocks that actually occurred (e.g. day-over-day or period-over-period move). For **FTR**, use **realized** DAM spreads or **historical** MTM change if no liquid series.
- **Portfolio:** Either **current** portfolio (what would happen if that history repeated today) or **stale** portfolio (as of the historical date) for backtest. **Procedure:** Document which portfolio is used; current is more relevant for limit/capital, stale for backtest.
- **Valuation:** Revalue portfolio at the **stressed** factor levels (e.g. curves as of the stress date). **Procedure:** Same valuation engine as production; run in batch; store **stressed P&L** and, if required, **stressed margin**.
- **Output:** **P&L** (and optional margin) per historical scenario; **comparison** across scenarios (see analysis below).

**FTR / power / gas specifics:** Historical power and gas **curves** and **vol** may be available from data providers or internal history; **FTR** path spreads often require **nodal/DAM** history or **proxy** (e.g. hub spread). Document **data source** and **coverage** (which paths, which hubs) per scenario.

### Hypothetical stress testing

**What it is:** Apply **defined** (what-if) shocks to risk factors — e.g. power hub +$X/MWh, gas +$Y/MMBtu, vol +Z%, FTR path spread ±W — and compute P&L and margin. Scenarios are **designed**, not replayed from history.

**Methodology and procedures**

- **Scenario definition:** Each scenario has a **name**, **description**, and **shock specification** (per factor or per bucket). Examples: "Power spike" (ERCOT North +$50/MWh all tenors), "Gas winter" (Henry +$2, basis SoCal +$1), "Vol up" (parallel +10%), "FTR blow-out" (path P spread +$20/MWh). **Procedure:** Maintain a **scenario library** (parameterized); version and approve scenarios for use in limits or reporting.
- **Shock application:** **Additive** (curve +$X), **multiplicative** (vol ×1.1), or **curve replace** (replace curve with a stressed curve). **Procedure:** Define **mapping** (which risk factors are shocked how); ensure **consistency** (e.g. no-arb preserved if required).
- **Correlation in multi-factor scenarios:** If several factors are shocked (e.g. power and gas and FTR), define whether shocks are **independent** (each applied to its factor) or **joint** (e.g. same historical day's moves). **Procedure:** Document **joint** vs **single-factor** hypotheticals; joint can be derived from a **historical** day (then it bridges to historical stress).
- **Portfolio and valuation:** **Current** portfolio; revalue at **stressed** factors. **Procedure:** Same as historical — same engine, batch run, store stressed P&L and margin.
- **Output:** **P&L** (and optional margin) per hypothetical scenario; **sensitivity** (e.g. P&L per $1 move in power) if scenarios are parameterized.

**FTR / power / gas specifics:** Hypotheticals should cover **all three books**: e.g. power-only, gas-only, FTR-only (path spread shocks), and **combined** (e.g. heat wave = power up, gas up, congestion up). **Concentration** scenarios (e.g. one path or one hub blows out) support limit and liquidity discussion.

### Analysis of results using standardized statistical metrics

So that **results** of different stress runs are **comparable** and **reportable**, use a **fixed set of metrics** for each scenario (and, if relevant, across scenarios).

**Suggested standardized metrics (per scenario)**

| Metric | Definition | Use |
|--------|------------|-----|
| **Stressed P&L** | Portfolio P&L (or P&L by book) when factors are set to the stress level. Signed (negative = loss). | Primary outcome of the stress. |
| **Stressed P&L (% of portfolio value or of capital)** | Stressed P&L divided by a reference (e.g. current MTM or regulatory capital). | Scale-independent comparison across portfolios or time. |
| **Max loss (min P&L)** | $\min_{\text{scenarios}} \text{P\&L}$ if multiple sub-scenarios (e.g. several historical dates). | Worst case in the set. |
| **Mean shortfall (average loss)** | Average of P&L over scenarios where P&L &lt; 0 (or over all scenarios if all are losses). | Expected loss in stress set. |
| **Percentile (e.g. 95th)** | 95th percentile of P&L across scenarios (if many scenarios, e.g. rolling historical). | Tail of the stress distribution. |
| **Contribution by book** | Stressed P&L broken down by FTR, power, gas. | Which book drives the result. |
| **Margin impact** | Change in IM/VM or collateral call under stress (if computed). | Liquidity and collateral planning. |

**Procedures for analysis**

- **Report card per run:** Each stress run (historical or hypothetical) produces a **standard table**: scenario name, stressed P&L (total and by book), stressed P&L %, max loss if applicable, mean shortfall if applicable, percentile if applicable, margin impact if applicable. **Procedure:** Template or schema so every run is reported the same way.
- **Comparison across scenarios:** Rank or compare scenarios by **stressed P&L** (or by **stressed P&L %**). **Procedure:** Summary table or dashboard: scenario × metrics; highlight **worst** scenarios for management.
- **Trend over time:** If stress is run **periodically** (e.g. monthly) with the **same** scenario set, track **stressed P&L** (and metrics) over time. **Procedure:** Time series of key metrics per scenario; explains whether the book has become more or less stressed.
- **Sensitivity:** For **hypothetical** scenarios with parameters (e.g. power +$X), report **P&L per unit** (e.g. per $1/MWh) or a **small grid** of X values. **Procedure:** Standard sensitivity output (table or chart) for key hypotheticals.

**Statistical nuance**

- **Historical** stress with **many** dates (e.g. rolling 1-year of daily moves) yields a **distribution** of stressed P&L; then **percentile**, **mean shortfall**, and **max loss** are natural. **Hypothetical** stress with **few** scenarios (e.g. 5–10 named scenarios) yields one number per scenario; **max** and **mean** across those; **percentile** less meaningful unless scenarios are sampled (e.g. Monte Carlo over shock size).
- **Standardized** means the **same** metrics are **always** reported (same names, same definitions) so that governance and limits can refer to "stressed P&L" or "95th percentile stressed P&L" unambiguously.

**Important metrics from hypothetical stress testing (with formulas)**

For **hypothetical** stress, each scenario $s$ is a **defined shock** (or vector of shocks) applied to risk factors; we revalue the portfolio at the stressed factors and optionally recompute margin. Below, $V_0$ = portfolio value (MTM) at **current** factors, $V_s$ = portfolio value at **stressed** factors under scenario $s$, and $\mathcal{S}$ = set of scenarios (e.g. a small list of named scenarios, or a parameterized grid).

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Stressed P&L** (single scenario $s$) | $\mathrm{P\&L}_s = V_s - V_0$ | Dollar gain/loss if the shock in scenario $s$ occurred. **Negative** = loss. |
| **Stressed P&L (% of MTM)** | $\mathrm{P\&L}_s^{\%} = \frac{V_s - V_0}{\lvert V_0 \rvert}$ or $\frac{V_s - V_0}{V_0}$ (if $V_0 > 0$) | Scale-independent; compare across portfolios or time. Often reported as **percentage of current MTM** (or of capital). |
| **Stressed P&L (% of capital)** | $\mathrm{P\&L}_s^{\%,\mathrm{cap}} = \frac{V_s - V_0}{K}$ | $K$ = regulatory or economic **capital**. Shows stress loss as a **share of capital**. |
| **Max loss** (across scenarios) | $\mathrm{MaxLoss} = \min_{s \in \mathcal{S}} \mathrm{P\&L}_s = \min_{s \in \mathcal{S}} (V_s - V_0)$ | Worst **hypothetical** outcome in the scenario set. Used for **limits** and **liquidity** (e.g. max loss must not exceed X). |
| **Mean shortfall** (across loss scenarios) | $\mathrm{MS} = \frac{1}{\lvert \mathcal{S}_- \rvert}\sum_{s \in \mathcal{S}_-} \mathrm{P\&L}_s$, where $\mathcal{S}_- = \{ s : \mathrm{P\&L}_s < 0 \}$; if $\mathcal{S}_-$ is empty, MS = 0 or N/A. | **Average loss** over scenarios that produce a loss. If all scenarios are losses, MS = mean of all $\mathrm{P\&L}_s$. |
| **Contribution by book** | $\mathrm{P\&L}_{s,\mathrm{FTR}} = V_{s,\mathrm{FTR}} - V_{0,\mathrm{FTR}}$, and similarly for power and gas; $\mathrm{P\&L}_s = \mathrm{P\&L}_{s,\mathrm{FTR}} + \mathrm{P\&L}_{s,\mathrm{power}} + \mathrm{P\&L}_{s,\mathrm{gas}}$. | **Which book** (FTR, power, gas) drives the stressed P&L. Sum of contributions = total stressed P&L. |
| **Margin impact** | $\Delta M_s = M_s - M_0$ | $M_0$ = current **initial margin** (or VM/collateral); $M_s$ = margin under stressed factors. **Liquidity** need in stress. |
| **Sensitivity** (P&L per unit shock) | For a **parameterized** scenario (e.g. power curve $+\delta$ \$/MWh): $\frac{\partial \mathrm{P\&L}}{\partial \delta} \approx \frac{V_{s,\delta+h} - V_{s,\delta}}{h}$ or $\frac{V_{s,\delta} - V_0}{\delta}$ (one-sided). | **Dollar P&L per unit** of shock (e.g. per \$1/MWh, per \$1/MMBtu). Linear approximation; useful for small shocks or for ranking factors. |

**Notation (compact):**
- $V_0$ = value at **current** curves/vol; $V_s$ = value at **stressed** curves/vol in scenario $s$.
- **Stressed P&L** = $V_s - V_0$ (loss if negative).
- **Max loss** = $\min_s (V_s - V_0)$ over the scenario set.
- **Mean shortfall** = average of $(V_s - V_0)$ over scenarios with $V_s - V_0 < 0$.

If you run **many** hypothetical scenarios (e.g. a grid of shock sizes), you can also report **percentiles** of stressed P&L (e.g. 95th percentile loss) and **distribution** statistics; the formulas above are the core set for a **finite list** of named hypothetical scenarios.

### End-to-end process

1. **Library:** Maintain **historical** periods and **hypothetical** scenario definitions (versioned, approved).
2. **Run:** For each scenario, **load** portfolio and factors, **apply** shock (historical or hypothetical), **revalue**, **compute** margin if needed.
3. **Compute metrics:** For each scenario, fill the **standard** table (stressed P&L, %, max, mean, percentile, by book, margin).
4. **Report:** **Report card** per run; **comparison** across scenarios; **trend** if repeated; **sensitivity** for parameterized hypotheticals.
5. **Review:** Use results for **limits** (e.g. max stressed P&L), **capital**, **liquidity**, and **management** communication; **update** scenarios periodically (new events, new risk factors).

### Interview angles (stress testing)

- **Historical vs hypothetical:** "Historical uses actual past moves so we see what would have happened; hypothetical lets us design tail events (e.g. power $100, gas $5) that may not have occurred. We use both — historical for validation and context, hypothetical for limits and liquidity."
- **Standardized metrics:** "We report every stress run with the same set: stressed P&L, P&L %, max loss, mean shortfall, contribution by book, margin impact. That way we can compare across scenarios and over time and satisfy governance with one definition."
- **Procedure:** "We keep a scenario library (historical periods and hypothetical shocks), run through the same valuation engine, and produce a standard report card. So the process is repeatable and auditable."

---

## 4. Configuring and calibrating risk systems (with Risk Management)

**Bullet:** Work with Risk Management to configure and calibrate risk systems.

### Scope (configuration and calibration; no repetition of model or reporting detail above)

Sections 1–3 cover **what** the risk models and reports do. Here the focus is **how** risk **systems** are **set up** (configure) and **tuned** (calibrate), and **how** the quant/research role **works with Risk Management** so that systems are aligned with policy, limits, and governance.

### Configuring risk systems

**What “configure” means:** Define the **inputs**, **parameters**, **limits**, and **outputs** of the risk platform so that it runs consistently and produces numbers Risk can use for limits, capital, and reporting.

- **Data and inputs:** **Position** sources (FTR registry, power/gas trading system, data lake); **curve** and **vol** feeds (vendor, internal build, or hybrid); **cutoff** times and **as-of** dates. Risk and research agree on **which** systems are authoritative and how often data is refreshed (e.g. T+0, T-1).
- **Risk factors and buckets:** **Which** factors drive VaR and Greeks (e.g. power hub × tenor, gas hub + basis × tenor, FTR path spread or proxy). **Bucket** definitions (e.g. tenors, regions) so that limits and reporting are consistent. Configure **mapping** (e.g. path → proxy hub for FTR) and document assumptions.
- **Parameters:** **VaR** method (historical vs Monte Carlo), **confidence** (e.g. 99%), **horizon** (e.g. 1-day), **lookback** (e.g. 2 years). **Stress** scenario set and refresh rules. **Discount** curve and any rate inputs. Risk signs off on these so limits and capital are based on the same config.
- **Limits and thresholds:** **Limit** definitions (e.g. VaR limit, delta limit by bucket, notional by path) and **alert** thresholds. Configure **where** limits are stored and how **breaches** are flagged and escalated.
- **Outputs and reporting:** **Report** definitions (daily pack, weekly attribution, etc.), **recipients**, and **distribution**. Ensure risk systems feed the same numbers into Risk’s dashboards and packs (Section 2).

**Procedure:** Maintain a **config** (file, DB, or parameter store) that is **versioned** and **reviewed** with Risk. Changes (e.g. new bucket, new lookback) go through **change control** and Risk sign-off.

### Calibrating risk systems

**What “calibrate” means:** Choose or **estimate** the **parameters** that the models need — so that VaR, stress, and Greeks are **well calibrated** (e.g. backtest passes, stress scenarios are plausible) and **agreed** with Risk.

- **VaR calibration:** **Lookback** length and **confidence** (e.g. 99%, 1-day). **Historical** VaR: same history and same portfolio convention (hypothetical vs realized). **Monte Carlo:** **vol** and **correlation** (and, if used, **copula** or **factor** model). **FTR proxy** (e.g. MTM series or congestion proxy) and its **mapping** to the portfolio. Calibrate so that **backtest** (exception rate, magnitude) is acceptable to Risk; if not, adjust lookback, proxy, or method and re-validate.
- **Volatility:** **Vol surfaces** (power, gas) — implied vol from market where available; **proxy** or **historical** for illiquid locations. **Term structure** and **smile** assumptions. Risk may require **conservative** or **stressed** vol for certain books. **Calibration** = choice of source (broker, internal, historical) and any **scaling** or **floors**; document and agree with Risk.
- **Correlation:** **Correlation** (and, if applicable, **copula**) across FTR, power, gas (and across tenors). Estimate from **historical** P&L or factor returns; **FTR proxy** drives correlation with power/gas. **Stress** correlation (e.g. higher in crisis) if used. Calibrate so **portfolio** VaR and **diversification** are reasonable; Risk may require **sensitivity** or **stressed** correlation for limit purposes.
- **Curves and marks:** **Curve** build (power, gas, FTR spread) — methodology and **inputs** (Section 1). “Calibrate” here means **align** with Risk on **which** curves feed risk (e.g. same as trading, or risk-specific) and **how** often they are updated. **Mark** vs **risk** consistency (same curves and vol in both) so that P&L explain and backtest are meaningful.
- **Stress scenarios:** **Historical** and **hypothetical** scenario set (Section 3). Calibrate = **define** shocks (e.g. power +$X, gas +$Y) and **refresh** (e.g. quarterly) with Risk input. **Standardized metrics** (stressed P&L, max loss, etc.) are part of the config.

**Procedure:** **Calibration** is **documented** (parameter set, data window, assumptions). **Backtest** and **sensitivity** (e.g. VaR vs lookback, vs correlation) are run and **reviewed** with Risk. **Approval** of calibration (or changes) sits with Risk; research supports with analysis and implementation.

**Instances where the risk system may need calibration (FTR, power, gas)**

Concrete situations in which **configuration or calibration** of the risk system is needed, by asset class.

**FTR**

- **FTR proxy for VaR / correlation:** There is **no liquid price series** for most FTR paths. The risk system needs a **proxy** (e.g. daily change in CRR portfolio MTM, or a congestion/LMP-spread index) to build **historical** or **simulated** returns for VaR and correlation. **Calibration** = choice of proxy, **mapping** (which paths use which proxy), and **scaling** (e.g. vol scale factor if the proxy is more or less volatile than the book). If **backtest** fails (e.g. too many VaR exceptions) or the portfolio mix changes, **re-calibrate** the proxy or the mapping.
- **Spread curve and mark consistency:** FTR marks depend on **path spread curves** (or nodal/scenario model). **Calibration** = which **curve build** (e.g. congestion model, historical DAM spreads, hub proxy + basis) feeds **risk** and whether it is the **same** as the curve used for **mark**. If Risk and trading disagree on marks, or if the curve methodology changes, **re-configure** or **re-calibrate** so risk and P&L are consistent.
- **Volatility for optional FTR:** PTP **options** (and any spread options on FTR) need **spread vol** (or vol of the proxy). There are typically **no liquid options** on most paths. **Calibration** = **historical** vol of the spread (or proxy), or **scaled** from a liquid hub; **term structure** and **smile** assumptions. Re-calibrate when **option book** grows or when **realized** vol diverges from assumed.
- **Settlement and horizon:** FTR settles on **DAM** over the contract period (e.g. monthly). **Calibration** = **horizon** (1-day vs remaining-days-in-month) and **P&L definition** (mark change vs hypothetical) for VaR and backtest. Align with Risk on whether **intramonth** (e.g. DART, remaining days) is in scope and how it is calibrated.

**Power**

- **Vol surface (hub and location):** **Implied vol** is observable at **major hubs** (e.g. ERCOT North, PJM West); **other locations** and **long tenors** often have **no** or **thin** option markets. **Calibration** = **hub** vol (market or smoothed) and **location** vol (proxy: e.g. scale from hub by historical vol ratio, or assume same smile in moneyness). **Term structure** (short vs long dated) and **smile** (e.g. SABR $\beta$, $\nu$, $\rho$) need to be set and refreshed. Re-calibrate when **option book** or **tenor mix** changes, or when **market** vol regime shifts.
- **Asian / vol of average:** Many power options settle on **average** price. **Calibration** = **vol of the average** (or term structure of “vol of average” vs “vol of spot”) for the relevant delivery period. Often **derived** from spot vol and averaging; re-calibrate when **Asian** book grows or when **realized** vol of average diverges.
- **Correlation (DAM vs RT, hub vs location):** **Portfolio** VaR and **diversification** depend on **correlation** between power tenors, hubs, and (if in scope) **DAM vs RT** or **peak vs off-peak**. **Calibration** = **historical** correlation from returns or P&L; **stressed** correlation if required by policy. Re-calibrate when **correlation** structure changes (e.g. renewables, new interconnects) or when **backtest** suggests under-/over-stated diversification.
- **Curve and basis:** **Forward curve** (hub, location) and **basis** feed delta and VaR. **Calibration** = which **curve** (broker, internal, blended) and **update** frequency; **basis** vol and correlation with hub if basis is a separate factor. Re-configure when **curve** source or methodology changes.

**Gas**

- **Hub and basis vol:** **Henry Hub** (and major hubs) may have **liquid** option quotes; **basis** (location − Henry) and **non-hub locations** often do not. **Calibration** = **hub** vol surface (market or historical) and **basis** vol (historical, or scaled from hub). **Term structure** (prompt vs strip) and **seasonality** (winter vs summer vol) need to be set. Re-calibrate when **option** or **basis** book changes, or when **vol regime** (e.g. winter spike) is not reflected.
- **Correlation (hub, basis, power):** **Portfolio** VaR and **stress** depend on **correlation** between gas hub, **basis** (by location), and **power** (e.g. spark spread). **Calibration** = **historical** correlation (from returns or P&L); **stressed** correlation for stress tests. Re-calibrate when **correlation** (e.g. gas–power) shifts or when **backtest** or **stress** results suggest the joint model is off.
- **Storage and swing:** **Storage** and **swing** optionality are valued with **forward curve** and **vol** (and often a **spread** or **inventory** model). **Calibration** = **vol** and **correlation** (e.g. prompt vs forward) used in the storage model; **constraints** (inject/withdraw limits, ramp). Re-calibrate when **storage** book or **realized** storage P&L vs model diverges.
- **Curve and basis curves:** **Gas forward** (hub + basis by location) feeds delta and VaR. **Calibration** = **curve** source and **basis** methodology; **consistency** with marks. Re-configure when **curve** build or **basis** quotes change.

**Cross-asset and platform**

- **Correlation (FTR, power, gas):** **Portfolio** VaR and **diversification** depend on **joint** correlation across the three books. **Calibration** = **full** correlation matrix (or factor/copula) and **FTR proxy** correlation with power and gas. Re-calibrate when **backtest** (e.g. too many joint exceptions) or **stress** suggests the joint model is mis-specified.
- **VaR lookback and confidence:** **Historical** VaR uses a **lookback** (e.g. 2 years); **confidence** (e.g. 99%) is a **config** choice. **Calibration** = whether lookback is **appropriate** (e.g. include or exclude a crisis period) and whether **confidence** matches **limit** and **capital** definitions. Re-visit when **regime** changes or when **backtest** fails.
- **Stress scenario set:** **Hypothetical** and **historical** stress scenarios (Section 3) are **calibrated** in the sense of **which** scenarios and **what** shock sizes. Re-calibrate (refresh scenarios, add new events) **periodically** or when Risk **policy** or **limits** change.

### Working with Risk Management

- **Governance:** Risk **owns** risk limits, **capital** usage, and **regulatory** or internal **policy**. Research/quants **implement** and **maintain** the systems that produce the numbers. **Configure** and **calibrate** jointly: Risk defines **what** is needed (e.g. “VaR at 99%, 1-day, with FTR in scope”); research **how** (data, model, buckets) and **proposes** config and calibration for Risk approval.
- **Validation:** Risk (or a dedicated **model validation** function) **validates** model changes and calibration. **Backtest** results, **stress** output, and **sensitivity** to parameters are reviewed. **Sign-off** before a new config or calibration goes live.
- **Documentation:** **Config** and **calibration** are **documented** (assumptions, data sources, parameter choices, limitations). So Risk and auditors can **understand** and **challenge** the numbers. **Change log** when parameters or config change.
- **Ongoing:** **Monitor** backtest and **stress** results; **tune** (e.g. adjust lookback or vol) if policy or market regime changes. **Re-calibrate** periodically (e.g. quarterly) and when **new** products or books are in scope. Keep Risk informed of **material** changes and **issues** (e.g. backtest breach, data break).

### Risk management policy change

**What counts as a policy change:** A **risk management policy change** is a change in **how** risk is defined, **measured**, **limited**, or **reported** — decided by Risk (and, where relevant, by regulation or the board). Examples: new or revised **limit** type (e.g. add vega limit, change VaR confidence from 95% to 99%); change in **scope** (e.g. include FTR in VaR, add intramonth power VaR); new **stress** scenario set or **capital** rule; change in **reporting** (e.g. new metric, new frequency, new recipient); **regulatory** or **internal** mandate (e.g. ES in addition to VaR, different lookback). Policy drives **what** the risk system must produce; config and calibration implement it.

**How policy change affects the risk system**

- **Configuration:** Policy may require **new** or **changed** config: e.g. new **limit** definitions (and where they are stored), new **buckets** (e.g. limit by congestion zone), new **report** or **dashboard**, or a **different** data cut (e.g. include bilateral FTR). **Configure** the system to reflect the new policy (parameters, limits, outputs).
- **Calibration:** Policy may require **re-calibration**: e.g. **confidence** level (99% vs 95%) or **horizon** (1-day vs 10-day) for VaR; **stress** scenario set; **correlation** or **vol** assumptions (e.g. stressed correlation for limits). **Calibrate** so that the system’s outputs match the new policy (e.g. VaR at new confidence, stress with new scenarios).
- **Limits and thresholds:** Policy often **sets** or **changes** limit levels (e.g. VaR cap, delta limit by book). The risk system must **read** and **apply** these limits; **alerts** and **escalation** must align with the new policy. Config update (and sometimes calibration, if limits are derived from risk metrics).
- **Reporting and governance:** Policy may require **new** reports, **new** metrics, or **new** distribution. **Reporting** config (Section 2) and **governance** (approval, sign-off) are updated to match.

**Procedure when policy changes**

1. **Capture and document:** Risk **documents** the policy change (what changed, why, effective date). Research understands **what** the system must do **after** the change (e.g. “VaR at 99%, 1-day; FTR in scope; new stress set X”).
2. **Impact assessment:** Identify **config** changes (limits, buckets, reports, data) and **calibration** changes (VaR params, vol, correlation, stress). Assess **effort** (build, test, deploy) and **dependencies** (data, vendor, validation).
3. **Implement:** Update **config** and **calibration** in the risk system; **test** (e.g. run VaR with new params, run stress with new scenarios, check limits and reports). **Version** config and document the change.
4. **Validate:** Risk (or model validation) **validates** that the system now **implements** the policy (e.g. VaR at 99%, correct stress metrics). **Sign-off** before go-live.
5. **Communicate and train:** **Stakeholders** (trading, management, ops) are informed of the change (e.g. “VaR is now 99%; new stress report as of date X”). **Training** or **runbooks** if behavior or reports change materially.
6. **Effective date and cutover:** Policy change has an **effective date**. **Cutover** (e.g. switch to new VaR config, new limits) is coordinated so that **old** and **new** numbers are not mixed; **history** (e.g. backtest, trend) may need a **bridge** (e.g. restate prior period with new method for comparison) if required by policy.

**Examples (FTR, power, gas)**

- **“FTR in scope for VaR”:** Policy change = FTR is now included in **portfolio** VaR. **Config:** Add FTR positions and **FTR proxy** (or MTM series) to the risk engine; add FTR to **limit** and **report** definitions. **Calibration:** Choose and **calibrate** FTR proxy and **correlation** with power/gas; **backtest** once FTR is in scope. **Validate** with Risk; go-live on effective date.
- **“New stress scenario set”:** Policy change = **replace** or **extend** the hypothetical/historical stress set (e.g. add “heat wave” and “cold snap” scenarios). **Config:** Update **scenario library**; **Calibration:** Define shock sizes and apply to portfolio; **reporting:** ensure **standardized metrics** (Section 3) are produced for new scenarios. **Validate** and publish new report.
- **“Vega limit by book”:** Policy change = **new** limit type: **vega** limit per book (FTR, power, gas). **Config:** Add vega **limit** definitions and **alert** logic; **reporting:** add vega by book to daily pack and limit-utilization view. **Calibration:** May need **vega** by book to be **stable** (e.g. sticky-delta convention); no change to VaR calibration unless policy links capital to vega.
- **“ES in addition to VaR”:** Policy change = **report** Expected Shortfall (ES) as well as VaR (e.g. for capital or regulatory). **Config:** Add ES to **output** and **reports**; **Calibration:** same as VaR (ES uses same P&L distribution); **validate** that ES is produced and used as policy requires.

**Summary:** Policy change = Risk (or regulation) changes **what** risk is measured, limited, or reported. The risk system must **configure** (limits, buckets, reports) and **calibrate** (params, scenarios) to **implement** the new policy; **validate** and **communicate**; **cutover** on effective date. Working with Risk ensures the system stays aligned with policy.

### Interview angles

- **Configure vs calibrate:** “Configure is **what** the system uses — data sources, buckets, limits, report definitions. Calibrate is **setting** the model parameters — VaR lookback, vol, correlation, stress scenarios — so the outputs are well calibrated and agreed with Risk.”
- **Working with Risk:** “I work with Risk to agree on **requirements** (e.g. confidence level, scope of FTR/power/gas), then **propose** config and calibration and **implement** in the risk system. Risk **validates** and **approves**; we **document** and **version** so changes are traceable. Ongoing, we **monitor** backtest and stress and **re-calibrate** when needed or when Risk policy changes.”
- **Policy change:** “When Risk **policy** changes — e.g. new limits, FTR in VaR, new stress set, or regulatory change — we **assess** what config and calibration must change, **implement** and **test**, then **validate** with Risk and **cut over** on the effective date. Policy drives **what** the system does; we keep config and calibration **aligned** with policy and document the change.”

---

## 5. Apply quantitative methods to solve risk topics (market liquidity, liquidation costs)

**Bullet:** Apply quantitative methods to solve risk topics, such as estimating market liquidity and liquidation costs.

### Scope

Sections 1–4 cover **risk models**, **reporting**, **stress testing**, and **config/calibration**. Here the focus is **applying quantitative methods** to **specific risk topics** that require modeling and estimation — in particular **market liquidity** (how easily positions can be traded without moving the market) and **liquidation costs** (cost to unwind positions, including in stress). These feed into **liquidity-adjusted risk** (e.g. LVaR), **limit setting**, **capital**, and **crisis planning**.

### Estimating market liquidity

**What “market liquidity” means:** The ability to **trade** a given size at a given **speed** without moving the price too much. Dimensions: **tightness** (bid-ask spread), **depth** (size available at/near the quote), **resilience** (how quickly the book refills after a trade), **immediacy** (how fast you can execute). For risk we care about: **how much** we can sell (or buy) over a horizon and at **what cost**, especially in **stress** when liquidity is thin.

**Quantitative approaches to estimate liquidity**

- **Bid-ask and spread:** **Quoted spread** (ask − bid) and **effective spread** (realized execution price vs mid) measure **immediate** cost of a small trade. **Time-series** of spread (level, volatility) by product and venue; **stress** = spread widening (e.g. 2× or 5× normal). **FTR/power/gas:** Many products are **OTC** or **thin**; use **broker quotes**, **historical** spread, or **proxy** (e.g. spread of a liquid hub or index).
- **Depth and volume:** **Order-book depth** (cumulative size at each price level) and **daily volume** (turnover) indicate **how much** can be traded per day without excessive impact. **Depth decay** (how depth falls as you move away from mid) and **volume concentration** (few large trades vs many small) matter for **block** unwinds. For **illiquid** paths or tenors, depth may be **model-based** (e.g. from historical fill data or expert assumption).
- **Market impact (price impact):** **Temporary** impact (price moves during the trade, partly reverts) and **permanent** impact (price level shift). Often modeled as **power law** in **size**: e.g. impact ∝ (Q / V)^α where Q = order size, V = typical volume (e.g. daily), α ∈ [0.5, 1]. **Square-root** (α ≈ 0.5) is a common empirical choice. **Calibration:** from **historical** execution data (implementation shortfall, VWAP slippage) or from **order-book** models.
- **Liquidity-adjusted VaR (LVaR):** VaR assumes positions can be **closed at mid** (or at current price). **LVaR** adjusts for **spread** and **impact**: e.g. add **half-spread** to the loss side, or add **estimated cost** to unwind the position over the VaR horizon (e.g. 1 day or N days). **Holding period** may be **lengthened** for illiquid books (e.g. 10-day VaR for hard-to-sell FTR). **Formula (simple):** LVaR ≈ VaR + (spread/2) × position + impact_cost(unwind_size, horizon); or **stochastic** spread and impact in a **simulation**.
- **Funding liquidity vs market liquidity:** **Market liquidity** = ease of **trading** the asset. **Funding liquidity** = ability to **borrow** or **post collateral** to hold the position. Both can dry up in stress; **quantitative** work may include **margin** runoffs (e.g. initial margin and VM under stress), **haircuts**, and **funding** cost under stress — relevant for **liquidation** decisions and **capital**.

**What is special about market liquidity for FTR**

- **No continuous liquid market:** Unlike exchange-traded futures, most **FTR/CRR paths** do **not** have a central order book or continuous trading. Liquidity is **discrete** (auctions) or **bilateral** (OTC). You cannot “click to sell” at a screen price for an arbitrary path; you must either **wait for the next auction**, **find a counterparty** OTC, or **hold to settlement** (receive congestion payments over the delivery period).
- **Auction-based liquidity:** In ERCOT (CRRs) and PJM (FTRs), a large share of **primary** liquidity is in **periodic auctions** (e.g. monthly CRR auctions, annual/periodic FTR auctions). **Volume** and **clearing prices** are observable **only at auction dates**; between auctions there is **no** exchange-style depth or spread for most paths. **Secondary** trading is OTC or via brokers — often **path-specific** and **thin**.
- **Path-specific and highly uneven:** **Major** paths (e.g. between large hubs, high-congestion corridors) may attract more bidders and have **tighter** implied spreads (from auction clearing); **minor** or **peripheral** paths can have **zero** or **very few** participants. So **liquidity is path-dependent**: some paths are “tradeable” in size at reasonable cost, many are **hold-to-settlement** in practice.
- **Mark is model-based, not transaction-based:** For most paths there are **no** frequent trades to define “last” or “mid.” **Marks** come from **congestion models**, **nodal/DAM spread** proxies, or **curve builds** (e.g. hub spread + basis). **Liquidity risk** for FTR is therefore not just “wide bid-ask” but “**no reliable exit price**” — unwinding may require a **large discount** to model mark or **holding to settlement**.
- **Tenor and product type:** **Monthly** vs **seasonal** vs **annual** rights have different auction and OTC liquidity. **Options** (e.g. PTP options) vs **obligations** can have different participant bases. **DAM PTP obligations** (bought in the day-ahead market) add another layer: liquidity is tied to **DAM clearing** and **real-time cash-out**, not a secondary FTR market.
- **Implications for risk:** **Liquidity** for FTR is estimated from **auction** participation and **cleared volumes** by path/tenor; **proxy** from liquid **hub power** or **congestion** indices where path-level data is thin. **LVaR** and **liquidation cost** should assume **long** unwind horizons (e.g. to next auction or to settlement) and **significant** discount to model mark for illiquid paths; **concentration** in a **few paths** amplifies liquidity risk.

**What is specific about market liquidity for power and gas ICE (exchange) contracts**

- **ICE as the liquid benchmark layer:** **ICE** (Intercontinental Exchange) and other exchanges list **power** and **gas** **futures and options** that are the **primary liquid** instruments for many North American hubs (e.g. **Henry Hub** gas, **ERCOT North** power, **PJM West**, **NGPL TexOk**, **SoCal Gas**). These are **exchange-traded**: **central order book**, **clearing**, **daily volume**, and **transparent** bid-ask. So for **standard** hub and **standard** tenor, **market liquidity** is **good** and can be measured with **spread**, **depth**, and **volume** much like other listed derivatives.
- **Liquidity by product and tenor:** Liquidity is **concentrated** in **near-term** and **benchmark** products. **Prompt** month (and next few months) and **key seasonal** strips (e.g. winter, summer) are **most** liquid; **back months** and **exotic** strips (e.g. specific monthly peak) are **thinner**. **Power:** **Peak** vs **off-peak** vs **7×24** — liquidity varies by **shape**; **monthly** and **quarterly** are more liquid than **daily** or **custom** blocks on exchange. **Gas:** **Henry** is very liquid; **basis** contracts (e.g. SoCal, TCO, regional) are **less** liquid on ICE, often **OTC** or **thin** on screen.
- **Location and basis:** **Hub** contracts (e.g. Henry, ERCOT North) are the **liquid** core. **Location-specific** power (e.g. a specific node or zone) and **basis** gas (location − Henry) are often **OTC** or traded via **brokers** with **wider** spreads and **less** depth. So “ICE liquidity” applies **first** to **hub** futures/options; **location** and **basis** add a **second**, **less liquid** layer.
- **Options on ICE:** Listed **options on futures** (calls, puts, sometimes swaptions) exist for major power and gas products. **Liquidity** in the **vol surface** varies by **strike** and **tenor** — **ATM** and **near-term** are more liquid; **OTM** and **long-dated** can be **thin**. **Implied vol** may be **broker-quoted** or **interpolated** for illiquid strikes/tenors.
- **Settlement and cash-out:** Power and gas ICE contracts are typically **financial** (cash-settled against an **index** — e.g. ERCOT North DAM, Henry Hub spot). So **liquidity** is about the ability to **close** or **hedge** the **financial** position on the exchange; **physical** delivery is a separate (often OTC) market. **Daily** mark-to-market and **margin** mean that **funding liquidity** (margin calls) is tied to **market liquidity** (ability to reduce position if needed).
- **Implications for risk:** For **hub** ICE products, use **exchange** bid-ask, **volume**, and **depth** to estimate spread and impact; **stress** = spread widening and **reduced** depth (e.g. 2× spread, 50% depth). For **basis** and **location** power/gas, treat more like **OTC**: **broker** quotes, **historical** spread, **proxy** from hub liquidity with a **liquidity haircut** by tenor and location.

**Important power and gas contracts on ICE (reference)**

| Asset | Region / hub | Examples of liquid ICE contracts (names / concepts) |
|-------|----------------|-----------------------------------------------------|
| **Gas (US)** | **Henry Hub** | **Henry Hub** natural gas futures and options — the **benchmark** US gas contract; prompt and seasonal strips. |
| | **Basis / locations** | **SoCal Border**, **PG&E Citygate**, **Transco Zone 6 (TCO)**, **Waha**, **Chicago (NGPL)**, **TexOk** — basis vs Henry; liquidity varies (Henry most liquid). |
| **Power (US)** | **ERCOT** | **ERCOT North** (and South, West) — peak, off-peak, 7×24; monthly and seasonal; core ERCOT liquid hub. |
| | **PJM** | **PJM Western Hub**, **PJM Eastern Hub** — peak, off-peak; major Eastern power market. |
| | **ISO-NE** | **Mass Hub** (and other ISO-NE hubs) — New England power. |
| | **NYISO** | **NYISO Zone A** (NYC), **Zone J** (West) — New York power. |
| | **MISO** | **Indiana Hub**, **Michigan Hub** — Midwest. |
| | **CAISO** | **SP15**, **NP15** — California South/North; often traded OTC or on ICE as financial. |

*Exact symbols and product codes (e.g. NG for Henry, ENA for ERCOT North) are on ICE’s website; the table above is by **hub/region** for interview context. European gas (e.g. **TTF**, **NBP**) and power are also on ICE but the JD focus is US FTR, gas and power.*

### Liquidation costs

**What “liquidation cost” means:** The **total cost** (or **shortfall**) to **unwind** a position or portfolio within a given **horizon**, including **spread**, **market impact**, **timing** (urgency), and, in stress, **fire-sale** effects (prices move against you as you sell).

**Quantitative approaches**

- **Implementation shortfall:** **Theoretical** P&L (if we could trade at decision price) vs **actual** P&L after execution. **Components:** **spread** (bid-ask), **market impact** (price move from our flow), **timing** (delay cost), **opportunity** (price moved before we traded). **Data:** from **execution** records; **estimate** liquidation cost by **scenario** (e.g. “sell 100% in 1 day” vs “sell over 5 days”).
- **Market impact models:** **Almgren–Chriss** (and variants): **optimal execution** that balances **market impact** (worse if you trade fast) vs **volatility risk** (worse if you trade slow). Gives **expected cost** and **variance** of cost for a given **liquidation schedule**. **Parameters:** **temporary** and **permanent** impact (from data or assumption); **volatility**; **risk aversion**. Used to **estimate** “cost to liquidate position X over N days” and to **optimize** trade-off speed vs cost.
- **Stress liquidation / fire sale:** In **stress**, liquidity is **reduced** (wider spread, less depth) and **urgency** is high. **Liquidation cost** = **normal** impact **scaled up** (e.g. 2× or 3× impact, or 2× spread) and possibly **longer** horizon (can’t sell in 1 day). **Fire-sale** = prices move **adversely** as we sell (down for long, up for short); can model with **feedback** (our flow affects price, which affects mark-to-market). **Scenario:** “Unwind entire book in 5 days under stress” → **estimated cost** = sum over positions of (spread + impact under stress) with **convexity** (later sales worse if price has already moved).
- **Portfolio-level liquidation:** **Correlation** of liquidity across assets: when **one** book is liquidated, **other** markets may be stressed (e.g. power and gas and FTR in same crisis). **Net** liquidation cost may be **higher** than sum of single-asset costs if **joint** stress is assumed. **Concentration** in **few** names or **paths** → **higher** impact per unit.

**Use in risk:** **Liquidation cost** estimates feed into: **liquidity buffers** and **capital** (e.g. add estimated cost to worst-case loss); **limit** design (e.g. max position size such that “cost to unwind in 3 days” stays below X); **stress** reporting (“stressed liquidation cost” as a metric); **recovery** and **resolution** planning.

**Methods to analyze liquidation cost**

| Method | What it does | Data / inputs | Output |
|--------|----------------|---------------|--------|
| **Implementation shortfall decomposition** | Splits **realized** execution P&L into spread, impact, timing, opportunity cost. | **Execution** records (decision price, execution price, size, time). | **Empirical** cost per trade or per strategy; **calibration** for impact/spread. |
| **Additive spread + impact** | **Liquidation cost** = (half-spread × size) + **impact**(size, horizon). Impact from a **power law** or **linear** in size vs daily volume. | **Bid-ask**, **volume** (or proxy), **impact** parameters (from shortfall or assumption). | **Point estimate** of cost to unwind a given size over N days. Simple, transparent. |
| **Almgren–Chriss (optimal execution)** | **Optimizes** trade-off: trade **fast** → high impact, low volatility risk; trade **slow** → low impact, high vol risk. Solves for **optimal trajectory** and **expected cost** + **variance** of cost. | **Temporary** and **permanent** impact (e.g. linear in rate), **volatility**, **risk aversion** (or target horizon). | **Expected** liquidation cost and **distribution** (e.g. cost at a confidence level); **optimal** schedule. |
| **Scenario-based (fixed horizon)** | Define **unwind rule**: e.g. “sell X% per day over 5 days” or “sell 100% in 1 day.” Apply **spread** and **impact** (normal or stressed) to each slice; sum. | **Spread** and **impact** by product; **stressed** multipliers if needed. | **Scenario** liquidation cost (e.g. “5-day orderly” vs “1-day fire sale”). Good for **stress** and **limits**. |
| **Monte Carlo (stochastic spread/impact)** | **Simulate** spread and impact as **random** (e.g. spread × stress factor, impact × volume shock). Run many paths; get **distribution** of liquidation cost. | **Distributions** for spread and impact (or for stress factors); **correlation** across assets. | **Distribution** of cost (e.g. mean, 95th percentile); **LVaR**-style liquidity add-on. |
| **Stress scaling** | Take **baseline** cost (e.g. from additive or Almgren–Chriss) and **scale** spread and impact by **stress factors** (e.g. 2× spread, 2× impact, or regime-dependent). | **Baseline** liquidity parameters; **stress** multipliers (historical crisis or policy). | **Stressed** liquidation cost for **capital** or **recovery** planning. |
| **Portfolio aggregation** | **Sum** single-position costs with **correlation** or **diversification** adjustment: when one book is liquidated, others may be stressed (same time, same crisis). **Concentration** → less diversification in liquidity. | **Per-position** cost estimates; **liquidity correlation** or **joint stress** scenario. | **Portfolio** liquidation cost (e.g. sum vs “sum with correlation haircut”). |

**Summary:** Use **implementation shortfall** to **calibrate** spread and impact from real trades. Use **additive** (spread + impact) or **Almgren–Chriss** for **point** or **distribution** of cost per position. Use **scenario-based** and **stress scaling** for **limits** and **stress** reporting. Use **Monte Carlo** when you want a **full distribution**; use **portfolio aggregation** when you care about **total** book cost and **correlation** of liquidity across FTR, power, and gas.

### Other risk topics (quantitative methods)

The same **quantitative** toolkit (estimation, calibration, scenario design, optimization) applies to other risk topics, for example:

- **Concentration risk:** **Herfindahl** or **concentration** by path/hub/counterparty; **marginal** contribution to VaR or stress; **limits** on single-name or single-path exposure.
- **Counterparty and credit:** **CVA/DVA**, **potential future exposure** (PFE), **wrong-way risk**; **collateral** and **margin** modeling.
- **Model risk:** **Backtesting** (VaR, ES), **sensitivity** to assumptions (vol, correlation, proxy), **benchmark** vs alternative models.
- **Operational and execution:** **Slippage** and **execution** quality; **latency** and **timing** risk in automated or high-frequency context.

For this JD, **market liquidity** and **liquidation costs** are the **called-out** examples; the role may extend to these related areas as needed.

### Interview angles

- **Liquidity vs liquidation:** “**Market liquidity** is how easily we can trade — spread, depth, impact. **Liquidation cost** is the **cost** to actually unwind a position or book over a horizon, which depends on liquidity (spread, impact) plus **how fast** we need to sell and **stress** (liquidity can dry up). I’d estimate liquidity from spreads, depth, and impact models, then use that to **estimate** liquidation cost for limit setting and stress.”
- **How you’d estimate it:** “I’d use **bid-ask** and **volume** data where we have it; for illiquid FTR or location power, **proxy** from liquid hubs or **historical** execution. **Market impact** I’d calibrate from implementation shortfall or a **power-law** in size vs volume; in **stress** I’d scale up spread and impact. **Liquidation cost** = spread + impact over the unwind horizon, possibly with **Almgren–Chriss**-style trade-off between speed and cost.”
- **Use in risk:** “We’d feed **liquidity** and **liquidation cost** into **LVaR** (liquidity-adjusted VaR), **limits** (max size such that unwind cost is bounded), and **stress** (e.g. ‘cost to liquidate in 5 days under stress’). So the quant work directly supports **risk** and **capital** decisions.”

---

## 6. Contribute to overall risk management team (risk analytics, processes, reporting; ad-hoc and firm-wide impact)

**Bullet:** Contribute to overall risk management team at BAM in risk analytics, processes, and reporting. This may involve ad-hoc risk analysis for portfolios that are not commodities-focused or investigation of impact of a commodities-focused portfolio to the overall risk of the firm.

### Scope

The role is **commodities-focused** (FTR, power, gas) but sits within a **broader** risk management function. You are expected to **contribute** to the **overall** team in **risk analytics**, **processes**, and **reporting** — not only for the commodities book. That can mean: (1) **Ad-hoc risk analysis** for **non-commodities** portfolios (e.g. equities, rates, credit, multi-asset) when the team needs extra capacity or specific quant input. (2) **Investigating** how a **commodities-focused** portfolio **affects** **overall firm risk** — e.g. correlation with other books, marginal contribution to firm VaR, concentration, and tail risk. Both directions matter: **commodities in context of the firm**, and **firm needs** that may pull you into other asset classes.

### Risk analytics, processes, and reporting (team-wide)

- **Analytics:** Apply the same **quantitative** discipline (metrics, models, data quality, backtesting) to **risk analytics** that the broader team uses — VaR/ES, Greeks, stress, attribution — so that **methodology** is **consistent** and **comparable** across books. You may **extend** or **review** analytics for non-commodities books (e.g. help with a new risk metric, a new decomposition, or a one-off study).
- **Processes:** Contribute to **process** design and improvement: data flow, run cadence, validation, escalation, documentation. Experience from **commodities** (e.g. curve builds, illiquid marks, auction-based liquidity) can inform **process** for other books (e.g. how to handle sparse data, how to define "mark" for hard-to-price positions).
- **Reporting:** Support **risk reporting** that is **firm-wide** or **cross-book**: e.g. firm VaR, limit utilization across desks, stress by asset class, concentration. Ensure **commodities** is **correctly** represented and that **aggregation** (e.g. correlation, diversification) is sound.

### Ad-hoc risk analysis for non-commodities portfolios

**Examples of non-commodities-focused portfolios:** Portfolios that are **not** primarily FTR, power, or gas. Concrete examples:

| Type | Examples | Typical risk analytics |
|------|----------|------------------------|
| **Equities** | Single-name, sector, index (e.g. S&P, sector ETFs), long/short equity, factor (value, momentum, quality). | Delta (beta, factor exposure), VaR/ES, stress (drawdown, sector shock), concentration, sector limits. |
| **Rates / fixed income** | Govt bonds (Treasuries, sovereigns), rates derivatives (swaps, futures, options), credit (IG/HY, CDS, structured credit). | Duration, convexity, key-rate sensitivity, VaR/ES, spread risk, stress (rate shock, spread widening). |
| **Credit** | Corporate bonds, CDS, indices (CDX, iTraxx), structured credit (CLOs, etc.). | Spread sensitivity, default/correlation, VaR, stress (default wave, spread blow-out). |
| **FX** | Spot, forwards, options; G10 and EM. | Delta (FX exposure), vol (vega), VaR, stress (EM devaluation, correlation break). |
| **Multi-asset / macro** | Mix of rates, FX, equities, sometimes commodities; discretionary or systematic. | Portfolio VaR/ES, correlation, marginal contribution by asset class, stress (risk-off, inflation shock). |
| **Quant / systematic** | Factor, stat arb, vol strategies; often cross-asset. | Factor exposure, crowding, backtest, regime sensitivity. |

- **When it arises:** The risk team may need **extra capacity** for a **one-off** or **time-bound** project on a **non-commodities** book — e.g. equities, rates, credit, FX, or a **multi-asset** portfolio. You may be asked to run **VaR** or **stress** with a new assumption, **explain** a P&L move, **backtest** a model, or **build** a small tool or report.
- **What you bring:** **Quant** skills are **transferable**: curve/vol construction, correlation, scenario design, backtesting, and clear documentation. You may need to **learn** the product and data (e.g. equity factor model, rate curve convention) quickly; the **analytical** approach is the same.
- **How to position it:** "I'm focused on commodities day-to-day but I'm comfortable supporting ad-hoc risk work on other books when the team needs it — same rigor on metrics, data, and process. I'd get up to speed on the product and systems and deliver in line with the team's standards."

### Impact of commodities portfolio on overall firm risk

- **Why it matters:** A **commodities** (FTR, power, gas) book is **one** part of the firm's total risk. Risk and management care about: **How much** does the commodities book **add** to **firm VaR** or **firm stress loss**? Is it **diversifying** (low correlation with equities/rates) or **concentrated** (correlation spikes in stress)? **Concentration** in a **single** asset class or **single** strategy can drive **tail** risk.
- **Investigation topics:** (1) **Marginal contribution** — incremental VaR or ES from the commodities book; (2) **Correlation** — correlation of commodities P&L (or returns) with other books (equities, rates, credit) in **normal** and **stress** periods; (3) **Stress** — contribution of commodities to **firm-wide** stress loss in historical or hypothetical scenarios; (4) **Concentration** — share of firm risk (VaR, notional, or exposure) from commodities; (5) **Liquidity** — how **commodities** liquidation cost or **funding** need in stress affects **firm** liquidity and recovery.
- **Deliverables:** **Reports** or **dashboards** that show commodities' **contribution** to firm risk (marginal VaR, stress contribution, correlation); **scenario** analysis ("if commodities book doubles, firm VaR changes by X"); **recommendations** for limits or capital if commodities is a **material** driver of firm risk.

**How we usually investigate one portfolio's impact on overall fund risk**

Standard ways to assess how a **single book or product** (e.g. commodities, equities, rates) affects the **overall** hedge fund portfolio:

| Approach | What it does | How it's used |
|----------|----------------|---------------|
| **Marginal / incremental VaR (and ES)** | **Firm VaR** with the book **included** minus firm VaR with the book **excluded** (or **component VaR**: sensitivity of firm VaR to a small change in the book). | Answers: "How much does this book **add** to total risk?" **Diversification**: marginal VaR < standalone VaR when the book is negatively correlated or uncorrelated with the rest. |
| **Correlation of P&L (or returns)** | **Time series** of daily (or weekly) P&L for the book vs P&L for the **rest of the fund** (or for other books). Compute **correlation** in **normal** periods and in **stress** periods (e.g. worst 5% of days). | Answers: "Does this book **move with** or **against** the rest of the fund?" **Stress correlation** often **increases** (everything falls together) — important for tail risk. |
| **Risk decomposition (Euler / contribution)** | **Total** firm VaR (or ES) is decomposed into **contributions** by book (or by factor): each book's **contribution** = its **weight** in the portfolio × its **marginal** effect. Sum of contributions = total VaR. | Answers: "Which **books** (or factors) **drive** firm VaR?" **Concentration**: one book contributing 50%+ of VaR → concentration risk. |
| **Stress contribution** | Run **historical** or **hypothetical** stress (e.g. equity -20%, rates +100 bp, oil -30%). Compute **firm** P&L under stress; then **attribute** the loss to each book (same scenario applied to each book's positions). | Answers: "How much does this book **contribute** to firm loss in scenario X?" **Joint** stress (all books stressed) vs **incremental** (only this book stressed). |
| **Notional / exposure share** | **Notional** (or **delta**, **VE**, **duration**) of the book as a **share** of firm total. Simple **size** view; does not capture vol or correlation. | Answers: "How **big** is this book relative to the fund?" Often reported alongside VaR contribution. |
| **Liquidity and funding** | **Liquidation cost** (or **time to liquidate**) for the book; **margin** and **collateral** that the book consumes; **funding** need in stress. | Answers: "If we have to **unwind** or **post more margin**, how much does this book drive **firm** liquidity need?" |
| **Scenario and sensitivity** | **Sensitivity**: "If this book's VaR doubles, firm VaR goes from X to Y." **Scenario**: "If we **remove** this book, firm VaR = Z." | Answers: "**What-if**" for limits, capital, or strategy (e.g. add/remove a book). |

**Typical workflow:** (1) **Define** the "book" (e.g. commodities, or FTR-only) and the **rest of the fund**; (2) **Compute** firm VaR/ES **with** and **without** the book (or use **component/marginal** VaR); (3) **Correlation** of book P&L vs rest-of-fund P&L (normal and stress); (4) **Decompose** firm VaR into contributions by book; (5) **Stress** scenarios: firm loss and each book's contribution; (6) **Report** contribution %, marginal VaR, correlation, and stress contribution so risk and management see the book in **context** of the whole fund.

### Interview angles (Section 6)

- **Contributing beyond commodities:** "I'd contribute to the overall risk team on **analytics**, **processes**, and **reporting** — same standards on methodology and documentation. I'm open to **ad-hoc** risk work on non-commodities portfolios when the team needs capacity; I'd lean on transferable quant skills and get up to speed on the product and data."
- **Commodities and firm risk:** "I'd help **investigate** how the commodities book affects **overall firm risk** — marginal contribution to firm VaR, **correlation** with other books in normal and stress, **stress** contribution, and **concentration**. That way risk and management see commodities in **context** and can set limits and capital appropriately."
- **Balance:** "My **primary** focus is commodities (FTR, power, gas) risk; I'd also support the **broader** team on ad-hoc analytics and on **firm-wide** risk views so the commodities book is properly integrated into the firm's risk picture."

---

## 7. Contribute to Global Risk Committee's understanding of risk drivers and considerations in related markets

**Bullet:** Contribute to Global Risk Committee's understanding of risk drivers and considerations in related markets.

### Scope

The **Global Risk Committee** (GRC) is typically a **senior** body (risk, management, sometimes trading and compliance) that reviews **firm-wide** risk, **limits**, **capital**, and **material** exposures. Your role is to **contribute** to the GRC's **understanding** of **risk drivers** and **considerations** in **related markets** — i.e. the markets that matter for the commodities book (FTR, power, gas) and how they **interact** with each other and with the rest of the firm. You are the **subject-matter** and **quant** voice so the committee can make informed decisions.

### What “risk drivers and considerations in related markets” means

- **Risk drivers:** **What** moves P&L and risk — e.g. **power** prices (hub, location, peak/off-peak), **gas** prices (hub, basis), **congestion** and **spreads** (FTR/CRR), **volatility**, **correlation**, **liquidity**, **regulation** (market rules, capacity, carbon). You **explain** which factors drive the commodities book and how they are **measured** (VaR, Greeks, stress).
- **Related markets:** Markets that are **linked** to the commodities book — e.g. **power ↔ gas** (spark spread, gas as fuel), **power ↔ congestion** (LMPs, FTR/CRR value), **power/gas ↔ weather** (demand, renewables), **regional** power markets (ERCOT, PJM, ISO-NE, etc.) and **cross-border** or **inter-regional** flows. “Related” also means **how** commodities risk **relates** to **other** firm books (equities, rates) — correlation, diversification, concentration.
- **Considerations:** **Non-model** or **judgment** aspects — e.g. **liquidity** (can we exit?), **regulatory** change (market design, capacity, emissions), **operational** (settlement, collateral, outages), **concentration** (single path, single hub, single counterparty). You help the GRC **understand** these so they can weigh risk vs return and set **policy**.

**Main risk drivers for FTR, power, and gas (reference)**

| Asset | Main risk drivers | Brief description |
|-------|-------------------|-------------------|
| **FTR / CRR** | **Congestion spread (path spread)** | Value = spread between sink and source (DAM or RT). **LMPs**, **nodal prices**, and **flows** drive the spread; **outages** and **load** change congestion. |
| | **Path / location** | Which **path** (source–sink); **hub** or **nodal**; **zone** (e.g. ERCOT North–South). Concentration in few paths = path risk. |
| | **Tenor / delivery** | **Monthly** vs **seasonal** vs **annual**; **remaining** days to settlement. Mark and volatility depend on tenor. |
| | **Liquidity** | **Auction-based** or **bilateral**; many paths **illiquid**. Exit cost and **liquidation** horizon matter. |
| | **Volatility (spread vol)** | **Realized** or **implied** vol of the path spread (or proxy). Options on FTR/CRR need **spread vol**. |
| **Power** | **Price (hub / location)** | **Forward** price by **hub** (e.g. ERCOT North, PJM West) and **tenor**; **location** and **basis** (node − hub). **Peak** vs **off-peak** vs **7×24**. |
| | **Volatility** | **Implied vol** from options; **spikes** and **mean reversion**; **term structure** of vol (short-dated often higher). **Asian** (vol of average) for settled-on-average options. |
| | **Shape / profile** | **Peak–off-peak** spread; **block** structure (on-peak hours). Shape risk when exposure is to a **profile** (e.g. 2×16). |
| | **Basis** | **Location − hub**; **DAM − RT**; **monthly − daily**. Basis can **widen** or **tighten** independently of hub. |
| | **Fuel / gas** | **Spark spread** (power − gas heat rate); **gas** price drives **marginal** power price in gas-dominated regions. |
| **Gas** | **Price (hub)** | **Henry Hub** (benchmark) and **other hubs**; **forward** by **tenor** (prompt, balance-of-month, monthly, seasonal strips). |
| | **Basis** | **Location − Henry** (e.g. SoCal, TCO, Waha, Chicago). **Basis** can move on **pipeline** capacity, **weather**, **storage**. |
| | **Volatility** | **Hub** and **basis** vol; **implied** from options; **seasonal** (winter vs summer vol). |
| | **Storage / seasonality** | **Inventory**, **inject/withdraw**; **winter strip** vs **summer strip**. **Calendar spread** (prompt vs forward). |
| | **Weather / demand** | **Heating** (winter) and **cooling** (summer) drive demand; **weather** drives **basis** and **vol**. |

*Cross-asset: **Power–gas** correlation (spark spread); **power–FTR** (congestion and LMPs); **gas–power** (fuel cost).*

### How you contribute

- **Present and explain:** **Summarize** risk metrics (VaR, ES, stress, concentration) and **explain** the **drivers** in plain language — e.g. “FTR risk is driven by congestion spreads; when power flows and LMPs change, FTR value changes; we proxy with hub spread and nodal model.” **Charts** and **dashboards** (exposure by hub, by path, stress contribution) so the committee **sees** the risk.
- **Related markets:** **Describe** how **power**, **gas**, and **FTR/congestion** interact (e.g. gas price → power price → congestion → FTR value). **Regional** differences (ERCOT vs PJM vs ISO-NE) and **seasonal** or **weather** effects. So the GRC understands **why** certain markets or periods are riskier.
- **Scenarios and stress:** **Translate** stress results into committee-friendly form — e.g. “In a heat-wave scenario, power and gas spike, congestion increases; our FTR and power book would lose X; here’s the contribution by book.” **Historical** events (e.g. Feb 2021, Aug 2020) as **reference** for “what could happen.”
- **Limits and policy:** **Support** the link between **analytics** and **limits** — e.g. “Our VaR limit is X; commodities contributes Y%; if we increase the commodities book, firm VaR would move by Z.” **Recommendations** (e.g. limit by path, by hub) when asked.
- **Ad-hoc questions:** The GRC may ask **one-off** or **deep-dive** questions (e.g. “Why did VaR jump?” “What’s our exposure to ERCOT North?” “How does gas basis affect the book?”). You **investigate** and **answer** with data and clear explanation.

### Interview angles

- **GRC contribution:** “I’d contribute to the Global Risk Committee by **explaining** risk drivers and metrics for the commodities book (FTR, power, gas) in clear terms — what moves P&L, how we measure it, and how **related markets** (power, gas, congestion, weather) interact. I’d present stress and concentration so the committee can make informed decisions on limits and capital.”
- **Related markets:** “Related markets for us are **power**, **gas**, and **congestion/FTR** — they’re linked (e.g. gas drives power, power flows drive congestion). I’d help the GRC understand those **linkages** and **regional** differences (ERCOT, PJM, etc.) so they see the full picture and the considerations (liquidity, regulation, concentration) that affect risk.”

---

## 8. Work with technology team: automate, maintain, and enhance integration of research and reporting

**Bullet:** Work with the technology team to automate, maintain, and enhance integration of research and reporting solutions into the existing infrastructure.

### Scope

You are **not** expected to own the firm's core technology stack, but you **do** work **with** the **technology team** so that **research** (e.g. curve builds, risk models, calibration) and **reporting** (e.g. risk packs, dashboards, attribution) are **automated**, **maintained**, and **well integrated** into **existing** infrastructure (data pipelines, risk platforms, data lakes, dashboards, APIs). You bring **domain** and **analytical** requirements; tech brings **platform**, **deployment**, and **scalability**. Together you **reduce** manual work, **keep** solutions **running**, and **improve** how research and reporting fit into the firm's systems.

### Automate

- **What to automate:** **Repetitive** or **scheduled** tasks — e.g. **curve** builds (power, gas, FTR) on a **cadence** (daily, intraday); **risk** runs (VaR, stress, Greeks) after **data** is ready; **report** generation (daily pack, weekly attribution) from **templates**; **data** pulls from **sources** (positions, market data, settlement). Goal: **no** (or minimal) **manual** steps for **periodic** deliverables.
- **How:** **Schedulers** (cron, Airflow, Prefect, or vendor) to trigger **pipelines** (data → curves → risk → report) in sequence with **dependencies** and **retries**. **Parameterized** jobs (e.g. report date, as-of time) so the same logic runs for any date. **Idempotency**: re-run with same inputs → same outputs. You **specify** the **logic** and **cadence**; tech helps with **orchestration**, **monitoring**, and **alerting**.
- **Ownership:** Research owns **what** runs (methodology, parameters); tech owns **where** it runs (servers, containers, queues) and **how** it's triggered. You **collaborate** on **failure** handling and **SLAs** (e.g. daily pack by 8am).

### Maintain

- **What to maintain:** **Keep** research and reporting solutions **running** — fix **breaks** when **data** or **APIs** change, **dependencies** upgrade, or **logic** needs a **bug fix**. **Version** code and **config** (e.g. curve params, VaR settings) so changes are **traceable** and **reproducible**. **Monitor** runs (success/fail, run time, data freshness) and **escalate** when something is wrong.
- **How:** **Version control** (e.g. Git) for **code** and **config**; **documentation** (runbooks, data dictionary) so tech and research can **debug**. **Regular** reviews (e.g. quarterly) of **dependencies** and **deprecations**. You **identify** and **prioritize** fixes; tech may implement **infra** or **deployment** changes.
- **Ownership:** Research owns **correctness** (model, numbers); tech owns **availability** and **performance**. **Shared** ownership for **integration** (e.g. "report reads from this table" — both sides must keep the contract).

### Enhance integration into existing infrastructure

- **What "integration" means:** Research and reporting **consume** data from and **publish** results to **existing** systems — e.g. **data lake** or **warehouse** (positions, curves, market data); **risk platform** (VaR, limits, stress); **dashboards** (Power BI, Dash, Streamlit); **APIs** or **shared** databases so other teams (trading, risk, finance) get **consistent** numbers without **duplicate** logic.
- **Enhance:** **Improve** how research/reporting **plug in** — e.g. **new** data sources or **new** outputs (e.g. publish curves to a **central** store so risk and trading use the **same** curve); **standardize** schemas and **refresh** schedules; **replace** one-off scripts with **pipeline** steps that **fit** the firm's **data** and **reporting** stack. You **define** requirements (what data, what format, what frequency); tech **implements** connectors, APIs, or **pipeline** stages.
- **Existing infrastructure:** Respect **current** platforms — don't duplicate **data** or **logic** that already exists; **extend** rather than replace where possible. **Align** with firm **standards** (e.g. Python version, database access, security).

### Interview angles

- **Working with tech:** "I'd work **with** the technology team to **automate** research and reporting — schedulers, pipelines, parameterized runs — so we don't rely on manual steps. I'd **maintain** solutions by versioning code and config, fixing breaks when data or deps change, and monitoring runs. I'd help **enhance integration** so our curves and reports **fit** into the existing infrastructure — same data sources, same outputs for risk and trading — and we extend the platform rather than building silos."
- **Ownership:** "Research owns **what** we compute and **why** (methodology, parameters); tech owns **where** and **how** it runs (orchestration, deployment). I'd specify **requirements** and **logic**; tech would help with **pipelines**, **monitoring**, and **integration**. We'd collaborate on **SLAs** and **failure** handling so deliverables are on time and traceable."

---

## 9. Work with risk management to onboard new portfolios and products

**Bullet:** Work with risk management to onboard new portfolios and products.

### Scope

When the firm **adds** a **new portfolio** (e.g. a new strategy, a new desk, or a new asset class within commodities) or **new products** (e.g. new FTR paths, new power/gas products, new regions or venues), they must be **brought into** the **risk framework** — data, models, limits, and reporting. You work **with risk management** to **onboard** these so that risk has **visibility**, **limits** are set, and **metrics** (VaR, stress, Greeks) are **correct** and **consistent** with the rest of the book. You provide **analytical** and **implementation** support; Risk owns **policy** and **approval**.

### What “onboard” means

- **Data:** **Position** and **market** data for the new portfolio or product must **flow** into the risk system — e.g. **source** (trading system, registry, broker), **mapping** (product ID, curve, vol), **cutoff** and **refresh**. You help **define** what data is needed and **validate** that it is **correct** and **complete**.
- **Models and valuation:** **How** to **value** and **risk** the new product — e.g. **curve** (which hub, which tenor), **vol** (surface or proxy), **FTR** path spread or **proxy**. You **implement** or **extend** the risk engine so the new product is **in scope** for VaR, Greeks, and stress.
- **Limits and risk policy:** Risk **defines** or **updates** **limits** (e.g. VaR, notional, delta by bucket) for the new portfolio/product. You **support** by showing **current** exposure, **marginal** contribution to firm risk, and **sensitivity** so Risk can set **appropriate** limits.
- **Reporting:** The new portfolio/product must appear in **risk reports** and **dashboards** — e.g. VaR by book, stress contribution, concentration. You **add** the new book/product to **report** definitions and **validate** that numbers are **consistent** with the rest of the framework.
- **Validation:** **Backtest**, **sensitivity**, and **reconciliation** (e.g. risk P&L vs trading P&L) so Risk is **confident** the onboarding is **correct** before **go-live**.

### Examples (FTR, power, gas)

- **New FTR/CRR paths or region:** e.g. firm starts trading **PJM** FTRs in addition to **ERCOT** CRRs. Onboard: **position** source (PJM FTR registry), **spread** curve or **proxy**, **mapping** to risk factors; **VaR** and **stress** with new paths; **limits** and **reporting** for the new book.
- **New power/gas products or hubs:** e.g. new **location** (basis), new **tenor** (e.g. daily options), or new **venue** (e.g. new exchange). Onboard: **curve** and **vol** for the new product; **bucket** definitions for limits and reports; **data** feed and **valuation** in risk engine.
- **New strategy or desk:** e.g. a **new** commodities strategy (e.g. structured options, storage). Onboard: **full** risk setup — data, models, limits, reporting — in **coordination** with Risk and trading.

### Interview angles

- **Onboarding:** “I’d work with **risk management** to **onboard** new portfolios and products — ensure **data** flows into the risk system, **models** and **valuation** cover the new product (curves, vol, mapping), **limits** are set with the right **exposure** view, and **reporting** includes the new book. I’d **validate** (backtest, reconcile) so Risk is confident before we go live.”
- **Partnership with Risk:** “Risk owns **policy** and **approval**; I’d provide **analytical** support — what data we need, how to map and value the product, what the exposure and marginal risk look like — so Risk can make informed decisions on limits and scope. We’d iterate until the new book is fully integrated into the risk framework.”

---

## 10. Experience with seasonality in commodities risk models

**Bullet:** Experience with seasonality in commodities risk models.

### Scope

**Seasonality** — systematic variation with **time of year** or **time of day** — is a **core** feature of power and gas (and, indirectly, congestion/FTR). Risk models that **ignore** seasonality can **misstate** exposure, **VaR**, and **stress**. You are expected to have **experience** incorporating **seasonality** into **curves**, **volatility**, **demand**, and **correlation** so that risk metrics are **realistic** across seasons and **peak/off-peak** regimes.

### Why seasonality matters in commodities

- **Demand and supply:** **Power** demand is **higher** in **summer** (cooling) and **winter** (heating) and **lower** in **shoulder** months; **intraday** (peak vs off-peak) is strongly seasonal. **Gas** demand is **winter-heavy** (heating) and **summer** (power gen for cooling); **storage** inject/withdraw creates **seasonal** patterns in **basis** and **spreads**. **Congestion** and **FTR** value follow **load** and **flows**, so they are **seasonal** too.
- **Prices and curves:** **Forward** curves and **basis** exhibit **seasonality** — e.g. winter strip vs summer strip, monthly **seasonal** component. **Curve-building** (Section 1) often uses **seasonal** dummies or **sinusoidal** terms so that **interpolation** and **extrapolation** respect **calendar** and **profile** (peak/off-peak).
- **Volatility:** **Vol** is **seasonal** — e.g. **higher** in **winter** (gas) or **summer** (power in some regions); **spikes** more likely in **peak** demand periods. **Risk** (VaR, stress) that uses a **single** vol or **flat** term structure can **understate** risk in **high-season** months and **overstate** in **low-season**.
- **Correlation:** **Correlation** between hubs, between power and gas, or between **tenors** can **change** by season (e.g. gas–power link stronger in winter). **Portfolio** VaR and **diversification** depend on **correlation**; seasonality in correlation affects **marginal** risk and **stress**.

### How seasonality appears in risk models

| Area | How seasonality is modeled | Risk impact if ignored |
|------|-----------------------------|--------------------------|
| **Forward curves** | **Seasonal** component in curve build (monthly dummies, sinusoidal, or seasonal spline); **peak vs off-peak** curves; **winter/summer** strip pillars. | **Delta** and **mark** wrong in high/low seasons; **hedge** ratios off. |
| **Volatility** | **Term structure** of vol by **month** or **season** (e.g. higher vol in Jan, Jul); **seasonal** vol in **options** pricing and **VaR** (historical or MC). | **Vega** and **VaR** understated in **high-vol** seasons; **stress** scenarios miss **seasonal** spikes. |
| **Demand / load** | **Load** forecast or **scenario** with **seasonal** shape; **congestion** and **FTR** proxy tied to **seasonal** load. | **Congestion** and **FTR** risk misstated by season. |
| **Correlation** | **Seasonal** correlation (e.g. **winter** gas–power vs **summer**); **rolling** or **regime** correlation by month. | **Portfolio** VaR and **diversification** wrong by season. |
| **Stress** | **Stress** scenarios that are **season-specific** (e.g. winter cold snap, summer heat wave) with **seasonal** vol and **spread** assumptions. | **Stress** loss and **limits** not aligned with **seasonal** risk. |

### Power, gas, and FTR specifics

- **Power:** **Peak** (e.g. 2×16, 7×8) vs **off-peak** vs **7×24**; **summer** (cooling) and **winter** (heating) **demand** peaks; **renewables** (wind, solar) add **seasonal** and **intraday** shape. **Curves** and **vol** by **bucket** and **month**; **Asian** options often need **vol of average** with **seasonal** input.
- **Gas:** **Winter** heating demand; **summer** power-gen demand; **storage** (inject in summer, withdraw in winter) drives **prompt vs strip** and **basis** seasonality. **Curve** and **vol** (e.g. winter strip vol higher); **basis** (e.g. SoCal) can be **more** volatile in **winter**.
- **FTR / congestion:** **Congestion** follows **load** and **flows** — **seasonal** (summer/winter peaks) and **intraday** (peak hours). **FTR** spread **curves** and **proxy** for VaR should reflect **seasonal** patterns; **stress** (e.g. heat wave) is **seasonal** by design.

**How to model seasonality in FTR, power, and gas**

| Market | What to model | Modeling approaches |
|--------|----------------|---------------------|
| **Power** | **Forward curve** by delivery month and **profile** (peak, off-peak, 7×24). | **Pillars:** Use **monthly** and **seasonal** contracts (winter strip, summer strip) as quoted; **interpolate** between months with a **seasonal** component — e.g. **monthly dummies** (one per month), **sinusoidal** (e.g. $a + b\cos(2\pi t/12) + c\sin(2\pi t/12)$ for annual cycle), or **Fourier** terms. **Peak vs off-peak:** Build **separate** curves for peak and off-peak (or shape factors); **ratio** or **spread** peak/off-peak can be **seasonal** (e.g. higher in summer). **Calendar** consistency: no arbitrage between overlapping products (e.g. monthly vs quarterly). |
| | **Volatility** by month/season and by **bucket**. | **Term structure of vol:** **Monthly** or **quarterly** vol (e.g. Jan vol, Jul vol) from **options** where liquid; **interpolate** or **smooth** (e.g. parametric in month). **Historical** vol: **rolling** window by **month** (e.g. same calendar month over past years) to get **seasonal** vol. **Spikes:** Allow **higher** vol in **peak** months (summer, winter); **regime** or **scaling** by month in VaR/stress. **Asian** options: **vol of average** with **seasonal** input (e.g. weight high-vol months more in the average period). |
| | **Demand / load** shape. | **Load forecast:** **Seasonal** profile (e.g. monthly factors, day-of-week, hour-of-day); **temperature**-driven demand (HDD/CDD) with **seasonal** coefficients. Used for **scenarios** and **congestion**-related risk. |
| **Gas** | **Forward curve** by delivery month; **basis** by location. | **Pillars:** **Prompt**, **balance-of-month**, **monthly**, **seasonal** strips (winter, summer); each pillar is the forward for that period. **Seasonal** component: **winter** (Nov–Mar) vs **summer** (Apr–Oct) typically differ; use **monthly dummies** or **sinusoidal** in curve build. **Basis** curves (location − Henry) often have **strong** seasonality (e.g. SoCal winter premium); model **basis** as **seasonal** spread or **separate** seasonal curve per location. **Storage:** Inject (summer) / withdraw (winter) creates **calendar spread** seasonality; can be implicit in strip prices or modeled with **storage** model. |
| | **Volatility** by month/season; **basis** vol. | **Hub vol:** **Implied** vol from options by **month** or **strip** (e.g. winter strip vol vs summer); **historical** vol by **calendar month** (rolling same month). **Basis** vol: **seasonal** (e.g. higher in winter for some locations); **separate** vol surface or **scale** from hub. **VaR:** Use **month-dependent** vol (or **seasonal** factor) in historical or Monte Carlo VaR. |
| | **Storage** and **calendar spread**. | **Storage** optionality: **seasonal** value (summer inject, winter withdraw); **spread** vol and **inventory** can be **seasonal**. **Calendar spread** (e.g. winter − summer): model as **seasonal** spread or **correlation** between tenors that varies by season. |
| **FTR / CRR** | **Path spread** (or **congestion** proxy) by **delivery month** and **profile**. | **No liquid forward** for most paths; **spread** is often **model-derived** (nodal/congestion model) or **proxy** (e.g. hub spread, historical DAM spread). **Seasonality:** (1) **Load-based:** Use **seasonal** load profile (summer/winter peaks) in the **congestion** or **nodal** model so **simulated** or **historical** spreads are **seasonal**. (2) **Historical spread by month:** For paths with **historical** DAM or auction data, compute **average** spread (or **vol**) by **calendar month**; use as **seasonal** curve or **seasonal** vol in VaR. (3) **Proxy:** If path is proxied by **hub** power spread, use **seasonal** power curve and **seasonal** vol for the proxy. (4) **Stress:** **Heat wave** / **cold snap** scenarios are **season-specific**; apply **seasonal** vol and **load** in stress. |
| | **Correlation** (path–path, path–power) by season. | **Correlation** of FTR returns (or proxy returns) with **power** (and gas) can **change** by season (e.g. stronger in high-load months). **Estimate** **rolling** correlation by **month** or use **regime** (summer vs winter); feed into **portfolio** VaR and **stress**. |

**Summary:** For **power** and **gas**, seasonality is modeled in **curves** (seasonal dummies or sinusoidals, peak/off-peak or winter/summer pillars), **vol** (month- or season-dependent term structure, from options or historical same-month), and **stress** (season-specific scenarios). For **FTR**, seasonality is modeled via **load-driven** congestion, **historical** spread/vol by month, or **proxy** with seasonal power; **correlation** with power/gas can be **seasonal**. All three benefit from **explicit** seasonal terms so that **risk** (VaR, Greeks, stress) is **correct** by season.

### Interview angles

- **Seasonality in risk:** "I have experience building **seasonality** into commodities risk models — **curves** (seasonal component, peak/off-peak, winter/summer strips), **vol** (term structure by month or season), and **stress** (season-specific scenarios like cold snap or heat wave). Ignoring seasonality **understates** risk in high-demand/high-vol periods and **overstates** it in shoulder months; I'd ensure VaR, Greeks, and stress are **seasonally** aware."
- **Power and gas:** "For **power**, seasonality is in **demand** (summer/winter peaks), **profile** (peak vs off-peak), and **renewables**; we'd use **seasonal** curve and vol by bucket and month. For **gas**, **winter** heating and **storage** create **seasonal** curves and **basis**; vol is often **higher** in winter. For **FTR**, congestion and path spreads follow **load**, so they're **seasonal** too — we'd model that in the **spread** curve and **proxy** for VaR."

---

## 11. Strong programming skills in Python and SQL; familiarity with numeric libraries

**Bullet:** Strong programming skills in Python and SQL. Must be familiar with numeric libraries such as pandas, numpy, etc.

### Scope

The role requires **production-quality** or **research-quality** code for **curves**, **risk** (VaR, stress, Greeks), **reporting**, and **data** pipelines. **Python** is the primary language for **analytics** and **modeling**; **SQL** is used to **query** and **transform** data (positions, market data, curves, results). You should be comfortable with **numeric** and **scientific** libraries (e.g. **pandas**, **numpy**) for **vectorized** operations, **curve** building, **optimization**, and **statistics** — and with **version control**, **testing**, and **documentation** so code is **maintainable** and **auditable**.

### Important Python libraries (reference)

| Category | Library | Typical use in risk / commodities |
|----------|---------|-----------------------------------|
| **Core numeric / data** | **NumPy** | **Arrays**, **vectorized** math, **linear algebra**, **random** (e.g. MC), **broadcasting**. Base for many other libs. |
| | **pandas** | **DataFrames** and **Series**; **time series** (curves, P&L, positions by date); **groupby**, **merge**, **pivot**; **read/write** CSV, Excel, Parquet; **resample** (e.g. daily → monthly). Core for **data** and **tables**. |
| **Scientific / stats** | **SciPy** | **Optimization** (minimize, root-finding), **interpolation** (splines), **stats** (distributions, correlation), **linear algebra** (sparse). Curve building, calibration, VaR. |
| | **scipy.stats** | **Distributions** (normal, t, etc.), **percentiles**, **correlation**, **tests**. VaR, backtest, stress. |
| **Visualization** | **matplotlib** | **Plots** (line, scatter, hist, heatmap); **publication**-style figures; **subplots**. Curves, P&L, exposure. |
| | **seaborn** | **Statistical** plots (distributions, correlation heatmaps, time series). Risk dashboards, exploration. |
| | **Plotly** | **Interactive** charts (zoom, hover); **Dash** for **dashboards**. Risk packs, Streamlit/Dash apps. |
| **Optimization** | **SciPy.optimize** | **Minimize** (e.g. curve fit, calibration), **least_squares**, **root**. Curve building, vol calibration. |
| | **CVXPY** (optional) | **Convex** optimization (e.g. portfolio construction, constraints). Advanced use. |
| **SQL / databases** | **SQL** (via **sqlalchemy**, **pandas.read_sql**, or **DB driver**) | **Query** positions, market data, curves; **JOIN**, **aggregate**, **filter**. ETL, reporting. |
| | **sqlalchemy** | **ORM** and **raw** SQL; **connection** to PostgreSQL, SQL Server, etc. Data layer. |
| **Other useful** | **datetime / pandas.Timestamp** | **Dates**, **time zones**, **business** days. Curve tenors, report dates. |
| | **requests** | **HTTP** calls to **APIs** (market data, internal services). Data ingestion. |
| | **pyarrow / Parquet** | **Columnar** storage; **fast** read/write for **large** datasets. Data lake, intermediate files. |
| | **pytest** | **Unit** and **integration** tests. Regression, correctness of curves and risk. |
| | **Jupyter** | **Notebooks** for **exploration**, **ad-hoc** analysis, **documentation**. Not for production runs. |

*For **commodities** and **risk** specifically: **pandas** + **numpy** for curves (pillars, interpolation, seasonality), **scipy** for splines and optimization, **pandas** for VaR (historical, percentile), **matplotlib/plotly** for exposure and P&L charts, **SQL** for position and market data. **Streamlit** or **Dash** for dashboards (Section 2).*

### Interview angles

- **Python and SQL:** "I have strong **Python** and **SQL** — **pandas** and **numpy** for data and numeric work (curves, VaR, time series), **scipy** for optimization and stats, **matplotlib/plotly** for visualization, and **SQL** for querying positions and market data. I write **readable**, **versioned** code and use **tests** where it matters for correctness."
- **Libraries:** "I'm familiar with **pandas** (DataFrames, time series, groupby, merge), **numpy** (arrays, vectorization, random), **scipy** (optimize, interpolate, stats), and **matplotlib/seaborn/plotly** for charts. For this role I'd use them for **curve** builds, **risk** runs, **reporting**, and **data** pipelines, with **SQL** for the data layer."

---

## 12. Advanced Python: virtual environments, release process, multi-processing

**Bullet:** Advanced Python knowledge including management of virtual environments, release process, or multi-processing.

### Virtual environments

**What they are:** Isolated **Python** environments with their own **interpreter** and **packages** so that **dependencies** for one project (or one run) don’t **conflict** with another. Essential for **reproducibility** (same code runs with same libs) and for **production** (controlled, versioned stack).

**Common tools and usage:**

| Tool | Create | Activate (Unix) | Activate (Windows) | Install / freeze |
|------|--------|-----------------|---------------------|-------------------|
| **venv** (built-in) | `python -m venv .venv` | `source .venv/bin/activate` | `.venv\Scripts\activate` | `pip install -r requirements.txt`; `pip freeze > requirements.txt` |
| **conda** | `conda create -n myenv python=3.11` | `conda activate myenv` | same | `conda install pandas`; `conda env export > environment.yml` |
| **virtualenv** | `virtualenv .venv` | same as venv | same | same as venv |
| **pyenv** | `pyenv virtualenv 3.11 myenv` | `pyenv activate myenv` | N/A (Unix) | manages **Python version**; often used with venv |

**Practice:** **One** venv (or conda env) **per project** or **per app**; **pin** versions in **requirements.txt** or **environment.yml**; **recreate** env from file for **CI** or **deploy** so builds are **reproducible**. **Never** install globally for production; use venv in **containers** (Docker) too if the image doesn’t already isolate.

### Release process

**What it means:** How **code** and **config** move from **development** to **production** — **versioning**, **testing**, **packaging**, and **deployment** so releases are **traceable** and **repeatable**.

**Typical elements:**

- **Version control (Git):** **Branches** (e.g. `main` = production, `develop` = integration, feature branches); **tags** for **releases** (e.g. `v1.2.0`). **Commits** and **PRs** so every release is tied to a **commit** or **tag**.
- **Versioning:** **Semantic** versioning (e.g. **MAJOR.MINOR.PATCH**); or **calver** (e.g. `2025.03.1`). **Bump** version in **code** or **config** (e.g. `__version__`, `pyproject.toml`, `setup.py`) and **tag** in Git.
- **Testing:** **Unit** tests (e.g. pytest) and **integration** tests **before** release; **CI** (e.g. GitHub Actions, Jenkins) runs tests on **push** or **PR**; **block** merge or deploy if tests fail.
- **Packaging (optional):** For **libraries** or **installable** apps: **setuptools**, **poetry**, or **flask**; **wheel** or **sdist**; **version** in package metadata. For **scripts** or **pipelines**, often **no** formal package — just **repo** + **requirements.txt** + **tag**.
- **Deployment:** **Deploy** a **tag** or **commit** (e.g. pull repo on server, `pip install -r requirements.txt`, run); or **container** (Docker image built from **tag**). **Rollback** = redeploy **previous** tag/commit.
- **Documentation:** **Changelog** or **release notes** (what changed); **runbook** (how to run, env vars, deps). So **releases** are **auditable**.

**For risk/research:** “Release” may be **tagged** code + **pinned** env + **config** (e.g. VaR params) so that **risk run** X is **reproducible** from **repo** + **tag** + **data as-of** date.

### Multi-processing (and parallelism)

**Why:** **Risk** runs (VaR, stress, curve build over many paths) can be **CPU-heavy**; **multi-processing** or **parallel** execution **reduces** wall-clock time.

**Options in Python:**

| Approach | Library / built-in | Use case | Note |
|----------|---------------------|----------|------|
| **multiprocessing** | `multiprocessing.Pool`, `Process` | **CPU-bound** tasks (e.g. many independent valuations, scenarios). | **Processes** (not threads) avoid **GIL**; **pickle** for args/return. |
| **concurrent.futures** | `ProcessPoolExecutor`, `ThreadPoolExecutor` | Same as above with **futures** API (submit, map, result). | Cleaner API; **ProcessPoolExecutor** for CPU, **ThreadPoolExecutor** for I/O-bound. |
| **threading** | `threading` | **I/O-bound** (e.g. many API calls, DB reads). | **GIL** limits CPU parallelism; good for **waiting** on I/O. |
| **joblib** | `joblib.Parallel` | **Parallel** loops (e.g. over paths, scenarios); often used with **sklearn**-style code. | Simple `Parallel(n_jobs=-1)(delayed(f)(x) for x in xs)`. |
| **Dask** (optional) | **dask** | **Larger-than-memory** or **distributed** DataFrames/arrays; **parallel** pipelines. | For **big** data or **cluster**; overkill for single-machine multi-core. |

**Practice:** **Partition** work into **independent** chunks (e.g. by path, by scenario, by date); **avoid** shared mutable state; **time** single vs parallel to confirm **speedup**; **limit** number of **processes** (e.g. `n_jobs=cpu_count()-1`) to avoid **thrashing**. For **risk** pipelines, **ProcessPoolExecutor** or **joblib** over **scenarios** or **books** is common.

### Git commands (reference with explanations)

**Setup and config**

| Command | Explanation |
|---------|-------------|
| `git init` | Create a new **repository** in the current directory (`.git` folder). |
| `git clone <url>` | **Clone** a remote repo (copy to local); default branch checked out. |
| `git config user.name "Name"` | Set **user name** for commits (often global: `--global`). |
| `git config user.email "email@example.com"` | Set **email** for commits. |

**Daily workflow (branch, add, commit)**

| Command | Explanation |
|---------|-------------|
| `git status` | Show **working tree** status: modified, staged, untracked files. |
| `git branch` | List **local** branches; `*` = current branch. |
| `git branch <name>` | Create a **new** branch (does not switch). |
| `git checkout <branch>` | **Switch** to branch (or commit). |
| `git checkout -b <name>` | **Create** and **switch** to new branch. |
| `git switch <branch>` | Same as checkout for **switching** branch (newer, clearer). |
| `git add <file>` | **Stage** file for next commit (add to index). |
| `git add .` | Stage **all** changes in current directory (and below). |
| `git reset HEAD <file>` | **Unstage** file (keep changes in working dir). |
| `git commit -m "message"` | **Commit** staged changes with message. |
| `git commit -am "message"` | Stage **tracked** files and commit (skip `git add` for modified). |

**History and diff**

| Command | Explanation |
|---------|-------------|
| `git log` | **History** of commits (current branch); `--oneline` for short. |
| `git log --graph --oneline` | **Graph** of branches and commits. |
| `git diff` | **Diff** between **working dir** and **staged** (or **HEAD** if nothing staged). |
| `git diff --staged` | Diff between **staged** and **last commit**. |
| `git diff <branch1> <branch2>` | Diff between two branches (or commits). |

**Remote and sync**

| Command | Explanation |
|---------|-------------|
| `git remote -v` | List **remotes** (e.g. `origin`) and URLs. |
| `git fetch origin` | **Fetch** updates from remote (no merge); updates remote-tracking branches. |
| `git pull` | **Fetch** and **merge** current branch from remote (e.g. `pull origin main`). |
| `git push origin <branch>` | **Push** branch to remote; e.g. `push origin main`. |
| `git push -u origin <branch>` | Push and set **upstream** so future `git push`/`pull` know the branch. |

**Merge, rebase, and undo**

| Command | Explanation |
|---------|-------------|
| `git merge <branch>` | **Merge** another branch into **current** branch (creates merge commit if needed). |
| `git rebase <branch>` | **Replay** current branch’s commits **on top of** branch (linear history). |
| `git reset --soft HEAD~1` | **Undo** last commit; keep changes **staged**. |
| `git reset --mixed HEAD~1` | Undo last commit; keep changes **in working dir**, **unstage**. |
| `git reset --hard HEAD~1` | **Discard** last commit and its changes (destructive). |
| `git revert <commit>` | **New** commit that **reverses** a given commit (safe for shared history). |

**Tags and release**

| Command | Explanation |
|---------|-------------|
| `git tag` | List **tags**. |
| `git tag v1.0.0` | Create **lightweight** tag at current commit. |
| `git tag -a v1.0.0 -m "Release 1.0"` | **Annotated** tag (recommended for releases). |
| `git push origin v1.0.0` | **Push** tag to remote. |
| `git checkout v1.0.0` | Checkout **detached HEAD** at tag (e.g. to build or run that version). |

**Stash and clean**

| Command | Explanation |
|---------|-------------|
| `git stash` | **Stash** working (and optionally staged) changes; clean working dir. |
| `git stash pop` | **Apply** most recent stash and **remove** it from stash list. |
| `git stash list` | List stashes. |
| `git clean -fd` | **Remove** untracked files and directories (`-f` force, `-d` dirs); use with care. |

**Useful for collaboration / PR**

| Command | Explanation |
|---------|-------------|
| `git pull --rebase origin main` | **Pull** and **rebase** your branch on top of `main` (cleaner history before push). |
| `git cherry-pick <commit>` | **Apply** one commit from another branch onto current branch. |
| `git log origin/main..HEAD` | Commits **in current branch** not in `origin/main` (what you’d push). |

**Summary:** **Virtual envs** = isolated Python + deps (venv/conda); **release** = versioning (Git tags), tests, optional packaging, deploy from tag; **multi-processing** = CPU parallelism (multiprocessing, ProcessPoolExecutor, joblib). **Git** = branch, add, commit, push/pull, merge/rebase, tags for releases; use **revert** to undo shared history, **reset** only for local undo.

### Interview angles

- **Virtual envs and release:** "I use **virtual environments** (venv or conda) per project and **pin** dependencies in **requirements.txt** or **environment.yml** so runs are **reproducible**. For **release**, we **tag** in Git (e.g. semantic versioning), run **tests** in CI, and **deploy** from the tag so every production run is **traceable** to a commit and env."
- **Multi-processing:** "For **CPU-heavy** risk runs (e.g. VaR over many scenarios, or curve build over many paths), I use **multiprocessing** or **ProcessPoolExecutor** (or **joblib**) to **parallelize** independent chunks. I keep **process count** bounded and avoid shared mutable state so we get a real **speedup** without thrashing."

---

## 13. Experience at hedge fund / asset management; exposure to systematic futures and portfolio construction

**Bullet:** Experience working at a hedge fund or other asset management firms with exposure to systematic futures strategies or portfolio construction.

### Scope

The role values **experience** in a **hedge fund** or **asset management** setting, and **exposure** to **systematic futures** strategies (e.g. trend, carry, momentum, multi-factor futures) and/or **portfolio construction** (e.g. optimization, risk parity, factor tilts). Even if the job is **commodities-focused** (FTR, power, gas), **futures** (power, gas, and other commodities) are part of the **broader** futures universe; **systematic** approaches (signals, rules, rebalancing) and **portfolio** construction (position sizing, diversification, limits) are **transferable**. You may be asked to **assess** or **monitor** the fund’s **exposure** to systematic futures strategies — e.g. how much **capital** or **risk** is in **systematic** vs **discretionary**, and **how** those strategies **contribute** to **total** risk and P&L.

### How to assess exposure to systematic futures strategies at a hedge fund

**What “exposure” means here:** How much of the **fund’s** capital, **notional**, or **risk** is **allocated** to **systematic futures** strategies (and, optionally, **which** sub-strategies or **factors**), and how that **drives** **portfolio** risk and **correlation** with the rest of the book.

**1. Define the universe and strategy breakdown**

- **Futures** vs **other** assets: Identify **which** positions are **futures** (listed derivatives: commodities, rates, FX, equity indices). **Power**, **gas**, and **FTR/CRR** are **commodities-related**; the fund may also run **systematic** strategies on **other** futures (e.g. rates, equity index).
- **Systematic** vs **discretionary:** **Systematic** = rule-based (signals, models, rebalancing); **discretionary** = human-driven. **Tag** or **attribute** positions (or **P&L**) by **strategy** (e.g. “systematic trend”, “systematic carry”, “discretionary commodities”). Requires **metadata** (strategy ID, book, or mandate) from **trading** or **risk** systems.
- **Sub-strategies / factors:** If the fund runs **multi-factor** or **multi-strategy** systematic (e.g. **trend**, **carry**, **momentum**, **value**), **exposure** can be broken down by **factor** or **signal** (e.g. notional or risk in “trend” vs “carry”). Needs **strategy** or **factor** labels per position or per **sub-book**.

**2. Exposure metrics (allocation and size)**

| Metric | What it measures | How to compute |
|-------|-------------------|-----------------|
| **Notional exposure** | **Dollar** size of futures positions (long + short, or **gross** / **net**). | Sum **notional** (contracts × contract size × price, or **delta**-equivalent) by **strategy** or **factor**; **ratio** to **total** fund notional or **AUM**. |
| **Number of contracts / positions** | **Breadth** of the systematic book (how many **markets** or **legs**). | Count **open** positions (or **names**) by strategy; **concentration** (e.g. top 5 markets as % of notional). |
| **Capital or risk allocation** | **Risk** (e.g. VaR, volatility, margin) **allocated** to systematic futures. | **VaR** or **vol** by **strategy** (same engine, **subset** of positions); **marginal** or **component** VaR from systematic futures; **ratio** to **total** fund VaR. |
| **Gross / net** | **Directional** vs **market-neutral** tilt. | **Gross** = sum of **absolute** notionals; **net** = sum of **signed** notionals. **Net/gross** ratio indicates **directional** vs **spread** exposure. |

**3. Factor and strategy exposure (if systematic is factor-based)**

- **Factor exposure (betas):** Regress **strategy** or **portfolio** **returns** on **factor** returns (e.g. **trend** factor, **carry** factor, **commodity** index, **rates** factor). **Betas** = **exposure** to each factor. **Data:** **Strategy** or **book** P&L (daily) and **factor** series (from vendor or internal).
- **Attribution:** **Attribute** P&L to **factors** or **signals** (e.g. “60% of systematic futures P&L from trend, 30% from carry”). **Exposure** = **sensitivity** (beta) × **factor** vol or **factor** weight in portfolio.
- **Concentration:** **Exposure** by **sector** (commodities, rates, FX, equity) or by **market** (e.g. energy vs metals vs ags). **Herfindahl** or **top-N** share of notional or risk.

**4. Risk and correlation**

- **Contribution to fund risk:** **Marginal** VaR or **component** VaR from the **systematic futures** book; **stress** contribution (e.g. systematic futures loss in a given scenario). **Correlation** of **systematic futures** **returns** with **rest of fund** (and with **discretionary** books) in **normal** and **stress** periods.
- **Diversification:** If **systematic** is **low** correlation with **discretionary** or **other** strategies, it **diversifies**; if **correlation** spikes in **stress**, **tail** risk may be **higher** than VaR suggests. **Exposure** in a **risk** sense = **contribution** to **portfolio** VaR and **tail** risk.

**5. Data and process**

- **Position** data: **Futures** positions (contract, size, side, book/strategy); **refresh** (daily or intraday). **Mapping:** contract → **sector**, **factor**, or **strategy**.
- **Returns / P&L:** **Daily** (or higher frequency) **P&L** or **returns** by **book** or **strategy** for **factor** regression and **correlation**.
- **Consistency:** **Exposure** and **risk** should use **same** **positions** and **curves** as **main** risk engine so numbers are **comparable** and **auditable**.

**Summary:** To **assess** exposure to **systematic futures** at a hedge fund: (1) **Define** universe (futures vs other) and **tag** systematic vs discretionary (and by factor/sub-strategy if applicable). (2) **Measure** **allocation** — notional, position count, **capital/VaR** — by strategy and **ratio** to total fund. (3) **Factor** exposure: **betas** to trend, carry, etc., and **attribution** of P&L. (4) **Risk** exposure: **marginal/component** VaR, **stress** contribution, **correlation** with rest of fund. (5) **Data:** positions with strategy/factor labels, returns by book, factor series; **process** aligned with main risk framework.

### Interview angles

- **Hedge fund / systematic experience:** "I have [or: I’m looking for] experience at a **hedge fund** or **asset manager** with **systematic futures** or **portfolio construction** — so I understand how **allocation**, **factor** exposure, and **risk** contribution are **measured** and how **systematic** and **discretionary** books **interact**. For **commodities** (FTR, power, gas), the same **discipline** — exposure by strategy, contribution to risk, correlation — applies."
- **Assessing systematic futures exposure:** "To assess **exposure** to systematic futures I’d **tag** positions by strategy (systematic vs discretionary, and by factor if multi-factor), then measure **notional** and **risk** (VaR, marginal VaR) by strategy and as a **share** of the fund. I’d look at **factor** betas (e.g. trend, carry) from **return** regression and **correlation** of systematic futures with the **rest** of the fund so we see **diversification** and **tail** risk."

---

## 14. Factor analysis, PCA, decomposition models for P&L and risk; machine learning

**Bullet:** Experience with factor analysis, PCA, decomposition models for P&L and risk, machine learning.

### Scope

The role values **experience** with **factor analysis**, **PCA** (principal component analysis), **decomposition** models for **P&L** and **risk** (e.g. P&L explain, VaR decomposition), and **machine learning** (ML). These tools support **risk** (dimension reduction, factor VaR, attribution), **valuation** (e.g. curve or vol from ML), and **signals** (e.g. in systematic strategies). Below: **factor analysis** and **PCA** in a risk context; **decomposition** for **P&L** and **VaR**; then **ML** approaches **specific** to **energy** (FTR, power, gas).

### Factor analysis (in risk and returns)

**What it is:** **Factor analysis** models **observed** variables (e.g. returns of many assets, or P&L of many books) as driven by a **smaller** set of **latent** or **observed** **factors** plus **idiosyncratic** noise. **Goals:** **dimension reduction**, **interpretation** (what drives co-movement?), **factor exposure** (betas), **factor VaR**.

**In risk and P&L:**
- **Returns:** Asset or **book** returns = **factor loadings** × **factor returns** + **residual**. **Factors** can be **observed** (e.g. market, sector, trend, carry) or **latent** (from PCA or factor analysis). **Exposure** = loadings (betas).
- **Factor VaR:** **VaR** of the **portfolio** from **factor** distribution: simulate or historical **factor** returns, apply **loadings**, get **portfolio** return distribution; **VaR** = percentile. **Decomposition:** **contribution** of each **factor** to VaR (e.g. component VaR by factor).
- **P&L attribution:** **Attribute** P&L to **factors** (e.g. "curve" = factor 1, "vol" = factor 2, "theta" = time decay) or to **positions/buckets**; **decomposition** = sum of contributions.

**Commodities:** **Factors** might be **hub** power, **gas** (Henry), **basis**, **congestion** (or FTR spread proxy), **vol**; or **latent** factors from PCA of **returns** or **curve** changes.

### PCA (principal component analysis)

**What it is:** **PCA** finds **linear** combinations of variables that **maximize variance** (in order). First **principal component (PC)** = direction of **max** variance; second = max variance **orthogonal** to first; etc. **Result:** **scores** (projections on PCs) and **loadings** (weights of each variable on each PC). **Use:** **dimension reduction**, **noise** reduction, **factor** extraction (PCs as factors).

**In risk and P&L:**
- **Curve / surface:** **PCA** on **curve** changes (e.g. daily changes in forward prices by tenor) or **vol surface** changes. **First** PC often ≈ **level** or **parallel** shift; **second** ≈ **slope** or **tilt**; **third** ≈ **curvature**. **VaR** or **stress** can be done in **PC space** (few dimensions) then **mapped back** to curve.
- **Returns:** **PCA** on **asset** or **book** returns to get **latent** factors; **factor VaR** using **PC** returns and **loadings**. **Decomposition:** **variance** (or VaR) **explained** by each PC.
- **Correlation / covariance:** **PCA** on **covariance** (or correlation) matrix; **reduced** rank **covariance** (e.g. keep top 3 PCs) for **VaR** or **simulation** to **stabilize** estimates and **reduce** noise.

**Commodities:** **PCA** on **power** hub curve changes, **gas** curve changes, **FTR** spread (or proxy) changes; **interpret** PCs as level/slope/curvature or **sector** (power vs gas vs congestion).

### Decomposition models for P&L and VaR

**P&L decomposition (P&L explain):**
- **Goal:** **Explain** **realized** P&L as sum of **contributions** from **curve** move, **vol** move, **theta**, **new trades**, **residual**.
- **Methods:** **Taylor** (delta–gamma–vega): ΔP&L ≈ **delta** × Δcurve + **gamma** × (Δcurve)² + **vega** × Δvol + **theta** × Δt. **Revaluation:** P&L = **value(t+1)** − **value(t)** with **curve/vol** as of t+1; **attribute** by **buckets** (e.g. by tenor, by hub) via **finite difference** or **sensitivity**. **Residual** = actual P&L − sum of attributed terms.
- **By book:** Decompose **total** P&L into **FTR** + **power** + **gas** (and sub-buckets). **By factor:** If using **factor** model, P&L = **factor** contributions (beta × factor return) + residual.

**VaR decomposition:**
- **Goal:** **Break down** **portfolio** VaR into **contributions** by **position**, **bucket** (hub, tenor, path), or **factor** so we see **what** drives tail risk.
- **Methods:** **Component VaR** (or **marginal** VaR): **Euler** allocation — each position's **contribution** = weight × **marginal** VaR (derivative of VaR w.r.t. position). **Factor VaR:** VaR from **factor** model; **contribution** of each **factor** = factor's **marginal** or **component** VaR. **Scenario** decomposition: **stress** P&L by **scenario**; **contribution** of scenario = loss in that scenario (or **conditional** contribution).
- **Use:** **Concentration** (which positions/factors dominate VaR?), **limits** (set limits by component), **diversification** (many small contributions vs few large).

**Summary:** **Factor analysis** = identify factors (latent or observed) and **loadings**; **PCA** = extract **principal** components for **dimension reduction** and **factor**-style VaR; **P&L decomposition** = attribute P&L to **curve**, **vol**, **theta**, **trades**, **buckets**, or **factors**; **VaR decomposition** = **component** or **marginal** VaR by **position**, **bucket**, or **factor**.

### Machine learning approaches in energy markets (FTR, power, gas)

**Use cases:** **Forecasting** (prices, load, congestion, vol), **valuation** or **curve** (e.g. illiquid points), **risk** (e.g. scenario generation, clustering), **signals** (for systematic strategies), **anomaly** detection (data quality, outliers).

**Power:**
- **Price / LMP forecasting:** **Regression** (e.g. **linear**, **ridge**, **elastic net**) or **tree** models (**random forest**, **gradient boosting** — XGBoost, LightGBM) with **features**: load, **temperature**, **wind/solar** gen, **gas** price, **day**/hour/month. **Time series:** **ARIMA**, **SARIMAX** (seasonal), **Prophet**; **deep** (e.g. **LSTM**, **Transformer**) for **long** sequences. **Goal:** **Day-ahead** or **real-time** price forecast for **trading** or **risk** (e.g. scenario paths).
- **Load forecasting:** **ML** (GBM, **neural nets**) or **statistical** (SARIMAX) with **weather**, **calendar**; **peak** vs **off-peak** or **profile** prediction. Feeds **congestion** and **FTR**-related models.
- **Vol / spike prediction:** **Classification** (e.g. **spike** vs no spike) or **regression** (vol, **quantiles**) with **features** (load, temp, renewables, season). **Use:** **VaR**, **stress**, **option** pricing.
- **Curve and illiquid points:** **ML** to **fill** or **smooth** **illiquid** tenors or **locations** (e.g. **basis** from **hub** + features); **neural** or **GBM** **surrogate** for **nodal** or **congestion** model where **full** run is costly.

**Gas:**
- **Price forecasting:** **Hub** (e.g. Henry) and **basis** (location − hub) with **features**: **weather** (HDD, CDD), **storage** (inventory, inject/withdraw), **supply** (production, LNG), **demand** (power gen). **Models:** **GBM**, **neural nets**, **SARIMAX**; **probabilistic** (e.g. **quantile** regression) for **scenarios**.
- **Basis and location:** **Predict** **basis** (or location price) from **hub** + **weather** + **pipeline**/storage **features**; **ML** for **illiquid** locations. **Curve** completion for **long** tenors or **exotic** strips.
- **Storage / optionality:** **Reinforcement learning** or **dynamic** programming with **ML**-based **price** (or **vol**) **forecast** for **storage** valuation or **exercise**; **surrogate** models for **high-dimensional** state.

**FTR / CRR / congestion:**
- **Spread / congestion forecasting:** **Predict** **path** spread or **congestion** (DAM or RT) from **load**, **generation**, **outages**, **weather**, **hub** prices. **Features:** nodal or zonal **load** forecast, **renewables** forecast, **outage** schedule. **Models:** **GBM**, **neural nets**, **panel** regression (path × time). **Use:** **mark** for **illiquid** paths, **scenario** for **VaR** or **stress**.
- **FTR proxy for VaR:** **No** liquid series for most paths. **ML** options: (1) **Predict** path **spread** or **return** from **factors** (hub power, load, congestion index) — **GBM** or **neural** net; (2) **Cluster** paths and use **cluster**-level **proxy**; (3) **Latent factor** (PCA or **autoencoder**) on **available** path or **nodal** data; (4) **Generate** **scenarios** of path spreads from **generative** model (e.g. **VAE**, **GAN**) or **copula** with **ML**-estimated marginals.
- **Auction or clearing:** **Predict** **clearing** price or **capacity** in **CRR/FTR** auctions from **network** and **demand** features (research; often **optimization**-based, ML for **input** or **surrogate**).

**Cross-cutting:**
- **Feature** engineering: **Temporal** (lags, day-of-week, month, season), **weather** (temp, HDD, CDD, wind, solar irradiance), **market** (hub price, basis, load, outages). **Domain** knowledge matters.
- **Validation:** **Backtest** (out-of-sample, **walk-forward**); **economic** (e.g. P&L of a **naive** strategy using forecast); **calibration** (e.g. **quantile** reliability). **Overfitting** risk with **limited** data (e.g. few years of power prices); **regularization**, **cross-validation**, **simple** baselines.
- **Interpretability:** **SHAP**, **feature** importance, **partial** dependence for **tree**/GBM; **attention** or **attribution** for **neural** nets — helps **risk** and **trading** trust and **audit** models.

**Summary table (ML in energy):**

| Domain | Typical ML use | Examples |
|--------|-----------------|----------|
| **Power** | Price/LMP forecast, load forecast, vol/spike, curve fill | GBM, LSTM, SARIMAX, Prophet; features: load, weather, renewables, gas |
| **Gas** | Hub/basis forecast, curve, storage/optionality | GBM, neural nets, quantile regression; features: weather, storage, supply/demand |
| **FTR / congestion** | Spread/congestion forecast, FTR proxy for VaR, scenario generation | GBM, neural nets, PCA/autoencoder, generative (VAE) or copula; features: load, outages, hub, nodal |

### Linear and integer programming (FTR, power, gas)

**Why it matters:** **Linear programming (LP)** and **integer programming (IP)** underpin **market clearing**, **unit commitment**, **transmission** and **gas network** flow, **auctions** (e.g. FTR/CRR), and **portfolio** or **hedge** optimization. As a **risk** or **quant** researcher you may **interpret** or **stress** outcomes of these optimizations, **replicate** simplified versions for **scenario** or **attribution**, or work with systems that **solve** them.

**Power (LP and IP):**
- **Economic dispatch / SCED:** **LP** (or **quadratic** for cost curves): minimize **generation cost** subject to **power balance** (supply = demand), **line flow** limits (DC or AC linearized), **gen** min/max. **Output:** LMPs (dual/shadow prices on balance constraint), **congestion** components (dual on flow limits). **Day-ahead** and **real-time** markets are **large-scale** LP (or QP).
- **Unit commitment (UC):** **Mixed-integer** (MIP): **binary** variables for **on/off** and **start-up**; **continuous** for **generation**. **Constraints:** min up/down time, **ramp** rates, **reserve** requirements. **UC** determines **which** units run; **economic dispatch** then sets **levels**. **Risk** relevance: **outage** or **scarcity** scenarios change **UC** solution and thus **LMPs** and **congestion**.
- **LMP decomposition:** **LMP** = **energy** component + **congestion** + **losses**. These come from **dual** (shadow) prices of the **dispatch** LP. **Congestion** component drives **FTR** value; **risk** may **stress** congestion or **re-run** dispatch under scenarios.

**Gas (LP and IP):**
- **Gas flow / nomination:** **LP** or **nonlinear** (Weymouth, etc.): **flow** in pipelines subject to **pressure** and **capacity**; **injections** and **withdrawals** at nodes. **Goal:** meet **demand** at least cost or **max throughput**. **Output:** **nodal** prices (or **basis**), **capacity** shadow prices. **Integer** can appear for **compressor** on/off or **discrete** contracts.
- **Storage and transport:** **LP** over **time** (multi-period): **inject/withdraw** subject to **inventory** limits, **rate** limits; **transport** capacity. **Valuation** or **optimization** of **storage** and **transport** often uses **stochastic** or **deterministic** LP. **Risk:** **scenario** of demand/supply → **re-solve** flow/storage LP → **price** and **basis** impact.

**FTR / CRR (LP and IP):**
- **FTR auction (e.g. ERCOT CRR):** **Market** clears by **optimization**: **maximize** (or **minimize** negative of) **social welfare** or **revenue** from **FTR** bids/offers subject to **network** (power flow) **feasibility**. **FTR** **obligations** are **injection/withdrawal** patterns; **constraints** = **PTDF**-based **flow** limits (linear in **injections**). So **clearing** is **LP** (or **MIP** if **indivisible** FTRs or **combinatorial** rules). **Output:** **clearing** prices by **path** (or zone pair), **allocated** FTRs.
- **FTR valuation / feasibility:** **Simulation** of **congestion** (e.g. from **dispatch** or **PTDF** × **injection** scenario) gives **path** **payoff**. **No** direct “solve an LP for FTR price” in the market, but **underlying** **LMP** and **congestion** come from **dispatch** LP; **FTR** payoff = **path** **congestion** component. **Portfolio** optimization (e.g. **hedge** FTR exposure, **budget** constraint on FTR purchase) can be **LP** (continuous FTR) or **MIP** (discrete lots).
- **PTDF and flow:** **Power Transfer Distribution Factors** are **linear**: **flow** on a line = **PTDF** matrix × **net injection** vector. **Feasibility** of a set of **FTRs** = **LP**: do **FTR** **injections** (scaled by FTR MW) cause **flow** within **limits**? **Simultaneous feasibility test (SFT)** in many markets is an **LP**.

**Risk / quant use:**
- **Interpret** **clearing** or **dispatch** output: **LMPs**, **congestion**, **shadow** prices → **explain** P&L or **stress** scenarios.
- **Scenario** or **stress:** **Re-run** (or approximate) **dispatch** or **flow** LP under **demand**/outage/**gas** price scenarios to get **congestion** and **FTR** payoff distribution for **VaR** or **stress**.
- **Simplified** **LP** for **curve** or **spread:** e.g. **single-node** or **reduced** network **LP** to **bound** or **approximate** congestion; **sensitivity** (dual) to **demand** or **capacity**.
- **Hedge** or **portfolio:** **LP** (or **MIP**) to **choose** FTRs or **gas** positions subject to **budget** and **risk** (e.g. **min variance** or **min CVaR** with linear constraints).

**Summary:** **LP** is central to **power** **dispatch** (LMPs, congestion), **gas** **flow** (nodal prices, basis), and **FTR** **clearing**/feasibility (PTDF-based). **IP/MIP** appears in **unit commitment** (power) and in **FTR** or **gas** when **discrete** decisions (on/off, integer lots) matter. For **FTR, power, and gas risk**, understanding these **optimization** building blocks helps **interpret** prices, **stress** congestion, and **link** positions to **underlying** market clearing.

### Interview angles

- **Factor analysis and PCA:** "I've used **factor analysis** and **PCA** for **dimension reduction** and **factor** extraction — e.g. **PCA** on **curve** changes for **level/slope/curvature** or on **returns** for **latent** factors; then **factor VaR** and **decomposition** (component VaR by factor). For **P&L** and **VaR** I've built **decomposition** models: **P&L explain** (curve, vol, theta, buckets) and **VaR** decomposition (Euler/component by position or factor)."
- **ML in energy:** "In **energy** (power, gas, FTR) I'd use **ML** for **forecasting** (prices, load, congestion, vol) with **GBM** or **neural nets** and **features** like weather, load, renewables; for **illiquid** **curve** or **spread** (e.g. FTR path proxy) where we have no liquid series; and for **scenario** or **VaR** (e.g. **generative** or **factor**-based). I'd **validate** with backtests and **calibration** and keep **interpretability** (SHAP, feature importance) so risk and trading can audit."
- **LP and IP in FTR, power, gas:** "**LP** is at the core of **power** dispatch (LMPs and **congestion** from the **dual** of the dispatch problem), **gas** flow (nodal prices, basis), and **FTR** **clearing** and **feasibility** (PTDF-based flow constraints). **MIP** shows up in **unit commitment** (on/off, start-up) and in **FTR** or **gas** when there are **discrete** decisions. For **risk**, I'd use this to **interpret** clearing outcomes, **stress** congestion by re-running or approximating the **underlying** optimization under scenarios, and **link** FTR/gas positions to **market** clearing."

---

### Interview Q&A

**Q: How would you construct a power forward curve for a liquid hub (e.g. ERCOT North)?**  
**A:** Use liquid products (day-ahead, balance-of-month, monthly, seasonal strips) as pillars. Bootstrap a discount curve if needed; then build the forward curve by no-arbitrage (e.g. monthly forwards from monthly contracts, quarterly from quarters). Interpolate between pillars (e.g. cubic spline in time or in log-price) and enforce no calendar arbitrage. Add seasonality (summer/winter) via monthly adjustments or a seasonal component. Validate against broker screens and recent trades.

**Q: What’s the difference between sticky-strike and sticky-delta when moving from current vol surface to a future date?**  
**A:** *Sticky-strike:* implied vol is constant in strike (e.g. $/MWh). As underlying moves, same strike keeps same vol; simple but can create odd delta/vega behavior. *Sticky-delta:* vol is constant in delta (or moneyness). Option’s moneyness is preserved, so delta is more stable; often used in FX/equities. For power/gas, neither is perfect (spikes, mean reversion); practitioners often use a hybrid or a parametric (e.g. SABR) that is recalibrated.

**Q: How do you ensure a volatility surface is arbitrage-free?**  
**A:** (1) *Calendar:* no arbitrage in time—call prices (or implied vols) non-decreasing in maturity for same strike (or appropriate no-arbitrage bounds). (2) *Butterfly:* convexity in strike—positive density, so positive butterfly spreads; in practice, no negative OTM call spreads. (3) *Triangle:* put-call parity and consistency across strikes/maturities. In implementation: constrain calibration (e.g. penalty for violation), use parameterizations that are arbitrage-free by construction (e.g. SVI with bounds), or post-process (smoothing that preserves no-arb).

**Q: Why is term-structure modeling different for power vs gas?**  
**A:** Power: non-storable, strong seasonality (temp-driven demand, renewables), spikes and mean reversion; forward curves can be built from liquid monthly/quarterly power contracts; storage doesn’t link prompt to forward. Gas: storable (with limits), inventory and weather drive basis; more liquid prompt and seasonal strips; storage creates link between prompt and winter/summer. Both need seasonal components; power often has higher short-term vol and more pronounced spikes.
