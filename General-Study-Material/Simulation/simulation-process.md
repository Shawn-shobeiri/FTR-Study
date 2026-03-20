# Simulating Energy Prices: From Exploratory Analysis to Process Choice

A step-by-step guide from a quant perspective: how to go from **historical data** to a **stochastic model** and **simulated paths**, with emphasis on distributional features, process selection, and pros/cons.

---

## 1. Why simulate prices?

- **Risk:** VaR, expected shortfall, stress scenarios, capital.
- **Valuation:** Options, storage, flexible generation, path-dependent contracts.
- **Strategy:** Backtesting, scenario analysis, hedging.

We need **paths** (e.g. $S_t$ over $t$) that are **statistically plausible** and, where possible, **consistent with observed** moments, autocorrelation, and tail behavior. That starts with **understanding the data**.

---

## 2. Step 1: Exploratory analysis of historical prices

Before choosing a process, we **inspect the history** to learn: distribution shape, tails, dependence over time, seasonality, and stationarity. Work in **returns** or **levels** depending on the process family (e.g. levels for mean-reverting price; returns for log-price).

### 2.1 What to look at

**(a) Distribution and tails**

- **Histogram / KDE** of price (or log-price, or returns). Is it roughly symmetric or skewed? Power and gas **levels** are often **right-skewed** (spikes up, floor near zero).
- **Q–Q plot** vs normal: if points deviate in the **tails**, the distribution is **heavy-tailed** (more extreme values than Gaussian). Energy prices typically have **fat tails**.
- **Empirical moments:** mean $\hat{\mu}$, variance $\hat{\sigma}^2$, **skewness** $\hat{\gamma}_1$, **kurtosis** $\hat{\gamma}_2$. Excess kurtosis $> 0$ suggests fat tails.
- **Takeaway:** If tails are heavy and/or skew is significant, a **Gaussian** (e.g. plain Brownian motion or OU in levels) may **understate** risk; consider **jump-diffusion** or **heavy-tailed** innovations.

**(b) Autocorrelation and mean reversion**

- **ACF** (autocorrelation function) of price or returns: does correlation decay with lag? **Slow decay** → long memory or near random walk; **fast decay** → mean-reverting.
- **Half-life:** If you model $dX_t = -\kappa X_t\, dt + \sigma\, dW_t$, the half-life is $\ln 2 / \kappa$. From data, you can **estimate** $\kappa$ (e.g. from an AR(1) on demeaned price or log-price) and get an implied half-life. **Short half-life** (days/weeks) → strong mean reversion; **long** → closer to random walk.
- **Takeaway:** Power and gas **spot** prices usually show **mean reversion** (supply/demand balance pulls price back). **Forward** returns may be closer to a random walk over short horizons.

**(c) Seasonality**

- **Within-day:** Hourly or block (peak/off-peak) pattern — average price by hour of day. Power has strong **daily** seasonality.
- **Within-week:** Weekday vs weekend (e.g. 5x16 vs 2x16).
- **Within-year:** Monthly or seasonal averages (summer/winter for gas and power). **De-trend** or **model seasonality** explicitly (e.g. $\theta(t)$ in a mean-reverting model).
- **Takeaway:** If seasonality is strong, the process should include a **deterministic** seasonal component or **separate** parameters by season/hour.

**(d) Stationarity**

- **Levels:** Is the **mean** of the price (or log-price) roughly constant over time, or is there a **trend** or **structural break**? Use visual inspection, rolling mean, or tests (e.g. ADF for unit root).
- **Returns / changes:** Often closer to stationary. For **prices**, if we model **log-price** or **spread** to a forward, we may get stationarity.
- **Takeaway:** **Non-stationary** levels (e.g. random walk in log-price) → differencing or modeling in **returns**; **stationary** levels (e.g. spread, or price around a seasonal mean) → mean-reverting process in levels.

**(e) Spikes and extremes**

- **Time series plot:** Identify **spikes** (short-lived jumps up or down). In power, spikes are common (outages, demand peaks).
- **Spike frequency and size:** Empirical distribution of **jump sizes** and **time between spikes** can inform a **jump** component (e.g. Poisson jumps with a given distribution).
- **Takeaway:** If spikes are a **material** part of the history, a **diffusion-only** model may **underprice** options and **understate** tail risk; consider **jump-diffusion** or **regime-switching**.

### 2.2 Summary of EDA outputs

| EDA check        | What it suggests for the model                                      |
|------------------|----------------------------------------------------------------------|
| Fat tails        | Jumps or heavy-tailed innovations (e.g. Student-t, jump process)   |
| Skewness         | Asymmetric jumps or skewed innovation distribution                  |
| Fast ACF decay   | Mean reversion (e.g. OU, 1-factor with $\kappa > 0$)               |
| Slow ACF decay   | Near random walk; consider GBM or low $\kappa$                     |
| Strong seasonality | Deterministic $\theta(t)$ or seasonal parameters                  |
| Non-stationary level | Model returns or use trend/cointegration; avoid stationary OU in raw level if level has a unit root |
| Visible spikes   | Add jump component or regime switch                                |

---

## 3. Step 2: Choosing the stochastic process

We list **candidate processes** with their **SDEs**, **interpretation**, and **typical use**. All can be written in risk-neutral or real-world form; for **simulation** we usually use **real-world** (historical) parameters unless we are pricing derivatives (then risk-neutral).

### 3.1 Brownian motion (BM) and geometric Brownian motion (GBM)

**BM:** $dX_t = \mu\, dt + \sigma\, dW_t$.  
**GBM (for price $S_t > 0$):** $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$, so $S_t = S_0 \exp\bigl((\mu - \sigma^2/2)t + \sigma W_t\bigr)$.

- **Interpretation:** No mean reversion; constant drift and volatility; log-price is BM.
- **Pros:** Very simple; closed-form solutions and option formulas (Black–Scholes type); easy to simulate (exact for GBM).
- **Cons:** No mean reversion; **thin tails** (Gaussian); no seasonality; often **poor fit** to power/gas **spot** (which revert and spike). Better suited to **forward** or **long-dated** log-returns in some markets.

---

### 3.2 Ornstein–Uhlenbeck (OU) — mean-reverting in levels

$dX_t = \kappa(\theta - X_t)\, dt + \sigma\, dW_t$.

- **Interpretation:** $X_t$ reverts to **long-run mean** $\theta$ at speed $\kappa$; volatility $\sigma$ constant. Stationary distribution is **Gaussian** with mean $\theta$ and variance $\sigma^2/(2\kappa)$.
- **Pros:** Captures **mean reversion**; tractable (conditional distribution is Gaussian; can simulate exactly); good for **spreads** or **de-meaned** prices. Can add **deterministic** $\theta(t)$ for seasonality.
- **Cons:** **Symmetric** (no skew); **thin tails**; cannot generate **spikes** unless $\theta(t)$ or $\sigma$ is made time-varying. **Negative** $X_t$ possible (fine for spread; for **price** we may need a variant, e.g. exponential OU or floor).

---

### 3.3 Exponential OU (or “1-factor” in log-level)

$S_t = e^{X_t}$ with $dX_t = \kappa(\theta - X_t)\, dt + \sigma\, dW_t$ (so $X_t = \ln S_t$ in a simple case).

- **Interpretation:** **Log-price** is mean-reverting; **price** $S_t$ is always **positive** and reverts to $e^\theta$ in distribution.
- **Pros:** Positive prices; mean reversion in log-space; relatively simple.
- **Cons:** Still **thin-tailed** in log-space; **no** explicit spikes (large moves require large $\sigma$ or fast moves). Volatility of **price** is state-dependent ($\sigma S_t$ if we write an SDE for $S_t$).

---

### 3.4 Mean-reverting with seasonal level (1-factor + seasonality)

$dX_t = \kappa\bigl(\theta(t) - X_t\bigr)\, dt + \sigma(t)\, dW_t$, with $\theta(t)$ and optionally $\sigma(t)$ **deterministic** (e.g. sinusoidal, or piecewise by month).

- **Interpretation:** Long-run mean and possibly vol vary with **time of year** (and optionally hour of day).
- **Pros:** Captures **seasonality** and **mean reversion**; widely used for **power** and **gas** spot.
- **Cons:** Still Gaussian shocks; no **jumps**; need to **specify** $\theta(t)$, $\sigma(t)$ (from EDA or fundamentals).

---

### 3.5 Jump-diffusion (e.g. Merton)

$dX_t = \mu\, dt + \sigma\, dW_t + J_t\, dN_t$, where $N_t$ is a **Poisson** process (intensity $\lambda$) and $J_t$ is the **jump size** (e.g. Gaussian or exponential). For **price** we might use $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t + (e^J - 1) S_{t-}\, dN_t$ so that jumps are multiplicative.

- **Interpretation:** “Normal” moves from diffusion; **spikes** from jumps.
- **Pros:** **Fat tails** and **skew** (depending on jump distribution); can fit **spike** frequency and **size** from data.
- **Cons:** More parameters (e.g. $\lambda$, jump mean/variance); **calibration** and **simulation** are heavier; need enough **spike** history to estimate jump part.

---

### 3.6 Regime-switching

Two (or more) **regimes** (e.g. “normal” vs “spike”); in each regime the process has different drift/vol or even different type (e.g. OU vs jump). Switching is usually **Markov** (transition probabilities).

- **Interpretation:** Market alternates between “calm” and “stressed” (or “spike”) states.
- **Pros:** Can capture **clustering** of volatility and **spikes** without a separate jump process.
- **Cons:** **Latent** state (regime not directly observed); more parameters; estimation (e.g. EM, filtering) and simulation are more involved.

---

### 3.7 Multi-factor models

Example: **two factors** — one **short-term** (mean-reverting, fast) and one **long-term** (slow or random walk). Price (or log-price) = sum of the two factors.

- **Interpretation:** Short-term factor captures **temporary** shocks (e.g. weather); long-term captures **trend** or **forward** level.
- **Pros:** Flexible **term structure** of volatility and correlation; used in **gas** and **power** for forward curves.
- **Cons:** More state variables and parameters; calibration and simulation are heavier.

---

### 3.8 Heavy-tailed innovations (no jumps)

Keep a simple **dynamics** (e.g. OU or discrete-time AR(1)) but replace **Gaussian** increments with **Student-t** or **stable** distribution.

- **Interpretation:** Same **autocorrelation** structure as Gaussian version, but **larger** tail probability.
- **Pros:** **Fat tails** without adding a jump process; implementation is straightforward (sample from t or stable).
- **Cons:** Less **interpretable** than explicit jumps; option pricing and moment formulas are less standard.

---

## 4. Step 3: Calibration / estimation

- **Moments:** Match **theoretical** moments (mean, variance, autocorrelation, half-life) to **sample** moments from EDA. For OU, $\kappa$ and $\sigma$ can be tied to variance and ACF decay.
- **MLE:** If the **transition density** is known (e.g. OU is Gaussian), **maximum likelihood** for the discretized series gives $\kappa$, $\theta$, $\sigma$. For **jump-diffusion**, MLE is harder (latent jumps); **EM** or **filtering** (e.g. particle filter) can be used.
- **Indirect:** Match **option** or **forward** implied vols if we have market options; then the process is risk-neutral calibrated.
- **Stability:** Check that **estimated** $\kappa > 0$ (mean reversion), $\sigma > 0$; if using **historical** data, use a long enough sample and be aware of **regime** changes.

---

## 5. Step 4: Simulation

- **Exact:** For **GBM**, $S_{t+\Delta} = S_t \exp\bigl((\mu - \sigma^2/2)\Delta + \sigma \sqrt{\Delta}\, Z\bigr)$ with $Z \sim N(0,1)$. For **OU**, $X_{t+\Delta}$ is Gaussian with known mean and variance given $X_t$ — can sample exactly.
- **Euler–Maruyama:** For a general SDE $dX_t = \mu(X_t,t)\, dt + \sigma(X_t,t)\, dW_t$, use $X_{t+\Delta} = X_t + \mu(X_t,t)\Delta + \sigma(X_t,t)\sqrt{\Delta}\, Z$. **Bias** decreases as $\Delta \to 0$; for **jumps**, add jump contribution when $N_t$ jumps in $(t, t+\Delta)$.
- **Milstein:** If $\sigma$ depends on $X_t$, adding a correction term improves accuracy; for **multi-dimensional** or **jump** models, stick to Euler or exact where available.
- **Path structure:** Generate **many paths** (e.g. 10k–100k) over the horizon; then compute **discounted payoffs** (valuation) or **empirical** VaR/ES (risk).

---

## 6. Step 5: Validation

- **Moment matching:** Compare **simulated** mean, variance, skewness, kurtosis, ACF to **historical** (and to **theoretical** if available). Adjust calibration if mismatch is large.
- **Backtest:** If the purpose is **VaR**, compare **simulated** VaR to **realized** breaches (e.g. traffic light); if **option pricing**, compare model value to market.
- **Stress:** Run **stress scenarios** (e.g. high vol, many jumps) and check that positions and risk metrics behave sensibly.

---

## 7. Pros and cons summary: process choice

| Process              | Pros                                      | Cons                                           | Best for                          |
|----------------------|-------------------------------------------|------------------------------------------------|-----------------------------------|
| **BM / GBM**         | Simple; closed-form; exact simulation     | No mean reversion; thin tails                  | Forwards; long-horizon log-return |
| **OU (levels)**     | Mean reversion; tractable; exact         | Thin tails; symmetric; can go negative        | Spreads; de-meaned price          |
| **Exponential OU**  | Positive price; mean reversion           | Thin tails in log; no spikes                   | Spot with mild vol               |
| **OU + seasonality**| Seasonality + mean reversion              | No jumps; Gaussian                             | Power/gas spot, base profile      |
| **Jump-diffusion**  | Fat tails; spikes; skew                  | More params; calibration harder               | Spot with spikes; optionality     |
| **Regime-switching**| Vol clustering; spike regimes             | Latent state; estimation heavy                 | When regimes are clear in data   |
| **Multi-factor**    | Rich term structure; flexible            | More state vars; calibration                   | Forwards; curve modeling         |
| **Heavy-tailed (t)**| Fat tails; simple dynamics               | Less standard for derivatives                  | Risk; VaR with fat tails          |

---

## 8. Prices in FTR, power, and gas: characteristics and simulation recommendations

Below we outline **what we simulate** (the “price” or payoff driver), **main characteristics** from a distribution and dynamics perspective, and **recommended process families** for each. This guides both **single-asset** simulation and **multi-asset** (e.g. power + gas + FTR) setups.

---

### 8.1 FTR / CRR “prices” (congestion spread, path value)

**What we simulate:**  
FTR payoff = **quantity** × **reference spread** over the delivery period. The “price” we care about is the **path spread** (sink price − source price) or, equivalently, the **congestion component** of that spread — i.e. the **volume-weighted average** of (LMP_sink − LMP_source) over the settlement interval (e.g. month). That spread is driven by **binding constraints** and their **shadow prices**: spread ≈ $\sum_{\text{constraints}} \text{shadow price} \times \text{PTDF}_{\text{path}}$. So the **underlying** we simulate is either (1) the **path spread** (or monthly average spread) or (2) the **constraint shadow prices** (and then we aggregate via PTDFs to get path value).

**Characteristics:**

- **Zero or near-zero often:** When the constraint(s) **do not bind**, shadow prices are zero and the path spread is zero (or very small). So the **distribution** of path spread (or daily/monthly average spread) is **spike-at-zero** or **mixed**: a mass at zero and a **continuous** part when binding. Many paths have **zero** payoff in many periods.
- **Positive or negative:** Path spread can be **positive** or **negative** depending on direction of congestion (flow vs FTR direction). So the **support** is real (both sides); not like power spot (non-negative).
- **Fat tails when binding:** When constraints **do** bind, shadow prices can be **large** (e.g. scarcity, outages). So **conditional on binding**, the spread can have **high variance** and **fat tails**. Unconditional distribution: **fat-tailed** and often **skewed**.
- **Mean reversion:** Congestion tends to **revert** (outages end, load patterns repeat). Over a month or season, average spread is mean-reverting around a level that depends on **topology** and **season**.
- **Seasonality:** Binding frequency and **level** of congestion vary by **season** (summer/winter demand, outages) and **hour type** (peak vs off-peak). Monthly or on-peak path spreads show **seasonal** patterns.
- **Discrete / structural:** Binding is **on/off** (constraint binds or not); outages are **events**. So the process has a **discrete** component (whether binding, which contingency) and a **continuous** component (shadow price level when binding).
- **Path-specific and correlation:** Each **path** has its own spread; paths sharing constraints are **correlated**. For a **portfolio** of FTRs, we need **joint** simulation of multiple path spreads (or constraint shadow prices) with **correlation** structure.

**Recommendations for simulation:**

| Use case | Recommended approach | Rationale |
|----------|------------------------|-----------|
| **Single path, monthly spread** | **Mixture:** (i) Probability $p$ of “no binding” (spread = 0); (ii) **conditional** spread when binding: **OU** or **OU + seasonality** (possibly with **heavy-tailed** or **jump** innovations). Calibrate $p$ and binding distribution from historical binding frequency and spread when non-zero. | Captures zero mass and mean reversion; fat tails when binding. |
| **Constraint shadow price** | **Regime-switching** or **jump-diffusion:** “Off” regime (shadow = 0) and “on” regime (positive shadow, mean-reverting or jump). Or **zero-inflated** OU: draw from OU only when “binding” (e.g. Bernoulli with probability from PCM or history). | Matches zero vs binding; spikes when binding. |
| **Portfolio of paths** | Simulate **constraint shadow prices** (one process per key constraint, with **correlation**), then form path spread = PTDF-weighted sum. Alternatively simulate **path spreads** with **correlation matrix** estimated from history (e.g. principal components or factor model). | Keeps constraint-level economics; correlation across paths. |
| **Outage impact** | **Scenario-based** or **event-driven:** Use **planned outage** calendar and **LODF** to shift which constraints bind; combine with a **stochastic** shadow-price model when binding. Or **bootstrap** historical spread by month/season and resample with correlation. | Structural (outages) + stochastic (level when binding). |

**Summary:** FTR “price” is **path spread** or **constraint shadow price**. It is **zero-inflated**, **mean-reverting when non-zero**, **fat-tailed** when binding, and **seasonal**. Use **mixture** (zero + conditional OU/jump) or **regime-switching**; for portfolios, simulate **correlated** constraint shadows or **correlated** path spreads.

---

### 8.2 Power market prices (spot and forwards)

**What we simulate:**  
**Spot:** LMP or hub price (e.g. hourly or block average — peak, off-peak). **Forwards:** Monthly or quarterly **base**, **peak**, **off-peak** (e.g. 5x16, 7x16) for valuation and curve evolution.

**Spot characteristics:**

- **Non-negative:** LMP can be zero or positive (and in some markets briefly negative). So the **support** is $[0, \infty)$ or, with negatives, $\mathbb{R}$; often **floor** at zero for modeling.
- **Strong mean reversion:** Supply/demand balance pulls price back; **half-life** is typically **hours to a few days**.
- **Seasonality:** **Daily** (peak vs off-peak), **weekly** (weekday vs weekend), **annual** (summer/winter). **Within-day** shape is critical for hourly simulation.
- **Spikes:** **Fat tails** and **positive skew**; **jumps** during scarcity or outages. **Regime** “normal” vs “stress” is common.
- **Volatility:** **State-dependent** (higher when price is high) and **time-dependent** (e.g. higher in peak hours or summer).

**Forward characteristics:**

- **Positive:** Forwards are quoted positive (price per MWh).
- **Log-returns** over short horizons are often **close to random walk** (low mean reversion); **correlation** across tenors (calendar structure).
- **Seasonality** in **level** (summer/winter strips); **volatility** can vary by tenor and season.

**Recommendations for simulation:**

| Object | Recommended process | Rationale |
|--------|---------------------|-----------|
| **Spot (hourly or block)** | **1-factor mean-reverting + seasonality** $\theta(t)$ (and optionally $\sigma(t)$). Add **jump-diffusion** or **regime-switch** if spikes are material for VaR or optionality. **Exponential OU** (positive price) or **OU in levels** with floor. | Mean reversion + seasonality; jumps for spikes. |
| **Spot, simple** | **OU + deterministic $\theta(t)$** (e.g. sinusoidal or monthly dummies); **heavy-tailed** (e.g. Student-t) innovations if no explicit jumps. | Tractable; fatter tails than Gaussian. |
| **Forward curve (single tenor)** | **GBM** for log-forward (or **OU** for short-tenor if mean reversion is observed). **Multi-factor** (e.g. short + long factor) for **full curve** with correlation across tenors. | Forwards often near random walk in log; multi-factor for curve. |
| **Multi-hub / multi-node** | **Correlated** processes (e.g. correlated OU or GBM); **correlation matrix** from historical returns or factor model. | Spread and basis risk. |

**Summary:** Power **spot** → **mean-reverting + seasonality + (optional) jumps or fat tails**; **forwards** → **GBM or multi-factor** in log-space with **correlation** across tenors and hubs.

---

### 8.3 Gas market prices (spot and forwards)

**What we simulate:**  
**Spot:** Hub price (e.g. daily or within-day) for physical/financial delivery. **Forwards:** Monthly, seasonal, or calendar strips (e.g. winter, summer, balance-of-season).

**Spot characteristics:**

- **Non-negative:** Gas price is positive (rarely zero at major hubs).
- **Mean reversion:** **Storage** and **seasonal demand** pull price toward a seasonal level; **half-life** typically **days to weeks**.
- **Seasonality:** **Strong** **annual** (winter vs summer); **within-season** (cold snaps, shoulder months). Less **within-day** structure than power (often daily or block).
- **Spikes:** **Less** spikey than power in many hubs, but **cold snaps** or **supply shocks** can cause **jumps** or **regimes**. **Positive skew** and **fat tails** in some periods.
- **Storage link:** **Prompt** vs **deferred** spread is related to **storage** and **convenience yield**; spot is influenced by inventory and refill/withdrawal season.

**Forward characteristics:**

- **Positive:** Forwards quoted positive ($/MMBtu).
- **Seasonal level:** Winter strip vs summer strip; **contango/backwardation** by season.
- **Log-returns** can be **mean-reverting** over short horizons (especially prompt) or **closer to random walk** for long-dated strips. **Correlation** across tenors (e.g. prompt vs next winter).

**Recommendations for simulation:**

| Object | Recommended process | Rationale |
|--------|---------------------|-----------|
| **Spot** | **OU with seasonal $\theta(t)$** (e.g. winter/summer or sinusoidal). **Exponential OU** if we want **positive** level and log-mean-reversion. Add **jump** or **regime** only if cold snaps/supply events are material. | Seasonality + mean reversion; gas less spikey than power. |
| **Spot, with storage** | **Two-factor:** **short-term** factor (mean-reverting, fast) + **long-term** or **seasonal** factor (slow or deterministic). Spot = sum (or exp of sum). | Separates prompt volatility from seasonal level. |
| **Forward curve** | **Multi-factor** (e.g. two-factor) for **curve** evolution; **correlation** across tenors. Or **GBM** per tenor with **correlation matrix** for simpler VaR. | Curve consistency; correlation. |
| **Basis (hub A − hub B)** | **OU** or **OU + seasonality** for **spread**; calibrate to historical basis. | Basis often mean-reverting. |

**Summary:** Gas **spot** → **mean-reverting + strong seasonality** ($\theta(t)$); **two-factor** if we separate short-term shock from seasonal level. Gas **forwards** → **multi-factor** or **correlated GBM** for curve. **Jumps** optional unless extreme events drive risk or optionality.

---

### 8.4 Cross-asset and FTR–power–gas

- **Power–gas:** **Correlation** (gas often marginal fuel); **spark spread** = power − heat rate × gas can be modeled as **spread** (OU or similar) or by simulating **both** with **correlation**.
- **FTR–power:** Path spread **depends on** LMPs (sink − source); FTR and power exposure are **linked**. Simulate **power** (or LMPs) and **derive** path spread from simulated LMPs and PTDFs; or simulate **path spread** directly with **correlation** to power price if that is sufficient for the use case.
- **Portfolio VaR:** Simulate **all** relevant underlyings (power spot/forwards, gas spot/forwards, FTR path spreads or constraint shadows) with **joint** distribution: **correlation** matrix or **factor** model estimated from history; use **appropriate** marginal process per asset (OU+jump for power spot, OU+seasonality for gas, mixture/regime for FTR spread).

---

## 9. One workflow to remember

1. **EDA:** Distribution (tails, skew, kurtosis), **ACF** (mean reversion), **seasonality**, **spikes**, **stationarity**.
2. **Choose process:** Match process to EDA (mean reversion ↔ OU family; spikes ↔ jumps or regimes; seasonality ↔ $\theta(t)$; fat tails ↔ jumps or heavy-tailed innovations).
3. **Calibrate:** Moments, MLE, or option-implied; check $\kappa$, $\sigma$, jump params.
4. **Simulate:** Exact where available (GBM, OU); otherwise Euler (or Milstein); many paths.
5. **Validate:** Simulated vs historical moments; backtest VaR or option fit; stress tests.

Then use the **simulated paths** for VaR, option pricing, storage valuation, or scenario analysis, with a clear understanding of the **model’s strengths and limitations**.
