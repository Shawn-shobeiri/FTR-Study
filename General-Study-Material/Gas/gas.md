# Gas Modeling, Storage, and Swing: Methods, Pros/Cons, Assumptions, and Formulas

A practical guide from the perspective of a **seasoned gas trader**: **gas price modeling**, **storage** (physical and valuation), **swing** (optionality on quantity), **methods** used, with **pros**, **cons**, **assumptions**, and **formulas**.

---

## 1. Gas price modeling

### 1.1 What we model

**Spot** price ($/MMBtu) at a hub (e.g. Henry Hub): **daily** or **within-day** for physical/financial delivery. **Forward** curve: **monthly**, **seasonal** (winter, summer), or **calendar** strips. **Drivers**: **demand** (temperature HDD/CDD, power burn, industrial), **supply** (production, LNG, imports), **storage** (inventory, inject/withdraw), **pipeline** capacity.

**Uses:** **Curve** building, **valuation** (forwards, options, storage, swing), **VaR** and **stress** (price paths), **trading** (rich/cheap vs model).

### 1.2 Methods for gas price modeling

| Method | Idea | Typical use |
|--------|------|-------------|
| **Curve from quotes** | Build **forward** curve from **NYMEX/ICE** and **broker** quotes; **interpolate** (e.g. cubic spline, seasonal) for non-quoted tenors. **Spot** = prompt forward or **separate** prompt model. | **Mark** and **delta**; **level** and **term structure**. |
| **Demand regression** | **Price** (or log price) on **HDD**, **CDD**, **storage** level, **production**, **season** dummies: $P_t = \mathbf{x}_t^\top \boldsymbol{\beta} + \varepsilon_t$. **Forecast** $P$ from **forecasted** weather and storage. | **Short-term** price **forecast**; **stress** (cold snap = high HDD). |
| **Mean-reverting (OU) spot** | Spot $S_t$ follows $dS_t = \kappa(\theta(t) - S_t)\,dt + \sigma\,dW_t$ with **seasonal** $\theta(t)$ (e.g. winter vs summer). **Calibrate** $\kappa$, $\sigma$, $\theta(t)$ from history. | **Simulation** for **VaR**, **storage** valuation; **positive** price via **exponential OU** or floor. |
| **Two-factor (spot)** | **Short-term** factor (mean-reverting, fast) + **long-term** or **seasonal** factor (slow or deterministic). $S_t = X_t + \theta(t)$ or $S_t = e^{X_t + \theta(t)}$. | **Separate** **prompt** volatility from **seasonal** level; **storage** and **swing** valuation. |
| **Multi-factor (curve)** | **Forward** curve as **multi-factor** (e.g. level + slope); **correlation** across tenors. **Simulate** curve for **VaR** or **path-dependent** products. | **Curve** **evolution**; **consistent** **forwards** and **spot**. |
| **Structural (supply–demand)** | **Supply** curve (production, storage withdrawal) and **demand** (HDD/CDD, power); **clear** at **equilibrium**. **Data-intensive** (balance, storage, flows). | **Fundamental** **view**; **stress** (low storage, cold snap). |

### 1.3 Key formulas (gas price)

**HDD (heating degree days):** $\mathrm{HDD}_t = \max(0, T_{\mathrm{base}} - T_t)$ (e.g. $T_{\mathrm{base}} = 65°F$). **CDD (cooling):** $\mathrm{CDD}_t = \max(0, T_t - T_{\mathrm{base}})$. **Demand** often modeled as linear in HDD/CDD.

**OU with seasonality:** $dS_t = \kappa(\theta(t) - S_t)\,dt + \sigma\,dW_t$; $\theta(t)$ = seasonal level (e.g. sinusoidal or monthly dummies). **Conditional** mean: $\mathbb{E}[S_T \mid S_0] = \theta(T) + (S_0 - \theta(0))e^{-\kappa T}$.

**Exponential OU (positive price):** $\ln S_t = X_t$ with $dX_t = \kappa(\theta - X_t)\,dt + \sigma\,dW_t$ ⇒ $S_t$ positive and **mean-reverting** in log.

**Regression:** $P_t = \beta_0 + \beta_1 \mathrm{HDD}_t + \beta_2 \mathrm{CDD}_t + \beta_3 \mathrm{Storage}_t + \beta_4 P_{\mathrm{gas},t-1} + \varepsilon_t$ (example); **forecast** = $\mathbf{x}_{\mathrm{forecast}}^\top \widehat{\boldsymbol{\beta}}$.

---

## 2. Storage

### 2.1 What is gas storage?

**Physical** storage (salt caverns, aquifers, depleted reservoirs, LNG) allows **inject** when price is **low** and **withdraw** when price is **high**, capturing **calendar spread** minus **costs**. **Constraints**: **working gas** (inventory min/max), **injection** and **withdrawal** **rates** (MMBtu/day), **cycle** limits (e.g. one fill/empty per year). **Value** = **optionality** to use the **spread** over time, not just **one** fixed trade.

### 2.2 Storage valuation: methods

| Method | Idea | Pros | Cons |
|--------|------|------|------|
| **Intrinsic (static)** | **Fixed** inject/withdraw **schedule** (e.g. fill in summer, empty in winter) at **forward** prices. Value = $\sum_t (P_t^{\mathrm{withdraw}} - P_t^{\mathrm{inject}} - c) \cdot q_t$ for **optimal** fixed $q_t$ subject to **capacity** and **rates**. | **Simple**; **lower bound** on value. | **Ignores** **optionality** (no response to **path**). |
| **Tree (binomial/trinomial)** | **Discrete** **price** tree; at each **node** decide **inject / withdraw / hold** to **maximize** expected **discounted** profit. **Backward** induction with **inventory** and **rate** constraints. | **Optimal** **exercise**; **path-dependent**. | **Curse of dimension** (state = inventory × time × price); **discrete** time/price. |
| **LSM (Least-Squares Monte Carlo)** | **Simulate** many **price paths**; at each **exercise** date **regress** **continuation value** on **state** (e.g. price, inventory); **compare** **exercise** value vs **continuation**; **forward** pass for **optimal** strategy. **Value** = average **discounted** cash flow over paths. | **Handles** **path-dependent** constraints; **flexible**; **multi-factor** price. | **Approximation** (regression); **many** paths needed; **calibration** of price process. |
| **Rolling intrinsic** | **Re-optimize** **fixed** schedule **each** period using **then-current** forwards ( **rolling** intrinsic). **Approximation** to optionality. | **Simpler** than full **tree/LSM**. | **Not** true **optimal**; **understates** value when **vol** is high. |

### 2.3 Storage: formulas and constraints

**Inventory:** $I_{t+1} = I_t + q_t^{\mathrm{inj}} - q_t^{\mathrm{wd}}$ (inject $q^{\mathrm{inj}}$, withdraw $q^{\mathrm{wd}}$). **Bounds:** $I_{\min} \le I_t \le I_{\max}$ (working gas). **Rates:** $0 \le q_t^{\mathrm{inj}} \le R_{\mathrm{inj}}$, $0 \le q_t^{\mathrm{wd}} \le R_{\mathrm{wd}}$ (MMBtu/day). **Cycle:** Sometimes **annual** **delivery** obligation or **inject/withdraw** limits per **season**.

**Cash flow (one period):** Withdraw: revenue $P_t \cdot q_t^{\mathrm{wd}}$; inject: cost $P_t \cdot q_t^{\mathrm{inj}}$; **net** = $P_t (q_t^{\mathrm{wd}} - q_t^{\mathrm{inj}}) - c_t$ (storage cost $c_t$). **Value** = $\mathbb{E}\bigl[\sum_t D(t) \cdot \text{cash flow}_t \bigr]$ under **optimal** strategy.

**Spread (winter − summer):** Storage operator **buys** summer (inject), **sells** winter (withdraw). **Gross** margin ≈ **winter** price − **summer** price − **storage cost** ($/MMBtu). **Optionality**: **when** to inject/withdraw and **how much** (within rates) depends on **path** of prices.

### 2.4 Storage: assumptions

| Assumption | Caveat |
|------------|--------|
| **Known** **forward** curve and **price process** | **Curve** and **vol** are **inputs**; **wrong** curve/vol → **wrong** value. |
| **No** **bid–ask** or **slippage** | **Execution** at **mid**; reality can have **liquidity** cost. |
| **Constraints** **correct** (rates, working gas) | **Operational** **limits** may **differ** from **contract**; **cycle** and **ratchets** matter. |
| **Single** **hub** (or **basis** fixed) | **Location** **spread** (e.g. Henry vs storage hub) can **move**. |

---

## 3. Swing

### 3.1 What is swing?

**Swing** (or **take-or-pay** with **swing**) = right, but **not** obligation, to take **variable quantity** within **limits** at a **strike** price. **Daily** (or **period**) **nomination**: holder chooses **volume** within **min/max per day** and **min/max over contract**. **Physical** delivery at **strike**; **value** = **optionality** to take **more** when **spot** is **high** and **less** when **spot** is **low**. So it is a **strip of American-style** daily options with **cumulative** and **daily** constraints.

### 3.2 Swing: constraints

- **Daily** **min** $q_{\min}^{\mathrm{day}}$ and **max** $q_{\max}^{\mathrm{day}}$ (MMBtu/day).
- **Contract** **min** $Q_{\min}^{\mathrm{tot}}$ and **max** $Q_{\max}^{\mathrm{tot}}$ (total over contract).
- **Strike** $K$ ($/MMBtu); **pay** $K \times q$ for **quantity** $q$ taken. **Value** of **optionality** = $\mathbb{E}\bigl[\sum_t D(t) \cdot (S_t - K)^+ \cdot q_t^* \bigr]$ (simplified; actual has **optimal** $q_t^*$ subject to **constraints**).

### 3.3 Swing valuation: methods

| Method | Idea | Pros | Cons |
|--------|------|------|------|
| **Tree** | **Price** tree + **state** (remaining **volume** flexibility, days left). **Backward** induction: at each node, **choose** $q_t$ in $[q_{\min}, q_{\max}]$ to **maximize** immediate payoff + **expected** continuation. **State space** = (price, remaining min, remaining max, days). | **Optimal** **exercise**; **exact** for **discrete** setup. | **State** **explosion** (volume × time × price); **hard** for **long** tenor or **fine** volume grid. |
| **LSM** | **Simulate** **price** paths; at each **nomination** date **regress** **continuation value** on **state** (price, **remaining** volume **headroom**, days left). **Optimal** $q_t$ = argmax over **feasible** $q$ of (exercise + continuation). **Forward** pass; **average** discounted cash flow. | **Handles** **path-dependent** and **volume** constraints; **scalable**. | **Approximation**; **design** of **basis functions** (state variables) matters. |
| **Bounded daily option** | **Approximate** swing as **strip** of **daily** options with **notional** = $q_{\max}^{\mathrm{day}} - q_{\min}^{\mathrm{day}}$ (optional part). **Value** ≈ sum of **Black** (or **daily** option) values. **Ignores** **cumulative** constraint. | **Fast**; **closed-form**. | **Wrong** when **cumulative** **binding** (e.g. must take **min** total); **overstates** value. |
| **Hybrid (intrinsic + optionality)** | **Decompose** into **base** (e.g. take **min** every day at strike) + **optional** (extra volume up to **max**). Value **optional** part by **tree** or **LSM** with **reduced** state. | **Interpretable**; **reduces** dimension. | **Approximation**; **interaction** of **min/max** and **path** can be subtle. |

### 3.4 Swing: formulas

**Payoff (one day):** Take $q_t$ at **strike** $K$; **spot** $S_t$. **Cash flow** = $q_t \cdot (S_t - K)$ (physical: we **receive** gas worth $S_t$, **pay** $K \cdot q_t$). **Optionality**: choose $q_t \in [q_{\min}, q_{\max}]$ (and satisfy **cumulative** $Q_{\min}^{\mathrm{tot}} \le \sum_s q_s \le Q_{\max}^{\mathrm{tot}}$).

**Simplified (no cumulative):** **Daily** optional volume = $q_{\max}^{\mathrm{day}} - q_{\min}^{\mathrm{day}}$. **Value** of **optional** part ≈ $(q_{\max}^{\mathrm{day}} - q_{\min}^{\mathrm{day}}) \cdot \sum_t D(t) \cdot \mathbb{E}[(S_t - K)^+]$ (strip of **calls**). **With** cumulative: **dynamic programming** or **LSM**.

**Bellman (conceptual):** $V(t, I, S) = \max_{q \in \mathcal{F}(t,I)} \bigl\{ q(S - K) \Delta t + D(t)\, \mathbb{E}[V(t+1, I - q, S_{t+1}) \mid S_t = S] \bigr\}$, where $I$ = remaining **obligation** or **headroom** and $\mathcal{F}(t,I)$ = **feasible** $q$ given **daily** and **cumulative** limits.

### 3.5 Swing: assumptions

| Assumption | Caveat |
|------------|--------|
| **Known** **price process** (and **curve**) | **Vol** and **path** distribution **drive** value; **wrong** process → **wrong** value. |
| **No** **nomination** **frictions** | **Lead time**, **scheduling** (e.g. pipeline **nomination** deadlines) can **constrain** **exercise**. |
| **Strike** **fixed** | **Indexed** strike (e.g. spot + spread) changes **optionality**. |
| **Single** **hub** | **Basis** (delivery point vs reference) can **move**. |

---

## 4. Pros and cons (summary)

### 4.1 Gas price modeling

| Method | Pros | Cons |
|--------|------|------|
| **Curve from quotes** | **Observable**; **consistent** with **market**. | **No** **forward-looking** **fundamental**; **extrapolation** for **long** tenors. |
| **Demand regression** | **Uses** **HDD/CDD**, **storage**; **interpretable**; **stress** via **weather**. | **Linear**; **omitted** vars (supply shock); **stationarity**. |
| **OU / exponential OU** | **Mean reversion**; **seasonality** $\theta(t)$; **tractable**; **simulation** easy. | **Thin tails**; **no** **jump** (freeze); **single** factor. |
| **Two-factor** | **Separates** **short** and **long**; **better** **fit** to **term structure**. | **More** **parameters**; **calibration** harder. |
| **Structural** | **Fundamental**; **stress** (storage, demand). | **Data**; **complex**; **model** risk. |

### 4.2 Storage valuation

| Method | Pros | Cons |
|--------|------|------|
| **Intrinsic** | **Simple**; **lower bound**; **no** **path** model. | **Ignores** **optionality**; **understates** value. |
| **Tree** | **Optimal** **exercise**; **exact** (discrete). | **Dimension**; **slow** for **large** state. |
| **LSM** | **Path-dependent**; **flexible**; **scalable**. | **Approximation**; **basis** choice; **paths**. |
| **Rolling intrinsic** | **Simpler** than **LSM**. | **Not** **optimal**; **understates** when **vol** high. |

### 4.3 Swing valuation

| Method | Pros | Cons |
|--------|------|------|
| **Tree** | **Optimal** **nomination**; **exact** (discrete). | **State** **explosion** (volume × time). |
| **LSM** | **Handles** **constraints**; **scalable**. | **Approximation**; **state** **variables** design. |
| **Bounded daily option** | **Fast**; **closed-form**. | **Ignores** **cumulative**; **can** **overstate**. |
| **Hybrid** | **Interpretable**; **reduced** dimension. | **Approximation**. |

---

## 5. Assumptions (cross-cutting)

| Area | Typical assumption | Caveat |
|------|---------------------|--------|
| **Price process** | **Mean-reverting** (OU) or **two-factor**; **seasonal** $\theta(t)$; **known** vol. | **Jumps** (freeze); **regime** change; **vol** **stochastic**. |
| **Curve** | **Consistent** with **quotes**; **no arbitrage** (e.g. **storage** spread **bounds**). | **Illiquid** tenors; **basis** **risk**. |
| **Storage constraints** | **Known** **rates**, **working gas**, **cycle**. | **Operational** vs **contract**; **ratchets**. |
| **Swing constraints** | **Known** **daily** and **total** min/max; **no** **lead time**. | **Nomination** **rules**; **scheduling**. |
| **Discounting** | **Risk-free** (or **funding**) **rate**; **no** **counterparty** risk. | **Funding** **spread**; **collateral**. |

---

## 6. Formulas (reference)

**OU (spot):** $dS_t = \kappa(\theta(t) - S_t)\,dt + \sigma\,dW_t$; $\mathbb{E}[S_T \mid S_0] = \theta(T) + (S_0 - \theta(0))e^{-\kappa T}$.

**Exponential OU:** $\ln S_t = X_t$, $dX_t = \kappa(\theta - X_t)\,dt + \sigma\,dW_t$ ⇒ $S_t > 0$.

**Storage inventory:** $I_{t+1} = I_t + q_t^{\mathrm{inj}} - q_t^{\mathrm{wd}}$; $I_{\min} \le I_t \le I_{\max}$; rate limits $q_t^{\mathrm{inj}} \le R_{\mathrm{inj}}$, $q_t^{\mathrm{wd}} \le R_{\mathrm{wd}}$.

**Storage cash flow (one period):** $\mathrm{CF}_t = P_t (q_t^{\mathrm{wd}} - q_t^{\mathrm{inj}}) - c_t$ (withdraw revenue − inject cost − storage cost).

**Swing (daily):** Optional volume band $[q_{\min}, q_{\max}]$; payoff $\approx q_t (S_t - K)$; cumulative $\sum_t q_t \in [Q_{\min}^{\mathrm{tot}}, Q_{\max}^{\mathrm{tot}}]$.

**Winter–summer spread:** $\Delta P = P_{\mathrm{winter}} - P_{\mathrm{summer}}$; storage **gross** margin ≈ $\Delta P$ − **storage cost** ($/MMBtu).

---

## 7. One-page recap

- **Gas modeling:** **Spot** (OU, exponential OU, two-factor) and **forward** curve (quotes, interpolation); **demand** (HDD/CDD) **regression**; **structural** (supply–demand). **Formulas:** OU, exponential OU, regression; **seasonality** $\theta(t)$. **Pros/cons:** Curve = observable vs no fundamental; regression = interpretable vs linear; OU = tractable vs thin tails.
- **Storage:** **Inject** when **cheap**, **withdraw** when **dear**; **constraints** = working gas, **inject/withdraw** rates. **Methods:** **Intrinsic** (static schedule), **tree**, **LSM**, **rolling** intrinsic. **Value** = **optionality** on **calendar** spread. **Assumptions:** Known curve/process, constraints correct, single hub.
- **Swing:** **Variable** **quantity** within **daily** and **total** min/max at **strike**; **daily** **nomination**. **Methods:** **Tree**, **LSM**, **bounded** daily option (approx), **hybrid**. **Formulas:** Payoff $q(S-K)$; **Bellman** for **optimal** $q$; **cumulative** constraint. **Assumptions:** Known price process, no nomination frictions.
- **Pros/cons** and **assumptions** drive **choice** of **method** by **product** (curve, storage, swing) and **use** (mark, VaR, stress, trading).
