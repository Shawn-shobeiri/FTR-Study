# Basis: Definition, Methodologies to Model It, Pros/Cons, and Issues (FTR, Power, Gas)

A practical guide from a quant perspective: what **basis** is, **methodologies** to model it, **pros and cons** of each, and **issues** specific to **FTR**, **power**, and **gas**.

---

## 1. What is basis?

**Basis** is the **price difference** between two related but distinct price series. It is a **risk factor** when we have **exposure** at one location or product but **hedge** or **mark** at another (liquid) reference.

**Types:**

- **Location basis:** Price at **location A** minus price at **location B** (e.g. gas: regional hub − Henry Hub; power: nodal LMP − hub index).
- **Product basis:** Price of one **product** minus another (e.g. **peak** − **off-peak**; one delivery month minus another = **calendar spread**). Calendar spread is sometimes called **time basis**.

**Formulas (reference):**

- **Location basis (power):** $B_t = \lambda_{\mathrm{node},t} - \lambda_{\mathrm{hub},t}$ ($/MWh), where $\lambda$ = LMP or SPP.
- **Location basis (gas):** $B_t = P_{\mathrm{hub}\,A,t} - P_{\mathrm{Henry},t}$ ($/MMBtu).
- **General:** $B_{A,B}(t) = P_A(t) - P_B(t)$.

**Why it matters:** **Curve building** (we need a **basis curve** to get forward at A from forward at B); **valuation** (MtM of position at A uses $F^A = F^B + \text{basis}$); **VaR** (basis is a risk factor); **hedging** (hedge in liquid B, exposure at A → basis risk). Modeling basis is needed whenever **location** or **product** mismatch exists.

---

## 2. Methodologies to model basis

Below are the main **approaches**, with **formulas** where useful, and **pros/cons**. Choice depends on **market** (FTR vs power vs gas), **data**, and **use** (curve, VaR, stress).

### 2.1 Historical average / mean reversion

**Idea:** Assume basis **reverts** to a **long-run mean** (possibly **seasonal**). **Curve:** basis curve = **historical average** basis by delivery month (or winter vs summer). **Dynamic:** $B_t = \theta + (B_{t-1} - \theta)\rho + \varepsilon_t$ (AR(1)) or discrete-time OU: $\mathbb{E}[B_{t+k}] = \theta + (B_t - \theta)\rho^k$.

**Formula (OU in levels):** $dB_t = \kappa(\theta - B_t)\,dt + \sigma\,dW_t$; conditional mean $\mathbb{E}[B_T \mid B_0] = \theta + (B_0 - \theta)e^{-\kappa T}$.

**Pros:** Simple; **no** structural assumptions; uses **observed** spread; **mean reversion** matches many empirical basis series.  
**Cons:** **Backward-looking**; **ignores** current fundamentals (pipeline, storage, load); **wrong** when **regime** changes (new pipe, demand shift, outage).

---

### 2.2 Regression on fundamental drivers

**Idea:** $B_t = \mathbf{x}_t^\top \boldsymbol{\beta} + \varepsilon_t$, where $\mathbf{x}_t$ = drivers (pipeline utilization, local demand, storage, congestion, season dummies). **Forecast:** $\widehat{B}_T = \mathbf{x}_T^\top \widehat{\boldsymbol{\beta}}$ using **forecasted** or **current** $\mathbf{x}_T$.

**Drivers (examples):**

- **Gas:** HDD/CDD, **storage** level, **pipeline** capacity or utilization, **production** (local), **season** dummies.
- **Power:** **Load**, **flow** on interfaces, **outage** dummies, **renewables**, **hour**/day type.
- **FTR:** Path spread regressed on **load**, **outage** dummies, **season** (see FTR section).

**Pros:** **Links** basis to **observables**; **interpretable**; can **forecast** from forecasted fundamentals; **stress** by shocking $\mathbf{x}$.  
**Cons:** **Data** on $\mathbf{x}$; **omitted** variable bias; **linearity**; **residuals** may be **heteroskedastic** or **autocorrelated** (use WLS, HAC SEs, or time-series errors).

---

### 2.3 Time series (AR, ARIMA, cointegration)

**Idea:** Model **basis** (or **levels** of $P_A$ and $P_B$ with **cointegration**) as **AR** or **ARIMA**. **AR(1):** $B_t = c + \phi B_{t-1} + \varepsilon_t$; **cointegration:** $P_A$ and $P_B$ cointegrated $\Rightarrow$ basis $B = P_A - P_B$ is **stationary**; model $B_t$ as AR or ARIMA.

**Formula:** Forecast $\mathbb{E}[B_{t+k}]$ from AR(1): $\mathbb{E}[B_{t+k}] = \frac{c}{1-\phi} + (B_t - \frac{c}{1-\phi})\phi^k$ (mean-reverting to $c/(1-\phi)$).

**Pros:** **Persistence** and **mean reversion**; good for **short-term** forecast and **simulation** (e.g. VaR); **no** need for fundamental data.  
**Cons:** **No** fundamentals; **long-run** level can **shift** (structural break); must check **stationarity** (unit root tests); **out-of-sample** can degrade if regime changes.

---

### 2.4 Structural / cost-based (congestion, transport)

**Idea:** **Power:** Basis (node − hub) ≈ **congestion component** of LMP = $\sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{node}}$ (relative to hub as reference). Build basis from **PCM** or **DC OPF** (shadow prices × PTDFs). **Gas:** Basis ≈ **transport cost** + **optionality** (pipeline capacity, storage access); sometimes $B = f(\text{capacity}, \text{distance}, \text{demand})$.

**Formula (power):** $\lambda_{\mathrm{node}} - \lambda_{\mathrm{hub}} = \sum_\ell \mu_\ell \cdot (\mathrm{PTDF}_{\ell,\mathrm{node}} - \mathrm{PTDF}_{\ell,\mathrm{hub}})$ (difference of shift factors to node vs hub).

**Pros:** **Theoretically grounded**; can **stress** with **outage** or **capacity** change; **consistent** with **physics** (power flow, pipeline).  
**Cons:** **Data-intensive** (PCM, pipeline data); **model risk**; observed basis can **spike** or go **negative** beyond “cost” (scarcity, congestion spikes); **calibration** can be hard.

---

### 2.5 Correlated processes (simulate both legs)

**Idea:** Model **both** $P_A$ and $P_B$ (e.g. two correlated **GBM** or **OU** processes); **basis** = $B_t = P_{A,t} - P_{B,t}$ by **construction**. **Correlation** $\rho$ and **volatilities** $\sigma_A$, $\sigma_B$ determine **basis** vol: $\mathrm{Var}(B) = \sigma_A^2 + \sigma_B^2 - 2\rho\sigma_A\sigma_B$.

**Pros:** **Joint** distribution for **portfolio** VaR; **basis** and **level** risk **consistent**; **spread options** (Kirk) use this structure.  
**Cons:** **Two** curves and **two** vol surfaces (and **correlation**) to maintain; **basis** is **derived** (no direct mean reversion on $B$ unless both legs are mean-reverting).

---

### 2.6 Option-implied / market-consistent

**Idea:** Where **basis options** or **spread options** trade, **imply** basis **distribution** or **volatility** from **option** prices (e.g. **Kirk** on spread $P_A - P_B$). Use **implied** vol (and correlation) for **valuation** and **VaR**.

**Pros:** **Market-consistent**; reflects **risk premium** and **tail**.  
**Cons:** **Only** where options exist; **liquidity** often **thin** for basis options; **coverage** (tenors, hubs) limited.

---

### 2.7 Hybrid

**Idea:** Combine methods: e.g. **historical** shape for basis curve + **regression** adjustment for **current** fundamentals; or **structural** (PCM) for **power** node basis + **historical** for **residual**; or **cointegration** for **long-run** level + **AR** for **short-run** dynamics.

**Pros:** **Flexible**; can fit **better** and use **strengths** of each.  
**Cons:** **Complexity** and **maintenance**; **multiple** assumptions to validate.

---

## 3. Pros and cons by methodology (summary table)

| Method | Pros | Cons |
|--------|------|------|
| **Historical average / mean reversion** | Simple; robust; uses observed spread; mean reversion | Backward-looking; ignores fundamentals; regime change |
| **Regression (fundamentals)** | Uses drivers; interpretable; forecastable; stress via $\mathbf{x}$ | Data on $\mathbf{x}$; linearity; omitted vars; heteroskedasticity/autocorrelation |
| **Time series (AR/ARIMA/cointegration)** | Persistence; short-term forecast; simulation; no fundamental data | No fundamentals; structural break; stationarity required |
| **Structural / cost-based** | Theoretic; stress (outage, capacity); physics-consistent | Data-intensive; model risk; basis can exceed “cost” |
| **Correlated processes** | Joint distribution; portfolio VaR; spread options | Two curves/vols + correlation; basis derived |
| **Option-implied** | Market-consistent; tail | Liquidity; coverage |
| **Hybrid** | Flexible; better fit | Complexity; maintenance |

---

## 4. FTR: basis in context and issues

### 4.1 What “basis” means for FTR

In FTR we rarely use the word **“basis”**; the analogous object is **path spread** (sink price − source price). It is a **spread between two locations** (nodes or hubs). So **path spread** = **basis** between sink and source. It can be **decomposed** into **congestion** (and **losses**) relative to a reference:

$$
\text{Path spread} = \lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}} = \sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}.
$$

So “modeling basis” for FTR = **modeling path spread** (or **constraint shadow prices** and **PTDFs**).

### 4.2 Methodologies (FTR)

| Approach | How | Typical use |
|----------|-----|-------------|
| **Structural (PCM)** | Run **PCM**; get **shadow prices** $\mu_\ell$ and **PTDFs**; path spread = $\sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}$. | **Fair value**, **scenario** (outage, load). |
| **Historical** | **Historical** path spread (or shadow) by **hour**, **day type**, **season**; **mean** or **distribution** for curve / VaR. | **Curve** (expected spread); **VaR** (distribution). |
| **Regression** | Regress **path spread** (or **shadow**) on **load**, **outage** dummies, **renewables**, **season**. | **Forecast** spread from **forecasted** fundamentals. |
| **Time series** | **AR** or **mean-reverting** on **path spread** (or **shadow**); **cointegration** if modeling sink and source LMPs separately. | **Short-term** forecast; **simulation** for VaR. |

### 4.3 Issues (FTR)

| Issue | What goes wrong | Mitigation |
|------|------------------|------------|
| **Zero-inflation** | Path spread = **0** when constraints **don’t bind**; **mixed** distribution (mass at 0 + continuous). | **Two-part** or **mixture** model; **conditional** model (spread \| binding); **historical** distribution including zeros. |
| **Topology change** | **Outage** → **PTDFs** and **LODFs** change → **path spread** distribution **shifts**. | **Scenario** by **outage**; **MC** over **topologies**; **update** PTDFs when topology changes. |
| **No liquid basis market** | Path spread is **not** traded; **no** market-implied basis curve. | **Model-based** (PCM, historical, regression); **IPV** not available. |
| **Correlation across paths** | Paths that **share** constraints have **correlated** spreads; **portfolio** VaR needs **joint** distribution. | **Correlation** matrix of path spreads (or shadows); **copula** or **factor** model. |

---

## 5. Power: basis in context and issues

### 5.1 What basis means (power)

**Basis** = **nodal LMP** − **hub** (or zone) index, $B_t = \lambda_{\mathrm{node},t} - \lambda_{\mathrm{hub},t}$ ($/MWh). Driven by **congestion** and **losses**: basis ≈ **congestion component** at node (relative to hub) + **loss** component.

### 5.2 Methodologies (power)

| Approach | How | Typical use |
|----------|-----|-------------|
| **Historical average** | **Historical** average basis by **node**, **month**, **hour** (or block). | **Basis curve** for curve building; **simple** VaR. |
| **Regression** | Regress **basis** on **load**, **flow**, **interface**, **outage** dummies, **renewables**. | **Forecast** basis from fundamentals; **stress** (high load, outage). |
| **Structural (PCM / DC OPF)** | **PCM** or **DC OPF** → **congestion** component at node = basis (if hub is reference). | **Scenario** and **stress**; **consistent** with **constraints**. |
| **Time series** | **AR** or **ARIMA** on basis; **cointegration** (node and hub LMP). Basis often **mean-reverting**. | **Short-term** forecast; **simulation** for VaR. |

### 5.3 Issues (power)

| Issue | What goes wrong | Mitigation |
|-------|------------------|------------|
| **Zero vs spike** | Basis can be **zero** (no congestion) or **spike** (severe congestion); **heteroskedastic** (high vol when basis large). | **Two-part** or **quantile** regression; **WLS** or **robust** SEs; **full** distribution (not just mean). |
| **Many nodes** | **Many** basis series (one per node or per node–hub pair) → **curse of dimension**; **maintenance** and **data**. | **Factor** model (e.g. few **constraint** factors × PTDF); **aggregate** by zone; **prioritize** liquid or material nodes. |
| **Shape (hourly)** | **Shaped** exposure needs **hourly** (or block) basis; **average** basis ≠ **value** of hourly exposure. | **HPFC** at node vs hub; **hourly** basis profile; **shape** risk. |

---

## 6. Gas: basis in context and issues

### 6.1 What basis means (gas)

**Basis** = **regional hub** − **Henry Hub** (or other benchmark), $B_t = P_{\mathrm{hub}\,A,t} - P_{\mathrm{Henry},t}$ ($/MMBtu). Driven by **transport** cost, **local** supply/demand balance, **storage**, **pipeline** capacity.

### 6.2 Methodologies (gas)

| Approach | How | Typical use |
|----------|-----|-------------|
| **Historical average** | **Historical** average basis by **month** or **season** (winter vs summer). | **Basis curve**; **simple** forward at regional hub = Henry + basis. |
| **Regression** | Regress **basis** on **HDD/CDD**, **storage** level, **pipeline** utilization, **production**, **season** dummies. | **Forecast** and **stress** (cold snap, low storage). |
| **Time series** | **AR** or **ARIMA**; **cointegration** (hub A and Henry). Basis often **mean-reverting**. | **Short-term** forecast; **simulation** for VaR. |
| **Cost-based** | Basis ≈ **transport** tariff + **optionality** (rough). | **Floor** or **anchor**; less used for **full** curve. |

### 6.3 Issues (gas)

| Issue | What goes wrong | Mitigation |
|-------|------------------|------------|
| **Basis can go negative** | **Regional** oversupply or **pipeline** reversal → basis **negative**. | **No** sign constraint in model (OLS on spread); **quantile** regression for **tails**. |
| **Seasonality** | **Winter** premium at **demand** hubs; **summer** different. | **Seasonal** dummies or **separate** model by season; **historical** by month. |
| **Thin liquidity** | **Regional** hub **thinner** than Henry → **noisier** curve and **vol**; **IPV** harder. | **Wider** reserves; **conservative** curve; **stress** basis. |
| **Extreme events** | **Freeze** (e.g. Texas) → **basis** (and **Henry**) **spike**; **tail** dependence. | **Stress** scenarios; **quantile** regression; **fat-tailed** or **copula** for VaR. |
| **Correlation (Henry–basis)** | **Spread options** and **portfolio** VaR need **joint** (Henry, basis) or **correlation**. | **Correlated** processes; **Kirk** or **MC** with **correlation**; **copula**. |

---

## 7. Formulas (reference)

**Basis (definition):**
$$
B_{A,B}(t) = P_A(t) - P_B(t).
$$

**Path spread (FTR), same structure as basis between two nodes:**
$$
\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}} = \sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}.
$$

**Forward basis curve (valuation):** MtM of basis position (long A, short B):
$$
V_{\mathrm{basis}} = (F_{0,T}^A - F_{0,T}^B) \times Q,
$$
where $F_{0,T}^A$, $F_{0,T}^B$ = forward prices at A and B for delivery $T$, $Q$ = volume.

**Regression:** $B_t = \mathbf{x}_t^\top \boldsymbol{\beta} + \varepsilon_t$; forecast $\mathbb{E}[B_T] = \mathbf{x}_T^\top \widehat{\boldsymbol{\beta}}$.

**Mean-reverting (OU):** $dB_t = \kappa(\theta - B_t)\,dt + \sigma\,dW_t$; $\mathbb{E}[B_T \mid B_0] = \theta + (B_0 - \theta)e^{-\kappa T}$; stationary variance $\mathrm{Var}(B_\infty) = \sigma^2/(2\kappa)$.

**Correlated legs:** If $P_A$ and $P_B$ have variances $\sigma_A^2$, $\sigma_B^2$ and correlation $\rho$, then $\mathrm{Var}(B) = \sigma_A^2 + \sigma_B^2 - 2\rho\,\sigma_A\,\sigma_B$.

---

## 8. One-page recap

- **Basis** = price at **A** minus price at **B** (location or product). **Risk factor** for **curve**, **valuation**, **VaR**, **hedging** when exposure is at A and hedge/mark at B.
- **Methodologies:** **Historical** average / mean reversion (simple, backward-looking); **regression** on fundamentals (interpretable, needs data); **time series** (AR/cointegration, short-term forecast); **structural** (PCM for power, transport for gas); **correlated processes** (joint for VaR); **option-implied** (where available); **hybrid**.
- **FTR:** Path spread = **basis** between sink and source; modeled via **congestion** (shadows × PTDF). **Issues:** **zero-inflation**, **topology** change, **no** liquid basis market, **correlation** across paths.
- **Power:** Basis = **node − hub**; **congestion** and **losses**. **Issues:** **zero vs spike**, **heteroskedasticity**, **many** nodes, **shape** (hourly).
- **Gas:** Basis = **hub − Henry**; **transport** and **local** balance. **Issues:** **negative** basis, **seasonality**, **thin** liquidity, **extreme** events, **correlation** Henry–basis.
- **Pros/cons** and **issues** drive **choice** of methodology by **market** and **use case** (curve vs VaR vs stress).
