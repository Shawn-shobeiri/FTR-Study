# Supply Stack Modeling in Power Markets

A practical guide from the perspective of a **seasoned power trader**: what **supply stack** (merit order) modeling is, **methods** used, **pros and cons**, **assumptions**, and **formulas**.

---

## 1. What is supply stack modeling?

The **supply stack** (or **merit order**) is the **ranking** of **generation units** by **short-run marginal cost** (SRMC). At any **demand** (load) level, **dispatched** units are those in **merit order** until **total output** equals **load**. The **price** in a **competitive** energy market is set by the **marginal** unit — the **last** unit needed to meet demand — so **price** = **marginal cost** of that unit (in the simplest case).

**Supply stack modeling** is the process of **building** and **using** this **supply curve** (quantity of supply at each price, or price as a function of load) to:

- **Predict** or **explain** **price** (LMP or hub index) given **load** (and optionally **renewables**, **outages**, **fuel**).
- **Stress** price under **high load**, **low renewables**, or **outage** scenarios.
- **Value** generation assets (spark spread, capacity value) or **shape** (HPFC) from **fundamentals**.
- **Support** **trading** (when is power rich/cheap vs the stack?) and **risk** (sensitivity of price to load, gas, outages).

**Single-node view:** Price $P$ clears where **demand** $D$ = **supply** $S(P)$; so $P = S^{-1}(D)$ (inverse supply). **Multi-node:** LMP = **energy** (marginal cost at reference) + **congestion** + **losses**; the **stack** drives the **energy** component and, via **dispatch**, **flows** and **congestion**.

---

## 2. Core idea and clearing condition

**Demand** = load (MW), possibly **net** of **must-run** renewables (i.e. **net load** = load − wind − solar if we treat renewables as **must-take**). **Supply** = sum of **dispatched** generation (MW) from units in **merit order**.

**Clearing (single node):** At **price** $P$, supply $S(P)$ = quantity that would be **dispatched** if price were $P$ (units with SRMC $\le P$ run). **Equilibrium:** $S(P^*) = D$ ⇒ **clearing price** $P^*$. So
$$
P^* = S^{-1}(D) \quad \text{(inverse supply at demand $D$)}.
$$
**Marginal unit:** The unit with SRMC = $P^*$ is the **marginal** unit; **price** equals its **marginal cost** (in a simple energy-only market).

**Assumption (simple case):** **No** **capacity** payments or **out-of-market** actions; **no** **congestion** (single node or we model **energy** component only); **rational** **economic** dispatch (minimize cost). **Reality:** Capacity markets, **unit commitment** (start costs, min run times), **transmission** constraints, and **strategic** behavior complicate this; stack models are **approximations**.

---

## 3. Methods used

### 3.1 Merit order (ordered list of units)

**Idea:** **List** all **dispatchable** units with **capacity** (MW) and **variable cost** ($/MWh). **Sort** by **variable cost** (ascending). **Supply curve** = **cumulative** capacity at each **cost** step: $(Q_0=0, c_1), (Q_1, c_2), \ldots$ where $Q_i$ = cumulative MW up to unit $i$, $c_i$ = SRMC of unit $i$. Given **load** $D$, **find** the **step** where $Q_{k-1} < D \le Q_k$ ⇒ **price** $P^* = c_k$ (marginal unit).

**Variable cost (thermal):** Often approximated as **fuel** cost + **VOM** (variable O&amp;M):
$$
\text{SRMC} \approx \frac{\text{fuel price}}{\text{heat rate}} + \text{VOM}, \quad \text{($/MWh)}.
$$
**Heat rate** = MMBtu/MWh (e.g. 7 for efficient gas CCGT). **Fuel price** in $/MMBtu (e.g. gas). So **spark spread** (power price − gas × heat rate) is the **margin** of a gas unit.

**Formula (clearing):** If supply is **step function** $S(P) = \sum_{i: c_i \le P} q_i$ (where $q_i$ = capacity of unit $i$), then $P^* = \min\{ P : S(P) \ge D \}$ = SRMC of the **marginal** unit.

**Pros:** **Simple**; **transparent**; **no** optimization; **fast**. **Cons:** **Ignores** **unit commitment** (start costs, min up/down); **no** **transmission**; **no** **outages** or **availability**; **single** snapshot (no inter-temporal constraints). **Assumption:** **Economic dispatch** only; **all** units **available**; **no** network.

---

### 3.2 Step supply curve with availability and outages

**Idea:** Same **merit order**, but each unit has **available capacity** = **nameplate** × **availability factor** (or **derate**). **Outages** **remove** capacity from the stack (or shift blocks). **Supply curve** = **cumulative** **available** capacity at each **cost** step. **Net load** = load − **must-take** renewables (wind, solar) so **dispatchable** demand is **net load**.

**Formula:** Same as 3.1 with $q_i$ replaced by **available** $q_i^{\mathrm{avail}}$. **Stress:** **Low** availability (e.g. forced outage) → **fewer** MW at **low** cost → **steeper** stack → **higher** price for same load.

**Pros:** **Captures** **outages** and **renewables** (net load); still **simple**. **Cons:** **Availability** is **exogenous** (not **optimized**); **no** UC; **no** transmission. **Assumption:** **Exogenous** availability; **net load** = load − renewables (renewables **must-take**).

---

### 3.3 Unit commitment and economic dispatch (UC/ED, PCM)

**Idea:** **Full** **optimization**: **Unit commitment** (which units **on/off** each hour, respecting **min up/down**, **start costs**, **ramp** rates) and **economic dispatch** (how much each **committed** unit **outputs**) to **minimize** total **cost** subject to **demand** (and **reserves**) and **transmission** constraints. **Output:** **Hourly** (or sub-hourly) **LMPs**, **dispatch** by unit, **binding** constraints, **shadow** prices. This is **production cost modeling** (PCM), e.g. **PLEXOS**, **Dayzer**, **Promod**, **Aurora**.

**Formula (conceptual):** Minimize $\sum_t \sum_i \bigl( C_i^{\mathrm{var}}(g_{i,t}) + C_i^{\mathrm{start}}(u_{i,t}) \bigr)$ subject to: $\sum_i g_{i,t} = D_t$ (balance); $u_{i,t} \in \{0,1\}$ (on/off); min/max **output**; **min up/down**; **ramp**; **transmission** (flow limits); **reserves**. **LMP** = **dual** (shadow price) of the **balance** constraint (and **nodal** LMP = balance + congestion + losses from **dual** of **flow** constraints).

**Pros:** **Physically** **realistic**; **captures** **UC** (start costs, ramps), **transmission**, **multi-node** LMPs, **congestion**. **Cons:** **Data-intensive** (unit data, topology, load, renewables); **slow** (large MILP); **calibration** (heat rates, costs, availability); **model** risk. **Assumption:** **Accurate** input data; **rational** cost minimization; **correct** topology and constraints.

---

### 3.4 Reduced-form (price as function of load)

**Idea:** **Bypass** explicit stack; **model** **price** (or **log** price) as a **function** of **load** (and optionally **renewables**, **fuel**): $P = f(D, W, G)$ where $W$ = wind/solar, $G$ = gas price. **Estimate** $f$ from **historical** data (e.g. **regression**, **spline**). **Convex** in $D$ (higher load → higher price); often **non-linear** (price **spikes** when load is near capacity).

**Formula (example):** **Polynomial** $P = \beta_0 + \beta_1 D + \beta_2 D^2 + \beta_3 W + \beta_4 G$; or **exponential** $P = a \exp(b \cdot D/C)$ near **capacity** $C$ (price **explodes** as $D \to C$). **Calibrate** $\beta$ or $(a,b)$ from **historical** $(P, D, W, G)$.

**Pros:** **Fast**; **no** unit-level data; **easy** to **stress** (plug in $D$, $W$, $G$). **Cons:** **Reduced form** — **no** **structural** link to **outages** or **new** units; **extrapolation** (e.g. $D$ above historical max) **unreliable**; **regime** change (new capacity) **breaks** fit. **Assumption:** **Stable** **relationship** $P = f(D, W, G)$; **history** is **representative**.

---

### 3.5 Regression (price on load, renewables, fuel)

**Idea:** **Linear** or **non-linear** **regression** of **price** (or **log** price) on **load**, **wind**, **solar**, **gas** price, **season** dummies, **hour** dummies: $P_t = \mathbf{x}_t^\top \boldsymbol{\beta} + \varepsilon_t$. **Forecast** price = $\mathbf{x}_{\mathrm{forecast}}^\top \widehat{\boldsymbol{\beta}}$. **Interpretation:** $\partial P / \partial D$ ≈ **marginal** effect of load (like **slope** of supply curve in reduced form).

**Formula:** $\widehat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top \mathbf{P}$ (OLS). **Heteroskedasticity:** Use **WLS** or **robust** SEs; **quantile** regression for **tail** (e.g. 95th percentile price).

**Pros:** **Simple**; **uses** **observable** drivers; **interpretable**; **fast** forecast. **Cons:** **Linear** (or **additive**) may **miss** **convexity** (stack effect); **omitted** variables (outages, transmission); **no** **structural** link to **stack**. **Assumption:** **Linear** (or specified non-linear) **conditional** expectation; **stationary** relationship.

---

### 3.6 Hybrid (stack + regression or stack + PCM)

**Idea:** Use **physical** **stack** (merit order or UC/ED) for **structure** and **scenario** (outages, new units); **calibrate** or **adjust** with **historical** **residual** (e.g. **regression** of **realized** price on **stack-implied** price to correct **level** or **bias**). Or use **PCM** for **hourly** **shape** and **scale** to **market** **block** prices (as in **fundamental** shaping).

**Pros:** **Combines** **structure** (stack) and **fit** (data). **Cons:** **More** **complex**; **two** models to **maintain**. **Assumption:** **Stack** gives **shape** or **relative** move; **regression** or **scaling** corrects **level**.

---

## 4. Formulas (reference)

**Short-run marginal cost (thermal):**
$$
\text{SRMC} \approx \frac{P_{\mathrm{fuel}}}{\mathrm{HR}} + \text{VOM}, \quad \text{($/MWh)},
$$
where $P_{\mathrm{fuel}}$ = fuel price ($/MMBtu), $\mathrm{HR}$ = heat rate (MMBtu/MWh), VOM = variable O&amp;M ($/MWh).

**Spark spread (gas unit margin):**
$$
\text{Spark spread} = P_{\mathrm{power}} - \mathrm{HR} \times P_{\mathrm{gas}} \quad \text{($/MWh)}.
$$
Unit **in the money** when spark spread > 0 (ignoring start and no-load costs).

**Clearing (step supply):** Demand $D$; supply steps $(Q_0=0, c_1), (Q_1, c_2), \ldots, (Q_{n-1}, c_n)$. $P^* = c_k$ where $k = \min\{ j : Q_j \ge D \}$.

**Net load:**
$$
D_{\mathrm{net}} = D_{\mathrm{load}} - G_{\mathrm{wind}} - G_{\mathrm{solar}} \quad \text{(MW)}.
$$
**Dispatchable** demand = net load (if wind/solar are **must-take**).

**Reduced-form (example):** $P = \beta_0 + \beta_1 D_{\mathrm{net}} + \beta_2 G_{\mathrm{gas}} + \varepsilon$; or $\ln P = \beta_0 + \beta_1 D_{\mathrm{net}} + \cdots$ for **multiplicative** effect.

**Residual demand (for one resource):** If **wind** is **must-take**, **residual** demand for **thermal** = $D_{\mathrm{load}} - G_{\mathrm{wind}} - G_{\mathrm{solar}}$. **Price** is set by **thermal** stack at **residual** demand.

---

## 5. Pros and cons (summary table)

| Method | Pros | Cons |
|--------|------|------|
| **Merit order (simple)** | Simple; transparent; fast; no UC/network. | No UC, transmission, outages; single snapshot. |
| **Step + availability / net load** | Captures outages, renewables (net load); still simple. | Availability exogenous; no UC, no transmission. |
| **UC/ED (PCM)** | Physically realistic; UC, transmission, LMPs, congestion. | Data-intensive; slow; calibration; model risk. |
| **Reduced-form** $P = f(D,W,G)$ | Fast; no unit data; easy stress. | No structure; extrapolation risky; regime change. |
| **Regression** | Simple; observable drivers; interpretable. | Linear/additive; no stack structure; omitted vars. |
| **Hybrid** | Structure + fit. | More complex; two systems. |

---

## 6. Assumptions (summary)

| Area | Typical assumption | Caveat |
|------|---------------------|--------|
| **Dispatch** | **Economic** dispatch (minimize cost); **rational** participants. | **Strategic** bidding; **out-of-market** actions; **capacity** payments. |
| **Single node** | **Price** = inverse supply at demand (no congestion). | **Multi-node**: LMP = energy + congestion + losses; **stack** gives **energy** component. |
| **Availability** | **Exogenous** (e.g. from outage data) or **100%**. | **Endogenous** (maintenance, forced) and **uncertain**. |
| **Renewables** | **Must-take** (net load = load − wind − solar) or **curtailed** by model. | **Curtailment** and **negative** prices when **renewables** > load. |
| **Fuel and heat rates** | **Known** **fuel** price and **heat rate** per unit. | **Fuel** **volatile**; **heat rate** **varies** with output (e.g. derating). |
| **Unit commitment** | **Ignored** (merit order) or **full** UC in PCM. | **Start** costs and **min up/down** **shift** **dispatch** and **price**. |
| **Transmission** | **Ignored** (single node) or **full** DC (or AC) in PCM. | **Congestion** and **losses** **split** **nodal** prices. |
| **Stability** | **Relationship** (stack or reduced form) **stable** over time. | **Retirements**, **new** capacity, **demand** change → **structural** break. |

---

## 7. Use cases (trader view)

- **Quick** **price** **sense**: **Merit order** or **step** stack with **today’s** gas and **forecast** load/net load → **rough** **price** (e.g. peak hour).
- **Stress**: **High** load, **low** renewables, **outage** of **marginal** unit → **stack** or **PCM** gives **stress** **price**.
- **Spark** **spread**: **Stack** tells us **which** unit is **marginal** → **implied** **power** price from **gas** and **heat rate**; **spark** **spread** = power − HR × gas.
- **HPFC** **shape**: **PCM** (or **stack** by hour with **load** and **renewable** profile) → **hourly** **price** **shape**; **scale** to **market** **block** for **fundamental** shaping.
- **FTR / congestion**: **PCM** gives **shadow** **prices** and **binding** **constraints** → **path** **value** and **basis** (node − hub).

---

## 8. One-page recap

- **Supply stack** = **merit order** (units ranked by **SRMC**). **Price** (single node) = **inverse** **supply** at **demand** (marginal unit’s cost). **Supply stack modeling** = building/using this to **predict** price, **stress**, **value** assets, **support** trading.
- **Methods:** **Merit order** (simple list, clear at $D$); **step** + **availability** / **net load** (outages, renewables); **UC/ED** (PCM: full UC, transmission, LMPs); **reduced-form** $P = f(D,W,G)$; **regression** of price on load, renewables, fuel; **hybrid** (stack + regression or PCM + scaling).
- **Formulas:** SRMC ≈ fuel/HR + VOM; **spark** spread = power − HR × gas; **clearing** $P^* = c_k$ where $Q_{k-1} < D \le Q_k$; **net** load = load − wind − solar.
- **Pros/cons:** Merit order = simple/fast but no UC/network; **PCM** = realistic but heavy; **reduced-form** = fast but no structure; **regression** = simple but linear/no stack.
- **Assumptions:** Economic dispatch, single node (or energy component), exogenous availability, must-take renewables (or net load), stable relationship. **Caveats:** Strategic behavior, congestion, UC, transmission, structural change.
- **Trader use:** Quick price, **stress** (high load, low renewables, outage), **spark** spread, **HPFC** shape (PCM), **FTR**/congestion (PCM shadows).
