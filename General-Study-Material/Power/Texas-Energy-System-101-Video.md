
## ISO vs RTO

- **ISO** — Operates the bulk power system (dispatch, reliability) in a region; can be a single state or part of one.
- **RTO** — An ISO that also runs a **regional wholesale electricity market** (day-ahead and real-time markets, LMPs, congestion management, capacity/ancillary markets). Formed under FERC Order No. 2000 to promote regional coordination.
- **Bottom line:** An RTO is an ISO that operates a regional energy market; an ISO may only do reliability and dispatch. ERCOT is an ISO that runs a market but is not an RTO (it is largely intrastate and not under FERC’s RTO framework).

- RTO is for larger geographical region than ISO
- FERC oversight both of them
- FERC responsibility is to regulate and oversee the interstate transmission of electricity and natural gas
- ISOs and RTOs are responsible for their region

## ISOs and RTOs in North America

**United States (7)**

| Name | Full name | HQ |
|------|-----------|-----|
| CAISO | California ISO | Folsom, CA |
| ERCOT | Electric Reliability Council of Texas | Austin, TX |
| ISO-NE | ISO New England | Holyoke, MA |
| MISO | Midcontinent Independent System Operator | Carmel, IN |
| NYISO | New York ISO | Rensselaer, NY |
| PJM | PJM Interconnection | Audubon, PA |
| SPP | Southwest Power Pool | Little Rock, AR |

**Canada (2)**

| Name | Full name | HQ |
|------|-----------|-----|
| AESO | Alberta Electric System Operator | Calgary, AB |
| IESO | Independent Electricity System Operator (Ontario) | Toronto, ON |

**Total:** 9 ISOs/RTOs (members of the ISO/RTO Council). They serve about two-thirds of U.S. electricity demand and over half of Canada’s population. 

*Note:* ERCOT is an ISO, not FERC-certified RTO (intrastate Texas). ERCOT has no synchronous AC ties to east and west interconnection. PUCT oversee ERCOT. Both ERCOT and PUCT operates within bounds of TEXAS legislature.

## ERCOT goals and responsibility
ERCOT is independent and non-profit. Delivers 90% of electricity.

* ERCOT balance supply and demand in Real-Time. Make sure transmission doesn't get overloaded and keeping the frequncy of the system around 60 hZ.

* ERCOT market is competative and prices clear through a market clearing process.

* ERCOT is nodal, prices are location specific. So cost effective sources are chosen.
* ERCOT plans for transmission project and generation projects. (Yes Energy and Enverus provide Grid maps including new projects)
* ERCOT oversees planning and operation of the infrastructure.

## Market participants in ERCOT
* Any entitiy that buys and/or sell power should be represented by a QSE (the company could be it's own QSE)

### QSE (Qualified Scheduling Entity)

- Submit **bids and offers** to ERCOT on behalf of resources.
- **Inform ERCOT** of a resource’s operations.
- **Financially settle** with both ERCOT and the Resource Entity for any power bought or sold.

Consumers are represented by LSEs which is either a competative retail provider or an electric cooperative or non-opt in entity (NOIE) in non competative market.

LSE buy and/or sell electricity from QSE in DA and/or RT markets or by a long term bilateral contract from a resource entity (RE).

Homes and Businesses pay LSEs for the electricity they consume.

![ERCOT market ecosystem](ERCOT-Flow.png)


## Long term contracts in ERCOT

### Long-term power contracts — for generators

- Provide a reliable revenue stream.
- Reduce exposure to volatility.
- Secure financing for new projects.


### Long-term power contracts — for consumers

- Provide stable and predictable power prices.

**Note:** The majority of power in ERCOT is initially contracted through these long-term agreements.

- since ERCOT doesn't have capacity markets, long-term PPA are very important
- in markets with capacity, plants are paid even for it's potential to generate electricity. In ERCOT generators only paid for the energy they actually generates.(some other payment in the AS market)

### Power Purchase Agreement (PPA)

*Generation resources selling power to buyers (Load Serving Entities, or LSEs) at an agreed price for specific durations.*

### Financial vs physical

**The buyer won’t necessarily receive that physical power directly from the seller.**
The flow of power across large areas is complex. also the flow of power and the real time balancing of power is complex the power price at the time of delivery could be very volatile hence ERCOT has risk management products called CRR.
Even with a bilateral agreement (e.g. PPA) between a generator and an LSE, physical power is dispatched and flows according to the grid operator (e.g. ERCOT) and physics—not along a direct path from that generator to that buyer. The contract is settled financially; congestion and location are handled by the market (e.g. LMPs, CRRs/FTRs).

### Purpose of CRRs (Congestion Revenue Rights)

- Protect participants against price volatility.
- Speculate on price variation across the system. These variation happens locationally.

## LMP
in nodal power market prices are different at each node
LMP: value of producing additional unit of power at a node

## System Lambda (λ)
*The cost of procuring the next cheapest unit of energy across the entire system.* Equivalently: *the cost of dispatching the next cheapest available generation across the entire system.* System-wide marginal energy cost; at each node, LMP reflects this plus congestion and losses.

### How System Lambda is set: supply stack (merit order)
Generation is dispatched in **merit order** (cheapest marginal cost first). The **supply stack** orders resources from lowest to highest $/MWh (e.g. Wind, Solar, Nuclear, Coal, Gas). **System demand** (in GW) determines which unit is **marginal** — the last unit needed to meet demand — and that unit’s price is **System Lambda**.

- **Example (day, 50 GW demand):** Stack might be Wind $10, Solar $12, Nuclear $15, Coal $25, Gas $40. Demand crosses the stack at Coal → **System Lambda = $25/MWh**.
- **Example (night, 55 GW demand):** No solar; stack Wind $10, Nuclear $15, Coal $25, Gas $40. Higher demand crosses at Gas → **System Lambda = $40/MWh**.

So System Lambda (and thus the energy component of 5‑minute LMPs at load zones/trading hubs) moves with demand and which fuel is on the margin.

### Other factors that influence System Lambda
- **Resource ramp rates** — how quickly generation can increase or decrease output.
- **System frequency** — grid frequency (e.g. 60 Hz) and its regulation, which affects dispatch and pricing.
- **Bid and offer curves of individual resources** — the price/quantity offers and bids from generators and load that clear in the market.

## Constraint
A **constraint** is a transmission element (a line, corridor, or interface between regions) that has a **limit on power flow** (in MW). The limit can be thermal (equipment rating), stability-related, or operational. In market and dispatch models, constraints are enforced so that flow on each element does not exceed its limit. When a constraint’s limit is **binding** (flow equals the limit), that constraint affects LMPs and creates congestion. any constraint has an export side and an import side.

## Congestion
*When a part of the transmission network is either overloaded, or is at risk of becoming overloaded.* Congestion prevents power from flowing freely between locations and causes LMP to differ from System Lambda across nodes (price separation); CRRs/FTRs hedge this congestion risk between settlement points. Congestion is the cause of price disparity between Settlement points. Congestion is factored in all of the LMPs accross the system.

### No congestion: LMP = System Lambda everywhere
When the transmission network is not constrained, power can flow freely and **LMP is the same at every node** — equal to **System Lambda** (e.g. $17/MWh at generation and at demand). In that case there is no locational price difference and no congestion value between settlement points.

## Shift Factor (SF)
*Represents how much impact that resource has on that constraint.* For a given transmission constraint (e.g. a line or interface), the shift factor at a node (or resource) measures how much an incremental injection of power at that location affects the flow on the constrained element. Shift factors are used in congestion management, LMP calculation, and FTR/CRR valuation (e.g. to see how much a path or resource is exposed to a constraint).

### A generator's impact on a constraint
**Δ Flow (MW) = (Δ output) × (SF)**  
- **Increase:** SF = 0.5, Δ output = +10 MW → Δ Flow = 10 × 0.5 = **+5 MW** (adds flow on the constraint).  
- **Decrease:** SF = 0.5, Δ output = -10 MW → Δ Flow = (-10) × 0.5 = **-5 MW** (reduces flow on the constraint, can relieve congestion).  

This relationship is used to quantify congestion and FTR/CRR exposure.

### Solving a constraint
When addressing a transmission constraint, three questions matter:
- **How severe it is** — magnitude of the overload or risk (drives congestion rent).
- **How much generation will need to be re-dispatched (using shift factors)** — which resources to move up or down to change flows on the constrained element.
- **How expensive it will be to re-dispatch that generation based on their offer curves** — the cost of re-dispatch sets the shadow price of the constraint and thus congestion costs that FTRs/CRRs hedge.

Constraint locations are often described in terms of an **import side** and an **export side** of the congested path.

## Shadow Price (SP)
*The cost, on a per megawatt basis, of re-dispatching generation to resolve the constraint.* The shadow price of a transmission constraint is the $/MW value of relaxing that constraint (e.g. $100/MW). It drives the congestion component of LMP differences between locations and is the basis for congestion rents that FTRs/CRRs hedge.

## Calculating LMPs
At a node, **LMP = System Lambda (λ) − (Shadow Price × Shift Factor)** for each binding constraint (and similarly for losses in full models). When **Shift Factor = 0**, the node is not on the constraint, so **LMP = λ**.

**Examples (Shadow Price = $100/MW, λ = $200/MWh):**
- **Positive SF:** Shift Factor = 0.5 → LMP = 200 − (100 × 0.5) = **$150/MWh** (LMP below λ; more generation here adds flow on the constraint).
- **Negative SF:** Shift Factor = −0.5 → LMP = 200 − (100 × (−0.5)) = 200 + 50 = **$250/MWh** (LMP above λ; more generation here reduces flow on the constraint, so this side is short and prices up).

The spread between LMPs on the two sides of the constraint is what FTRs/CRRs pay or receive.

When multiple constraint at the same time, ERCOT determine LMPs by repeating the same calculation across every constraint and for every settlement point, then find the sum of these values at every settlement point and subtract the value from system lambda. and that would be the SPP of the node.

## ERCOT nodes and settlement points (2024)

- **17,000 nodes** in ERCOT (connection points on the grid).
- **Just under 900** of these have a **unique LMP** (distinct locational marginal price).
- Nodes with a unique LMP are known as **Settlement Points** — the locations where prices are defined and where market and CRR/FTR settlements are referenced. Geographically, these settlement points are distributed across Texas (and the ERCOT footprint), with higher density in central and eastern regions.

### Resource Node vs Settlement Point

- **Resource Node:** A transmission-connected resource that participates in wholesale markets and can respond to dispatch instructions (e.g. generation or load connected to the grid).
- **Settlement Point:** A node with a unique LMP used for pricing and settlement; the ~900 such points appear on ERCOT maps as the main price/settlement locations. Some areas (e.g. far west Texas, panhandle, eastern border) may be outside the ERCOT footprint or represented differently.

- **Load zones / trading hubs:** ERCOT produces **5-minute interval prices** (LMP) for load zones and trading hubs, which are aggregated settlement points used for trading, hedging, and settlement.

## How ERCOT wholesale market works

### Day-Ahead Market (DAM)
*Participants submit bids and offers for power to be delivered the next operating day.* The day-ahead market clears before the operating day and produces scheduled quantities and day-ahead LMPs by location; real-time markets then adjust for actual delivery. DAM is for Energy and AS.

**DAM flow (participants and bids):** ERCOT runs the Day-Ahead and Real-Time wholesale market at the center. **QSEs** (Qualified Scheduling Entities) represent **generation (Resource Entities)** and **load resources** (e.g. data centers); they submit **bids and offers** to ERCOT. **LSEs** (Load Serving Entities) also submit **bids to buy electricity** to ERCOT and serve **commercial & industrial** and **residential** consumers, often through **distribution**. The **Transmission Service Provider (TSP)** operates the transmission grid. Power can also be arranged via **bilateral contracts** between generation (RE) and LSEs outside the central market.

**Supply and demand in the DAM:** In the Day-Ahead Market, **supply** is the aggregation of **offer curves** submitted by QSEs (generators): at each price, the total MW offered. **Demand** is the aggregation of **bids to buy** from loads and LSEs. The **market clears** where the supply and demand curves intersect, giving the clearing **price** and **volume** (MW) for the day-ahead schedule. In a nodal market like ERCOT this is done per location, so each node has a day-ahead LMP; the Texas map with dots illustrates the many generation and load points across the ERCOT footprint where these prices and quantities are defined.

**What influences energy prices in the DAM:**
- **Startup costs and startup times of resources** — turning units on/off is costly and slow; the market accounts for this in the day-ahead schedule and prices.
- **Other services resources offer** — ancillary services, capacity, or other products that resources bid alongside energy.
- **Physical limits of the transmission network** — constraints on lines and interfaces limit where power can flow and create congestion, so day-ahead LMPs differ by location.

**DAM timeline:** The **Day-Ahead** period is the day before the **Operating day**. During the day-ahead window (e.g. 6:00–10:00 on the day ahead), participants **submit bids and offers**; the **Day-Ahead Market is then executed** and produces a schedule and day-ahead LMPs for each hour of the next operating day. **RUC (Reliability Unit Commitment)** runs after the DAM run: forecasted capacity is continuously assessed, and RUC runs every hour (from roughly midday 14:30 on the day-ahead through to the start of the operating day) to commit additional units if needed for reliability. On the **Operating day**, **real-time operations** run: the committed energy is delivered in the scheduled hours and real-time markets adjust for deviations from the day-ahead schedule.

After 10:00 ERCOT executes. For each hour of the following operating day, LMP is generated at each Settlemen point. Meanwhile **In the Day-Ahead Market, for every operating hour a system-wide clearing price is determined for each Ancillary Service** (e.g. regulation, reserves)—unlike energy, which has locational LMPs; AS prices are typically single system-wide values per product per hour. Award for Energy and AS are co-optimized to ensure the least cost across the system. Then these awards are relayed to resources via QSEs. Then QSEs update operating plan for their respective REs. 

If ERCOT feels like it needs more supply for the next day, the extra is bought through RUC. RUC runs from 14:30 of DA until 00:00 of Operating day. Forecasted capacity is continuoulsy assessed by RUC. RUC runs every hour. RUC can commit operators to be online for the operating day.

## Offer curves (from QSEs)
**Offer curves** are the price–quantity schedules that QSEs submit to ERCOT on behalf of generation resources. For each resource (or block of capacity), the curve states how much energy (MW) the resource is willing to supply at each price level ($/MWh). Typically they are **step functions**: e.g. “offer 50 MW at $20/MWh, another 100 MW at $35/MWh,” and so on. ERCOT uses these curves in the day-ahead and real-time markets to run **economic dispatch**: it stacks all offers in merit order (cheapest first) and clears the market where supply meets demand, which determines System Lambda and LMPs. Offer curves therefore directly drive which units are dispatched and the clearing price; they also determine the **cost of re-dispatch** when relieving a constraint (and hence shadow prices and congestion costs).

Participants in energy and **ancillary services (AS)** can submit offer curves for **both** simultaneously. Common types include: **Energy Offer** (MW of energy at each $/MWh); **Regulation Up Offer** (MW of upward regulation capacity, sometimes at low or negative prices when the resource wants to be dispatched); and **Responsiveness Reserve Service Offer** (MW of reserve capacity). Each is a step-wise curve of MW vs price; the market clears energy for each ancillary service product separately, using the relevant offer curves. 
 
## ERCOT Ancillary Services
Frequency of ERCOT is 60 Hz.

### What do Ancillary Services do?
1. **Manage minor deviations in frequency** — keep the grid near 60 Hz during normal small imbalances.
2. **Recover significant deviations in frequency** — restore frequency after larger disturbances.
3. **Provide fast-responding capacity to meet demand** — reserves that can ramp quickly when needed.

### What are the four Ancillary Services?
1. **Regulation (Up and Down)** — Regulation manages small deviations in either direction when frequency is just above or below 60 Hz; resources increase or decrease output to bring frequency back to 60 Hz. **Regulation Down** (when frequency is above 60 Hz): reduces frequency by importing energy or reducing generation—e.g. a Battery Energy Storage System (BESS) does this by importing (charging) or reducing export (discharging less). **Regulation Up** (when frequency is below 60 Hz): increases frequency by exporting energy or increasing generation—e.g. a BESS exports (discharges) or reduces import (charges less).
2. **Responsive Reserve Service (RRS)** — capacity that can respond quickly to meet demand or replace lost capacity. During an under-frequency event, different RRS layers activate at set thresholds: **RRS (Primary)** at 59.983 Hz; **RRS (Under Frequency Response)** at 59.85 Hz; **RRS (Fast Frequency Response)** at 59.7 Hz.
3. **ERCOT Contingency Reserve Service (ECRS)** — reserves held for contingency events (e.g. unit or line outages). **ECRS** activates at **59.91 Hz** during an under-frequency event.
4. **Non-Spinning Reserve Service (Non-Spin)** — capacity that can be brought online within a defined time (e.g. offline or partially loaded units).

## Real Time Market and SCED
Supply and demand of energy are never perfectly balanced in the DAM, so balancing is done in **Real Time**. Generation and load resources have up to an hour before the start of each operating hour to adjust their offer and bid curves; demand must be met at lowest cost. **Dispatch occurs every five minutes through SCED.**

### Security Constrained Economic Dispatch (SCED)
**SCED** is an algorithm that evaluates:
- Real-Time bids and offers
- Grid constraints (transmission limits)
- System frequency
- Forecasted changes in generation and demand  

*…in order to determine the most cost-effective dispatch of resources.* SCED runs every 5 minutes in real time and produces dispatch instructions and real-time LMPs. **SCED sends base points to resources** — i.e. it issues target output levels (MW) to each generation and demand resource so they adjust their power output to meet demand and respect constraints. **In the real-time market**, SCED dispatches resources to meet the **projected increase in demand in the next interval** (e.g. over each 5-minute window); **congestion costs are also taken into account**, so dispatch and LMPs reflect transmission constraints and their shadow prices. Every **5 minutes** ERCOT runs a **State Estimation** process (to estimate voltage magnitudes, angles, and flows across the grid from measurements). **During state estimation**, ERCOT uses **power flow data** received from QSEs and LSEs (and from the transmission grid) to build a consistent snapshot of the system state for use in SCED and reliability analysis. **Aggregated power flows** from this process form the **"base-case"** — the reference solution (voltages, angles, flows) used for dispatch and constraint analysis. The **5-minute operating sequence** runs in order: **State Estimation** → **Contingency Analysis** → **Economic Dispatch** (SCED). **Contingency** means *potential events that may cause transmission congestion* (e.g. line or unit outages); contingency analysis uses the base-case to test these events and identify binding constraints before SCED runs. **Dispatch** occurs in **5-minute intervals** (each a SCED interval); **settlement** is over a **15-minute interval** (one settlement period covers three 5-minute SCED intervals). The **settlement price** for that 15-minute period is the **average of the three SCED interval prices**: e.g. Price = (A + B + C) / 3, where A, B, and C are the prices from the three 5-minute intervals within the settlement window.

SCED is used to balance supply and demand in Real Time.

## Price Adders (two kind)

### System Reserves
*All the available power supply that isn't currently being used.* System reserves are the difference between **available capacity** (all online resources, including those committed to reserves) and **current generation output** — i.e. the headroom not yet dispatched. When **renewables or other resources are offline** or **system demand is high** (e.g. 95% of capacity), reserves shrink and the system is tighter; scarcity and the cost of holding reserves can show up as **price adders** in the market. Price adders are designed to ensure that additional supply is priced appropriately using the Operating Reserve Demand Curve (ORDC). When system reserves fall below 7 GW, ERCOT attach price adders to all LMPs across system based on the ORDC. When fewer reserves, the price adder increases. 3 GW or less system reserves indicate Emergency Condtions in ERCOT. at this stage all the prices on the system are set at the system wide offer cap of 5000$/MWh (highest amount generators are paid to generate in ERCOT set by PUCT)



### Reliability Deployment Price Adder
*Comes into play when ERCOT takes "out-of-market" reliability actions to reduce demand or increase supply.* When ERCOT deploys or commits resources outside the normal market (e.g. for reliability, reserves, or emergency actions), the associated costs are recovered through a **Reliability Deployment Price Adder** applied to market prices. **Reliability Unit Commitment (RUC)** is when ERCOT commits a generating unit to be **online at a specified time** (e.g. “We need you to be online at 19:00”) to meet forecasted demand or reserve requirements that the day-ahead market did not clear. The unit is compensated for this out-of-market commitment; RUC costs can flow through to the **Reliability Deployment Price Adder**.

Using RUC can actually supress prices in ERCOT since it may end up with excess supply online that it doesn't need. 

To calculate this price adder ERCOT finds the difference of System lambda without RUC - System lambda with RUC. in majority of the time the value is $0/MWh. 

When either of the two kinds of price adders are above 0, it applies to all LMPs in the ERCOT.

---

## Supply stack modeling

**Supply stack modeling** is a way to represent how **wholesale power prices** (e.g. System Lambda, the energy component of LMP) are set by **ordering available generation from cheapest to most expensive** and finding where **demand** crosses that stack. It is the same idea as **merit order** dispatch: the **marginal unit** (the last unit needed to meet demand) sets the clearing price.

### What the supply stack is

- **Supply stack** — A curve (or step function) of **cumulative capacity (MW)** vs **price ($/MWh)**. Each “step” is a block of generation (e.g. a unit or a fuel segment) offered at a given price. The stack is ordered from **lowest to highest** offer price.
- **Demand** — Total system load (or scheduled demand) in **MW** at a point in time (e.g. an hour or 5‑minute interval).
- **Clearing** — The **height** of the stack at the demand quantity is the **marginal cost** of the last unit dispatched — i.e. **System Lambda** (before congestion and losses). So: **stack + demand → System Lambda**.

### Why it matters

- **Price formation** — System Lambda (and thus the energy component of LMP at unconstrained nodes) is the **marginal** cost of supply. The stack model makes this explicit: same demand, different stack (e.g. more cheap renewables vs more gas) → different price.
- **Scenarios and stress** — You can **shift** demand (e.g. hot day, high load) or **remove** capacity (outages, low wind) and see how the **marginal unit** and **price** change. Used for **price forecasting**, **stress testing**, and **VaR**/scenario analysis.
- **Congestion** — The stack is often built **system-wide** (or for a hub). **Locational** differences come from **congestion** and **losses** (LMP = System Lambda − shadow price × shift factor + loss component). So the stack explains the **energy** piece; **constraints** explain **spreads** between nodes.

### Building a supply stack (conceptually)

1. **Capacity by price** — For each resource or segment (e.g. wind, solar, nuclear, coal, gas peakers), assign **available capacity (MW)** and **marginal cost or offer price ($/MWh)**. Data can come from **offer curves** (what generators actually bid), **cost models** (heat rates, fuel prices), or **typical merit order** by fuel.
2. **Order by price** — Sort all capacity from **lowest to highest** $/MWh and form a **cumulative** MW curve. That’s the supply stack.
3. **Demand** — Plot **demand** (MW) on the horizontal axis. Where demand hits the stack (vertical line) gives **System Lambda** on the vertical axis.
4. **Sensitivities** — Change **demand** (e.g. +5 GW), **remove** capacity (outage), or **shift** offer levels (e.g. higher gas price) and re-read the new marginal price.

### Relation to ERCOT markets

- **Day-Ahead and Real-Time** — ERCOT clears the market using **offer curves** submitted by QSEs. The **market** effectively builds a **stack** from those offers (merit order) and clears where **supply** meets **demand**; the clearing price is System Lambda (at the hub or before congestion). So supply stack modeling is a **simplified representation** of that process.
- **Single-node vs nodal** — A **single** stack usually gives a **system-wide** or **hub** energy price. **Nodal** LMPs add **congestion** and **loss** components from the **network** (constraints, shift factors, shadow prices).
- **Use in practice** — Stack models are used for **fundamental** price views, **stress** (e.g. “what if 10 GW of wind is off?”), **margin** analysis (spark spread, dark spread), and **explaining** why prices moved (demand up, marginal unit moved from coal to gas).

### Short summary

**Supply stack modeling** orders generation from cheapest to most expensive and finds the **marginal unit** where demand crosses the stack; that marginal price is **System Lambda**. It’s used to **explain** and **forecast** power prices, run **scenarios** (demand, outages, fuel costs), and stress **energy** component of LMP; **congestion** and **losses** then explain **locational** differences on top of that.

---

## Heat rate and modeling it

**Heat rate** measures how much **fuel energy** (input) a generator needs to produce one unit of **electrical energy** (output). It is the inverse of **thermal efficiency**: lower heat rate = more efficient. Heat rate is central to **marginal cost** and **offer curves** for thermal units (gas, coal, etc.) and thus to **supply stack** and **spark spread** modeling.

### What heat rate is

- **Definition** — **Heat rate** = fuel input (energy) per unit of electricity output. Common units: **MMBtu per MWh** (million Btu per megawatt-hour). So a unit with heat rate **7.5 MMBtu/MWh** burns **7.5 MMBtu** of fuel to produce **1 MWh** of electricity.
- **Efficiency** — **Efficiency (%)** ≈ 3,412 / heat rate (when heat rate is in Btu/kWh). Lower heat rate (e.g. 7 MMBtu/MWh) = more efficient; higher (e.g. 10 MMBtu/MWh) = less efficient. Combined-cycle gas (CCGT) is typically **~7–8 MMBtu/MWh**; simple-cycle gas peakers **~10–11 MMBtu/MWh**; coal **~9–10 MMBtu/MWh** (varies by unit).
- **Gross vs net** — **Gross heat rate** uses **gross** electrical output (before station service/parasitic load). **Net heat rate** uses **net** output (after internal consumption). For **cost and offer** modeling, **net** heat rate is the right one (what you actually sell).

### Why it matters for pricing and the stack

- **Marginal cost (\$/MWh)** — For a thermal unit, **variable** cost of producing one more MWh is (approximately) **fuel price (\$/MMBtu) × heat rate (MMBtu/MWh)**. Example: gas at **$3/MMBtu**, heat rate **8 MMBtu/MWh** → **$24/MWh** marginal cost. That drives where the unit sits on the **supply stack** and when it is **marginal**.
- **Offer curves** — In ERCOT (and other markets), gas units often offer energy at a level tied to **fuel cost + heat rate** (plus a margin or uplift). So **heat rate** is a key **input** to the **offer curve** and thus to **System Lambda** when gas is on the margin.
- **Spark spread** — **Spark spread** = power price ($/MWh) − (gas price × heat rate). It is the **gross margin** (before O&M, start costs) of burning gas to make power. Modeling heat rate lets you compute **spark spread** and assess when gas units are **in the money** and how **sensitive** power prices are to **gas prices**.

### Modeling heat rate

1. **Single value** — Use a **constant** heat rate per unit or per technology (e.g. 8 MMBtu/MWh for CCGT). Simple; good for **screening** and **stack** models when you don’t have unit-level data.
2. **Unit-level** — Use **reported** or **estimated** heat rates per plant/unit (from EIA, Enverus, or operator data). Improves **accuracy** of **marginal cost** and **stack** order, especially when units differ (e.g. old vs new CCGT).
3. **Load-dependent (heat rate curve)** — Heat rate often **worsens** at **low load** (e.g. 50% load → higher MMBtu/MWh than 90% load). Model **incremental heat rate** (IHR) or **average heat rate** as a function of **output (MW)** so that **marginal cost** varies with dispatch level. Important for **unit commitment** and **detailed** dispatch models.
4. **Inputs to the stack** — In a **supply stack** model, each thermal block’s **offer price (\$/MWh)** can be set as **fuel price × heat rate** (plus O&M or adder). So **heat rate** + **fuel price** (e.g. gas at hub) → **$/MWh** → place that block in the **merit order**. **Sensitivities**: change **gas price** or **heat rate** to see how **marginal unit** and **System Lambda** change.

### In the ERCOT context

- **Gas-heavy margin** — In ERCOT, **gas** is often the **marginal** fuel (especially in peak hours and when wind/solar are low). So **gas price** and **gas unit heat rates** directly drive **System Lambda** and **power prices** in many hours.
- **Data** — Heat rates by unit are available from **EIA**, **ERCOT** (resource data), and commercial data (e.g. Yes Energy, Enverus). **Gas price** is usually a **hub** price (e.g. Houston Ship Channel, Katy, Waha) or a basis to one of those.
- **Risk and valuation** — **Spark spread** (power − gas × heat rate) is a key **exposure** for gas-fired generators and for **power** traders. Modeling **heat rate** correctly is needed for **margin** analysis, **hedging** (how much gas per MWh sold), and **stress** (e.g. gas spike → how much does power move?).

### Short summary

**Heat rate** (MMBtu/MWh) is **fuel input per MWh**; it defines **thermal efficiency** and, with **fuel price**, the **marginal cost** ($/MWh) of thermal generation. **Modeling** it (constant, unit-level, or load-dependent) feeds **supply stack** and **spark spread** models and explains how **gas** (and other thermal) **prices** and **efficiency** drive **power prices** in ERCOT and other markets.

---

## Spark spread and dark spread

**Spark spread** and **dark spread** are **gross margin** measures for **gas-fired** and **coal-fired** generation: they compare **power price** to the **fuel cost** (per MWh) of producing that power. They are used for **valuation**, **hedging**, **trading**, and **risk** (e.g. when is a unit “in the money”?).

### Spark spread

- **Definition** — **Spark spread** = **power price (\$/MWh)** − (**gas price (\$/MMBtu)** × **heat rate (MMBtu/MWh)**). It is the **gross margin** (before O&M, start-up, emissions) from selling 1 MWh of power produced by burning gas. Units: **$/MWh**.
- **Interpretation** — **Positive** spark spread → gas unit can cover **variable** (fuel) cost and contribute to fixed costs and profit. **Negative** → fuel cost exceeds power revenue at that heat rate. **Zero** → power price equals **marginal** fuel cost (breakeven for fuel).
- **Formula (typical)** — **Spark spread ($/MWh)** = **LMP** (or hub power price) − (**gas price × heat rate**). Example: LMP **$40/MWh**, gas **$4/MMBtu**, heat rate **8 MMBtu/MWh** → spark spread = 40 − (4 × 8) = **$8/MWh** (positive margin).
- **Why it matters** — Determines when **gas** units are **dispatched** and **profitable**; used for **plant valuation**, **hedging** (e.g. sell power, buy gas; or trade spark spread options), and **risk** (sensitivity of margin to power and gas prices). In ERCOT, **gas** is often on the margin, so **spark spread** is a core **exposure** for gas generators and power traders.

### Dark spread

- **Definition** — **Dark spread** = **power price (\$/MWh)** − (**coal price (\$/MMBtu or \$/ton)** converted to **\$/MWh** via **heat rate**). Same idea as spark spread but for **coal**. Sometimes written as: **power** − (**coal price × heat rate**), with coal in **\$/MMBtu** (or **\$/ton** with a conversion). May include **carbon/emissions cost** (see below).
- **Interpretation** — **Positive** dark spread → coal unit covers **variable** (fuel) cost. Used to assess **coal** plant **margin**, **dispatch** order vs gas (merit order), and **hedging** (power vs coal).
- **Coal price** — Coal is often quoted in **\$/ton**. To get **\$/MWh**: use **heat content** of coal (MMBtu/ton) and **heat rate** (MMBtu/MWh): **fuel cost per MWh** = (coal $/ton) × (heat rate / heat content). Example: coal **$50/ton**, **20 MMBtu/ton**, heat rate **9 MMBtu/MWh** → fuel cost = 50 × (9/20) = **$22.50/MWh**; dark spread = **LMP − $22.50/MWh**.
- **ERCOT note** — ERCOT is **gas-heavy**; coal is a smaller share of the stack. Dark spread is still used for **coal** units that exist, **cross-commodity** views (coal vs gas margin), and in **other** markets (e.g. PJM, MISO) where coal is more prominent.

### Clean spark spread and clean dark spread

- **With emissions** — If **carbon** (or emissions) has a price, **variable** cost includes **fuel + emissions**. **Clean spark spread** = power − (gas × heat rate) − (CO₂ cost per MWh). **Clean dark spread** = power − (coal fuel cost per MWh) − (CO₂ cost per MWh). Used in regions with **carbon pricing** or **allowances** (e.g. RGGI, EU ETS). ERCOT has no carbon price today, but the concept applies if one is introduced or for **forward** views.

### Modeling spark and dark spread

1. **Inputs** — **Power price** (LMP or hub, \$/MWh); **gas price** (hub, \$/MMBtu); **heat rate** (MMBtu/MWh) for gas; for dark spread: **coal price** (\$/ton or \$/MMBtu) and **coal heat rate** (and heat content if in $/ton).
2. **Single period** — Compute **spark** = power − gas × HR; **dark** = power − coal cost per MWh. Compare to **zero** or to **O&M** to assess **margin**.
3. **Over time** — **Time series** of spark/dark spread (e.g. by hour or day) for **historical** analysis, **distribution** (how often positive?), and **stress** (e.g. gas spike → spark spread collapse).
4. **Sensitivities** — **Delta** to power price (+1 $/MWh → +1 $/MWh spark); to gas price (−heat rate $/MWh per $/MMBtu gas); to heat rate (−gas price $/MWh per MMBtu/MWh). Same idea for dark spread with coal price and coal heat rate.
5. **Link to supply stack** — When **spark spread** is **positive** for a gas unit at its heat rate, that unit is **in the money** (power above its marginal fuel cost). The **supply stack** is built from **marginal cost** = fuel × heat rate; **clearing** power price vs that stack shows which units are **marginal** and what **spark** (or dark) **margin** they earn.

### Use in practice

- **Valuation** — Expected **spark** or **dark** spread (over time) × capacity × availability → gross margin potential for a plant or portfolio.
- **Hedging** — Sell power, buy gas (or coal) to lock in **spark** or **dark** spread; or trade **spark spread** products (e.g. power − gas × fixed heat rate) to manage **basis** between power and fuel.
- **Risk** — **Exposure** to **power** and **fuel** prices; **correlation** and **stress** (e.g. gas up, power up but not enough → spark spread down). **VaR** or **scenario** on **spread** distribution.
- **Trading** — **Spread** as a single number (or curve) to trade; **spark spread options** (e.g. pay-off when spark > strike).

### Short summary

**Spark spread** = power price − (gas price × heat rate): **gross margin** for gas-fired generation in **$/MWh**. **Dark spread** = power price − coal fuel cost per MWh: same for **coal**. **Modeling** uses power price, fuel price(s), and heat rate(s); over time and with sensitivities for **valuation**, **hedging**, and **risk**. **Clean** spreads subtract **carbon cost** when relevant. In ERCOT, **spark spread** is the main one (gas on the margin); **dark spread** applies to remaining coal and to **cross-market** comparison.
