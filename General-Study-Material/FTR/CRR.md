# CRR (Congestion Revenue Rights)

## Course audience

The material is for anyone who wants to **participate in CRR markets** or **buy Point-to-Point (PTP) Obligations** in the Day-Ahead Market.

**CRR markets** include:
- CRR **allocation**
- CRR **auction**
- **Bilateral trading** of CRRs

**Typical audience:**
- **CRR Account Holders** – hold and trade CRRs
- **Non-Opt In Entities (NOIEs)** – eligible for pre-assigned CRRs
- **Qualified Scheduling Entities (QSEs)** – buy PTP Obligations in the Day-Ahead Market (DAM)

## Course objectives

After the course you will be able to:

1. **Participate** – Identify what you and your company need to do to participate in the CRR market.
2. **Processes** – Explain CRR market processes and components: the **CRR auction**, **trades**, and **credit requirements**.
3. **Financial outcomes** – Describe how CRRs are **financially settled** in ERCOT markets and the possible financial outcomes of holding CRRs.

## Course modules

The course is split into 6 modules. Modules 2–4 go deeper into topics introduced in the fundamentals.

1. **Fundamentals of Congestion Revenue Rights** – End-to-end overview: what CRRs are, pricing, and how to acquire and use them.
2. **CRR Auction & Allocation Processes** – How CRRs are offered and allocated.
3. **Trading of CRRs** – Bilateral buying and selling of CRRs.
4. **Day-Ahead Market Point-to-Point Obligations** – Acquiring PTP Obligations in the DAM.
5. **Credit Limits** – How ERCOT credit limits are calculated and how credit is used when buying CRRs in the auction or PTP Obligations in the DAM.
6. **CRR Settlements** – How CRRs are financially settled in ERCOT markets.

## Fundamentals of CRR (Module 1)

**Module objectives** – After this module you will be able to:

1. **Locational Marginal Prices (LMPs)** – Describe the basics of how LMPs work.
2. **Congestion cost exposure** – Explain how congestion creates cost exposure in ERCOT’s market design.
3. **Types of CRRs** – Describe the types of Congestion Revenue Rights available to **hedge** that congestion cost exposure.

**What are CRRs?** **Congestion Revenue Rights** are **financial instruments** that entitle the owner to a **payment or a charge** when the transmission grid is congested in the **Day-Ahead Market**. They give the owner rights to (a share of) the **Congestion Rent** pool. CRRs are the **primary tool for hedging congestion costs** in ERCOT. Important: **A CRR is not a right to deliver physical energy or use physical transmission**—it is purely financial. **Uses:** (1) **Financial hedge**—price certainty; lock in congestion cost at the CRR purchase price; pay for congestion in advance to hedge exposure from energy positions. (2) **Financial investment**—speculative; owner seeks return; profitable when **Congestion Rent received > CRR purchase price**.

### Types of CRRs

All CRRs in ERCOT are **Point-to-Point (PTP)**. Each is defined by a **source** (point of injection) and a **sink** (point of withdrawal); both must be **Settlement Points** (e.g. source = resource node, sink = load zone). **Settlement** = payment or charge based on the **difference between Settlement Point Prices at sink and source**. Two instruments: **Point-to-Point Options** and **Point-to-Point Obligations**.

**Point-to-Point Options:** Hedge that can **only result in a payment** (never a charge). For each hour in the DAM, value = **Sink SPP − Source SPP**. If positive → owner receives that amount per MW; if negative → **payment = $0** (option does not pay when sink price is below source). Example: Source $5, Sink $10 → $5/MW payment; Source $15, Sink $10 → $0.

**Point-to-Point Obligations:** Hedge that may result in a **payment or a charge**. Same valuation: **Sink SPP − Source SPP** per hour. If positive → owner receives payment; if negative → owner pays a charge. Example: Source $5, Sink $10 → $5/MW payment; Source $15, Sink $10 → $5/MW charge.

**Acquiring CRRs:** Three ways—(1) **CRR Auction** (most CRRs); (2) **Allocation** (special cases, e.g. municipal utilities, electric cooperatives); (3) **Bilateral trades**.

**CRR Account Holder:** To own CRRs (however acquired), a company must **register and qualify** as a CRR Account Holder. Only a CRR Account Holder may own CRRs (a company can hold other registrations, e.g. QSE, LSE). Requirements: CRR Account Holder Application and Standard Form Agreement; bank account information (for ERCOT settlements); demonstrate capability to perform Account Holder functions (bids/offers, portfolio management); satisfy ERCOT **creditworthiness** requirements.

**Hedging example (Day-Ahead):** QSE buys 5 MW in the DAM for delivery to Load Zone; as CRR Account Holder it owns 5 MW PTP Option (source = Resource Node A, sink = Load Zone). **No congestion:** all nodes $20/MWh → energy cost $100, PTP payment $0, net $100. **With congestion:** Load Zone $25, Node A $20 → energy cost $125, PTP Option pays (25−20)×5 = $25 → **net $100** (same as buying at source; hedge offsets congestion). The PTP Option was purchased in the CRR Auction—congestion cost is effectively paid upfront there to lock in the hedge.

**Real-Time congestion hedging:** If the QSE buys forward energy at a settlement point other than its Load Zone (e.g. 5 MW trade at Resource Node A, 5 MW load at Load Zone), it is exposed to **RT congestion**: paid at Node A price, charged at Load Zone price. No congestion (all $30) → payment $150, charge $150, exposure $0. With congestion (Node A $30, Load Zone $40) → payment $150, charge $200, **exposure $50**. Hedge: buy a **Day-Ahead Market PTP Obligation** (source = Node A, sink = Load Zone). In RT it pays (40−30)×5 = $50 → offsets exposure; **net RT cost $0**. Congestion cost was paid in DAM (e.g. $25) instead of $50 in RT.

**Day-Ahead Market PTP Obligations:** Financial instruments bought **in the DAM** (at the DAM price spread between source and sink) and **settled in Real-Time** (at the RT price spread). Hedge against **RT congestion** or against **change in congestion between DAM and RT**. Use as **financial hedge** (lock in RT congestion cost at DAM prices) or **financial investment** (speculate; profit when RT value > purchase price). **Only QSEs** may participate in the DAM, so only QSEs can buy DAM PTP Obligations. QSE registration: application, bank info, capability (bids/offers, communications), creditworthiness—analogous to CRR Account Holder.



### Settlement points

All energy in the ERCOT market is settled at one of **three types of settlement points**:

1. **Resource nodes** – Points where generation or supply connects to the grid.
2. **Load zones** – Geographic zones (e.g. regions of Texas) where load is aggregated.
3. **Hubs** – Aggregated or reference points used for trading.

**Each settlement point has its own Settlement Point Price.** These prices can differ a lot depending on conditions on the transmission grid (congestion, losses, etc.). That variation is what creates congestion cost exposure and makes CRRs useful as hedges.

### Locational Marginal Pricing (LMP)

**What is LMP?** The name spells it out:

- **Pricing** – A **cost**.
- **Marginal** – Cost to serve the **next increment of load** (however small).
- **Locational** – At a **specific location**: an **electrical bus**.

So: **LMP = cost to serve the next increment of load at an electrical bus.**

An **electrical bus** is a point of interconnection in the ERCOT transmission system (a node). Buses can be:

- **Load buses** – Generally load substations.
- **Generation resource buses** – Where generators connect to the transmission system.
- **Hub buses** – 345 kV buses that make up a hub; many forward energy transactions are scheduled there.
- **Other buses** – No load, no generation, not part of a hub; just interconnection points.

**LMP components:** Two—**energy** (marginal cost to match generation and load system-wide) and **congestion** (change in marginal cost at a node when the system is congested). No congestion → same price at all nodes. With congestion → prices differ; import-constrained areas tend to see higher LMPs, export-constrained areas lower.

**Losses:** Some markets put a loss component in LMP. **ERCOT does not:** losses are not in LMPs; ERCOT reflects them by adjusting metered load volumes.

![LMP-Scenario](LMP-Scenario.png)

**LMP example (simplified):** 20 MW load; Gen 1 (20 MW @ $20), Gen 2 (20 MW @ $10), Gen 3 (40 MW @ $30). Transmission limits: 5 MW on path from Gen 2 toward load, 10 MW between hub and load bus. Dispatch: cheapest first → Gen 2 clears 5 MW (limit); Gen 1 clears 5 MW; Gen 3 clears 10 MW (total 20 MW). **LMP at 345 kV Hub bus = $20** (marginal unit there is Gen 1). **LMP at 69 kV Load bus = $30** (marginal unit there is Gen 3). Congestion causes **price separation** between hub and load even when they are electrically close—this is what CRRs hedge.

**Congestion rent:** With congestion, **charges to buyers > payments to sellers** (e.g. load pays $600; gens receive $450; **$150 surplus**). This surplus is called **Congestion Rent**. In ERCOT, **Day-Ahead Market congestion rent funds Congestion Revenue Rights (CRRs)**—CRR holders are paid from this pool.

**Congestion cost exposure:** When LMPs vary (congestion), Settlement Point Prices at resource nodes, hubs, and load zones also diverge. That **price separation** exposes **load** (pays more at its load zone) and **resources** (lost opportunity when their node price is below what load pays). Exposure can arise in the DAM or in Real-Time (e.g. load buying at a settlement point other than its load zone; resource selling at a point other than its resource node). **ERCOT provides tools to hedge these congestion costs**—CRRs are the main one.

Understanding LMPs is required to understand how Settlement Point Prices (and thus CRRs) work.

### Settlement Point Prices and LMPs

Settlement Point Prices are **calculated from Locational Marginal Prices (LMPs)**. The formula depends on the type of settlement point:

- **Resource node** – Time-weighted average of LMPs at that resource node.
- **Load zone** – Time-weighted and **load-weighted** average of LMPs at all load buses in the zone.
- **Hub** – Time-weighted and **simple** average of LMPs at the hub’s defined buses.

**Real-Time vs Day-Ahead:** In Real-Time, time-weighting is used to build 15-minute Settlement Point Prices from 5-minute LMPs. In the **Day-Ahead Market**, where **CRRs are cashed in**, Settlement Point Prices and LMPs are both **hourly**, so time-weighting effectively drops out.


### Module summary (Fundamentals)

In this module you learned about:

1. **The basics of LMPs** – and how they drive Settlement Point Prices.
2. **Congestion cost exposure** in ERCOT markets – who is exposed (load, resources) and when (DAM, RT).
3. **Financial instruments for hedging congestion costs** – CRRs (PTP Options, PTP Obligations from auction/allocation/trade), CRR Account Holder requirements, and Day-Ahead Market PTP Obligations (QSE-only, bought in DAM, settled in RT).

---
## Auction & Allocation Process

### Congestion Revenue Rights Life Cycle

CRRs are acquired in **three ways**; all three feed into the **Day-Ahead Market**. From there, **CRRs** are settled in the DAM and **DAM PTP Obligations** (bought in the DAM) are settled in **Real-Time Operations**.

**Roles:** CRRs from **Auction**, **Allocation**, and **Trades** are owned by **CRR Account Holders**. **Point-to-Point Obligations** may also be bought **in the Day-Ahead Market** (DAM PTP Obligations) to realize or hedge congestion value. **Only QSEs (Qualified Scheduling Entities)** may buy products in the Day-Ahead Market; **most CRR Account Holders are also registered as QSEs**, so companies can use both CRRs and DAM PTP Obligations. DAM PTP Obligations, once purchased in the DAM, are **cashed out in Real-Time Settlements** for the following operating day.

1. **Allocation**
   - **Pre-Assigned CRRs (PCRRs)** are allocated to **NOIEs** (Municipal Utilities and Electric Cooperatives).
   - Allocation occurs **prior to the CRR Auction**.
   - These CRRs then enter the same settlement path as auction- and trade-acquired CRRs.

2. **CRR Auction**
   - The **majority of CRRs** are acquired here.
   - Participants submit **bids to buy** and **offers to sell**.
   - **Monthly auctions** – CRR Account Holders buy and sell CRRs for the **upcoming month**.
   - **Semi-annual auctions** – Participants buy and sell CRRs for **multiple months**, up to **two years** in the future.

3. **CRR Trades**
   - **Bilateral transactions** between **CRR Account Holders** that transfer CRR ownership from one holder to another.
   - Trades add a third acquisition path; CRRs acquired through trades also flow to the Day-Ahead Market for settlement.

4. **Day-Ahead Market**
   - **Daily settlement of CRRs** – All CRRs (from allocation, auction, or trade) are **cashed out in the Day-Ahead Market** on a daily basis using **DAM prices** over the period they are owned.
   - **Buy DAM PTP Obligations** – QSEs may also **buy Point-to-Point Obligations in the DAM** (at the DAM spread); these instruments are then settled in Real-Time (see below).

5. **Real-Time Operations**
   - **Settlement of DAM PTP Obligations** – PTP Obligations purchased in the Day-Ahead Market are **settled in Real-Time** (payment or charge based on the **RT** spread between sink and source) for the **following operating day**.

This life cycle is built on in later modules (e.g. CRR Network Model, Pre-Assigned CRR impact, auction inputs/process/outputs, trading of CRRs).

### Availability of Congestion Revenue Rights

CRRs are available through **monthly** and **semi-annual** auctions.

**Timing of auctions**

- **Monthly**
  - Typically run **two to three weeks before the first day** of the month in which the CRRs are active.
  - CRR Account Holders buy and sell CRRs for the **upcoming month**.

- **Semi-annual (Long Term Auction Sequence)**
  - **Four successive auctions**, each covering a **six-month period** (January–June or July–December).
  - Sequence: auction the 1st six-month period → wait about a week → auction the 2nd six-month period → wait about a week → auction the 3rd six-month period → wait about a week → auction the 4th six-month period.
  - When the sequence is complete, ERCOT has auctioned CRRs for **up to two years** in the future.

*Exact dates are on the **CRR Activity Calendar** at [ercot.com/mktinfo/crr](http://www.ercot.com/mktinfo/crr).*

**Available capacity**

CRRs are **financial** instruments, but their **availability is limited by the physical capacity** of the ERCOT transmission system.

- **Monthly auction**
  - ERCOT makes **90%** of transmission capacity available for CRRs in the monthly auction.
  - The 90% cap allows for **unplanned outages** and operational headroom.

- **Long-term auction sequence**
  - For the four successive six-month periods, ERCOT further limits how much capacity can be committed to CRRs:
    - **60%** for the first six months
    - **45%** for the second six months
    - **30%** for the third six months
    - **15%** for the fourth six months
  - These percentages apply to capacity **including** what was already auctioned or allocated in earlier periods.

- **Example:** If long-term auction sequences have already sold CRRs using **50%** of transmission capacity, the **monthly auction** for a given month (e.g. February) has only **40%** of capacity left (90% − 50% = 40%).

Conceptually, transmission paths can be shown as **available** (e.g. capacity still open for CRRs) or **consumed** (capacity already committed to CRRs or out of service).

### CRR Allocation — Pre-Assigned CRRs (PCRRs)

The **CRR Allocation** process distributes **Pre-Assigned CRRs (PCRRs)** to eligible **Non-Opt-In Entities (NOIEs)**.

**Who receives PCRRs**
- **NOIEs** – **Municipally Owned Utilities** or **Electric Cooperatives** that have **not** opened their service areas to retail competition.
- **Eligibility:** NOIEs must have **long-term supply contracts in place prior to September 1, 1999**.

**Allocation**
- **Allocated to NOIEs** on a **monthly** or **annual** basis (even with the Long-Term Auction Sequence).
- **Based on long-term supply contracts.**

**Cost**
- **Cost is based on the auction clearing price**, but is **5% to 20%** of the clearing price, depending on the nature of the long-term supply contract.
- When allocated **for a year**, PCRRs are **charged in two installments**; prices from the **Long-Term Auction Sequences** are used to determine what NOIEs pay.

**Simultaneous Feasibility Test (SFT)**

The **Simultaneous Feasibility Test (SFT)** confirms that the transmission system can **support an awarded set of CRRs** during **normal system conditions**.

- **Process:** A **DC power-flow model** is used for simplicity. CRRs are treated as **injections and withdrawals** at the appropriate **settlement points**; the model checks that the resulting flows respect transmission limits.
- **When SFT is used:**
  - **During allocation** – To **validate the requested allocation of PCRRs** before the **Monthly** and **Long-Term Auctions**.
  - **Prior to each Day-Ahead Market** – To ensure the **awarded set of CRRs and PCRRs** is still **feasible** for that **operating day**.

So SFT is used both to approve allocation requests and to re-check feasibility before daily DAM settlement.

**Impact of allocation on auction capacity**

Pre-Assigned CRR allocation takes place **before** the CRR Auction that covers the **same period**. As a result:

- **Eligible NOIEs have first rights** to the available transmission capacity to support their PCRRs.
- **Only after** NOIEs have received their allocated PCRRs is the **remaining** transmission capacity made available to the **CRR Auction**.

So the sequence is: (1) **Possible transmission capacity available for allocation** (total capacity in the CRR Network Model); (2) **Allocation** of PCRRs to NOIEs; (3) **Possible transmission capacity available prior to the auction** (what is left); (4) **CRR Auction** uses that remaining capacity. This is why the auction sees less capacity than the full model—PCRRs have already claimed a portion.

### CRR Auction Process

The CRR Auction Process can be described in terms of **inputs**, the **CRR Auction Engine**, and **outputs**.

**Transmission capacity before and after the auction**

Transmission capacity is discussed here in the context of **capacity following the auction clearing process**. An initial **Allocation process** consumes a portion of transmission capacity (PCRRs to NOIEs), leaving the remainder **available prior to the auction**. Once the **monthly CRR Auction** has been completed and validated, **up to 90% of total transmission capacity** may be **booked against CRRs** for that particular month. So **possible transmission capacity available prior to the auction** (what remains after allocation) is relatively large; **possible transmission capacity available after the auction** is much smaller—many paths that had available capacity before the auction are now bound by awarded CRRs. This before/after contrast is why post-auction maps of “available” capacity show a sparser network: most capacity that can be committed to CRRs for the month has been committed by the auction (and allocation).

**Transmission capacity in the Day-Ahead Market**

CRRs sold or awarded in the **Auction** (and from Allocation and Trades) **settle in the Day-Ahead Market**. Because CRRs are **cashed out in the DAM**, the transmission capacity that was **booked against CRRs** for the month **becomes available again** in the Day-Ahead Market. In other words, the **Day-Ahead Market starts with a clean slate**: it can **re-book** that transmission capacity against **other financial transactions**, such as **Point-to-Point Obligations** (DAM PTP Obligations) and energy schedules. So:

- **CRRs purchased in the Auction are settled in the DAM** (daily settlement of CRRs as in the life cycle).
- **Settlement of CRRs "frees up" available network capacity for the DAM** — the same capacity that was committed to CRRs for the month is again available for the DAM to use for that operating day (e.g. for DAM PTP Obligations and energy).

Conceptually: **possible transmission capacity available after the auction** is the capacity still uncommitted to CRRs for the month; **possible transmission capacity available for the Day-Ahead Market** is the full capacity the DAM can use each day, because CRR settlement in the DAM releases the capacity booked against CRRs back into the pool the DAM clears against.

**Inputs (into the CRR Auction Engine)**
- **Bids** – Participants’ bids to **buy** CRRs.
- **Offers** – Participants’ offers to **sell** CRRs.
- **CRR Model** – Includes:
  - **Allocated CRRs** (e.g. PCRRs already assigned to NOIEs)
  - **Previously awarded CRRs** (from earlier auctions)
  - **Credit limits** (participant credit available for the auction)

**Constraints submitted by ERCOT**

The **CRR Model** and related inputs are **provided by ERCOT** and define the **constraints** the auction must respect:

- **Total transmission capacity** – The **CRR Model** (CRR Network Model) provides the **total transmission capacity** that may be bound by CRRs once the auction is complete. This is the physical/economic ceiling for CRR awards.
- **Transmission capacity already “owned”** – **Allocated CRRs** (e.g. PCRRs) and **Previously awarded CRRs** represent transmission capacity **already held** in the form of CRRs. That capacity is **already bound** and **unavailable** for this auction unless the current owner **offers** it (in which case it can be re-awarded to others).
- **Credit limit as budget constraint** – A CRR Account Holder’s **Credit Limit** acts as a **budget constraint** in the auction. The auction **never clears** CRRs in a way that **exceeds** a CRR Account Holder’s **Available Credit Limit**.

**Bids (detail)**

CRR Account Holders who wish to **purchase** CRRs submit bids through the **CRR Market User Interface**. A **CRR bid** represents a **willingness to buy** CRRs in a **Monthly** or **Long-Term** Auction.

- **Each bid must indicate:**
  - **Not-to-Exceed Price** – maximum price the participant is willing to pay ($/MW).
  - **Maximum MWs** of CRR the participant wishes to buy on a **specific path** (Source and Sink settlement points).
- **Path and timing:** The user selects **Source** and **Sink** settlement points from a dropdown (only valid names are accepted), and specifies **MWs**, **price**, and **Time-of-Use Block**. **Start date** and **End date** are typically auto-populated based on the selected auction.
- **Hedge type:** On the bid screen, **Buy/Sell** defaults to **Buy** and **Hedge Type** defaults to **OPT** (Option); the user may change Hedge Type to **Obligation (OBL)**.
- **PTP Option:** A bid to buy a **PTP Option** must have a **Not-to-Exceed Price greater than zero**.
- **PTP Obligation:** A bid to buy a **PTP Obligation** **may** have a **negative** Not-to-Exceed Price.
- **Bid limits (software):** The total number of bids allowed in the auction process is **capped at 300,000**. Each qualified CRR Account Holder is allowed a **maximum number of bids** equal to **300,000 divided by the number of qualified CRR Account Holders**.

**Offers (detail)**

A **CRR offer** represents a **willingness to sell** CRRs in a **Monthly** or **Long-Term** Auction.

- **Each offer must indicate:**
  - **Minimum Reservation Price** – the minimum price **per MW per hour** that the CRR Account Holder is willing to accept for the offered CRRs.
  - **Available quantity in MW** – the amount of CRRs (on a specific path, TOU, etc.) that the holder is offering to sell.
- **Only the Owner of Record can offer a CRR.** The CRR Account Holder must have **acquired** the CRR through a **previous process**, such as a long-term auction sequence or a **trade**. A **NOIE** may also **offer allocated PCRRs** into the auction process.

On the **offer screen** in the CRR Market User Interface, the holder **locates the CRR in their current portfolio** and **drags it into the editing screen**; that **prepopulates all fields except MW and Price**. The user then enters the **MWs they wish to offer** and the **price they are willing to accept**. **Only MW and Price are editable**—other fields (path, TOU, dates, hedge type, etc.) are not editable, as changing them would change the nature of the CRR. **Validation:** if the user tries to offer **more MW than they currently own**, the system **returns an error**.

**CRRs are auctioned or allocated in: one-month strips and Time-of-Use blocks**

Whether CRRs are **auctioned** or **allocated**, they are always **monthly instruments**. In Long-Term Auction Sequences, CRRs are offered as **collections of monthly instruments** across consecutive months. CRRs are also defined in **Time-of-Use (TOU) blocks**. When buying CRRs (auction or allocation), a CRR Account Holder obtains **one-month strips of TOU blocks**.

**Three Time-of-Use blocks in ERCOT:**

| TOU block       | Hours      | Days |
|-----------------|------------|------|
| **Peak Weekday**  | 0700–2200  | Monday through Friday, excluding ERCOT-defined holidays |
| **Peak Weekend**  | 0700–2200  | Saturday, Sunday, and ERCOT-defined holidays |
| **Off-Peak**      | 0100–0600 and 2300–2400 | Every day (Sunday through Saturday) |

So each CRR product is a **path** (Source–Sink) × **one month** × **one TOU block** (Peak Weekday, Peak Weekend, or Off-Peak).

**7×24 block bids in monthly auctions**

In **monthly auctions**, a CRR Account Holder may submit a bid that is **all-or-nothing** across the three TOU blocks: they buy **all three** Time-of-Use blocks on a path for the month, or **none**. This is called a **7×24 block bid**; it is treated as a **single bid** covering **all hours in the month**.

- **Awarded:** If **Bid Price ≥ weighted average (by hour) of all three TOU clearing prices** → the 7×24 block bid is **awarded**.
- **Not awarded:** If **Bid Price < weighted average (by hour) of all three TOU clearing prices** → the 7×24 block bid is **not awarded**.

So the bid clears only when the participant’s price is at or above the hour-weighted average of Peak Weekday, Peak Weekend, and Off-Peak clearing prices for that path and month.

**Example: 7×24 block bid clearing**

A CRR Account Holder enters a **7×24 bid** for a CRR from **Source A to Sink B** in the **monthly auction for February**. Bid price = **$6**. February has **672 hours** total: **224 Off-Peak**, **128 Peak Weekend**, **320 Peak Weekday**.

The three TOU clearing prices for CRR A–B are: **$2** (Off-Peak), **$3** (Peak Weekend), **$8** (Peak Weekday). The **weighted average price** (by hour) is:

(224×$2 + 128×$3 + 320×$8) / 672 = **$5.048**

Because the bid price **$6 ≥ $5.048**, the **7×24 block bid is awarded**.

**No 7×24 block bids in Long-Term Auction Sequences**

**Long-Term Auction Sequences do not allow 7×24 block bids.**

- **Monthly auctions:** All three TOU blocks are **cleared simultaneously**, so the auction can enforce “all three or nothing” and award 7×24 block bids when the bid price is at or above the weighted average.
- **Long-Term Auction Sequences:** Each **Time-of-Use block is cleared in a separate process** (separate optimization). Clearing all TOU blocks together would make the auction very slow or unsolvable. As a result, there is **no way to process** a bid that can only be fulfilled by clearing multiple TOU blocks together, so **7×24 block bids are not offered** in long-term sequences.

**Minimum bid price and auction fees (PTP Options)**

There are **no brokerage or clearing house fees** for buying CRRs in the auction. ERCOT does, however, set a **minimum bid price for Point-to-Point (PTP) Options**.

- **Minimum bid price for PTP Options:** Currently **$0.01/MW/hour**. This value is **reviewed by the ERCOT Technical Advisory Committee (TAC) annually**.
- **Clearing below minimum:** PTP Options **may clear at fractional prices or zero**. If an option clears **below** the minimum bid price, the **awarded CRR Account Holders pay an Auction Fee**.
- **Auction fee:** The fee is the **difference between the clearing price and the minimum price**. The result is that, regardless of the clearing price, the **total price to the awarded CRR Account Holder is $0.01/MW/hour** (clearing price + auction fee = $0.01/MW/hour when clearing is below minimum).

**CRR Auction Engine — Clearing Process**

The ERCOT CRR Auction uses a **single-round, simultaneous** auction clearing engine: **all available capacity** is released to the auction **at one time**, and **all bids and offers are cleared simultaneously** in one run.

- **Objective:** Maximize **net auction revenue**, i.e. **Maximize [Bid-based Value − Offer-based Cost]**, subject to applicable constraints. The engine does this by clearing the **highest-priced bids** and **lowest-cost offers** first, consistent with transmission and credit limits.
  - **Bid-based Value** = Sum of **(Bid Price × Cleared Bid Quantity)** over all cleared bids.
  - **Offer-based Cost** = Sum of **(Offer Price × Cleared Offer Quantity)** over all cleared offers.
- **Important:** In this step the auction uses **bid prices** and **offer prices**, **not clearing prices**. The engine is determining **award quantities** (how much to clear); **Auction Clearing Prices** are determined **afterward**.
- **Constraints:**  
  - **Transmission system limits** (from the CRR Model: total capacity, net of allocated and previously awarded CRRs).  
  - **Available Credit Limits** (no CRR Account Holder may be awarded CRRs in excess of their credit).

The engine matches bids and offers against this capacity and these limits and determines **which CRRs are awarded** and **at what clearing prices**. The result is a single set of **Auction Results** (postings, settlements) and **Data Transmitted Daily** (credit, settlements).



**Outputs**

After an auction, the **CRR Auction Engine** produces outputs that must be provided to the **Market** and other **ERCOT systems**.

- **Auction results**
  - **MIS postings** – Once a CRR Auction has been completed and validated, ERCOT posts results on the **Market Information System (MIS)**:
    - **MIS Public Area** (anyone may view): **Identities of awarded CRR Account Holders**; **Awarded CRRs** by Source–Sink, **TOU** block, total **MWs** awarded, **Clearing Prices**, and **Effective Dates**; **Binding constraints** from the auction, including modeled flow on the limiting elements. ERCOT also posts **all CRR auction bids and offers** used in the auction **without identifying** the CRR Account Holders who submitted them.
    - **MIS Certified Area** (per account holder): Each awarded Account Holder receives information specific to their company: **all of their awarded bids and offers** and the **unique identifiers** for their awarded CRRs.
  - **Settlements** – Auction results are also sent to the **ERCOT Settlement System** for proper **invoicing of CRR Account Holders** (payments/charges from the auction).
- **Data transmitted daily** – The CRR system sends data to other ERCOT systems **daily**:
  - **Credit** – The **ERCOT Credit Management System** needs **daily updates of CRR ownership** for **credit exposure** calculations.
  - **Settlements** – The **ERCOT Settlement System** **cashes out CRRs daily** in the **Day-Ahead Market** and also requires **daily ownership updates**.

*Summary (inputs → engine → outputs):* **Inputs:** Bids, Offers, CRR Model / Allocated CRRs / Previously Awarded CRRs / Credit Limits. **Outputs:** Auction Results (MIS Postings, Settlements); Data Transmitted Daily (Credit, Settlements).

The following sections (e.g. Modeling for Congestion Revenue Rights) describe how one key input—the **CRR Network Model**—is built and used.

### Modeling for Congestion Revenue Rights

Available capacity for each auction is determined from ERCOT’s **Network Operations Model**.

**ERCOT system capacity from the Network Operations Model**

- ERCOT’s **system capacity** (the basis for CRR availability) is determined from the **Network Operations Model**.
- The Network Operations Model reflects the **physical characteristics** of the ERCOT transmission system, including:
  - **Topology** – layout and interconnection of the grid
  - **Equipment ratings** – capacity and limits of lines, transformers, and other infrastructure
  - **Other operational limits** – constraints that affect how the system can be operated

**CRR Network Model**

- ERCOT does **not** use the Network Operations Model directly for CRRs. Instead it builds a **CRR Network Model** that is **derived from** the Network Operations Model.
- The **CRR Network Model**:
  - Is **derived from** the Network Operations Model
  - **Represents transmission capacity for each month**
- The goal is to take a model that is **updated daily** (the Operations Model) and **generalize** it so it represents **available transmission capacity for the entire month**, which is what is used for CRR auctions and awards.

**What the CRR Network Model reflects**

The CRR Network Model is built to represent the **most constraining conditions** over the month. It reflects:

1. **Transmission facilities** expected to be **in-service on the first day** of the specified month. System upgrades that enter service *during* the month are **not** included until the **following month**.
2. **Significant outages** – All scheduled outages expected to **significantly impact transfer capability** during the month. “Significant” includes:
   - Consecutive or continuous approved outages lasting **five days or more**
   - Approved outages involving **Transmission Elements in a 345 kV Transmission Facility**
   - Approved outages requiring a **Block Load Transfer (BLT)**
   - Any other approved outage ERCOT determines has **substantial risk of significant congestion**
3. **Dynamic ratings** – **Dynamic Ratings** of transmission elements, to the extent provided. ERCOT updates these based on **maximum forecasted temperatures** for the month.
4. **Monitored elements** – Only transmission elements **actively monitored** by ERCOT’s real-time security analysis. Elements not monitored (because no circumstances push them near limits) are excluded, since they would not impact system prices.
5. **Contingencies** – Certain **contingencies** from the Network Operations Model that, if they occurred, would **significantly impact congestion costs**. These contingency cases are used in the **auction clearing engine**.
6. **Settlement points** – **All valid Settlement Points** in ERCOT.

The result is a **single model for the entire month** aimed at capturing the most constraining conditions for CRR availability and pricing.


![Option-clearing](Option-clearing.png)

**Simple transmission model (for clearing examples)**

A **simple transmission model** is often used to illustrate the CRR clearing process:

- **Settlement points:** Six points, labeled **A, B, C, D, E, F**. CRRs are modeled as **injections** of power at a **Source** settlement point and **withdrawals** at a **Sink** settlement point.
- **Network topology:**  
  - There is **no direct link** from A to B. Power between **A and B** must flow **A → E → F → B**.  
  - There is **no direct link** from C to D. Power between **C and D** must flow **C → E → F → D**.
- **Transmission capacities:**  
  - **E–F:** **100 MW** (the central bottleneck).  
  - **All other paths** (A–E, C–E, F–B, F–D): **200 MW** each.

So A and C act as potential sources, B and D as potential sinks, and E and F form a central path with limited capacity (100 MW). These values are used in worked clearing examples to show how awards and shadow prices are determined.

**Example: Case 1 — Bids only**

Two account holders wish to **buy** PTP Option CRRs (no offers):

- **Ellen:** 150 MW from **A to B**, willing to pay **$20/MW**.
- **Jack:** 20 MW from **C to D**, willing to pay **$10/MW**.

Both paths **use the E–F link** (A→B flows A→E→F→B; C→D flows C→E→F→D). E–F has **100 MW** capacity, so at most 100 MW of combined A–B and C–D flow can be cleared. The auction **clears highest-priced bids first**: Ellen’s bid is prioritized. Ellen is awarded **100 MW** (capped by E–F); **Jack is awarded 0 MW** because no E–F capacity remains.

- **Optimal clearing:** Ellen 100 MW, Jack 0 MW.  
  **Bid-based value** = (100×$20) + (0×$10) = **$2000**. Offer-based cost = $0. **Net = $2000.** ✓  
- **Alternative:** 80 MW Ellen + 20 MW Jack would give (80×$20) + (20×$10) = $1800; worse than $2000, so the auction does not choose it.

Clearing prices (e.g. for A–B, C–D, and the binding constraint E–F) can both be **$20** in this setup, consistent with the marginal value of the binding capacity.

**Example: Case 2 — Bids only (reversed prices)**

Same two bidders and paths, but **bid prices are reversed**:

- **Ellen:** 150 MW **A to B**, now willing to pay **$10/MW**.
- **Jack:** 20 MW **C to D**, now willing to pay **$20/MW**.

The auction clears **highest-priced bids first**, so **Jack’s bid is cleared first**. Jack is awarded **all 20 MW** he requested (there is enough C–D capacity). Both paths use E–F; Jack’s award uses **20 MW** on E–F, leaving **80 MW** for Ellen. So **Ellen is awarded 80 MW** (not 100).

- **Optimal clearing:** Jack 20 MW, Ellen 80 MW.  
  **Bid-based value** = (20×$20) + (80×$10) = **$1200**. Offer-based cost = $0. **Net = $1200.** ✓  
- **Alternative:** Ellen 100 MW, Jack 0 MW would give 100×$10 = **$1000**; worse than $1200, so the auction does not choose it.

Clearing prices in this case are **$10** on A–B, C–D, and E–F (P_AB = P_CD = P_EF = $10). The **shadow price** on E–F is the marginal cost to make one more MW available on that link; it is used to determine these clearing prices.

**Example: Case 3 — Bids and offer**

**Naomi** holds 30 MW on the **E–F** path and **offers to sell** 30 MW at **$15/MW**. Ellen and Jack submit the same bids as in Case 2 (Ellen 150 MW A→B @ $10, Jack 20 MW C→D @ $20). Total E–F capacity is 100 MW; with Naomi’s 30 MW offered into the auction, the **capacity available for other awards** is effectively **70 MW** (the rest is tied to her offer). The auction maximizes **bid-based value minus offer-based cost**.

- **Solution 1:** Clear **20 MW of Naomi’s offer** (matched with Jack’s bid) and **70 MW of Ellen’s bid**. Bid-based value = (20×$20) + (70×$10) = $1100; offer-based cost = 20×$15 = $300; **net = $800**.
- **Solution 2 (optimal):** **Do not clear Naomi’s offer.** Jack 20 MW, Ellen **50 MW** (only 50 MW remains on E–F for Ellen once Jack takes 20). Bid-based value = (20×$20) + (50×$10) = $900; offer-based cost = $0; **net = $900.** ✓

So the **best solution** is **Jack 20 MW, Ellen 50 MW, Naomi 0 MW** (her offer is not cleared). **Clearing prices** are **$10** (P_AB = P_CD = P_EF = $10). The **shadow price** of **E–F** (the limiting element) is found by asking: what is the least cost to make one more MW available on E–F? **Dropping one MW of Ellen’s cleared bid** costs $10; **clearing one more MW of Naomi’s offer** costs $15. The **least cost is $10**, so the shadow price of E–F is **$10**, and that sets the clearing prices for paths that use E–F (A–B and C–D). Ellen pays $10 (her bid price); Jack pays $10 (less than his $20 bid); Naomi is not awarded because the clearing price $10 is **below** her $15 minimum reservation price.

**The shadow price**

**Shadow price** (economists’ definition): the **marginal cost to make an additional increment of a commodity available**.

In the **CRR Auction**, the **commodity** is **transmission capacity** (e.g. the capacity on the E–F path in the simple model). The **cost** of that increment **depends on the bids and offers** in the auction: it is the value that would be gained or given up if one more unit of that capacity were available. So the shadow price on a transmission link is the **marginal value** of that link in the clearing solution; it shows up as clearing prices for CRRs that use that link (as in Case 1, where the binding E–F link drives a $20 clearing price).

**Case 4: Bids and offer (Naomi’s 90 MW)**

Ellen and Jack bid as in earlier cases. **Naomi** already holds **90 MW** on the **E–F** path and **offers** that capacity at **$15/MW** in the auction. There are 100 MW on E–F in total, but only **10 MW** are “free” to the highest bidder; the other 90 MW are subject to Naomi’s offer (pricing constraint). Jack’s bid price is higher, so his bid is considered first.

- **Scenario 1:** Match Jack’s 20 MW bid with 20 MW of Naomi’s offer. That leaves 10 MW on E–F available to support Ellen’s bid.  
  - Bid-based value: (20×$20) + (10×$10) = $500; offer-based cost: 20×$15 = $300 → **net $200**.
- **Scenario 2 (optimal):** Do not clear Ellen’s bid. Clear Jack’s full 20 MW; only **10 MW** of Naomi’s offer need to be cleared (10 MW free on E–F for the highest bidder).  
  - Bid-based value: (20×$20) + (0×$10) = $400; offer-based cost: 10×$15 = $150 → **net $250**.

The auction maximizes **bid-based revenue minus offer-based cost**, so **Scenario 2** is chosen. **Awards:** Jack 20 MW, Naomi 10 MW (of her 90 MW offer), Ellen 0 MW. The cost to make one more MW available on E–F is clearing one more MW from Naomi at $15, so the **shadow price** of the limiting element is **$15**, and that becomes the **clearing price** for all three paths: **P_AB = P_CD = P_EF = $15**. Jack is awarded 20 MW at $15/MW (below his $20 bid); Naomi sells 10 MW at $15/MW; Ellen is not awarded because the clearing price $15 exceeds her $10 bid. Naomi’s offer was **marginal**—only 10 MW cleared despite offering 90 MW.




**Dynamic ratings (examples)**

Dynamic ratings are limits that **vary with conditions** (rather than a single fixed value). In the CRR Network Model, ERCOT incorporates them to the extent provided and updates them using maximum forecasted temperatures for the month. Examples:

- **Overhead transmission lines** – Thermal capacity depends on **ambient temperature** and **wind**. Colder weather and higher wind allow more current; hotter, still air reduces it. Using the month’s **maximum forecasted temperature** yields a conservative thermal limit for that month in the model.
- **Conductor ampacity** – **Solar heating**, **wind speed**, and **air temperature** determine how much current a conductor can carry before overheating or excessive sag. Dynamic ratings reflect these factors instead of a worst-case static rating.
- **Transformers** – Loading limits can depend on **ambient temperature** and **load history**. A dynamic approach uses forecast conditions (e.g. monthly max temperature) to set the rating used in the model.

In short, dynamic ratings in the network model are mainly **temperature- and weather-dependent thermal limits** on lines and other elements, updated (e.g. monthly) from forecasts so the model reflects **available capacity for that period** rather than a fixed worst-case static rating.

**Uses and posting of the CRR Network Model**

The CRR Network Model is an **input to both** the **CRR Auction Process** and the **CRR Allocation Process** for NOIEs.

For **transparency**, ERCOT posts the CRR Network Models on the **Market Information System (MIS) Secure Area** prior to each auction. This allows **CRR Account Holders** to download the model and use it to develop their **bid or offer strategies** for the auction.

**Posting deadlines (per Protocols):**
- **Monthly Auction** – Model posted **no later than 10 business days** before the Monthly Auction.
- **Long-Term Auction Sequence** – **All models** for the sequence must be posted **no later than 20 business days** before the sequence begins.

### Module summary (Auction & Allocation)

In this module you've learned about:

- **The role of the CRR Network Model in CRR Auctions** – How the model is derived from the Network Operations Model, what it reflects (facilities, outages, dynamic ratings, monitored elements, contingencies), and how it defines available transmission capacity for the auction.
- **Impacts of Pre-Assigned CRRs on CRR Auctions** – Allocation occurs before the auction; eligible NOIEs have first rights to capacity for PCRRs, so the capacity **available prior to the auction** is what remains after allocation. SFT is used to validate allocation and feasibility.
- **Inputs and outputs of the CRR Auction Process** – **Inputs:** Bids, Offers, CRR Model (including allocated and previously awarded CRRs), Credit Limits. **Outputs:** Auction results (MIS postings—public and certified—and settlements); daily data to Credit and Settlements systems.
- **CRR Auction Process** – Transmission capacity before and after the auction; single-round simultaneous clearing; bid and offer structure; TOU blocks and 7×24 block bids (monthly only); minimum bid price and auction fees; clearing objective and shadow prices; worked examples (Cases 1–4).

You should now be able to **describe the role of the CRR Network Model** in the CRR Auction and **explain the impact of Pre-Assigned CRRs** on the CRR Auction; **identify the inputs and outputs** of the CRR Auction; and **describe key details** of the CRR Auction Process.

---
## Definitions

**SCED (Security-Constrained Economic Dispatch)**  
The process that determines **how much** each committed resource should produce in each interval. It minimizes production cost (or maximizes social welfare) subject to power balance, unit limits (min/max, ramps), and **transmission flow and security constraints** (e.g. N‑1). SCED runs in **real time** (e.g. every 5 minutes in ERCOT) and in the **day-ahead** market. Its solution produces **LMPs** and **dispatch setpoints**; congestion appears as different LMPs across nodes and drives CRR value.

**SCUD (Security-Constrained Unit Dispatch)**  
Often used for the **commitment** step: **which** units are on/off and their **schedule**, subject to the same security and transmission constraints. So: **SCUD** (or **SCUC**, Security-Constrained Unit Commitment) decides **which** units run and when; **SCED** decides **how much** each produces. Both are security-constrained.

**Contingency**  
A **contingency** is the **loss or unavailability of one or more system elements** (e.g. a transmission line, transformer, or generator) that is explicitly modeled to verify the grid remains secure **after** that loss. **N‑1** means the outage of a **single** major element; the system must still meet load and respect thermal and voltage limits. Contingencies are used so that if that element fails, the rest of the grid does not overload. In the **CRR Network Model**, ERCOT includes contingencies that would **significantly affect congestion costs**; the auction clearing engine runs with these cases so CRR awards and prices reflect **post-contingency** transfer limits as well as the base case.


## Trading of CRR

**Module objectives**

Upon completion of this module, learners will be able to:

1. **Identify which CRRs are tradable**
2. **Describe the process of registering CRR trades with ERCOT**
3. **Describe the ERCOT requirements to trade CRRs**

**CRR Life Cycle and trades**

The life cycle diagram shows three acquisition methods—**Allocation** (PCRRs to NOIEs, prior to the CRR Auction), **CRR Auction** (bids to buy, offers to sell), and **CRR Trades** (bilateral transactions between CRR Account Holders)—all leading to **Day-Ahead Market** **daily settlement of CRRs**.

**Definition of a trade**  
A **trade** is a **bilateral transaction** that **transfers CRR ownership** between **two CRR Account Holders**.

**Requirements**
- **To buy a CRR through a trade:** You must be a **registered CRR Account Holder**.
- **To sell a CRR through a trade:** You must be a **qualified CRR Account Holder** and you must **currently own** the CRR you want to sell.

**Settlement**  
Just as with CRRs acquired through auction and allocation, **CRRs acquired through trades** are **cashed out in the Day-Ahead Market**. Over the period the CRRs are owned, they are **settled on a daily basis** using **Day-Ahead Market prices**.

**Tradable Congestion Revenue Rights**

A distinction must be made with regard to **tradability**:

| Type of CRR | Tradable |
|-------------|----------|
| **PTP Options** | ✓ Yes |
| **PTP Obligations** | ✓ Yes |
| **PTP Options w/ Refund** | No |
| **PTP Obligations w/ Refund** | No |

**PTP Options** and **PTP Obligations** (acquired via auction or trade) are **fully tradable**. **PTP Options with Refunds** and **PTP Obligations with Refunds** are types of **pre-assigned CRRs** allocated to eligible **NOIEs** free of charge, with the restriction that they are **only for hedging congestion costs** associated with production from the **Resource in their long-term supply contract**. Any revenues **beyond** hedging those actual congestion costs must be **refunded**. As such, **these CRRs are not tradable**.

**Parameters for trading CRRs**

A trade is defined by the **parameters of the CRR** being transferred. Example: **CRR Account Holder Jane** wants to trade a CRR she **purchased in an auction**. The CRR is a **10 MW Peak Weekend Point-to-Point Obligation** from **Resource Node 1** to **Load Zone 4** for the **month of July**. In offering to trade this CRR, Jane has **flexibility in how she formulates her offer**; what she **can and cannot do** is governed by ERCOT rules (e.g. registration, requirements).

Key parameters that identify the CRR and appear in trading (e.g. in the CRR Market User Interface or trade registration) include:

| CRR ID | Account Holder | Source | Sink | MW | Start Date | End Date | Time Of Use | Hedge Type |
|--------|----------------|--------|------|-----|------------|----------|-------------|------------|
| 54321 | Jane | RN1 | LZ4 | 10 | 07/01/2014 | 07/31/2014 | Peak WE | OBL |

- **CRR ID** – Unique identifier for the CRR.
- **Source / Sink** – Settlement points (e.g. Resource Node RN1, Load Zone LZ4).
- **MW** – Quantity (e.g. 10 MW).
- **Start Date / End Date** – Period the CRR covers (e.g. one month: 07/01–07/31).
- **Time Of Use** – TOU block (e.g. **Peak WE** = Peak Weekend).
- **Hedge Type** – **OBL** = Point-to-Point Obligation; **OPT** = Point-to-Point Option.

**What fields may be modified when offering a CRR for trade?**

In offering a CRR for trade, **certain characteristics of the original CRR cannot be modified**. Those include the **Source**, **Sink**, the **Time-of-Use Block**, and the **Hedge Type**. However, the CRR Account Holder **can choose to modify** the **MWs** and the **effective days** of the CRR.

- **Cannot modify:** Source, Sink, Time-of-Use Block, Hedge Type.
- **Can modify:** **MWs of CRRs**, **Effective Days of CRR**.

In the Jane example: while she **owns 10 MW** of the Point-to-Point Obligation, she **may choose to offer fewer than 10 MW** (e.g. 5 MW). She **cannot offer more** than she actually owns. For trading purposes, Jane may also **offer less than the entire month’s worth** of CRRs she owns—in other words, she is **allowed to break up the monthly strip of Time-of-Use Blocks into individual Time-of-Use Blocks** (e.g. offer only certain days within the month, or a subset of TOU blocks that make up her holding).

**Example: Jane’s two offers**

After considering her needs and options, Jane offers to trade her **Peak Weekend Point-to-Point Obligations** in **two different ways**. She will **maintain ownership** of whatever is not traded.

| Offer | CRR ID | Account Holder | Source | Sink | MW | Start Date | End Date | Time Of Use | Hedge Type |
|-------|--------|----------------|--------|------|-----|------------|----------|-------------|------------|
| **1** | 54321 | Jane | RN1 | LZ4 | **3** | **07/12/2014** | **07/13/2014** | Peak WE | OBL |
| **2** | 54321 | Jane | RN1 | LZ4 | **2** | 07/01/2014 | 07/31/2014 | Peak WE | OBL |

- **Offer 1:** Jane is willing to sell **3 MW** for a **single weekend** during the month (12–13 July 2014). Source, Sink, TOU block, and Hedge Type are unchanged; she has modified **MW** and **effective days** (narrow window).
- **Offer 2:** Jane is willing to sell **2 MW** for **all Peak Weekend Time-of-Use blocks** in the month (full July). Again she has modified **MW** (2 instead of 10); the **effective days** span the whole month, so she is offering a smaller quantity over the full Peak Weekend strip.

Both offers illustrate the flexibility to **modify MWs and effective days** while leaving Source, Sink, Time-of-Use Block, and Hedge Type fixed.

**Posting offers and bids for trades**

ERCOT hosts a **trading platform** for **posting and reporting** CRR trades. CRR Account Holders use this platform to indicate their **willingness to sell** or **buy** a CRR. The platform functions like a **bulletin board**: owners can **post CRRs they are willing to trade** (offers for sale), and can **post information on CRRs they wish to purchase** (want-to-buy). When a CRR Account Holder finds an interesting posting, it is their **responsibility to contact the other party** and **negotiate the trade terms**. The **actual bilateral transaction**, including any **money exchange**, is handled **outside** ERCOT’s systems. Once the parties agree on a transaction, the **final transfer of CRR ownership** is **reported through ERCOT’s CRR system**.

CRR Account Holders may indicate willingness to:
- **Sell a CRR in a trade**
- **Buy a CRR in a trade**

The platform typically provides two types of listings (e.g. under a “Postings” or “My Trades” interface):

**CRRs for Sale** – Postings by account holders offering to sell. Key columns include: **CRR ID**, **Initiating Account Holder**, **Source**, **Sink**, **MW**, **Start Date**, **End Date**, **Time-of-Use**, **Hedge Type**, **Contact Info** (to reach the seller), **Status** (e.g. Open). Example: “AH Vale” might post CRR 12345, 5 MW from RN1 to LZ4, 07/01/2008–07/31/2008, Peak WE, OBL, status Open.

**Want to Buy** – Postings by account holders seeking to buy. Columns may include: **Initiating Account Holder**, **Flowgate** (or Source/Sink), **Source**, **Sink**, **MW**, **Start Date**, **End Date**, **Time-of-Use**, **Hedge Type**, **Contact Info** (to reach the buyer), **Status**. Example: “AH Caster” might post a want-to-buy for 22.5 MW (e.g. Hub1 to LZ5), June 2008, Peak WE, OBL; “AH Davis” might post for 15 MW (e.g. LZ4 to RN1), August 2008, Peak WE, OPT.

**Example: Completing and reporting a trade (Jane and Jill)**

Another CRR Account Holder, **Jill**, sees **both of Jane’s offers** in the CRR system. Jill **contacts Jane** to negotiate for **Offer #1** (3 MW, 12–13 July 2014, Peak Weekend, RN1→LZ4, OBL). The two **agree on a price** and **trade the CRR**. At that point, **Jane and Jill must report the trade to ERCOT** if they wish for ERCOT to **change the owner of record**—the actual transfer of ownership is recorded and reported through ERCOT’s CRR system once the parties have agreed and reported it.

| Offer | CRR ID | Account Holder | Source | Sink | MW | Start Date | End Date | Time Of Use | Hedge Type |
|-------|--------|----------------|--------|------|-----|------------|----------|-------------|------------|
| **1** | 54321 | Jane | RN1 | LZ4 | 3 | 07/12/2014 | 07/13/2014 | Peak WE | OBL |

Summary: **See offers** (bulletin board) → **Contact counterparty** → **Negotiate and agree** (including price; payment is bilateral, outside ERCOT) → **Report trade to ERCOT** so that the **owner of record** is updated.

**Reporting and confirming trades in the ERCOT CRR system**

The **reporting of CRR trades** is handled through the **ERCOT CRR system**. The sequence is:

1. **Selling party reports the trade to ERCOT** – The seller (e.g. Jane) submits the trade to ERCOT via the CRR system.
2. **Buying party is notified** – The CRR system **notifies the buying party** (e.g. Jill) that there is an **outstanding trade**.
3. **Buying party confirms the trade through ERCOT** – The buyer logs into the CRR system and **confirms** the trade.

**Until the trade is confirmed by the buying party, the owner of record will not change.** So both parties must complete their steps in the CRR system for the transfer of ownership to be finalized.

**ERCOT’s role after confirmation**

Once the **buying CRR Account Holder confirms** the trade, **ERCOT** performs two key functions:

1. **Checks Account Holders’ Available Credit Limits** – ERCOT checks **both** CRR Account Holders’ **available credit limits**. ERCOT must confirm that **each** Account Holder has **sufficient available credit** to cover any **increased credit exposure** resulting from the trade. For example, a CRR Account Holder who **buys a Point-to-Point Obligation** may be exposed to **charges** in future Day-Ahead Markets, so the trade **increases their credit exposure**. Conversely, a CRR Account Holder who **sells a Point-to-Point Option** may be giving up an instrument that **frequently provides them with revenue**; that trade **could also increase their credit exposure**. The trade is approved only if credit is sufficient for both parties.
2. **Financially settles with new CRR owner** – Once the trade is **approved**, ERCOT **begins settling with the new CRR owner** in any **future Day-Ahead Markets** (daily settlement of CRRs as described in the life cycle).

**Settlements of traded Congestion Revenue Rights**

Once the trade is complete, the **traded CRR reflects** a **new Account Holder** and a **new CRR ID**. The new owner will receive a **new CRR ID** for the traded CRR; ERCOT’s systems treat it as a distinct CRR for settlement and record-keeping (same economic terms—Source, Sink, MW, dates, TOU, Hedge Type—but new owner and new identifier).

*Example (continuing Jane/Jill):* After the trade, the CRR that was Jane’s Offer #1 (originally CRR ID 54321) is now held by Jill under a new ID:

| CRR ID | Account Holder | Source | Sink | MW | Start Date | End Date | Time Of Use | Hedge Type |
|--------|----------------|--------|------|-----|------------|----------|-------------|------------|
| 56789 | Jill | RN1 | LZ4 | 3 | 07/12/2014 | 07/13/2014 | Peak WE | OBL |

ERCOT will **settle with Jill** (the new owner) in the Day-Ahead Market for this CRR going forward.

### Module summary (Trading)

In this module you've learned about:

- **Which CRRs are tradable** – PTP Options and PTP Obligations (from auction or trade) are fully tradable; PTP Options and Obligations *with Refunds* (pre-assigned to NOIEs) are not tradable.
- **The process of registering CRR trades with ERCOT** – Bulletin board (post offers / want-to-buy); contact and negotiate bilaterally; seller reports the trade, buyer confirms; ERCOT checks credit limits and, once approved, settles with the new owner; traded CRR gets a new Account Holder and new CRR ID.
- **The ERCOT requirements to trade CRRs** – Must be a registered (to buy) or qualified (to sell) CRR Account Holder; seller must currently own the CRR; only certain fields may be modified when offering (MW, effective days); payment is bilateral; ownership transfer and settlement are reported and processed through ERCOT’s CRR system.

## DAM PTP Obligations

### PTP Obligation vs virtuals

**PTP Obligation** and **virtuals** are both **financial-only** (no physical delivery), but they differ in **what** they expose you to and **where** they are used:

| | **PTP Obligation** | **Virtuals** (virtual bid/offer) |
|--|---------------------|-----------------------------------|
| **Definition** | **Two-point** instrument: **source** and **sink** settlement points. Value = **Sink SPP − Source SPP** per MW (payment or charge). | **Single-point** position: buy (virtual demand) or sell (virtual supply) at **one** settlement point in the DAM; no physical energy. |
| **Settlement** | **Spread** between two locations (e.g. DAM spread for CRR obligations; RT spread for DAM PTP Obligations). | **Price at one location**: typically (RT SPP − DAM SPP) × quantity for virtual demand, or (DAM SPP − RT SPP) × quantity for virtual supply. |
| **Risk** | **Congestion / basis** between two points (spread risk). | **DAM vs RT price** at a single point (timing/location price risk at one node). |
| **Where acquired** | **CRR auction** or **bilateral** (CRR Account Holder), or **in the DAM** (DAM PTP Obligation; QSE only). | **Day-Ahead Market** (submitted as virtual demand or virtual supply at a node). |
| **Typical use** | **Hedge** congestion cost between source and sink; or **speculate** on the spread. | **Speculate** on the difference between DAM and RT price at one location; or **provide liquidity** to the DAM. |

**Summary:** A **PTP Obligation** is a **spread** product (two nodes): you are paid or charged the price difference between sink and source. A **virtual** is a **single-node** product: you are settled on the difference between DAM and RT price at that node. PTP Obligations hedge or bet on **congestion between two points**; virtuals hedge or bet on **price at one point** across the DAM/RT boundary.


# Credit Limit

## Module 5: Credit Limits — Introduction

So far we have looked at **acquiring CRRs** through the **auction** and **allocation** processes, **trading of CRRs** (bilateral transactions between CRR Account Holders), and **acquiring Point-to-Point Obligations in the Day-Ahead Market** (DAM PTP Obligations, QSE-only). In each of these processes, **credit limits** appear as a constraint: the CRR Auction does not award CRRs in excess of a CRR Account Holder’s Available Credit; CRR trades are approved only if both parties have sufficient credit; and the Day-Ahead Market does not award bids and offers beyond a QSE’s Available Credit. **In this module we look at credit limits in more detail** — how they are calculated and how they are used when buying CRRs in the auction or PTP Obligations in the DAM.

**Module objectives:** Upon completion of this module, you will be able to:

1. **Recognize how a company establishes available credit**
2. **Explain the process of allocating credit for a CRR Auction**
3. **Describe how credit is utilized in the CRR Auction**
4. **Recognize how credit is shared between QSEs and CRR Account Holders**

### Introducing the Counter-Party

As part of any discussion of **credit**, we first need to introduce the **Counter-Party**.

**Definition (ERCOT protocols):** The **Counter-Party** is a **single Entity** that is also a **QSE** and/or a **CRR Account Holder**. In practice, **all QSEs and CRR Account Holders** that are part of the **same legal entity** will have the **same Counter-Party**. The **Counter-Party** is **ultimately responsible for managing the credit** that is available to their QSEs and CRR Account Holders.

**Summary:**

- **Counter-Party (CP):** Entity that is also a QSE and/or a CRR Account Holder; **responsible for managing Available Credit**.
- **Relationship:** One Counter-Party can have multiple **CRR Account Holders** and/or **QSEs** under it (same legal entity). Credit is **managed at the Counter-Party level** and is **shared** or **allocated** to those QSEs and CRR Account Holders.

### Available Credit

What is **available credit** and how does the **Counter-Party** manage it? Every Counter-Party has **credit exposure** that depends on its **company’s activities in the ERCOT Market**. The Counter-Party may also be allowed a certain amount of **Unsecured Credit** — credit by virtue of **good standing** (e.g. financial strength, history). The Counter-Party can **post Secured Collateral** to **make credit available** to its QSEs and CRR Account Holders. **Secured Collateral** can be **cash**, **letters of credit**, or **bonds**.

**Components:**

- **Total credit capacity** (what the Counter-Party has to work with) = **Unsecured Credit** + **Secured Collateral**.
- **Credit Exposure** = the portion of that capacity that is **already used** (e.g. by existing CRR positions, DAM awards, other ERCOT market activity).
- **Available Credit** = the portion **remaining** for new activity: **Available Credit** = (Unsecured Credit + Secured Collateral) − Credit Exposure.

So: the Counter-Party **posts Secured Collateral** (and may have Unsecured Credit) to establish total credit capacity; **Credit Exposure** consumes part of it; the **remainder is Available Credit** for its QSEs and CRR Account Holders (e.g. for the CRR Auction or the Day-Ahead Market).

### CRR Auction inputs (credit limits)

![Collateral](Collateral.png)

Focusing on **establishing credit limits for the CRR Auction**: as discussed earlier, **Credit Limits** are one of the **inputs to the CRR Auction Engine**. The other inputs are **Bids**, **Offers**, and the **CRR Model** (which includes **Allocated CRRs**, **Previously Awarded CRRs**, and **Credit Limits**). **A CRR Account Holder’s Credit Limit acts as a budget constraint** for that holder as the auction determines which bids and offers to clear — the auction will not award CRRs in excess of a participant’s Available Credit. The next step is to see **how these credit limits are determined** and **how credit is consumed** in the CRR Auction.

### CRR Auction Credit Limit (ACLC)

**ERCOT calculates the Counter-Party’s Available Credit Limit for the CRR Auction (ACLC)** from the Counter-Party’s **Secured Collateral**, after accounting for what has already been consumed.

Looking at **Secured Collateral** only: **some of it has already been consumed**. Part is consumed by **exposure from CRRs currently owned** (**CRR Credit Exposure**). Part is also consumed by **QSE activities** (**Secured Collateral consumed by QSE**). **What remains** after subtracting those two uses is the **Counter-Party’s Available Credit Limit for the CRR Auction**, or **ACLC**. So: **ACLC** = Secured Collateral − CRR Credit Exposure − Secured Collateral consumed by QSE (conceptually; other components may apply per ERCOT rules).

The **Counter-Party** may then **allocate up to 90% of ACLC** to **all CRR Account Holders** within their company (there may be up to three). That allocated amount is what constrains each CRR Account Holder’s ability to be awarded CRRs in the auction.

### Utilizing available credit — Budget constraint in CRR Auction

How is that **available credit** actually **utilized** in the CRR Auction? As already noted, the **CRR Account Holder’s credit limit** acts as a **budget constraint** in the auction.

- **ERCOT** calculates the **ACLC** (Available Credit Limit for the CRR Auction) for the **Counter-Party**.
- The **Counter-Party** must **set a Credit Limit for the upcoming auction** in order for their **CRR Account Holder(s)** to **participate**. They may utilize **up to 90% of ACLC** as that credit limit for the auction.
- The **Counter-Party must lock credit by the close of the Bid Window** for the CRR Auction — i.e. they must **actively commit** the credit before the auction runs, so that ERCOT and the auction engine know how much credit each CRR Account Holder has available for that auction.

**CRR Account Holder self-imposed credit limit:** A **CRR Account Holder** may **assign a self-imposed Credit Limit** (lower than the amount the Counter-Party has set for them). Since the self-imposed limit is **lower** than the Counter-Party’s limit, the **self-imposed credit limit** is what **forms the CRR Account Holder’s budget constraint** in the CRR Auction — i.e. the auction will not award that holder more than their self-imposed limit. It is important to note that **the Counter-Party Credit Limit determines how much credit is locked for the auction**, even if the CRR Account Holder self-imposes a lower limit; the **locked credit** (the amount committed by the Counter-Party) **remains locked until the auction is complete and invoices have posted**.

### Special rules for Long-Term Auction Sequence

For the **Long-Term Auction Sequence**, there are **special rules** for locking credit. Each **Long-Term Auction Sequence** consists of **four separate CRR Auctions** (one for each six-month period). Consequently:

1. **Counter-Party must lock credit separately for each auction in the sequence** — i.e. for each of the four auctions in the Long-Term Sequence, the Counter-Party must lock credit by that auction’s bid-window close.
2. **Counter-Party must lock credit separately for each Time-of-Use (TOU)** — since each **Time-of-Use block** is cleared through a **separate optimization**, credit must be locked per TOU as required by ERCOT.

In all cases, **CRR Account Holders** still have the option of setting a **self-imposed credit limit** that is lower than the Counter-Party’s locked credit limit. **For credit-lock deadlines**, refer to the **CRR Activity Calendar** posted on [ercot.com](https://www.ercot.com) (e.g. [ercot.com/mktinfo/crr](http://www.ercot.com/mktinfo/crr)).

### Credit consumption in CRR Auction

**Credit is consumed** during the **CRR Auction clearing process**. Ideally, consumption would be based on **clearing prices**, but because **credit limits constrain the auction**, clearing prices are not known in advance. So **bid (or offer) prices** are used to calculate credit consumption — they represent the **maximum prices** that might be charged. The **volumes** used are **potentially awarded volumes** in the clearing process, not simply bid volumes.

**Credit is consumed as follows:**

| **Instrument** | **Credit consumption** |
|----------------|------------------------|
| **PTP Option Bids** | Volume × Bid price |
| **PTP Obligation Offers** | Volume × Min(0, Offer price) — offers normally do not consume credit (seller is giving up a position); if the offer has a **negative** price, credit may be consumed as volume × offer price. |
| **PTP Obligation Bids** | Volume × (Bid price + **Path-Specific Adders**) — **Path-Specific Adders** are included to reflect the **increased risk** associated with Obligations on certain paths. |

So: **PTP Option bids** consume credit as volume times bid price. **PTP Obligation offers** consume credit only when the offer price is negative (Min(0, Offer price) in the formula). **PTP Obligation bids** consume credit as volume times (bid price + path-specific adders).

### Path-Specific DAM-Based Adder for PTP Obligation Bids

The **Path-Specific Adder** used in credit consumption for **PTP Obligation Bids** is **calculated for each source/sink pair** using a **three-year look-back** of historical data.

**Process:** For each such path and **monthly Time-of-Use (TOU) block**, the **average Day-Ahead Market (DAM) price** is computed over the look-back period. This produces a **distribution of prices** (e.g. a histogram or density of average DAM prices per monthly TOU block). The distribution might be centered around a typical value (e.g. a frequent price) with outcomes sometimes higher or lower.

**Adder (Aci99):** ERCOT uses the **lower boundary of the 99th percentile confidence interval** of that distribution — i.e. a price such that **99% of future prices** (under the historical distribution) are **equal to or greater than** that value. This value is called **Aci99** (Adder at the 99th percentile **C**onfidence **I**nterval). Using the 99th percentile lower bound reflects **increased risk** on certain paths for PTP Obligations and thus drives a higher credit charge (bid price + adder) for obligation bids on those paths.

### Auction PTP Obligation Credit Requirement (AOBLCR)

Credit consumption for a **PTP Obligation Bid** in the auction is given by the **Auction PTP Obligation Credit Requirement (AOBLCR)** formula:

**AOBLCR = BOBLMW × Max(0, BPOBL − Min(0, Aci, ACP))**

Where:

- **BOBLMW** = (Potentially) awarded PTP Obligation volume (MW)
- **BPOBL** = Bid price for the PTP Obligation (submitted by the CRR Account Holder)
- **Aci** = Path-Specific Adder for that source/sink (e.g. Aci99 from the 99th percentile confidence interval)
- **ACP** = Auction Clearing Price from the **most recent** auction (for that path/TOU)

**Interpretation:** The term **Min(0, Aci, ACP)** is the **path-specific adder** used in the credit calculation. If the **most recent ACP** is **less than Aci** (path has become riskier), **Aci** is effectively chosen. If **Aci** or **ACP** are **negative**, the adder increases the credit consumed to acquire the Obligation. If **Aci** and **ACP** are **positive**, **Min(0, Aci, ACP) = 0**, so there is very little risk assumed for the PTP Obligation (the owner almost always pays in the DAM). **Max(0, …)** ensures that if the combination of bid price and effective adder is **negative** (i.e. the CRR Account Holder is effectively **paid** to take the PTP Obligation), **no credit is consumed** for that bid. **Buyer beware:** the Obligation will likely create **credit exposure** for the owner for the entire time it is owned (e.g. in subsequent DAM settlements).

### Scenario: Budget constraint in the CRR Auction

**Scenario 1 (simplified — single hour; CRRs are typically in Time-of-Use blocks):** A **CRR Account Holder** sets a **self-imposed credit limit of \$50,000** and submits bids for a **Monthly CRR Auction**. They bid to buy **100 MW of PTP Options from Point A to Point B** at a **Bid Price of \$1000/MW**. The auction runs and **awards them 50 MW at \$20** (clearing price).

**What happened?** They **hit their budget constraint**. The CRR Account Holder’s **self-imposed credit limit** acts as their **budget constraint** in the auction clearing process. The auction ensures that **cleared volume × bid price** does not exceed the self-imposed credit limit for that CRR Account Holder. Here: **50 MW × \$1000/MW = \$50,000**, which equals the \$50,000 limit — so they could not be awarded more than 50 MW at their bid price. The **clearing price** (\$20) is what they actually pay per MW for the awarded 50 MW; the **bid price** (\$1000) is used for **credit consumption** and thus caps how many MW can be awarded before the budget is exhausted.

**Scenario 2 (PTP Obligations and Path-Specific Adder):** A **CRR Account Holder** sets a **self-imposed credit limit of \$18,000** and submits bids for a **Monthly CRR Auction**: **100 MW PTP Obligations from D to C** at **\$180/MW** bid price. The auction **awards them 90 MW at -\$20** (clearing price).

**What happened?** They **hit their budget constraint** again, but **in a different way**. On **volume and bid price alone**, 100 MW × \$180 = \$18,000 would exactly match the limit — yet they were only awarded **90 MW**. For **PTP Obligations**, **Path-Specific Adders** are included in credit consumption: credit per MW = bid price + (effective adder). The **entire \$18,000** was consumed by **90 MW**, so the **credit requirement** was **\$18,000 ÷ 90 MW = \$200 per MW**. That implies **\$180 + effective adder = \$200**, so the **effective path-specific adder** was **\$20 per MW** (e.g. if the adder term is **-\$20** in the formula, then **\$180 − (-\$20) = \$200**). So the **Path-Specific Adder** on this path (D to C) **increased** the credit consumed per MW and reduced the award from 100 MW to 90 MW before the \$18,000 limit was reached.

### The rest of the credit picture — Credit shared between CRR Account Holders and QSEs

So far we have focused on **credit utilization by CRR Account Holders** (e.g. CRR Auction credit limit, locking credit, credit consumption in the auction). **Most CRR Account Holders** in the ERCOT market are **also registered as QSEs**, and **available credit for a particular company is shared** by their **CRR Account Holders** and **QSEs**.

The **Counter-Party** is responsible for **maintaining appropriate levels of Secured Collateral with ERCOT** and then **portioning the available credit** across their **CRR Account Holders** and **QSEs**. So:

- **CRR Auction Credit Limit** — allocated to **CRR Account Holder(s)** for participation in the CRR Auction (as discussed: lock credit by bid-window close, up to 90% of ACLC, self-imposed limit optional).
- **Day-Ahead Market Credit Limit** — allocated to **QSE(s)** for buying products in the **Day-Ahead Market** (e.g. energy, DAM PTP Obligations). If a QSE is planning to **buy anything in the Day-Ahead Market**, they **need available credit** in order to do so.

So **available credit** (from Secured Collateral and Unsecured Credit, after Credit Exposure) is **shared** by the Counter-Party between **CRR Account Holders** (for the CRR Auction) and **QSEs** (for the Day-Ahead Market). How the **Day-Ahead Market Credit Limit** for QSEs is **established** (e.g. allocation rules, timing) is the next part of the credit picture; the CRR Auction Credit Limit for CRR Account Holders has already been covered.

### Day-Ahead Market Credit Limit (ACLD)

**ERCOT calculates the Counter-Party’s Available Credit Limit for the Day-Ahead Market (ACLD)** from the same pool: **Secured Collateral** and **Unsecured Credit**, after **QSE Credit Exposure** and **CRR Credit Exposure** (and, when applicable, **credit locked for the CRR Auction**) are taken into account. The **QSE gets 90% of ACLD** as its **DAM Credit Limit** (the amount it can use to buy energy and PTP Obligations in the Day-Ahead Market).

**Two scenarios:**

- **No CRR Auction in progress:** ERCOT includes **all available credit** (after QSE and CRR exposures) in the Counter-Party’s **ACLD**. The QSE then gets **up to 90% of ACLD** as its **DAM Credit Limit**.
- **CRR Auction in progress:** The Counter-Party has **locked credit for the auction**. The **remaining** available credit (after QSE exposure, CRR exposure, and **credit locked for Auction**) forms the pool for **ACLD**. The QSE gets **90% of that remaining ACLD** as its DAM Credit Limit — i.e. **90% of what’s left** after the lock.

**Why would the QSE be concerned?** If the Counter-Party **locks too much** of its available credit **for a CRR Auction**, the **QSE may have very little credit** left for the Day-Ahead Market (buying energy, DAM PTP Obligations). So the **portioning** of credit between CRR Auction and DAM is a **trade-off** for the Counter-Party and its entities.

**Buying PTP Obligations in the DAM:** **Participating in the Day-Ahead Market** (including **DAM Point-to-Point Obligations**) **requires available credit**. The **QSE’s Day-Ahead Market Credit Limit** (90% of ACLD, as above) **acts as a budget constraint in the Day-Ahead Market Engine** — the DAM will not award bids and offers beyond that limit. **Not enough credit, and the QSE is effectively locked out of the Day-Ahead Market.** The same inputs feed the DAM as before: **PTP Obligation Bids**, **Energy Bids and Offers** (from the QSE), and **Day-Ahead Network Model**, **Credit Limits** (from ERCOT). Note also: **each CRR Auction may take several days to solve**, and **credit allocated (locked) for the auction remains locked until the auction invoices are posted** — so CRR Auction activity can tie up credit for an extended period and reduce what is left for the QSE’s DAM Credit Limit.

### Module summary (Credit Limits)

In this module you have learned about:

1. **How a company establishes available credit** — Counter-Party, Secured Collateral (cash, letters of credit, bonds), Unsecured Credit, Credit Exposure; Available Credit = (Unsecured + Secured) − Exposure; ACLC and allocation to CRR Account Holders (up to 90%); locking credit by bid-window close; self-imposed limits.
2. **The process of allocating credit for a CRR Auction** — ERCOT calculates ACLC for the Counter-Party; Counter-Party locks credit (separately per auction in the Long-Term Sequence and per TOU); Counter-Party may allocate up to 90% of ACLC to CRR Account Holders; CRR Account Holder may set a lower self-imposed limit.
3. **How credit is utilized in the CRR Auction** — Credit consumption formulas (PTP Option bids, PTP Obligation offers, PTP Obligation bids with Path-Specific Adders); AOBLCR formula; budget constraint (cleared volume × bid price or effective price ≤ limit); scenarios (Options vs Obligations with adder); credit locked until auction invoices post.
4. **How credit is shared between QSEs and CRR Account Holders** — Available credit is shared; Counter-Party portions credit to CRR Auction (CRR Account Holders) and to DAM (QSEs); ACLD and 90% as QSE DAM Credit Limit; trade-off when CRR Auction locks credit; QSE needs credit to participate in the DAM or is locked out.

## CRR Settlements

**Module objectives:** Upon completion of this module, you will be able to:

1. **Identify the settlements associated with buying, owning, and selling CRRs**
2. **Describe the flow of money in the CRR Auction and for settlements of CRRs in the Day-Ahead Market**
3. **Explain how ERCOT uses the CRR Balancing Account**
4. **Identify the settlements associated with buying PTP Obligations in the DAM**
5. **Describe the flow of money for DAM PTP Obligations**

### Three settlement processes (allocation, auction, bilateral trades)

**CRR Settlements** involve **three settlement processes**:

1. **CRR Auction Settlement** — **CRR Account Holders** settle for **buying or selling CRRs** in **CRR Auctions** (e.g. pay clearing price when buying; receive when selling). This covers CRRs acquired in the auction (and similarly, allocation and bilateral trades have their own settlement timing and flows).

2. **Day-Ahead Market** — **CRR owners** are **settled for the value of their CRRs on a daily basis** in the Day-Ahead Market (payment or charge based on DAM spread Sink − Source). If ERCOT **cannot collect enough money from the Day-Ahead Market** to pay CRR Account Holders what they are owed, **Shortfall Charges** may apply (e.g. shortfall allocated to CRR holders or other market participants as per ERCOT protocols).

3. **CRR Balancing Account** — A **“rainy day” fund** that ERCOT uses to manage mismatches between DAM congestion rent and CRR payouts. It may allow ERCOT to **return Shortfall Charges to CRR Account Holders on a monthly basis** (or otherwise smooth or true-up CRR-related payments).

### CRR Auction Settlement Timeline

The **CRR Auction Settlement** process follows a **timeline** from auction completion to payments. **Any given auction may take several days to solve.** Once the auction is **completed** and **results are approved**:

- **One day after** auction completion (Day 1, **ERCOT Business Day**): **Auction invoices** are sent to **CRR Account Holders** (buyers pay; sellers receive).
- **Payments due to ERCOT:** CRR Account Holders who owe money (e.g. bought CRRs) must pay **three bank business days** after the invoice has been issued (e.g. Day 4 on a **Bank Business Day** scale).
- **Payments from ERCOT to CRR Account Holders:** ERCOT pays sellers (or refunds as applicable) on the **next day that is both an ERCOT business day and a bank business day** (e.g. Day 5).

**Summary (order of events):** (1) **Auction completed** → Auction results approved. (2) **Day 1\*** → Auction invoice issued. (3) **Day 4\*\*** → Payments due to ERCOT (three bank business days after invoice). (4) **Day 5\*\*\*** → Payments from ERCOT to CRR Account Holders (next day that is both an ERCOT business day and a bank business day).

\* ERCOT Business Day  \*\* Bank Business Day  \*\*\* ERCOT Business Day and Bank Business Day

### Charges and payments for CRR Auction

ERCOT **invoices each CRR Account Holder** for both **bids** and **offers** awarded in a CRR auction.

**Charge for awarded CRR bid:**  
= **(Price) × (CRRs) × (TOU Hours)**  
i.e. **Auction clearing price** × **MWs of CRRs awarded** × **Number of hours in the Time-of-Use block**.

**Payment for awarded CRR offer:**  
= **(−1) × (Price) × (CRRs) × (TOU Hours)**  
Same as the charge formula, but the result is **multiplied by −1**. In **all ERCOT settlements, money flowing away from ERCOT is represented as a negative number**. A **payment** from ERCOT to a CRR Account Holder (e.g. for an awarded offer at a positive clearing price) is money **away from ERCOT**, so it is **negative** in ERCOT’s books; the (−1) ensures this sign convention is applied correctly.

**Example:** Suppose **CRR Account Holder 1 (CRRAH1)** is **awarded on a Point-to-Point Option bid**: **20 MW** of **Peak Weekday (5×16)** PTP Option for **February** at a **price of \$5/MW**. Peak Weekday is a 5×16 block (5 days per week, 16 hours per day), so there are **320 Peak Weekday hours** in February.

- **For one hour:** (Price) × (CRRs) = **(\$5/MW) × (20 MW) = \$100**.
- **For the entire TOU block:** \$100 × 320 hours = **\$32,000** total charge to CRRAH1 for this award.

### CRR Auction money flow — Collection of auction revenues

Understanding **money flow** in CRR Auctions is important. **Auction Revenues** (net proceeds from a CRR Auction) are collected in a **CRR Auction Revenues** pool (conceptually a “bucket” ERCOT manages).

**Money flowing *in* to the pool:** **Charges for awarded CRR Bids** (buyers pay ERCOT) and **revenues from Pre-Assigned CRRs (PCRRs)** (e.g. NOIEs pay for allocated CRRs). These are **inflows** into the CRR Auction Revenues bucket.

**Money flowing *out* of the pool:** **Payments for awarded CRR Offers** (ERCOT pays sellers) and **Payments for awarded CRR Bids** when obligations clear at a **negative price** (ERCOT effectively pays the buyer to take the obligation). These are **outflows** from the bucket.

**Net:** The **CRR Auction Revenues** bucket can hold **large amounts** (millions or tens of millions of dollars) — the **net** of inflows minus outflows. What ERCOT does with this money is described next.

#### Distribution of Auction Revenues

The **short answer** is that **Auction Revenues** are **paid out to QSEs representing Load** based on their **Load Ratio Share**.

- **Intra-Zonal CRRs\***  
  Revenues from **Intra-Zonal CRRs** (CRRs whose source and sink are in the **same 2003 Congestion Management Zone**) are distributed by **Zonal Load Ratio Share**. Each QSE receives a share of those revenues based on its share of **load in that zone** during the **monthly peak interval**.

- **Inter-Zonal CRRs\***  
  Revenues from **Inter-Zonal CRRs** (source and sink in **different 2003 Congestion Management Zones**) are distributed by **ERCOT-wide Load Ratio Share**. Each QSE receives a share based on its share of **load ERCOT-wide** during the **monthly peak interval**.

- **Timing:** Distribution occurs **once a month**, immediately after settling the **last operating day** of the month.

- **Recipient:** **All** Auction Revenues are distributed to **QSEs representing Load**. None of these revenues are retained to fund CRRs during the month.

\*Based on **2003 Congestion Management Zones**.

#### Day-Ahead Settlement of CRRs — Money flow (CRRs settled in the Day-Ahead)

CRRs are **funded from Congestion Rent** collected in the **Day-Ahead Market (DAM)**. This is a separate money flow from the CRR Auction Revenues bucket.

- **Congestion Rent — inflows (hourly):**  
  Money flows **into** the **Congestion Rent** bucket from **charges for cleared DAM Energy Bids** and **charges for cleared DAM Point-to-Point Obligation bids**.

- **Congestion Rent — outflows (hourly):**  
  Money flows **out** of the bucket as **payments for cleared DAM Energy Offers** and **payments for cleared DAM PTP Obligation bids** that cleared at **negative prices**.

- **Net:** If charges exceed payments, there is a **net amount of Congestion Rent** in the bucket. This money is used to **pay CRR Account Holders** what they are due for the CRRs they own (Target Payment, subject to deration and Hedge Value rules). **Surplus:** In some hours ERCOT collects **more Congestion Rent** than is needed to pay CRR Owners; any excess for that hour flows into the **CRR Balancing Account**, which can be thought of as a rainy-day fund and is used per ERCOT protocols. **Shortfall:** In some hours there **may not be enough** Congestion Rent to pay what CRR Owners are due; shortfalls are addressed per ERCOT protocols (e.g. use of the CRR Balancing Account or other settlement mechanisms).

- **Calculation:** CRR settlement in the Day-Ahead is **calculated hourly**. The payment due to CRR Account Holders is often called the **Target Payment**.

#### Shortfall Charges (when Congestion Rent is insufficient)

When **Congestion Rent** collected in an hour is **less** than the total **Target Payment** due to CRR Owners for that hour, ERCOT addresses the shortfall by assessing a **Shortfall Charge** to each CRR Owner. Each owner’s charge is proportional to their **share of the total Target Payment** that was due in the market for that hour:

$$
\text{Shortfall Charge} = (\text{Total CRR Shortfall for the hour}) \times \frac{\text{CRR Owner's Target Payment}}{\text{Total CRR Target Payments for the hour}}
$$

**Example (Hour Ending 1300):** Suppose Total CRR Target Payment for the hour is **$20 million** and Congestion Rent collected is **$19 million**. Then **Total CRR Shortfall** = $20M − $19M = **$1 million**. A CRR Owner whose Target Payment for that hour is **$2 million** has share $2M / $20M = **10%** of total target payments, so their **Shortfall Charge** = $1M × 0.10 = **$100,000**. In effect, CRR Owners are short-paid in proportion to the shortfall, and the Shortfall Charge formalizes each owner’s share of that shortfall.

#### CRR Rolling Balancing Account and Balancing Account Fund

When a CRR Account Holder is short-paid (due to insufficient Congestion Rent and Shortfall Charges), **all is not lost**: excess Congestion Rent collected in hours when more was collected than needed to pay CRR Owners flows into the **CRR Balancing Account** and is held until **end of the month**. **Shortfall Charges** to CRR Owners during the month are effectively **IOUs** — ERCOT withholds part of the Target Payment with the intent to pay in full by month-end.

**Month-end liquidation:** On the **last operating day of the month**, the **CRR Balancing Account is liquidated**. First, CRR Account Holders who had Shortfall Charges are paid (to the extent funds are available). Any **remaining** excess is placed in a savings account called the **CRR Balancing Account Fund**, which is used to cover future Shortfall Charges. The **Protocols allow a maximum of $10 million** to be carried in the CRR Balancing Account Fund from month to month. If that **$10 million limit** is reached, ERCOT distributes any additional remaining Balancing Account funds to **QSEs representing Load on a load ratio share basis**.

**If the Balancing Account is short at month-end:** If the CRR Balancing Account does **not** have enough to pay CRR Account Holders who were short-paid during the month, ERCOT pays out everything from the CRR Balancing Account and then draws **extra funds from the Balancing Account Fund** to pay those CRR Account Holders in full, if the Fund has sufficient balance.

**If both are insufficient:** The Balancing Account Fund may be **low or empty**. If the **CRR Balancing Account and the Balancing Account Fund together** do not have enough to pay CRR Account Holders in full, ERCOT pays out what is available. **CRR Account Holders will then remain forever short paid** for that shortfall.

#### Payment for CRRs settled in Day-Ahead (Target Payment)

Before the collected **Congestion Rent** can be distributed to CRR Account Holders, ERCOT must determine **how much is due each CRR Account Holder**. The **Target Payment** is the full expected payment for a CRR and is calculated as follows.

**Target Payment (per hour):**

$$
\text{Target Payment} = (\text{Price}) \times (\text{Quantity}) \quad \text{per hour}
$$

- **Price:**  
  **Day-Ahead Settlement Point Price at the sink minus Day-Ahead Settlement Point Price at the source.**  
  $$
  \text{Price} = \text{DASPP}_{\text{sink}} - \text{DASPP}_{\text{source}}
  $$

- **Quantity:**  
  The **MW of CRRs owned** on that **source-to-sink path**   (the same path the CRR is defined on).

- **PTP Options:**  
  **Point-to-Point Options** only result in a **payment** to the CRR Owner; they do not create a charge. If the price (DASPP_sink − DASPP_source) is **negative**, the Target Payment is set to **zero** and there is **no charge** to the CRR Owner.

- **PTP Obligations:**  
  The **Target Payment** for **Point-to-Point Obligations** is calculated the **same way** (Price × Quantity per hour). The main difference is that **PTP Obligations** can result in **either a payment or a charge** to the CRR Owner (unlike Options, which only result in a payment and never a charge).

**Example:** Suppose a CRR Account Holder owns **2 MW** of PTP Options between **Source A** and **Sink B**. Settlement Point A has a price of **$12/MWh** and Settlement Point B **$20/MWh**. Then Price = DASPP_sink − DASPP_source = $20 − $12 = **$8/MWh**, and Quantity = **2 MW**, so **Target Payment** = ($8/MWh) × (2 MW) = **$16 per hour**.

So for each hour, each CRR Account Holder’s entitlement from Congestion Rent is the **spread** (DASPP_sink − DASPP_source) times the **MW of CRRs** they hold on that path; these amounts are summed across paths and hours to determine total payments from the Congestion Rent bucket.

#### PTP Obligations bought in the Day-Ahead Market

**Charge for DAM PTP Obligation Bids (purchase in the DAM):** Awarded **Day-Ahead Market Point-to-Point Obligations** are **purchased** in the Day-Ahead Market. The initial settlement is this purchase. The **charge to the QSE** (or payment to the QSE if the price is negative) is:

**Charge (or payment) = (Price) × (Quantity)** per hour

- **Price:** **DASPP_sink − DASPP_source** (Day-Ahead Settlement Point Price at sink minus at source). The sink-minus-source price **can be negative**; if so, the QSE may be **paid** to take the PTP Obligations rather than charged.
- **Quantity:** The **MW of PTP Obligations awarded** on that source-to-sink path.

These charges and payments (when PTP Obligation bids clear at negative prices) are exactly what flow **into** and **out of** the **Congestion Rent** bucket alongside charges and payments for cleared DAM Energy Bids and Offers.

**Payment for DAM PTP Obligations in Real-Time (cash-out):** Once a QSE **owns** DAM PTP Obligations, those instruments are **cashed out in Real-Time Settlements**. Again the settlement is **price × quantity** per hour. DAM PTP Obligations are **hourly** instruments, but Real-Time uses **15-minute** Settlement Point Prices. The **price** is therefore the **hourly average** of the sink-minus-source difference: for each of the **four 15-minute intervals** in the hour, compute (RTSPP_sink − RTSPP_source), **sum** the four values, and **divide by 4**. The **quantity** is the **MW of DAM PTP Obligations owned** on the path. So:

**Payment to QSE in Real-Time** = (Price) × (Quantity) per hour, where  
**Price** = Σ_{i=1 to 4} (RTSPP_sink,i − RTSPP_source,i) / 4  
**Quantity** = MW of DAM PTP Obligations owned on path  

(RTSPP = Real-Time Settlement Point Price.)

#### Reduced CRR Payments (Deration)

CRR owners may **not** receive the full **Target Payment** in certain circumstances. One such circumstance is **deration**: **CRR payments may be derated** when all of the following are true:

1. **Transmission elements are oversold** — i.e. under present conditions, **more MW of CRRs are owned** along a particular path than the transmission system can support. The CRR Auctions use a **network model** representative of the **entire month** and incorporating **significant scheduled outages** at the time the CRR Network Model was created. On a given day during the month, **unplanned outages** or **short-term outages** that were not deemed significant for the month can occur, so the actual transmission capability may be lower than the auction model assumed, leading to oversold conditions.
2. **The Target Payment is a positive value** — if the Target Payment is negative, there is no deration.
3. **The CRR source or sink is a Resource Node** — if no Resource Node is involved (e.g. path is between two Load Zones), there is no deration.

So: **if Target Payment is negative or if no Resource Node is involved, there is no deration.** Deration only applies when transmission is oversold, the CRR would otherwise receive a positive payment, and the CRR path touches a Resource Node.

**How oversold is determined (prior to Day-Ahead Market):** ERCOT runs a two-step process each day before the Day-Ahead Market clears.

1. **Day-Ahead Network Operations Model** — The first step is to develop the **Day-Ahead Network Operations Model**. Like the CRR (Auction) model, it is based on the **Network Operations Model**. It is **developed daily** and reflects the **forecasted transmission system for the next operating day**, updated with **scheduled outages** and **forecasted system conditions**.

2. **Day-Ahead Simultaneous Feasibility Test** — The next step is to run the **Simultaneous Feasibility Test** (the same type of test used elsewhere, e.g. for Pre-assigned CRRs to NOIEs). It is **executed daily, just prior to clearing the Day-Ahead Market**. The **Day-Ahead Market Simultaneous Feasibility Test** verifies the **current feasibility** of CRRs that were sold in the Auction, based on **expected conditions for the operating day**.

**Outcomes:** If **all CRRs currently owned are still simultaneously feasible** under this test, transmission elements are **not oversold** and CRR Account Holders are entitled to their **full Target Payment**. If **any transmission elements are oversold**, then CRRs with a **Resource Node** as source or sink are subject to a **reduced payment** (deration).

**Degree of deration:** The amount by which a CRR payment is reduced depends on the **impact of the CRR’s source or sink Resource Node on the binding transmission constraint**. If the constraint is in one part of the grid but the Resource Node is far away (e.g. constraint in the north, Resource Node in the south), the Resource Node has **minimal impact** on that constraint and the CRR is subject to **minimal deration**. If the Resource Node is right next to or strongly affects the constrained element, it has **significant impact** on the constraint and the CRR is subject to **significant deration**.

**Why deration — reducing gaming:** Derating CRRs reduces opportunities for market manipulation. A company that owns both a CRR and a generator at a Resource Node can influence the price at that node. When a transmission outage creates oversold conditions, there can be incentive to **manipulate CRR value** (e.g. drive the price **down** at a source Resource Node or **up** at a sink Resource Node to increase the CRR payoff). Deration proportionally reduces CRR value when transmission capacity is reduced, which **discourages** such behavior. ERCOT also aims to ensure other CRR Account Holders are not harmed by the deration process.

**Hedge Value — maintaining value of CRR as hedge:** **Hedge Value** is used to reduce gaming while **maintaining a floor value** for CRRs as a hedge. It is based on generic **Minimum** and **Maximum Resource Prices**:

- **Minimum Resource Price (at source)** — When a Resource Node is the CRR **source**, this is the **lowest price** a resource owner would reasonably set based on generator technology (used in the hedge-value calculation so the CRR is not unduly written down by extreme offers).
- **Maximum Resource Price (at sink)** — When a Resource Node is the CRR **sink**, this is the **highest price** a resource owner would reasonably set based on generator technology.

Examples of these prices for common resource types (MINRESPR_J at source, MAXRESPR_K at sink): **Nuclear** −$20/MWh (min), $15/MWh (max); **Coal** $0 (min), $18/MWh (max); **Simple Cycle >90 MW** FIP×10 (min), FIP×14 (max); **Combined Cycle >90 MW** FIP×5 (min), FIP×9 (max); **Wind** −$35/MWh (min), $0 (max). An exhaustive list is in **Section 4 of the ERCOT Protocols**.

**Hedge Value Price** is the sink-minus-source price difference used for this floor value (analogous to how CRR value is DASPP_sink − DASPP_source). **Minimum Resource Price** is substituted for the Day-Ahead Settlement Point Price when the **source** is a Resource Node; **Maximum Resource Price** is substituted when the **sink** is a Resource Node. If **no Resource Node** is involved, no Hedge Value is calculated. The formulas by scenario:

- **Source is a Resource Node, Sink is not:**  
  HV PRICE = Max(0, DASPP_sink − MINRESPR_source)

- **Source is not a Resource Node, Sink is a Resource Node:**  
  HV PRICE = Max(0, MAXRESPR_sink − DASPP_source)

- **Both Source and Sink are Resource Nodes:**  
  HV PRICE = Max(0, MAXRESPR_sink − MINRESPR_source)

In each case, **Max(0, …)** ensures the Hedge Value Price is non-negative.

**Payment when deration applies:** Hedge Value is compared to Target Payment to determine whether a CRR is exposed to deration and what the CRR Owner actually receives:

- **Target Payment < Hedge Value:** The CRR Owner receives the **Target Payment**, even if there are oversold transmission elements (no reduction below Target Payment in this case).
- **Hedge Value < Target Payment and CRR is derated:** The CRR Owner receives **Hedge Value or the derated payment, whichever is greater** — so the floor from Hedge Value is applied when deration would otherwise cut the payment below that floor.

#### CRR Settlements — summary

In this section you have seen:

- **Settlements associated with CRRs** — buying, owning, and selling CRRs (e.g. CRR Auction revenues, Day-Ahead Target Payment, deration, Hedge Value, Shortfall Charges, CRR Balancing Account and Fund).
- **The flow of money related to CRRs in the ERCOT markets** — CRR Auction money flow (collection and distribution to QSEs representing Load); Day-Ahead Congestion Rent (inflows, outflows, surplus, shortfall); payment to CRR Account Holders; how ERCOT uses the **CRR Balancing Account** (month-end liquidation, Balancing Account Fund, $10M cap, distribution to QSEs when over cap; shortfalls and when CRR Account Holders remain short paid).
- **Settlements associated with DAM PTP Obligations** — charge (or payment) for DAM PTP Obligation bids in the Day-Ahead Market; payment to QSEs for DAM PTP Obligations in Real-Time (cash-out). The flow of money for DAM PTP Obligations (into and out of Congestion Rent, and in Real-Time) is covered in the subsection above.









































# CAISO

---

# Congestion in the Day-Ahead Market

- **What is congestion?** Congestion occurs when there is **insufficient available transmission capacity** to accommodate all energy schedules simultaneously in the Day-Ahead Market.

- **Directional nature:** Energy exchanged in the Day-Ahead Market is **not** directionally dependent (power can flow either way on a line). **Congestion is directional**: insufficient transmission capacity may occur in a **specific direction** on a path.

- **Summary:** Energy flow is **bidirectional** on a transmission path; congestion may occur in **either direction but not both simultaneously** on that path. So a single path can be congested in one direction at a time, which drives locational price differences and the value of financial transmission rights (FTRs) that pay when congestion occurs in a specified direction.

---

# What Is Grid Congestion, and How Does It Impact Prices?

*Summary based on [Yes Energy — What Is Grid Congestion, and How Does It Impact Prices?](https://www.yesenergy.com/blog/what-is-electricity-grid-congestion).*

- **How electricity flows:** Electricity flows through transmission lines like water through pipes; **load** (e.g. turning on a light) “drains” power from the grid. Lines have different **sizes/capacities**. **Transmission lines have a maximum safe flow**; electricity must be **produced and consumed in near real time**, which makes it hard to control.

- **Why control flow:** **System operators** (ISOs/RTOs in competitive markets) must **monitor and control** flow so the grid stays **safe and reliable** for all consumers.

- **What is grid congestion:** Congestion occurs when **a piece of equipment exceeds its capacity** — more power is flowing than it can **safely** hold. **Capacity** = amount of electricity that can safely flow through a line or other equipment. Too much flow can **damage equipment**, cause **outages**, or **fire**. Analogy: like a **traffic jam** — too many electrons on a line.

- **What happens when there’s congestion:** ISOs/RTOs use **contingency planning** and **mathematical models** (day-ahead and real-time) to find areas at risk. When the model finds an issue, the ISO puts a **constraint** on the system. A **constraint** marks equipment that is in danger of being congested. Operators **influence generation** via **pricing signals**: **higher prices** → more generation; **lower prices** → less generation.

- **How LMPs differ under a constraint:** **LMPs** carry the price signals. The **shadow price** is the value of relaxing a binding constraint by 1 MW. The ISO multiplies it by a **shift factor** (between -1 and 1). Nodes **strongly affected** by the constraint have **larger |shift factor|** → prices move **up or down** where the grid must respond. **Relief:** a plant may **ramp up** when LMP spikes (sell at higher price) or **ramp down** when LMP drops (e.g. **wind curtailment** when LMP goes negative).

- **Example (Lenox constraint):** Pennsylvania (near Scranton), overcast Wednesday ~5 a.m. **Before constraint:** nodal prices flat; congestion component ~**\$0.37/MWh**. **At 5:05 a.m.** a **Lenox constraint** is binding: congestion **drops to -\$660/MWh** on one node and **surges to \$944/MWh** on the other — signal to **increase generation to the northeast**, **decrease to the west**. Constraint is on a **115 kV line**; contingency is the **Etowanda–Hillside 230 kV line** (if that 230 kV line fails, flow would overload the 115 kV). **Hamilton Liberty** combined cycle plant (870 MW) at 5 a.m. earns ~**\$21/MWh** at full output; at 5:05 a.m. LMP at its node goes to **-\$357/MWh** (paying to put power on). The plant **ramps down** in response. At **5:25 a.m.** constraint clears, LMP returns to ~**\$23/MWh**, plant **ramps back up**. Illustrates how **constraints and congestion** keep the grid safe and how **generators respond to price signals**.

- **Use for participants:** **Historical constraint data** is used to analyze when constraints may recur; this informs **dispatch and operations** and **transmission planning**, and is a **key input** to many **trading strategies**.

---

# Congestion Revenue Rights

- **Definition:** **Congestion Revenue Rights (CRRs)** are financial instruments that allow holders to **hedge congestion variability** under day-ahead **Locational Marginal Pricing (LMP)**.

- **Acquisition:** CRRs are acquired by:
  - **ISO allocation** to Load Serving Entities (LSEs)
  - **Auction** to any qualified entities whose bids are awarded CRRs

## Two types of CRRs

- **CRR Obligation:**
  - The holder is **paid** if congestion is in the **same direction** as the CRR.
  - The holder is **charged** if congestion is in the **opposite direction** of the CRR.
  - Acquired through **allocation or auction**.

- **CRR Option:**
  - The holder is **paid** if congestion is in the **same direction** as the CRR.
  - **No payment or charge** if congestion is in the **opposite direction** of the CRR (option-like payoff).
  - Available to **project sponsors of merchant transmission facilities** that do not elect some form of regulatory cost recovery, or **converted merchant transmission facilities**.

## CRR acquisition opportunities

- **Allocation at no cost:** CRRs are **allocated at no cost** to entities that support the upkeep of the transmission system through payment of the **Transmission Access Charge (TAC)** or **Wheeling Access Charge (WAC)**.

### CRR allocation overview

- The ISO has the **authority to allocate (give) CRRs at no cost** to entities that qualify. Qualified entities are limited to **Internal Load-Serving Entities (LSEs)** and **qualified Out of Balancing Authority Area LSEs (OBAALSEs)**. These entities must meet **specific requirements** to participate in the CRR allocation process.

- **Qualification criteria:**
  - **LSEs:** Qualifications are determined based on their **eligible load**.
  - **OBAALSEs:** Qualifications are determined based on both their **eligible load** and **existing contracts**.

- **Allocation process (three steps):**
  1. **ISO determines need** — The ISO identifies the need for CRR allocation.
  2. **CRR allocation given** — The ISO grants CRRs to qualified entities.
  3. **LSE/OBAALSE becomes CRR holder** — The qualified entity officially receives and holds the CRRs.

### CRR allocation process

- The ISO allocates CRRs through both **monthly** and **annual** processes.

- **Monthly allocation:**
  - Begins approximately **30 days before** the start of the relevant operational month.
  - **Eligible MW quantity** is determined based on **forecasted load data**.
  - **Outages are modeled** (e.g. transmission line disruptions) in the monthly process.

- **Annual allocation/auction:**
  - Begins approximately **4 months before** the beginning of the CRR year.
  - **Eligible MW quantity** is determined based on **historic load data**.
  - **Outages are generally not modeled**; the assumption is that all transmission lines are in-service unless a **long-term outage** is specifically known prior to execution of the annual process.

- **Eligible allocation entities:**
  - **Internal Load-Serving Entities (LSEs):** A transmission or distribution utility **inside the CAISO Balancing Authority Area** that has contractual or regulatory obligations to connect its load to the transmission grid.
  - **Out of Balancing Authority Area LSEs (OBAALSEs):** Authorized to provide additional resource capacity to be **imported into the Balancing Authority Area** when needed.
  - **Project sponsors of merchant transmission facilities** that do **not** elect some form of regulatory cost recovery. A **merchant transmission facility** is a transmission facility on the CAISO Controlled Grid whose costs are paid by a project sponsor that does **not** recover the cost of the transmission investment through the CAISO Access Charge, WAC, or other regulatory cost recovery mechanism.

- **Auction of unallocated CRRs:** The ISO may **auction unallocated CRRs** to candidate CRR holders who provide the **required minimum collateral**.

### CRR auction overview

- **CRRs that are not allocated** are put up for auction. After the **monthly and annual allocation** processes, **qualified entities** interested in acquiring CRRs may submit a **bid** through an **annual** and/or **monthly** auction. The **annual auction does not include Long Term CRRs**.

- **Auction process (three steps):**
  1. **Remaining CRRs sent to auction** — Unallocated CRRs are offered for sale.
  2. **Qualified entity submits bid** — Interested entities bid for CRRs (subject to collateral and eligibility).
  3. **Entity may receive award & become CRR holder** — Winning bidders receive CRRs and become CRR holders.

- **Secondary market:** Some entities may also **acquire CRRs from CRR holders** through the **Secondary Registration System (SRS)**, where CRRs are **traded bilaterally** (i.e. not through the ISO auction).

### Auction bidding

- **All bids** submitted into the auction process are subject to:

  - **Initial validations** of **maximum portfolio credit exposure** against the **aggregate credit limit**.

  - **Bid designation:** Bids must be designated to **one** of these locations:
    - **Load aggregation point (LAP)**
    - **Generator (GEN)**
    - **Trading hub (TH)**
    - **Scheduling point (SP)**

  - A **Simultaneous Feasibility Test (SFT)** with **all previously allocated CRRs** for the same period and **Time-of-Use (TOU)**, modeled as **fixed injections and withdrawals** (i.e. feasibility is checked jointly with existing CRRs).

### Auction clearing prices

- **CRR APNode Market Clearing Prices (MCPs)** are **published after each market**.

- **General formula:** The CRR clearing price is the **MCP at the source/injection minus the MCP at the sink/withdrawal**:
  - **CRR clearing price = MCP<sub>source</sub> − MCP<sub>sink</sub>**

- **Buy offers:**
  - A **positive** clearing price is a **charge to the bidder** (e.g. MCP<sub>source</sub> = $300, MCP<sub>sink</sub> = $200 → clearing price = $100 charge).
  - A **negative** clearing price is a **payment to the bidder**.

- **Sell offers:**
  - A **positive** clearing price is a **payment to the seller** (e.g. MCP<sub>source</sub> = $300, MCP<sub>sink</sub> = $200 → clearing price = $100 payment).
  - A **negative** clearing price is a **charge to the seller**.

## Components of CRRs

Every CRR is described by **six components**:

- **CRR Type**
- **CRR Term**
- **Sink / Withdrawal** (withdrawal node or zone)
- **Source / Injection** (injection node or zone)
- **Time-of-use:** Refers to **on-peak** or **off-peak** hours.
- **MW Quantity:** Refers to the **number of megawatts** specified in the CRR.

### What are source and sink?

- **Source (injection):** A **source**, or **injection**, occurs when **available energy is added** to the ISO grid.

- **Sink (withdrawal):** A **sink** is the opposite: it is a **withdrawal of energy** from the ISO grid.

- **Flow on constraints:** Each **source/sink pair** creates flow on the operating constraints of the **Full Network Model (FNM)**. The direction of the CRR (source → sink) determines the direction of the hedged congestion.

- **Balancing in the CRR model:** **Injection and withdrawal megawatts (MW)** should be **balanced** in the CRR model (i.e. the MW quantity at the source equals the MW quantity at the sink for the CRR).

## Simultaneous Feasibility Test

- **Purpose:** The **Simultaneous Feasibility Test (SFT)** is used to ensure the ISO issues CRRs that are **feasible** with respect to flow based on **network constraints**.

- **Process:** The SFT takes the **CRR source(s)**, **CRR sink(s)**, and **MW quantity(ies)** from the CRR nomination (allocation) or CRR bid (auction) and applies them to the **Full Network Model (FNM)** as if they were **generator(s)** and **load(s)**. Feasibility is then checked against the network.

- **FNM used:** The FNM used in the SFT is **similar to the model used in the day-ahead market**, including **topology** and **constraint limits**. This ensures CRRs are consistent with the same network representation used for market clearing.

## CRR terms

There are **four terms** for CRRs:

- **Monthly CRR:** A CRR acquired for **one calendar month**. Monthly CRRs are made available on a **Time-Of-Use (TOU)** basis.

- **Seasonal CRR:** A CRR acquired through the **annual allocation or auction** process with a term of **one season**, either on-peak or off-peak. For CRR processes, a season is defined as:
  - **Season 1:** January, February, March  
  - **Season 2:** April, May, June  
  - **Season 3:** July, August, September  
  - **Season 4:** October, November, December  

- **Long-Term CRR (LT):** One of the tiers in the **annual allocation process**. The **first year** is awarded as a **seasonal CRR**; the **remaining 9 years** are awarded as **LT CRRs**.

- **Merchant Transmission:** A CRR with a term of **30 years** or the **pre-specified intended life of the facility**, whichever is less. Acquisition is through a **separate process** (for project sponsors of merchant transmission facilities that do not elect regulatory cost recovery, or converted merchant transmission facilities).

## Key points

- **Congestion (Day-Ahead Market):** Congestion occurs when there is **insufficient available transmission capacity** to accommodate all energy schedules simultaneously.

- **CRRs:** CRRs help CRR holders **hedge congestion variability** in the Day-Ahead Market.

- **Allocation:** The ISO may **allocate CRRs** to entities that **maintain the transmission system** (e.g. via TAC/WAC).

- **Auction:** The ISO may **auction unallocated CRRs** to **registered CRR entities** that post the **required minimum collateral**.

- **CRR definition:** CRRs are defined by **type**, **term**, **time-of-use**, **MW quantity**, **sink**, and **source**.

- **Types:** There are **two types** of CRRs: **obligation** and **option**.

- **Terms:** CRR terms include **annual** (seasonal), **monthly**, **long-term**, and **merchant transmission**.

- **Time-of-use:** Time-of-use may be **on-peak** or **off-peak** hours.

- **Source (injection):** A source or injection occurs when **available energy is added** to the ISO grid.

- **Sink (withdrawal):** A sink is the opposite—**withdrawal of energy** from the available ISO grid.

- **FNM modeling:** In the **Full Network Model (FNM)**, a source is modeled as an **injection**; a sink is modeled as a **withdrawal**.

- **Allocation to LSEs/OBAALSEs:** CRR **allocations** are given to **eligible LSEs and OBAALSEs** based on **specified criteria**.

- **Auction:** **Remaining CRRs** are **auctioned** to qualified entities (e.g. Scheduling Coordinators) who may **submit bids** in order to **earn income** from the CRR.

- **Secondary market (SRS):** Some entities may also **acquire CRRs from CRR holders** through the **Secondary Registration System (SRS)**.

- **Monthly eligible MW:** The **eligible MW quantity** for **monthly** CRRs is based on **forecasted load data**.

- **Annual eligible MW:** The **eligible MW quantity** for **annual** CRRs is based on **historical load data**.

---

