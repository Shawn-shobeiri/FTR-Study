# Day in the Life of an FTR Analyst (ERCOT & CAISO)

Focus: analysis supporting the **upcoming auction** (CRR/FTR).

---

## Scope

- **Markets:** ERCOT, CAISO
- **Role:** FTR/CRR analyst preparing and running analysis ahead of the auction
- **Content:** To be filled from your inputs (workflow, data sources, deliverables, timing, etc.)

---

## What is a constraint?

A **constraint** (in this context) is a **physical or operational limit** on the power system that the ISO enforces when clearing the day-ahead or real-time market. When that limit is reached, it **binds** and affects prices and flows.

- **Transmission constraints** — Thermal, voltage, or stability limits on lines, transformers, or interfaces (e.g. “Line A–B can carry at most 500 MW”). When flow on that element hits the limit, the ISO redispatchs (e.g. backs off cheap generation and uses more expensive generation elsewhere), which creates **congestion** and **locational price differences** (LMPs diverge). Those price differences are exactly what CRRs/FTRs are meant to hedge.
- **Other limits** — Interface limits (e.g. import/export caps between zones), generation or reserve limits, or stability constraints can also be modeled as constraints.

In FTR/CRR analysis, a “constraint” usually means **the specific transmission element or interface whose limit is binding** (or likely to bind). The analyst cares about it because: (1) binding constraints drive congestion rent and CRR payoffs, and (2) **outages** (e.g. a line down) change which constraints bind and by how much, so planned-outage and flow-delta analysis are done **per constraint** to support auction strategy.

---

## What is a contingency?

A **contingency** is the **loss or unavailability of one or more system elements** (e.g. a transmission line, transformer, or generator) that is **explicitly modeled** to check that the grid remains secure **after** that loss. The system must still serve load and respect thermal, voltage, and stability limits with the element(s) out.

- **N-1:** The outage of a **single** major element (e.g. one line or one transformer). Planning and market models often enforce that the system remains feasible under N-1; **N-1 contingency** means “assume this one element is out and re-solve the power flow or dispatch.”
- **In market and CRR/FTR context:** ISOs run **security-constrained** dispatch (e.g. SCED) that can include **post-contingency constraints**: limits that apply in the **contingency state** (e.g. “after line X is out, line Y must not exceed 400 MW”). So **one contingency** (e.g. “line X out”) can create or affect **many** binding constraints in the model — one per element that becomes limiting in that post-contingency state. In binding-constraint and shift-factor data, constraints are often labeled by **device** (the element whose limit binds) and **contingency** (the outage scenario in which it binds).
- **Analyst use:** Planned-outage and **LODF** work (e.g. “flow delta on the constraint when line *j* is out”) are **contingency-based**: each outage is a contingency. The impact table (outages × days, with LODF or flow impact) is a **contingency view** of how constraint binding and congestion change when specific elements are out. Triage and fair-value analysis should account for which **contingencies** drive binding for each constraint (base case vs post-outage).

---

## Dynamic rating of an element

The **rating** of a transmission element (e.g. a line or transformer) is the **maximum flow** (typically in MW) it can carry without exceeding thermal, voltage, or stability limits. A **dynamic rating** (or **dynamic line rating**, DLR) means this limit **varies with ambient and operating conditions** rather than being a fixed **static rating**.

- **Why it varies:** Thermal limits depend on **temperature** (conductor and ambient), **wind** (cooling), **solar heating**, and sometimes **ice/snow**. So the same line may have a **higher** effective capacity on a cool, windy day and a **lower** capacity on a hot, still day. The ISO or transmission owner may use real-time or forecast weather to update the **dynamic rating** of the element (e.g. hourly or sub-hourly).
- **Impact on constraints and congestion:** When the dynamic rating **increases**, the constraint is less likely to bind (more headroom); when it **decreases**, the constraint binds more often and congestion (and shadow prices) can rise. So the analyst's view of **when** a constraint binds and **how much** it is worth depends on whether **static** or **dynamic** ratings are used in the market and in the analyst's PCM/OPF.
- **Analyst use:** For triage constraints, consider whether the element has **dynamic rating** (and if so, how it is published or modeled). Use dynamic ratings in outage/LODF and PCM work when available, so binding frequency and fair value reflect time-varying capacity. Ignoring dynamic rating can over- or understate constraint binding and path value (e.g. assuming a fixed summer static rating when actual rating is often higher in winter or during high wind).

---

## What is a shadow price?

A **shadow price** (in economic dispatch or optimal power flow) is the **dual variable** or **Lagrange multiplier** associated with a constraint. It answers: *“By how much would the objective (e.g. total production cost) improve if we relaxed this constraint by 1 unit?”*

- **In power markets:** For a **transmission constraint** (e.g. line limit in MW), the shadow price is the **marginal cost of that constraint** — the extra $/MWh (or $/MW) the system would pay to have one more MW of capacity on that line. When the constraint **binds**, its shadow price is **positive** (relaxing it would reduce cost); when it does not bind, the shadow price is zero.
- **Link to LMP:** The **congestion component** of LMP at a bus is built from the shadow prices of binding constraints, weighted by how sensitive that bus is to each constraint (e.g. via PTDFs/shift factors). So shadow prices are the “prices” of congestion that create locational price differences and drive CRR/FTR payoffs.
- **Analyst use:** Shadow prices (from SCED, PCM runs like Dayzer, or DC OPF) tell you **how much the constraint is worth** when it binds — and thus feed **fair value** of the constraint, path valuation (path value ≈ sum over constraints of shadow price × PTDF for the path), and comparison with auction clearing.

---

## PTDF and LODF

- **PTDF (Power Transfer Distribution Factor):** For a given **line** (or constraint) and a **transfer** (inject 1 MW at bus A, withdraw 1 MW at bus B, e.g. a source–sink pair), the PTDF is the **fraction of that 1 MW that appears as flow on that line**. So flow on line $\ell$ from a transfer of $P$ MW from A to B is $F_\ell = \text{PTDF}_{\ell,(A,B)} \times P$. PTDFs are linear (in the DC power-flow approximation) and come from the network admittance matrix. **Use for the analyst:** They tell you how much a trade or injection/withdrawal at two nodes changes flow on the constraint — i.e. **sensitivity of constraint flow to position**. Used in congestion analysis, FTR path valuation (path spread ≈ sum of constraint shadow prices × PTDF), and in DC OPF as shift factors.

- **LODF (Line Outage Distribution Factor):** When **line $j$ is out** (outage), the **LODF** for another line $i$ is the **change in flow on line $i$ per unit of pre-outage flow on line $j$**. So if before the outage line $j$ had flow $F_j$, then after line $j$ opens, the change in flow on line $i$ is $\Delta F_i = \text{LODF}_{i,j} \times F_j$. LODFs are derived from the same DC model (and PTDFs) and encode how power is redistributed when a line is removed. **Use for the analyst:** They give the **flow delta on the constraint (line $i$) when a planned outage (line $j$) happens** — directly supporting the impact table (rows = outages, columns = days, values = impact on the constraint). Tools like Panorama or Power World (or a DC OPF) compute PTDFs and LODFs; the analyst uses them to fill the outage × day impact table and to prioritize which outages matter most for each constraint.

---

## Tools & software

The analyst uses:

- **Panorama** — *(add use case as you provide input)*
- **Enverus** — *(add use case as you provide input)*
- **Yes Energy** — *(add use case as you provide input)*
- **Power World** — *(add use case as you provide input)*

---

## Workflow / inputs

- **Triage list from trader:** The analyst is given a **triage list** from the trader — the **list of constraints** to focus on for the upcoming auction. This list drives which constraints (and associated paths, nodes, or zones) the analyst prioritizes in ERCOT and CAISO when running congestion, power-flow, or CRR/FTR analysis.

**Correct order of workflow steps (pre-auction → auction → post-auction):**

1. **Triage list** (inputs) — constraints to focus on  
2. **Per-constraint analysis** — planned outages, outage probability, LODF table by day of month  
3. **Fundamental analysis** — historical binding, drivers of binding (e.g. ERCOT transmission planning)  
4. **Fair value of the constraint** — expected congestion value; shift factors from Yes Energy / Panorama / Power World  
5. **Production cost modeling (Dayzer)** — UC/ED simulation over CRR period; shadow prices, binding  
6. **Scenario analysis** — MC simulations for shift factors / topology uncertainty  
7. **Mapping** — exposure→path, constraint→path, node/bus names; vendor mapping (before choosing paths)  
8. **Choosing paths (source–sink)** — short list of paths for the auction  
9. **Bid strategy** — MW and price per path; submit to auction  
10. **[Auction runs]**  
11. **Post-mortem** — what cleared / did not, why; competitor analysis (de-anonymization, generator behavior)  
12. **MtM and VaR** — each day until payout; then **How many payments** (reference)



---

## Per-constraint analysis (planned outages & flow impact)

For **each constraint** on the triage list, the analyst:

1. **Planned outage analysis** — Identify and pull planned outages (e.g. transmission or generation) that can affect the constraint or the flow on the monitored line.
2. **Outage probability** — Assign or estimate a **probability that each outage will occur** (e.g. from schedules, historical availability, or operator input).
3. **Flow delta (impact of outage on the line)** — For each outage scenario, compute the **change in flow on the line where the constraint binds** (flow with outage vs. base case). This is done **by day of the month** for the **CRR month** in scope.
4. **How it’s done** — Flow deltas are calculated using **Panorama**, **Power World**, or by **running a DC OPF** (e.g. shift factors, PTDFs, or full DC OPF with/without the outage).

**Deliverable: impact table**

- **Rows:** Different outages (or outage scenarios).
- **Columns:** Different **days of the month** (for the CRR month under analysis).
- **Cell values:** **LODF** — the Line Outage Distribution Factor for the constraint (monitored line) given that outage. So each cell is the LODF value (constraint flow change per unit of pre-outage flow on the outaged line). The flow impact in MW on the constraint for that day is then LODF × (pre-outage flow on the outaged line for that day) when needed.

This table supports bidding and risk decisions for the upcoming CRR/FTR auction (which paths/constraints to target and how outage timing affects congestion).

---

## Fundamental analysis (historical binding & drivers)

For **each constraint** on the triage list, the analyst performs **fundamental analysis** to understand when and why the constraint tends to bind:

1. **Historical binding** — Review **when the constraint has bound in the past** (e.g. from SCED binding reports, shadow prices, or congestion summaries). Identify patterns by hour, day type, season, and weather/load.
2. **Drivers of binding** — Identify the **drivers** that push the constraint to its limit (e.g. high load, generation mix, renewables output, imports/exports, or specific outages). This supports forward-looking views for the CRR month and improves bid/strategy.
3. **ERCOT:** Use **ERCOT transmission planning** (e.g. planning models, constraint lists, and study results) to inform which constraints are critical, how they are expected to behave, and what drivers (load growth, new generation, retirements, new lines) affect binding. This ties historical binding to the planning narrative and to the upcoming auction period.

Outputs feed into constraint prioritization, scenario assumptions for the LODF/outage table, and narrative for the trader (why a constraint is in the triage list and how it may bind in the CRR window).

---

## Fair value of the constraint

For **each constraint** on the triage list, the analyst estimates the **fair value** of the constraint — i.e. what the constraint is “worth” in terms of expected congestion or CRR/FTR payoff over the CRR period (e.g. the auction month or term).

- **What it represents:** The value to a CRR/FTR holder when the constraint binds: e.g. expected shadow price (congestion component of LMP) or expected payoff per MW of CRR on a path that is sensitive to this constraint. Fair value guides how much to bid in the auction and how to rank constraints.
- **How it’s derived:** Can combine (1) **historical** — average or distribution of constraint shadow prices when binding (from SCED/congestion data), (2) **forward-looking** — scenario-weighted expected shadow price using binding frequency and driver assumptions from the fundamental analysis, (3) **model-based** — DC OPF or full market simulation over the CRR window to get expected congestion rent or shadow price. Outage probabilities and LODF impact (from the earlier table) can be used to adjust for planned outages that change when and how often the constraint binds. **Shift factors** used in the DC OPF or path valuation are **generated or obtained from Yes Energy, Panorama, or Power World** (see below).
- **Use:** Compare fair value to auction clearing or market-implied congestion; identify constraints that are rich or cheap relative to the analyst’s view; support bid levels and path selection for the upcoming auction.

**What is a shift factor?** A **shift factor** (in power flow / congestion analysis) is the **sensitivity of flow on a line (or constraint) to a 1 MW injection at a bus** (and corresponding withdrawal at the slack/reference bus), or equivalently the **sensitivity to a 1 MW transfer** between two buses. In the DC power-flow approximation, shift factors are linear and equivalent to **PTDFs**: they tell you how much an extra MW at a given location “shifts” onto the monitored line. So flow on constraint $\ell$ from injections $\mathbf{P}$ is $F_\ell = \sum_i \text{SF}_{\ell,i} \, P_i$ (or, for a transfer A→B, $F_\ell = \text{PTDF}_{\ell,(A,B)} \times P$). **Analyst use:** Shift factors (from Yes Energy, Panorama, or Power World) are used to compute constraint flow from bus injections, to value paths (path flow = sum of constraint flows × PTDF along the path), and to run DC OPF for fair value or congestion. They are the building blocks for constraint shadow prices and thus for the fair value of the constraint.

---

## Production cost modeling (Dayzer)

The analyst runs **production cost modeling (PCM)** to simulate unit commitment and economic dispatch over the CRR period (e.g. the auction month), using **Dayzer** software.

- **What it is:** A production cost model (PCM) solves **unit commitment (UC)** and **economic dispatch (ED)** — which units run, at what level, and at what cost — subject to transmission and operational constraints. Outputs typically include hourly (or sub-hourly) LMPs, binding constraints, shadow prices (congestion components), and flows. This gives a forward view of when and where constraints bind and what congestion value they produce.
- **Dayzer:** **Dayzer** is a commercial PCM platform used for power market simulation (e.g. ERCOT, CAISO, other ISOs). The analyst builds or updates the case (load, generation stack, transmission topology, outages), runs the simulation, and extracts constraint binding, shadow prices, and LMPs by node/zone/hub.
- **Use in the workflow:** PCM results feed into **fair value** (expected congestion/shadow prices by constraint), **fundamental analysis** (which constraints bind under the analyst's load/gen/outage view), and **scenario comparison** (e.g. with/without planned outages). Combined with the triage list, LODF/outage table, and shift factors, Dayzer helps ground constraint valuation and auction strategy in a full market simulation.

---

## Scenario analysis (MC simulations for shift factors)

The analyst runs **scenario analysis** using **Monte Carlo (MC) simulations** that vary or simulate **shift factors** (and related inputs) to assess the range of outcomes for constraint binding, congestion, or CRR/FTR value.

- **Why:** Shift factors depend on network topology (which lines are in service). Under **planned outages** or **uncertainty** in which outages occur, the effective shift factors (and PTDFs) change. MC sims let the analyst explore many topology/outage scenarios and get a **distribution** of constraint flows, shadow prices, or path values instead of a single point estimate.
- **How:** (1) Define a set of **scenarios** (e.g. draw which outages occur using the outage probabilities from the triage analysis; or sample from historical topology states). (2) For each scenario, obtain **shift factors** (and LODFs if needed) for that topology — from Yes Energy, Panorama, Power World, or an in-house DC model. (3) Run the **economic dispatch or DC OPF** (or use PCM output) with those shift factors to get constraint flow and shadow price for that scenario. (4) Repeat over many draws to get **distributions** (e.g. expected constraint value, percentiles, probability of binding).
- **Use:** Informs **risk** (e.g. downside/upside of constraint value), **bid sizing** (how much to bid given uncertainty in shift factors and binding), and **sensitivity** to outage assumptions. Complements the single-case PCM (Dayzer) run with a probabilistic view of congestion and fair value.

---

## The issue of mapping in FTRs

**Mapping** in FTR/CRR work is the problem of aligning (1) your **economic or physical exposure** (e.g. generation, load, or commercial position at specific nodes/zones) with (2) the **biddable CRR/FTR paths** and (3) the **settlement point definitions** the ISO uses. It affects path choice, hedge effectiveness, and bid strategy.

- **Exposure → path:** Your real exposure may be at **resource nodes**, **load zones**, or **hubs**. The auction offers a **limited set of paths** (e.g. hub-to-hub, zone-to-zone, or specific source–sink pairs). There is rarely a 1:1 match: you must **map** your exposure to one or more biddable paths. That can leave **basis risk** (the path you can bid doesn't perfectly track your exposure) or require a **basket** of paths to approximate the hedge.
- **Constraints → paths:** Your analysis is **constraint-centric** (triage list, LODF, fair value by constraint). CRRs are **path-centric** (source–sink). Mapping from "which constraints matter" to "which paths to bid" requires knowing **path PTDFs** (or shift factors) to those constraints: only paths with meaningful exposure to the triage constraints are relevant. Path definitions in ERCOT/CAISO may not align with the constraint set you analyzed (e.g. different node sets, hubs, or aggregation), so the analyst must map constraint impact to the actual biddable path list.
- **Settlement points:** CRRs settle on **settlement point prices** (SPPs) — e.g. hub SPP, load zone SPP. Mapping ensures the **path definition** (source/sink) matches the **SPP definitions** used for settlement (e.g. ERCOT Hub Average, specific load zones). Mismatch (e.g. valuing a path using one hub definition while settlement uses another) distorts fair value and P&L.
- **Why mapping is hard — name changes and retired nodes/buses:** A major source of mapping difficulty is that **node and bus names change over time** (ISO renames, model updates, or standardizations) and that **some nodes or buses are no longer there** (retired, merged, or restructured in the network model). Historical data, path definitions, and vendor/ISO files may refer to old names or to elements that no longer exist; linking old and new identifiers and handling "dead" nodes/buses is required for consistent constraint→path and exposure→path mapping across years and datasets.
- **Vendor mapping:** **Some vendors provide mapping** (e.g. node/bus/path crosswalks, historical-to-current identifier tables, or mapping services) to reconcile changing names and retired nodes/buses across ERCOT, CAISO, and other ISOs. The analyst can use these to align triage constraints, biddable paths, and settlement points with the correct current (or historical) definitions and to avoid using stale or invalid node/bus names in PCM, shift factors, and bid strategy.
- **In practice:** The analyst must (1) **map** physical/commercial exposure to biddable paths and quantify basis risk, (2) **map** triage constraints to paths via PTDFs so chosen paths actually capture the constraint value, (3) **use consistent SPP/path definitions** in PCM, shift factors, and bid strategy so fair value and settlement are comparable, and (4) **reconcile node/bus names and retired elements** (internally or via vendor mapping) so all inputs refer to the same, current network. Mapping issues are a recurring theme when choosing paths and setting MW/price.

---

## Choosing paths (source–sink)

Using the triage list, fair value, outage/LODF impact, PCM results, MC scenario output, and **mapping** (biddable paths, SPP definitions, node/bus alignment), the analyst **selects which paths (source–sink pairs)** to target in the upcoming CRR/FTR auction.

- **What a path is:** A **path** is a **source–sink** pair: inject power at the **source** (node, zone, or hub) and withdraw at the **sink**. A CRR/FTR on that path pays (or charges) based on the price difference between sink and source (e.g. LMP_sink − LMP_source) over the contract period. Path value is driven by **congestion** on constraints that separate source and sink — i.e. constraints for which the path has non-zero PTDF (shift factor).
- **How paths are chosen:** (1) **Constraint alignment** — Prefer paths that have strong exposure (PTDF) to the **triage constraints** with high fair value and binding likelihood. (2) **Expected value** — Rank paths by expected congestion payoff (e.g. from PCM shadow prices and path PTDFs). (3) **Risk and scenarios** — Use MC scenario output to favor paths with attractive payoff distribution and acceptable downside. (4) **Outage robustness** — Consider how planned outages (and LODF impact) affect path value; avoid paths that depend heavily on topology that may change. (5) **Liquidity and auction design** — Align with biddable path definitions (ERCOT/CAISO CRR path lists) and typical liquidity.
- **Output:** A **short list of source–sink paths** (and optionally volumes or bid levels) for the trader to use in the upcoming auction, with supporting rationale (constraint exposure, fair value, risk).

---

## Bid strategy (MW and price for chosen paths)

For each **chosen path**, the analyst (with the trader) defines **bid strategy**: **MW** (volume to bid) and **price** (or price curve) to submit in the upcoming CRR/FTR auction.

- **Price:** Informed by **fair value** of the path — e.g. expected congestion payoff (path spread) over the CRR period from PCM and scenario analysis. The bid price may be set at fair value, below it to improve fill probability, or with a spread (e.g. bid only if clearing is below a target). **Scenario/MC output** gives a range (e.g. percentile of path value) to set min/max acceptable price or to size a price ladder.
- **MW (volume):** Driven by **risk and concentration** — how much exposure to each path is desired given portfolio limits, liquidity, and correlation with existing positions. **Constraint exposure** (PTDF to triage constraints) and **outage sensitivity** (LODF/MC) inform how much MW to bid on each path; paths with high variance or outage sensitivity may get lower MW. Auction **capacity** or **offer caps** (ERCOT/CAISO rules) can cap max MW per path or per participant.
- **Auction mechanics:** Depending on the auction (e.g. pay-as-bid vs uniform price, sealed vs multi-round), the analyst may produce a **bid curve** (MW at each price level) or a single (path, MW, price) recommendation. Coordination with the trader ensures bids align with risk limits and overall book view.
- **Output:** **Bid recommendations** per path: **MW** and **price** (or price schedule), with rationale (fair value, scenario range, constraint/outage sensitivity). Ready for submission to the upcoming auction.

---

## Post-mortem analysis (after auction clears)

Once the auction has **cleared**, the analyst runs **post-mortem analysis** to learn from outcomes and refine the next cycle.

- **What cleared and what did not — and why:** Compare **our bids** to **clearing results**: which paths (and at what MW/price) **cleared** and which **did not**. For **uncleared** bids: assess whether the cause was **price** (we bid below clearing or our price was too low to clear), **volume** (we hit capacity or were curtailed), **path** (path was not offered or was oversubscribed), or **auction design** (e.g. pay-as-bid vs uniform, allocation rules). For **cleared** bids: compare clearing price to our fair value and to pre-auction view. Document **why** (e.g. “cleared on path X because we were above clearing; path Y did not clear because competitor demand pushed clearing above our bid”). This improves next round’s bid levels, path choice, and MW allocation.
- **Competitor analysis — de-anonymization of bid owners and bidding behavior:** Public or partially public auction results (ERCOT, CAISO) often report **aggregate** clearing (path, MW, price) or **anonymized** bid/offer data. **De-anonymization** is the process of inferring or matching **which market participant (bid owner)** is behind which bids or cleared positions — using patterns, public filings, ownership of assets (e.g. generation at specific nodes), and historical behavior. **Bidding behavior of generators** is of particular interest: generators often bid for CRRs/FTRs to hedge their congestion exposure (e.g. from generation at a node that is frequently congested). Analyzing **who** bid on which paths, at what price/MW, and how that aligns with **generator locations and commercial positions** (e.g. which plants, which zones) reveals competitor strategy, concentration, and likely behavior in future auctions. Outputs: (1) **cleared vs not cleared** summary with reasons, (2) **competitor view** — inferred or de-anonymized bid owners and generator bidding behavior — to inform next auction strategy and path/MW/price decisions.

---

## MtM and VaR (each day until payout)

From the day the **CRR position is held** (e.g. after auction award) until **payout** (settlement over the CRR period), the analyst (or risk team) calculates **Mark-to-Market (MtM)** and **VaR** on the CRR portfolio **on each business day** (or daily).

- **Mark-to-Market (MtM):** The **current value** of the CRR position. For a CRR on a path, value is the expected (or market-implied) **congestion payoff** over the remaining life of the CRR — e.g. path spread (sink − source price) × volume, discounted or projected using **forward congestion** (from curves, PCM, or historical shape). MtM updates as forward prices, congestion views, or remaining tenor change. Used for P&L, balance-sheet reporting, and collateral/risk limits.
- **VaR (Value at Risk):** **VaR** measures potential loss over a given horizon (e.g. 1-day) at a chosen confidence level (e.g. 95% or 99%). For CRRs, risk factors include **path spread** (or hub/zone prices driving the path), **congestion** (constraint shadow prices), and **volatility** of those factors. VaR is computed each day (e.g. historical simulation, parametric, or Monte Carlo on path spreads / constraint factors) so the firm knows exposure to the CRR book until payout. Supports **risk limits**, capital, and stress comparison.
- **Why each day until payout:** CRR value and risk **change daily** as (1) time to settlement shortens, (2) forward congestion and price curves move, (3) new information (outages, load, fundamentals) updates the distribution of settlement. Daily MtM and VaR allow the desk and risk to monitor the position, enforce limits, and attribute P&L until the CRR period is over and payout is realized.

**Steps to calculate VaR for a CRR portfolio**

1. **Define the portfolio:** List all CRR positions — path (source–sink), volume (MW), obligation vs option, and remaining tenor (e.g. days until end of CRR month). Each position’s P&L is driven by the **path spread** (sink price − source price) over the settlement intervals in the remaining life.
2. **Identify risk factors:** CRR value is sensitive to **path spreads** (or the underlying settlement point prices). Choose risk factors: (a) **path-level** — historical or implied volatility of the path spread for each path, or (b) **factor-level** — hub/zone prices or constraint shadow prices, then map path value to these via PTDFs/shift factors. For correlation and dimension reduction, **principal components** of price/spread returns are often used.
3. **Get historical data or calibrate a model:** For **historical VaR:** collect a time series of path spreads (or factor returns) over a lookback window (e.g. 1–2 years). For **parametric VaR:** estimate means, volatilities, and correlations of factor returns. For **Monte Carlo VaR:** calibrate a distribution (e.g. multivariate normal, t, or scenario-based) for factor returns.
4. **Map positions to risk factors:** For each CRR, express **change in value** (e.g. 1-day) as a function of risk-factor moves. For path-spread factors: $\Delta V \approx \sum_{\text{paths}} \text{volume} \times \text{remaining hours} \times \Delta(\text{path spread})$. If using hub/constraint factors, use PTDFs to get path spread = $f(\text{hub prices}, \text{shadow prices})$ and then $\Delta V = f(\Delta \text{ factors})$.
5. **Generate scenarios:** **Historical:** apply historical factor (or path-spread) returns to today’s position to get a set of simulated 1-day P&L outcomes. **Parametric:** draw from the estimated distribution (e.g. normal with estimated $\mu$, $\Sigma$). **Monte Carlo:** simulate many paths of factor returns (e.g. with copulas or time-series models), then revalue the portfolio each path.
6. **Compute VaR:** Order the simulated 1-day P&L outcomes (or use the analytical quantile if parametric). **VaR at confidence level $\alpha$** (e.g. 95%) is the **$\alpha$-quantile of the loss distribution** — e.g. the 5th percentile of P&L (so that with probability $\alpha$, loss does not exceed VaR). Report VaR in dollars (or as a percentage of notional) for the chosen horizon (e.g. 1-day) and confidence (e.g. 95%, 99%).
7. **Optional — liquidity and horizon:** For less liquid path spreads, apply **liquidity adjustment** (e.g. scale volatility by horizon or add a liquidation cost). For **multi-day VaR** (e.g. 10-day), scale 1-day VaR by $\sqrt{10}$ only if returns are i.i.d.; otherwise use multi-day simulation.
8. **Backtest and review:** Compare **realized P&L** to **VaR** ex post: count exceedances (days when loss > VaR). Too many exceedances suggest VaR is understated; too few may mean overstatement or clustering. Update model (e.g. vol, correlation, or tail assumption) and document for risk governance.

---

## How many payments does a CRR owner receive?

- **Settlement intervals vs cash payments:** The CRR payoff is **calculated over many settlement intervals** during the CRR term (e.g. in ERCOT, Real-Time SPPs every **15 minutes**; in other markets, **hourly**). For each interval, the holder is effectively “paid” or “charged” the congestion component (path spread × volume) for that interval — so there are **many settlement intervals** (e.g. hundreds or thousands over a month or year) that determine total CRR value.
- **Number of actual cash payments:** How many **actual payments** (cash flows from the ISO to the holder) the owner receives depends on **market rules**. Typically the ISO **aggregates** interval-level settlement and pays (or nets) on a **periodic** basis — e.g. **one payment per month** for a monthly CRR (after the month is over and final SPPs are known), or **one payment at the end** of the CRR term. Some markets may settle more frequently (e.g. weekly or daily). So in practice a CRR owner often receives **one payment per settlement period** (e.g. one payment per month for a one-month CRR, or 12 payments for an annual CRR if the market settles monthly), not one payment per 15‑minute or hourly interval.
- **CRR obligation vs option:** For an **obligation**, the owner can receive **payments** (when congestion is in the CRR direction) or make **payments** (when congestion is opposite). For an **option**, the owner receives payments when congestion is favorable and has **no payment** (no charge) when it is unfavorable. The **count** of payments is still driven by how often the market settles (e.g. monthly), not by obligation vs option.
- **When, for a given monthly CRR:** For a **monthly CRR** (e.g. January), the owner receives **one payment** (or net payment/charge) **after the CRR month ends**. The ISO needs the full month of settlement data (all 15‑minute or hourly SPPs for that month) to compute the final CRR payoff. So for a January monthly CRR, payment typically occurs **in February** (or shortly after month-end, per the ISO settlement calendar — e.g. a set number of business days after the month closes). Exact timing is set by ERCOT, CAISO, or the relevant market (see ISO settlement and invoicing calendars).

---

## Number of bids and strip structure (trader consideration)

Traders must take into account **how many bids** they submit and how those bids are structured, especially as auction design changes.

- **ERCOT from 2027:** In ERCOT, **starting in 2027**, participants **cannot submit a single price for a sequential month** (e.g. one bid covering multiple consecutive months). Instead, **one bid per strip** is required — i.e. **one bid for each strip** (each monthly or period strip in the auction). So for sequential months (e.g. Jan, Feb, Mar), the trader must submit **separate bids for each month/strip**, not one combined bid. This increases the number of bids to manage, the need for strip-level MW and price strategy, and coordination with the analyst’s path and fair-value work at the strip level.

---

## Some facts


* Atlas power creating largest congestion at charlie creek to watford 230kV in north dakota for SPP/MISO
* Riot's Rockdale crypto in ERCOT
* line flow correlation with shadow prices
* EmPower for yes energy analysis
* Live Power provides quickly updated, 60-second data on how large loads (flexible, e.g. crypto, and non-flexible, e.g. data centers) are operating.
* Demand Forecasts offer ERCOT load forecasts with regression models, weather, and near-term data. EnCompass supports future scenarios and ERCOT price trends. Infrastructure Insights shows what’s in the ERCOT large-load interconnection queue.
* ERCOT: Load and capacity (Winter 2026 Reference Case): Peak load is projected to grow from 90 GW in 2026 to 117 GW in 2031; firm capacity from 100 GW to 133 GW over the same period. 
* Capacity coming online: Substantial nameplate capacity is expected, but much new solar does not add to firm capacity because peak demand has shifted into the evening when solar output is low. Most of the increase in firm capacity comes from natural gas (combined cycle and combustion turbine) and energy storage. Texas is one of the fastest-growing battery markets; RTC+B (treating batteries as unified storage resources) is noted as supporting continued battery growth and market impact.
* Congestion overview: Average nodal congestion across all ERCOT nodes (Jan 2022–Aug 2025) shows: South Zone had the most negative congestion; Panhandle and North also negative; Houston neutral to slightly positive; West consistently positive over the period. Average monthly hub and zone congestion (delta between LMP and System Lambda) reflects these patterns—negative in South and Panhandle, positive in West.
* What happened: On the morning of Feb 19, ERCOT real-time LMPs spiked to new record levels. At one node, LMPs averaged $28,187/MWh between 8–9 AM and stayed above $12,000/MWh from 5:30 AM until 10:05 AM. The highest prices were concentrated at two settlement points in the Round Rock area: NF_BRP_RN and RHESS2_ESS1. Congestion drove these prices, not system-wide shortage: system lambda never exceeded $540/MWh and reserve price adders were small, so virtually all of the ~$28,000/MWh was congestion. ERCOT’s System-Wide Offer Cap (SWCAP) is $5,000/MWh (reduced from $9,000 after Winter Storm Uri), but nodal LMPs can exceed SWCAP when there are irresolvable constraints. There were 13 constraints binding between 8–9 AM at RHESS2_ESS1, each adding at least $688 to the LMP, for a cumulative congestion impact over $26,500. The previous ERCOT RT record was just over $12,700/MWh during Uri (extreme congestion plus system-wide offers at the then $9,000 cap)
* PowerSignals is used to visualize nodes, nodal prices, transmission, outages, constraints, plants, weather, and gas in one place and to drill into maps, charts, and tables to identify drivers of volatility and avoid over- or under-bidding on follow-on days.
- **Context:** **West Texas** is known for **extreme congestion** given its more isolated position on the ERCOT grid. In **October 2024**, the **Odessa Switch to Yarborough** constraint (**Odehv–Yarbr**) produced a distinct congestion pattern. For users of **Live Power** grid monitoring, this represented a major **ERCOT power trading opportunity**.

- **Congestion on Odehv–Yarbr:** Congestion on the constraint **began in mid-September** and **ramped up in October** (visible in **Constraint Profile** in PowerSignals). **Shift-factor analysis** for the constraint shows the **highest positive shift factor**—and thus the node where prices were most elevated—at the **Permian Basin gas plant** (Constraint Summary in PowerSignals).

- **Trading implication:** A **10 MW point-to-point** position between **Odessa** and **Permian Basin** during the hours when Live Power showed Permian Basin turning off overnight would have netted **close to $60,000** over October (illustrated by **Nodal Spread Profile** in PowerSignals).

- **Conclusion:** **Live Power** provides **60-second** updates from proprietary sensors on generation and transmission; with coverage of key plants and lines, it can surface congestion drivers and **ERCOT power trading opportunities** that delayed ISO data would miss. Demo available for Live Power and ERCOT trading use cases.

Transmission constraints generally: Transmission lines and equipment have thermal (and other) limits. When flow approaches those limits, constraints bind and must be managed. Constraints are central to price formation and nodal analysis; participants need to understand shift factors of nodes on each constraint. GTCs are one type of constraint in ERCOT that drive shift factors and market fundamentals.

What is a GTC in ERCOT? A Generic Transmission Constraint (GTC) is a constraint created by ERCOT that consists of two or more transmission elements (lines or equipment). Unlike a single-line constraint, a GTC applies a limit to the combined flow over that group; the limit is the generic transmission limit. GTCs act like internal interfaces between geographic regions within ERCOT; other ISOs have analogous internal interfaces under different names.

(FTR) Why competitive intelligence matters: Understanding market trends, competitors, and their behavior is key to bidding and risk management. At a macro level, three datasets matter: number of participants, trading volume, and cost (total market investment). Cost (total market investment): Indicates risk appetite. PJM, SPP, ERCOT, and MISO have the largest net dollar investment; pricing more efficient, returns more stable, profits possibly lower. Lower-investment markets offer higher reward but more risk.

Yes Energy tools: FTR Positions Dataset tracks participants, volume, and investment by ISO to spot market shifts; harmonizes auction data at entity and parent level (competitor view, trade by trade); 10+ years of auction data per ISO. PowerSignals adds constraints (position size, profit, how competitors perform and shift over time). Infrastructure Insights (in PowerSignals): generation, large load, and transmission projects (announced, in development, under construction); filter by ISO, activity type, stage; map view; project records with who, what, when, where and forecasted grid impact. Success depends on competition, liquidity, and investment flows plus anticipation of future congestion; Yes Energy provides the data and tools so you can focus on the trading model and execution (e.g. geospatial/grid mapping, simulation, automation). Demo available.

Price trend: Production surge in 2023 drove a sharp decline in prices; Henry Hub cash hit $10/MMBtu in summer 2022 then fell. LNG growth, Mexico exports, and power generation were strong but not enough to sustain prices. US is top LNG exporter; market stays volatile; brief spike >$13 in Jan (winter storms, production issues) then quick drop. Prices down ~60% YoY in the period shown.

Yes Energy + NGI: NGI produces daily natural gas price indexes at 160+ North American locations and forward curves to 10 years at 70 pricing locations. Yes Energy + NGI Daily Gas Index subscribers get that data in Yes Energy products at no extra charge. Reach out for partnership details.

RTC+B went live Dec 5, 2025

---

## Other transmission elements that can be constraints (besides a line)

In market and reliability models, a **constraint** is any **limit on power flow** (or related quantity) that the operator enforces. Besides a **single transmission line**, the following **transmission elements** (or combinations) are commonly modeled as constraints:

- **Transformers** — **Step-up** transformers at plants, **step-down** at substations, and **intertie** transformers between zones or systems have **MVA** or **thermal** limits. When flow through the transformer approaches its rating, it becomes a **binding constraint**; the constraint is often modeled as a **flow limit** (MW or MVA) on that transformer.
- **Interfaces / flowgates** — An **interface** (or **flowgate**) is a **cut-set** or **boundary** across the grid: the **sum of flows** on a set of lines (and sometimes transformers) that together define “flow from region A to region B.” The **limit** is on the **net flow** across that boundary (e.g. “North–South interface” or “import into zone X”). The constraint is not a single line but the **aggregate flow** on multiple elements; binding limits on interfaces drive **congestion** and **nodal price** differences.
- **Generic Transmission Constraints (GTCs)** — As noted earlier, a **GTC** in ERCOT is a constraint made of **two or more transmission elements** (lines, transformers, or other equipment) with a **single combined limit**. So the “element” that is constrained is a **group** of facilities; the limit is the **generic transmission limit** on that group. GTCs act like **internal interfaces** within ERCOT.
- **Stability-related limits** — **Angular stability** (transient or small-signal) or **voltage stability** can imply **maximum flow** on a path or corridor. These are often represented in market and reliability tools as **flow limits** on a **single equivalent branch** or on an **interface** (e.g. “stability limit on corridor X”). So the underlying “element” is a **stability limit**, not just the thermal rating of one line.
- **Substation equipment** — **Bus sections**, **breakers**, **switches**, or **cables** within a substation can have **thermal** or **operational** limits. When power flow through a substation (or through a particular bus section) is limited, that is modeled as a constraint (e.g. flow through a **substation boundary** or **bus section**).
- **Series devices** — **Phase-shifting transformers (PSTs)**, **FACTS** devices (e.g. TCSC, STATCOM used in series), or other **series** components have **through-flow** or **MVA** limits. Flow through the device is constrained; in the network model this appears as a **limit on that branch** or **element**.
- **Corridors and multi-element limits** — A **corridor** (e.g. “West–East tie”) may bundle **several lines and/or transformers** with a **shared** or **combined** limit (e.g. N‑1 or N‑2 secure limit). The constraint is on the **corridor**, not on each line individually.

**Summary:** Besides a **single line**, constraints can be on **transformers**, **interfaces/flowgates** (aggregate flow across a boundary), **GTCs** (groups of elements with one limit), **stability-derived** flow limits, **substation** equipment (bus sections, breakers), **series devices** (PSTs, FACTS), and **corridors** (multi-element limits). In all cases, when the limit is **binding**, it affects **dispatch**, **LMPs**, and **FTR/CRR** value.

