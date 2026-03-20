# Mark-to-Market (MtM) in Energy Commodities: FTR, Power, and Gas

A practical guide from the perspective of a seasoned quant in the energy commodity space: what MtM is, the steps and methodologies we use, and how they differ — with pros and cons — for **FTR**, **power**, and **gas** products.

---

## 1. What is Mark-to-Market?

**Mark-to-Market (MtM)** is the process of assigning a **current fair value** to a position or portfolio using **observable** (or model-consistent) **prices** and **methodologies** as of a given **valuation date**. That value is the amount we would expect to receive (or pay) if we **settled** or **transferred** the position at that date under market conditions.

**Why it matters:**

- **P&amp;L and reporting:** Trading and risk need a **daily** (or intraday) value for positions for **profit and loss**, **balance sheet**, and **regulatory** reporting.
- **Risk and limits:** MtM feeds **VaR**, **exposure**, and **limit** monitoring; we need a consistent, auditable value to measure risk.
- **Collateral and margin:** Many contracts are **collateralized**; margin calls are based on **MtM change** (e.g. variation margin).
- **Fair value and trading:** Traders use MtM to compare **carry** value vs **market** and to **explain** P&amp;L (delta, vega, time decay, curve move).

**Who uses it:** **Traders** (daily P&amp;L, position view), **risk** (limits, VaR, stress), **finance** (books and records, audit), **counterparties** and **clearing houses** (margin). Methodologies are often set by **product control** or **valuation** policy and must be **documented** and **consistent** across front office and risk.

---

## 2. Generic MtM process: steps and building blocks

The **same logical steps** apply across products; the **inputs** and **valuation engine** change by asset class.

### 2.1 High-level steps

| Step | What | Typical owner |
|------|------|----------------|
| **1. Data** | Gather **positions** (contracts, volumes, terms), **market data** (quotes, curves, vols), and **reference data** (settlement rules, calendars). | Data / Ops / Quant |
| **2. Curves** | Build or refresh **forward curves** (and, where needed, **vol surfaces**, **correlation**) for each underlying and delivery period. | Quant / Curve team |
| **3. Valuation** | For each position, compute **fair value** using the chosen **model** (e.g. forward payoff, Black-76, Monte Carlo) and **current** curves and inputs. | Quant / Valuations |
| **4. Aggregation** | Sum position-level values to **book**, **desk**, **counterparty**, or **portfolio** level; apply **funding** or **reserves** if policy requires. | Finance / Risk |
| **5. Reporting** | Produce **MtM report** (by product, book, currency), **P&amp;L explain** (vs prior day: curve, vol, time, new trades), and feed **risk** (VaR, limits). | Product control / Risk |
| **6. Controls** | **Reconcile** to **exchange** or **broker** marks where available; **independent price verification (IPV)**; **model validation**; **limit** checks. | Middle office / Risk |

### 2.2 Methodologies: what we mean

- **Observable inputs:** Use **quoted** prices (e.g. listed futures, broker curves) where **liquid** and **reliable**. For illiquid tenors or underlyings, we **interpolate** or **extrapolate** under a documented **curve-building** method (see term-structure doc).
- **Model choice:** Each product type has a **standard** model (e.g. **forward** = curve price × volume; **vanilla option** = Black-76; **Asian** = closed form or MC; **spread option** = Kirk/Margrabe or MC). The model must be **calibrated** to liquid options where they exist (e.g. implied vol surface).
- **Consistency:** Same **curve** and **vol** (and rates) used for **trading**, **risk**, and **finance** so that P&amp;L and limits are aligned. **Stale** or **inconsistent** inputs cause breaks and disputes.
- **Documentation:** **Valuation policy** describes product → model, data sources, fallbacks, and **review** frequency (e.g. IPV monthly, model validation annually).

### 2.3 Generic valuation formulas (reference)

- **Single cash flow at $T$:** Present value = $D(T) \times \mathbb{E}[\text{payoff at } T \mid \mathcal{F}_0]$, where $D(T)$ is the discount factor to time $T$ and $\mathcal{F}_0$ is today’s information.
- **Portfolio MtM:** Sum over positions: $\mathrm{MtM}_{\mathrm{portfolio}} = \sum_i V_i$, where $V_i$ is the fair value of position $i$ (same valuation date and curves).
- **P&amp;L explain (one period):** $\Delta \mathrm{MtM} \approx \Delta V \approx \sum \frac{\partial V}{\partial x_k} \Delta x_k + \frac{1}{2}\sum \frac{\partial^2 V}{\partial x_k^2}(\Delta x_k)^2 + \cdots$ (Taylor in risk factors: curve, vol, time). In practice we report **delta** (curve), **vega** (vol), **theta** (time), **new trades**.

### 2.4 Pros and cons of a disciplined MtM process

**Pros:**

- **Transparent** P&amp;L: we can **explain** moves (curve, vol, time, new trades).
- **Consistent** risk: VaR and limits use the **same** value as trading.
- **Auditable**: methodology is written down; inputs and models can be **checked** by risk and audit.
- **Margin and collateral** are computed on a **standard** basis, reducing disputes.

**Cons:**

- **Cost:** Building and maintaining **curves**, **models**, and **data** is resource-intensive.
- **Illiquidity:** For **illiquid** products (e.g. long-dated power options, odd lots), we rely on **models** and **assumptions**; marks can differ from “true” exit value.
- **Procyclicality:** When markets **gap** or **dry up**, marks can **move sharply** and trigger **margin** or **limits** even if we don’t intend to exit — so **stress** and **liquidity** views are needed alongside MtM.

---

## 3. MtM for FTR (Financial Transmission Rights)

FTRs (or CRRs) are **path-based** contracts: payoff = **path spread** (sink price − source price) over the CRR period, typically **per MW** and **per interval** (e.g. 15-min), then summed. There is **no** liquid **secondary market** in most ISOs, so MtM is **model-based** using **forward** congestion (path spread) and **remaining** life.

### 3.1 What we are marking

- **Position:** Path (source–sink), **volume** (MW), **type** (obligation vs option), **CRR period** (e.g. calendar month).
- **Value:** Expected **payoff** over the **remaining** settlement intervals, using **current** view of path spread (or constraint shadow prices).

### 3.2 Steps (FTR-specific)

| Step | What | Detail |
|------|------|--------|
| **Data** | Position list (path, MW, type, period); **forward** path spread (or hub/zone prices, or constraint shadows); **remaining** intervals (calendar). | Path spread may come from **curve** (if quoted), **PCM** output, or **historical** shape applied to forward power curve. |
| **Curve** | **Path-spread curve** (or **congestion** view): expected path spread **per interval** (or per day/month) over the **remaining** life. Often built from: (1) **forward** hub/zone prices and **spread** assumption, (2) **PCM** run with current topology, (3) **historical** average spread × current forward level. | No liquid “path spread futures”; curve is **model** or **fundamental** driven. |
| **Valuation** | $\mathrm{MtM} = Q \times \sum_{\text{remaining intervals}} \mathbb{E}[\pi_{\text{path}}(t) \mid \mathcal{F}_{\text{today}}]$ where $\pi_{\text{path}}(t)$ = payoff per MW in interval $t$ (obligation or option). Sum over remaining intervals; optional **discounting** (often omitted for simplicity). | For **obligation**: $\pi = \text{path spread}$; for **option**: $\pi = \max(\text{path spread}, 0)$. |
| **Risk mapping** | For **VaR** and **sensitivities**: map position to **risk factors** — e.g. **path spread** per path, or **constraint shadow prices** × PTDF. $\Delta V \approx Q \sum_{\ell} \mathrm{PTDF}_{\ell,\text{path}} \cdot \Delta\mu_\ell \cdot (\text{remaining hours})$. | Enables **portfolio** VaR and **decomposition** by path or constraint. |

### 3.3 Methodologies (FTR)

- **Path-spread source:** (1) **Direct** path-spread curve if desk or vendor provides one; (2) **Hub spread**: forward price at sink − forward at source (from power curve), possibly with **congestion** adjustment; (3) **Constraint-based**: forward **shadow prices** (from PCM or historical) × **PTDF** for the path, summed over constraints.
- **Remaining tenor:** Only **future** intervals count; **past** intervals are either **settled** (known payoff) or **locked** (e.g. day-ahead already published). MtM uses **remaining** intervals × expected spread.
- **Optionality (option FTR):** $\pi = \max(\text{spread}, 0)$; we need **distribution** of spread (or binding frequency and conditional spread) to get $\mathbb{E}[\max(\text{spread}, 0)]$. Often approximated by **historical** or **PCM** average payoff when binding, × probability of binding.

### 3.5 Formulas (FTR reference)

**Path spread (one interval):**
$$
\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}} = \sum_{\ell \in \mathcal{C}} \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}},
$$
where $\lambda$ = reference price (LMP/SPP) at sink/source, $\mathcal{C}$ = set of constraints, $\mu_\ell$ = shadow price of constraint $\ell$ ($\$/MWh$), $\mathrm{PTDF}_{\ell,\mathrm{path}}$ = PTDF of path on $\ell$.

**Payoff per MW, one interval:** Obligation: $\pi_{\mathrm{obl}} = \lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}}$. Option: $\pi_{\mathrm{opt}} = \max(\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}},\ 0)$.

**MtM (undiscounted):**
$$
\mathrm{MtM}_{\mathrm{FTR}} = Q \cdot \sum_{t \in \text{remaining}} \mathbb{E}\bigl[ \pi_{\mathrm{path}}(t) \mid \mathcal{F}_{\mathrm{today}} \bigr],
$$
with $Q$ = volume (MW). With discounting:
$$
\mathrm{MtM}_{\mathrm{FTR}} = Q \cdot \sum_{t \in \text{remaining}} D(t) \cdot \mathbb{E}\bigl[ \pi_{\mathrm{path}}(t) \mid \mathcal{F}_{\mathrm{today}} \bigr].
$$

**Change in value (for VaR / risk mapping):**
$$
\Delta V \approx Q \cdot \sum_{\ell} \mathrm{PTDF}_{\ell,\mathrm{path}} \cdot \Delta\mu_\ell \cdot (\text{remaining MW$\cdot$h}),
$$
or, with path spread as risk factor: $\Delta V \approx Q \cdot (\text{remaining MW$\cdot$h}) \cdot \Delta(\text{path spread})$.

**Option FTR (approximation):** If spread $S$ when binding is approximately normal with mean $\bar{s}$ and variance $\sigma_s^2$, then $\mathbb{E}[\max(S, 0)] \approx \bar{s}\, \Phi(\bar{s}/\sigma_s) + \sigma_s\, \phi(\bar{s}/\sigma_s)$ (with $\Phi$, $\phi$ standard normal cdf/pdf). In practice we often use **binding probability** $p_b$ and **conditional** expected payoff $\bar{\pi}_b$: $\mathbb{E}[\pi_{\mathrm{opt}}] \approx p_b \cdot \bar{\pi}_b$.

### 3.6 Pros and cons (FTR MtM)

| Pros | Cons |
|------|------|
| **Conceptually clear:** value = expected payoff over remaining life. | **No liquid market:** path spread is **not** traded; we rely on **model** (PCM, historical, curve). |
| **PTDF mapping** gives **portfolio** view and **VaR** by constraint/path. | **Sensitive** to **topology** and **outages**: one outage can **shift** shadows and path value a lot. |
| **Aligns** with **settlement** (same payoff definition). | **Zero-inflation:** when constraints don’t bind, spread = 0; **distribution** is mixed (discrete + continuous); mean can be **unstable**. |
| **Daily** refresh with **updated** curves and **remaining** tenor is straightforward. | **IPV** is hard: no exchange mark; we compare to **broker** or **internal** view only. |

---

## 4. MtM for Power products

Power positions include **forwards** (physical or financial), **options** (vanilla, Asian, caps/floors, spread options), and **structured** deals (e.g. shaped blocks, tolling). MtM uses **forward curves** (and **vol surfaces** where options exist) and **standard** models per product.

### 4.1 What we are marking

- **Forwards:** Monthly or block (e.g. 5x16, 7x16) **price** × **volume** (MW × hours). Value = forward price from **curve** × volume.
- **Options:** Vanilla, Asian, cap/floor, spread. Value = **model** (Black-76, Asian formula, Kirk, etc.) with **forward** and **vol** from **curve** and **vol surface**.
- **Shaped / HPFC:** If the contract is on **hourly** or **shaped** delivery, we use an **HPFC** (hourly price forward curve) to get **hourly** forward prices, then value = sum over hours of (forward price × volume).

### 4.2 Steps (Power-specific)

| Step | What | Detail |
|------|------|--------|
| **Data** | Positions (underlying hub/block, delivery, volume, strike for options); **power forward curve** (by delivery month/block); **vol surface** $\sigma(K,T)$ for options; **rates** for discounting. | Curve from **broker**, **exchange**, or **internal** curve build. |
| **Curve** | **Power forward curve** (e.g. ERCOT North 5x16 by month); **vol surface** (strike and term) for options; **HPFC** if contract is hourly or shaped. | See Term-Structure and Shaping docs. |
| **Valuation** | **Forward:** $V = F_{0,T} \times Q \times \text{hours}$. **Vanilla option:** Black-76 with $F_{0,T}$, $K$, $T$, $\sigma(K,T)$. **Asian:** Closed form or MC on average price. **Cap/floor:** Sum of caplets/floorlets. **Shaped:** Sum over hours of HPFC price × volume. | Same formulas as in Option doc; discount factor $D(T)$ if policy uses it. |
| **Reporting** | MtM by **book**, **hub**, **delivery**; **P&amp;L explain**: delta (curve), vega (vol), theta (time), new trades. | |

### 4.3 Methodologies (Power)

- **Curve:** Build from **liquid** forward quotes (prompt, balance-of-month, calendar months, quarters); **interpolate** (e.g. cubic spline, seasonal) for non-quoted tenors; **no-arbitrage** where possible (e.g. block = weighted sum of peak/off-peak).
- **Vol:** Where **options** trade (OTC, some listed), use **implied** vol surface; otherwise **historical** or **relative** (e.g. same smile as liquid hub). **Sticky strike** or **sticky delta** for revaluation (see Volatility doc).
- **Shaping:** For **hourly** or **block** products, use **HPFC** (hourly price forward curve) from **peak/off-peak** decomposition or **historical** weights; value = sum over hours (or blocks) of forward × volume.

### 4.5 Formulas (Power reference)

**Forward (physical or financial, block/month):**
$$
V_{\mathrm{fwd}} = F_{0,T} \times Q \times H, \qquad \text{(e.g. } Q \text{ in MW, } H \text{ = hours in delivery period)}
$$
With discounting: $V_{\mathrm{fwd}} = D(T) \times F_{0,T} \times Q \times H$.

**Vanilla option (Black-76):** Call value
$$
C = D(T)\bigl[ F_{0,T} \Phi(d_1) - K \Phi(d_2) \bigr], \quad d_1 = \frac{\ln(F_{0,T}/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}.
$$
Put: $P = D(T)\bigl[ K \Phi(-d_2) - F_{0,T} \Phi(-d_1) \bigr]$. Use $\sigma = \sigma(K, T)$ from vol surface.

**Cap (strip of caplets):** $\mathrm{Cap} = \sum_{\mathrm{months}} \mathrm{Caplet}(F_{0,T_i}, K, T_i, \sigma_i)$; each caplet is a call (or Asian call if settlement on average price). **Floor** = strip of put/floorlets.

**Shaped / HPFC:** If $F_{0,h}$ is the forward price for hour $h$ (from HPFC) and $Q_h$ is volume in that hour:
$$
V_{\mathrm{shaped}} = \sum_{h \in \mathrm{period}} F_{0,h} \times Q_h \quad \text{or} \quad V_{\mathrm{shaped}} = D(T) \sum_h F_{0,h} \times Q_h.
$$

**Asian option (average price):** Use closed-form (e.g. Levy/Turnbull–Wakeman) or Monte Carlo on $\bar{S} = \frac{1}{n}\sum_i S_{t_i}$; see Option doc.

**Spread option (e.g. spark, basis):** Kirk or Margrabe approximation with $F_1$, $F_2$, $\sigma_1$, $\sigma_2$, $\rho$; see Option doc.

### 4.6 Pros and cons (Power MtM)

| Pros | Cons |
|------|------|
| **Liquid** forwards (and some options) in major hubs → **observable** curve and vol. | **Many** underlyings (hub × block × month) → **curve** and **vol** maintenance is **heavy**. |
| **Standard** models (Black-76, Asian, Kirk) are **well understood** and **auditable**. | **Illiquid** strikes/expiries and **shaped** products → **model** and **HPFC** assumptions matter a lot. |
| **IPV** possible for **liquid** hubs (broker, exchange). | **Spikes** and **non-normality** → **Black** is a convention; **tail** risk may be understated. |

---

## 5. MtM for Gas products

Gas positions include **forwards** (physical or financial, by hub and delivery), **options** (vanilla, caps/floors, basis options), **storage**, and **spread** (e.g. spark, basis) deals. MtM uses **gas forward curves** (and **vol** for options) and **standard** models.

### 5.1 What we are marking

- **Forwards:** Hub × delivery (e.g. Henry Hub monthly) **price** × **volume** (MMBtu). Value = forward from **curve** × volume.
- **Options:** Vanilla, cap/floor, **basis** or **spread** options. Value = **model** (Black-76, Kirk, etc.) with **forward(s)** and **vol** (and **correlation** for spread).
- **Storage:** Optionality to **inject/withdraw** over time; value = **optionality** (e.g. spread between winter and summer) plus **physical** constraints. Often **tree** or **MC**.
- **Basis:** Spread between two hubs (e.g. Henry Hub vs regional). Value = **forward spread** × volume, or **option on spread** (Kirk/Margrabe or MC).

### 5.2 Steps (Gas-specific)

| Step | What | Detail |
|------|------|--------|
| **Data** | Positions (hub, delivery, volume, strike for options); **gas forward curve** (by hub and delivery); **vol surface** (and **correlation** for spread options); **rates**. | Henry Hub and major hubs have **liquid** curves; **basis** curves (hub − Henry) for location. |
| **Curve** | **Gas forward curve** (e.g. Henry monthly, seasonal strips); **basis** curves; **vol surface** $\sigma(K,T)$ per hub; **correlation** (hub vs hub, or gas vs power for spark). | |
| **Valuation** | **Forward:** $V = F_{0,T} \times Q$. **Vanilla option:** Black-76. **Spread option:** Kirk or MC with two forwards and correlation. **Storage:** Optionality model (tree/MC). | |
| **Reporting** | MtM by **book**, **hub**, **product**; P&amp;L explain (curve, vol, time). | |

### 5.3 Methodologies (Gas)

- **Curve:** Build from **NYMEX/ICE** and **broker** quotes; **seasonal** structure (winter premium); **basis** = regional hub − Henry (or similar).
- **Vol:** **Implied** from **liquid** options (Henry, some regionals); **relative** or **historical** for illiquid hubs. **Correlation** for spread options from **historical** or **quoted**.
- **Storage:** Model **inject/withdraw** optionality and **constraints** (inventory, rates); value = expected profit from spread capture; **tree** or **LSM** (Monte Carlo) common.

### 5.5 Formulas (Gas reference)

**Forward (physical or financial):**
$$
V_{\mathrm{fwd}} = F_{0,T} \times Q, \qquad \text{(e.g. } Q \text{ in MMBtu)} \qquad \text{or} \qquad V_{\mathrm{fwd}} = D(T) \times F_{0,T} \times Q.
$$

**Vanilla option (Black-76):** Same as power: $C = D(T)\bigl[ F_{0,T} \Phi(d_1) - K \Phi(d_2) \bigr]$, $d_1 = \frac{\ln(F_{0,T}/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$. Put: $P = D(T)\bigl[ K \Phi(-d_2) - F_{0,T} \Phi(-d_1) \bigr]$.

**Basis (spread between two hubs):** Forward value of basis position: $V_{\mathrm{basis}} = (F_{0,T}^{(A)} - F_{0,T}^{(B)}) \times Q$, where $A$, $B$ are the two hubs.

**Spread option (e.g. spark $S_1 - H S_2$, or basis option):** Kirk approximation: composite vol
$$
\sigma_c^2 = \sigma_1^2 + \left( \frac{H F_2}{F_1 - K} \right)^2 \sigma_2^2 - 2\rho\, \sigma_1\, \sigma_2\, \frac{H F_2}{F_1 - K};
$$
then call on $S_1 - H S_2 - K$ is approximated as Black on $(F_1 - H F_2 - K)$ with vol $\sigma_c$. Margrabe (exchange option, $K=0$): $\sigma^2 = \sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2$; $C = D(T)\bigl[ F_1 \Phi(d_1) - H F_2 \Phi(d_2) \bigr]$.

**Cap / floor:** Strip of caplets/floorlets (each valued as Black call/put on the relevant forward and vol).

**Storage:** No single closed form; value = $\mathbb{E}[\text{optimal inject/withdraw profit}]$ under constraints; typically **tree** or **LSM** (Monte Carlo) with spot/forward process and inventory limits.

### 5.6 Pros and cons (Gas MtM)

| Pros | Cons |
|------|------|
| **Liquid** **Henry Hub** (and some regionals) → **good** curve and **IPV**. | **Basis** and **regional** hubs can be **thin** → **curve** and **vol** more model-dependent. |
| **Standard** models (Black, Kirk, storage models) are **accepted**. | **Storage** and **spread** options are **complex**; model choice and **correlation** affect mark. |
| **Seasonal** structure is **well documented** (winter/summer). | **Extreme** events (freeze, demand spike) can **gap** curves and vol; **stress** needed. |

---

## 6. Comparison: FTR vs Power vs Gas MtM

| Dimension            | FTR                                                             | Power                                                | Gas                                                     |
| ----------------------| -----------------------------------------------------------------| ------------------------------------------------------| ---------------------------------------------------------|
| **Underlying**       | Path spread (sink − source)                                     | Forward price (hub × block × delivery)               | Forward price (hub × delivery)                          |
| **Curve**            | Path-spread or congestion view (model/PCM/historical)           | Power forward curve (+ HPFC if shaped); vol surface  | Gas forward curve; basis; vol surface                   |
| **Liquidity**        | **No** liquid secondary market                                  | **Liquid** forwards (and some options) in major hubs | **Liquid** Henry (and some hubs); basis less so         |
| **Core model**       | Expected payoff over remaining intervals (path spread × volume) | Forward × volume; Black/Asian/Kirk for options       | Forward × volume; Black/Kirk for options; storage model |
| **Key risk factors** | Path spread (or constraint shadows × PTDF)                      | Forward price, vol                                   | Forward price, vol, correlation (spread)                |
| **IPV**              | **Hard** (no exchange mark)                                     | **Possible** for liquid hubs                         | **Possible** for Henry / liquid hubs                    |
| **Sensitivity**      | Topology, outages, binding frequency                            | Curve, vol, shaping                                  | Curve, vol, basis, correlation                          |

---

## 7. Assumptions and caveats

- **Valuation date:** MtM is **as of** a given date; **settlement** may be later (e.g. monthly FTR payment). **Funding** and **collateral** (e.g. CVA, DVA) may be in scope for **fair value** under accounting rules; here we focus on **trading** MtM.
- **Observable vs model:** Where markets are **illiquid**, we use **model** and **assumptions**; the **mark** may not equal **exit** value. **IPV** and **reserves** (e.g. bid–ask, model uncertainty) are used to reflect that.
- **Consistency:** Same **curve**, **vol**, and **rates** across **trading**, **risk**, and **finance** to avoid **arbitrage** and **disputes**.
- **FTR:** Path spread is **not** traded; **topology** and **outages** can **change** path value **quickly**; **zero-inflation** (spread = 0 when not binding) makes **distribution** and **mean** sensitive to assumptions.

---

## 8. One-page recap

- **MtM** = current **fair value** of a position using **observable** (or model-consistent) prices and a **documented** methodology.
- **Generic steps:** Data → Curves → Valuation → Aggregation → Reporting → Controls (reconcile, IPV, limits).
- **FTR:** Value = expected **path spread** payoff over **remaining** intervals; **curve** from PCM, historical, or hub spread; **no** liquid market → **model-based**; **PTDF** mapping for VaR. **Pros:** clear definition, aligned with settlement. **Cons:** no IPV, sensitive to topology and zero-inflation.
- **Power:** Value = **forward** × volume (forwards); **Black/Asian/Kirk** for options using **power curve** and **vol surface**; **HPFC** for shaped. **Pros:** liquid curves and some options; standard models. **Cons:** many underlyings; illiquid strikes/shaping.
- **Gas:** Value = **forward** × volume (forwards); **Black/Kirk** for options; **storage** model for optionality. **Pros:** liquid Henry and standard models. **Cons:** basis and correlation; storage complexity.
- **Consistency** (same curves/models across trading and risk), **documentation** (valuation policy), and **controls** (IPV, reconciliation) are essential for **reliable** MtM and **P&amp;L** explain.
