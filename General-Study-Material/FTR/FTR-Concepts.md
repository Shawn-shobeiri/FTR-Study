# FTR Market in North America — Concepts

## 1. Motivation: Why FTRs Exist

**Locational marginal prices (LMPs)** differ by node. Load and generation therefore face **congestion risk**: the price spread between two points can move against them. **FTRs** (Financial Transmission Rights) and **CRRs** (Congestion Revenue Rights) are **financial contracts** that pay the **congestion spread** between a source and a sink, hedging that risk or allowing speculation. They are used by **load-serving entities**, **generators**, and **traders**.

---

## 2. LMP and Congestion — Foundation

**LMP** at a node is the marginal cost of serving one more MWh at that node.

**Decomposition** (single binding constraint):

$$
\text{LMP}_n = \lambda - \mu \cdot \text{SF}_n

$$

where $\lambda$ = system energy price, $\mu$ = constraint shadow price, $\text{SF}_n$ = shift factor at node $n$.

**Full form** (energy + congestion + losses):

$$
\text{LMP}_n = \lambda + \text{Congestion}_n + \text{Loss}_n.

$$

Some markets (e.g. ERCOT) do not embed losses in LMP; they are reflected elsewhere (e.g. adjusted load).

**Congestion:** When a transmission constraint binds, LMPs diverge across nodes. **Congestion rent** is the surplus from charging load more and paying generation less at constrained nodes; it funds FTR/CRR payouts.

**Contingency:** A **contingency** is the **loss or unavailability of one or more system elements** (e.g. a transmission line, transformer, or generator) that is explicitly modeled to check that the grid remains secure **after** that loss. **N-1** means the outage of a **single** major element; the system must still serve load and respect thermal and voltage limits. Contingencies are used so that if that element fails, the rest of the grid does not overload. In market and CRR/FTR models, ISOs often include contingencies that **significantly affect congestion**; binding constraints and transfer limits can be enforced in the **post-contingency** case as well as in the base case.

**Constraint vs device vs contingency:**

- **Each constraint = one device.** In binding-constraint and shift-factor tables, each **constraint** is a single network element (e.g. one transmission line, one transformer). The **DeviceName** often looks like “two things” (e.g. `1739 DENISND_6949 DENISDMA 1`) because it encodes the **two endpoints** of that single element (from-bus and to-bus, and possibly circuit number). So it is **one line** or **one device**, not two separate devices.
- **Each contingency can involve many devices.** A **contingency** is one outage scenario (e.g. “line X is out”). After that outage, the system is redispatched and **other** elements can become binding. So under **one** contingency name (e.g. DFOWSMG5), there can be **many** binding constraints — one per device that binds in that post-contingency state. In other words: one contingency → many devices (many constraints); one device → one constraint, often labeled as **DeviceName | Contingency**.

**Slack bus (swing/reference bus):** In power‑flow models, the **slack bus** is a special node that **balances the system** and provides a **reference angle**. All other buses are modeled with specified injections (PQ or PV); the slack bus has a fixed **voltage magnitude and angle** (often $|V|$ fixed and angle $0^\circ$), and its **real and reactive power injections are solved for** so that total generation equals total load plus losses. Physically it represents the “rest of the grid” or a large balancing generator that absorbs whatever mismatch remains after all other injections and withdrawals are applied.

---

## 3. FTR/CRR Definition and Payoff

A **Point-to-Point (PTP)** right is defined by a **source** (injection) and **sink** (withdrawal) settlement point.

**PTP obligation** payoff:

$$
\text{Payoff} = (\text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}}) \times \text{MW}.

$$

Can be positive (payment) or negative (charge).

**PTP option** payoff:

$$
\text{Payoff} = \max(0,\, \text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}}) \times \text{MW}.

$$

Option pays only when the spread is positive; no charge when it is negative.

**Naming:** CAISO and ERCOT use **CRR**; PJM and MISO use **FTR**. Same economic idea; settlement (DAM vs RT, loss treatment) differs by market.

---

## 4. North American Markets — Comparison


| Market     | Instrument | Settlement     | Obligation / Option                  | Notes                                                           |
| ------------ | ------------ | ---------------- | -------------------------------------- | ----------------------------------------------------------------- |
| **PJM**    | FTR        | DAM LMP spread | Both                                 | Annual + monthly auctions                                       |
| **ERCOT**  | CRR        | DAM SPP spread | PTP only; DAM PTP (QSE) for RT hedge | Monthly + long-term auctions; DAM PTP obligations hedge DAM→RT |
| **CAISO**  | CRR        | DAM            | PTP                                  | Allocation + auction; deration when deliverability drops        |
| **MISO**   | FTR        | DAM            | Both                                 | Annual + monthly                                                |
| **NYISO**  | TCC        | DAM            | Similar PTP                          | Transmission Congestion Contracts                               |
| **ISO-NE** | FTR        | DAM            | —                                   |                                                                 |
| **SPP**    | TCR        | DAM            | —                                   | Transmission Congestion Rights                                  |

---

## 5. Creation and Allocation

**Allocation:** Rights are granted to load or transmission owners before auction (e.g. **NOIEs** in ERCOT receive **Pre-Assigned CRRs (PCRRs)**; remainder goes to auction).

**Auction:** Participants submit bids to buy and offers to sell. The ISO runs a **feasibility test** (e.g. **SFT — Simultaneous Feasibility Test**) so the awarded set of FTRs/CRRs is **simultaneously feasible** on the transmission model. Only feasible combinations are awarded.

**Revenue adequacy:** Under the same network and assumptions, **congestion rent** should be at least **total FTR/CRR payouts**. In practice, **shortfall** can occur (outages, model changes, losses), leading to **proration** of payouts or **shortfall charges** to FTR/CRR holders.

**ERCOT: network model (and contingencies) before auction.** ERCOT does **not** publish a separate “contingency results” file before the CRR auction. It **does** post the **CRR Network Model** on the **Market Information System (MIS) Secure Area** (and in the CRR Market User Interface) **prior to each auction**. That model includes the **contingencies** that significantly affect congestion and are used in the auction clearing engine, so contingency-related information is available for bid/offer strategy. The **CRR Activity Calendar** (by April 1 each year) includes **Network Model Posting Dates** for planning.

---

## 6. Deration (CRR/FTR Reduction)

**Deration:** When the network model or outages reduce deliverable capacity, the ISO may **reduce** (derate) the MW of existing CRRs/FTRs so the remaining set stays feasible. **CRR deration** (e.g. ERCOT, CAISO): existing CRRs can be cut. **Deration analysis** is the assessment of which paths and periods are exposed and by how much.

---

## 7. Key Formulas Summary


| Concept          | Formula                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------- |
| LMP at node      | $\text{LMP}_n = \lambda - \sum_k \mu_k \cdot \text{SF}_{n,k}$ (+ loss term if applicable) |
| PTP obligation   | $(\text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}}) \times \text{MW}$                |
| PTP option       | $\max(0,\, \text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}}) \times \text{MW}$       |
| Revenue adequacy | Congestion Rent$\geq$ Total FTR/CRR Payouts (same model)                                  |

---

## 8. Risks in Congestion Trading

- **Model risk (mispricing paths):** Congestion, LMP, or constraint models are wrong (constraints, outages, load, generation, topology, TOU patterns), so you systematically **overpay for low‑value paths** or **under‑hedge real risk**.
- **Volume and shape risk:** Hedge has the wrong **MW**, **time‑of‑use block**, or **seasonality** relative to the underlying exposure (physical load, generation, PTPs, virtuals), leaving **residual unhedged congestion** or creating **over‑hedged positions**.
- **Topology and outage risk:** Real‑world topology (planned/unplanned outages, new lines, derates, dynamic ratings) diverges from the **auction network model**, so constraints **move or disappear**, and new constraints appear.
- **CRR/FTR deration and revenue adequacy risk:** ISOs may **derate CRRs/FTRs** or experience **shortfalls in congestion rent**, so actual payouts are **less than modeled**, even if congestion realized in the expected direction.
- **Liquidity and exit risk:** Many CRR/FTR paths are **illiquid**; secondary markets are thin, making it hard to **resize or unwind** positions without **price impact** or slippage.
- **Credit and margin risk:** Auctions and positions consume **credit limits**; adverse mark‑to‑market moves can trigger **margin or collateral calls**, forcing de‑risking at bad times or crowding out other trades.
- **Regime and rule‑change risk:** Changes in **market design**, **network modeling**, or broader **policy/regulatory shifts** alter congestion patterns and break strategies calibrated on historical data.
- **Correlation and tail risk:** Constraints, hubs, and paths that look diversified can **co‑move under stress** (extreme weather, fuel shocks, large outages), causing the portfolio to behave like a **concentrated bet** with large tail P&L swings.

### 8.1 Market Risk on a Single FTR Path

- **Spread (level) risk:** The realized spread $LMP_{\text{sink}} - LMP_{\text{source}}$ for the path is very different from your **expected spread** because constraints, outages, load, fuel prices, or topology evolve differently than modeled.
- **Direction (sign) risk:** You are long congestion in one direction (e.g. Sink $>$ Source), but in realized markets the dominant congestion is the **opposite sign**, turning the FTR into a **loss‑maker** instead of a hedge.
- **Volatility risk:** Even if the **average** spread is roughly right, higher‑than‑expected **volatility** in daily/hourly spreads leads to larger P&L swings and higher VaR/ES on that path.
- **Path‑specific basis risk:** The FTR nodes do not perfectly match your **physical or financial exposure** (e.g. path is Hub→Zone, but your risk is at a particular node), leaving **residual basis** between the FTR payoff and your true exposure.
- **Constraint‑mix risk:** The path’s spread is driven by a **changing mix of constraints** over time; value can migrate to constraints you did **not** intend to express a view on.
- **Tenor and seasonality mismatch:** A monthly/annual FTR may underperform if the path’s value is **seasonal or event‑driven** (e.g. only pays in a few extreme weeks) and those events do not occur in the tenor you hold.
- **Crowding and auction‑price risk:** Popular “obvious” paths can clear at **inflated auction prices** when many participants share the same view, so even if congestion materializes your **entry price** can eat most of the P&L.

### 8.2 Historical analysis to build probabilistic binding models

To design FTR portfolios around **individual constraints**, it is useful to estimate, for each constraint $k$, a **probabilistic binding model**: $P_k(\text{binds} \mid \text{state})$.

- **Data set construction (per constraint):**

  - Build a long history of **DAM/RT runs** (or security‑constrained dispatch runs) with:
    - Binary **binding indicator** $Y_{k,t} \in \\{0,1\\}$ for each constraint $k$ and day/hour $t$.
    - Associated **shadow price** $\\mu_{k,t}$ (zero or near‑zero when not binding).
    - **System state features** $X_t$: load by region, net exports, fuel prices, topology flags, season, TOU, weather indices, outage indicators, etc.
  - Optionally augment with **path‑level features** that measure how important constraint $k$ is for the FTR paths you care about (e.g. distribution of $\Delta \text{SF}^{(k)}_{\text{path}}$).
- **Static binding‑probability models:**

  - **Logistic / probit regression:** Model $P(Y_{k,t}=1 \\mid X_t)$ as a function of system state (and possibly lagged $Y_{k,t-1}$). Output is an **estimated binding probability** for each future scenario.
  - **Generalized linear models with splines / interactions:** Capture non‑linear effects such as “binds only when load in Zone A is high **and** a certain line is out”.
  - **Tree‑based methods (random forest, gradient boosting, XGBoost):** Non‑parametric models that naturally handle interactions and thresholds in $X_t$; give both **binding probability** and **variable importance** for drivers of congestion on each constraint.
- **Time‑series and regime‑switching structure:**

  - **Markov / regime‑switching models:** Allow constraints to have **regimes** (e.g. “normal”, “high‑stress summer”, “winter storm”) with different binding probabilities; model transitions between regimes over time.
  - **Hidden Markov Models (HMMs):** Treat observed binding patterns as emissions from a small number of latent **system‑stress states**; infer the probability that the system is in each state and the constraint‑specific binding probability in that state.
  - **Autoregressive components:** Include lags of $Y_{k,t}$ and $\\mu_{k,t}$ to capture **persistence** (constraints that once bind are more likely to bind again in nearby hours).
- **Joint structure across constraints:**

  - **Copula / multivariate probit models:** After estimating marginal $P_k(\\text{binds})$, impose a **dependence structure** across constraints to simulate **joint binding events** (important for portfolio tail risk).
  - **Dimension reduction:** Use **PCA / factor models** on the matrix of $Y_{k,t}$ (constraints × time) to identify a few **common congestion factors**; then model factor dynamics and map back to per‑constraint binding probabilities.
- **From historical model to FTR inputs:**

  - For each planning horizon/scenario, use the model to produce:
    - **Binding probability** for each constraint $k$ (marginal and conditional on scenarios).
    - **Conditional distribution of shadow prices** $\\mu_{k}$ given binding.
  - Combine with **path shift factors** to derive a **distribution of congestion rent** per path and a **constraint‑centric view** of which constraints drive path risk most of the time and in the tails.

These historical‑analysis tools let you move from a purely **deterministic** view of binding constraints to an **explicit probabilistic model** that can be plugged into FTR portfolio optimization and risk management.

### 8.3 Simulating shadow prices with skewed and high‑kurtosis distributions

Constraint **shadow prices** $\mu_k$ are often **zero or near‑zero** when the constraint does not bind, and **positive** (sometimes large) when it binds. The resulting **unconditional** distribution is **highly skewed** and **fat‑tailed** (high kurtosis): a point mass at zero and a right tail of positive spikes. Simulating $\mu_k$ realistically is needed for congestion revenue, FTR payouts, and basis simulation (Section 10.1). Practical approaches:

- **Two‑part (hurdle) and zero‑inflated models:** Split the draw into **(1) bind or not**, **(2) magnitude of $\mu_k$ given binding**. Step 1: draw the binding indicator from a binary model (e.g. logistic / probit as in Section 8.2, or empirical frequency). Step 2: **conditional on binding**, draw $\mu_k$ from a distribution fitted to **observed positive $\mu_k$ only**. This avoids diluting the positive tail with zeros and preserves **skewness and kurtosis** of the positive part. **Zero‑inflated** formulations explicitly model $P(\mu_k = 0)$ and the distribution of $\mu_k \mid \mu_k > 0$ (e.g. zero‑inflated gamma or lognormal).

- **Heavy‑tailed distributions for the positive part:** For $\mu_k \mid \mu_k > 0$, use a distribution that allows **skew and fat tails**. **Lognormal** is simple and right‑skewed but often **understates** extreme spikes. **Gamma** and **Weibull** are right‑skewed and non‑negative. **Student‑$t$** (possibly shifted/truncated to be positive) or **skewed‑$t$** add **kurtosis**. **Stable** (e.g. Lévy) or **generalized Pareto** (for the tail above a threshold) capture **very heavy tails**. **Mixtures** of two or more distributions (e.g. “normal” vs “spike” regime) can match both the bulk and the tail of empirical $\mu_k \mid \text{bind}$.

- **Conditional distribution from binding model:** Use the **binding probability** $P(Y_{k,t}=1 \mid X_t)$ from Section 8.2; then model the **conditional distribution** of $\mu_{k,t}$ given $Y_{k,t}=1$ (and optionally $X_t$) via regression (e.g. **quantile regression** for several quantiles), **GLM** (e.g. gamma with log link), or **non‑parametric** (kernel density on positive $\mu_k$). Simulate by first drawing $Y_{k,t}$ from the binary model, then if $Y_{k,t}=1$ drawing $\mu_{k,t}$ from the fitted conditional distribution. This keeps **state‑dependent** levels and tail.

- **Empirical and semi‑parametric:** **Resample** (bootstrap) from **historical positive $\mu_k$** (optionally stratified by season, TOU, or system state) to preserve empirical skew and kurtosis without assuming a parametric form. **Kernel density estimation (KDE)** on $\ln(\mu_k)$ or on $\mu_k$ (with boundary correction for the origin) gives a smooth density for the positive part. **Quantile‑based** simulation: fit quantiles (e.g. 0.5, 0.9, 0.99, 0.999) and interpolate or use a **piecewise** distribution; good for matching **tail percentiles** used in VaR/ES.

- **Joint simulation across constraints:** Shadow prices of **multiple** constraints are **dependent** (e.g. same hour, same stress). After fitting **marginal** distributions (each $\mu_k$ via two‑part + heavy‑tailed or empirical), impose **dependence** with a **copula** (e.g. **$t$‑copula** for tail dependence) on the probability integral transforms. Alternatively, **factor structure**: $\mu_k = f_k(Z) + \varepsilon_k$ where $Z$ is a low‑dimensional stress factor and $\varepsilon_k$ are residuals; simulate $Z$ and $\varepsilon_k$, then form $\mu_k$. Preserves **joint spikes** (many constraints binding together in stress).

- **Regime and stress scenarios:** In **high‑stress** regimes (e.g. heat wave, major outage), both **binding probability** and **conditional $\mu_k$** can be much higher. Use **regime‑switching** (Section 8.2): in the “stress” regime, use a distribution for $\mu_k \mid \text{bind}$ with **higher mean and variance** (or a separate fitted distribution for stress hours). **Stress testing**: set $P(\text{bind})=1$ and draw $\mu_k$ from the **upper tail** or from a **conservative** distribution to assess worst‑case congestion revenue and FTR payouts.

**Summary:** Simulate **binding vs not** first (e.g. from Section 8.2), then **magnitude given binding** with a **skewed, heavy‑tailed** or **empirical** distribution. Two‑part / zero‑inflated + lognormal, gamma, skewed‑$t$, or Pareto tail are common; copulas or factor models handle **joint** constraint shadow prices for portfolio and basis simulation.

---

## 9. Shadow Prices, Shift Factors, and Path Value

### 9.1 Congestion rent on a path vs shadow price

**Congestion rent on a path** and **shadow price** are related but **not the same**.

- **Shadow price (of a constraint):** \$/MW — the marginal value of relaxing that **constraint** by 1 MW in the optimization. It is defined **per constraint**, not per path.
- **Path value (congestion component of the spread):** For path Source→Sink,
  $$
  \text{Path value} = \text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}}.

  $$

  With multiple binding constraints, this spread equals a **sum over constraints** of (shadow price × the path's shift-factor difference for that constraint), not a single shadow price.

### 9.2 Source and sink each have a shift factor per constraint

A **path** is between two settlement points (e.g. nodes A and B). For each **binding constraint** $k$:

- **Source node** has shift factor $\text{SF}_{\text{source},k}$.
- **Sink node** has shift factor $\text{SF}_{\text{sink},k}$.

The **path's sensitivity** to constraint $k$ is the difference:

$$
\Delta \text{SF}^{(k)}_{\text{path}} = \text{SF}_{\text{sink},k} - \text{SF}_{\text{source},k}.

$$

Constraint $k$'s **contribution** to the path's spread is

$$
\Delta \text{LMP}^{(k)}_{\text{path}} = -\mu_k \,\Delta \text{SF}^{(k)}_{\text{path}}.

$$

### 9.3 Each path has multiple shadow-price contributions

A single path does **not** have one shadow price. It has **one contribution per binding constraint**:

$$
\text{LMP}_{\text{sink}} - \text{LMP}_{\text{source}} = \sum_k \Delta \text{LMP}^{(k)}_{\text{path}} = -\sum_k \mu_k \big( \text{SF}_{\text{sink},k} - \text{SF}_{\text{source},k} \big).

$$

So: **one shadow price per binding constraint**; the path's value is the **sum** of (constraint shadow price × path's shift-factor difference) over all binding constraints. If $\text{SF}_{\text{sink},k} \approx \text{SF}_{\text{source},k}$ for a constraint, that constraint contributes little to the path even if $\mu_k$ is large.

### 9.4 One shadow price per binding constraint

- Each **binding constraint** has **one** shadow price $\mu_k$ in a given run (DAM/SCED). That $\mu_k$ is the **same** for all nodes and all paths.
- Each **node** has a **shift factor** for each constraint: $\text{SF}_{n,k}$.
- So: **one shadow price per constraint**; **one shift factor per (node, constraint)**. There is no single "shadow price for the path" or "one shadow price for all nodes."

### 9.5 Example: path A→B with 10 binding constraints

For path **A → B** (A = source, B = sink) and **10 binding constraints** $k=1,\ldots,10$:

- For each constraint $k$: one **shadow price** $\mu_k$, one **shift factor at A** $\text{SF}_{A,k}$, one **shift factor at B** $\text{SF}_{B,k}$.
- The **contribution** of constraint $k$ to the A→B spread is $-\mu_k (\text{SF}_{B,k} - \text{SF}_{A,k})$.
- The **total path spread** is $\text{LMP}_B - \text{LMP}_A = \sum_{k=1}^{10} \big(-\mu_k (\text{SF}_{B,k} - \text{SF}_{A,k})\big)$.

There is **not** a separate "shadow price for A→B" stored anywhere; the path's value is **derived** from the constraint shadow prices and the two nodes' shift factors.

### 9.6 In ERCOT (and similar markets)

When the market runs (DAM or SCED):

- You get **one shadow price per binding constraint** (e.g. $\mu_1, \mu_2, \ldots$), not one shadow price for the whole system or for all nodes.
- You get **one shift factor per (node, constraint)** — each node has its own $\text{SF}_{n,k}$ for each constraint $k$.

The **LMP at each node** $n$ is

$$
\text{LMP}_n = \lambda - \sum_k \mu_k \cdot \text{SF}_{n,k}.

$$

So: the **same** constraint shadow prices $\mu_k$ are used for every node; what differs by node is the **shift factors** $\text{SF}_{n,k}$. That is why each node has a different LMP and why path spreads differ. There is **no** single "one unique shadow price for all the nodes."

---

## 10. Market Risks for a Solar Energy Producer

A **solar energy producer** sells energy (and possibly ancillary services) at the **LMP** at its node or hub. Beyond general congestion and FTR risks (Sections 8–9), solar faces **generation-specific** and **profile-specific** market risks.

- **Volume and shape risk (intermittency and profile):** Solar output is **zero at night** and peaks around solar noon. **Realized generation** can differ from forecast due to **clouds**, **soiling**, **curtailment**, and **availability**. If hedges (PPAs, forwards, FTRs) are **flat** in MWh or tied to a different shape (e.g. peak-only), the producer bears **shape risk**: revenue is low when the sun is strong but **prices are low** (e.g. midday duck curve), and high when output is weak but prices are high. **Volume risk** is the deviation of actual MWh from expected, affecting both energy revenue and any volume-linked obligations.

- **Price (revenue) risk:** Revenue = **volume × price**. Even with perfect volume forecast, **LMP** at the plant node can be low when solar is generating (e.g. **merit-order effect**: high solar supply depresses prices). **Negative prices** in surplus hours increase risk. Revenue is exposed to **energy price level**, **volatility**, and **correlation** between solar output and price (often **negative** in midday).

- **Congestion and locational risk:** The plant receives the **LMP at its node**, not the hub or load-weighted average. **Congestion** can **decouple** the plant node from the rest of the system: the node can be **congested out** (low or negative LMP when the rest of the system is high) or **congested in** (high LMP when the plant is generating). **Transmission outages** or **new generation/load** nearby can **shift constraints** and change the plant’s **shift factors** and exposure to binding constraints, altering the value of any FTR/CRR used to hedge.

- **Curtailment and deliverability risk:** The ISO or utility may **curtail** solar when **congestion** or **oversupply** (e.g. minimum generation, voltage, stability) limits deliverability. Curtailment is **volume loss** at times when the plant could have generated; it is often **correlated with low prices** (curtailment and low LMP both occur in high-solar, low-load hours), so revenue impact is compounded. **Network upgrades** or **changes in priority** (e.g. pro forma LGIP, deliverability status) can change curtailment frequency and magnitude.

- **Basis and PPA risk:** If the producer has a **fixed-price PPA** or a **floating PPA** indexed to a hub, **basis risk** is the spread between **revenue at the plant node** (actual LMP × actual MWh) and the **contract reference** (e.g. hub LMP × contract volume). **Congestion** and **losses** drive this basis. FTRs/CRRs can hedge **part** of the congestion component of the spread between plant node and reference, but **volume and shape** (actual vs contract MWh and timing) remain. **Contract tenor**, **termination**, and **credit** of the offtaker add further market and counterparty risk.

- **Seasonality and tenor mismatch:** Solar value is **highly seasonal** (summer vs winter insolation) and **intraday** (day vs night). **Monthly or annual FTRs/CRRs** may not match the **hours when solar generates**; a path that pays in peak hours may not align with solar’s peak. **Seasonal and TOU alignment** between hedges and actual generation is critical to avoid **residual unhedged** or **over-hedged** positions.

- **Regulatory and policy risk:** **Subsidy changes** (e.g. ITC, production tax credit, state REC programs), **net metering** or **export tariff** changes, and **capacity or ancillary service rules** affect revenue and the value of energy vs capacity. **Carbon or environmental policy** can shift the merit order and the correlation between solar output and price. These **regime changes** can alter congestion patterns and the value of FTR/CRR hedges.

- **Correlation and tail risk:** In **stress** (e.g. extreme heat, wildfires, widespread outages), **solar and load** can move together (e.g. high load and high solar), and **constraints** can bind in clusters. The producer’s **portfolio** (physical plant + FTRs/CRRs + PPAs) may exhibit **tail correlation**: losses on one leg (e.g. curtailment, low price) coincide with **adverse moves** on hedges (e.g. FTR path loses value when congestion flips). **Diversification** across nodes, paths, and tenor helps but does not remove tail risk.

### 10.1 Simulation methodologies to simulate basis

**Basis** here is the spread between two prices or price indices (e.g. **node LMP vs hub LMP**, **plant node vs PPA reference**, or **path spread** for FTR valuation). Simulating basis is needed for **P&L distribution**, **VaR/ES**, **hedge sizing**, and **contract pricing**. Common approaches:

- **Historical simulation (HS):** Use the **empirical distribution** of historical basis (e.g. daily or hourly spreads). Draw **blocks** or **single observations** from the history (with or without replacement). **Pros:** no parametric assumption; captures observed skew and tails. **Cons:** past may not repeat; limited extreme scenarios; **non-stationarity** (topology, fuel mix, renewables) can make history stale. **Variants:** **block bootstrap** (preserve autocorrelation); **filtered historical simulation** (scale residuals by current volatility); **seasonal/TOU stratification** (draw from same month or hour type).

- **Parametric (joint price) models:** Model **node and hub** (or reference) as a **bivariate distribution** (e.g. Gaussian, Student-*t*, or skewed-*t*), then basis = node − hub is implied. **Pros:** tractable; easy to vary correlation and volatilities. **Cons:** Gaussian underestimates **tails** and **skew**; energy prices are often **fat-tailed** and **bounded** (e.g. price caps, negative prices). **Improvements:** **marginal** distributions for each price (e.g. lognormal, Johnson, or empirical), then **copula** for dependence (see below).

- **Factor and regression-based simulation:** Model basis as a function of **drivers**: e.g. $\text{basis}_t = \alpha + \beta_1 \cdot \text{hub}_t + \beta_2 \cdot \text{load}_t + \beta_3 \cdot \text{renewables}_t + \varepsilon_t$, or **congestion components** (shadow prices × shift factors). **Simulate** the drivers (e.g. hub path, load, renewables from historical or parametric models), then **apply** the estimated equation to get simulated basis. **Pros:** interpretable; can stress specific drivers. **Cons:** specification risk; residuals $\varepsilon_t$ may be heteroskedastic or non-normal; need to simulate drivers consistently (e.g. joint model for hub and load).

- **Copula-based joint simulation:** Fit **marginal** distributions to **node LMP** and **reference (hub) LMP** (or to **basis** and **hub**), then fit a **copula** (Gaussian, *t*, Clayton, Gumbel, etc.) to the **rank** or **probability integral transform** of the data. **Simulate** by drawing from the copula and transforming back with the marginals. **Pros:** separates **marginals** (e.g. skew, fat tails) from **dependence** (including tail dependence). **Cons:** choice of copula and marginals; high dimensions (many nodes/hours) need **factor or vine copulas** to stay tractable.

- **Time-series and structural models:** Model basis (or its components) as **AR/GARCH**, **regime-switching**, or **jump-diffusion**. **Simulate** paths forward (e.g. Monte Carlo over horizons). **Pros:** captures **autocorrelation**, **volatility clustering**, and **regimes**. **Cons:** more parameters; multi-node or multi-hour requires **vector** models (VAR, multivariate GARCH) or **reduced form** (e.g. principal components of basis across nodes).

- **Scenario generation (optimization-based):** Generate a **discrete set of scenarios** (e.g. tree or fan) for **hub price** and **basis** (or node price) that match **moments** (mean, variance, correlation) or **historical statistics**, and optionally **probability weights**. Used in **stochastic programming** for hedging and unit commitment. **Pros:** fits into optimization; can enforce **arbitrage-free** or **consistency** constraints. **Cons:** finite scenarios; may understate tail risk unless scenarios are designed for stress.

- **Hybrid and congestion-decomposition:** Decompose basis into **energy component** (e.g. hub-related) and **congestion component** (sum over constraints of $\mu_k \cdot \Delta\text{SF}$). **Simulate** hub (e.g. historical or parametric) and **constraint shadow prices** (e.g. from binding-probability and conditional $\mu_k$ models in Section 8.2), then **reconstruct** node LMP and basis using shift factors. **Pros:** aligns with **physical** and **FTR** logic; can stress **specific constraints**. **Cons:** requires **shift factors** and **constraint model**; more data and structure.

**Summary:** A solar producer is exposed to **volume** (availability, curtailment, shape), **price** (LMP at node, merit-order effect, negative prices), **congestion** (location, shift factors, constraint mix), **basis** (node vs hub/PPA), **seasonality/TOU** (hedge vs generation profile), and **regulatory/policy** shifts. FTRs/CRRs can hedge the **congestion component** of the spread between the plant node and a reference; they do not hedge **energy price level**, **volume**, or **curtailment**.

### 10.2 Capturing shaping risk in power prices

**Shaping risk** is the risk that the **time profile** of power prices (hourly, daily, seasonal) moves against the portfolio—e.g. peak/off‑peak spreads, the duck curve, or hour‑to‑hour correlations change. It matters when **revenue or cost** depends on **which hours** (e.g. solar or load profile × LMP). Ways to **capture** it:

- **Define exposure and benchmark:** Compare **shaped** value (e.g. $\sum_h \text{generation}_h \times \text{LMP}_h$) to a **flat** price, a **reference shape** (e.g. standard peak/off‑peak blocks), or a **hedge product**. **Shaping risk** is the risk of the **spread** between realized shaped value and that benchmark.

- **Level–shape decomposition:** Split price into **level** (e.g. mean over the period) and **shape** (hourly or block deviations from the mean). Model level and shape separately (e.g. level as scalar process, shape as load‑duration or profile); simulate both so that the **profile** can shift (e.g. flatter or steeper) while level moves independently. Preserves **correlation** between level and shape if needed.

- **Principal components (PCs) or factor models:** **PCA** on hourly (or block) prices across days: first PC ≈ **level**, next PCs ≈ **shape** (e.g. peak vs off‑peak, midday dip). Simulate **PC scores** (joint or time‑series), then **reconstruct** hourly prices. Measure **sensitivity** of shaped P&L to each PC to see how much **shape** (e.g. second PC) drives risk. Allows **stress tests** on shape (e.g. “flatter” profile) without changing average level.

- **Block / index decomposition:** Define **blocks** (peak, off‑peak, super‑peak) or **indices** (e.g. 2×16, 5×16). Model **block prices** (or block spreads vs baseload) and their **correlations**; simulate jointly (e.g. copula, multivariate). **Shaping risk** is the risk that **relative** block prices move (e.g. peak weakens vs off‑peak). Value shaped exposure against **block strips** and get P&L distribution when block structure changes.

- **Historical and residual shape:** Use **historical average shape** (e.g. hourly multipliers vs daily mean) by month or hour type; model **level** and **residuals** (e.g. GARCH, regime‑switching). Simulate level and residuals, then apply **historical or stressed shapes**. Capture shaping risk by **varying the shape** (e.g. different historical periods, or perturb peak/midday) and repricing.

- **Correlation and joint simulation across time:** Fit **correlation** of hourly (or block) prices; use in **copula** or **multivariate** simulation so paths have realistic **intraday and interday** dependence. Shaping risk is then in the **joint distribution**: if peak and off‑peak correlation or variance of certain hours changes, shaped P&L reflects it.

- **Metrics:** **Profile mismatch** (e.g. RMSE or correlation between realized and expected/hedge profile); **shaped VaR/ES** (VaR/ES of shaped P&L under level+shape simulations); **sensitivity** of P&L to **shape factors** (e.g. regression of shaped P&L on level and PC2, PC3, or peak–off‑peak spread).

- **Hedging:** **Shaping basis** = shaped value − flat/block hedge; model this basis (Section 10.1) with **seasonal/TOU** stratification. **Calendar or spread options** (e.g. peak − off‑peak) hedge shape directly; their delta/gamma show how much shape risk is reduced.

**Summary:** Capture shaping risk by **(1)** defining shaped exposure and benchmark, **(2)** decomposing level vs shape (or using PCs/blocks), **(3)** simulating **joint** prices across hours so the profile can change, **(4)** measuring **shaped P&L** distribution and **sensitivity to shape factors**, and **(5)** modeling **shaping basis** vs flat/block hedges.

---

## 11. Sources of Revenue for BESS

**BESS** (Battery Energy Storage Systems) can earn revenue from several wholesale and retail streams in electricity markets. The mix depends on market rules, location, duration (hours), and how the asset is registered and dispatched.

- **Energy arbitrage:** Charge when prices are low and discharge when they are high. Revenue is the **spread** between discharge and charge prices (net of round‑trip losses and degradation). Strongest when **intraday** or **day‑ahead vs real‑time** spreads are large (e.g. solar duck curve, overnight vs peak).

- **Ancillary services:** **Frequency regulation** (e.g. ERCOT Reg‑Up/Reg‑Down, PJM Reg D, CAISO): pay for **capacity (MW)** and **performance** (accuracy, response speed). **Spinning / non‑spinning reserves**: pay for availability and sometimes for deployment. **Voltage support / reactive power** where markets or tariffs compensate it.

- **Capacity:** Capacity markets (PJM, ISO‑NE, NYISO, etc.) or **resource‑adequacy** programs (e.g. CAISO) pay for **committed capacity (MW)** in future periods. BESS can earn as a capacity resource; rules (duration, minimum run‑time, accreditation) vary by market.

- **Congestion / locational value:** Storage can reduce congestion by charging where/when LMP is low and discharging where/when LMP is high, capturing **locational spreads**. In some designs **FTRs/CRRs** or virtuals can hedge or complement this; the main revenue is from **energy** bought and sold at different nodes (implicit congestion value in LMP).

- **Black‑start and other reliability services:** Payments for **black‑start** capability or other reliability products where the ISO or utility procures them.

- **Utility or offtaker contracts:** **PPAs** or **storage service agreements**: fixed or indexed payments for **capacity (MW or MWh)** and/or performance. **Demand charge management** (behind‑the‑meter): value is **reduced demand charges** for the host.

- **Renewable pairing and shaping:** Co‑located or virtually paired with **solar/wind**: charge on excess renewable output, discharge into high‑price periods. Revenue can be structured as **energy + capacity + ancillary** or embedded in a **renewable PPA** (e.g. “solar + storage” offtake).

- **Market‑based demand response:** Where BESS is eligible, participation in **demand‑response** or **load‑curtailment** programs that pay for reducing demand or providing flexibility at key times.

**Summary:** Main **wholesale** revenue streams are **energy arbitrage**, **frequency regulation**, **other ancillary services**, and **capacity**; **congestion** value is captured through energy buy/sell at different nodes. Contracted revenue (PPAs, utility deals) and **retail** value (demand charges, backup) add to the stack.

### 11.1 Risks for BESS

BESS faces **market**, **operational**, **regulatory**, and **financial** risks that can reduce revenue or increase cost.

- **Market and price risk:** **Spread/arbitrage risk**: DA–RT or intraday spreads can **compress** as more storage, renewables, or flexible supply enters the market, reducing arbitrage margin. **Ancillary service price risk**: regulation and reserve **clearing prices** are volatile; new entrants or rule changes can lower capacity and performance pay. **Capacity value risk**: **accreditation** (e.g. ELCC) can be derated over time; capacity demand curves and rules change. **Congestion/locational risk**: value depends on **nodal LMPs**; topology, new generation/load, or transmission upgrades can reduce locational spreads.

- **Operational and technical risk:** **Availability and performance**: outages, derates, or failure to meet **performance** (e.g. regulation accuracy) cut revenue and can trigger **penalties**. **Degradation and cycle life**: capacity and efficiency **fade** with use; aggressive cycling for arbitrage or regulation shortens **cycle life** and raises replacement risk. **Round‑trip efficiency**: real efficiency below assumptions reduces net spread and increases effective cost of energy.

- **Regulatory and policy risk:** **Market design and rule changes**: new products, settlement rules, or **eligibility** (e.g. duration limits, minimum size) can shift value across revenue streams. **Safety and standards**: stricter **fire/safety** or grid codes can increase cost or restrict siting/operation.

- **Financial and counterparty risk:** **Revenue stacking and cannibalization**: more storage (or other flexibility) competing for the same spreads and ancillary products can **erode** prices. **Contract and offtaker risk**: PPA or utility contract **tenor**, **termination**, **credit**, and volume/performance guarantees affect contracted revenue. **Capital and financing**: high **upfront cost** and cost of capital; revenue uncertainty can make refinancing or project finance harder.

**Summary:** BESS is exposed to **market** (spreads, ancillary and capacity prices, location), **operational** (availability, degradation, efficiency), **regulatory** (rules, safety), and **financial** (cannibalization, contracts, financing) risks.
