# Energy Options: Products, Valuation, Mark-to-Market, and Risk Management

A practical guide from the perspective of a seasoned option trader: product types, how we value them, how we mark them, how we manage risk, and what we expect from the risk manager.

---

## 1. Option products in energy: what we trade

Energy options are written on **underlyings** that are often **forwards** (e.g. monthly peak power, winter gas strip) or **averages** (e.g. daily average price, monthly average). Settlement can be **cash** (difference between reference price and strike) or **physical** (right to buy/sell at strike). Below we outline the main **product types** and how they differ from plain equity/rate options.

---

### 1.1 Vanilla calls and puts (European)

- **Underlying:** A **single** forward or index (e.g. ERCOT North 5x16 peak for a given month, or Henry Hub gas for a given month). Settlement at **expiry** $T$ against a **reference price** $S_T$ (e.g. average of daily settlements, or final day price, depending on contract).
- **Payoff:** Call: $\max(S_T - K, 0)$; Put: $\max(K - S_T, 0)$. Usually **cash-settled** in $/MWh or $/MMBtu per unit of volume (e.g. 1 MW × hours in period).
- **Where they trade:** OTC and, in some markets, listed (e.g. CME, ICE). Common for **power** (hub × block × month) and **gas** (hub × month or strip).
- **Trader use:** Directional view, hedging forward exposure, cap/floor on cost or revenue.

---

### 1.2 Asian (average-price) options

- **Underlying:** The **average** of the reference price over a **fixing period** (e.g. daily fixes over the contract month). So payoff is on $\bar{S} = \frac{1}{n}\sum_{i=1}^n S_{t_i}$, not on $S_T$.
- **Payoff:** Call: $\max(\bar{S} - K, 0)$; Put: $\max(K - \bar{S}, 0)$. Often **cash-settled**; volume = quantity × number of hours (or days) in the period.
- **Why they exist:** Closer to **physical** exposure (buyer cares about average cost, not one day). **Less volatility** than European on spot (averaging smooths), so typically **cheaper** than European at same strike for same period.
- **Trader use:** Hedging **average** price risk; often embedded in supply contracts or sold as a cap/floor on average price.

---

### 1.3 Spread options

- **Underlying:** **Difference** (or ratio) between two prices. Common types:
  - **Spark spread:** Power price − heat rate × Gas price (e.g. $S_{\mathrm{power}} - H \times S_{\mathrm{gas}}$). Option on this spread (e.g. call = right to capture spread when positive).
  - **Basis spread:** Hub A − Hub B (e.g. ERCOT North − Houston Ship Channel).
  - **Calendar spread:** Forward month $i$ − Forward month $j$ (e.g. Summer − Winter).
- **Payoff:** Call: $\max(S_1 - H \cdot S_2 - K, 0)$ (spark); or $\max(S_1 - S_2 - K, 0)$ (basis/calendar). $K$ is often 0.
- **No closed form** under standard Black–Scholes (spread is difference of two lognormals). Valued by **closed-form approximation** (e.g. Kirk, Margrabe-type) or **Monte Carlo**.
- **Trader use:** Generation optionality (spark), location arbitrage (basis), calendar structure (calendar spread option).

---

### 1.4 Swing options (physical)

- **Underlying:** **Right**, but not obligation, to take **variable quantity** within a **band** (min/max per day, min/max over the period) at a **strike** price. Often **daily** exercise: each day the holder can nominate within the band.
- **Payoff:** Physical delivery at strike; **value** = optionality to take more when spot is high and less when spot is low. So it is a **strip of American-style** daily options with **cumulative** and **daily** constraints.
- **Valuation:** **Tree** or **Monte Carlo** with **optimal exercise** (dynamic programming or least-squares Monte Carlo). Constraints make it path-dependent and high-dimensional.
- **Trader use:** Gas and power **physical** optionality; storage-like value; often sold with long-term supply.

---

### 1.5 Caps, floors, and collars

- **Cap:** Series of **call options** (e.g. one per month); buyer is protected if **average price** (or settlement price) for that month is **above** strike. Payoff each month: $\max(\bar{S} - K, 0) \times \text{volume}$.
- **Floor:** Series of **put options**; buyer is protected if price is **below** strike.
- **Collar:** Long cap + short floor (or vice versa). Limits upside and downside; can be zero-cost by choosing strikes.
- **Underlying:** Usually **monthly** average or **block** (e.g. 5x16) price; each “caplet”/“floorlet” is an **Asian** or **European** option on that month.
- **Trader use:** Cost protection (cap), revenue protection (floor), or structured hedge (collar).

---

### 1.6 Optionality embedded in physical contracts

- **Take-or-pay** with **swing:** Minimum volume at fixed price + right to take more at same (or tiered) price within limits.
- **Indexed** deals with **caps/floors:** Price = index ± spread, but **capped** or **floored** (explicit optionality).
- **Valuation:** Decompose into **forward** + **option** (cap/floor/swing); value the option via same tools (Black, Asian, Monte Carlo, or tree).

---

### 1.7 Summary: product types and main valuation approach

| Product           | Underlying              | Payoff type        | Typical valuation              |
|-------------------|-------------------------|--------------------|---------------------------------|
| Vanilla Euro call/put | Single forward/index | $\max(S_T - K, 0)$ etc. | Black(-76) on forward           |
| Asian call/put    | Average price $\bar{S}$ | $\max(\bar{S} - K, 0)$ etc. | Closed-form (e.g. Levy) or MC   |
| Spread option     | $S_1 - H S_2$ or $S_1 - S_2$ | $\max(\text{spread} - K, 0)$ | Kirk/Margrabe approx or MC      |
| Swing             | Daily quantity band    | Physical at strike | Tree or LSM with constraints    |
| Cap / floor       | Strip of monthly options | Sum of caplets/floorlets | Strip of Black or Asian        |

---

## 2. Valuation

### 2.1 Inputs

- **Forward curve:** For each delivery period (month, block), we need the **forward price** $F_{0,T}$. This comes from the **curve-building** process (term structure). Option value is sensitive to **level** (delta).
- **Volatility:** For each expiry/delivery and strike we need **volatility** $\sigma$. In energy we often have:
  - **Flat vol** per expiry (one number per month/option).
  - **Vol surface:** $\sigma(K, T)$ — strike (or delta) and term. Can be **quoted** (broker) or **implied** from liquid options; otherwise **historical** or **model-based**.
- **Discounting:** Risk-free rate (e.g. OIS) and, if relevant, **funding spread** for uncollateralized. Discount factor $D(T)$ from the **rates curve**.
- **Strike and notional:** Strike $K$; notional = quantity × volume (e.g. MW × hours, or MMBtu).

### 2.2 Black(-76) for vanilla on forward

**Assumptions:**

- The **forward** $F_{t,T}$ (or the **spot** at $T$ that settles the option) follows a **lognormal** distribution at expiry: $\ln F_{T,T}$ is normal with mean $\ln F_{0,T} - \frac{1}{2}\sigma^2 T$ and variance $\sigma^2 T$ under the pricing measure.
- **Volatility** $\sigma$ is **constant** (no smile, no term structure of vol).
- **Interest rates** are deterministic; discount factor $D(T)$ is known.
- **No dividends** (or convenience yield) between now and $T$ — or they are already in the forward.
- **Frictionless** trading, no arbitrage; settlement is **cash** at $T$ on the reference price.

**Formulas:**

- **Call:** $C = D(T)\bigl[ F_{0,T} \Phi(d_1) - K \Phi(d_2) \bigr]$.
- **Put:** $P = D(T)\bigl[ K \Phi(-d_2) - F_{0,T} \Phi(-d_1) \bigr]$.
- **Where:** $d_1 = \frac{\ln(F_{0,T}/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $\quad d_2 = d_1 - \sigma\sqrt{T}$, and $\Phi$ is the standard normal cdf.

**Greeks (Black-76, call):**

- **Delta:** $\Delta_{\mathrm{call}} = D(T)\, \Phi(d_1)$. Put: $\Delta_{\mathrm{put}} = -D(T)\, \Phi(-d_1)$.
- **Gamma:** $\Gamma = D(T)\, \frac{\phi(d_1)}{F_{0,T}\,\sigma\sqrt{T}}$ (same for call and put), with $\phi = \Phi'$.
- **Vega:** $\mathrm{Vega} = D(T)\, F_{0,T}\, \phi(d_1)\, \sqrt{T}$ (per 1% move in $\sigma$: multiply by 0.01).
- **Theta:** $\Theta = -\frac{D(T)\, F_{0,T}\, \phi(d_1)\, \sigma}{2\sqrt{T}} + \mathrm{drift\ term}$ (drift from $D(T)$ and possibly $F$; often quoted as calendar decay).

**Pros:** Closed-form; fast; easy Greeks; standard for vanillas; good for **forwards** when vol is quoted per expiry.  
**Cons:** No **vol smile**; no **mean reversion** (spot); **thin tails**; wrong for **path-dependent** or **multi-asset** payoffs.

---

### 2.3 Asian options

**Assumptions (closed-form, e.g. Levy / Turnbull–Wakeman):**

- **Arithmetic average** $\bar{S} = \frac{1}{n}\sum_{i=1}^n S_{t_i}$ is approximated by a **lognormal** (or moment-matched lognormal) distribution. Exact lognormality of $\bar{S}$ does **not** hold when $S_t$ is lognormal; the formula is an **approximation** using first two moments of $\bar{S}$.
- **Fixings** $t_1, \ldots, t_n$ and forward curve $F_{0,t_i}$ and vols $\sigma_i$ (or constant $\sigma$) are given; **no** early exercise.
- **Rates** deterministic; **cash** settlement at expiry on $\bar{S}$.

**Formulas (conceptual):**

- **Levy-type:** Moment-match $\bar{S}$ to a lognormal: set $E[\bar{S}] = M_1$, $E[\bar{S}^2] = M_2$ from the (lognormal) process for $S_t$; then $\ln \bar{S}$ is approximated as normal with mean $m = 2\ln M_1 - \frac{1}{2}\ln M_2$ and variance $v^2 = \ln M_2 - 2\ln M_1$. Call value:
  $$C_{\mathrm{Asian}} \approx D(T)\bigl[ e^{m + v^2/2}\, \Phi(d_1) - K\, \Phi(d_2) \bigr], \quad d_1 = \frac{m - \ln K + v^2}{v}, \quad d_2 = d_1 - v.$$
- **Turnbull–Wakeman:** Similar idea with a **continuously sampled** average approximation; uses moments of the geometric average and a correction. Exact expressions are in the literature; implementation is standard in many systems.
- **Monte Carlo:** $C \approx D(T)\, \frac{1}{N}\sum_{j=1}^N \max(\bar{S}_j - K, 0)$ where $\bar{S}_j$ is the average along the $j$-th path. No closed-form Greeks; bump **forward** and **vol** for delta and vega.

**Pros:** Closed-form (Levy/TW) is **fast** and adequate for many **average-price** caps/floors; **smoothing** reduces vol vs European so price is lower.  
**Cons:** **Approximation** only (arithmetic avg is not lognormal); **discrete** fixings need correct moment formulas; **Greeks** less standard; for **complex** path or **correlation** across dates, **Monte Carlo** is preferred.

---

### 2.4 Spread options

**Assumptions (Kirk-type):**

- **Two underlyings** $S_1$, $S_2$ (e.g. power and gas) are **lognormal** at expiry with correlation $\rho$: $\ln S_1 \sim N(\mu_1, \sigma_1^2)$, $\ln S_2 \sim N(\mu_2, \sigma_2^2)$, $\mathrm{corr}(\ln S_1, \ln S_2) = \rho$.
- **Forward** prices $F_1$, $F_2$ and vols $\sigma_1$, $\sigma_2$ (and $\rho$) are given; **strike** $K$ (often 0 for spark).
- **Cash** settlement at $T$ on $\max(S_1 - H S_2 - K, 0)$; **rates** deterministic.

**Formulas (Kirk approximation for call on $S_1 - H S_2 - K$):**

- Define **composite** forward and vol: $F_c = F_1 - H F_2 - K$ (or adjusted so the “underlying” is positive), and
  $$\sigma_c^2 = \sigma_1^2 + \left( \frac{H F_2}{F_1 - K} \right)^2 \sigma_2^2 - 2\rho\, \sigma_1\, \sigma_2\, \frac{H F_2}{F_1 - K}.$$
- Then **call** (on $S_1 - H S_2 - K$) is approximated as **Black** on $F_1 - H F_2 - K$ with vol $\sigma_c$:
  $$C_{\mathrm{spread}} \approx D(T)\bigl[ (F_1 - H F_2 - K) \Phi(d_1) \bigr] \quad \text{if } F_1 - H F_2 > K, \quad d_1 = \frac{\ln((F_1 - K)/(H F_2)) + \frac{1}{2}\sigma_c^2 T}{\sigma_c \sqrt{T}}.$$
  (Exact Kirk formula uses $d_2 = d_1 - \sigma_c\sqrt{T}$ and the same structure as Black; see literature for the full expression. Some implementations use $F_{\mathrm{eff}} = F_1 / (H F_2 + K)$ and a modified vol.)
- **Margrabe** (exchange option, $K=0$): closed form for option on $S_1 - H S_2$ when both are lognormal: $C = D(T)\bigl[ F_1 \Phi(d_1) - H F_2 \Phi(d_2) \bigr]$ with $d_1 = \frac{\ln(F_1/(H F_2)) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$, $\sigma^2 = \sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2$.

**Pros:** **Fast**; no simulation; good for **spark** and **basis** when inputs are available; **Greeks** via finite difference on the formula.  
**Cons:** **Approximation** (spread is not lognormal); **correlation** and vol inputs are critical; **negative spread** or **extreme** $K$ can be unstable; **path-dependent** or **non-Gaussian** spread needs **Monte Carlo**.

**Monte Carlo (spread):** Simulate **both** underlyings with **correlation** $\rho$ (e.g. correlated lognormal or mean-reverting); payoff $\max(S_1 - H S_2 - K, 0)$; discount and average over paths. Use when **joint** distribution is non-Gaussian or payoff is **path-dependent**.

### 2.5 Swing and path-dependent optionality

**Assumptions:**

- **Spot** (or forward) follows a **given** process (e.g. lognormal or mean-reverting); **daily** exercise dates; **volume constraints**: min/max per day, min/max cumulative over the period.
- **Optimal exercise:** Holder maximizes **expected** discounted payoff; **no** transaction costs or frictions in the valuation model.
- **LSM:** Continuation value is **approximated** by regression on state variables (e.g. spot, remaining volume); **basis functions** (e.g. polynomials) and **finite** paths imply **approximation error**.

**Formulas (no single closed form):**

- **LSM:** At each exercise date $t$, regress $e^{-r\Delta t} V_{t+\Delta t}$ on $(S_t, R_t)$ (spot and remaining volume); set $V_t = \max(\mathrm{exercise}_t, \widehat{\mathrm{continuation}}_t)$; roll back. Value = average of $V_0$ over paths.
- **Tree:** Backward induction: $V_t(s, r) = \max\bigl( (S_t - K)\cdot q_t + e^{-r\Delta t} E[V_{t+1} \mid S_t, R_t], \; e^{-r\Delta t} E[V_{t+1} \mid S_t, R_t] \bigr)$ with $q_t$ in [min_daily, max_daily] and $R_t$ updated by $q_t$; constraints enforced at each node.

**Pros:** **Flexible** (any process, constraints); **LSM** scales to **many** dates and paths; **tree** is exact for **low-dimensional** state.  
**Cons:** **No** closed form; **slow** (MC or tree); **sensitive** to process and **regression** design (LSM); **Greeks** via bumping.

**Summary: assumptions, formulas, pros and cons**

| Model / product | Main assumptions | Formula type | Pros | Cons |
|-----------------|------------------|--------------|------|------|
| **Black(-76)** vanilla | Lognormal forward at $T$; constant $\sigma$; deterministic rates | $C = D(T)[F\Phi(d_1)-K\Phi(d_2)]$; $d_1,d_2$ in $\ln(F/K)$, $\sigma\sqrt{T}$ | Closed-form; fast; standard Greeks | No smile; thin tails; no path-dependence |
| **Asian** (Levy/TW) | $\bar{S}$ approx lognormal (moment match); discrete fixings | $C \approx D(T)[e^{m+v^2/2}\Phi(d_1)-K\Phi(d_2)]$; $m,v$ from moments | Fast; good for avg-price caps | Approximation only; Greeks less standard |
| **Asian** (MC) | Any process for $S_t$; fixings as in contract | $C \approx D(T)\,\frac{1}{N}\sum \max(\bar{S}_j - K, 0)$ | Flexible; same process as book | Slow; Greeks by bumping |
| **Spread** (Kirk/Margrabe) | $S_1$, $S_2$ lognormal; correlation $\rho$; cash settle | Modified Black on composite $F_c$, $\sigma_c$; or Margrabe for $K=0$ | Fast; no MC; Greeks by bump | Approximation; $\rho$, vol critical; can be unstable |
| **Spread** (MC) | Joint process for $S_1$, $S_2$ (e.g. correlated lognormal) | $C \approx D(T)\,\frac{1}{N}\sum \max(S_1 - H S_2 - K, 0)$ | Any joint dist; path-dependent | Slow; Greeks by bumping |
| **Swing** (LSM/tree) | Process for spot; daily exercise; volume constraints | Backward induction; LSM regress continuation on $(S, R)$ | Flexible; handles constraints | No closed form; slow; regression/process sensitive |

### 2.6 Model risk

- **Vol:** Wrong **level** or **smile** distorts value and **vega**. Use **consistent** vol surface (marked by risk or middle office) and **stress** vol up/down.
- **Forward:** Wrong **curve** distorts **delta** and **mark**. Option desk should use **same** curve as the rest of the book for MtM.
- **Process:** **Mean reversion** and **jumps** affect **long-dated** and **exotic** value. Document assumption (e.g. Black vs mean-reverting + MC) and **sensitivity**.

---

## 3. Mark-to-market (MtM)

### 3.1 What we mark

- **Position:** Every option (and strip of options) has a **mark** = **fair value** using **agreed** inputs: **forward curve**, **vol surface**, **rates**, and **model**.
- **Consistency:** Option **mark** must use the **same** curve and (where applicable) **same** vol surface as the rest of the trading book so that **hedges** (forwards, other options) and **option** P&amp;L are **consistent**.

### 3.2 Day-over-day P&amp;L and attribution

- **Total P&amp;L:** Mark today − Mark yesterday (plus any **cashflows** — premium, settlement).
- **Attribution:** Decompose P&amp;L into:
  - **Delta (curve):** Move in **forward** curve × option **delta** (sensitivity to underlying). Approximate: $\Delta \text{Mark} \approx \Delta \times (F_{\mathrm{new}} - F_{\mathrm{old}})$ for small move.
  - **Vega:** Move in **vol** × option **vega** (sensitivity to vol). Approximate: $\Delta \text{Mark} \approx \mathrm{Vega} \times (\sigma_{\mathrm{new}} - \sigma_{\mathrm{old}})$.
  - **Theta:** Time decay (option value loss as we move toward expiry).
  - **Gamma (curve):** Convexity in underlying; second-order effect when **curve** moves a lot.
  - **Residual:** Unexplained (model, cross-greeks, discrete cashflows). Should be **small** if model and inputs are stable; large residual suggests **missing** risk or **wrong** model/inputs.

### 3.3 Who marks

- **Independent** marking (e.g. **risk** or **middle office**) using **same** or **approved** model and **approved** inputs (curve, vol). **Trader** may run **internal** mark for P&amp;L explain; **official** book mark is independent.
- **Vol surface:** Often **maintained** by risk or quant; **updated** from broker runs, liquid options, or historical. Option trader **expects** a **transparent** and **consistent** surface so that **vega** risk and **mark** are interpretable.

---

## 4. Risk management: Greeks and limits

### 4.1 Greeks we care about

- **Delta:** Sensitivity of option value to **underlying** (forward price). $\Delta = \frac{\partial V}{\partial F}$. For a **strip** (cap/floor), **delta** = sum of deltas of each caplet/floorlet. **Hedging:** Delta-hedge with **forwards** or **futures** so that **combined** book delta is within limit.
- **Gamma:** Sensitivity of **delta** to underlying. $\Gamma = \frac{\partial^2 V}{\partial F^2}$. **High gamma** → delta moves a lot when price moves; rehedge more often; also **beneficial** when we are long optionality (long gamma = profit from large moves).
- **Vega:** Sensitivity to **volatility**. $\mathrm{Vega} = \frac{\partial V}{\partial \sigma}$. Option books are often **long vega** (long options). **Hedging:** Sell other options or **vol** products to reduce vega; or **limit** vega exposure.
- **Theta:** Time decay. $\Theta = \frac{\partial V}{\partial t}$. Long option → negative theta (value decays). Relevant for **carry** and **P&amp;L** explain.
- **Rho (rates):** Sensitivity to **interest rate**. Usually **small** for short-dated energy options; relevant for **long-dated** or when **funding** is material.
- **Vanna:** Cross-sensitivity: **delta to vol** (or vega to underlying). $\mathrm{Vanna} = \frac{\partial^2 V}{\partial F \partial \sigma}$. Matters when **both** curve and vol move; P&amp;L explain can have a vanna term when curve and vol move together.
- **Volga (vomma):** Sensitivity of **vega to vol** (vol convexity). $\mathrm{Volga} = \frac{\partial^2 V}{\partial \sigma^2}$. Long options have **positive** volga (vega increases when vol rises); short options have **negative** volga. Relevant for **large** vol moves and **vol surface** hedging.

**Sign of Greeks by position (call/put, buyer/seller):**

| Position      | Delta | Gamma | Vega | Theta | Rho  | Vanna | Volga |
|---------------|-------|-------|------|-------|------|-------|-------|
| **Long call** (buyer)  | +     | +     | +    | −     | +    | +     | +     |
| **Short call** (seller)| −     | −     | −    | +     | −    | −     | −     |
| **Long put** (buyer)   | −     | +     | +    | −     | −    | −     | +     |
| **Short put** (seller) | +     | −     | −    | +     | +    | +     | −     |

- **Delta:** Long call and short put are **long** underlying (delta > 0); short call and long put are **short** underlying (delta < 0).
- **Gamma:** **Long** optionality (long call, long put) has **positive** gamma; **short** optionality (short call, short put) has **negative** gamma.
- **Vega:** Long options (long call, long put) **gain** when vol rises (vega > 0); short options **lose** when vol rises (vega < 0).
- **Theta:** Long options **lose** value over time (theta < 0); short options **gain** (theta > 0), all else equal.
- **Rho:** Long call and short put have **positive** rho (value up when rates up); long put and short call have **negative** rho. Magnitude is small for short-dated energy options.
- **Vanna:** Long call and short put have **positive** vanna (delta increases when vol rises; vega increases when underlying rises for call). Long put and short call have **negative** vanna. Second-order for P&amp;L when curve and vol move together.
- **Volga:** Long options (long call, long put) have **positive** volga (vega increases when vol increases — convex in vol); short options have **negative** volga. Matters for large vol moves and vega hedging.

### 4.1.1 Taylor expansion and P&amp;L approximation

The **change in option value** (or **P&amp;L**) over a short period can be approximated by a **Taylor expansion** in the risk factors: underlying $F$, volatility $\sigma$, and time $t$.

**Second-order expansion in $F$ and $\sigma$ (and first order in $t$):**

$$
\Delta V \approx \frac{\partial V}{\partial F}\,\Delta F + \frac{\partial V}{\partial \sigma}\,\Delta\sigma + \frac{\partial V}{\partial t}\,\Delta t
+ \frac{1}{2}\,\frac{\partial^2 V}{\partial F^2}\,(\Delta F)^2 + \frac{1}{2}\,\frac{\partial^2 V}{\partial \sigma^2}\,(\Delta\sigma)^2 + \frac{\partial^2 V}{\partial F\,\partial \sigma}\,\Delta F\,\Delta\sigma + \cdots
$$

In **Greeks notation:**

$$
\boxed{
\Delta V \approx \Delta\,\Delta F + \mathrm{Vega}\,\Delta\sigma + \Theta\,\Delta t
+ \frac{1}{2}\,\Gamma\,(\Delta F)^2 + \frac{1}{2}\,\mathrm{Volga}\,(\Delta\sigma)^2 + \mathrm{Vanna}\,\Delta F\,\Delta\sigma
}
$$

- **First-order (linear):** $\Delta \cdot \Delta F$ (delta P&amp;L), $\mathrm{Vega} \cdot \Delta\sigma$ (vega P&amp;L), $\Theta \cdot \Delta t$ (theta). This is the **standard** P&amp;L explain: curve move, vol move, time decay.
- **Second-order:** $\frac{1}{2}\Gamma\,(\Delta F)^2$ (gamma effect: convexity in underlying), $\frac{1}{2}\mathrm{Volga}\,(\Delta\sigma)^2$ (vol convexity), $\mathrm{Vanna}\,\Delta F\,\Delta\sigma$ (cross term: when **both** curve and vol move, vanna contributes). For **large** moves in $F$ or $\sigma$, the second-order terms matter; ignoring them leaves **residual** in the P&amp;L explain.

**Use:** (1) **P&amp;L attribution:** Decompose daily P&amp;L into delta, vega, theta, gamma, volga, vanna; residual = actual − Taylor estimate. (2) **Risk:** Approximate **distribution** of $\Delta V$ when $(\Delta F, \Delta\sigma)$ are random (e.g. for VaR). (3) **Hedging:** Delta-hedge removes the $\Delta\,\Delta F$ term; delta–gamma–vega hedging aims to remove first-order and part of second-order sensitivity.

**Caveat:** Taylor is a **local** approximation. For **large** moves (e.g. spikes), **full revaluation** is more accurate; Taylor **understates** risk when we are **short** gamma or **short** volga.

---

### 4.1.2 Delta–gamma–vega hedging: approach and issues

**Objective:** Reduce **sensitivity** of the option portfolio to **underlying** (curve) and **volatility** by taking **offsetting** positions in **forwards** (or futures) and, when possible, **other options** (or vol products).

**Delta hedging:**

- **Idea:** Hold **forwards** so that **net delta** = portfolio delta + forward delta = 0 (or within limit). Then **first-order** P&amp;L from curve move is removed: $\Delta V \approx \Theta\,\Delta t + \mathrm{Vega}\,\Delta\sigma + \frac{1}{2}\Gamma\,(\Delta F)^2 + \cdots$.
- **Hedge ratio:** Forward position = $-\Delta_{\mathrm{portfolio}}$ (in same units as delta, e.g. MW or MWh).
- **Rehedge:** When **delta** changes (because $F$ or $\sigma$ or $t$ changed), **rebalance** the forward position. **Discrete** rehedging (e.g. daily or when delta moves by a threshold) means we do **not** remove curve risk entirely — we are left with **gamma** (and path) risk between rehedges.

**Delta–gamma hedging:**

- **Idea:** Make **net delta** and **net gamma** zero. Delta is offset by **forwards**; gamma is offset by **other options** (e.g. vanilla options on the same underlying), because **forwards** have zero gamma. So we solve: portfolio $\Delta + n_F \cdot 1 + n_C\,\Delta_C + n_P\,\Delta_P = 0$ and portfolio $\Gamma + n_C\,\Gamma_C + n_P\,\Gamma_P = 0$ for **notions** $n_F$, $n_C$, $n_P$ (forwards, calls, puts). In practice we use **liquid** options (e.g. ATM) to add **gamma** of the opposite sign.
- **Effect:** **Second-order** P&amp;L from $(\Delta F)^2$ is reduced. **Vega** and **theta** (and vanna, volga) remain unless we also hedge those.

**Delta–gamma–vega hedging:**

- **Idea:** Set **net delta**, **net gamma**, and **net vega** to zero (or within limits). We need **three** “instruments”: (1) **forwards** (delta only), (2) **options** (delta, gamma, vega). With **two** option strikes (e.g. ATM and one wing) we can typically solve for **delta = 0**, **gamma = 0**, **vega = 0** by choosing **forward** position and **two** option notionals. More strikes → more flexibility (e.g. bucket vega by expiry).
- **Effect:** First-order **curve** and **vol** risk reduced; **theta** (and **vanna**, **volga**) may still move the book. **Vanna** and **volga** are **second-order** — they matter when **both** $F$ and $\sigma$ move or when **vol** moves a lot; hedging them requires **more** option positions or **accepting** residual.

**Issues we face:**

| Issue | Description |
|-------|-------------|
| **Discrete rehedging** | We rehedge at **intervals** (e.g. daily), not continuously. Between rehedges, **delta** drifts (gamma effect) and **curve** can move. So we are exposed to **path** and **timing**; **short gamma** books can **lose** on large moves between rehedges. |
| **Transaction costs** | Every **trade** (forward or option) costs **bid–ask** and possibly **commission**. **Frequent** rehedging **increases** cost; **infrequent** rehedging **increases** risk. Trade-off: **rehedge frequency** vs **cost**. |
| **Vol is not a traded asset** | We **cannot** buy or sell “volatility” directly. We hedge **vega** by trading **options** (or variance swaps where they exist). So vega hedging **changes** our **delta** and **gamma**; we must **solve** for a **combination** of forwards + options that hits delta, gamma, vega targets. |
| **Vol surface moves** | **Vega** is usually quoted per **point** (e.g. 1% absolute vol). In reality the **whole surface** can **shift** and **tilt** (e.g. short-dated vol up, long-dated flat). **Single** vega number **misses** term structure; we need **vega buckets** (e.g. by expiry) and possibly **volga** and **vanna** when moves are large. |
| **Liquidity** | **Options** on some underlyings (e.g. off-peak power, long-dated gas) are **illiquid**. We may **not** be able to **trade** the size we need to gamma/vega hedge, or only at **wide** bid–ask. Then we **limit** option size and **accept** residual risk or hedge with **proxy** (e.g. ATM only). |
| **Basis and mapping** | Our **option** may be on **hub A, block B, month T**; the **hedge** is in **futures** or options on **slightly** different product (e.g. different delivery period or hub). **Basis** (A vs B) can move; **mapping** (which hedge instrument) is approximate. So **delta** hedge is **imperfect**. |
| **Cross-greeks (vanna, volga)** | After delta–gamma–vega hedging we still have **vanna** ($\Delta F \cdot \Delta\sigma$) and **volga** ($(\Delta\sigma)^2$). When **curve and vol move together** (e.g. spike = price up and vol up), **vanna** P&amp;L can be large. When **vol** moves a lot, **volga** matters. Hedging them **fully** would require **more** options and **more** calibration; often we **monitor** and **limit** vanna/volga or **stress** the book. |
| **Model and input risk** | **Greeks** depend on **model** (Black vs MC) and **inputs** (curve, vol). If **mark** or **Greeks** are wrong, the **hedge** is wrong. **Independent** marking and **transparent** vol/curve reduce this; **residual** in P&amp;L can signal **model** or **input** error. |
| **Funding and collateral** | **Options** may be **uncollateralized** or **partially** collateralized; **hedges** (forwards, listed options) may be **collateralized**. **Funding** cost and **basis** between **option** and **hedge** affect **carry** and **P&amp;L**; not captured by **delta–gamma–vega** alone. |

**Summary:** **Delta** hedging removes **first-order** curve risk; **delta–gamma** adds **options** to remove **gamma**; **delta–gamma–vega** targets **curve** and **vol** first-order. **Taylor expansion** gives the **formula** for P&amp;L (and residual). **Issues:** discrete rehedging, transaction costs, vol not tradeable, surface moves, liquidity, basis, vanna/volga, model/input risk, funding. Risk manager and trader must **agree** on **rehedge** policy, **limits** on unhedged Greeks (e.g. vanna, volga), and **stress** tests.

### 4.2 Scenario and stress

- **Curve shift:** Revalue book under **parallel** or **structured** move in forward curve (e.g. +$5, −$5 per MWh). Compare **full reval** to **delta-based** estimate to see **gamma** effect.
- **Vol shift:** Revalue under **vol up/down** (e.g. +5%, −5% absolute). Captures **vega** and, for large moves, **vol convexity**.
- **Stress:** **Extreme** move (e.g. 2008-style spike, or **outage** scenario). Option book may have **large** positive P&amp;L (long options) or **large** negative (short options); must be **within** stress limit and **understood** by risk.

### 4.3 Limits

- **Delta:** Limit on **net** delta (option delta + forward position) by **hub**, **tenor**, or **book**. Prevents **directional** bet beyond appetite.
- **Vega:** Limit on **net** vega (long − short) by **expiry** or **bucket**. Prevents **vol** bet or **mark** sensitivity to vol beyond appetite.
- **Gamma:** Limit on **net** gamma (or **max** loss from a given curve move). Protects against **delta** blowing out when price moves.
- **Position / notional:** Limit on **notional** (e.g. MW×months, or MMBtu) by product type or counterparty. Caps **size** of optionality sold or bought.
- **Stress loss:** Limit on **loss** in a **defined** stress scenario (e.g. curve −$10, vol +10%). Ensures **capital** and **liquidity** can absorb stress.

---

## 5. What the option trader expects from the risk manager

### 5.1 Independent and consistent marking

- **Mark** the option book using **agreed** model and **same** inputs (curve, vol, rates) as used for **hedges** and **rest of book**. **No** “trader mark” vs “risk mark” gap that cannot be **explained** (e.g. different vol or curve).
- **Document** model and assumptions (e.g. Black vs Asian formula, Monte Carlo specs). So that **disputes** (e.g. broker run vs internal) can be **resolved** objectively.

### 5.2 Transparent vol surface and curve

- **Vol surface** (and curve) should be **published** or **accessible** so the trader can **replicate** mark and **explain** P&amp;L. **Changes** to surface (e.g. vol bump) should be **visible** and **dated** so that **vega** P&amp;L and **residual** are interpretable.
- **Consistency:** Same **tenor** and **underlying** should use the **same** vol and curve across **trading**, **risk**, and **finance**.

### 5.3 Limit monitoring and escalation

- **Monitor** Greeks and **stress** against **limits** in **real time** (or daily). **Escalate** when we are **close** to or **breach** limit so that trader can **reduce** (hedge or unwind) before risk forces action.
- **Understand** product: risk should be able to **interpret** why **delta** or **vega** is large (e.g. short cap = short vega, long spark call = long power delta and short gas delta). So that **limits** are **sensible** and **exceptions** are discussed, not just blocked.

### 5.4 P&amp;L explain and residual

- **Daily** (or intraday) **P&amp;L explain**: decompose into **curve**, **vol**, **theta**, **residual**. **Large residual** should trigger **review** (wrong curve, vol, or model). Risk should **challenge** unexplained P&amp;L and **ensure** model and inputs are correct.
- **Backtesting:** Where possible, compare **realized** P&amp;L to **expected** (e.g. delta × curve move). Improves **model** and **hedging** over time.

### 5.5 Model risk and new products

- **New product** (e.g. new payoff, new underlying): risk should **review** **model** (formula or MC), **inputs** (vol, curve), and **Greeks** before we **trade** in size. So that **mark** and **risk** are **defined** from day one.
- **Model change** (e.g. switch from Black to MC for Asian): **parallel run** and **impact** on existing book (mark and Greeks) should be **assessed** and **agreed** with risk.

### 5.6 Summary: risk manager’s role from trader’s view

| Expectation                              | Why it matters                                           |
| ------------------------------------------| ----------------------------------------------------------|
| **Independent mark** with same curve/vol | No arbitrage between option and hedge; fair P&amp;L      |
| **Transparent vol (and curve)**          | Trader can explain P&amp;L and hedge vega                |
| **Limit monitoring + escalation**        | Trader can manage risk proactively; no surprise breach   |
| **Product understanding**                | Sensible limits; sensible exceptions; fewer false alarms |
| **P&amp;L explain + residual review**    | Catches input/model error; improves discipline           |
| **New product / model review**           | Clean mark and risk from start; no “fix later”           |

---

## 6. One-page recap

- **Products:** Vanilla (European on forward), **Asian** (average price), **spread** (spark, basis, calendar), **swing**, **cap/floor**. Each has a **payoff** and a **typical** valuation method (Black, Asian formula, Kirk/MC, LSM/tree).
- **Valuation:** **Forward curve** + **vol surface** + **rates**; **Black** for vanilla on forward; **closed-form or MC** for Asian; **Kirk or MC** for spread; **LSM or tree** for swing.
- **MtM:** **Mark** = fair value with **agreed** inputs; **P&amp;L** = mark change + cashflows; **attribution** = curve (delta) + vol (vega) + theta + residual.
- **Risk:** **Delta**, **gamma**, **vega**, **theta**; **limits** on delta, vega, gamma, stress; **scenario** reval for curve and vol moves.
- **Risk manager:** **Independent** mark, **transparent** vol/curve, **limit** monitoring and escalation, **product** understanding, **P&amp;L** explain and residual review, **new product** and **model** review. So that the option book is **marked** fairly, **risk** is **measured** and **controlled**, and the trader can **hedge** and **explain** P&amp;L with confidence.
