# ERCOT Wholesale Market 101

## Course Topics

1. Introduction
2. Real-Time Dispatch and Pricing
3. Forward Markets
4. Energy Settlements
5. Congestion
6. Ancillary Services
7. System Capacity

---

## 1. Introduction

### ERCOT Market Operations (in general)

Two main phases:

1. **Day-Ahead**
2. **Operating Day** (follows Day-Ahead)

Timeline (key times):

| Phase | Time |
|-------|------|
| Day-Ahead Market | starts ~10:00, past 13:30 |
| Adjustment Period | For each operating hour of the operating day: starts **18:00** day-ahead, ends **1 hour before** that operating hour. |
| Hour Ahead | For each operating hour: starts when the Adjustment Period for that hour **ends**, ends when the operating hour **begins**. |
| Operating Hour | the hour of operation |

Key timestamps: **10:00**, **13:30**, **18:00**.

### ERCOT market ecosystem (entities and flows)

**Entities**

- **LSE** — Load Serving Entity  
- **QSE** — Qualified Scheduling Entity  
- **RE** — Resource Entity (generation)  
- **TSP** — Transmission Service Provider  
- **DSP** — Distribution Service Provider  
- **Consumers** — end use  
- **ERCOT** — ISO / market operator  
- **Independent Market Monitor** — market oversight  
- **PUCT** — Public Utility Commission of Texas — regulator  

**Flows**

- **Wholesale settlement:** LSE ↔ QSE  
- **Operations & settlement:** QSE ↔ ERCOT; QSE → RE  
- **Trades:** RE → LSE  
- **Physical path:** RE → TSP → DSP → Consumers  
- **Operations (to ERCOT):** RE, TSP, DSP → ERCOT  
- **Retail settlement:** LSE → Consumers  
- **Data:** ERCOT → Independent Market Monitor  
- **Reporting:** Independent Market Monitor → PUCT  
- **Oversight:** PUCT → ERCOT  

![ERCOT market ecosystem](ERCOT-Flow.png)

### A few words of economics — supply and demand curves

![Supply and Demand Curve](supply-demand.png)
- **Axes:** $/MWh (price) vs MW (quantity).
- **Bids** — downward-sloping (demand): as price falls, quantity demanded (MW) rises.
- **Offers** — upward-sloping (supply): as price rises, quantity supplied (MW) rises.
- **Intersection** of bids and offers = **market equilibrium** (clearing price and quantity).
- In ERCOT: bids = what buyers (e.g. LSEs) are willing to buy at each price; offers = what sellers (e.g. generators) are willing to supply at each price.

### A couple of definitions

- **Bid** — proposal to **buy**:
  - A product  
  - At a location  
  - For a price  

- **Offer** — proposal to **sell**:
  - A product  
  - At a location  
  - For a price  

### Economics and ERCOT market operations

**Some ERCOT processes are optimized for value.**
![Supply and Demand Curve optimized](supply-demand-optimized.png)
- Same axes: **$/MWh** (price) vs **MW** (quantity); **Bids** (demand) and **Offers** (supply) curves.
- The **intersection** of bids and offers is the market outcome:
  - **Optimized value** — the clearing price ($/MWh) at that point.
  - **Solution** — that price and the clearing quantity (MW) together; the result of the optimization.

**Other ERCOT processes are optimized for cost.**
![Supply and Demand Curve optimized cost](supply-demand-optimized-cost.png)
- Graph: **MW** (x-axis) vs **$/MWh** (y-axis); **Offers** curve only (upward-sloping supply).
- **Required MW** — a given quantity that must be supplied (vertical line).
- **Optimized cost** — the (green) area under the Offers curve up to Required MW: total cost of meeting that quantity by stacking offers from lowest cost upward (cost minimization).

### Mini-market topology (for scenarios)

This topology is used later in the presentation for different scenarios.

![Mini-market for scenarios](Mini-Market-for-Scenarios.png)

---

## 2. Real-Time Dispatch and Pricing

### Real-Time Dispatch — Goals

- Manage reliability
- Match generation with demand
- Keep transmission flows within limits
- Operate the system at least cost

Real-time dispatch balances **reliability** and **economics**.

### Real-Time Dispatch Timing

- **Day-Ahead** — before 00:00 (market/commitments).
- **Operating Day** — from 00:00 (physical delivery, real-time dispatch).
- **Operating Hour** — one hour within the Operating Day (dispatch/pricing granularity).

### Security Constrained Economic Dispatch (SCED)

**Inputs:** Offers, System Conditions, Network Model.  
**Outputs:** Five-minute Base Points (dispatch instructions to resources), Five-minute Prices (LMPs).

SCED matches generation with demand, manages congestion, and achieves least-cost dispatch while balancing **reliability** and **economics**. **Base points** are determined every **5 minutes**.

### Offers to SCED — Energy Offer Curve

- Monotonically increasing ($/MWh vs MW).
- Up to **10 price/quantity pairs** per curve.
- **1 MW** minimum quantity per segment.
- Prices between **-$250** and **SWCAP** (System-Wide Offer Cap).

### Discussion: System Conditions (Monitored Conditions)

**What does SCED need to know?** SCED’s “System Conditions” input reflects **monitored conditions** across the delivery chain: generation (output, status), transmission (flows, limits, topology), distribution, and load. The physical flow is: Generation → Transmission → Distribution → Consumption.

### Network Operations Model

Represents the **physical transmission grid** (topology, lines, limits, substations). Used for **reliability studies** and **all market processes** (including SCED and congestion/FTR-related processes).

### Scenario: Find Dispatch Solution

![Dispatch solution](dispatch-solution.png)
Simplified network: **345 kV Hub**; **Load Zone** (1100 MW load), connected to the Hub and to **Resource Node 3**; **Resource Node 1** and **Resource Node 2** connected to the Hub. Each resource has an **Energy Offer** curve (price/quantity steps). SCED finds the least-cost dispatch of generation from these nodes to meet the 1100 MW load subject to the network model and offers (e.g. Node 1: 150 MW @ $30, +150 @ $35, +50 @ $40; Node 2: 200 MW @ $20; Node 3: 400 MW @ $30, +300 @ $50, +100 @ $120). **Variant:** If **Resource Node 2 is unavailable** (e.g. out of service), SCED must meet the 1100 MW load using only Node 1 and Node 3; the solution fills in dispatch quantities, flows, and LMPs at each node.

---

## 3. Forward Markets

### Hedging and Price Certainty

**Hedging** is transacting at a known price now to protect from having to transact at an unknown price later. Forward contracts, CRRs/FTRs, and other financial instruments provide this price certainty.

### Forward Energy Markets in ERCOT

- **Day-Ahead Market (DAM)** — Centralized market with supply and demand curves; clearing sets price and quantity.
- **Bilateral Trades** — Parties trade $ and MW directly (e.g. forward contracts) outside the DAM.

### Bilateral Trades — Decentralized Forward Market

- **QSE-to-QSE transactions** — Trades are between Qualified Scheduling Entities.
- **Transfers settlement responsibility** — The bilateral agreement shifts who is responsible for settlement with ERCOT (e.g. who pays or receives for the energy).
- **Buyer and Seller QSE must confirm trades** — One QSE reports the trade; the other QSE must confirm it for the trade to be valid.

### Day-Ahead Market — Timing

Timeline (day before operating day): **10:00** → **13:30** = DAM window (bids/offers, clearing). **00:00** = start of **Operating Day** (physical delivery). The “Day-Ahead” period runs up to 00:00; the DAM itself runs between 10:00 and 13:30.

### Day-Ahead Market — Transactions

**Inputs:** Bids, Offers, Network Model. **Outputs:** Hourly Awards, Hourly Prices. The DAM clears supply and demand (with network constraints) to set awards and prices for each hour of the operating day.

**Types of Bids (into the DAM):** Energy Bid; PTP Obligation Bid (Point-to-Point, for hedging congestion).

### Day-Ahead Market Point-to-Point (PTP) Obligation Bid

**Submitted between any two Settlement Points.** Each bid specifies Source, Sink, and Bid (MW and $/MW). Examples: 345 kV Hub → Load Zone; Resource Node 1 → Load Zone; Resource Node 2 → Resource Node 3; Resource Node 1 → 345 kV Hub. **Payment or charge is in Real-Time** (settled against RT LMPs).

### Energy Offers — Three-Part Supply Offer

- **Startup Offer** — $/Start (cost to start the unit).
- **Minimum Energy Offer** — $/MWh for the minimum output level.
- **Energy Offer Curve** — $/MWh vs MW (piecewise; marginal cost at each output step).

### Day-Ahead Market Energy-Only Offer

Proposal to **sell energy in the DAM**; offered at **any Settlement Point**. Supply curve: $/MWh vs MW (upward-sloping). Creates a **financial obligation in Real-Time** (settlement against real-time outcomes).

### Day-Ahead Market Energy Bid

Proposal to **buy energy in the DAM**; submitted at **any Settlement Point**. Bid curve: $/MWh vs MW (downward-sloping). Results in **financial credit in Real-Time** (settlement against real-time outcomes).

### Scenario: Forward Market Transactions (e.g. Hour 1500)

**Load teams:** Given load forecast → determine **Bid MWs** and **Bid Price**.  
**Generation teams:** Given MWs to offer → determine **Offer MWs** and **Offer Price**.  
Instructor clears the market; class evaluates hedging "Success."

![Historical Data](Historical-Data.png)

## 4. Energy Settlements

### Energy Settlement in ERCOT

- **Bilateral Trade** — QSEs settle their transactions (between themselves).
- **DAM** — ERCOT settles (Day-Ahead Market clearing).
- **Real-Time** — ERCOT settles (real-time market outcomes).

### Day-Ahead Market Energy Settlement

- **Charge for awarded Energy Bid:** = Awarded MWs × **DASPP**
- **Payment for awarded Energy Offer:** = (−1) × Awarded MWs × **DASPP**  
  **DASPP** = Day-Ahead Settlement Point Price.

### Real-Time Energy Settlement — Real-Time Energy Imbalance

= (−1) × [ SUPPLIES − OBLIGATIONS ] × **RTSPP**  
**RTSPP** = Real-Time Settlement Point Price.

### Real-Time Energy Imbalance Components

= (−1) × [ (Inflows) − (Outflows) ] × **RTSPP**

- **Inflows:** Metered Generation + DAM Energy Purchases + Trade Energy Purchases  
- **Outflows:** DAM Energy Sales + Trade Energy Sales + Metered Load  

Each **Settlement Point** is settled separately.

### DAM Awards & Trades in Real-Time Energy Settlements

- DAM awards and settles **hourly MWs**; Energy Trades are reported as **hourly MWs**.
- Real-Time settles **15-minute MWhs** (four intervals per hour).
- To align: **multiply DAM awards and Trades by ¼ hour** to get MWh per 15-minute interval.

### Example: Real-Time Energy Imbalance (Interval 0715)

**Setup:** DAM awarded Energy Offer at resource node: Hour 0800, 200 MW, DASPP $25/MWh. Real-Time metered generation in interval 0715: 45 MWh, RTSPP $20/MWh.

**Calculation:**  
= (−1) × [ (Metered Gen + DAM Purchases + Trade Purchases) − (DAM Sales + Trade Sales + Metered Load) ] × RTSPP  
= (−1) × [ 45 MWh − (200 MW × ¼ h) ] × $20/MWh = (−1) × (45 − 50) × 20 = **$100** (imbalance payment).

### Scenario: Energy Settlement

**Load teams** determine settlement using: **Awarded Energy Bid in DAM** and **Adjusted Metered Load in Real-Time**.  
**Generation teams** use: **Awarded Energy Offer in DAM** and **Metered Generation in Real-Time**.

**Example (Hour 1400):**  
- **Load Zone QSE:** DAM awarded bid 100 MW @ DASPP $35/MWh; Real-Time adjusted metered load (four 15-min intervals): 24, 25, 26, 25 MWh at RTSPPs $30, $31, $75, $70/MWh.  
- **Resource Node QSE:** DAM awarded offer 300 MW @ DASPP $35/MWh; Real-Time metered generation: 70, 72, 85, 85 MWh at same RTSPPs.  

Settlement is summarized per interval as **DAM Award** + **Real-Time Energy Imbalance** = **Net**.

**Load Zone QSE** (DAM charge = 100 MW × ¼ h × $35/MWh = $875 per interval):

| Interval | DAM Award | Real-Time Energy Imbalance | Net |
|----------|-----------|---------------------------|-----|
| 1315 | −$875 | (−1)×(25−24)×$30 = −$30 | −$905 |
| 1330 | −$875 | (−1)×(25−25)×$31 = $0 | −$875 |
| 1345 | −$875 | (−1)×(25−26)×$75 = $75 | −$800 |
| 1400 | −$875 | (−1)×(25−25)×$70 = $0 | −$875 |

**Resource Node QSE** (DAM payment = 300 MW × ¼ h × $35/MWh = $2,625 per interval):

| Interval | DAM Award | Real-Time Energy Imbalance | Net |
|----------|-----------|---------------------------|-----|
| 1315 | $2,625 | (−1)×(70−75)×$30 = $150 | $2,775 |
| 1330 | $2,625 | (−1)×(72−75)×$31 = $93 | $2,718 |
| 1345 | $2,625 | (−1)×(85−75)×$75 = −$750 | $1,875 |
| 1400 | $2,625 | (−1)×(85−75)×$70 = −$700 | $1,925 |


## 5. Congestion

![Scenario](Scenario.png)
### Results from a Previous Scenario

In the “Find Dispatch Solution” scenario (345 kV Hub, Load Zone 1100 MW, Resource Nodes 1–3 with their energy offer curves), the **results** show **nodal prices of $40/MWh** at every node: Resource Node 1, Resource Node 2, Resource Node 3, the 345 kV Hub, and the Load Zone. Resource Node 2’s *offer curve* shows 200 MW at **$20/MWh** (its marginal cost at that output).

**Question:** Price for Resource Node 2 — shouldn’t it be $20/MWh?  

No. The **LMP** at a node is the *marginal cost of serving one more MW at that node*, not the generator’s own offer price. With no congestion, all nodes see the same system marginal cost (here $40/MWh). Resource Node 2 is *inframarginal*: it gets the clearing price $40/MWh for its output even though its offer is $20/MWh; the “extra” ($40 − $20) is surplus to the generator.



![Scenario: Clearing with Transmission Constraints](scenario-congestion.png)

### Scenario: Clearing with Transmission Constraints

Same network (345 kV Hub, Load Zone 1100 MW, Resource Nodes 1–3 with the same energy offer curves), but with **transmission limits**:

- **Resource Node 2 → 345 kV Hub:** **100 MW limit**
- **345 kV Hub → Load Zone:** **400 MW limit**

The market clears subject to these constraints; flow on the Hub–Load Zone path is capped at 400 MW, and flow from Node 2 to the Hub is capped at 100 MW. **Dispatch:** Node 2 = 100 MW (at limit), Node 1 = 300 MW, Node 3 = 700 MW (400 from Hub→Load + 700 from Node 3 = 1100 MW load). **LMPs** (marginal cost of serving one more MW at each node, with both limits binding):

| Node | LMP ($/MWh) |
|------|-------------|
| Resource Node 1 | 35 |
| Resource Node 2 | 20 |
| Resource Node 3 | 50 |
| 345 kV Hub | 35 |
| Load Zone | 50 |

Hub and Node 1 see the same price (marginal supply at Hub is Node 1 @ $35). Load Zone and Node 3 see $50 (marginal supply at Load is Node 3 @ $50). Node 2 is below Hub price because its output would increase flow on the binding Hub→Load constraint; its LMP equals its marginal offer ($20).

### Discussion: Real-Time Congestion Costs

Example: a QSE has a **100 MW trade** (purchase at 345 kV Hub, delivery to Load Zone). **DAM prices:** Hub $38/MWh, Load Zone $42/MWh. **Real-Time (RT) LMPs:** Hub $35/MWh, Load Zone $50/MWh. The RT spread (Hub $35 vs Load $50) reflects **real-time congestion**: it is more expensive to deliver power to the Load Zone in real time. Settlement compares **payment at Hub** (for the purchase) and **charge at Load Zone** (for the delivery) in DAM vs RT to get a **net amount** (e.g. congestion cost or surplus).

| Settlement | Payment at Hub | Charge at Load Zone | Net Amount |
|------------|----------------|---------------------|------------|
| DAM | 100 × $38 = $3,800 | 100 × $42 = $4,200 | $4,200 − $3,800 = **$400** |
| RT | 100 × $35 = $3,500 | 100 × $50 = $5,000 | $5,000 − $3,800 = **$1,200** |

In RT the charge at Load Zone is higher ($5,000); net amount = $5,000 − $3,800 = $1,200.

### Example: Hedging Real-Time Congestion Costs — DAM Point-to-Point (PTP) Obligations

A **Point-to-Point (PTP) obligation** (e.g. 100 MW from Source to Sink) can hedge congestion: the holder is credited the price difference (Sink − Source) × MW. Using the same prices: **Source** DAM $38/MWh, RT $35/MWh; **Sink** DAM $42/MWh, RT $50/MWh.

| Settlement | Sink minus Source Price | PTP Obligation Amount |
|------------|--------------------------|------------------------|
| DAM | $42 − $38 = **$4/MWh** | 100 × $4 = **$400** |
| RT | $50 − $35 = **$15/MWh** | 100 × $15 = **$1,500** |

The PTP pays the spread; in RT the spread is larger ($15 vs $4), so the obligation is worth more when congestion appears.

**Settlement by type (100 MW, Hub→Load Zone):**

| Settlement Type | Amount |
|-----------------|--------|
| DAM — PTP Obligation | $400 |
| RT — Energy Imbalance | −$1,500 (cost: pay RT spread 100 × $15) |
| RT — PTP Obligation | $1,500 (hedge payment) |
| **Total** | **$400** (DAM PTP; RT nets to $0) |

The RT energy imbalance cost ($1,500) is offset by the RT PTP obligation payment ($1,500), so the PTP hedges the congestion; the net result is the DAM PTP value ($400).

### Scenario: Optimizing with PTP (Node 2, Hub, Load Zone)

| | Resource Node 2 | 345 kV Hub | Load Zone |
|---|-----------------|------------|-----------|
| **DAM SPP** | $36/MWh | $38/MWh | $40/MWh |
| **Average RT SPP** | $15/MWh | $35/MWh | $42/MWh |

QSE position: **100 MW trade sale at Hub**, **100 MW output at Resource Node 2**. Flow: Node 2 → Hub → Load Zone. PTP obligations between these points can hedge the spread risk.

### Point-to-Point Obligations (hourly)

**Hourly financial instruments:** Purchased at the **DAM price spread** (Source–Sink); **settled at the Real-Time price spread**.

![Introducing CRR](Introducing-CRR.png)

### Hedging Congestion Costs Longer Term — Congestion Revenue Rights (CRRs)

**Congestion Revenue Rights (CRRs)** are **monthly** financial instruments: **purchased at auction price**, **settled at the DAM price spread** (Source–Sink). They hedge congestion over longer horizons than hourly PTPs.

**Two types of CRR instruments:**

- **Point-to-Point Obligation** — *Payment or charge in DAM* (holder can receive or pay depending on the spread).
- **Point-to-Point Option** — *Payment only in DAM* (holder receives when the spread is favorable; no charge when unfavorable).

### Example: Congestion Revenue Rights — Point-to-Point Obligations

Network: **345 kV Hub** (DAM $38/MWh), **Resource Node 3** (DAM $42/MWh), **Load Zone** (DAM $42/MWh). **CRR1:** 100 MW Hub → Load Zone. **CRR2:** 100 MW Resource Node 3 → Hub (Source = Node 3, Sink = Hub). CRRs settle at DAM spread (Sink − Source).

| Settlement | Sink minus Source Price | CRR Amount |
|------------|--------------------------|------------|
| CRR1 | $42 − $38 = **$4/MWh** | 100 × $4 = **$400** |
| CRR2 | $38 − $42 = **−$4/MWh** | 100 × (−$4) = **−$400** |

### Example: Congestion Revenue Rights — Point-to-Point Options

Same network and DAM prices. For **PTP Options**, the holder receives payment only when the spread is positive (no charge when negative).

| Settlement | Sink minus Source Price | CRR Amount |
|------------|--------------------------|------------|
| CRR1 | $42 − $38 = **$4/MWh** | 100 × $4 = **$400** |
| CRR2 | $38 − $42 = **−$4/MWh** | **$0** (option does not pay when spread ≤ 0) |

CRR1 has positive spread, so the option pays $400. CRR2 has negative spread, so the option pays $0 (no charge).

### Acquiring Congestion Revenue Rights — CRR Auction Transactions

**Inputs:** Bids, Offers, Network Model → **CRR Auction** → **Outputs:** Awards, Prices. Same structure as the DAM: participants submit bids/offers; the auction clears subject to the network model and produces CRR awards and clearing prices.

### CRRs Are Auctioned By

- **Time-of-Use Blocks** — CRRs are offered in blocks defined by time of use.
- **One-month strips** — Monthly products.

**Time-of-Use Blocks (example):** Off-Peak (0100–0600) and Off-Peak (2300–0000) apply all week; **Peak Weekday** (0700–2200) Mon–Fri; **Peak Weekend** (0700–2200) Sat–Sun.

### Discussion: Congestion Costs Hedging — The Big Picture

**Timeline:** CRR Auction → Day-Ahead Market → Real-Time.

- **Congestion Revenue Rights (CRRs):** Acquired at the **CRR Auction**; settled at the **DAM** price spread (Source–Sink). Involves **CRRAH** (Congestion Revenue Right Account Holder).
- **Point-to-Point (PTP) Obligations:** Entered in the **Day-Ahead Market**; settled at the **Real-Time** price spread. Involves **QSEs** in Real-Time.

So: CRRs hedge congestion over a longer horizon (auction → DAM settlement); PTP obligations hedge from DAM through Real-Time (DAM → RT settlement).

## 6. Ancillary Services

### Real-Time Dispatch Review

**Security Constrained Economic Dispatch (SCED):** Matches generation with demand; manages congestion; achieves least-cost dispatch. Balances **reliability** and **economics**. **Base points** are determined every **5 minutes**.

### Discussion: Is five-minute dispatch enough?

Discussion topic: whether **5-minute** SCED dispatch frequency is sufficient for the system (e.g. given load and resource changes, the 345 kV Hub / Load Zone / resource-node topology, and the need to balance reliability and economics). The meter at “60” in the slide can represent a 60-second or other time scale for comparison.

### Introducing Ancillary Services — Regulation Service

**Regulation Service** (a key ancillary service):
- **Matches generation with demand** — fine-tuning output to balance the system.
- **Responds to frequency deviations** — e.g. target **60 Hz**; **Regulation Up** (increase generation) and **Regulation Down** (decrease generation) to correct deviations.

Regulation is deployed continuously within **5-minute** intervals around **base points** (the SCED-determined targets); resources move up and down from base to follow frequency and balance load.

### Responsive Reserve Service

**Responsive Reserve Service** is another ancillary service. **Possible uses:** **Loss of generation** (e.g. unit trip); **large load-ramps** (fast changes in demand). Resources are held in reserve and can respond quickly (e.g. within minutes) to restore balance or frequency (e.g. when frequency drops below 60 Hz, as suggested by a reading like 59.983).

### ERCOT Contingency Reserve Service

**ERCOT Contingency Reserve Service** has a **10-minute** response requirement. **Possible uses:** **Restoring Responsive Reserve** (replenish responsive reserve after it is deployed); **large renewable ramps** (manage fast changes in wind/solar output).

### Non-Spinning Reserve Service

**Non-Spinning Reserve Service** has a **30-minute** response requirement. **Possible uses:** **Larger load than expected**; **local transmission issues**. Resources are not required to be online (spinning) and can be committed and deployed within the 30-minute window.

### Ancillary Services Acquired Mostly in DAM

Ancillary services are procured mainly in the **Day-Ahead Market**: **Inputs** — Bids, Offers, Network Model → **DAM** → **Outputs** — Awards, Prices.

**Types of offers (into the DAM):**
- **Three-Part Supply Offer** — Startup, minimum energy, incremental energy.
- **DAM Energy-Only Offer** — Energy only, no ancillary component.
- **Ancillary Service (AS) Offer** — Offer to provide regulation, reserves, or other AS.

### Ancillary Service Offers — Resource-Specific Offers for Each Service

Each service is offered in **MW** and **$/MW**:

| Type of Service | Offer |
|-----------------|-------|
| Regulation Up | MW, $/MW |
| Regulation Down | MW, $/MW |
| Responsive Reserve | MW, $/MW |
| Contingency Reserve | MW, $/MW |
| Non-Spinning Reserve | MW, $/MW |

**Multiple offers from a single resource:** A resource can offer **multiple ancillary services**; AS offers **may be combined with energy offers**.

### Economics and Day-Ahead Market Operations — Co-Optimization

**Energy and Ancillary Services are co-optimized** in the DAM. A single clearing uses **Bids** (demand, downward-sloping in $/MWh vs MW) and **Offers (Energy and AS)** (supply, upward-sloping). The **intersection** of the bid and offer curves is the **Solution** (clearing price and quantity). The **optimized value** is the total value from the market outcome at that solution.


## 7. System Capacity

**ERCOT dispatches Generation to follow Demand.** Both **Generation Output** and **System Demand** operate within **System Capacity**. Demand is driven by factors such as the **hourly load forecast**; ERCOT adjusts generation output (via SCED and commitment decisions) so that supply tracks demand within the system’s capability.

### Two Needs for Capacity

Within **System Capacity** (Generation Output), capacity is split into: (1) **Available for Energy Dispatch** — used to serve load; (2) **AS Capacity** — reserved for **Ancillary Services** (regulation, reserves). **System Demand** (e.g. from the **hourly load forecast**) is met from the energy-dispatch portion; the remainder supports AS and reserves.

### Expected System Capacity — Current Operating Plan (COP)

**Current Operating Plan (COP)** = **Anticipated resource operating conditions**. It includes **Resource Status** (e.g. ON, OFF, OUT), **Resource Limits**, and **Ancillary Service Commitments**. **Resource QSEs must maintain a COP for each hour of the next 7 days.**

![Discussion: What if not enough generators plan to run?](What-if-Scenario.png)



### Reliability Unit Commitment (RUC)

When not enough generators plan to run, **Reliability Unit Commitment (RUC)** is used to commit additional units. **RUC ensures:** (1) **Enough capacity to serve the forecasted load**; (2) **Capacity in the right locations** (so that power can be delivered where demand is). It addresses the “what if” scenario where voluntary market outcomes would leave the system short of capacity or poorly located.

**RUC process:** **Inputs** — Offers, Current Operating Plans (COPs), Forecasted Conditions, Network Model → **RUC** → **Outputs** — **Resource Commitments** (units committed to run) or **Nothing** (units not committed).

![Timeline](Timeline.png)

## 8. Load forecasting

**Load forecasting** is the process of predicting **system demand** (MW) and often **load by location** (e.g. zone or node) over future time horizons. It is central to **day-ahead scheduling**, **real-time dispatch**, **unit commitment**, **RUC**, and **congestion** and **price** outlooks in ERCOT.

### Why load forecasting matters in ERCOT

- **Day-Ahead Market (DAM):** Participants and ERCOT use **load forecasts** to form **bids** (demand) and **offers** (supply). The **hourly load forecast** drives how much energy is scheduled and at what locations; errors in load affect **clearing prices** and **schedules**.
- **Real-time operations:** **Load** must be balanced in **real time**. **Short-term load forecasts** (e.g. next hour, next 5–15 minutes) feed **SCED** and **state estimation** so that generation and reserves are deployed to follow actual demand.
- **Reliability and RUC:** **RUC** uses **forecasted load** (and reserve requirements) to decide whether to **commit** additional units. Under-forecasting load can lead to **shortfalls**; over-forecasting can lead to **excess commitment** and **suppressed prices** (as noted in the Reliability Deployment Price Adder discussion).
- **Congestion and LMP:** **Load** is a key driver of **power flows** and **constraint binding**. **Nodal or zonal load forecasts** support **congestion** and **LMP** outlooks and **CRR/FTR** valuation.

### Typical inputs and drivers

- **Weather:** **Temperature** (cooling and heating degree days), **humidity**, and sometimes **wind speed** or **solar irradiance** (for load correlation or behind-the-meter solar). In Texas, **summer peak** load is strongly driven by **air conditioning**.
- **Calendar and time:** **Hour of day**, **day of week**, **month**, **holidays**, **season** — load has strong **daily** and **seasonal** patterns (e.g. morning ramp, evening peak, weekend vs weekday).
- **Economic and behavioral:** **Industrial** activity, **special events**, **COVID-style** demand shifts; **demand response** or **conservation** events can step-change load.
- **Historical load:** **Past** system and nodal load (and forecast errors) are used to **calibrate** and **validate** models.

### Forecast horizons

- **Long-term (years):** Planning (transmission, generation, resource adequacy); often **scenario-based** or **growth** models.
- **Medium-term (days to weeks):** **Unit commitment**, **RUC**, **week-ahead** scheduling; **hourly** or **sub-hourly** load by zone/node.
- **Short-term (hours to minutes):** **Day-ahead** and **real-time** operations; **hourly load forecast** for the DAM, **rolling** short-term (e.g. next 1–6 hours, or next 5–15 minutes) for **SCED** and **reserve** deployment.

### Methods (brief)

- **Statistical:** **Time series** (e.g. ARIMA, SARIMAX) with **seasonality**; **regression** of load on **temperature**, **hour**, **day type**; **similar-day** or **analog** methods (e.g. load from a similar weather/day in the past).
- **Machine learning:** **Tree-based** (random forest, gradient boosting) or **neural networks** with **weather**, **calendar**, and **lag** features; sometimes **LSTM** or other **sequence** models for **multi-step** forecasts.
- **Hybrid:** **Ensemble** of statistical and ML; **post-processing** (bias correction, smoothing) using **historical errors** or **weather updates**.

### ERCOT-specific notes

- **Hourly load forecast** is published and used in **market** and **reliability** processes; **nodal** or **zonal** load may be used for **network** and **congestion** analysis.
- **Forecast error** affects **imbalance** (actual load vs scheduled), **real-time** prices, and **reserve** deployment; **over-** or **under-forecasting** can shift **System Lambda** and **RUC** outcomes.
- **Extreme weather** (heat waves, cold snaps) drives **peak** load and is often the hardest to forecast; **stress** and **scenario** analysis use **high-load** or **extreme-weather** load assumptions.

### Short summary

**Load forecasting** predicts **system and locational demand (MW)** over various horizons. It is an essential input to the **DAM**, **real-time dispatch (SCED)**, **RUC**, and **congestion/LMP** analysis. **Inputs** include **weather** (especially temperature), **calendar**, and **historical load**; **methods** range from **statistical** (time series, regression) to **ML** (GBM, neural nets). In ERCOT, **hourly load forecast** drives scheduling and commitment; **forecast error** influences **prices**, **reserves**, and **reliability**.

## Summary

### Market Information System (MIS) Data Access

Three levels of data access:

- **MIS PUBLIC** — Also available on ercot.com; publicly accessible.
- **MIS SECURE** — Available to all Market Participants (login/credentials required).
- **MIS CERTIFIED** — Available to specific Market Participants (certification or specific authorization required).

![Summary](Summary.png)
