# Solar and BESS: Revenue Sources, Risk Factors, Portfolio Management, and Risk Metrics

A practical guide from the perspective of a seasoned quant at a **solar and BESS** company: **sources of revenue** for solar and BESS, **risk factors** for each, **portfolio management**, **methods to calculate risk** (and their risk factors), with **pros**, **cons**, **assumptions**, and **formulas**.

---

## 1. Sources of revenue

### 1.1 Solar

| Source | Description | Formula (conceptual) |
|--------|-------------|------------------------|
| **Energy (merchant / spot)** | Sell **energy** (MWh) at **market** price (LMP or hub index). Revenue = volume × price per interval, summed. | $R_{\mathrm{energy}} = \sum_t P_t \cdot G_t \cdot \Delta t$, where $P_t$ = price ($/MWh), $G_t$ = generation (MW), $\Delta t$ = interval length (e.g. 1 h). |
| **Energy (PPA / contract)** | **Fixed** or **indexed** price per MWh over a **term**. Revenue = contracted volume × contract price (or index + spread). | $R_{\mathrm{PPA}} = \sum_t \min(G_t \Delta t, Q_t) \cdot K_t$, where $K_t$ = contract price (or index + spread), $Q_t$ = contract cap if any. |
| **RECs / environmental** | **Renewable Energy Certificates** (or green attributes) sold separately from energy. Revenue = REC volume × REC price. | $R_{\mathrm{REC}} = (\text{MWh sold}) \times P_{\mathrm{REC}}$. |
| **Capacity** | **Capacity** payments (e.g. capacity market) for **qualified** capacity (MW) available in a future period. Revenue = capacity (MW) × capacity price ($/MW-day or $/MW-month). | $R_{\mathrm{cap}} = C_{\mathrm{qual}} \times \pi_{\mathrm{cap}} \times (\text{days or months})$. |
| **Incentives (ITC, PTC)** | **Investment** tax credit (ITC) or **production** tax credit (PTC). One-time (ITC) or per MWh (PTC). | PTC: $R_{\mathrm{PTC}} = \sum_t G_t \Delta t \times \tau_{\mathrm{PTC}}$ (e.g. $\$/MWh$ credit). |

**Assumptions (typical):** Generation $G_t$ from **irradiance** and **plant** model (capacity, degradation, availability); **price** $P_t$ from **curve** or **HPFC**; **curtailment** (e.g. when $P_t < 0$ or grid constraint) reduces **volume**. **PPA**: **basis** risk if settlement is at different node/index than contract.

---

### 1.2 BESS (Battery Energy Storage System)

| Source | Description | Formula (conceptual) |
|--------|-------------|------------------------|
| **Energy arbitrage** | **Charge** when price is **low**, **discharge** when price is **high**. Revenue = (discharge revenue − charge cost) net of **round-trip loss**. | $R_{\mathrm{arb}} = \sum_t \bigl( P_t^{\mathrm{disch}} \cdot D_t \cdot \eta_{\mathrm{disch}} - P_t^{\mathrm{ch}} \cdot C_t / \eta_{\mathrm{ch}} \bigr) \Delta t$, or simplified: $R \approx \sum_{\mathrm{cycles}} (P_{\mathrm{high}} - P_{\mathrm{low}}/\eta_{\mathrm{rt}}) \cdot E$, with $\eta_{\mathrm{rt}} = \eta_{\mathrm{ch}}\eta_{\mathrm{disch}}$. |
| **Ancillary services (regulation)** | **Frequency regulation** (respond to AGC signal): payment per **MW** (capacity) and sometimes **performance** (MWh delivered). | $R_{\mathrm{reg}} = C_{\mathrm{reg}} \times \pi_{\mathrm{reg}} \times (\text{period}) + \text{performance component}$. |
| **Ancillary services (reserves)** | **Spinning** or **non-spinning** reserves: **capacity** (MW) held available; **energy** if called. | $R_{\mathrm{res}} = C_{\mathrm{res}} \times \pi_{\mathrm{res}} + \sum_{\mathrm{called}} (P_{\mathrm{energy}} - P_{\mathrm{opportunity}}) \cdot E_{\mathrm{delivered}}$. |
| **Capacity** | **Capacity** market payments for **qualified** capacity (MW) that can discharge when needed. | $R_{\mathrm{cap}} = C_{\mathrm{qual}} \times \pi_{\mathrm{cap}} \times (\text{period})$. |
| **Congestion / curtailment** | **Reduce** congestion or **absorb** curtailment (e.g. charge when renewables are curtailed, discharge later). Value = avoided cost or contract. | Site- and market-specific. |
| **Behind-the-meter (BTM)** | **Demand charge reduction**, **backup**, **time-of-use** arbitrage for a host. Revenue = contract or savings share. | $R_{\mathrm{BTM}} = f(\text{demand savings}, \text{energy savings}, \text{contract})$. |

**Assumptions (typical):** **Round-trip efficiency** $\eta_{\mathrm{rt}}$ (e.g. 85–90%); **power** and **energy** limits (MW, MWh); **degradation** (capacity fade over cycles/time); **cycling** and **SoC** constraints. **Arbitrage** value depends on **spread** (high − low price) and **shape** of prices; **ancillary** value on **market** clearing prices and **performance** rules.

---

### 1.3 Co-located solar + BESS

**Hybrid** plant: solar **and** battery at same **point of interconnection**. Revenue = solar revenue + BESS revenue, with **interaction**:

- **Charging** battery from **solar** (when price low or curtailment) and **discharging** when price high → **arbitrage** and **curtailment** reduction.
- **Firming / shaping:** Battery **smooths** or **shifts** solar output → better **PPA** value or **capacity** qualification.
- **Ancillary:** Battery can provide **regulation** or **reserves** while solar runs; **ramp** support.

**Revenue** can be **greater** than sum of standalone solar + standalone BESS due to **synergies** (e.g. shared interconnection, combined offer in markets). **Modeling:** joint **dispatch** optimization (maximize revenue subject to solar output, battery constraints, market rules).

---

## 2. Risk factors: Solar

| Risk factor | Description | Impact on revenue / value |
|-------------|-------------|----------------------------|
| **Power price** $P_t$ | **Level** and **path** of LMP (or hub index). | **Merchant** revenue = volume × price; **PPA** basis if index ≠ settlement. **Delta** to price. |
| **Price shape** | **Hourly** (or sub-hourly) **profile** of prices. | Solar generates in **daylight**; revenue depends on **price during sun hours**. **Shape** risk: prices **low** when solar is **high** (duck curve). |
| **Basis (node − hub)** | Difference between **nodal** LMP and **hub** (or PPA index). | **Location** risk; **curtailment** or **congestion** at node. |
| **Irradiance / weather** | **Solar** resource (GHI, DNI, or POA); **cloud**, **soiling**, **temperature**. | **Generation** $G_t$; **low** irradiance → **low** volume → **low** revenue. **Volatility** of **resource**. |
| **Curtailment** | **Grid** or **market** instruction to **reduce** output (e.g. congestion, oversupply). | **Volume** risk; **revenue** loss when curtailed. |
| **Availability** | **Forced** or **planned** outage; **inverter** or **tracker** failure. | **Capacity** factor and **volume**; **capacity** payment qualification. |
| **REC price** | Price of **RECs** (or green attributes). | **REC** revenue; **merchant** REC exposure. |
| **Contract (PPA) terms** | **Strike** (price), **volume** (cap), **index**, **curtailment** allocation. | **Basis**, **volume**, and **price** risk under contract. |

---

## 3. Risk factors: BESS

| Risk factor | Description | Impact on revenue / value |
|-------------|-------------|----------------------------|
| **Price spread** (arbitrage) | **Difference** between **high** and **low** prices within a **cycle** (e.g. day). | **Arbitrage** revenue ≈ spread × throughput × (efficiency factor). **Delta** to **spread**. |
| **Price shape** | **Timing** of **high** and **low** prices (e.g. peak vs overnight). | **Optimal** charge/discharge **timing**; **wrong** shape → **lower** arbitrage. |
| **Ancillary service prices** | **Regulation** ($/MW), **reserves** ($/MW), **performance** ($/MWh). | **Ancillary** revenue; **volatility** and **clearing** risk. |
| **Capacity price** | **Capacity** market clearing price ($/MW-day or $/MW-month). | **Capacity** revenue; **qualification** (availability, duration). |
| **Efficiency** $\eta_{\mathrm{rt}}$ | **Round-trip** efficiency (charge → discharge). | **Arbitrage** margin; **degradation** can **reduce** $\eta$ over time. |
| **Degradation** | **Capacity fade** and **resistance** increase over **cycles** and **time**. | **Throughput** and **capacity** decline; **replacement** cost; **lifetime** value. |
| **Availability** | **Forced** or **planned** outage; **BMS** or **inverter** failure. | **Volume** and **capacity** qualification. |
| **Market rules** | **Eligibility**, **performance** scoring, **duration** requirements. | **Ancillary** and **capacity** revenue; **regulatory** risk. |

---

## 4. Portfolio management: Solar and BESS

### 4.1 Objectives

- **Maximize** **risk-adjusted** return (e.g. revenue or NPV subject to **risk** limits).
- **Hedge** **price**, **basis**, and **volume** risk via **contracts** (PPA, swaps, options) or **operational** diversification.
- **Allocate** **capital** and **capacity** across **sites**, **markets**, and **revenue streams** (energy vs ancillary vs capacity).
- **Monitor** **limits** (VaR, exposure, concentration) and **stress** (price crash, low spread, low solar).

### 4.2 Levers

| Lever | What | How |
|-------|------|-----|
| **Contracting (PPA, hedge)** | **Fix** price (or cap/floor) for **part** of volume. | **Reduce** **merchant** price risk; **basis** risk remains if index ≠ node. **Trade-off**: give up **upside** for **certainty**. |
| **Dispatch / offer strategy** | **When** to **charge/discharge** (BESS) or **curtail** (solar). | **Optimize** against **HPFC** or **forecast**; **ancillary** vs **energy** trade-off. **Real-time** and **day-ahead** offers. |
| **Diversification** | **Sites** (nodes, regions), **markets** (ERCOT, CAISO, etc.), **revenue** mix (energy, reg, reserves, capacity). | **Lower** **idiosyncratic** risk (e.g. single-node congestion); **correlation** across sites/markets matters. |
| **Co-location (solar + BESS)** | **Hybrid** at same node. | **Synergy** (curtailment reduction, firming); **single** interconnection; **joint** optimization. |
| **Limits and reserves** | **VaR**, **concentration** (max % in one node/market), **min** liquidity or **hedge** ratio. | **Risk** governance; **capital** allocation. |

### 4.3 Revenue and value (formulas)

**Solar (merchant) revenue over period $\mathcal{T}$:**
$$
R_{\mathrm{solar}} = \sum_{t \in \mathcal{T}} P_t \cdot G_t \cdot \Delta t \cdot (1 - \gamma_t),
$$
where $\gamma_t$ = curtailment fraction at $t$, $G_t$ = available generation (MW). **Expected** revenue uses **HPFC** $F_{0,t}$ and **expected** generation $\mathbb{E}[G_t]$ (from irradiance model).

**BESS arbitrage (simplified, one cycle):** If charge at price $P_{\mathrm{low}}$, discharge at $P_{\mathrm{high}}$, energy $E$ (MWh), round-trip efficiency $\eta_{\mathrm{rt}}$:
$$
R_{\mathrm{arb}} = E \cdot \Bigl( P_{\mathrm{high}} \cdot \eta_{\mathrm{rt}} - \frac{P_{\mathrm{low}}}{\eta_{\mathrm{rt}}} \Bigr) \quad \text{(simplified; actual has many cycles and constraints).}
$$
**Multi-period** arbitrage value = **optimal** dispatch value (dynamic program or **LSM**) over **price paths** and **SoC** constraints.

**Portfolio value:** $V = V_{\mathrm{solar}} + V_{\mathrm{BESS}} + V_{\mathrm{hybrid}} + \cdots$ (sum of asset values). **MtM** = expected **discounted** cash flows under **current** curves and **operating** strategy.

---

## 5. Methods to calculate risk: Risk factors and formulas

### 5.1 Risk factors (summary)

| Risk factor | Solar | BESS | Portfolio |
|-------------|--------|------|-----------|
| **Power price** $P_t$ (level) | ✓ (energy revenue) | ✓ (arbitrage, opportunity cost) | ✓ |
| **Price shape** (hourly profile) | ✓ (solar profile vs price) | ✓ (spread timing) | ✓ |
| **Price spread** (high − low) | — | ✓ (arbitrage) | ✓ |
| **Basis (node − hub)** | ✓ | ✓ (if nodal) | ✓ |
| **Ancillary prices** (reg, reserves) | — | ✓ | ✓ |
| **Capacity price** | ✓ (if qualified) | ✓ | ✓ |
| **Irradiance / generation** $G_t$ | ✓ (volume) | — | ✓ |
| **Efficiency / degradation** | — | ✓ | ✓ |
| **Curtailment** | ✓ | — | ✓ |

### 5.2 VaR (Value at Risk)

**Definition:** VaR at confidence $\alpha$ = $(1-\alpha)$-quantile of **loss** (or minus P&amp;L) over horizon (e.g. 1-day, 1-month).

**Loss:** $L = -\Delta V$, where $\Delta V$ = change in **portfolio value** (e.g. change in **expected** revenue or **NPV**).

**Methods:**

| Method | Idea | Risk factors | Pros | Cons |
|--------|------|--------------|------|------|
| **Historical** | Apply **historical** $\Delta$ (price, spread, irradiance) to **current** portfolio; empirical quantile of P&amp;L. | Price, spread, ancillary, irradiance (if available). | No distributional assumption; uses history. | Backward-looking; no worse-than-history. |
| **Parametric (delta-normal)** | **Delta** of value to risk factors; assume **factor** returns **normal**. VaR = $\Phi^{-1}(1-\alpha) \cdot \sigma_L$. | Same; **covariance** of factors. | Fast; analytical. | **Non-linearity** (spread, options) understated; **fat tails**. |
| **Monte Carlo** | **Simulate** **paths** of risk factors (price, spread, ancillary, irradiance); **revalue** portfolio (or **dispatch** model); empirical quantile of **loss**. | Full **joint** distribution. | **Non-linear**; **path-dependent** (BESS); **flexible**. | **Cost**; **model** risk. |

**Assumptions:** **Mapping** from risk factors to **value** (revenue or NPV) is **correct**; **distribution** of factors is **stationary** or **calibrated**; **no** **liquidity** or **funding** risk in horizon (or adjust).

**Formula (parametric, single factor):** If $\Delta V \approx \delta \cdot \Delta P$ (delta to price $P$), then $\sigma_L = |\delta| \sigma_{\Delta P}$ and $\mathrm{VaR}_\alpha = \Phi^{-1}(1-\alpha) \cdot \sigma_L$ (assuming zero mean $\Delta P$).

---

### 5.3 Sensitivity (delta, scenario)

**Delta:** $\frac{\partial V}{\partial P}$ = **$ change in value per $1/MWh** change in price (or per unit of spread, ancillary price). **Scenario:** Revalue at **shocked** price (e.g. −$20/MWh), **shocked** spread (−$5), **low** solar (e.g. 80% of expected). **Stress:** **Extreme** scenario (e.g. price spike to $500, or price crash to −$50).

**Pros:** **Interpretable**; **fast**; **communication** with trading/management. **Cons:** **Local** (non-linearity); **no** probability attached to scenario.

---

### 5.4 Expected Shortfall (ES) and tail risk

**ES** = $\mathbb{E}[L \mid L \ge \mathrm{VaR}_\alpha]$ = **average loss** given loss **exceeds** VaR. **Use:** **Tail** risk; **coherent**; often required for **capital**. **Computation:** From **same** simulation or historical P&amp;L as VaR; average the **worst** $(1-\alpha)$ fraction of losses.

---

### 5.5 Assumptions and issues

| Assumption | When it fails | Mitigation |
|------------|----------------|------------|
| **Linear (delta)** | **BESS** value is **non-linear** in **spread** (option-like); **solar** with **PPA** floor/cap. | **Full revaluation** (MC); **delta–gamma** if tractable. |
| **Stationary factors** | **Regime** change (new market rules, demand shift); **structural** break. | **Stress** tests; **update** model; **conservative** VaR. |
| **Correct dispatch** | **Optimal** dispatch **assumed** in valuation; **real** dispatch may differ. | **Operational** model alignment; **backtest** realized vs assumed. |
| **No liquidity** | **Cannot** exit or **hedge** at mark in stress. | **Liquidity** adjustment; **holding period**; **stress** with **wider** bid–ask. |

---

## 6. Formulas (reference)

**Solar energy revenue (merchant):**
$$
R_{\mathrm{solar}} = \sum_t P_t \cdot G_t \cdot (1 - \gamma_t) \cdot \Delta t.
$$

**BESS arbitrage (single cycle, simplified):**
$$
R_{\mathrm{arb}} = E \cdot \Bigl( \eta_{\mathrm{disch}} P_{\mathrm{disch}} - \frac{P_{\mathrm{ch}}}{\eta_{\mathrm{ch}}} \Bigr), \qquad \eta_{\mathrm{rt}} = \eta_{\mathrm{ch}} \cdot \eta_{\mathrm{disch}}.
$$

**Portfolio P&amp;L (change in value):** $\Delta V \approx \sum_i \frac{\partial V}{\partial r_i} \Delta r_i$ (delta approximation), where $r_i$ = risk factor (price, spread, ancillary, etc.).

**VaR (parametric, zero mean):** $\mathrm{VaR}_\alpha = \Phi^{-1}(1-\alpha) \cdot \sigma_L$, with $\sigma_L^2 = \boldsymbol{\delta}^\top \boldsymbol{\Sigma} \boldsymbol{\delta}$ if $\Delta V = \boldsymbol{\delta}^\top \Delta\mathbf{r}$ and $\mathrm{Var}(\Delta\mathbf{r}) = \boldsymbol{\Sigma}$.

**Expected Shortfall:** $\mathrm{ES}_\alpha = \mathbb{E}[L \mid L \ge \mathrm{VaR}_\alpha]$.

---

## 7. Pros and cons: Revenue sources and risk methods

### 7.1 Revenue sources (summary)

| Source | Pros | Cons |
|--------|------|------|
| **Solar: Merchant** | **Upside** when price high; **no** long-term contract lock-in. | **Price** and **shape** risk; **curtailment**; **basis**. |
| **Solar: PPA** | **Stable** revenue; **financing**; **reduces** price risk. | **Basis** (index vs node); **volume** cap; **give up** upside. |
| **Solar: RECs** | **Additional** revenue stream; **decoupled** from energy. | **REC** price **volatility**; **policy** risk. |
| **BESS: Arbitrage** | **Spread** capture; **optionality** on **price path**. | **Spread** **volatility**; **efficiency** and **degradation**; **competition** (more BESS → lower spread). |
| **BESS: Ancillary** | **Stable** capacity payment; **complements** energy. | **Market** rule risk; **performance** risk; **clearing** price **volatility**. |
| **BESS: Capacity** | **Predictable** if qualified. | **Qualification** (availability, duration); **price** risk. |

### 7.2 Risk methods (summary)

| Method | Pros | Cons |
|--------|------|------|
| **VaR (historical)** | No distribution; uses history. | Backward-looking; no tail beyond sample. |
| **VaR (parametric)** | Fast; analytical. | Linear; understates non-linearity and tails. |
| **VaR (MC)** | Non-linear; path-dependent; flexible. | Cost; model risk. |
| **Sensitivity / scenario** | Simple; interpretable. | Local; no probability. |
| **ES** | Coherent; tail. | Needs same data as VaR; heavier tail. |

---

## 8. One-page recap

- **Solar revenue:** **Energy** (merchant or PPA), **RECs**, **capacity**, **incentives** (ITC/PTC). **Risk factors:** **Price**, **shape**, **basis**, **irradiance**, **curtailment**, **availability**, **REC** price.
- **BESS revenue:** **Energy arbitrage** (charge low, discharge high), **ancillary** (regulation, reserves), **capacity**, **congestion/curtailment**, **BTM**. **Risk factors:** **Spread**, **shape**, **ancillary** prices, **capacity** price, **efficiency**, **degradation**, **availability**.
- **Co-located solar + BESS:** **Synergies** (curtailment reduction, firming); **joint** dispatch; **portfolio** value can exceed sum of parts.
- **Portfolio management:** **Contracting** (PPA, hedges), **dispatch/offer** optimization, **diversification** (sites, markets, revenue mix), **limits** (VaR, concentration). **Formulas:** Solar $R = \sum P_t G_t (1-\gamma_t) \Delta t$; BESS arbitrage $R \approx E (P_{\mathrm{high}}\eta_{\mathrm{rt}} - P_{\mathrm{low}}/\eta_{\mathrm{rt}})$; portfolio $\Delta V \approx \boldsymbol{\delta}^\top \Delta\mathbf{r}$.
- **Risk calculation:** **VaR** (historical, parametric, MC) with **risk factors** = price, spread, ancillary, basis, irradiance, efficiency. **Sensitivity** (delta, scenario, stress); **ES** for tail. **Assumptions:** Mapping value ↔ factors; stationarity; dispatch as modeled. **Issues:** Non-linearity (BESS), regime change, liquidity.
- **Pros/cons:** Merchant = upside vs risk; PPA = stability vs basis/give-up; arbitrage = optionality vs spread competition; ancillary = stable vs rules. VaR historical = robust vs backward-looking; parametric = fast vs thin tails; MC = flexible vs cost.
