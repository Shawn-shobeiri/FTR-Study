<!-- LaTeX: use Markdown Preview Enhanced (Open in Browser) or export to HTML with MathJax so formulas render. Currency uses \$. -->
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

## Texas power system & ERCOT – 20‑min review bullets

*To view LaTeX formulas: use **Markdown Preview Enhanced** (right‑click → Open in Browser) or export to HTML with MathJax.*

### 1. ISO / RTO and ERCOT basics

- **ISO vs RTO**
  - **ISO (Independent System Operator)**: runs the **bulk power system** (reliability, dispatch) for a region; may or may not operate markets.
  - **RTO (Regional Transmission Organization)**: an ISO that also runs **regional wholesale markets** (DA/RT energy, congestion, sometimes capacity & AS) under **FERC Order 2000**.
  - **Key distinction:** an RTO is an ISO **with organized markets and broader regional scope**; an ISO might just handle reliability/dispatch.
- **Who are the ISOs/RTOs**
  - **US ISOs/RTOs (7):** `CAISO`, `ERCOT`, `ISO‑NE`, `MISO`, `NYISO`, `PJM`, `SPP`.
  - **Canada (2):** `AESO`, `IESO`.
  - Together, they serve ~**two‑thirds of US demand** and over half of Canada’s population.
- **ERCOT’s special status**
  - **ERCOT** is an ISO that operates **Texas’s grid & markets**, but is **not FERC‑certified as an RTO** because it is largely **intrastate** and sits outside the Eastern/Western interconnections.
  - **PUCT** (Public Utility Commission of Texas) oversees ERCOT; both operate within Texas legislation.
  - ERCOT has **no synchronous AC ties** to the Eastern/Western interconnects (only limited DC ties).
- **ERCOT’s core responsibilities**
  - **Balance supply and demand in real time**, maintaining frequency around **60 Hz**.
  - Ensure **transmission limits** are respected so lines and interfaces do not overload.
  - Run a **competitive nodal wholesale market** where prices clear through a **market clearing process**.
  - **Plan** and coordinate transmission and generation expansion (transmission projects, interconnections).

### 2. Market participants and long‑term contracts

- **Key market participants**
  - **Resource Entities (REs):** generators and some controllable loads that produce or absorb power.
  - **Load Serving Entities (LSEs):** serve end‑use customers (retail providers, co‑ops, NOIEs).
  - **Qualified Scheduling Entities (QSEs):** represent REs and LSEs in the market.
    - Submit **bids and offers** (energy and AS) to ERCOT.
    - Provide **operational information** to ERCOT.
    - **Financially settle** with ERCOT and with the Resource Entities / LSEs they represent.
  - **Transmission Service Providers (TSPs):** own/operate transmission.
- **Long‑term power contracts**
  - **For generators:** provide **revenue certainty**, reduce exposure to spot price volatility, and support **project finance**.
  - **For consumers/LSEs:** provide **stable, predictable power prices**.
  - In ERCOT (no capacity market), **PPAs and other long‑term contracts are critical** to support investment, because generators are **only paid for energy** (and AS), not “being available” via a capacity payment.
- **PPAs and financial vs physical**
  - **PPA:** RE sells power to an LSE at an agreed price/tenor (often fixed or structured).
  - **Physical flows:** even with a PPA, physical power is dispatched according to **ERCOT’s dispatch and network physics**, not along the contract path.
  - **Settlement:** contract is settled **financially**; congestion and locational price differences are handled by LMPs and **CRRs/FTRs**.
- **CRRs (Congestion Revenue Rights)**
  - Designed to **hedge congestion risk** between two settlement points (source → sink).
  - Also used for **speculation** on **locational price differences** that arise when the network is constrained.

### 3. LMP, System Lambda, constraints, and congestion

- **Locational Marginal Price (LMP)**
  - In a **nodal market**, prices differ by location (node / settlement point).
  - **Definition:** value of producing one **additional MWh at a given node**, considering **system‑wide marginal energy cost**, **congestion**, and **losses**.
- **System Lambda (λ)**
  - **System‑wide marginal energy cost**: the cost of procuring the next cheapest MWh across the system (ignoring location).
  - At each node, **LMP = λ + congestion component + loss component**.
  - Intuition: λ is the **energy price** if there were **no network constraints or losses**.
- **How System Lambda is set (merit order / supply stack)**
  - Generation is dispatched in **merit order**: **cheapest marginal cost first**.
  - The **supply stack** orders resources from lowest to highest \\$/MWh (e.g. wind, solar, nuclear, coal, gas).
  - **Demand (MW)** intersects this stack at a **marginal unit**; that unit’s marginal cost is **System Lambda**.
  - Example: low demand → coal marginal; higher demand or less low‑cost capacity → gas marginal → higher λ.
- **Constraints and congestion**
  - A **constraint** is a line/interface limit (MW) due to **thermal**, **stability**, or **operational** reasons.
  - When flow on a constraint **hits its limit**, it is **binding** and affects dispatch and LMPs.
  - **Congestion:** when part of the network is overloaded or at risk; power cannot flow freely, so **LMPs diverge from λ** across nodes.
  - **No congestion case:** network unconstrained → **LMP = λ everywhere**, no locational spreads, no congestion rent.

### 4. Shift factors, shadow prices, and LMP formula

- **Shift Factor (SF)**
  - Measures how a 1 MW **injection/withdrawal** at a node affects **flow on a specific constraint**.
  - **ΔFlow (MW) = ΔOutput (MW) × SF**.
    - Example: SF = 0.5, +10 MW output → +5 MW on the line.
  - Used to quantify how **generation changes relieve or worsen** congestion and to measure **FTR/CRR exposure** to each constraint.
- **Shadow Price (SP)**
  - **SP of a constraint**: \$/MW cost of relaxing that constraint by 1 MW (cost of redispatch).
  - Sets the **congestion component** of LMPs and underpins **congestion rents** that CRRs/FTRs hedge.
- **LMP decomposition**
  - At a node for a single binding constraint:
    - **LMP = λ − SP × SF** (sign convention: nodes that **worsen** the constraint get **lower** prices; nodes that **relieve** it get **higher** prices).
  - **Positive SF:** injection increases flow → LMP below λ.
  - **Negative SF:** injection reduces flow → LMP above λ.
  - The **spread between two nodes** on opposite sides of a constraint equals **SP × (SF_difference)** and is what FTRs/CRRs pay or receive.
- **Multiple constraints**
  - ERCOT repeats this calculation for **all binding constraints** and **all settlement points**.
  - LMP at each node sums contributions from **each constraint’s shadow price × shift factor**, then adds losses and λ.

### 5. Nodes, settlement points, and prices in ERCOT

- **Nodes vs settlement points**
  - ~**17,000 nodes** in ERCOT (physical connection points).
  - Just under **900 have unique LMPs**; these are **Settlement Points** where prices and CRR/FTR settlements are defined.
  - **Resource node:** transmission‑connected generator or load with dispatch instructions.
  - **Settlement Point:** node with a unique LMP used for **settlement and trading**.
- **Load zones and trading hubs**
  - ERCOT aggregates settlement points into **load zones** and **trading hubs**, publishing **5‑minute LMPs** for each.
  - Traders commonly reference **hub / zone prices**, but CRRs and granular risk are tied to **node‑level settlement points**.
- **ERCOT trading hubs (all 7)** — Settlement point price (SPP) indices used for trading and CRR path source/sink:
  1. **HB_HUBAVG** — Hub Average (system-wide hub average)
  2. **HB_BUSAVG** — Hub Bus Average
  3. **HB_HOUSTON** — Houston Hub
  4. **HB_NORTH** — North Hub
  5. **HB_PAN** — Panhandle Hub
  6. **HB_SOUTH** — South Hub
  7. **HB_WEST** — West Hub  
  CRR paths and PTP obligations are often specified between these hubs (or between hub and load zone); SPPs are published for each (e.g. in ERCOT NP6-905-CD, DAM/RT SPP reports).

### 6. Day‑Ahead Market (DAM), offer curves, and ancillary services

- **Day‑Ahead Market**
  - Participants submit **bids to buy** and **offers to sell** energy and AS for the **next operating day**.
  - DAM clears before the operating day, producing:
    - **Day‑ahead schedules** (MW by hour and location).
    - **Day‑ahead LMPs** at each settlement point.
  - Real‑time market then adjusts for actual demand, outages, and deviations.
- **DAM supply and demand**
  - **Supply:** aggregation of **offer curves** from QSEs (generators).
  - **Demand:** aggregation of **bids** from LSEs/loads.
  - ERCOT clears where **supply meets demand** at each location; in a nodal market this is effectively a **networked market‑clearing optimization**.
- **Offer curves**
  - For each resource, QSEs submit a **price‑quantity step function** (MW vs \\$/MWh).
  - ERCOT stacks these in **merit order** to run economic dispatch and set **System Lambda** and **LMPs**.
  - Offer curves also determine the **cost of redispatch** to relieve constraints, which feeds into **shadow prices** and **congestion costs**.
- **Ancillary Services (AS)**
  - **Purpose:** manage **small and large frequency deviations** and provide **fast‑responding capacity**.
  - Four key ERCOT AS:
    - **Regulation Up / Down:** continuous balancing to keep frequency near **60 Hz**.
    - **Responsive Reserve Service (RRS):** fast response for under‑frequency events (multiple layers at different Hz thresholds).
    - **ERCOT Contingency Reserve Service (ECRS):** reserves for contingencies (e.g. sudden loss of a unit/line).
    - **Non‑Spin:** capacity that can be brought online within a specified time (offline/part‑loaded units).
  - **AS prices** are cleared system‑wide per hour (not locational like energy LMPs).

### 7. Real‑Time Market, SCED, and settlement

- **Real‑Time Market**
  - Balances **actual** supply and demand when conditions differ from the DAM schedule.
  - Generation and load can **update offer and bid curves** up to an hour before each operating hour.
  - Dispatch and pricing are determined every **5 minutes**.
- **SCED (Security‑Constrained Economic Dispatch)**
  - Core algorithm that:
    - Takes **real‑time bids/offers**, **network constraints**, **frequency**, and **forecasted changes** in load/gen.
    - Solves for the **least‑cost dispatch** that respects all constraints.
  - Runs every **5 minutes**, issuing **base points** (MW targets) to resources and producing **5‑minute LMPs**.
- **State estimation and contingency analysis**
  - Every 5 minutes ERCOT:
    - Runs **State Estimation** to build a consistent view of voltages, angles, and flows.
    - Runs **Contingency Analysis** (N‑1, etc.) to identify potential constraints that may bind if an element trips.
    - Then runs **SCED** using this base‑case and set of binding/monitored constraints.
- **Settlement**
  - Dispatch occurs in **5‑minute SCED intervals**.
  - Settlement typically uses **15‑minute intervals**, with the settlement price being the **average of three 5‑minute LMPs** in that window.

### 8. Price adders in ERCOT

- **System Reserves and ORDC price adder**
  - **System reserves:** available capacity not currently generating (headroom).
  - When reserves are low (e.g. **< 7 GW**), ERCOT applies a **scarcity price adder** using the **Operating Reserve Demand Curve (ORDC)**.
  - As reserves decline, the adder **increases**, reflecting the rising value of additional capacity.
  - At very low reserves (e.g. **≤ 3 GW**), prices can reach the **system‑wide offer cap** (currently **\$5,000/MWh**, set by PUCT).
  - This adder applies to **all LMPs system‑wide** when non‑zero.
- **Reliability Deployment Price Adder (RUC‑related)**
  - When ERCOT commits resources **out‑of‑market** via **RUC (Reliability Unit Commitment)**, it can distort supply/demand in the energy market.
  - The **Reliability Deployment Price Adder** recovers costs from these reliability actions and adjusts market prices accordingly.
  - Calculated as the difference between **λ without RUC** and **λ with RUC**; most of the time this is **\$0/MWh**.
  - Also applies system‑wide to all LMPs when non‑zero.

### 9. Supply stack modeling

- **Concept**
  - **Supply stack modeling** represents how wholesale power prices are set by **stacking generation from cheapest to most expensive** and intersecting with **demand**.
  - The intersection gives the **marginal unit** and its **marginal cost**, which is **System Lambda** (before congestion and losses).
- **How to build a stack**
  - Define **capacity and marginal cost** (\\$/MWh) for each resource/segment (wind, solar, nuclear, coal, gas, etc.).
  - Sort all resources by **increasing cost** and form a **cumulative capacity curve**.
  - For a given **demand level**, find where it hits the curve → read off the **marginal price**.
  - Run **sensitivities**: change demand, remove capacity (outages), or shift fuel/offer prices to see new λ and marginal fuel.
- **Use cases**
  - **Price formation & intuition:** understand which fuel is on the margin and why prices are high/low.
  - **Scenario / stress testing:** high‑demand days, low wind/solar, outages, fuel price shocks.
  - **Margin analysis:** link to **spark/dark spreads** and unit profitability.
  - **Limitations:** single‑node stack explains **energy price**; **congestion and losses** explain **locational spreads** on top.

### 10. Heat rate – efficiency and marginal cost

- **Definition and units**
  - **Heat rate** = **fuel input energy per MWh of electricity output** (e.g. **MMBtu/MWh**).
  - Lower heat rate = **more efficient**; higher = **less efficient**.
  - Rough benchmarks:
    - CCGT: ~**7–8 MMBtu/MWh**.
    - Gas peaker: ~**10–11 MMBtu/MWh**.
    - Coal: ~**9–10 MMBtu/MWh** (varies).
- **Gross vs net heat rate**
  - **Gross:** based on total electrical output (before internal use).
  - **Net:** based on net output to the grid; used for **costing and offers**.
- **Link to marginal cost and offers**
  - **Marginal fuel cost (\\$/MWh)** ≈ **fuel price (\$/MMBtu) × heat rate (MMBtu/MWh)**.
  - This drives a unit’s **position on the supply stack** and whether it is **marginal**.
  - Many generators construct offers as **fuel cost + margin**, so accurate heat rate is key.
- **Modeling heat rate**
  - **Constant heat rate** per technology: simple screening model.
  - **Unit‑level heat rate**: use plant‑specific data for more accurate stacks and valuation.
  - **Load‑dependent heat rate curves**: efficiency worsens at low output → model **incremental** heat rate vs MW to capture realistic marginal cost.
- **ERCOT relevance**
  - ERCOT often has **gas on the margin**, so **gas price × gas unit heat rate** is crucial to λ.
  - Proper heat‑rate modeling is essential for **spark spread**, **plant margins**, **hedging**, and **stress tests** when gas prices move.

### 11. Spark spread and dark spread

- **Spark spread (gas)**
  - **Formula:** Spark spread = **power price (\\$/MWh)** − (**gas price (\$/MMBtu) × heat rate (MMBtu/MWh)**).
  - Interpreted as **gross margin per MWh** for a **gas‑fired** plant before non‑fuel costs.
  - **Positive** spark spread: gas plant is **in the money** on a fuel basis.
  - **Key uses:** gas plant valuation, hedging (sell power / buy gas), trading spark‑spread products, risk analysis.
- **Dark spread (coal)**
  - **Formula:** Dark spread = **power price (\\$/MWh)** − **coal fuel cost per MWh**.
  - Coal fuel cost per MWh = (coal price \$/ton) × (heat rate / coal heat content).
  - Measures **gross margin per MWh** for a **coal‑fired** plant.
  - More prominent in coal‑heavy markets (e.g. PJM, MISO); ERCOT is more **gas‑dominated**.
- **Clean spreads**
  - In regions with **carbon pricing**, add **CO₂ cost per MWh** to variable cost:
    - **Clean spark spread** = power − gas × HR − CO₂ cost.
    - **Clean dark spread** = power − coal cost/MWh − CO₂ cost.
- **Modeling and risk**
  - Inputs: **LMP/hub power price**, **fuel prices**, **heat rates**.
  - Analyze as **time series** for distribution, % of time positive, and behavior in **stress events**.
  - Sensitivities: +\$1/MWh power → +\$1/MWh spark; +\$1/MMBtu gas → −(HR) \$/MWh spark.
  - Directly tied to the **supply stack**: positive spreads indicate units that are above their marginal fuel cost at the current λ.

---

## ERCOT Wholesale Market 101 – 10‑min review

### 1. Introduction — timeline and entities

- **Two phases:** **Day-Ahead** (market/commitments before 00:00); **Operating Day** (physical delivery, real-time dispatch from 00:00).
- **Key times:** **10:00** DAM starts; **13:30** DAM past; **18:00** start of **Adjustment Period** for each operating hour (ends 1 hour before that hour); **Hour Ahead** runs until the operating hour begins.
- **Entities:** **LSE** (Load Serving Entity), **QSE** (Qualified Scheduling Entity), **RE** (Resource Entity), **TSP**, **DSP**, **ERCOT**, **Independent Market Monitor**, **PUCT**.
- **Economics:** **Bids** = demand (downward-sloping \\$/MWh vs MW); **Offers** = supply (upward-sloping). **Intersection** = clearing price and quantity. Some processes **optimize value** (bid/offer intersection); others **optimize cost** (meet required MW at least cost by stacking offers).

### 2. Real-time dispatch and SCED

- **Goals:** Reliability; match generation with demand; keep flows within limits; **least-cost** dispatch.
- **SCED (Security Constrained Economic Dispatch):** **Inputs** — Offers, System Conditions, Network Model. **Outputs** — **5‑minute Base Points** (dispatch instructions), **5‑minute Prices** (LMPs). Runs every **5 minutes**.
- **Energy offer curve:** Monotonically increasing; up to **10** price/quantity pairs; prices between **−\$250** and **SWCAP** (System-Wide Offer Cap).
- **LMP** at a node = **marginal cost of serving one more MW at that node** (not the generator’s offer price). With **no congestion**, all nodes can see the **same** LMP; **inframarginal** generators receive the clearing price.

### 3. Forward markets — DAM and bilaterals

- **DAM:** Centralized; **Bids** and **Offers** + Network Model → **Hourly Awards**, **Hourly Prices**. **PTP Obligation Bids** (Point-to-Point) hedge congestion between two settlement points (Source, Sink).
- **Bilateral trades:** **QSE-to-QSE**; transfer **settlement responsibility**; **buyer and seller QSE must confirm**.
- **Energy offers (DAM):** **Three-part** — Startup Offer (\$/Start), Minimum Energy Offer (\\$/MWh), Energy Offer Curve (\\$/MWh vs MW). **Energy-only** offer = sell energy at a settlement point; creates **financial obligation in Real-Time** (settled against RT). **Energy bid** = buy; creates **financial credit in Real-Time**.

### 4. Energy settlements

- **Three settlement types:** **Bilateral** (QSEs between themselves); **DAM** (ERCOT: awards × DASPP); **Real-Time** (ERCOT: imbalance × RTSPP).
- **DAM:** Charge for awarded **Energy Bid** = Awarded MW × **DASPP**. Payment for awarded **Energy Offer** = (−1) × Awarded MW × **DASPP**.
- **Real-Time Energy Imbalance** = (−1) × [ SUPPLIES − OBLIGATIONS ] × **RTSPP**. **Inflows:** Metered Gen + DAM Purchases + Trade Purchases. **Outflows:** DAM Sales + Trade Sales + Metered Load. Settled per **Settlement Point**; RT uses **15‑minute** intervals (DAM awards in MW → multiply by ¼ h for MWh per interval).

### 5. Congestion — LMPs, PTP, CRRs

- **With transmission limits:** Binding constraints → **nodal LMPs differ**. LMP at each node = marginal cost of serving **one more MW at that node** (can be below or above a generator’s offer when that generator is constrained).
- **Hedging RT congestion:** **DAM PTP Obligation** (e.g. 100 MW Source→Sink): holder receives **(Sink − Source) × MW** at **RT** (and in DAM). **RT energy imbalance** cost (paying the RT spread) can be **offset** by **RT PTP obligation** payment → PTP hedges congestion.
- **CRRs (Congestion Revenue Rights):** **Monthly** instruments; **auctioned** (bids/offers + network → awards, prices). **Settled at DAM spread** (Sink − Source). **PTP Obligation** = payment or charge in DAM; **PTP Option** = payment only (no charge when spread ≤ 0). **CRRs** hedge **longer term** (auction → DAM); **PTP obligations** in DAM hedge **DAM → Real-Time**.

### 6. Ancillary services

- **Procured mainly in DAM.** **Co-optimized** with Energy: single clearing with **Bids** and **Offers (Energy + AS)** → **Solution** (clearing price and quantity).
- **Types:** **Regulation** (Up/Down — match gen with demand, respond to frequency); **Responsive Reserve** (fast response to loss of gen, load ramps); **ERCOT Contingency Reserve** (e.g. 10‑min response); **Non-Spinning Reserve** (e.g. 30‑min response).
- **AS offers:** Per service, in **MW** and **\$/MW**. A resource can offer **multiple** AS; AS offers **may be combined with energy offers**.

### 7. System capacity and RUC

- **ERCOT dispatches generation to follow demand** within **System Capacity**. Capacity split: **Available for Energy Dispatch** (serve load) and **AS Capacity** (reserves). Demand driven by **hourly load forecast**.
- **COP (Current Operating Plan):** Anticipated resource conditions (status, limits, AS commitments). **QSEs maintain COP for each hour of the next 7 days.**
- **RUC (Reliability Unit Commitment):** When voluntary market leaves **insufficient capacity** (or in wrong locations), **RUC** commits additional units. **Inputs:** Offers, COPs, Forecasted Conditions, Network → **Outputs:** Resource Commitments (or nothing). Ensures **enough capacity for forecasted load** and **capacity in the right locations**.

### 8. Load forecasting (brief)

- **Load forecasting** = predicting **system and locational demand (MW)**. Essential for **DAM** (bids/offers), **real-time** (SCED), **RUC**, and **congestion/LMP** outlooks.
- **Inputs:** **Weather** (temperature, humidity), **calendar** (hour, day, season), **historical load**. **Horizons:** long-term (planning), medium-term (UC/RUC), short-term (DAM hourly, rolling for SCED).
- **ERCOT:** **Hourly load forecast** drives scheduling and commitment; **forecast error** affects **imbalance**, **prices**, and **reserves**; **extreme weather** drives peak and is hardest to forecast.

---

## CRR (Congestion Revenue Rights) – 30‑min review

*Source: CRR.md. Focus: ERCOT CRR market — fundamentals, auction & allocation, trading, credit, settlements. Brief CAISO comparison at end.*

### 1. Audience and objectives

- **Audience:** CRR Account Holders, NOIEs (pre-assigned CRRs), QSEs (DAM PTP Obligations). **Course goals:** Participate in CRR market; explain auction, trades, credit; describe financial settlement and outcomes.

### 2. Fundamentals — What are CRRs?

- **Definition:** **Congestion Revenue Rights** are **financial instruments** that entitle the owner to a **payment or charge** when the grid is congested in the **Day-Ahead Market**. They give rights to (a share of) **Congestion Rent**. **Not** a right to deliver physical energy or use physical transmission — **purely financial**.
- **Uses:** (1) **Financial hedge** — lock in congestion cost; pay upfront to hedge exposure from energy positions. (2) **Financial investment** — speculative; profit when Congestion Rent received > CRR purchase price.
- **Settlement points:** All energy settled at **Resource nodes**, **Load zones**, or **Hubs**. Each has its own **Settlement Point Price (SPP)**; variation across points = congestion exposure = what CRRs hedge.

### 3. Types of CRRs and acquisition

- **All ERCOT CRRs are Point-to-Point (PTP):** **Source** (injection) and **Sink** (withdrawal); both **Settlement Points**. **Settlement** = (Sink SPP − Source SPP) × MW.
- **PTP Option:** **Payment only** (never a charge). Value per hour = Sink SPP − Source SPP; if **negative → \$0**. Hedge that can only pay.
- **PTP Obligation:** **Payment or charge**. Same formula; if negative → owner **pays**. Full two-way exposure.
- **Acquiring CRRs:** (1) **CRR Auction** (most CRRs); (2) **Allocation** (Pre-Assigned CRRs to NOIEs); (3) **Bilateral trades** (between CRR Account Holders).
- **CRR Account Holder:** Must **register and qualify** to own CRRs (application, bank info, capability, **creditworthiness**). Only CRR Account Holders may own CRRs.
- **DAM PTP Obligations:** Bought **in the Day-Ahead Market** (at DAM spread), **settled in Real-Time** (at RT spread). Hedge **RT congestion** or DAM→RT change. **Only QSEs** can buy DAM PTP Obligations.

### 4. LMP, congestion, and Congestion Rent

- **LMP** = cost to serve **next increment of load at a bus**. **Components:** **energy** (system marginal cost) and **congestion** (locational adjustment). No congestion → same price everywhere; with congestion → prices differ.
- **ERCOT:** Losses **not** in LMPs (reflected via adjusted metered load).
- **Congestion rent:** With congestion, **charges to buyers > payments to sellers** → **surplus** = **Congestion Rent**. In ERCOT, **DAM Congestion Rent funds CRR payments**.
- **Congestion cost exposure:** Load (pays more at load zone) and resources (lost opportunity when node price is low). Exposure in DAM or RT; **CRRs** are the main hedge.

### 5. Settlement Point Prices (SPPs)

- **SPPs** are **calculated from LMPs**: **Resource node** = time-weighted average of LMPs; **Load zone** = time- and **load-weighted** average; **Hub** = time- and **simple** average of hub buses. **RT:** 15‑min SPPs from 5‑min LMPs. **DAM:** hourly; **CRRs are cashed out in the DAM** using DAM SPPs.

### 6. CRR life cycle

- **Allocation** (PCRRs to NOIEs) → **before** CRR Auction. **CRR Auction** (bids to buy, offers to sell) → **monthly** and **semi-annual (Long-Term)**. **CRR Trades** (bilateral) → transfer ownership. All CRRs (auction, allocation, trade) → **settled daily in the Day-Ahead Market**. **DAM PTP Obligations** (bought in DAM by QSEs) → **settled in Real-Time** for the next operating day.

### 7. Availability and capacity caps

- **Monthly auction:** **90%** of transmission capacity available for CRRs (10% headroom for unplanned outages).
- **Long-Term Auction Sequence (four six-month periods):** **60%** (1st period), **45%** (2nd), **30%** (3rd), **15%** (4th) of capacity — cumulative with prior periods. Example: if long-term already used 50%, monthly has **40%** left (90% − 50%).
- **Pre-Assigned CRRs (PCRRs):** Allocated to **NOIEs** (municipal utilities, electric cooperatives, non–retail-competition) with **long-term supply contracts prior to Sept 1, 1999**. **Cost:** 5–20% of auction clearing price depending on contract. **Allocation before auction** → NOIEs have **first rights** to capacity; **remaining** capacity goes to auction.
- **Simultaneous Feasibility Test (SFT):** **DC power-flow** model checks that awarded CRRs (injections/withdrawals at settlement points) **respect transmission limits**. Used **during allocation** (validate PCRRs) and **prior to each DAM** (feasibility for operating day).

### 8. CRR Auction — inputs and structure

- **Inputs:** **Bids** (buy), **Offers** (sell), **CRR Model** (allocated CRRs, previously awarded CRRs, **credit limits**). **Constraints:** transmission capacity (total minus allocated/awarded), **credit limit per CRR Account Holder** (budget).
- **Bids:** **Not-to-Exceed Price** (\$/MW), **Max MW**, **path** (Source, Sink), **Time-of-Use Block**. **Hedge type:** OPT (Option) or OBL (Obligation). PTP Option bid price must be **> 0**; PTP Obligation **may be negative**. **Bid cap:** 300,000 total bids; per Account Holder = 300,000 / number of qualified Account Holders.
- **Offers:** **Minimum Reservation Price**, **MW** (on specific path/TOU). **Only owner** can offer; must have acquired CRR (auction, trade); NOIE may offer allocated PCRRs. **Validation:** cannot offer more MW than owned.
- **Strips and TOU:** CRRs are **one-month strips** in **Time-of-Use blocks**. **Three TOU blocks:** **Peak Weekday** (0700–2200 Mon–Fri excl. holidays), **Peak Weekend** (0700–2200 Sat/Sun/holidays), **Off-Peak** (0100–0600, 2300–2400 every day).
- **7×24 block bid (monthly only):** Bid for **all three TOU blocks** on a path for the month — **all or nothing**. Awarded if **Bid Price ≥ hour-weighted average** of three TOU clearing prices. **Long-Term Auction Sequence:** **no** 7×24 block bids (TOU blocks cleared separately).
- **PTP Option minimum bid:** **\$0.01/MW/hour** (set by TAC). If option clears **below** minimum, **Auction Fee** = difference (total cost to buyer = \$0.01/MW/hour).

### 9. CRR Auction — clearing and outputs

- **Single-round, simultaneous** clearing. **Objective:** Maximize **net auction revenue** = **Bid-based Value − Offer-based Cost**, subject to **transmission limits** and **credit limits**. Clears **highest-priced bids** and **lowest-cost offers** first; **clearing prices** determined **after** award quantities.
- **Outputs:** **Auction results** (MIS Public: awarded holders, paths, TOU, MW, clearing prices, binding constraints; bids/offers **without** holder identity; MIS Certified: per-holder awards and CRR IDs). **Settlements** (invoicing). **Daily data** to Credit and Settlements (ownership, CRR cash-out in DAM).

### 10. CRR Network Model

- **Derived from Network Operations Model**; represents **transmission capacity for the month** (not daily). **Reflects:** (1) facilities **in-service first day** of month; (2) **significant outages** (e.g. ≥5 days, 345 kV, BLT, or substantial congestion risk); (3) **dynamic ratings** (e.g. max forecasted temps for month); (4) **monitored elements** only; (5) **contingencies** that significantly impact congestion; (6) **all valid Settlement Points**.
- **Posted on MIS Secure** before each auction (e.g. **10 business days** before Monthly; **20 business days** before Long-Term Sequence). Used for **auction** and **allocation**; participants use it for **bid/offer strategy**.
- **Transmission capacity:** After **allocation**, **remaining** capacity is **available prior to auction**. After **auction**, up to **90%** of total may be **booked to CRRs** for the month. **DAM:** CRRs settle in DAM → that capacity **frees up** each day for **DAM** (e.g. DAM PTP Obligations, energy); **DAM starts with clean slate** each day.

### 11. Clearing examples and shadow price

- **Simple model:** Settlement points A–F; paths A→B and C→D both use **E–F** (100 MW). **Case 1 (bids only):** Ellen A→B \$20, Jack C→D \$10 → clear Ellen 100 MW (cap), Jack 0. **Case 2 (reversed):** Jack \$20, Ellen \$10 → Jack 20 MW, Ellen 80 MW. **Case 3:** Naomi offers 30 MW E–F @ \$15; optimal = do not clear Naomi; Jack 20, Ellen 50. **Case 4:** Naomi offers 90 MW @ \$15; Jack 20 MW, Naomi 10 MW cleared, Ellen 0; **shadow price = \$15** (marginal cost of one more MW on E–F).
- **Shadow price** = marginal cost to make one more unit of transmission capacity available; depends on bids/offers; sets **clearing prices** for paths using that link.

### 12. Trading of CRRs

- **Trade** = **bilateral** transfer of CRR ownership between **two CRR Account Holders**. **Buy:** must be registered CRR Account Holder. **Sell:** must be qualified and **currently own** the CRR.
- **Tradable:** **PTP Options** and **PTP Obligations** (from auction or trade). **Not tradable:** **PTP Options/Obligations with Refund** (pre-assigned to NOIEs for hedging long-term supply; excess refunded).
- **Parameters:** Source, Sink, MW, Start/End dates, TOU, Hedge Type. **Cannot modify:** Source, Sink, TOU, Hedge Type. **Can modify:** **MW**, **Effective days** (e.g. offer subset of month or days).
- **Process:** **Bulletin board** (post for sale / want-to-buy) → **contact and negotiate** (price bilateral, outside ERCOT) → **seller reports trade to ERCOT** → **buyer confirms** → **ERCOT checks both parties’ credit** → **approved** → **new owner**, **new CRR ID**; ERCOT settles with new owner in DAM going forward.

### 13. DAM PTP Obligation vs virtuals

- **PTP Obligation:** **Two-point** (source, sink); value = **Sink SPP − Source SPP**; **spread/congestion** risk; acquired in **CRR auction**, **bilateral**, or **DAM** (QSE).
- **Virtual:** **Single-point** (buy or sell at one node in DAM); value = **DAM vs RT price** at that node; **timing/location** risk at one point; acquired in **DAM**.

### 14. Credit limits — Counter-Party and ACLC

- **Counter-Party:** Single entity that is QSE and/or CRR Account Holder; **responsible for managing Available Credit** for its QSEs and CRR Account Holders.
- **Available Credit** = (Unsecured Credit + Secured Collateral) − Credit Exposure. **Secured Collateral** = cash, letters of credit, bonds.
- **ACLC (Available Credit Limit for CRR Auction)** = Secured Collateral − CRR Credit Exposure − Secured Collateral consumed by QSE (conceptually). **Counter-Party** may allocate **up to 90% of ACLC** to CRR Account Holders. **Lock credit by bid-window close** for the auction; **self-imposed limit** (lower) optional per Account Holder — **auction will not award** in excess of that limit.
- **Long-Term Sequence:** Credit locked **separately per auction** (each of four) and **per TOU** (each block cleared separately).

### 15. Credit consumption in auction and DAM

- **Consumption** uses **bid/offer prices** (not clearing prices) × **potentially awarded volumes**. **PTP Option bids:** Volume × Bid price. **PTP Obligation offers:** Volume × Min(0, Offer price) (only if offer negative). **PTP Obligation bids:** Volume × (Bid price + **Path-Specific Adder**). **Path-Specific Adder** (e.g. **Aci99**): from **99th percentile lower bound** of historical DAM price distribution (3-year look-back) for that path/TOU — reflects risk on obligation.
- **AOBLCR** (Auction PTP Obligation Credit Requirement): formula includes BOBLMW, BPOBL (bid price), Aci, ACP (most recent clearing price); **Max(0, …)** so no credit consumed if effectively paid to take obligation.
- **DAM Credit Limit (ACLD):** **QSE** gets **90% of ACLD** for **Day-Ahead Market** (energy, DAM PTP Obligations). When **CRR auction in progress**, **locked credit** reduces pool for ACLD → **trade-off** between auction and DAM; **insufficient credit** → QSE **locked out** of DAM.

### 16. CRR settlements — auction

- **Timeline:** Auction complete → **Day 1** (ERCOT business day): **invoice** to CRR Account Holders. **Day 4** (bank): payments **due to ERCOT**. **Day 5** (ERCOT + bank): **payments from ERCOT** to sellers.
- **Charge (awarded bid)** = Clearing price × MW × TOU hours. **Payment (awarded offer)** = (−1) × (same). **Auction revenues** (bucket): **in** = charges for bids, PCRR payments; **out** = payments for offers, payments when obligations clear negative. **Distribution:** Revenues paid to **QSEs representing Load** — **Intra-Zonal** by **Zonal Load Ratio Share**, **Inter-Zonal** by **ERCOT-wide Load Ratio Share**; **once per month** after last operating day of month.

### 17. CRR settlements — Day-Ahead (Target Payment, Congestion Rent, shortfall)

- **CRRs settled daily in DAM.** **Congestion Rent** (bucket): **in** = charges for cleared DAM Energy Bids and DAM PTP Obligation bids; **out** = payments for cleared Energy Offers and PTP Obligation bids at negative price. **Net** Congestion Rent → **pay CRR owners** (Target Payment). **Surplus** → **CRR Balancing Account**. **Shortfall** → **Shortfall Charge** to each CRR owner = (Total shortfall) × (Owner’s Target Payment / Total Target Payments).
- **Target Payment** (per hour) = **(DASPP_sink − DASPP_source)** × **MW**. **PTP Option:** if price negative → Target Payment = \$0 (no charge). **PTP Obligation:** same formula; can be payment or charge.

### 18. Balancing Account, deration, Hedge Value

- **CRR Balancing Account:** Holds **surplus** Congestion Rent; **Shortfall Charges** = IOUs until month-end. **Month-end:** Liquidate Balancing Account → pay short-paid CRR owners; remainder → **Balancing Account Fund** (max **\$10M** carried over); over cap → distribute to QSEs (Load Ratio Share). If **Balancing Account + Fund** insufficient → CRR owners **remain short paid**.
- **Deration:** When **transmission oversold** (actual capability < auction model, e.g. unplanned outages), **Target Payment positive**, and **path has Resource Node** (source or sink) → CRR payment **reduced** (proportional to resource node impact on binding constraint). **Hedge Value:** Floor value using **Minimum Resource Price** (at source) and **Maximum Resource Price** (at sink) by resource type (e.g. nuclear, coal, CCGT, wind). **Payment:** If Target Payment < Hedge Value → pay Target Payment; if derated and Hedge Value < Target Payment → pay **max(Hedge Value, derated payment)**.

### 19. DAM PTP Obligations — settlement

- **Purchase in DAM:** Charge (or payment if negative) = **(DASPP_sink − DASPP_source)** × **MW** per hour. **Cash-out in Real-Time:** Payment to QSE = **(hourly average of four 15‑min (RTSPP_sink − RTSPP_source))** × **MW** per hour.

### 20. CAISO CRR (brief)

- **Congestion:** Insufficient transmission capacity in **one direction** on a path (energy flow bidirectional; congestion directional). **CRRs:** Hedge **congestion variability** under day-ahead LMP. **Acquisition:** **Allocation** (to LSEs/OBAALSEs, TAC/WAC payers) and **Auction** (unallocated; minimum collateral). **Types:** **Obligation** (pay or charge) and **Option** (pay only if favorable). **Terms:** Monthly, Seasonal, Long-Term, Merchant Transmission. **SFT** with Full Network Model; **clearing price** = MCP_source − MCP_sink. **Secondary market:** SRS (bilateral). **Components:** Type, term, sink/source, TOU (on/off-peak), MW.

---

## Balyasny-FTR: Day in the Life of an FTR Analyst – 30‑min review

*Source: Balyasny-FTR.md. Focus: ERCOT & CAISO; analysis supporting the **upcoming CRR/FTR auction**.*

### 1. Scope and role

- **Markets:** ERCOT, CAISO.
- **Role:** FTR/CRR analyst preparing and running analysis **ahead of the auction** (workflow, data sources, deliverables, timing).

### 2. What is a constraint?

- **Constraint** = a **physical or operational limit** the ISO enforces when clearing DA or RT market. When the limit is **reached**, it **binds** and affects **prices and flows**.
- **Transmission constraints:** Thermal, voltage, or stability limits on **lines**, **transformers**, or **interfaces** (e.g. “Line A–B ≤ 500 MW”). Binding → redispatch → **congestion** and **locational price differences** (LMPs diverge) → what CRRs/FTRs hedge.
- **Other limits:** Interface limits (import/export caps), generation/reserve limits, or stability constraints can also be modeled as constraints.
- **Analyst focus:** (1) Binding constraints drive **congestion rent** and **CRR payoffs**. (2) **Outages** change which constraints bind → **planned-outage** and **flow-delta** analysis **per constraint** to support auction strategy.

### 3. Dynamic rating of an element

- **Rating** = max flow (MW) an element can carry (thermal, voltage, stability). **Dynamic rating (DLR)** = limit **varies with conditions** (ambient temp, wind, solar, ice) rather than fixed **static** rating.
- **Impact:** Higher dynamic rating → less binding; lower → more binding, higher shadow prices. Analyst should use **dynamic** ratings in outage/LODF and PCM when available so **binding frequency** and **path value** reflect reality; ignoring DLR can misstate constraint value.

### 4. Shadow price

- **Shadow price** = **dual variable** (Lagrange multiplier) for a constraint: *“By how much would total cost improve if we relaxed this constraint by 1 unit?”*
- **Power markets:** For a transmission constraint (e.g. line limit MW), shadow price = **marginal cost of that constraint** (\$/MW to have one more MW on that line). **Binding** → positive shadow price; **non-binding** → zero.
- **Link to LMP:** **Congestion component** of LMP at a bus = shadow prices of binding constraints weighted by **sensitivity** (PTDFs/shift factors). Shadow prices feed **fair value**, **path valuation**, and comparison with auction clearing (e.g. from SCED, PCM, DC OPF).

### 5. PTDF and LODF

- **PTDF (Power Transfer Distribution Factor):** For a **line** (constraint) and a **transfer** (inject 1 MW at A, withdraw 1 MW at B), PTDF = **fraction of that 1 MW that appears as flow on that line**. Flow on line ℓ from transfer P from A→B: **F_ℓ = PTDF_ℓ,(A,B) × P**. Linear in DC approximation; from network admittance. **Use:** Sensitivity of constraint flow to **position** (injection/withdrawal); path valuation (path spread ≈ sum over constraints of shadow price × PTDF); DC OPF.
- **LODF (Line Outage Distribution Factor):** When **line j is out**, LODF for line *i* = **change in flow on line i per unit of pre-outage flow on line j**. ΔF_i = LODF_i,j × F_j. **Use:** **Flow delta on the constraint when a planned outage (line j) happens** → supports **impact table** (rows = outages, columns = days). From Panorama, Power World, or DC OPF.

### 6. Tools and workflow order

- **Tools:** Panorama, Enverus, Yes Energy, Power World (use cases as in doc).
- **Triage list:** Trader gives analyst the **list of constraints** to focus on for the upcoming auction → drives prioritization in ERCOT/CAISO.
- **Correct workflow order (pre-auction → auction → post-auction):**
  1. **Triage list** (constraints to focus on)
  2. **Per-constraint analysis** — planned outages, outage probability, **LODF table by day of month**
  3. **Fundamental analysis** — historical binding, drivers (e.g. ERCOT transmission planning)
  4. **Fair value of the constraint** — expected congestion value; shift factors (Yes Energy / Panorama / Power World)
  5. **Production cost modeling (Dayzer)** — UC/ED over CRR period; shadow prices, binding
  6. **Scenario analysis** — MC simulations for shift factors / topology uncertainty
  7. **Mapping** — exposure→path, constraint→path, node/bus names; vendor mapping (before choosing paths)
  8. **Choosing paths** (source–sink) — short list for auction
  9. **Bid strategy** — MW and price per path; submit to auction
  10. **[Auction runs]**
  11. **Post-mortem** — what cleared / did not, why; competitor analysis (de-anonymization, generator behavior)
  12. **MtM and VaR** — each day until payout; then **How many payments** (reference)

### 7. Per-constraint analysis (planned outages and impact table)

- For **each constraint** on triage list: (1) **Planned outage analysis** — identify outages (transmission or generation) that affect the constraint. (2) **Outage probability** — assign probability each outage occurs. (3) **Flow delta** — change in flow on the **constraint** (monitored line) when outage occurs, **by day of month** for the CRR month. (4) **How:** Panorama, Power World, or DC OPF (shift factors, LODFs).
- **Deliverable: impact table** — **Rows:** outages (or scenarios). **Columns:** days of the month. **Cells:** **LODF** for the constraint given that outage (constraint flow change per unit pre-outage flow on outaged line). Supports bid and risk decisions for the auction.

### 8. Fundamental analysis (historical binding and drivers)

- For each constraint: (1) **Historical binding** — when has it bound (SCED reports, shadow prices, congestion summaries); patterns by hour, day type, season, weather/load. (2) **Drivers** — what pushes it to the limit (load, gen mix, renewables, imports/exports, outages). (3) **ERCOT:** Use **ERCOT transmission planning** (planning models, constraint lists, studies) for which constraints are critical and how load growth, new gen, retirements, new lines affect binding.
- Outputs feed **constraint prioritization**, **scenario assumptions** for LODF/outage table, and **narrative** for the trader.

### 9. Fair value of the constraint and shift factors

- **Fair value** = what the constraint is “worth” in expected congestion or CRR payoff over the CRR period (e.g. expected shadow price or payoff per MW of CRR on a path sensitive to this constraint). Guides **how much to bid** and **constraint ranking**.
- **How derived:** (1) **Historical** — average/distribution of constraint shadow prices when binding. (2) **Forward-looking** — scenario-weighted expected shadow price from fundamental analysis. (3) **Model-based** — DC OPF or market simulation over CRR window. Use **outage probabilities** and **LODF impact** to adjust for planned outages. **Shift factors** from Yes Energy, Panorama, or Power World.
- **Shift factor** = sensitivity of **flow on a line (constraint) to 1 MW injection at a bus** (withdrawal at slack), or to a 1 MW **transfer** between two buses. In DC approximation, equivalent to **PTDF**. Flow on constraint ℓ from injections: F_ℓ = Σ SF_ℓ,i × P_i. **Use:** constraint flow from bus injections; path valuation; DC OPF for fair value.

### 10. Production cost modeling (Dayzer)

- **PCM** = unit commitment + economic dispatch over CRR period. Outputs: hourly (or sub-hourly) **LMPs**, **binding constraints**, **shadow prices**, **flows**. Forward view of when/where constraints bind and congestion value.
- **Dayzer** = commercial PCM (ERCOT, CAISO, etc.). Analyst builds/updates case (load, stack, topology, outages), runs sim, extracts binding, shadow prices, LMPs by node/zone/hub.
- **Use:** Feeds **fair value**, **fundamental analysis**, **scenario comparison** (e.g. with/without outages). With triage, LODF table, shift factors, Dayzer grounds **constraint valuation** and **auction strategy** in full market simulation.

### 11. Scenario analysis (MC for shift factors)

- **Why:** Shift factors depend on **topology** (which lines in service). Under **planned outages** or **uncertainty**, effective shift factors change. **MC** explores many topology/outage scenarios → **distribution** of constraint flows, shadow prices, path values.
- **How:** (1) Define scenarios (e.g. draw outages from outage probabilities; or sample topology). (2) Per scenario, get **shift factors** (Yes Energy, Panorama, Power World, or in-house DC). (3) Run **ED or DC OPF** (or use PCM) → constraint flow and shadow price. (4) Repeat → **distributions** (expected value, percentiles, P(binding)).
- **Use:** **Risk** (downside/upside), **bid sizing**, **sensitivity** to outage assumptions. Complements single-case Dayzer with **probabilistic** view.

### 12. Mapping (exposure → path, constraint → path, names)

- **Mapping** = aligning (1) **exposure** (gen, load, position at nodes/zones) with (2) **biddable CRR/FTR paths** and (3) **settlement point definitions**. Affects path choice, **hedge effectiveness**, bid strategy.
- **Exposure → path:** Exposure at resource nodes, load zones, hubs; auction has **limited path set**. **Map** exposure to one or more paths → **basis risk** or **basket** of paths.
- **Constraint → path:** Analysis is **constraint-centric**; CRRs are **path-centric**. Need **path PTDFs** to triage constraints so chosen paths capture constraint value. Path definitions (ERCOT/CAISO) may not align with constraint set → map constraint impact to **biddable path list**.
- **Settlement points:** CRRs settle on **SPPs** (hub, zone). Path source/sink must match **SPP definitions** used for settlement; mismatch distorts fair value and P&L.
- **Name changes and retired nodes/buses:** **Node/bus names change** (ISO renames, model updates); **some nodes retired** or merged. Historical data and vendor files may use old names or dead elements → need **crosswalks** and **vendor mapping** for consistent constraint→path and exposure→path.
- **In practice:** (1) Map exposure to paths, quantify basis risk. (2) Map triage constraints to paths via PTDFs. (3) Use **consistent SPP/path definitions** in PCM, shift factors, bids. (4) Reconcile **node/bus names and retired elements** (internal or vendor).

### 13. Choosing paths (source–sink)

- **Path** = **source–sink** pair. CRR pays (or charges) on **LMP_sink − LMP_source** over contract period. Value driven by **congestion** on constraints with **non-zero PTDF** for that path.
- **How chosen:** (1) **Constraint alignment** — paths with strong PTDF to **triage constraints** with high fair value and binding likelihood. (2) **Expected value** — rank by expected congestion payoff (PCM + path PTDFs). (3) **Risk/scenarios** — MC output for payoff distribution and downside. (4) **Outage robustness** — effect of planned outages (LODF) on path value. (5) **Liquidity** — align with biddable path list.
- **Output:** **Short list of source–sink paths** (and optionally volumes/bid levels) for the trader, with rationale.

### 14. Bid strategy (MW and price per path)

- **Price:** From **fair value** (expected path spread from PCM/scenarios). Bid at fair value, below for fill, or with spread (e.g. bid only if clearing below target). **Scenario/MC** gives range for price ladder.
- **MW:** **Risk and concentration** — how much exposure per path given limits, liquidity, correlation. **Constraint exposure** (PTDF) and **outage sensitivity** (LODF/MC) inform MW; high variance or outage sensitivity → lower MW. **Auction caps** (ERCOT/CAISO) may cap MW per path or participant.
- **Output:** **Bid recommendations** per path: **MW** and **price** (or schedule), with rationale. Ready for submission.

### 15. Post-mortem (after auction clears)

- **What cleared / what did not and why:** Compare **our bids** to **clearing**. Uncleared: **price** (bid below clearing), **volume** (capacity/curtailment), **path** (not offered/oversubscribed), **auction design**. Cleared: compare clearing to fair value. Document **why** to improve next bid levels, path choice, MW.
- **Competitor analysis — de-anonymization:** Auction results often **aggregate** or **anonymized**. **De-anonymization** = infer **which participant** is behind which bids/positions (patterns, filings, **asset ownership** e.g. gen at nodes). **Generator bidding** is key: they hedge congestion. **Who** bid on which paths, at what price/MW, and how that aligns with **plant locations and positions** → competitor strategy and future behavior.
- **Outputs:** (1) Cleared vs not cleared + reasons. (2) **Competitor view** (de-anonymized bid owners, generator behavior) for next auction.

### 16. MtM and VaR (each day until payout)

- **MtM:** **Current value** of CRR position = expected **congestion payoff** over remaining life (path spread × volume; forward congestion from curves/PCM). Updates with forwards, views, tenor. For P&L, reporting, limits.
- **VaR:** **Potential loss** over horizon (e.g. 1-day) at confidence (e.g. 95%). Risk factors: **path spread**, **congestion** (shadow prices), **volatility**. Computed **each day** (historical, parametric, or MC) until payout. For **risk limits**, capital, stress.
- **Why daily:** Value and risk **change** as time to settlement shortens, forwards move, and new info (outages, load) updates distribution. Daily MtM and VaR for monitoring, limits, P&L attribution.
- **Steps to calculate VaR for CRR portfolio:** (1) **Define portfolio** — paths, volume, obligation/option, remaining tenor. (2) **Risk factors** — path spreads or hub/zone/constraint prices; map path value via PTDFs; often **principal components** of spread returns. (3) **Data/model** — historical series, or parametric (μ, Σ), or MC distribution. (4) **Map positions to factors** — ΔV = f(Δ path spread) or f(Δ factors). (5) **Scenarios** — historical returns, parametric draws, or MC paths. (6) **VaR** — α-quantile of loss (e.g. 5th percentile of 1-day P&L for 95% VaR). (7) **Optional:** liquidity adjustment, multi-day (e.g. √10 scaling if i.i.d.). (8) **Backtest** — realized P&L vs VaR; update model.

### 17. How many payments does a CRR owner receive?

- **Settlement intervals:** CRR payoff is **calculated** over many intervals (e.g. ERCOT RT SPPs every **15 min**; others **hourly**). Many intervals determine **total** value.
- **Actual cash payments:** ISO usually **aggregates** and pays **periodically** — e.g. **one payment per month** for a monthly CRR (after month ends), or one at end of term. So owner often gets **one payment per settlement period** (e.g. one per month for one-month CRR), not one per 15‑min or hour.
- **Obligation vs option:** **Obligation** → can receive or **pay**. **Option** → receive when favorable; **no charge** when unfavorable. Payment count still by **settlement frequency** (e.g. monthly).
- **Monthly CRR (e.g. January):** **One payment** (or net) **after the month ends** (e.g. February), once ISO has full month SPPs. Exact timing per ISO settlement calendar.

### 18. Number of bids and strip structure (ERCOT from 2027)

- **ERCOT from 2027:** Participants **cannot submit one price for a sequential month** (e.g. one bid for Jan–Mar). **One bid per strip** required — **separate bid for each month/period**. So more bids to manage, **strip-level** MW and price strategy, and coordination with analyst’s path and fair value at strip level.

### 19. Facts and context (market color, tools, ERCOT)

- **Examples:** Atlas Power (congestion Charlie Creek–Watford 230 kV, SPP/MISO); Riot Rockdale crypto in ERCOT; line flow correlation with shadow prices; EmPower for Yes Energy; **Live Power** — 60‑second data on large loads (crypto, data centers); Demand Forecasts (ERCOT load, regression, weather); EnCompass (scenarios, price trends); Infrastructure Insights (ERCOT large-load queue).
- **ERCOT load/capacity (Winter 2026):** Peak load 90 GW (2026) → 117 GW (2031); firm capacity 100 GW → 133 GW. New solar often doesn’t add to firm capacity (evening peak); firm capacity growth from gas and storage. Texas fast-growing battery market; **RTC+B** supports battery growth (RTC+B live Dec 5, 2025).
- **Congestion (Jan 2022–Aug 2025):** South Zone most negative; Panhandle/North negative; Houston neutral/slightly positive; **West** consistently positive. Hub/zone congestion (LMP − λ) reflects this.
- **Feb 19 event:** RT LMPs spiked (e.g. one node ~\$28,187/MWh 8–9 AM, >\$12,000 from 5:30–10:05 AM at Round Rock area nodes NF_BRP_RN, RHESS2_ESS1). **Congestion-driven**, not system shortage (λ never >\$540/MWh; small reserve adders). Nodal LMPs can **exceed SWCAP** (\$5,000/MWh) under **irresolvable constraints**. 13 constraints binding at RHESS2_ESS1 8–9 AM, each ≥\$688 → cumulative congestion >\$26,500. Previous record ~\$12,700/MWh (Uri).
- **PowerSignals:** Nodes, prices, transmission, outages, constraints, plants, weather, gas; maps, charts, tables; volatility drivers, bid calibration.
- **Odehv–Yarbr (Oct 2024):** West Texas; Odessa Switch–Yarborough constraint. Congestion ramped mid-Sep into Oct. Shift-factor analysis → highest positive SF at **Permian Basin gas plant**. **10 MW PTP** Odessa–Permian Basin in hours when Permian turned off overnight → ~**\$60,000** over October (Nodal Spread Profile). Live Power 60‑second updates surface congestion opportunities.
- **GTC (ERCOT):** **Generic Transmission Constraint** = constraint of **two or more** transmission elements (lines/equipment) with **one combined limit** (generic transmission limit). Acts like **internal interface**; other ISOs have analogous interfaces.
- **Competitive intelligence:** Participants, volume, **cost (market investment)** → risk appetite. PJM, SPP, ERCOT, MISO largest investment; lower-investment markets → higher reward, more risk. **Yes Energy:** FTR Positions Dataset (participants, volume, investment by ISO; auction data entity/parent; 10+ years). PowerSignals (constraints, position, profit, competitors). Infrastructure Insights (gen, large load, transmission projects; stage, map, impact). **Gas:** Henry Hub dropped from 2022 highs; NGI indexes and curves; Yes Energy + NGI Daily Gas Index in Yes Energy products.

### 20. Other transmission elements that can be constraints (besides a line)

- Besides a **single line**, constraints can be on: **transformers** (step-up, step-down, intertie; MVA/thermal); **interfaces/flowgates** (cut-set, aggregate flow across boundary); **GTCs** (group of elements, one limit); **stability-related** limits (angular/voltage stability → flow limit on path or interface); **substation equipment** (bus sections, breakers, switches, cables); **series devices** (PSTs, FACTS; through-flow/MVA limits); **corridors** (multi-element shared/combined limit). When **binding**, each affects **dispatch**, **LMPs**, and **FTR/CRR** value.

---

## Interview: “Day in the life of an FTR trader” (concise)

**Use this as a 1–2 minute answer.** Adjust past tense (“I would…” / “My day…”) depending on whether you’re describing a prior role or how you’d approach the role.

### Script / talking points

- **Morning:** I start by **checking overnight and morning market moves** — DAM clears, RT prices, and any **constraint or outage** updates (e.g. ERCOT/CAISO alerts, Live Power or Yes Energy). I look at **where congestion showed up** and how our **CRR/FTR book** and **physical or financial exposure** are positioned. I’ll **sync with the analyst** on the **triage list**, any **planned outages** that matter for the next auction, and **fair value** or scenario output so we’re aligned on which paths and constraints to focus on.
- **Midday:** A lot of the day is **pre-auction work** when we’re close to an auction: reviewing **path recommendations** (source–sink), **bid strategy** (MW and price per path), and **risk** — how much we want to put on each path given **constraint exposure**, **outage sensitivity**, and **limits**. I’ll **place or adjust bids** in the auction system and stay on top of **deadlines** (e.g. ERCOT DAM, CRR auction windows). If it’s not auction day, I’m still **monitoring congestion and spreads**, **hedging** exposure (e.g. PTP vs physical), and **talking to the desk** on power and gas so our FTR view fits the broader book.
- **Afternoon / ongoing:** I track **MtM and risk** on the CRR book — **VaR**, concentration, and **sensitivity to path spreads** and key constraints. After an auction I do a **quick post-mortem**: what **cleared**, what **didn’t**, and **why** (price, volume, path, competition), and I’ll look at **competitor behavior** where we can (e.g. who’s bidding which paths, generator-heavy vs financial) so we refine the next round. I also make sure **mapping** is clean — our **exposure**, **paths we bid**, and **settlement points** line up so we’re not surprised at payout.
- **In one sentence:** My day is **staying on top of congestion and constraints**, **working with the analyst on triage, fair value, and bids**, **executing and managing the CRR book**, and **learning from clears and competitors** to improve the next auction and hedge the book.

### Analysis and results (what the analyst produces and how the trader uses it)

When you’re asked to elaborate on **analysis and results**, you can structure it like this: **what we run**, **what we get out of it**, and **how I use it as the trader**.

- **Per-constraint analysis (outages and flow impact)**  
  **Analysis:** For each constraint on the triage list we pull **planned outages** (transmission and generation), assign **outage probabilities**, and compute the **flow impact on the constraint** (via LODFs) **by day of the month** for the CRR period (e.g. Panorama, Power World, or DC OPF).  
  **Results:** An **impact table**: rows = outages (or scenarios), columns = days of the month, cells = **LODF** (or flow delta) — i.e. how much the constraint is affected when that outage happens on that day.  
  **How I use it:** I see **which outages matter most** for which constraints and **when** (which days). That drives **which paths to bid** (paths exposed to those constraints), **how much** to bid (e.g. lower volume when outage risk is high and uncertain), and **risk narrative** for the desk — e.g. “Constraint X is hot in week 2 because of the planned outage on line Y.”

- **Fundamental analysis (historical binding and drivers)**  
  **Analysis:** We look at **when each triage constraint has bound in the past** (SCED/congestion data) and **what drives it** — load, renewables, gen mix, imports/exports, specific outages — and we tie that to **ERCOT (or CAISO) transmission planning** (load growth, new gen, retirements, new lines).  
  **Results:** **Binding patterns** (hour, day type, season, weather) and a **driver narrative** — e.g. “Constraint Z binds on hot summer afternoons when West load is high and wind is low.”  
  **How I use it:** I know **when** our paths are likely to pay (e.g. peak hours, certain days) and **why** — so I can size bids and explain to the desk or risk. It also feeds **scenario assumptions** (e.g. assume a hot week in the CRR month) for the next layer of analysis.

- **Fair value of the constraint**  
  **Analysis:** We estimate **expected congestion value** for each triage constraint over the CRR period — combining **historical** shadow prices when binding, **forward-looking** scenarios (from fundamental analysis), and/or **model-based** runs (DC OPF or full PCM). We use **shift factors** (Yes Energy, Panorama, Power World) and, where relevant, **outage probabilities and LODF** to adjust for planned outages.  
  **Results:** A **fair value per constraint** (e.g. \$/MW or expected \$ over the period) and often a **ranking** of constraints by value or binding likelihood.  
  **How I use it:** I compare **our fair value** to **auction clearing** or market-implied congestion to decide **which paths are rich vs cheap**. That drives **bid price** (e.g. bid up to fair value, or below to improve fill) and **path prioritization** — we focus on paths that capture the highest fair-value constraints.

- **Production cost modeling (e.g. Dayzer)**  
  **Analysis:** We run **unit commitment and economic dispatch** over the CRR window (load, gen stack, transmission, outages) to simulate **hourly (or sub-hourly) LMPs**, **binding constraints**, **shadow prices**, and **flows**.  
  **Results:** **Forward view** of **when and where** constraints bind, **shadow prices** by constraint and hour, and **LMPs** by node/zone/hub. Often summarized into **expected path spread** (sink − source) over the period.  
  **How I use it:** I get a **single, consistent scenario** of congestion and path value. I use it to **anchor bid levels** (e.g. path fair value from PCM), **stress** the book (e.g. what if this binding pattern holds), and **cross-check** the analyst’s constraint-level fair value with path-level payoff.

- **Scenario analysis (Monte Carlo on shift factors / topology)**  
  **Analysis:** We run **many scenarios** where **shift factors** (and thus constraint flows and shadow prices) change with **topology** — e.g. different outage draws from our outage probabilities, or sampled historical topologies. For each scenario we get constraint flow and shadow price (or path value).  
  **Results:** **Distributions** of constraint value or path value — e.g. **expected value**, **percentiles** (5th, 95th), **probability of binding**, or **probability path pays above X**.  
  **How I use it:** I see **risk** around our base case — **downside** (e.g. path pays little if outages don’t happen or topology is unfavorable) and **upside** (e.g. path pays a lot if key outages hit). That shapes **bid size** (e.g. reduce MW on high-variance paths) and **price** (e.g. bid more conservatively when the distribution is wide). I can say: “Our expected path value is $Y/MW but the 10th percentile is $Z — so we’re not bidding full size at full fair value.”

- **Mapping (exposure → path, constraint → path)**  
  **Analysis:** We align **our exposure** (gen, load, commercial position at nodes/zones) with **biddable CRR paths** and **settlement point definitions**; we map **triage constraints** to **paths** via **path PTDFs** so we know which paths actually capture which constraint value; we reconcile **node/bus names** and **retired elements** (with vendor mapping if needed).  
  **Results:** A **mapping** that says: “Our exposure is here; we hedge with these paths (and here’s the basis risk)” and “These paths have high PTDF to our top constraints.” Plus **consistent naming** so PCM, shift factors, and bids all refer to the same nodes/paths/SPPs.  
  **How I use it:** I **choose paths** that both **hedge our exposure** and **capture the constraint value** we care about. I avoid bidding paths that don’t match our exposure or that don’t load on the constraints we’ve analyzed. I also avoid **mapping surprises** at settlement (wrong hub, wrong zone, or stale node names).

- **Path recommendation and bid strategy**  
  **Analysis:** Using triage, **outage impact**, **fair value**, **PCM output**, **scenario distributions**, and **mapping**, we produce a **short list of source–sink paths** and, for each, a **recommended MW and price** (or price schedule).  
  **Results:** **Path list** with **MW and price per path** and **rationale** (constraint exposure, fair value, risk, outage sensitivity, liquidity).  
  **How I use it:** This is my **execution guide** for the auction. I may adjust **MW** for risk or concentration limits and **price** for fill vs value (e.g. bid a bit below fair value on paths we really want). I submit **bids** from this and track **deadlines** and **clearing**.

- **Post-mortem (after auction)**  
  **Analysis:** We compare **our bids** to **clearing results** (what cleared, what didn’t, at what price/MW) and try to **de-anonymize** who bid what (e.g. generator vs financial, which plants/zones).  
  **Results:** **Cleared vs not cleared** with **reasons** (price, volume, path, auction design) and a **competitor view** — who’s active on which paths, how aggressive they were.  
  **How I use it:** I **learn for next time** — e.g. “We didn’t clear on path A because we were below clearing; next auction we’ll bid higher or accept less volume.” Or “Generator-heavy bidding on path B suggests we’ll see more competition there next month.” That feeds **next round’s path choice** and **bid levels**.

**Summary for the interviewer:** “The analyst runs **per-constraint** work (outages, LODF impact table), **fundamental** work (historical binding and drivers), **fair value** (expected congestion by constraint), **PCM** (Dayzer or similar for forward LMPs and shadow prices), and **scenario analysis** (MC on shift factors for distributions). The **results** are an **impact table**, **constraint fair values**, **path-level expected value and risk**, and a **path list with MW and price**. I use those to **pick paths**, **set bid levels**, **size risk**, and **explain to the desk**. After the auction we **post-mortem** clearing and competitors and feed that back into the next cycle.”

### Even shorter (30 seconds)

“As an FTR trader, my day revolves around **congestion and CRRs**: in the morning I check **prices and constraints** and align with the analyst on **which paths to target** and **bid levels**. Through the day I’m **managing the book** — bidding in auctions, hedging exposure, and watching **MtM and VaR**. After an auction I do a **post-mortem** on what cleared and why and what **competitors** did, so we keep improving our path choice and bid strategy. So it’s a mix of **fundamental congestion analysis**, **risk and execution**, and **iterating on results**.”


---

## Balyasny JD-CV: US FTR, Gas and Power Risk – Quantitative Researcher (90‑min review)

*Source: Balyasny-JD-CV.md. Condensed prep for each JD bullet: scope, key content, interview angles. Use for a ~90‑minute read-through.*

---

### 1. Risk models (term structures, volatility surfaces)

**Bullet:** Formulate and implement models for risk analysis of commodity products and derivatives (term structures, volatility surfaces).

- **Term structures:** Curve-building from liquid pillars (prompt, BOM, monthly, quarters, strips); interpolation (linear, spline, Nelson–Siegel); seasonality (monthly dummies, sinusoidal); no-arbitrage across products. **Basis:** location (F_loc = F_hub + B), calendar (F_T1 − F_T2), spot–forward; basis risk when hedging exposure P with index I.
- **Vol surfaces:** Implied vol from options; strike (moneyness) and term; sticky-strike vs sticky-delta (sticky-delta common in commodities for stable Greeks). Power/gas: spikes, mean reversion, seasonal vol; SABR, local vol (Dupire), stochastic vol + jumps. No-arb: butterfly (∂²C/∂K² ≥ 0), calendar consistency.
- **Black-76** for options on forwards (no storage/carry); **Asian** options for power (settlement on average, lower vol, manipulation-resistant). **VaR/CVaR:** 1-day 99% VaR = loss threshold; ES = average loss when loss > VaR.
- **Greeks:** Delta, gamma, vega, theta, rho; vanna, volga. **Delta–gamma–vega hedging** for FTR/power/gas; higher-order (vanna, volga) usually not hedged (magnitude, liquidity, model risk).
- **Important risk metrics (table):** VaR, ES, delta by bucket, gamma, vega, limit utilization, concentration, stress P&L, correlation/diversification, P&L attribution, MTM/mark uncertainty.
- **MTM:** FTR (spread curves, proxy, optionality); power (curves, vol, Asian, basis); gas (hub + basis, storage/swing). **Collateral:** ERCOT credit for CRR; ISDA/CSA + UMR for power/gas; VM/IM drivers; liquidity and dispute handling.
- **Correlation:** Historical, factor model, copulas (t, Gumbel, Clayton), scenarios; FTR proxy; use in VaR, margin, stress.
- **VaR platform (steps):** Scope, data (positions, curves, history, covariance); valuation/P&L; historical VaR (P&L series, quantile, no √t for mean-reverting); MC VaR (factors, simulate, revalue, quantile); backtest (exception rate, binomial, traffic light); **√t scaling** often wrong for commodities (mean reversion); prefer h-day P&L or h-day simulation.
- **Backtesting:** Realized vs hypothetical P&L; exception = loss > VaR; binomial test; by-book; FTR marks noisy.
- **Intramonth VaR:** DAM, RT, DART (spread); 1-day or remaining-days; historical or MC; no √t.
- **Stochastic processes:** OU, Schwartz 1-factor, jump-diffusion, two-factor (Schwartz–Smith), FTR spread (two OUs or single OU/jump), multi-asset (Cholesky correlation).
- **Copulas:** Sklar; tail dependence; Gaussian, t, Clayton (lower), Gumbel (upper); fit marginals then copula; simulate for VaR/CVaR.
- **HPFC:** Hourly curve from block/month forwards; no-arb (average = forward); methods: proportional, load-based, temperature, PCA, spline, regression, constrained QP.
- **Gas modeling:** OU/Schwartz, jump-diffusion, two-factor, hub + basis, forward dynamics, storage/swing (DP, LSMC).
- **Products table:** FTR/CRR (ERCOT, PJM, MISO, SPP, CAISO, NYISO, ISO-NE); power (hubs, CME/ICE, OTC); gas (Henry, basis, ICE/NYMEX).

**Interview angles:** Term structure from pillars and no-arb; vol surface with sticky-delta for risk; Black-76 for commodity forwards; Asian for power settlement; VaR + ES; delta–gamma–vega; avoid √t for commodities; backtest hypothetical for model validation.

---

### 2. Risk reporting (risk analysis, P&L attribution, portfolio construction)

**Bullet:** Improve and extend risk reporting tools: risk analysis, P&L attribution, portfolio construction; periodic and ad-hoc.

- **Reporting layer:** Deliver risk (VaR, Greeks, stress) via dashboards, packs, ad-hoc; improve existing (views, pipelines, automation).
- **Risk analysis in reporting:** Metrics by book, tenor, location, factor; exposure, limit utilization, scenario comparison; filtering, export.
- **P&L attribution:** Decompose P&L into **curve (delta)**, **vol (vega)**, **theta**, **new trades**, **residual**. By **book** (FTR, power, gas) and by **product** (forwards, swaps, options, FTR obl/opt, storage, basis). **FTR:** curve = path spread; vol for options; residual = realization, volume. **Power/gas:** curve by hub/tenor and basis; vega, theta; residual = gamma, basis, fixing. **Reconciliation:** attributed ≈ actual; large residual → refine buckets.
- **Portfolio construction platform:** Single source of truth (positions, risk factors, versioning); unified valuation/risk engine; views (exposure, concentration, marginal VaR, limits, correlation); scenario and what-if (add trade, shock curve/vol); optional optimization (objective + constraints → trade list); integration with execution and reporting.
- **Periodic:** Daily (risk pack), weekly (attribution, trend), monthly (portfolio summary, attribution), quarterly (full risk report); process = data → run → validate → distribute; ownership, SLAs, automation.
- **Ad-hoc:** Examples for FTR (delta by path, attribution, concentration, what-if, auction summary); power (delta by hub/tenor, peak/off-peak, vega, basis, DAM vs RT); gas (delta hub/basis, storage, swing); cross-asset (why VaR moved, correlation, stress, limit utilization).
- **Tooling:** Streamlit (quick Python apps), Dash (reactive dashboards), Power BI (enterprise, scheduled, governance).

**Interview angles:** Map data flow and bottlenecks; extend incrementally; periodic = automate + SLAs; ad-hoc = parameterized/modular; Streamlit/Dash for quants, Power BI for broad distribution.

---

### 3. Stress testing (historical, hypothetical, standardized metrics)

**Bullet:** Develop methodologies and procedures for historical and hypothetical stress testing; analyze results with standardized statistical metrics.

- **Historical:** Replay **past** market moves on **current** (or past) portfolio; factor alignment (curves/vol as of stress date); revalue; output = stressed P&L (and margin). FTR: use realized DAM or proxy.
- **Hypothetical:** **Defined** shocks (e.g. power +$X, gas +$Y, vol +Z%, FTR spread ±W); apply to factors; revalue. Scenario library; joint vs single-factor.
- **Standardized metrics (per scenario):** Stressed P&L; stressed P&L % (of MTM or capital); max loss; mean shortfall; percentile (if many scenarios); contribution by book; margin impact. **Formulas:** P&L_s = V_s − V_0; max loss = min_s P&L_s; mean shortfall over loss scenarios.
- **Process:** Library → run (apply shock, revalue) → compute metrics → report card → comparison and trend; use for limits, capital, liquidity.

**Interview angles:** Historical = actual moves; hypothetical = designed tails; same metrics every run for comparability and governance.

---

### 4. Configuring and calibrating risk systems (with Risk)

**Bullet:** Work with Risk Management to configure and calibrate risk systems.

- **Configure:** Data sources, risk factors, buckets, **parameters** (VaR method, confidence, horizon, lookback), **limits** and thresholds, **outputs** and reporting. Versioned config; change control and Risk sign-off.
- **Calibrate:** **VaR** (lookback, confidence, FTR proxy, correlation); **vol** (surfaces, proxy for illiquid); **correlation** (FTR–power–gas); **curves** (alignment with Risk); **stress** scenario set.
- **When to re-calibrate (FTR):** Proxy choice/mapping, spread curve vs mark, vol for options, settlement/horizon. **Power:** Vol surface (hub/location), Asian/vol of average, correlation (DAM/RT, hub/location), curve/basis. **Gas:** Hub/basis vol, correlation (hub, basis, power), storage/swing, curves. **Cross-asset:** Correlation matrix, VaR lookback/confidence, stress set.
- **Working with Risk:** Risk owns policy and approval; research proposes config/calibration and implements; Risk validates; document and version; monitor backtest and re-calibrate when needed.
- **Policy change:** New limits, scope (e.g. FTR in VaR), stress set, reporting → **configure** (new buckets, limits, reports) and **calibrate** (params, scenarios); impact assess → implement → validate → communicate → effective date.

**Interview angles:** Configure = what the system uses; calibrate = set parameters so outputs are agreed with Risk; policy change → update config and calibration and validate.

---

### 5. Quantitative methods (liquidity, liquidation costs)

**Bullet:** Apply quantitative methods to risk topics: market liquidity, liquidation costs.

- **Market liquidity:** Tightness (spread), depth, resilience, immediacy. **Estimate:** bid-ask, effective spread; depth and volume; **market impact** (e.g. power law (Q/V)^α, α ≈ 0.5). **LVaR:** VaR + spread/2 × position + impact cost; or lengthen horizon for illiquid.
- **FTR liquidity:** No continuous market; auction-based; path-specific; marks model-based; estimate from auction participation and proxy; LVaR with long horizon and discount to mark.
- **Power/gas ICE:** Hub futures/options liquid (spread, depth, volume); basis/location thinner; stress = 2× spread, reduced depth.
- **Liquidation cost:** Implementation shortfall (spread, impact, timing, opportunity); **Almgren–Chriss** (optimal execution, cost vs vol risk); stress (scale impact/spread, fire-sale); portfolio (correlation of liquidity). **Methods table:** shortfall, additive, Almgren–Chriss, scenario-based, MC, stress scaling, portfolio aggregation.

**Interview angles:** Liquidity = ease of trading; liquidation cost = cost to unwind over horizon; estimate from spread and impact (power law, shortfall); use in LVaR, limits, stress.

---

### 6. Contribute to overall risk team (ad-hoc, firm-wide)

**Bullet:** Contribute to risk team: analytics, processes, reporting; ad-hoc for non-commodities or commodities' impact on firm risk.

- **Team-wide:** Same discipline on analytics, process, reporting; may support non-commodities when needed; commodities correctly in firm reports.
- **Ad-hoc non-commodities:** Equities, rates, credit, FX, multi-asset, systematic — VaR, stress, explain, backtest; transferable quant skills.
- **Commodities' impact on firm:** Marginal/incremental VaR; correlation (normal and stress); risk decomposition (Euler/contribution); stress contribution; notional share; liquidity/funding. **Workflow:** Define book → firm VaR with/without → correlation → decompose → stress → report.

**Interview angles:** Primary = commodities; support broader team; investigate commodities' contribution to firm VaR, correlation, stress.

---

### 7. Global Risk Committee (risk drivers, related markets)

**Bullet:** Contribute to GRC understanding of risk drivers and considerations in related markets.

- **Risk drivers:** What moves P&L — power price (hub, location, shape), gas (hub, basis), congestion/FTR spread, vol, correlation, liquidity, regulation. **Related markets:** power↔gas (spark spread), power↔congestion (LMPs, FTR), weather, regional (ERCOT, PJM, etc.). **Considerations:** liquidity, regulatory, operational, concentration.
- **Reference table:** FTR (spread, path, tenor, liquidity, spread vol); power (price, vol, shape, basis, fuel); gas (price, basis, vol, storage, weather).
- **Contribute:** Present and explain; related markets and linkages; scenarios and stress in plain language; limits and policy; answer ad-hoc (why VaR moved, exposure, basis).

**Interview angles:** Explain drivers and metrics clearly; describe power–gas–FTR linkages and regional differences; support limits and policy.

---

### 8. Work with technology (automate, maintain, integrate)

**Bullet:** Work with technology team to automate, maintain, and enhance integration of research and reporting.

- **Automate:** Schedulers (cron, Airflow); pipelines (data → curves → risk → report); parameterized, idempotent; research = what/cadence, tech = where/how.
- **Maintain:** Fix breaks (data, APIs, deps); version code and config; monitor runs; document.
- **Enhance integration:** Research/reporting consume and publish to data lake, risk platform, dashboards; align schemas and refresh; extend rather than replace.

**Interview angles:** Research owns what and why; tech owns where and how; collaborate on SLAs and failure handling.

---

### 9. Onboard new portfolios and products (with Risk)

**Bullet:** Work with risk management to onboard new portfolios and products.

- **Onboard:** **Data** (positions, market data, mapping); **models/valuation** (curve, vol, FTR proxy); **limits** (Risk sets with exposure view); **reporting** (new book in reports); **validation** (backtest, reconcile) before go-live.
- **Examples:** New FTR paths/region (position source, spread curve, VaR/stress, limits); new power/gas product or hub (curve, vol, buckets, data feed).

**Interview angles:** Data, models, limits, reporting, validate with Risk; Risk owns policy, research provides analytical support.

---

### 10. Seasonality in commodities risk models

**Bullet:** Experience with seasonality in commodities risk models.

- **Why:** Demand/supply (power summer/winter, gas winter heating); curves (seasonal dummies, peak/off-peak, winter/summer strips); **vol** (higher in peak months); **correlation** (e.g. gas–power by season). Ignoring → wrong VaR/Greeks/stress by season.
- **Modeling (table):** Curves (seasonal component, peak/off-peak); vol (term structure by month); demand (load shape); correlation (seasonal or regime); stress (season-specific scenarios). **Power:** seasonal curve and vol; peak/off-peak; renewables. **Gas:** winter/summer; storage; basis. **FTR:** load-driven congestion; historical spread by month; proxy with seasonal power.

**Interview angles:** Build seasonality into curves, vol, stress; power/gas/FTR all seasonal; VaR and stress seasonally aware.

---

### 11. Python and SQL; numeric libraries

**Bullet:** Strong Python and SQL; familiar with pandas, numpy, etc.

- **Libraries (reference):** NumPy (arrays, vectorized, random); pandas (DataFrames, time series, groupby, I/O); SciPy (optimize, interpolate, stats); matplotlib/seaborn/Plotly (viz); SQL/sqlalchemy (query); pytest (tests). For commodities: curves, VaR, reporting, data pipelines.
- **Interview angles:** Strong Python/SQL; pandas/numpy for data and numerics; scipy for optimization and stats; versioned, tested code.

---

### 12. Advanced Python (venv, release, multi-processing, Git)

**Bullet:** Advanced Python: virtual environments, release process, multi-processing.

- **Virtual envs:** venv/conda per project; pin in requirements.txt or environment.yml; reproducible.
- **Release:** Git (branches, tags); versioning (semver or calver); testing (pytest, CI); optional packaging; deploy from tag; changelog.
- **Multi-processing:** multiprocessing, ProcessPoolExecutor, joblib for CPU-bound (VaR scenarios, curve over paths); threading for I/O-bound; partition work, avoid shared state.
- **Git (reference):** init, clone, config; status, branch, checkout, add, commit; log, diff; remote, fetch, pull, push; merge, rebase, reset, revert; tag; stash.

**Interview angles:** Venv per project, pin deps; release = tag + tests + deploy from tag; multi-processing for CPU-heavy risk runs (ProcessPoolExecutor, joblib).

---

### 13. Hedge fund / systematic futures experience

**Bullet:** Experience at hedge fund/asset manager with exposure to systematic futures or portfolio construction.

- **Assess exposure:** Define universe (futures) and tag systematic vs discretionary (and by factor). **Metrics:** notional, position count, capital/VaR by strategy and share of fund; gross/net. **Factor exposure:** Regress returns on factor returns (trend, carry); attribution. **Risk:** Marginal/component VaR, stress contribution, correlation with rest of fund. **Data:** Positions with strategy labels; returns by book; factor series.

**Interview angles:** Tag by strategy; measure notional and VaR by strategy; factor betas and attribution; marginal VaR and correlation for diversification and tail risk.

---

### 14. Factor analysis, PCA, decomposition, ML; LP/IP

**Bullet:** Experience with factor analysis, PCA, decomposition for P&L and risk, machine learning.

- **Factor analysis:** Latent or observed factors; loadings; factor VaR; P&L attribution to factors.
- **PCA:** Curve/surface (level, slope, curvature) or returns; dimension reduction; factor-style VaR; variance explained.
- **P&L decomposition:** Curve (delta), vol (vega), theta, new trades, residual; by book and bucket. **VaR decomposition:** Component/marginal VaR (Euler); by position, bucket, or factor.
- **ML in energy:** **Power:** LMP/load/vol forecast (GBM, LSTM, SARIMAX); features (weather, load, renewables). **Gas:** Hub/basis forecast, storage (GBM, neural nets, quantile). **FTR:** Spread/congestion forecast; FTR proxy (predict from factors, cluster, PCA/autoencoder, generative); scenario generation. Cross-cutting: features, validation, interpretability (SHAP).
- **LP/IP:** **Power:** SCED = LP (LMPs, congestion from duals); UC = MIP (on/off). **Gas:** Flow = LP; storage/transport = multi-period LP. **FTR:** Auction clearing = LP (PTDF constraints); SFT = LP. **Use:** Interpret clearing, stress by re-running/approximating, hedge/portfolio optimization.

**Interview angles:** PCA on curve changes for factors; P&L explain and VaR decomposition; ML for forecasting and FTR proxy; LP at core of dispatch, gas flow, FTR clearing; MIP for UC and discrete decisions.

---

### Interview Q&A (condensed)

- **Power forward curve (liquid hub):** Pillars from liquid products; no-arb; interpolate; seasonality; validate vs broker.
- **Sticky-strike vs sticky-delta:** Sticky-strike = vol constant in K; sticky-delta = vol constant in moneyness; for power/gas often sticky-delta for stable Greeks.
- **Arbitrage-free vol surface:** Calendar (no calendar arb), butterfly (positive density), triangle (put-call parity); constrain calibration or use arbitrage-free parameterization.
- **Power vs gas term structure:** Power non-storable, spikes, seasonality; gas storable, storage links prompt to forward; both need seasonal; power higher short-term vol.

---


## Interview Q&A (condensed)

**Q: Power forward curve (liquid hub)?** Pillars from liquid products; no-arb; interpolate; seasonality; validate vs broker.

**Q: Sticky-strike vs sticky-delta?** Sticky-strike: vol constant in $K$; delta can be unstable. Sticky-delta: vol constant in moneyness; delta stable; use for power/gas.

**Q: Arbitrage-free vol surface?** Calendar (no calendar arb); butterfly $\partial^2 C/\partial K^2 \geq 0$; put-call parity. Constrain calibration or use arbitrage-free parameterization.

**Q: Power vs gas term structure?** Power non-storable, spikes, seasonality; gas storable, storage links prompt to forward; both seasonal; power higher short-term vol.

**Q: When does $\sqrt{t}$ scaling fail?** Mean reversion (commodities); autocorrelation; time-varying vol; fat tails. Use $h$-day P&L or $h$-day simulation.

**Q: Why hypothetical P&L for FTR backtest?** Marks noisy and model-based; hypothetical isolates market move; cleaner for validation.

**Q: LVaR for FTR?** Long unwind horizon; discount to model mark; concentration amplifies; no continuous market.

**Q: How contribute to GRC?** Explain drivers in plain language; charts; linkages (gas → power → congestion); translate stress; support limits.

**Q: Onboard new region?** Data, models, limits, reporting, validate with Risk; document; go-live.

**Q: Config vs calibrate?** Configure = what system uses (data, factors, params, limits, outputs). Calibrate = set parameters (VaR, vol, correlation, curves, stress). Policy change → update both; validate.

**Q: Book impact on firm risk?** Marginal VaR (firm with book $-$ without); correlation (normal and stress); Euler decomposition by book; stress contribution; notional share; liquidity (liquidation cost, margin).

**Q: Reporting process?** Data readiness → run (idempotent) → validate (sanity, reconciliation) → distribute with version; SLAs; ownership; automation (scheduler).

**Q: Why not hedge vanna/volga?** Magnitude small (second-order); no liquid instruments in power/gas/FTR; estimation noisy; cost $>$ benefit.

**Q: Historical vs MC VaR?** Historical: no distribution assumption, limited tail. MC: impose structure, model risk. Use both; FTR proxy affects both.

**Q: Backtest too many exceptions?** Check vol (scale/lookback), correlation, FTR proxy; consider MC with fatter tails; document and Risk sign-off.

**Q: SABR?** $\mathrm{d}F = \sigma F^\beta\,\mathrm{d}W_1$, $\mathrm{d}\sigma = \nu\sigma\,\mathrm{d}W_2$; approximate implied vol; calibrate at liquid hubs; for illiquid transfer or scale from hub; no jumps.

**Q: Component vs marginal VaR?** Component VaR = Euler allocation (contribution of position to portfolio VaR); marginal VaR $= \partial\mathrm{VaR}/\partial w_i$ or VaR(with) $-$ VaR(without).

**Q: PTDF?** Linear map from net injections to line flows; used in FTR feasibility and clearing (LP).

**Q: DART?** Day-ahead–real-time spread; exposure to $(RT - DAM)$.

---

## Procedures (short)

**Power forward curve:** (1) Identify liquid products (day-ahead, BOM, monthly, seasonal strips). (2) Collect quotes; define pillars (price per delivery period). (3) No-arb: e.g. quarterly = consistent average of monthly forwards; solve or interpolate. (4) Interpolation (e.g. cubic spline in time or log-price). (5) Add seasonality (monthly dummies or sinusoidal). (6) Validate vs broker screens and recent trades. (7) Version and store curve (as-of date, source).

**Historical VaR (1-day):** (1) Define scope (books: FTR, power, gas; risk factors). (2) Load positions and curves as of today. (3) Load historical market data (curves, vol) for each date $s$ in lookback (e.g. 500 days). (4) For each $s$, value portfolio at $s$ and $s-1$; $\mathrm{P\&L}_s = V_s - V_{s-1}$. (5) Order P&L series. (6) VaR at $\alpha$ = $\alpha$-quantile of P&L (e.g. 5th percentile for 95% VaR). (7) ES = average of P&Ls below VaR. (8) Optionally decompose by book.

**Hypothetical stress:** (1) Load scenario library (name, description, shock spec per factor) and current portfolio and curves/vol. (2) For each scenario $s$: apply shocks (additive/multiplicative/curve replace) to risk factors; revalue portfolio at stressed factors → $V_s$; stressed P&L $_s = V_s - V_0$. (3) Compute standardized metrics: P&L %, max loss, mean shortfall, contribution by book, margin impact if needed. (4) Fill report card (scenario $\times$ metrics). (5) Distribute and archive.

**P&L attribution (daily):** (1) Curve: revalue at $t$ with curves $t-1$ (or $\sum \Delta_k \Delta F_k$). (2) Vol: vega $\times \Delta\sigma$. (3) Theta; (4) New trades; (5) Residual = actual $-$ sum.

**Onboard new FTR region:** Data (position source, spread curve) → models (extend engine) → limits (with Risk) → reporting → backtest/reconcile → Risk sign-off → go-live.

**Policy change procedure (short):** (1) Capture and document (what changed, why, effective date). (2) Impact: config (limits, buckets, reports) and calibration (VaR params, vol, correlation, stress). (3) Implement: update config and calibration; test; version and document. (4) Validate: Risk validates; sign-off before go-live. (5) Communicate; effective date and cutover; bridge history if required.

---

## Definitions and acronyms

- **Hypothetical P&L:** Revalue fixed portfolio at $t$ and $t-1$; no new trades. **Realized P&L:** Actual trading P&L.
- **Component VaR:** Euler allocation; contribution of position/book to portfolio VaR. **Marginal VaR:** $\partial\mathrm{VaR}/\partial w_i$ or VaR(with) $-$ VaR(without).
- **Mean shortfall:** $\mathrm{avg}\{(V_s - V_0) : V_s - V_0 < 0\}$. **Implementation shortfall:** Theoretical $-$ actual execution P&L (spread, impact, timing, opportunity).
- **FTR proxy:** Substitute series for path returns (e.g. CRR MTM change, congestion index). **LVaR:** VaR $+$ liquidity adjustment (spread $+$ impact or longer horizon).
- **SCED:** Economic dispatch LP; duals = LMPs, congestion. **PTDF:** Power transfer distribution factors; flow = PTDF $\times$ net injection. **SFT:** Simultaneous feasibility test (LP for FTR feasibility).
- **OU:** Ornstein–Uhlenbeck; $\mathrm{d}X = \kappa(\theta-X)\,\mathrm{d}t + \sigma\,\mathrm{d}W$. **SABR:** Stochastic vol model; $\mathrm{d}F = \sigma F^\beta\,\mathrm{d}W_1$, $\mathrm{d}\sigma = \nu\sigma\,\mathrm{d}W_2$.
- **HPFC:** Hourly price forward curve; no-arb = block average = forward. **DART:** Day-ahead–real-time spread. **CRR:** Congestion revenue right (ERCOT FTR). **Backtest exception:** 1 if $\mathrm{P\&L}_t < -\mathrm{VaR}_{t-1}$; rate $\hat{p} = N/T$. **No-arbitrage (surface):** butterfly $\partial^2 C/\partial K^2 \geq 0$; calendar consistency; put-call parity. **Spark spread:** Power price $-$ (heat rate $\times$ gas price).

---

## Quick one-line answers (self-test)

- Power curve: pillars from liquid products, no-arb, interpolate, seasonality, validate vs broker.
- Sticky-strike: vol constant in $K$; sticky-delta: vol constant in moneyness; use sticky-delta for stable Greeks.
- Arbitrage-free surface: butterfly $\partial^2 C/\partial K^2 \geq 0$, calendar consistency, put-call parity; constrain calibration or use arbitrage-free parameterization.
- Power vs gas term structure: power non-storable, spikes, seasonality; gas storable, storage links prompt to forward; both seasonal; power higher short-term vol.
- $\sqrt{t}$ fails: mean reversion, autocorrelation, time-varying vol, fat tails; use $h$-day P&L or $h$-day simulation.
- Hypothetical backtest for FTR: marks noisy and model-based; hypothetical isolates market move.
- GRC contribution: explain drivers and metrics in plain language; charts; describe linkages; translate stress; support limits.
- LVaR for FTR: long unwind horizon (to auction or settlement), discount to model mark; concentration amplifies.
- Onboard new region: data, models, limits, reporting, validate with Risk; document; go-live.
- Seasonality in vol: term structure by month (options or historical same-month); higher vol in peak months; month-dependent vol in VaR.
- BSM assumptions break: constant vol (use surface), constant $r$ (use $P(t,T)$), lognormal (fat tails, jumps), complete market (illiquid).
- Book impact on firm: marginal VaR, correlation (normal and stress), decomposition, stress contribution, notional share, liquidity.
- LP/IP: SCED = LP (LMPs, congestion); UC = MIP; gas flow = LP; FTR clearing = LP (PTDF); interpret and stress.
- Reporting process: data readiness → run → validate → distribute; SLAs; ownership; automation.
- No vanna/volga hedge: magnitude small, no liquid instruments, estimation noisy, cost $>$ benefit.
- Historical vs MC VaR: Historical = no distribution assumption, limited tail; MC = impose structure, model risk; use both.
- Backtest too many exceptions: check vol (scale/lookback), correlation, FTR proxy, horizon; consider MC with fatter tails; document and Risk sign-off.
- Simple LVaR for power: VaR $+$ (half-spread $\times$ position) $+$ impact (e.g. $k(Q/V)^{0.5}$); calibrate $k$; stress = 2$\times$.
- Large residual: finer buckets, gamma, basis not in buckets, model/data change, new-trade timing; drill by book/date.
- Discount curve: option MTM and forward PV use $P(t,T)$; rho usually small; same curve for mark and risk.
- New power hub: data (positions, curve, history); add to curve/vol and buckets; limits and reporting; backtest and correlation; Risk sign-off.
- LSMC: least-squares Monte Carlo; for American/optional exercise (e.g. storage) by regression on state.
- $t$-copula: symmetric tail dependence. Gumbel: upper tail (e.g. joint spikes). Clayton: lower tail (e.g. joint losses).
- Euler allocation: sum of component VaRs = total VaR; component $_i = w_i \times$ marginal VaR $_i$.
- Almgren–Chriss: optimal execution model; balance market impact vs volatility risk; expected cost and variance.
- FTR proxy: substitute series for path returns (e.g. CRR MTM change, congestion index); needed because most paths have no liquid price series.

---

## Stress scenario examples

- **Power spike:** e.g. ERCOT North +\$50 \$/MWh. **Gas winter:** Henry +\$2, basis SoCal +\$1. **Vol up:** parallel +\$10%. **FTR blow-out:** path spread +\$20 \$/MWh. **Heat wave:** power up, gas up, congestion up. **Cold snap:** winter demand, gas spike. **Concentration:** one path or one hub blows out. **Historical:** Aug 2020 heat wave; Feb 2021 cold snap; rolling worst $N$ days.

---

## Section recap (one line each)

- **§1 Risk models:** Term structure (pillars, no-arb, Nelson–Siegel); Black-76, Asian; VaR/ES; Greeks; no $\sqrt{t}$; backtest; OU, jump, two-factor, copulas; HPFC; products; intramonth.
- **§2 Reporting:** P&L attribution (curve, vol, theta, new trades, residual); portfolio construction; periodic (daily/weekly/monthly); process and SLAs; Streamlit/Dash, Power BI.
- **§3 Stress:** Historical vs hypothetical; metrics (stressed P&L, %, max loss, mean shortfall, by book, margin); report card; process.
- **§4 Config/calibrate:** Configure (data, factors, params, limits); calibrate (VaR, vol, correlation, curves, stress); re-calibrate triggers; policy change; work with Risk.
- **§5 Liquidity:** Market liquidity, LVaR; FTR liquidity (auction-based); liquidation cost (shortfall, Almgren–Chriss); concentration, counterparty, model risk.
- **§6 Firm:** Commodities impact (marginal VaR, correlation, decomposition, stress, notional, liquidity); support non-commodities.
- **§7 GRC:** Risk drivers (FTR, power, gas); related markets; present drivers, charts, linkages, stress; support limits.
- **§8 Technology:** Automate (schedulers); maintain (version, monitor); enhance (data lake, extend not replace); research = what/why, tech = where/how.
- **§9 Onboarding:** Data, models, limits, reporting, validation; new FTR region, new hub; Risk sign-off.
- **§10 Seasonality:** Curves, vol, demand, correlation, stress by season; power/gas/FTR specifics.
- **§11 Python/SQL:** NumPy, pandas, SciPy, viz, SQL; curves, VaR, pipelines.
- **§12 Advanced Python:** venv, pin deps; Git, pytest, CI; multi-processing; release from tag.
- **§13 Systematic:** Universe, strategy tag; notional, VaR by strategy, factor betas, correlation.
- **§14 Factor/PCA/ML/LP:** Factor, PCA; P&L and VaR decomposition; ML (power, gas, FTR); LP (SCED, gas, FTR clearing); PTDF; risk use.

---

## Interview angles (one line per section)

- **§1:** Term structure from pillars + no-arb; vol sticky-delta for risk; Black-76 for commodity forwards; Asian for power; VaR + ES; avoid $\sqrt{t}$; backtest hypothetical for validation.
- **§2:** Map data flow; extend incrementally; periodic = automate + SLAs; ad-hoc = parameterized; Streamlit/Dash for quants, Power BI for broad distribution.
- **§3:** Historical = actual moves; hypothetical = designed tails; same metrics every run for comparability and governance.
- **§4:** Configure = what the system uses; calibrate = set parameters for agreed outputs; policy change → update both and validate.
- **§5:** Liquidity = ease of trading; liquidation cost = cost to unwind; estimate from spread + impact (power law, shortfall); use in LVaR, limits, stress.
- **§6:** Primary = commodities; support broader team; investigate commodities' contribution (marginal VaR, correlation, stress, concentration).
- **§7:** Explain drivers and linkages clearly; stress and concentration for committee; support limits and policy.
- **§8:** Research owns what/why; tech owns where/how; collaborate on SLAs and failure handling.
- **§9:** Data, models, limits, reporting, validate with Risk; Risk owns policy, research provides analytical support.
- **§10:** Build seasonality into curves, vol, stress; power/gas/FTR all seasonal; VaR and stress seasonally aware.
- **§11:** Strong Python/SQL; pandas/numpy for data and numerics; scipy for optimization and stats; versioned, tested code.
- **§12:** Venv per project, pin deps; release = tag + tests + deploy; multi-processing for CPU-heavy risk runs.
- **§13:** Tag by strategy; measure notional and VaR by strategy; factor betas and attribution; marginal VaR and correlation for diversification and tail risk.
- **§14:** PCA on curve changes; P&L explain and VaR decomposition; ML for forecasting and FTR proxy; LP at core of dispatch, gas flow, FTR clearing; MIP for UC.

---

## What to say when (short)

- **"How do you build a curve?"** → Pillars from liquid products, no-arb, interpolate, seasonality; validate vs broker.
- **"Why Black-76?"** → Options on forwards; power non-storable, gas complex; market convention; same curve for risk and options.
- **"Why no $\sqrt{t}$?"** → Mean reversion; use $h$-day P&L or $h$-day simulation.
- **"Why hypothetical backtest for FTR?"** → Marks noisy and model-based; hypothetical isolates market move.
- **"How do you attribute P&L?"** → Curve ($\sum \Delta_k \Delta F_k$), vol (vega $\times \Delta\sigma$), theta, new trades, residual; by book and product; reconcile.
- **"How do you stress?"** → Historical = replay past moves; hypothetical = defined shocks; same metrics every run (stressed P&L, %, max loss, by book, margin).
- **"How do you work with Risk?"** → Risk owns policy/limits; we propose config and calibration and implement; Risk validates; document and version.
- **"How do you handle FTR liquidity?"** → No continuous market; auction-based; LVaR with long horizon and discount to mark; concentration amplifies.
- **"How do you contribute to GRC?"** → Explain drivers and metrics in plain language; charts; describe linkages (gas→power→congestion); translate stress; support limits.
- **"How do you onboard a new product?"** → Data, models, limits, reporting, validation; Risk sign-off; document.

---

## Final checklist (scan before interview)

- Term structure: pillars, no-arb, interpolation, seasonality, Nelson–Siegel $y(\tau)$.
- Forward $F(t,T) = \mathbb{E}^Q[S_T \mid \mathcal{F}_t]$; basis location/calendar/spot–forward; basis risk $\mathrm{Var}(P-I)$.
- Vol surface: smile, sticky-strike vs sticky-delta (use sticky-delta); no-arb butterfly $\partial^2 C/\partial K^2 \geq 0$.
- Black-76: $C = P(t,T)(F_0 N(d_1) - K N(d_2))$; $d_1$, $d_2$; why for commodities; BSM assumptions that break.
- Asian: payoff on average $A$; no closed form; MC or approximations.
- VaR $\mathrm{VaR}_\alpha(L) = -q_\alpha(L)$; ES $\mathrm{ES}_\alpha = \mathbb{E}[-L \mid -L \geq \mathrm{VaR}_\alpha]$; 1-day 99% meaning.
- Greeks: $\Delta$, $\Gamma$, $\mathcal{V}$, theta, rho; delta–gamma–vega hedge; why not vanna/volga.
- Risk metrics: VaR, ES, delta by bucket, gamma, vega, concentration, stress, P&L attribution.
- MTM: FTR (spread curves, vol); power/gas (curves, vol, basis); collateral ERCOT/ISDA/CSA, UMR.
- Correlation: FTR–power–gas; historical, factor, copulas; FTR proxy (CRR MTM, congestion index).
- VaR platform: Historical vs MC; no $\sqrt{t}$; backtest (exception, $\hat{p}$, binomial, traffic light); hypothetical for FTR.
- OU: $\mathrm{d}X = \kappa(\theta-X)\,\mathrm{d}t + \sigma\,\mathrm{d}W$; $\mathbb{E}[X_T\mid X_t]$, $\mathrm{Var}(X_T\mid X_t)$; Schwartz, jump, two-factor.
- Copulas: Sklar; Gaussian, $t$, Clayton, Gumbel; tail dependence; fit marginals then copula.
- HPFC: no-arb block average = forward; methods (proportional, load, temp, PCA, QP). Gas: storage DP/LSMC.
- Products: FTR (ERCOT, PJM, …); power (hubs, peak/off-peak); gas (Henry, basis); acquisition; settlement.
- Intramonth: DAM, RT, DART; no $\sqrt{t}$; 1-day or remaining-days P&L.
- P&L attribution: curve ($\sum \Delta_k \Delta F_k$), vol (vega $\times \Delta\sigma$), theta, new trades, residual; by book/product; reconcile.
- Portfolio construction: single source of truth; views; what-if; optional optimization.
- Periodic: daily/weekly/monthly/quarterly; process (data → run → validate → distribute); SLAs.
- Stress: historical (replay past) vs hypothetical (defined shocks); metrics ($V_s - V_0$, max loss, mean shortfall, by book, margin); report card.
- Configure: data, factors, buckets, params, limits, outputs. Calibrate: VaR, vol, correlation, curves, stress.
- Re-calibrate: FTR (proxy, spread, vol); power (vol, Asian, correlation, curve); gas (vol, correlation, storage); cross-asset.
- Policy change: capture → impact → implement → validate → communicate → cutover. Work with Risk.
- Liquidity: spread, depth, impact $(Q/V)^\alpha$; LVaR = VaR $+$ spread/2 $\times$ position $+$ impact.
- FTR liquidity: no continuous market; auction-based; LVaR long horizon, discount to mark; concentration.
- Liquidation: implementation shortfall; Almgren–Chriss; methods (shortfall, additive, scenario, stress).
- Firm impact: marginal VaR, correlation, decomposition, stress contribution, notional, liquidity; workflow.
- GRC: drivers (FTR, power, gas); related markets; present, charts, linkages, stress; support limits.
- Technology: automate (schedulers); maintain (version, monitor); enhance (data lake); research vs tech.
- Onboarding: data, models, limits, reporting, validation; new FTR region, new hub; Risk sign-off.
- Seasonality: curves, vol, demand, correlation, stress by season; power/gas/FTR.
- Python/SQL: NumPy, pandas, SciPy, viz, SQL; curves, VaR, pipelines.
- Advanced Python: venv, pin deps; Git, pytest, CI; multi-processing (CPU vs I/O); release from tag.
- Systematic: universe, strategy tag; notional, VaR by strategy, factor betas, correlation.
- Factor/PCA: factor VaR; PCA on curve/returns; P&L and VaR decomposition (Euler).
- ML: power (LMP, load, vol); gas (hub/basis, storage); FTR (spread, proxy, scenario); validate, interpretability.
- LP/IP: SCED = LP (LMPs, congestion); UC = MIP; gas flow = LP; FTR clearing = LP (PTDF); SFT; risk use.

---

## Abbreviations

- **BOM** balance-of-month; **DAM** day-ahead market; **RT** real-time; **DART** day-ahead–real-time spread.
- **LMP** locational marginal price; **CRR** congestion revenue right (ERCOT FTR); **ARR** allocation revenue right (PJM).
- **PTDF** power transfer distribution factor; **SFT** simultaneous feasibility test; **SCED** security-constrained economic dispatch; **UC** unit commitment.
- **HPFC** hourly price forward curve; **LSMC** least-squares Monte Carlo.
- **CVA** credit valuation adjustment; **PFE** potential future exposure; **UMR** uncleared margin rules; **CSA** credit support annex; **VM/IM** variation/initial margin.

---

## Key equations (LaTeX reference)

- Forward: $F(t,T) = \mathbb{E}^Q[S_T \mid \mathcal{F}_t]$. Discount: $P(t,T)$.
- Black-76 call: $C = P(t,T)(F_0 N(d_1) - K N(d_2))$, $d_1 = \frac{\ln(F_0/K) + \sigma^2 T/2}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$.
- Put-call: $C - P = e^{-rT}(F-K)$. Butterfly: $\frac{\partial^2 C}{\partial K^2} = e^{-rT}\varphi(K) \geq 0$.
- VaR: $\mathrm{VaR}_\alpha(L) = -q_\alpha(L)$. ES: $\mathrm{ES}_\alpha = \mathbb{E}[-L \mid -L \geq \mathrm{VaR}_\alpha]$.
- OU: $\mathrm{d}X = \kappa(\theta - X)\,\mathrm{d}t + \sigma\,\mathrm{d}W$; $\mathbb{E}[X_T\mid X_t] = \theta + (X_t-\theta)e^{-\kappa(T-t)}$; $\mathrm{Var}(X_T\mid X_t) = \frac{\sigma^2}{2\kappa}(1-e^{-2\kappa(T-t)})$.
- Nelson–Siegel: $y(\tau) = \beta_0 + \beta_1 \frac{1-e^{-\tau/\lambda}}{\tau/\lambda} + \beta_2\bigl(\frac{1-e^{-\tau/\lambda}}{\tau/\lambda} - e^{-\tau/\lambda}\bigr)$.
- SABR: $\mathrm{d}F = \sigma F^\beta\,\mathrm{d}W_1$, $\mathrm{d}\sigma = \nu\sigma\,\mathrm{d}W_2$.
- Sklar (copula): $F(\mathbf{x}) = C(F_1(x_1),\ldots,F_d(x_d))$.
- Attribution: curve $\approx \sum_k \Delta_k \Delta F_k$; vol $\approx \mathcal{V}\Delta\sigma$; residual = actual $-$ attributed.
- LVaR: $\mathrm{VaR} + \frac{\mathrm{spread}}{2}\times \mathrm{position} + \mathrm{impact}$; impact $\propto (Q/V)^\alpha$.
- Stressed P&L: $V_s - V_0$. Mean shortfall: $\mathrm{avg}\{(V_s - V_0) : V_s - V_0 < 0\}$.
- Component VaR (Euler): $\mathrm{component}_i = w_i \times \frac{\partial\mathrm{VaR}}{\partial w_i}$; $\sum_i \mathrm{component}_i = \mathrm{VaR}$.
- HPFC no-arb: $\frac{1}{|B|}\sum_{h \in B} P_h = F_B$ for each traded block $B$.
- Exception rate: $\hat{p} = N/T$; binomial test vs $p_0$ (e.g. $0.01$ for 99% VaR).
- Asian (arithmetic): $A = \frac{1}{n}\sum_{i=1}^n S_{t_i}$; payoff $(A-K)^+$.
- Location basis: $B = F_{\mathrm{loc}} - F_{\mathrm{hub}}$; $F_{\mathrm{loc}} = F_{\mathrm{hub}} + B$.
- Marginal VaR: $\frac{\partial\mathrm{VaR}}{\partial w_i}$ or $\mathrm{VaR}(\mathrm{with}) - \mathrm{VaR}(\mathrm{without})$.
- Market impact (power law): $\mathrm{impact} \propto (Q/V)^\alpha$, $\alpha \approx 0.5$.
- Two-factor (Schwartz–Smith): $\ln S_t = x_t + \xi_t$; $x_t$ OU (short-term), $\xi_t$ drift+vol (long-term).

### Greeks signs (vanilla European options)

| Greek | Long call | Short call | Long put | Short put |
|-------|-----------|------------|----------|-----------|
| **$\Delta$** (Delta) | $+$ | $-$ | $-$ | $+$ |
| **$\Gamma$** (Gamma) | $+$ | $-$ | $+$ | $-$ |
| **$\mathcal{V}$** (Vega) | $+$ | $-$ | $+$ | $-$ |
| **$\Theta$** (Theta) | $-$ | $+$ | $-$ | $+$ |
| **$\rho$** (Rho) | $+$ | $-$ | $-$ | $+$ |
| **Vanna** | $\pm$ | $\mp$ | $\pm$ | $\mp$ |
| **Volga** | $+$ | $-$ | $+$ | $-$ |

*Vanna is position-dependent; volga: long option $+$, short $-$.*

---

## Hedging basis risk in power portfolios (incl. PCA)

- **Basis risk** = mismatch between the price exposure you have (e.g. at a specific node or shape) and the price of the hedge (e.g. hub, index, or block). Your P&L moves with *your* price; the hedge moves with the *hedge* price; the difference is basis.
- **In power:** Common cases: **(1)** *Location basis* — you have load or generation at node A but hedge with hub/index H; basis = $P_A - P_H$. **(2)** *Shape basis* — you have an hourly or block profile but hedge with 7×24 or peak/off‑peak; the profile of your exposure doesn’t match the hedge. **(3)** *Product/tenor basis* — e.g. DAM vs RT (DART), or monthly vs daily; you’re exposed to one, you hedge with another.
- **Hedging idea:** Reduce basis risk by making the hedge’s price move as close as possible to your exposure. That means: **(1)** *Match location* where possible (e.g. node‑specific products or proxies). **(2)** *Match shape* using an HPFC and hedging by block or hour so the hedge profile matches your volume profile. **(3)** *Match tenor/product* (e.g. hedge DAM exposure with DAM products). **(4)** When you can’t match exactly, *explain and limit* residual basis (stress it, put it in VaR, set limits).
- **PCA (Principal Component Analysis) for basis and hedging:** PCA finds a small number of **factors** that explain most of the variance in a set of prices (e.g. many nodes, or many hours, or hub + basis series). **(1)** Run PCA on *returns* or *price levels* of your exposure and hedge candidates (e.g. hub, key nodes, indexes). **(2)** The first few PCs (e.g. level, slope, curvature) describe the main joint moves. **(3)** *Hedge the factor exposure:* if your portfolio’s P&L is mainly sensitive to PC1 (e.g. “system‑wide level”), hedge with a product that loads on PC1 (e.g. hub). **(4)** *Measure residual basis:* the part of your exposure that loads on higher PCs or is orthogonal to the hedge; that’s the basis you can’t easily hedge with liquid instruments. **(5)** Use PCA to choose *which* hub or index best reduces variance (the one that aligns with the dominant PCs of your exposure), or to build a *synthetic hedge* from several products (e.g. hub + one or two node spreads) that replicates the first 2–3 PCs. In practice: PCA on historical node/hub (and optionally shape) returns → factor loadings → hedge notionals so that net factor exposure is small → residual = basis risk; monitor and stress that residual.

---

## Loss modeling in LMP (other ISOs)

- **Why a loss component:** Transmission dissipates roughly **2–3%** of energy as heat. Delivering 1 MWh at a distant or high-loss node requires more than 1 MWh to be injected somewhere; the **marginal cost of losses** is the value of that extra energy. So LMP is usually decomposed as
  $$\mathrm{LMP} = \lambda + \text{(loss component)} + \text{(congestion component)}$$
  (sign conventions differ by ISO).
- **Common building blocks:** **(1)** *Reference (slack) bus* — one bus is the price reference; loss component at other buses is computed relative to it (reference bus often has zero loss component by design). **(2)** *Loss penalty factor (LPF)* or *delivery factor* — how much additional system loss (or delivery) results from a 1 MW injection at that bus. **(3)** *Marginal loss distribution factors (MLDF)* or similar — sensitivity of total system losses to injection/withdrawal at each bus, used inside the market OPF. **(4)** *DC vs AC* — many ISOs use **DC optimal power flow** (DCOPF) for speed; losses are then **approximated** (e.g. piecewise linear, pre-calculated loss factors, or loss sensitivity matrices). **AC OPF** models losses more accurately but is computationally heavier; some markets use AC or hybrid methods for day-ahead and DC for real-time.
- **By ISO (brief):**
  - **PJM:** $\mathrm{LMP} = \lambda + \text{congestion} + \text{loss}$. Loss component from **marginal loss factors** (loss penalty factors) relative to the reference bus; computed in the market solution (DCOPF with loss representation). Loss component can be positive or negative by location.
  - **MISO:** Three-part LMP: $\mathrm{LMP} = \lambda + \text{loss} + \text{congestion}$. Loss component derived from **loss modeling in the market optimization** (reference-bus-based); similar idea to PJM.
  - **CAISO:** $\mathrm{LMP}_i = \mathrm{SMEC}_r + \mathrm{MCC}_i + \mathrm{MCL}_i$ — System Marginal Energy Cost at reference bus $r$, Marginal Congestion Cost at bus $i$, and Marginal Cost of Losses at $i$. Loss component $\mathrm{MCL}_i$ is the marginal cost of supplying an extra MWh at bus $i$ accounting for losses between reference and $i$.
  - **NYISO:** $\mathrm{LBMP} = \text{Energy} + \text{Loss} - \text{Congestion}$ (sign convention: congestion is subtracted). Loss component uses **delivery factors**: at a gen bus,
    $$\mathrm{DF} = 1 - \frac{\text{incremental NYCA losses}}{\text{increment of injection at that bus}}.$$
    $\mathrm{DF} > 1$ → injection reduces system loss → **positive** loss price; $\mathrm{DF} < 1$ → increases loss → **negative** loss price. Loss component is part of the LBMP formula and is published with energy and congestion.
  - **ISO-NE:** Three-component LMP: $\mathrm{LMP} = \lambda + \text{loss} + \text{congestion}$. Loss component from **loss factors** relative to the reference bus, computed in the nodal market solution.
  - **ERCOT (contrast):** ERCOT’s **real-time LMP** has historically been $\mathrm{LMP} = \lambda + \sum_k \mu_k \,\mathrm{SF}_k$ (System Lambda $\lambda$ plus congestion: shadow prices $\mu_k$ × shift factors $\mathrm{SF}_k$). **Marginal losses** have not been included as a separate LMP component in the same way as in PJM/MISO/CAISO/NYISO/ISO-NE; ERCOT has studied adding marginal losses to market pricing (e.g. PUCT request, benefits analysis). So when comparing “how loss is modeled in other ISOs,” the Eastern ISOs and CAISO typically **do** include an explicit **loss component** in LMP; ERCOT is the notable case where LMP has been energy + congestion (with loss treatment differing or deferred).
- **Practical takeaway:** In ISOs that include it, the **loss component** makes $\mathrm{LMP}$ at a node reflect the full marginal cost of serving that node ($\lambda + \text{loss cost} + \text{congestion}$). It affects **settlement** (you pay or receive the full LMP including loss), **hedging** (CRRs/FTRs may or may not include loss; check each ISO), and **risk** (loss component adds locational spread and volatility). When valuing or hedging across regions, note whether the market uses a three-part LMP with loss or a two-part (energy + congestion) like ERCOT.

---

## Three methods for VaR calculation (general)

- **Definition:** $\mathrm{VaR}_\alpha(L) = -q_\alpha(L)$ is the **$\alpha$-quantile of the loss distribution** (e.g. 1-day 99% VaR = loss level that is exceeded with probability $1-\alpha = 1\%$). Loss $L$ is typically P\&L or change in portfolio value (so positive $L$ = loss).

### 1. Historical (simulation) VaR

- **Idea:** Use the **empirical distribution** of past P\&L. No parametric assumption on returns or factors.
- **Steps:** (1) Choose a lookback window (e.g. 500 days). (2) For each date $s$ in the window, compute 1-day P\&L (e.g. $L_s = V_{s-1} - V_s$ or revalue portfolio at $s$ and $s-1$). (3) Order the P\&L series (losses = positive). (4) VaR at confidence $\alpha$ = the $\alpha$-quantile of this series (e.g. 99% VaR = 99th percentile of losses, or equivalently the 1st percentile of P\&L).
- **Formula (conceptually):** $\widehat{\mathrm{VaR}}_\alpha = -\widehat{q}_\alpha(\{L_s\})$ where $\widehat{q}_\alpha$ is the sample quantile (e.g. linear interpolation between order statistics).
- **Pros:** No distributional assumption; captures realized correlations and fat tails in the data. **Cons:** Limited tail information (only as many tail points as history); past may not represent future; sensitive to lookback length; no scenario flexibility.

### 2. Parametric (variance–covariance) VaR

- **Idea:** Assume **returns (or risk-factor changes) are jointly normal** (or another parametric family). VaR follows from the quantile of that distribution.
- **Single position / single factor:** If P\&L (or return) is normal with mean $\mu$ and variance $\sigma^2$, then $\mathrm{VaR}_\alpha = -(\mu + \sigma\,\Phi^{-1}(1-\alpha))$ (often $\mu \approx 0$ for short horizon), so $\mathrm{VaR}_\alpha \approx \sigma\,\Phi^{-1}(\alpha)$ for the loss side (with $\Phi^{-1}(\alpha) < 0$ for $\alpha < 0.5$). For 99%, $\Phi^{-1}(0.01) \approx -2.33$, so $\mathrm{VaR}_{0.99} \approx 2.33\,\sigma$.
- **Portfolio:** If P\&L is $L = \mathbf{\Delta}^\top \mathbf{R}$ (deltas × factor returns) and $\mathbf{R} \sim N(\boldsymbol{\mu},\Sigma)$, then $L$ is normal with mean $\mathbf{\Delta}^\top\boldsymbol{\mu}$ and variance $\mathbf{\Delta}^\top \Sigma \mathbf{\Delta}$; VaR = quantile of that normal.
- **Formula:** $\mathrm{VaR}_\alpha = -(\mathbf{\Delta}^\top\boldsymbol{\mu} + \sqrt{\mathbf{\Delta}^\top \Sigma \mathbf{\Delta}}\;\Phi^{-1}(1-\alpha))$; often $\boldsymbol{\mu}=\mathbf{0}$ → $\mathrm{VaR}_\alpha = \sqrt{\mathbf{\Delta}^\top \Sigma \mathbf{\Delta}}\;\Phi^{-1}(\alpha)$ (taking the positive number for the loss quantile).
- **Pros:** Fast; analytic; easy to decompose (marginal/component VaR). **Cons:** Normality underestimates tail risk (fat tails, skew); no non-linear payoffs unless approximated (e.g. delta-only); $\Sigma$ and $\boldsymbol{\mu}$ must be estimated (estimation error).

### 3. Monte Carlo VaR

- **Idea:** **Simulate** many possible paths of risk factors (or returns) from a chosen model; **revalue** the portfolio under each scenario; VaR = empirical quantile of the simulated P\&L distribution.
- **Steps:** (1) Specify a model for risk factors (e.g. joint normal, $t$, or time series with vol/correlation). (2) Estimate parameters (e.g. $\Sigma$, degrees of freedom, or GARCH). (3) Draw $N$ scenarios $\mathbf{R}^{(1)}, \ldots, \mathbf{R}^{(N)}$ (e.g. Cholesky of $\Sigma$, or copula + marginals). (4) For each scenario, compute P\&L $L^{(i)}$ (full revaluation: $L^{(i)} = V_0 - V(\mathbf{R}^{(i)})$ or delta–gamma approximation). (5) VaR = sample $\alpha$-quantile of $\{L^{(1)}, \ldots, L^{(N)}\}$.
- **Formula (conceptually):** $\widehat{\mathrm{VaR}}_\alpha = -\widehat{q}_\alpha(\{L^{(i)}\}_{i=1}^N)$.
- **Pros:** Can use **fat-tailed** or **non-normal** distributions (e.g. $t$, copulas); **full revaluation** for options (gamma, vega); stress scenarios and custom dependencies. **Cons:** Computationally heavier; **model risk** (choice of distribution and parameters); variance of the VaR estimate (simulation noise) unless $N$ is large.

---
