# Value at Risk (VaR) in Energy Commodities: Methods, Copulas, and Portfolio VaR for FTR, Power, and Gas

A practical guide from the perspective of a seasoned quant in an energy commodity shop: what VaR is, the main methods to compute it, the role of **copulas**, VaR for **FTR**, **power**, and **gas** portfolios, pros/cons, common issues, and the **simulations** needed in the process.

---

## 1. What is VaR?

**Value at Risk (VaR)** is a **quantile** of the **distribution of loss** (or of minus P&amp;L) over a given **horizon** at a chosen **confidence level**. In words: “With probability $\alpha$ (e.g. 95% or 99%), the loss over the next $h$ days will not exceed VaR.”

**Definition (loss in dollars):** Let $L = -\Delta V$ be the **loss** over the horizon (so $L > 0$ when value **decreases**). Then
$$
\mathrm{VaR}_\alpha = \inf\bigl\{ x : \mathbb{P}(L \le x) \ge \alpha \bigr\} = \text{$\alpha$-quantile of $L$}.
$$
So **VaR at confidence $\alpha$** (e.g. 95%) is the **$(1-\alpha)$-quantile of the loss** — e.g. 95% VaR = 5th percentile of loss (or 95th percentile of the *negative* of P&amp;L). Often we say “95% VaR = $X$” meaning: with probability 95%, loss ≤ $X$.

**Horizon:** Usually **1-day** for trading risk; **10-day** for regulatory capital (e.g. scaled from 1-day). For energy, **1-day** is standard for limits; **multi-day** requires either **scaling** (e.g. $\sqrt{T}$ only if i.i.d.) or **multi-day simulation**.

**Why we use it:** **Limits** (desk, book, factor), **capital** (regulatory or economic), **comparison** across books, and **communication** with risk committees. VaR does **not** describe the **tail beyond** the quantile — for that we use **Expected Shortfall (ES)** or **stress tests**.

---

## 2. Formulas (reference)

**Loss and P&amp;L:** Portfolio value $V$; change over horizon $\Delta V$. Loss $L = -\Delta V$. So
$$
\mathbb{P}(L \le \mathrm{VaR}_\alpha) = \alpha \quad \Leftrightarrow \quad \mathbb{P}(\Delta V \ge -\mathrm{VaR}_\alpha) = \alpha.
$$

**Expected Shortfall (ES), conditional VaR (CVaR):** The **average loss** given that loss **exceeds** VaR:
$$
\mathrm{ES}_\alpha = \mathbb{E}[ L \mid L \ge \mathrm{VaR}_\alpha ].
$$
ES is **coherent** (subadditive); VaR is not. Regulators often require **ES** for the tail; VaR remains in wide use for **limits** and **reporting**.

**Scaling (1-day → T-day):** If **1-day** losses (or returns) are **i.i.d.** and we assume **square-root-of-time** for volatility, then
$$
\mathrm{VaR}_{\alpha,T\mathrm{-day}} \approx \sqrt{T} \cdot \mathrm{VaR}_{\alpha,1\mathrm{-day}}.
$$
This is **not** valid when returns are **autocorrelated** or **non-stationary**; then use **multi-day simulation** (simulate $T$ steps and compound P&amp;L).

---

## 3. Methods to compute VaR

We need the **distribution of $\Delta V$** (or $L$). That distribution comes from (1) **historical** realizations, (2) a **parametric** model for risk factors, or (3) **Monte Carlo** simulation. The **mapping** from **risk factors** to **portfolio value** can be **linear** (delta approximation) or **full revaluation**.

### 3.1 Historical simulation (HS)

**Idea:** Use **historical** changes in risk factors (e.g. past 1–2 years of daily path spreads, forward returns, vol changes). For each historical date, apply those **changes** to **today’s** risk factors, revalue the portfolio (or use **delta** approximation), and get a **historical** 1-day P&amp;L. **VaR** = empirical **$(1-\alpha)$-quantile** of that P&amp;L distribution (i.e. the $\alpha$-quantile of **loss** $L = -\Delta V$).

**Steps:**
1. Choose **risk factors** (e.g. path spreads, forward prices, vols).
2. Get **historical** series of 1-day **changes** $\{\Delta r_1, \ldots, \Delta r_T\}$ (e.g. $T = 500$ days).
3. For each date $s$, compute **hypothetical** P&amp;L: either **full revaluation** at $F_{\mathrm{today}} + \Delta r_s$, or **delta** (and optionally **gamma/vega**) approximation: $\Delta V_s \approx \sum_k \frac{\partial V}{\partial r_k} \Delta r_{s,k}$.
4. Order P&amp;L (or loss); **VaR** = $(1-\alpha)$-quantile of loss (e.g. 95% VaR = 95th percentile of loss = 5th percentile of P&amp;L).

**Formula (conceptual):** If $\{L_1, \ldots, L_T\}$ are historical losses, then $\mathrm{VaR}_\alpha \approx L_{(\lceil (1-\alpha)T \rceil)}$ (the appropriate order statistic).

**Pros:** No distributional assumption; uses **actual** history; captures **correlations** and **fat tails** that appeared in the sample.  
**Cons:** **Past** may not reflect **future** (regime change, new products); **limited** by sample size (e.g. 99% VaR with 500 days = 5th worst day — noisy); **no** scenarios **worse** than the worst in the sample.

### 3.2 Parametric (variance–covariance, delta-normal)

**Idea:** Assume **risk factor returns** (or changes) are **multivariate normal**. Map portfolio to risk factors via **delta** (first order). Then **P&amp;L** is **linear** in factor returns, so the **distribution of $\Delta V$** is **normal** with mean $\mu_V$ and variance $\sigma_V^2$. VaR = $\mu_V + \Phi^{-1}(\alpha) \cdot \sigma_V$ (for **loss** we use the left tail: $\mathrm{VaR}_\alpha = -\mu_V + \Phi^{-1}(1-\alpha) \cdot \sigma_V$; for typical short horizon $\mu_V \approx 0$, so $\mathrm{VaR}_\alpha \approx \Phi^{-1}(1-\alpha) \cdot \sigma_V$).

**Setup:** Risk factor vector $\mathbf{r}$; 1-day change $\Delta\mathbf{r}$. **Delta** vector $\boldsymbol{\delta}$: $\delta_k = \frac{\partial V}{\partial r_k}$. Then
$$
\Delta V \approx \boldsymbol{\delta}^\top \Delta\mathbf{r}, \qquad \mathbb{E}[\Delta V] \approx \boldsymbol{\delta}^\top \boldsymbol{\mu}, \qquad \mathrm{Var}(\Delta V) \approx \boldsymbol{\delta}^\top \boldsymbol{\Sigma}\, \boldsymbol{\delta},
$$
where $\boldsymbol{\mu}$ = mean of $\Delta\mathbf{r}$, $\boldsymbol{\Sigma}$ = covariance of $\Delta\mathbf{r}$. So
$$
\mathrm{VaR}_\alpha \approx -\boldsymbol{\delta}^\top \boldsymbol{\mu} + \Phi^{-1}(1-\alpha) \cdot \sqrt{\boldsymbol{\delta}^\top \boldsymbol{\Sigma}\, \boldsymbol{\delta}}.
$$
If $\boldsymbol{\mu} = \mathbf{0}$: $\mathrm{VaR}_\alpha = \Phi^{-1}(1-\alpha) \cdot \sigma_V$ (e.g. 95% → $\Phi^{-1}(0.95) \approx 1.65$, 99% → $\approx 2.33$).

**Pros:** **Fast**; **analytical**; easy to **decompose** VaR by factor (marginal VaR).  
**Cons:** **Normal** assumption **understates** tail risk (energy has **fat tails**, **skew**); **delta-only** ignores **gamma** and **vega** (options); **correlation** can **break down** in stress.

### 3.3 Monte Carlo (MC) VaR

**Idea:** **Simulate** many (e.g. 10k–100k) **scenarios** of risk factor **changes** from a **calibrated** joint distribution; for each scenario **revalue** the portfolio (full revaluation or delta–gamma–vega); **VaR** = empirical **$(1-\alpha)$-quantile** of the simulated **loss** distribution.

**Steps:**
1. **Specify** joint distribution of $\Delta\mathbf{r}$ (e.g. multivariate normal, **t**, or **copula** + marginals).
2. **Calibrate** (means, covariances, correlations, tail parameters) from history or option-implied.
3. **Draw** $N$ independent scenarios $\{\Delta\mathbf{r}^{(1)}, \ldots, \Delta\mathbf{r}^{(N)}\}$.
4. For each $i$: compute $\Delta V^{(i)}$ (full reval or Taylor); $L^{(i)} = -\Delta V^{(i)}$.
5. **VaR** = empirical $(1-\alpha)$-quantile of $\{L^{(i)}\}$ (e.g. sort and take the $\lceil (1-\alpha)N \rceil$-th largest loss).

**Pros:** Can use **fat-tailed** or **skewed** marginals and **copulas**; **full revaluation** captures **gamma**, **vega**, **path-dependence**; **flexible**.  
**Cons:** **Computational cost** (many pricings); **model risk** (distribution and correlation choice); **validation** needed (backtest, stress).

### 3.4 Hybrid and filtered approaches

- **Filtered historical simulation:** Use **historical** scenarios but **scale** each scenario by **current** volatility (e.g. GARCH) so that **today’s** vol is reflected. Reduces **stale** vol in plain HS.
- **Hybrid parametric + MC:** **Parametric** (e.g. normal or t) for **factor** distribution; **MC** for **revaluation** (delta–gamma–vega or full reval). Balances speed and non-linearity.
- **Stress VaR:** **Predefined** stress scenarios (e.g. 2008 crisis, COVID, freeze); report **loss** under each; **no** probability attached — used alongside statistical VaR.

---

## 4. Copulas: why and how

**Problem:** We have **many** risk factors (path spreads, forwards, vols) with **different** marginal distributions (e.g. path spread **zero-inflated**, power returns **fat-tailed**, gas **seasonal**). **Correlation** alone (e.g. Gaussian) does **not** fix **joint tails** — in stress, **correlations** often **increase** (tail dependence). A **copula** separates **marginal** distributions from **dependence structure**.

**Definition:** A **copula** $C(u_1, \ldots, u_n)$ is a **multivariate** cdf on $[0,1]^n$ with **uniform** marginals. By **Sklar’s theorem**, any joint cdf $F(x_1,\ldots,x_n)$ with marginals $F_1, \ldots, F_n$ can be written
$$
F(x_1, \ldots, x_n) = C\bigl(F_1(x_1), \ldots, F_n(x_n)\bigr).
$$
So we **specify** marginals $F_k$ and **dependence** via $C$; **simulation**: draw $(U_1,\ldots,U_n) \sim C$, then $X_k = F_k^{-1}(U_k)$.

**Common copulas in risk:**

| Copula | Dependence | Tail dependence | Use |
|--------|------------|-----------------|-----|
| **Gaussian** | Correlation matrix $\boldsymbol{\rho}$ | None (thin tails) | Baseline; fast. |
| **Student-t** | $\boldsymbol{\rho}$ + **degrees of freedom** $\nu$ | **Symmetric** tail dependence (joint extremes) | Fatter tails; stress. |
| **Clayton** | Asymmetric | **Lower** tail (joint crashes) | When we care about joint downside. |
| **Gumbel** | Asymmetric | **Upper** tail (joint spikes) | When we care about joint upside. |
| **Empirical** | From **rank** correlation / historical joint ranks | Data-driven | No parametric copula; use **empirical** copula or **reorder** historical draws. |

**Simulation with copula:** (1) **Calibrate** marginals $F_k$ (e.g. empirical, normal, t, mixture) and copula $C$ (e.g. fit $\boldsymbol{\rho}$ and $\nu$ for t-copula). (2) Draw $(U_1,\ldots,U_n)$ from $C$. (3) Set $X_k = F_k^{-1}(U_k)$. (4) Use $\mathbf{X}$ as **risk factor** scenario; revalue portfolio.

**Pros of copulas:** **Flexible** marginals (e.g. zero-inflated for FTR, skewed for power) + **controlled** dependence and **tail dependence**.  
**Cons:** **Calibration** (which copula, how to estimate); **high dimension** (many factors) can be **noisy**; **stability** of tail dependence estimates.

---

## 5. VaR for FTR portfolio

**Risk factors:** (1) **Path spread** per path (and optionally per period), or (2) **Constraint shadow prices** $\mu_\ell$ (then path value = PTDF-weighted sum). **Correlation** across paths (or constraints) is **critical** — paths that share constraints have **correlated** payoffs.

### 5.1 Mapping (FTR)

**Path-spread as factor:** For path $p$, position $Q_p$ (MW), remaining MW·h = $H_p$. Change in value:
$$
\Delta V_p \approx Q_p \cdot H_p \cdot \Delta(\text{path spread}_p).
$$
**Constraint-based:** $\Delta\mu_\ell$ = change in shadow price of constraint $\ell$; then
$$
\Delta V \approx \sum_p Q_p \cdot H_p \cdot \sum_\ell \mathrm{PTDF}_{\ell,p} \cdot \Delta\mu_\ell = \sum_\ell \Delta\mu_\ell \cdot \sum_p Q_p\, H_p\, \mathrm{PTDF}_{\ell,p}.
$$
So we can work with **constraint** factors $\Delta\mu_\ell$ and **loadings** $\sum_p Q_p H_p\, \mathrm{PTDF}_{\ell,p}$ per $\ell$.

### 5.2 Distributional issues (FTR)

- **Zero-inflation:** Path spread is **zero** when constraints don’t bind; **non-zero** (positive or negative) when they do. **Marginal** distribution is **mixed** (point mass at 0 + continuous). **Gaussian** VaR is **wrong**; use **historical** (empirical distribution), **mixture** (prob of binding × conditional distribution), or **copula** with **zero-inflated** marginal for path spread.
- **Correlation:** Paths sharing constraints are **correlated**; **correlation matrix** of path spreads (or of constraint shadows) from **historical** realizations or **PCM** scenarios. **Copula** (e.g. t) can capture **tail dependence** (many paths bad at once).
- **Tenor:** Remaining MW·h **decreases** over time; **vol** of path spread may **change** with time to settlement. Use **tenor-specific** vol or **scaling** in the mapping.

### 5.3 Simulations needed (FTR)

| Simulation | Purpose |
|------------|--------|
| **Historical path spreads (or shadows)** | Historical VaR: apply historical $\Delta(\text{spread})$ to current position. |
| **Joint scenarios of constraint shadows** | MC VaR: simulate $\Delta\mu_\ell$ from calibrated distribution (e.g. multivariate normal/t or **copula** + marginals that allow **zeros** and **spikes**). |
| **PCM / fundamental scenarios** | **Stress** or **scenario** VaR: run PCM under **outage** or **demand** scenarios; get **shadow** and **path spread** distribution; combine with **probability** of scenario if desired. |
| **Topology / outage draws** | **Regime** uncertainty: draw **which** outages occur; for each topology get **PTDF/LODF** and **shadow** distribution; **aggregate** to path spread distribution. |

### 5.4 Pros and cons (FTR VaR)

| Pros | Cons |
|------|------|
| **PTDF mapping** gives **parsimonious** factors (constraints) and **portfolio** diversification. | **No** liquid market → **no** market-implied distribution; **model** and **history** driven. |
| **Historical** VaR uses **actual** spread/shadow history (including zeros and spikes). | **Zero-inflation** and **non-normality** → **parametric** (delta-normal) **understates** tail. |
| **Copula** + **zero-inflated** (or mixture) marginals can improve **tail** and **joint** behavior. | **Topology** change (outage) can **shift** PTDFs and **correlations**; **stale** correlation in stress. |

---

## 6. VaR for Power portfolio

**Risk factors:** **Forward** prices (by hub, block, delivery), **volatility** (by strike/expiry), and optionally **correlation** (e.g. for spread options). Positions: **forwards**, **options** (vanilla, Asian, cap/floor, spread), **shaped** deals.

### 6.1 Mapping (Power)

**Delta (forwards):** $\Delta V \approx \sum_{\mathrm{tenors}} \frac{\partial V}{\partial F}\, \Delta F$; sensitivity = **volume × hours** (or MMBtu for gas).  
**Delta–gamma–vega (options):** $\Delta V \approx \Delta\, \Delta F + \frac{1}{2}\Gamma\, (\Delta F)^2 + \mathrm{Vega}\, \Delta\sigma + \cdots$. For **many** underlyings, **risk factors** = vector of **forward returns** and **vol changes**; **covariance** matrix from history or implied.

**Full revaluation:** For each scenario of $\Delta F$, $\Delta\sigma$, **reprice** every option (Black, Asian, Kirk); sum. **Slower** but **accurate** for **gamma** and **vega**.

### 6.2 Distributional issues (Power)

- **Fat tails and skew:** Power **returns** and **spikes** are **non-normal**; **delta-normal** VaR **understates** risk. Use **historical** or **MC** with **t** or **jump** marginals; **copula** for **multi-hub** / **multi-tenor**.
- **Vol risk:** **Vega** is material for options; **vol** changes must be **simulated** (e.g. from **historical** vol changes or **vol-of-vol**). **Correlation** between **forward** and **vol** (e.g. vol rises when price spikes) can be captured in **copula** or **joint** MC.
- **Many underlyings:** **Dimension** (hubs × blocks × months) is large; **factor** model (e.g. few principal components) or **block**-level aggregation reduces dimension; **correlation** matrix must be **positive semi-definite** and **stable**.

### 6.3 Simulations needed (Power)

| Simulation | Purpose |
|------------|--------|
| **Historical forward (and vol) returns** | Historical VaR: apply historical $\Delta F$, $\Delta\sigma$ to current curve/surface; revalue. |
| **Correlated forward + vol scenarios** | MC VaR: draw from **joint** distribution (e.g. **copula** + marginals: lognormal or t for forwards, normal or scaled for vol changes). |
| **Path simulation for path-dependent** | **Asian**, **storage**, **shaped**: simulate **paths** of spot/forward over the contract period; value at each path; **distribution** of value change for VaR. |
| **Spike / jump scenarios** | **Stress**: add **jump** component or **regime** (e.g. high-vol regime); **fat-tailed** innovations (e.g. Student-t). |

### 6.4 Pros and cons (Power VaR)

| Pros | Cons |
|------|------|
| **Liquid** forwards (and some options) → **good** history and **implied** vol for **parametric**/MC. | **Many** underlyings → **curse of dimension**; **factor** or **aggregation** needed. |
| **Full revaluation** (MC) captures **gamma**, **vega**, **smile**. | **Delta-normal** **understates** option book risk; **vol** and **correlation** assumptions matter. |
| **Historical** VaR **no** distributional assumption; **MC + copula** for **tail** and **dependence**. | **Spikes** and **regime** changes can **break** historical and parametric VaR. |

---

## 7. VaR for Gas portfolio

**Risk factors:** **Forward** prices (hub × delivery), **volatility**, **basis** (hub − Henry), **correlation** (e.g. for **spark** or **basis** options). Positions: **forwards**, **options**, **storage**, **spread** deals.

### 7.1 Mapping (Gas)

Same **logic** as power: **delta** for forwards ($\Delta V \approx \sum \frac{\partial V}{\partial F}\, \Delta F$); **delta–gamma–vega** for options; **full revaluation** for **storage** and **spread** options (Kirk, MC). **Basis** risk: factor = **spread** between two hubs; **correlation** between **Henry** and **basis** (or **regional** hub) from history.

### 7.2 Distributional issues (Gas)

- **Seasonality:** **Winter** vs **summer** vol and **correlation** can differ; **calibrate** by season or use **seasonal** parameters.
- **Extreme events:** **Freezes**, **supply** shocks → **fat tails**; **t-copula** or **stress** scenarios.
- **Storage:** **Path-dependent**; value depends on **path** of prices; VaR via **MC** of **paths** and **revaluation** of storage optionality.

### 7.3 Simulations needed (Gas)

| Simulation | Purpose |
|------------|--------|
| **Historical forward (and vol, basis) returns** | Historical VaR. |
| **Correlated forwards + vol + basis** | MC VaR; **copula** for **joint** (e.g. Henry, basis, regional). |
| **Storage:** **Price paths** over contract | **LSM** or **tree** for storage value; **distribution** of $\Delta V$ from **path** scenarios. |
| **Freeze / stress** | **Stress** VaR: apply **historical** or **hypothetical** shock (e.g. winter 2021). |

### 7.4 Pros and cons (Gas VaR)

| Pros | Cons |
|------|------|
| **Liquid** Henry (and some hubs) → **good** data for **parametric**/MC. | **Basis** and **regional** **thinner** → **noisier** correlation and vol. |
| **Standard** models (Black, Kirk) for **revaluation** in MC. | **Storage** and **spread** options **complex**; **path** simulation **costly**. |

---

## 8. Summary: methods and when to use

| Method | Best for | FTR | Power | Gas |
|--------|----------|-----|--------|-----|
| **Historical** | No distributional assumption; use **actual** history | ✓ (path spread / shadow history) | ✓ (forward/vol history) | ✓ (forward/vol/basis history) |
| **Parametric (delta-normal)** | **Speed**; **linear** books | Limited (non-normal spreads) | Forwards only; **understates** options | Forwards only |
| **MC (full reval)** | **Options**, **non-linearity**, **path-dependent** | ✓ (with proper marginals) | ✓ (gamma, vega, Asian, spread) | ✓ (options, storage) |
| **Copula** | **Joint** distribution with **flexible** marginals and **tail dependence** | ✓ (path spreads / shadows) | ✓ (multi-hub, forward+vol) | ✓ (Henry + basis + vol) |

---

## 9. Common issues and pitfalls

| Issue | What goes wrong | Mitigation |
|-------|------------------|------------|
| **Non-linearity** | **Delta-only** VaR **understates** option and **gamma** risk. | **Delta–gamma** (second order) or **full revaluation** in MC. |
| **Fat tails** | **Normal** assumption **understates** tail; **too few** exceedances in backtest. | **Historical** VaR; **t** or **copula** (e.g. t-copula); **ES** alongside VaR. |
| **Correlation breakdown** | In **stress**, correlations **increase** (everything moves together); **Gaussian** understates **joint** tail. | **t-copula** or **stress** scenarios; **conservative** correlation in stress. |
| **Zero-inflation (FTR)** | **Gaussian** or **lognormal** for path spread is **wrong** (mass at zero). | **Mixture** or **empirical** marginal; **historical** or **MC** with **correct** marginal. |
| **Liquidity** | **Mark** may not be **realizable** in crisis; **VaR** assumes we can **hold** or **exit** at mark. | **Liquidity** adjustment (e.g. **holding period** scaling, **haircut**); **stress** with **wider** bid–ask. |
| **Scaling (1d → 10d)** | $\sqrt{10}$ **invalid** if returns **autocorrelated** or **non-stationary**. | **Multi-day** simulation (simulate $T$ days, compound P&amp;L). |
| **Backtesting** | **Too many** VaR exceedances → VaR **understated**; **too few** → **overstated** or **clustering**. | **Traffic light** (e.g. Basel); **conditional** coverage tests; **update** model (vol, correlation, tail). |
| **Model risk** | **Distribution**, **copula**, **mapping** are **chosen**; wrong choice **biases** VaR. | **Document** assumptions; **validate** (backtest, stress); **conservative** where uncertain. |

---

## 10. Simulations in the VaR process: checklist

| Step | What to simulate | Used in |
|------|-------------------|--------|
| **Risk factor scenarios** | **Joint** draws of 1-day (or T-day) **changes** in risk factors (path spreads, forwards, vols, basis). Margination: **empirical**, **normal**, **t**, **mixture**. Dependence: **correlation** matrix or **copula** (Gaussian, t, etc.). | Historical (actual history); Parametric (mean/cov); MC VaR (scenario draws). |
| **Copula + marginals** | **Marginals** per factor (e.g. zero-inflated for FTR spread, t for power return); **copula** for **joint** (t for tail dependence). Draw $(U_1,\ldots,U_n)$, invert to factors. | MC VaR with **non-normal** joint. |
| **Full revaluation** | For each **scenario** of factors, **reprice** portfolio (options, storage, shaped). Produces **scenario** P&amp;L; **VaR** = quantile of scenario losses. | MC VaR for **non-linear** books. |
| **Path simulation** | **Paths** of spot/forward over **contract** period (e.g. OU + seasonality + jump). For **path-dependent** (Asian, storage, shaped): value at each path; **distribution** of value. | VaR for **path-dependent** power/gas; **storage** VaR. |
| **PCM / fundamental** | **Constraint shadows** (or path spreads) from **PCM** runs under **outage** or **demand** scenarios. Use as **scenarios** or to **calibrate** distribution. | FTR **stress** / **scenario** VaR; **calibration** of shadow distribution. |
| **Topology / outage** | **Draw** outage sets; for each, **PTDF/LODF** and **shadow** distribution. **Aggregate** to path spread distribution. | FTR **regime** uncertainty; **scenario** VaR. |
| **Backtest** | **Compare** **realized** 1-day P&amp;L to **VaR** each day; count **exceedances**; test **coverage** and **independence**. | **Validation** of VaR model. |

---

## 11. One-page recap

- **VaR** = **$(1-\alpha)$-quantile of loss** over a horizon (e.g. 1-day, 95% or 99%). Used for **limits**, **capital**, **reporting**.
- **Methods:** **Historical** (empirical quantile of historical P&amp;L); **Parametric** (delta-normal, Gaussian factors); **Monte Carlo** (draw scenarios, revalue, empirical quantile). **Hybrid** and **filtered** variants exist.
- **Copulas** separate **marginals** from **dependence**; allow **fat-tailed** or **zero-inflated** marginals + **tail dependence** (e.g. t-copula). **Simulation:** draw from copula, invert marginals to get **joint** factor scenarios.
- **FTR VaR:** Risk factors = **path spread** or **constraint shadows**; **PTDF** mapping; **zero-inflation** and **correlation** critical; use **historical** or **MC** with **appropriate** marginals (mixture/empirical) and **copula**. Simulations: historical spreads/shadows, **joint** shadow scenarios, **PCM**/topology scenarios.
- **Power VaR:** Risk factors = **forwards**, **vol**; **delta–gamma–vega** or **full reval**; **fat tails** and **many** underlyings; **copula** for **multi-hub** and **forward+vol**. Simulations: historical returns, **correlated** forward+vol, **path** simulation for path-dependent.
- **Gas VaR:** Similar to power; add **basis** and **storage** (path simulation). **Seasonality** and **freeze** stress.
- **Issues:** Non-linearity (use full reval or delta–gamma); **fat tails** (avoid pure normal); **correlation breakdown** (copula/stress); **zero-inflation** (FTR); **liquidity**; **scaling**; **backtest** and **model risk**.
- **Simulations** in the process: **risk factor** scenarios (joint), **copula** + marginals, **full revaluation**, **path** simulation (path-dependent), **PCM**/topology (FTR), **backtest**.
