# FTR Trading: Before the Auction, After the Auction, and How a Quant Can Help

From the perspective of a seasoned FTR trader: what FTR trading is, the analysis we do before each auction, what we do after the auction until settlement, and how a quantitative researcher supports the desk.

---

## 1. What is FTR trading?

**FTR (Financial Transmission Right)** or **CRR (Congestion Revenue Right)** is a **financial** contract that pays (or charges) the holder based on the **price difference** between two locations — the **path**: source (injection) and sink (withdrawal) — over a set period (e.g. a month, a quarter, a year). The payoff is **congestion**: when the grid is constrained, LMPs diverge; the path spread (sink price − source price) is exactly what FTRs are designed to hedge or trade.

- **Obligation:** You receive the path spread when it’s positive and **pay** when it’s negative (so you are “short” congestion the wrong way if the spread goes against you).
- **Option:** You receive the path spread when it’s positive and **pay nothing** when it’s negative (optionality).

We **don’t** trade power physically on the path; we trade the **right** to the **financial** payoff. We **acquire** FTRs mainly via **ISO auctions** (e.g. ERCOT, CAISO, PJM). So FTR trading is: (1) **deciding which paths to bid on** and **at what price and volume**, (2) **submitting bids** in the auction, (3) **managing the position** from award until **settlement** (MtM, risk, optional hedging), and (4) **receiving (or paying)** at settlement.

**Why we trade FTRs:** To **capture congestion value** (paths we think will pay), to **hedge** our own congestion exposure (e.g. generation or load at a node), or to **speculate** on future congestion. Success depends on **understanding which constraints drive congestion**, **when** they bind, **how** outages and fundamentals affect them, and **how** that maps to **path value** and **auction clearing**.

---

## 1.1 Formulas and assumptions (reference)

### Payoff and path spread

- **Path spread** (one settlement interval): $\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}}$, where $\lambda$ is the **reference price** (e.g. LMP or SPP) at the settlement point for that interval.
- **Obligation payoff** (per MW, one interval): $\pi_{\mathrm{obl}} = \lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}}$. Can be positive (we receive) or negative (we pay).
- **Option payoff** (per MW, one interval): $\pi_{\mathrm{opt}} = \max(\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}},\ 0)$.
- **Total payoff** over the CRR period (e.g. a month): sum over all settlement intervals in the period of (payoff per interval $\times$ volume in MW $\times$ length of interval in hours or fraction of hour). For **energy-weighted** settlement, the reference is usually the **average** price over the interval at sink and source; formulas are applied per interval then summed.

**Link to constraints (DC approximation):** The **congestion component** of LMP at a bus is a linear combination of **constraint shadow prices** weighted by **shift factors** (PTDFs). So the path spread can be written as:
$$
\lambda_{\mathrm{sink}} - \lambda_{\mathrm{source}} = \sum_{\ell \in \mathcal{C}} \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}},
$$
where $\mathcal{C}$ is the set of constraints, $\mu_\ell$ is the **shadow price** of constraint $\ell$ ($\$/MWh$ or $\$/MW$), and $\mathrm{PTDF}_{\ell,\mathrm{path}}$ is the **PTDF** of the path (source→sink) on constraint $\ell$. When $\ell$ does not bind, $\mu_\ell = 0$. So **path value** is driven by **binding** constraints for which the path has non-zero PTDF.

### PTDF and LODF

- **PTDF (Power Transfer Distribution Factor):** For a **transfer** of 1 MW from **source** (inject) to **sink** (withdraw), the **flow** on constraint (line) $\ell$ is:
  $$
  F_\ell = \mathrm{PTDF}_{\ell,\mathrm{path}} \times P \quad \text{(for transfer } P \text{ MW)}.
  $$
  So $\mathrm{PTDF}_{\ell,\mathrm{path}}$ is the **fraction** of the transfer that appears as flow on $\ell$. Under **DC power flow**, PTDFs are **linear** and come from the network admittance matrix.

- **LODF (Line Outage Distribution Factor):** When **line $j$** is out, the **change in flow** on line $i$ is:
  $$
  \Delta F_i = \mathrm{LODF}_{i,j} \times F_j^{\mathrm{pre}},
  $$
  where $F_j^{\mathrm{pre}}$ is the **pre-outage** flow on line $j$. So $\mathrm{LODF}_{i,j}$ is the change in flow on $i$ per unit of pre-outage flow on $j$. Used to build the **outage × constraint** impact table (flow delta on our constraint when a given outage occurs).

### Fair value (expected path payoff)

- **Path value** (one interval, per MW) in terms of constraints:
  $$
  V_{\mathrm{path}} = \sum_{\ell} \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}.
  $$
- **Expected path payoff** over the CRR period (fair value per MW): 
  $$
  \mathrm{FV}_{\mathrm{path}} = \sum_{\mathrm{intervals}} D(t) \cdot \mathbb{E}\bigl[ \pi_{\mathrm{path}}(t) \bigr],
  $$
  where $\pi_{\mathrm{path}}(t)$ is the payoff per MW in interval $t$ (obligation or option) and $D(t)$ is discount factor if we discount. Often we work in **undiscounted** $/MWh$ or **total $/MW** over the period; then $\mathrm{FV}_{\mathrm{path}} = \mathbb{E}[\text{sum of interval payoffs per MW}]$. We estimate this from **historical** shadow prices and binding frequency, **PCM** output, or **scenario-weighted** average.

### Mark-to-market (MtM)

- **MtM** of a position = **expected payoff** over the **remaining** life of the CRR, using **current** forward prices (or congestion view):
  $$
  \mathrm{MtM} = Q \cdot \sum_{\mathrm{remaining\ intervals}} \mathbb{E}\bigl[ \pi_{\mathrm{path}}(t) \mid \mathcal{F}_{\mathrm{today}} \bigr],
  $$
  where $Q$ is volume (MW). In practice we use **forward** path spread (or hub spread) curve and remaining tenor; optional discounting.

### VaR (risk factor mapping)

- **Change in value** (e.g. 1-day) for a portfolio of FTRs:
  $$
  \Delta V \approx \sum_{\mathrm{paths}} Q_p \cdot \bigl( \text{remaining MW$\cdot$h} \bigr)_p \cdot \Delta(\text{path spread}_p),
  $$
  if we use **path spread** as the risk factor. Or, with **constraint** shadow prices and PTDFs:
  $$
  \Delta V \approx \sum_p Q_p \sum_{\ell} \mathrm{PTDF}_{\ell,p} \cdot \Delta\mu_\ell \cdot (\text{remaining hours}).
  $$
  VaR is then the **quantile** of the distribution of $\Delta V$ (e.g. from historical $\Delta(\text{path spread})$ or $\Delta\mu_\ell$, or from a parametric/MC model).

### Assumptions (summary)

| Area | Assumption | Caveat |
|------|------------|--------|
| **Payoff** | Settlement on **reference price** (SPP/LMP) at contract source/sink; **no** optionality beyond contract type (obligation vs option) | Realized price may differ from reference (e.g. hub vs node); check contract |
| **Congestion** | **DC power flow**: LMP congestion = linear combination of **shadow prices** × **PTDF**; **linear** PTDFs | AC effects and losses ignored; good for congestion component |
| **PTDF / LODF** | **Topology** is known (or from vendor/ISO); **single** base topology per run; **LODF** for single-line outage | Topology changes with outages; PTDF/LODF depend on topology; MC over topologies for scenario analysis |
| **Fair value** | **Expected** payoff is approximated by historical average, PCM run, or scenario-weighted mean; **binding** frequency and shadow distribution estimated | Distribution of shadows is heavy-tailed; mean may understate risk |
| **MtM** | **Forward** path spread (or congestion) is observable or modeled; **no** funding spread in payoff | Funding/collateral affect our P&amp;L but not the ISO payoff |
| **VaR** | **Risk factors** (path spread or shadow prices) have a **stationary** or **calibrated** distribution; **mapping** position → factors is **linear** (PTDF) | Non-stationarity; tail events; mapping error if PTDF/topology wrong |

---

## 2. Analysis before each auction

Before we submit bids, we need a **disciplined** process: triage constraints, analyze outages and fundamentals, value paths, choose paths, set bid strategy. Much of the **heavy lifting** is done by an **analyst** or **quant**; as the trader I **consume** that work and **make** path/MW/price decisions. Below is what has to be done and in what order.

### 2.1 Triage: which constraints (and paths) to focus on

- **Input:** A **triage list** — the set of **constraints** (lines, interfaces, GTCs) we believe will drive congestion and FTR value in the **auction period** (e.g. the next month or quarter). This can come from historical binding reports, planning studies, analyst screens, or trader experience.
- **Why it matters:** We can’t analyze every constraint in the system. Triage **narrows** the set so we run **outage**, **fundamental**, **fair value**, and **PCM** work only on constraints (and thus paths) that matter.
- **Trader role:** I **define or approve** the triage list (e.g. with the analyst), so it aligns with our **risk** and **view** (e.g. focus on West Texas, or on interfaces into a load pocket).

### 2.2 Per-constraint analysis: planned outages and flow impact

- **What:** For **each** triage constraint, we need: (1) **planned outages** (transmission or generation) that can affect that constraint or the flow on the monitored element, (2) **probability** each outage occurs (schedule, history), (3) **flow impact** on the constraint when an outage happens — e.g. **LODF** (Line Outage Distribution Factor) or flow delta by **day of the month** for the CRR period.
- **Deliverable:** An **impact table**: rows = outages, columns = days (or periods); cells = LODF or flow delta. So we see **when** and **how much** each outage pushes the constraint.
- **Trader use:** I use this to **prioritize** paths that are **exposed** to high-value, high-probability outage scenarios and to **avoid** paths that get killed when a key line is out. It also feeds **scenario** weighting for fair value.

### 2.3 Fundamental analysis: historical binding and drivers

- **What:** For each triage constraint: **when** has it bound in the past (hour, day type, season, weather/load), and **what drives** binding (load, renewables, imports, outages). In ERCOT, **transmission planning** and study reports add context (load growth, new gen, retirements, new lines).
- **Deliverable:** Narrative and data: binding frequency, drivers, and how that might change in the **CRR window**.
- **Trader use:** I need to know **why** a constraint is in the triage and **how** it might behave in the auction month — e.g. summer peak vs shoulder, or “this constraint binds when line X is out.” That shapes **path choice** and **bid price** (e.g. pay more for paths that capture that constraint when we’re confident it will bind).

### 2.4 Fair value of the constraint (and path)

- **What:** For each triage constraint, **how much** is it “worth” over the CRR period — e.g. expected **shadow price** (or congestion component) when binding, or expected **payoff per MW** of a path that has exposure (PTDF) to that constraint. Fair value can combine **historical** shadow prices, **forward-looking** scenarios (with outage probabilities), and **model** output (DC OPF or PCM).
- **Shift factors / PTDFs:** Path value = sum over constraints of (shadow price × PTDF for the path). Shift factors (from Yes Energy, Panorama, Power World, or in-house DC model) are needed to go from **constraint** value to **path** value.
- **Trader use:** Fair value is the **anchor** for **bid price**. I compare path fair value to **auction clearing** (or broker runs) to decide if we’re bidding **rich** or **cheap** and to set **price** and **volume**.

### 2.5 Production cost modeling (PCM, e.g. Dayzer)

- **What:** Run **unit commitment** and **economic dispatch** over the CRR period (e.g. the auction month) with **load**, **generation stack**, **transmission topology**, and **outages**. Output: **hourly** (or sub-hourly) **LMPs**, **binding constraints**, **shadow prices**, and **flows**.
- **Use:** PCM gives a **forward** view of **when** and **where** constraints bind and **how much** congestion they produce. We use it to **ground** fair value, **stress** scenarios (e.g. with/without a planned outage), and **path** ranking.
- **Trader use:** I rely on the analyst/quant to run PCM and hand me **constraint-level** and **path-level** expected congestion (or distribution). I use it to **sanity-check** fair value and to **size** bids (e.g. paths that show high PCM value get more attention and possibly higher bid price).

### 2.6 Scenario analysis (e.g. Monte Carlo on topology / shift factors)

- **What:** **Uncertainty** in **which outages** occur (and thus **topology** and **shift factors**) means constraint and path value are **random**. Scenario analysis (e.g. MC draws of outage sets, or sampling topologies) produces a **distribution** of constraint value or path value instead of a single number.
- **Use:** **Risk** (e.g. downside/upside), **bid sizing** (how much MW at what price given that distribution), and **sensitivity** to outage assumptions.
- **Trader use:** I want to see **percentiles** (e.g. 10th, 50th, 90th) of path value so I can bid **aggressively** on paths with good downside and **conservatively** on paths with high variance or outage sensitivity.

### 2.7 Mapping: exposure → path, constraint → path, names

- **What:** (1) **Exposure → path:** Our **physical or commercial** exposure (e.g. gen at node A, load at zone B) must be **mapped** to **biddable** paths; often no perfect match → **basis risk**. (2) **Constraint → path:** Triage constraints are **constraint-centric**; the auction is **path-centric**. We need **path PTDFs** to the triage constraints so we know **which paths** actually capture the value we analyzed. (3) **Names and settlement:** Node/bus/path **names** and **settlement point** definitions (ERCOT SPP, CAISO LMP) must be **consistent** across data, PCM, and bid submission; **retired** or **renamed** nodes require mapping (internal or vendor).
- **Trader use:** I need to know that the **paths we bid** are the right **proxy** for our analysis and our exposure. Mapping errors (wrong path, wrong hub, stale names) lead to **wrong** fair value and **wrong** hedge.

### 2.8 Choosing paths (source–sink) and bid strategy

- **Path choice:** Using triage, fair value, outage impact, PCM, scenario output, and **mapping**, we **select** a **short list** of **source–sink paths** to bid. Prefer paths with **strong PTDF** to **high fair-value** constraints, **robust** to outages we care about, and **liquid** / biddable in the auction.
- **Bid strategy:** For each chosen path: **MW** (volume) and **price** (or price ladder). **Price** is informed by **fair value** and **scenario** range; we may bid at fair value, below to increase fill, or with a cap. **MW** is driven by **risk**, **concentration**, and **auction** capacity/limits.
- **Trader role:** I **approve** path list and **set** (or approve) MW and price per path; I **submit** bids (or delegate submission) per auction rules (e.g. ERCOT from 2027: **one bid per strip** for sequential months — more bids to manage).

### 2.9 Pre-auction checklist (summary)

| Step | What | Trader need |
|------|------|-------------|
| 1. Triage | Constraints to focus on | Approve list; aligns with view and risk |
| 2. Outage / LODF | Impact table: outages × days | Which outages matter for which constraints |
| 3. Fundamental | Historical binding, drivers | Why constraint binds; forward view |
| 4. Fair value | Constraint and path value | Anchor for bid price |
| 5. PCM | UC/ED over CRR period; shadow prices | Forward congestion; path ranking |
| 6. Scenario | MC or scenarios on topology/value | Distribution of value; risk and sizing |
| 7. Mapping | Exposure→path, constraint→path, names | Right paths; consistent SPP/path defs |
| 8. Path choice | Short list of source–sink paths | Paths to bid |
| 9. Bid strategy | MW and price per path | What we submit |

---

## 3. After the auction until settlement (and at settlement)

Once the **auction clears**, we have a **position** (cleared paths, MW, price paid or received). From that day until **the end of the CRR month** (and then **settlement**), we monitor, mark, and manage risk.

### 3.1 Post-mortem: what cleared, what didn’t, why

- **Compare** our **bids** to **clearing**: which paths **cleared** (and at what MW/price) and which **did not**. For **uncleared** bids: was it **price** (we were below clearing), **volume** (we were cut), **path** (path not offered or oversubscribed), or **auction design**?
- **Competitor view:** Use **de-anonymization** (where possible) and **generator/location** analysis to infer **who** bid on which paths and **why** (e.g. generators hedging their nodal exposure). That informs **next** auction: path choice, price, and MW.
- **Trader role:** I **review** post-mortem with the analyst; we **adjust** path set and bid strategy for the **next** auction.

### 3.2 Mark-to-market (MtM) and VaR: each day until payout

- **MtM:** The **current value** of the FTR position = expected **congestion payoff** over the **remaining** life of the CRR. We use **forward** congestion (from curves, PCM, or historical shape) and **remaining** tenor. MtM **changes** as forwards, congestion view, or time to settlement changes. Used for **P&amp;L**, **balance sheet**, and **limits**.
- **VaR:** **Value at Risk** (e.g. 1-day, 95% or 99%) on the FTR book. Risk factors: **path spread** (or hub/zone prices, constraint shadow prices). VaR is computed **daily** (historical, parametric, or Monte Carlo) so we and risk know **exposure** until payout.
- **Trader role:** I **monitor** MtM and VaR; I need **daily** (or at least regular) reports so I can see **P&amp;L** and **risk** and stay within **limits**. If MtM or VaR moves a lot (e.g. new outage, curve move), I may **reduce** exposure (if we can trade secondary market) or **accept** the mark and wait for settlement.

### 3.3 Monitoring: outages, fundamentals, curve

- **Outages:** **Planned** outages that **start** or **end** during the CRR month can **change** which constraints bind and **path** value. I (or the analyst) **track** outage calendar and **update** view of congestion (and MtM) when topology changes.
- **Fundamentals:** **Load**, **weather**, **renewables**, and **generation** updates can shift **expected** congestion. We don’t re-run full PCM every day, but we **flag** big changes (e.g. heat wave, plant outage) and **refresh** view when material.
- **Curve:** **Forward** power (and gas) **curves** move; they affect **implied** congestion (e.g. hub spread). MtM and VaR should use **current** curves.

### 3.4 Settlement: “how many payments”

- **Settlement intervals:** The CRR payoff is **calculated** over **many** intervals (e.g. ERCOT Real-Time **15-minute** SPPs). So there are **many** intervals that **determine** total value.
- **Cash payments:** The **number of actual cash payments** from the ISO to the holder is set by **market rules**. Often the ISO **aggregates** and pays **once per period** — e.g. **one payment per month** after the month ends. So for a **monthly** CRR (e.g. January), we typically receive **one** payment **in February** (or per the ISO settlement calendar).
- **Trader role:** I need to know **when** we get paid (or pay) and **how** the final payoff is computed (e.g. sum of interval payoffs, obligation vs option). That drives **cash flow** and **reconciliation** with the ISO.

### 3.5 After-auction checklist (summary)

| Phase | What | Trader role |
|-------|------|-------------|
| **Post-mortem** | Cleared vs not; competitor view | Review; adjust next auction |
| **MtM** | Daily (or regular) mark on FTR book | Monitor P&amp;L; limits |
| **VaR** | Daily VaR on FTR book | Monitor risk; limits |
| **Monitoring** | Outages, fundamentals, curve | Update view; refresh when material |
| **Settlement** | Final payoff; payment timing | Reconcile; cash flow |

---

## 4. How a quantitative researcher can help the FTR trader

A **quantitative researcher** (or a strong quant-minded analyst) can support the **whole** cycle: **before** the auction (data, models, fair value, scenarios), **at** the auction (bid tools, checks), and **after** (MtM, VaR, monitoring). Below is what I, as the trader, **expect** and **use**.

### 4.1 Before the auction

| Need | How the quant helps |
|------|----------------------|
| **Triage** | Build **screens** (e.g. historical binding frequency, shadow price stats, correlation with load/outages) to **rank** constraints and suggest triage list. **Automate** pull of constraint lists and binding history from ISO or vendor. |
| **Outage / LODF** | **Automate** outage calendar pull and **LODF** (or flow-delta) calculation per constraint and day; produce **impact table** in a standard format. Implement or interface to **DC OPF** (or vendor) for shift factors and LODFs under different topologies. |
| **Fair value** | **Model** expected constraint value: e.g. historical distribution of shadow prices × binding probability; or **forward** scenario-weighted expected shadow price. **Map** constraint value to **path** value via PTDFs. Deliver **path-level** fair value (point and, where possible, distribution). |
| **PCM** | **Run** or **support** PCM (e.g. Dayzer): case setup, runs with/without outages, **extract** binding constraints and shadow prices. **Summarize** by constraint and path for the trader (tables, dashboards). |
| **Scenario / MC** | **Design** and **run** scenario or MC framework: e.g. draw outages from probabilities; for each topology get shift factors (or PCM output); **aggregate** to path value distribution. Deliver **percentiles** and **sensitivities** (e.g. to outage set, to load). |
| **Mapping** | **Maintain** and **automate** mapping: exposure → biddable paths; constraint → path (PTDF); node/bus/path **name** reconciliation (including retired nodes and vendor crosswalks). **Validate** that PCM and bid system use **same** path/SPP definitions. |
| **Bid strategy** | **Tool** or **model**: input path list, fair value, scenario distribution, limits → output **recommended** MW and price (or ladder). **Backtest** past auctions: our bid vs clearing vs realized payoff to **improve** strategy over time. |

### 4.2 At and after the auction

| Need | How the quant helps |
|------|----------------------|
| **Post-mortem** | **Automate** comparison: our bids vs clearing; **flag** paths that cleared/didn’t and **suggest** reasons. **Competitor** analysis: link clearing to entity/parent (e.g. from Yes Energy or public data); summarize **who** bid what and **generator** behavior. |
| **MtM** | **Build** and **maintain** MtM model: path spread (or constraint shadow) **forward** curve; map position to risk factors; **value** = expected payoff over remaining life. **Daily** run with **current** curves and tenor. **Explain** MtM change (curve, vol, time). |
| **VaR** | **Implement** VaR for FTR book: risk factors (path spread or hub/constraint); historical or parametric or MC; **map** positions to factors (e.g. via PTDFs); **report** daily VaR and, where useful, **decomposition** (which paths/factors contribute). **Backtest** VaR vs realized P&amp;L. |
| **Monitoring** | **Alerts**: e.g. when **planned outage** starts/ends that affects our paths; when **binding** or **shadow** data (from ISO) deviates from our assumption. **Dashboard**: MtM, VaR, key constraints, outage calendar, curve snapshot. |

### 4.3 Qualities I value in a quant on FTR

- **Grid and market literacy:** Understands **constraints**, **PTDF/LODF**, **shadow prices**, **path** payoff, and **auction** mechanics. Can **read** ISO/vendor data and **map** it to our triage and paths.
- **Automation and robustness:** Delivers **repeatable** workflows (triage → outage → fair value → path choice → bid) and **checks** (mapping, name consistency, units). So we **don’t** redo everything by hand each auction.
- **Clear outputs:** **Tables** and **dashboards** I can use in a **short** time: path fair value, scenario percentiles, bid recommendations, MtM, VaR. **Narrative** when something is **off** (e.g. “this path didn’t clear because clearing was above our bid by $X”).
- **Willingness to iterate:** Auction design and data **change** (e.g. ERCOT one-bid-per-strip from 2027). The quant **adapts** tools and **documents** assumptions so we can **audit** and **improve** over time.

---

## 5. One-page recap

- **FTR trading** = bid on **paths** (source–sink) in **ISO auctions**, **manage** the position from award until **settlement**, and **receive (or pay)** based on **path spread** over the CRR period.
- **Before each auction:** **Triage** constraints → **outage/LODF** impact → **fundamental** analysis → **fair value** (constraint and path) → **PCM** (forward congestion) → **scenario** (distribution of value) → **mapping** (exposure and constraint to path, names) → **path choice** → **bid strategy** (MW, price) → **submit**.
- **After auction until settlement:** **Post-mortem** (cleared vs not; competitors) → **daily MtM** and **VaR** → **monitor** outages, fundamentals, curve → **settlement** (one payment per period, per market rules).
- **Quant researcher** helps by **automating** and **modeling** triage, outage/LODF, fair value, PCM, scenario, mapping, bid recommendation, post-mortem, MtM, VaR, and monitoring — so the trader can **focus** on **view**, **risk**, and **execution**.
