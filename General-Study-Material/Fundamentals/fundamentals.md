# Market Fundamentals and Main Risk Factors: FTR, Power, and Gas

A practical guide from the perspective of a seasoned quant: what **market fundamentals** are, how they drive prices and value, and what the **main risk factors** are for **FTR**, **power**, and **gas** — for valuation, risk (VaR, stress), and trading.

---

## 1. What are market fundamentals?

**Market fundamentals** are the **physical and economic** inputs that determine **supply**, **demand**, and **clearing** in a commodity market. They are the **drivers** behind observed prices and congestion. In energy we typically track:

- **Demand / load:** How much energy (power in MW, gas in MMBtu or Bcf) is consumed — by hour, day, season, and location. Driven by **weather** (temperature, humidity), **economic activity**, **day type** (weekday vs weekend), and **behavior** (EV charging, HVAC).
- **Supply / generation (power):** Which plants run, at what cost (fuel, heat rate), and **availability** (outages, derates). **Renewables** (wind, solar) are **variable** and **weather-dependent**.
- **Supply (gas):** **Production** (dry gas, associated gas), **imports** (pipelines, LNG), **storage** (inject/withdraw). **Pipeline capacity** and **operational** constraints limit flow.
- **Transmission (power):** **Network topology** (which lines and transformers are in service), **flow limits** (thermal, stability), **outages**. Constraints **bind** when flow hits a limit → **congestion** and **LMP** differences across nodes.
- **Storage (gas, and limited power):** **Inventory** levels, **inject/withdraw** rates, **seasonal** pattern (refill in summer, draw in winter). Affects **prompt vs deferred** spread and **volatility**.
- **Weather:** **Temperature** (heating and cooling demand; gas demand; wind/solar output), **wind speed**, **irradiance**, **precipitation** (hydro). Often the **primary** short-term driver of load and renewables.
- **Fuel prices:** **Gas** price (and oil, coal where relevant) drives **marginal cost** of thermal generation → **power** price and **spark spread**. **Power–gas** link is central in many markets.

**Why they matter:** **Valuation** (curves, fair value, HPFC) and **risk** (VaR, stress, scenario analysis) depend on **how** fundamentals evolve. We use fundamentals to **explain** price moves, **forecast** prices or congestion, and **stress** the book (e.g. heat wave, outage, freeze).

---

## 2. FTR: Fundamentals and main risk factors

### 2.1 Market fundamentals (FTR)

FTR payoff is **path spread** (sink − source price) over the CRR period. That spread is **congestion**: it appears when **transmission constraints** bind. So FTR fundamentals are whatever drives **which constraints bind** and **how much** they are worth (shadow price).

| Fundamental | How it affects FTR |
|-------------|---------------------|
| **Load (demand)** | **Higher load** → more flow on many paths → more constraints **binding**; **location** of load (load pockets) vs generation drives **direction** of congestion. **Peak** hours and **summer/winter** peaks increase binding frequency and shadow magnitude. |
| **Generation stack and dispatch** | **Marginal** unit and **cost** at each node; **outages** (gen or transmission) **shift** flows and can **create or relieve** congestion. **Renewables** (wind, solar) change **net load** and **flow patterns** (e.g. west-to-east when wind is strong). |
| **Transmission topology and outages** | **Line/transformer outages** change **PTDFs** and **LODFs**; flow is **re-routed** → some constraints get **tighter**, others **looser**. **Planned** outages (maintenance) and **forced** outages drive **scenario** analysis and **binding** probability. |
| **Renewables (wind, solar)** | **High** renewable output often **lowers** net load and can **reduce** congestion in some hours; **low** wind/solar → more thermal dispatch and **different** flow patterns. **Location** of renewables vs load matters (e.g. West Texas wind vs South load). |
| **Weather** | **Temperature** → load (cooling/heating); **wind speed** and **irradiance** → wind and solar output. **Extreme** heat or cold → **spikes** in load and sometimes **congestion** and **shadow** spikes. |
| **Fuel (gas) price** | Affects **level** of **energy** component of LMP and **marginal** cost; **congestion component** (shadow prices) is determined by **binding** constraints, but **overall** LMP level (and thus path spread **level**) can move with gas. |

**Link to path value:** Path spread = $\sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}$. So **fundamentals** affect **which** $\ell$ bind ($\mu_\ell > 0$) and **how large** $\mu_\ell$ is. **Outages** and **load** are usually the **first-order** drivers of **binding** and **shadow** level.

### 2.2 Main risk factors (FTR)

**Risk factors** are the **variables** we use for **MtM**, **VaR**, and **stress**: their **distribution** and **correlation** drive P&amp;L and risk.

| Risk factor | Description | Why it matters |
|-------------|-------------|----------------|
| **Path spread** | Sink price − source price (per interval or average over period). | **Direct** driver of FTR payoff; **zero** when constraints don’t bind, **non-zero** (positive or negative) when they do. **VaR** and **MtM** use path-spread distribution (or constraint shadows × PTDF). |
| **Constraint shadow price** $\mu_\ell$ | $/MWh (or $/MW) on constraint $\ell$ when binding; 0 when not binding. | **Decomposition** of path spread; **portfolio** VaR via **PTDF** mapping: $\Delta V \approx \sum_p Q_p \sum_\ell \mathrm{PTDF}_{\ell,p} \Delta\mu_\ell \cdot (\text{remaining h})$. **Correlation** across constraints drives **portfolio** risk. |
| **Binding frequency** | Probability (or count) that a constraint binds over the CRR period. | Drives **expected** path value (zero-inflation); **option** FTR value = binding prob × expected payoff when binding. |
| **Topology / PTDF / LODF** | Which lines are in service; **PTDF** and **LODF** depend on topology. | **Outage** → topology change → **PTDF** and **shadow** distribution change. **Model risk**: wrong PTDF or stale topology **misstates** path exposure and VaR. |
| **Forward power (hub) price** | Level of energy at hub or zone. | Path spread can be **approximated** by **hub spread** (sink hub − source hub) when congestion is **small**; **curve** move affects **implied** congestion view and **MtM**. |
| **Time to settlement** | Remaining intervals (MW·h) in the CRR period. | **Variance** of path spread often **decreases** as we approach settlement; **VaR** and **MtM** use **remaining** tenor. |

**Summary:** FTR risk is **path-spread risk** (or **constraint-shadow** risk via PTDF). Fundamentals (**load**, **outages**, **renewables**, **weather**) drive **when** and **how much**; **topology** and **PTDF** map constraints to path value.

---

## 3. Power: Fundamentals and main risk factors

### 3.1 Market fundamentals (power)

Power price (LMP or hub index) is set by **supply–demand balance** at each **node** (or zone) and **congestion** between nodes. Fundamentals determine **level**, **volatility**, and **shape** (hourly, daily, seasonal).

| Fundamental | How it affects power price |
|--------------|----------------------------|
| **Load (demand)** | **Higher load** → higher **marginal cost** of supply (more expensive units dispatched) → **higher** price. **Peak** hours and **summer/winter** peaks → **higher** average price and **spikes** when capacity is tight. **Shape**: weekday vs weekend, hour of day. |
| **Generation availability** | **Outages** (planned or forced) **reduce** supply → **higher** price and **volatility**. **New** capacity (renewables, gas) or **retirements** (coal, nuclear) **shift** the **supply curve** over time. |
| **Renewables (wind, solar)** | **High** output → **lower** net load and often **lower** price (merit order effect); **low** output → **higher** price. **Intermittency** → **volatility** and **within-day** shape (e.g. solar duck curve). **Location** affects **nodal** LMP and **congestion**. |
| **Fuel prices (gas, coal, etc.)** | **Marginal** unit is often **gas**; **gas** price drives **short-run** marginal cost → **power** price and **spark spread**. **Coal** and **nuclear** matter where they set the margin. |
| **Transmission and congestion** | **Binding** constraints → **nodal** price differences (LMP ≠ hub); **congestion** component of LMP. Affects **basis** (node − hub) and **path spread** (FTR). |
| **Weather** | **Temperature** → **load** (cooling/heating); **wind/irradiance** → **renewables**. **Extreme** weather → **spikes** and **stress** scenarios. |
| **Imports / exports** | **Ties** to neighboring markets; **flow** and **price** in adjacent ISOs affect **border** nodes and **arbitrage**. |

**Link to price:** In a **single-node** view, price ≈ **marginal cost** of meeting load (supply curve). **Multi-node**: LMP = **energy** component (marginal cost at reference) + **congestion** (sum of shadow prices × shift factors) + **losses**. Fundamentals drive **all three**.

### 3.2 Main risk factors (power)

| Risk factor | Description | Why it matters |
|-------------|-------------|----------------|
| **Forward price** $F_{0,T}$ | Price (e.g. $/MWh) for delivery at hub/block (e.g. ERCOT North 5x16, month $T$). | **Delta** of forwards and **options**; **MtM** and **VaR** use **curve** as risk factor. **Level** and **term structure** (prompt vs deferred). |
| **Volatility** $\sigma(K, T)$ | Implied or realized vol by strike and expiry. | **Vega** of options; **VaR** (parametric or MC) needs **vol** (and possibly **vol of vol**). **Spikes** → **fat tails** and **smile**. |
| **Load / demand** | Actual or forecast load (MW). | **Driver** of price; **stress** (e.g. heat wave) = high load scenario. **Shape** risk (hourly profile). |
| **Renewable output** | Wind and solar generation (MW or % of load). | **Driver** of **net load** and **price**; **low** renewables → **high** price scenario. **Correlation** with load and gas. |
| **Basis (node − hub)** | Difference between **nodal** LMP and **hub** (or zone) index. | **Location** risk; **physical** or **financial** exposure at node vs hub. **Congestion** and **losses**. |
| **Spark spread** | Power price − heat rate × gas price. | **Generation** margin; **spread options** and **tolling**; **correlation** power–gas. |
| **Shape (hourly profile)** | **Peak vs off-peak**, **within-day** pattern. | **HPFC** and **shaped** contracts; **block** prices vs **hourly** exposure. **Risk**: shape **realized** different from **forward** shape. |

**Summary:** Power risk is **price** (level, vol), **basis**, **shape**, and **spark spread**. Fundamentals (**load**, **renewables**, **fuel**, **outages**, **weather**) drive **level** and **volatility**; **curve** and **vol surface** are the **risk factors** we use for **valuation** and **VaR**.

---

## 4. Gas: Fundamentals and main risk factors

### 4.1 Market fundamentals (gas)

Gas price at a hub is set by **supply** (production, imports, storage withdrawal) and **demand** (power burn, heating, industrial). **Storage** and **pipeline** capacity create **links** across time and location.

| Fundamental | How it affects gas price |
|-------------|---------------------------|
| **Demand** | **Heating** (winter) and **cooling** (summer AC → power burn) drive **seasonal** peaks. **Temperature** (HDD, CDD) is the **main** short-term driver. **Industrial** and **power** demand add **level** and **volatility**. |
| **Supply (production)** | **Dry gas** and **associated gas**; **rig count** and **productivity** drive **long-term** supply. **Short-term**: **maintenance**, **freezes** (e.g. Texas freeze), **outages** can **cut** supply → **spikes**. |
| **Storage** | **Inventory** level (Bcf or % full). **Low** storage → **scarcity** and **higher** price (especially into winter). **Inject/withdraw** rates and **capacity** limit **flexibility**. **Refill** season (spring–fall) vs **draw** season (winter). |
| **Pipeline capacity and flows** | **Pipeline** capacity and **scheduling** limit **flow** between regions. **Basis** (hub A − Henry) reflects **transport** cost and **local** balance. **Outages** or **constraints** → **basis** spikes. |
| **LNG** | **Exports** (US) or **imports** (Europe, Asia) tie **regional** gas to **global** price. **LNG** demand and **shipping** affect **premium** or **discount** at coastal hubs. |
| **Weather** | **Temperature** (HDD/CDD) → **demand**. **Extreme** cold → **demand** spike and sometimes **supply** disruption (freeze-offs) → **price** spike. |
| **Power sector** | **Gas** for **power burn**; **spark spread** links **gas** and **power** price. **High** power demand or **low** renewables → **high** gas demand. |

**Link to price:** **Spot** price = **marginal** cost of meeting **current** demand (supply curve; storage inject/withdraw margin). **Forward** price reflects **expected** balance and **storage** optionality; **winter premium** when winter demand is high relative to supply and storage.

### 4.2 Main risk factors (gas)

| Risk factor | Description | Why it matters |
|-------------|-------------|----------------|
| **Forward price** $F_{0,T}$ | Price ($/MMBtu) at hub (e.g. Henry Hub) for delivery month or strip $T$. | **Delta** of forwards and **options**; **MtM** and **VaR**; **curve** level and **term structure**. |
| **Volatility** $\sigma(K, T)$ | Implied or realized vol by strike and expiry. | **Vega** of options; **VaR** and **stress** (vol can **spike** in events). |
| **Basis (hub − Henry)** | Spread between **regional** hub and **Henry Hub** (or other benchmark). | **Location** risk; **transport** and **local** balance. **Basis** options and **exposure** at non-Henry hubs. |
| **Storage level** | Inventory (Bcf or % of capacity). | **Driver** of **prompt vs deferred** spread and **winter** premium; **stress** (low storage → high price scenario). |
| **Temperature (HDD/CDD)** | **Heating** and **cooling** degree days. | **Demand** driver; **stress** (cold snap, heat wave). **Correlation** with **demand** and **price**. |
| **Correlation (gas–power)** | Correlation between **gas** and **power** price (or returns). | **Spark spread** options and **portfolio** VaR; **joint** scenarios. |

**Summary:** Gas risk is **price** (level, vol), **basis**, **storage**, and **correlation** with power. Fundamentals (**demand**, **supply**, **storage**, **weather**, **pipeline**) drive **level** and **volatility**; **curve**, **vol surface**, and **basis** are the **risk factors** for **valuation** and **VaR**.

---

## 5. Cross-market links

| Link | How it works |
|------|----------------|
| **Power–gas** | **Gas** is **marginal** fuel in many markets → **gas** price drives **power** **marginal cost** and **spark spread**. **Power** demand (especially **peak**) drives **gas** demand (power burn). **Correlation** and **spark spread** are **risk factors** for **combined** books. |
| **FTR–power** | **Path spread** = sink LMP − source LMP; **congestion** component of LMP. **Power** curve (hub price) and **congestion** view together give **path spread**. **FTR** and **power** exposure are **linked** when we have **nodal** or **path** exposure. |
| **Weather** | **Common** driver: **temperature** → **load** (power and gas demand) and **cooling/heating**; **wind/irradiance** → **renewables** (power). **Stress** (heat wave, freeze) affects **power**, **gas**, and **congestion** (FTR) **together**. |

---

## 6. Summary table: fundamentals and risk factors by market

| Market | Main fundamentals | Main risk factors |
|--------|-------------------|-------------------|
| **FTR** | Load, generation (outages, renewables), **transmission topology and outages**, weather, fuel (level) | **Path spread**, **constraint shadow price**, **binding frequency**, **topology/PTDF**, **forward power (hub)** |
| **Power** | Load, **generation stack and outages**, **renewables**, **fuel** (gas), transmission/congestion, weather, imports | **Forward price**, **volatility**, **load**, **renewables**, **basis**, **spark spread**, **shape** |
| **Gas** | **Demand** (temperature, power burn), **supply** (production, LNG), **storage**, **pipeline**, weather | **Forward price**, **volatility**, **basis**, **storage level**, **temperature**, **correlation (gas–power)** |

---

## 7. One-page recap

- **Market fundamentals** = **physical and economic** drivers of **supply**, **demand**, and **clearing**: **load**, **generation** (availability, fuel, renewables), **transmission** (topology, outages), **storage** (gas), **weather**, **fuel prices**. They **explain** and **forecast** prices and congestion; they feed **stress** and **scenario** analysis.
- **FTR fundamentals:** **Load**, **outages** (gen and transmission), **renewables**, **weather** drive **which** constraints **bind** and **shadow** prices. **Path spread** = $\sum_\ell \mu_\ell \cdot \mathrm{PTDF}_{\ell,\mathrm{path}}$. **Main risk factors:** **path spread** (or **constraint shadows**), **binding frequency**, **topology/PTDF**, **forward power** (hub).
- **Power fundamentals:** **Load**, **gen stack**, **renewables**, **fuel** (gas), **outages**, **weather** drive **LMP** level and **volatility**. **Main risk factors:** **forward price**, **volatility**, **load**, **renewables**, **basis**, **spark spread**, **shape**.
- **Gas fundamentals:** **Demand** (temperature, power burn), **supply** (production, LNG), **storage**, **pipeline**, **weather** drive **price** and **basis**. **Main risk factors:** **forward price**, **volatility**, **basis**, **storage**, **temperature**, **correlation (gas–power)**.
- **Cross-market:** **Power–gas** (spark spread, correlation); **FTR–power** (path spread from LMPs); **weather** (common driver for load, renewables, demand). For **portfolio** VaR and **stress**, we need **joint** fundamentals and **risk factors** across FTR, power, and gas.
