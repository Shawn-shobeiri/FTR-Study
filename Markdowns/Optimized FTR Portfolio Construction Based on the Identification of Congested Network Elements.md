# Optimized FTR Portfolio Construction Based on the Identification of Congested Network Elements

## Abstract

**Congestion and constraints**

- A **constraint** is a transmission element with a flow limit; when binding, it causes **congestion** (LMPs differ by location).
- **Shift factor (SF)** = impact of a resource’s output on a constraint’s flow; Δ Flow = Δ output × SF.
- **Shadow price (SP)** = cost of re-dispatching to resolve the constraint ($/MW).
- **LMP** at a node: LMP = λ − (SP × SF); congestion creates locational price differences (Source–Sink spread).

**Identifying congested elements**

- Binding constraints are those at their flow limits in the market solution (SCED/DAM).
- Congested **network elements** (lines, interfaces) drive the Source–Sink spreads that CRRs/FTRs pay on.

**CRRs / FTRs as congestion hedges**

- **Congestion Revenue Rights (CRRs)** / **Financial Transmission Rights (FTRs)** pay the **price spread** (Sink − Source) × MW.
- **PTP Obligation:** payment or charge in DAM (or RT, depending on product).
- **PTP Option:** payment only when spread is favorable; no charge when negative.
- **CRR auction:** inputs = Bids, Offers, Network Model → outputs = Awards, Prices. CRRs are auctioned by time-of-use blocks and one-month strips.

**Portfolio construction**

- **Objective:** choose a set of CRRs/FTRs (Source–Sink, MW, product type) to hedge congestion risk or optimize value given expected congestion patterns.
- **Relevance of congested elements:** portfolios are built around **identified binding constraints** and the **Source–Sink pairs** whose spreads are most affected (e.g. via shift factors and shadow prices).
- **Data:** network model, historical or forecast LMPs/spreads, constraint binding patterns, and CRR auction results support identification of congested elements and portfolio optimization.

**Operational context**

- **SCED** (Security Constrained Economic Dispatch) runs every 5 minutes; binding constraints and shadow prices determine real-time LMPs.
- **DAM** clears energy and ancillary services; DAM LMPs (and spreads) drive CRR settlement for monthly CRRs.
- **Real-time** spreads drive PTP obligation settlement when products are settled at RT.

**Slack bus (swing/reference bus) in the network model**

- In the underlying power‑flow model, one bus is chosen as the **slack (swing or reference) bus**. It has fixed **voltage magnitude and angle** (angle usually set to $0^\circ$) and its **real and reactive power injections are solved for** so that total generation equals total load plus losses.
- All other buses inject/withdraw specified P and/or Q (PQ or PV buses); the slack bus represents the **balancing resource/grid** that absorbs the mismatch between scheduled injections and actual flows and anchors the system’s voltage angle reference.

**Paper focus and approach**

**Goal of the paper:** Build an **optimized FTR/CRR portfolio** for a market participant by focusing on **binding constraints** (not LMP differences across all node pairs), letting the participant choose **focus constraints** and **positions**, and constructing the portfolio with the **minimum number of node pairs** via **orthogonal matching pursuit (OMP)**.

- Builds an **optimized FTR/CRR portfolio** for a market participant given his assessment of **binding-constraint frequency and economic impact**.
- Recasts FTR selection from **LMP-difference-based methods** (data-heavy, compute-heavy) to a **constraint-centric** view: **binding constraints** are physically observable and drive LMP differentials via the DAM clearing model.
- **LMP differentials** are due to congestion and are **manifestations of binding constraints** in the transmission network.
- Exploits **topological characteristics** of large-scale interconnections.
- Participant specifies the subset of **“focus” constraints** and the **position** he is willing to take on each.
- Uses **orthogonal matching pursuit (OMP)** to construct the optimized FTR portfolio with the **minimum number of node pairs** for specifying FTR elements.
- Applied to a **PJM-based test system** to illustrate capabilities in **realistic large-scale** networks.

## Introduction

**Congestion and its impacts (summary from literature)**

- Congestion has **major impacts** on electricity markets: it can **restrict** some transactions and **block** others.
- With congestion, **sellers** cannot sell wherever they wish and **buyers** cannot buy from whomever they want → **higher electricity prices** at various locations.
- **Focus:** congestion in **day-ahead markets (DAMs)**. In each hourly DAM, sellers receive the **LMP at the point of injection** and buyers pay the **LMP at the point of withdrawal**.
- When seller LMP ≠ buyer LMP, **congestion rents** are collected by the **independent grid operator (IGO)**.
- **LMP uncertainty** → **uncertain congestion rents** → creates **demand for hedging instruments**: Financial Transmission Rights (FTRs), Congestion Revenue Rights (CRRs), or Flow Gate Rights (FGRs).

**FTR vs FGR; FTR definition and use**

- **FTR:** Entitle the holder to receive the **value of congestion** as established by the **LMP difference** of each DAM over the holding period.
- **FGR:** Entitle the holder to be reimbursed the value of congestion determined by **transmission usage charges** on a congested network element in a specified direction.
- **Paper focus:** **FTR**, since FTRs are the hedging instruments widely used by IGOs.

**How FTR hedges physical delivery**

- A holder with a **physical transaction** at the **same injection–withdrawal node pair** as the FTR is **not impacted financially** by the LMP difference between the nodes as long as the FTR **MW is at or above** the physical delivery.
- The FTR **reimburses** the holder the **congestion rents** collected by the IGO for that path.

**FTR structure**

- **Directional:** Defined by a **source (from)** and **sink (to)** node pair.
- **Holding period:** Start and end times.
- **Class:** Coverage subperiods — typically **on-peak**, **off-peak**, or **around-the-clock**.

**FTR contract vs option**

- **FTR contract:** Pays the holder when congestion is in the direction of the FTR (positive LMP difference); becomes a **liability** when the LMP difference is **negative** (congestion in the opposite direction).
- **FTR option:** **Exercised only when** the reimbursement is **beneficial** to the holder (no liability when congestion is opposite).

**FTR auctions and market participants**

- The **IGO runs periodic auctions** in which it **sells FTR** to buyers who bid for offered quantities.
- **Hedgers:** Buy FTR to ensure **reimbursement** for congestion rents incurred on their **physical transactions**.
- **Speculators:** Purchase FTR **without physical flows** in order to make profits.
- IGOs promote **FTR market liquidity** and encourage participation of entities without physical flows to **increase competition** in FTR auctions. Although FTR were originally intended as **insurance for physical transactions**, speculation is common industry practice.

**Literature and paper contribution**

- **Origins:** Hogan [3] introduced the mathematical framework for FTR; a more detailed treatment followed in 2002 [4]. Implementation varies by jurisdiction [5]–[8], with comparative analyses in [9]. Auction clearing and outcomes are studied in [11]–[14]; FTR in transmission expansion and investment in [15]–[18]; comprehensive survey in [19].
- **Gap:** **Systematic construction of FTR portfolios** (for speculative or hedging purposes) has **not been studied**.
- **This paper:** Develops a **methodology** for building FTR portfolios for use by **hedgers or speculators** (referred to as **market players**). The focus is on **insights from DAM analysis** that participants can use to construct FTR portfolios effectively.

**FTR as a set of constraints; paradigm and methodology**

- **LMP differentials** across the system are **manifestations of congestion**. Different binding constraints can affect an FTR’s sink–source LMP differential in **opposite** ways (one constraint may increase the spread, another decrease it).
- **Purchasing FTR** is thus equivalent to **taking positions on a set of constraints**. FTR give participants a way to **express views** on **transmission usage charges** arising from **network element constraints**.
- **Paper’s main thrust:** **Use these FTR characteristics and the topological features of large-scale interconnections to systematically construct an FTR portfolio.** Propose a **practical methodology** to build an **optimized FTR portfolio** by:
  - Choosing a set of **“focus” constraints** and
  - Specifying the **positions** the participant is willing to take on those constraints.
- **Paradigm shift:** Move from **computationally intensive** use of **historical LMP differences** of node pairs to a **constraint-centric** view based on **binding constraints** in the transmission network.
- **Constraint classification:** Explicitly account for the participant’s ability to **model transmission usage charges** on a constraint. Classify all focus constraints into **three non-overlapping** subsets:
  - **Specified congestion participation**
  - **Zero congestion participation**
  - **Do-not-care congestion participation**
- **Portfolio construction:** From the **specified flows** on each constraint, select a **subset of nodes** (using **topological** considerations) as candidate FTR **source or sink** nodes, and build the portfolio with the **minimum number of FTR positions**. The resulting portfolio **induces the desired real power flows** on the specified constraints.
- **Benefit:** Formulating the problem in terms of **underlying constraints** (rather than node-pair LMP differences) lets participants **use their views** on **system transfer capability limitations** in a structured way.

## FTR MARKET PARTICIPANT PROBLEM

**Market participants and portfolio construction challenges**

- **Market participants** are **hedgers** and **speculators**.
- **Hedgers** have physical flows on the network and may pay congestion rents to the IGO; they aim to build an FTR portfolio whose **revenues over the holding period are at least equal to** the congestion rents they pay.
- **Speculators** buy FTR in auctions as an **“investment”** (no physical flows).
- Both face a **difficult portfolio construction problem**: uncertainty and the **large number of possible FTR combinations** make the problem **unmanageable** unless additional specific constraints are introduced.
- There is **inadequate information** about **future revenue streams** from FTR holdings.
- **Exhaustive evaluation** of all possible FTR combinations in a large-scale network is **computationally too demanding**, especially when accounting for the **wide variation in LMP differences** across nodes over the **many hours** of the holding period.

**Simplifying assumptions and solution approach**

- The paper **solves the portfolio construction problem** under **simplifying assumptions**.
- **Setting:** FTR acquisition in a **single auction**, for **contracts of identical class** over a **specified holding period**.
- **Price-taker assumption:** Participants do **not** procure **significant MW** of FTR so as to **impact auction clearing prices**.
- **Isolated analysis:** For a given participant, **all other FTR** already held by that participant are **ignored**.
- **Reformulation:** The problem is **recast** so that the **topological and physical nature** of the network and **historical data** can be used effectively.
- **Result:** This yields **mathematical insights** that **reduce the solution state space** and support the **proposed solution approach**.

**Congestion and transmission usage charges**

- The analysis **starts from congestion** on the network: some **network elements** are **congested** when their **transfer capability limits** are reached and the **associated constraints become binding**.
- The **IGO** charges every **transaction that flows on a congested element** for its use; the charge is set at the **marginal benefit of the last MW** of flow that makes the constraint binding.
- These **transmission usage charges** on **binding constraints** are the **basis for computing the congestion rents** collected by the IGO.

**Hedger reimbursement**

- A **hedger** who holds **FTR** in a given **MW amount** from a **source to a sink** node and has a **physical transaction** in the **same MW amount** on the **same node pair** receives **reimbursement** from the IGO for the **transmission usage charges** whenever **congestion occurs** during the **holding period**.

**Speculator revenues**

- A **speculator** who holds **FTR** for the **same node pair and amount** has **no physical flows**, so he **does not incur congestion charges**; the **reimbursements** paid by the IGO (when congestion occurs on that path) **constitute his revenues**.

**Nomenclature**


| Symbol                                 | Definition                                                                               |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| $\|\mathbf{a}\|_p$                     | $p$-norm of vector $\mathbf{a}$.                                                         |
| $\mathcal{F}$                          | FTR portfolio.                                                                           |
| $\mathcal{G}$                          | Subset of nodes selected to construct$\mathcal{F}$.                                      |
| $K$                                    | Number of FTR in$\mathcal{F}$.                                                           |
| $\mathcal{L} \mid h$                   | Set of connected lines in the network in hour$h$.                                        |
| $\tilde{\mathcal{L}} \mid h$           | Set of congested lines in hour$h$.                                                       |
| $\mathcal{L}[c]$                       | Subset of outaged lines.                                                                 |
| $\mathcal{Q}_j$                        | System pattern class$j$.                                                                 |
| $\mathcal{R}_0$                        | "Zero congestion participation" subset.                                                  |
| $\mathcal{R}_1$                        | "Specified congestion participation" subset.                                             |
| $(\mathcal{R}_0 \cup \mathcal{R}_1)^c$ | "Do-not-care congestion participation" subset.                                           |
| $\mathcal{T}$                          | FTR holding period.                                                                      |
| $\mathcal{U}$                          | Set of ordered node pairs that belong in$\mathcal{G}$.                                   |
| $U$                                    | Cardinality of the set$\mathcal{U}$.                                                     |
| $z$                                    | MW position on a constraint.                                                             |
| $\Gamma = \{i, j, \gamma\}$            | FTR with the source (sink) node$i$ ($j$) in the amount $\gamma$ MW.                      |
| $\delta$                               | Categorical variable; determines if a line belongs to$\mathcal{R}_0$ or $\mathcal{R}_1$. |


| Symbol                        | Definition                                                                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $\Delta f_\ell \mid_h$        | Change in the real power flow at line$\ell$ in hour $h$.                                                                                                                |
| $\zeta$                       | Quadruplet that specifies the market participant's requirements.                                                                                                        |
| $\eta \mid_h$                 | $\Gamma$ FTR revenues in hour $h$.                                                                                                                                      |
| $\lambda_n \mid_h$            | LMP at node$n$ in hour $h$.                                                                                                                                             |
| $\mu_\ell \mid_h$             | Transmission usage charge for line$\ell$ in hour $h$.                                                                                                                   |
| $\mu_\ell^M \mid_h$           | Dual variable for the transmission constraint in the forward direction in hour$h$.                                                                                      |
| $\mu_\ell^m \mid_h$           | Dual variable for the transmission constraint in the reverse direction in hour$h$.                                                                                      |
| $\phi_\ell^{\{n,n'\}} \mid_h$ | Line$\ell$ PTDF with respect to node pair $\{n, n'\}$ in hour $h$.                                                                                                      |
| $\tilde{\Phi}$                | Matrix of the PTDFs with respect to the node pairs in$\mathcal{W}$ of the lines and for the network topologies specified by $\zeta$s; row $v$ corresponds to $\zeta^v$. |
| $\Omega = \{m, n, a\}$        | Transaction from node$m$ to node $n$ in the amount $a$ MW.                                                                                                              |

## DAM CLEARING MECHANISM

The power system has **(N+1) nodes** $\mathcal{N} = \{0, 1, \ldots, N\}$ with the **slack bus** at node 0, and **$L$ lines** $\mathcal{L} = \{l_1, \ldots, l_L\}$. Each line $l$ is an ordered pair $(n, m)$ (from node $n$ to node $m$, $n, m \in \mathcal{N}$); real power flow $f_l \geq 0$ when flow is from $n$ to $m$, and $f_l < 0$ otherwise. The network is **lossless**. We use the **diagonal branch susceptance matrix** $\mathbf{B}_d \in \mathbb{R}^{L \times L}$, the **reduced branch-to-node incidence matrix** $\mathbf{A} \in \mathbb{R}^{L \times N}$ (for nodes $\mathcal{N} \setminus \{0\}$), and the **nodal susceptance matrix** $\mathbf{B} \in \mathbb{R}^{N \times N}$. There are **no phase shifting devices**. The **slack bus nodal susceptance vector** is $\mathbf{b}_0 = [b_{01}, \ldots, b_{0N}]^T$ with $\mathbf{b}_0 + \mathbf{B}\mathbf{1}^N = \mathbf{0}$ ($\mathbf{1}^N$ = $N$-vector of ones). The subscript $|_h$ denotes the value for **hour $h$** of the holding period.

The **hour $h$ DAM problem** is stated for **sellers** $\mathcal{S}|_h \triangleq \{s_1|_h, \ldots, s_S|_h\}$ and **buyers** $\mathcal{B}|_h \triangleq \{b_1|_h, \ldots, b_B|_h\}$. The hour $h$ DAM clearing **maximizes the social surplus** of these buyers and sellers. **Power injection** and **withdrawal** at each node $n \in \mathcal{N}$ are:

$$
p_n^e|_h = \sum_{\substack{s_i|_h \in \mathcal{S}|_h \\ \text{at node } n}} p^{s_i}|_h

$$

$$
p_n^x|_h = \sum_{\substack{b_j|_h \in \mathcal{B}|_h \\ \text{at node } n}} p^{b_j}|_h

$$

**The hour $h$ DAM optimization problem** is:

$$
\max \left\{ \sum_{j=1}^{B|_h} \beta^{b_j|_h}\big(p^{b_j|_h}\big) - \sum_{i=1}^{S|_h} \kappa^{s_i|_h}\big(p^{s_i|_h}\big) \right\}

$$

subject to (dual variables on the right):

$$
\underline{\mathbf{p}}^e|_h - \underline{\mathbf{p}}^x|_h = \underline{\mathbf{B}}|_h \underline{\boldsymbol{\theta}}|_h \quad \longleftrightarrow \quad \underline{\lambda}|_h \quad \text{(power balance)}

$$

$$
p_0^e|_h - p_0^x|_h = \underline{\mathbf{b}}_0^T|_h \underline{\boldsymbol{\theta}}|_h \quad \longleftrightarrow \quad \lambda_0|_h \quad \text{(slack bus)}

$$

$$
\underline{\mathbf{f}}|_h = \underline{\mathbf{B}}_d|_h \underline{\mathbf{A}}|_h \underline{\boldsymbol{\theta}}|_h \leq \underline{\mathbf{f}}^M|_h \quad \longleftrightarrow \quad \underline{\mu}^M|_h \quad \text{(flow upper limit)}

$$

$$
-\underline{\mathbf{f}}|_h \leq \underline{\mathbf{f}}^m|_h \quad \longleftrightarrow \quad \underline{\mu}^m|_h \quad \text{(flow lower limit)} \qquad (17)

$$

Network topology and line flow limits can change over the FTR holding period; these effects are not captured in FTR auctions but are reflected in **DAM clearing outcomes** and thus in FTR revenues. The **dual variables** in (17) are central to FTR analysis: $\underline{\lambda}|_h$ and $\lambda_0|_h$ are the **LMPs**; a non-zero LMP difference between two nodes indicates **binding transmission constraints**. The duals for the transmission constraints are $\underline{\mu}^M|_h$ (forward flow limit) and $\underline{\mu}^m|_h$ (reverse flow limit). At most one of the two limits is binding at any time, so at least one of $\underline{\mu}^M|_h$ and $\underline{\mu}^m|_h$ is zero. The **transmission usage charge vector** for the $L|_h$ lines in hour $h$ is $\underline{\mu}|_h = \underline{\mu}^M|_h - \underline{\mu}^m|_h$.

---

**Problem formulation and notation**

- The **salient structural characteristics** of the power system network are used to **recast the market participant's problem** into a **more convenient form**; notation is introduced to obtain a **mathematical statement** of the problem.
- **Single FTR (equation 1):** An FTR with **source** node $i$, **sink** node $j$, and **MW amount** $\gamma$ is denoted by the ordered triplet

  $$
  \Gamma = \{i, j, \gamma\}

  $$
- **Portfolio (equation 2):** The **set of FTR in the portfolio** is

  $$
  F = \{\Gamma_k : k = 1, 2, \ldots, K\}

  $$

  where the portfolio contains $K$ FTRs.
- For each $\Gamma_k$ in $F$, the triplet elements $i_k$ (source), $j_k$ (sink), and $\gamma_k$ (MW) are specified for $k = 1, \ldots, K$.
- **Holding period:** $T = \{h_1, \ldots, h_{|T|}\}$ denotes the FTR holding period (discrete time intervals or hours; $|T|$ = number of intervals).

**LMP difference and congested lines (equation 3)**

- The **hourly DAM** is formulated mathematically as described above; the presentation is simplified by considering **only lines** as network elements.
- **Congested lines** in hour $h$: $\tilde{\mathcal{L}}_h = \{ \ell_i : \ell_i \in \mathcal{L} \mid h,\ \mu_{\ell_i} \mid h \neq 0 \}$. **Uncongested lines** do not contribute to LMP differences because their dual variable $\mu \mid h$ is zero by **complementary slackness**.
- The **LMP difference** between a node pair and the **dual variables** of transmission constraints are related via the **Lagrangian**, **stationarity**, and **complementary slackness** conditions, yielding **equation (3):**

  $$
  \lambda_{n'} \mid h - \lambda_n \mid h = \sum_{\ell \in \tilde{\mathcal{L}}_h} \phi_{\ell}^{\{n,n'\}} \mid h \left( \mu_{\ell}^M \mid h - \mu_{\ell}^m \mid h \right) \quad (3)

  $$

  - **LHS:** $\lambda_{n'} \mid h - \lambda_n \mid h$ = LMP at node $n'$ minus LMP at node $n$ in hour $h$.
  - **RHS:** Sum over **congested lines** $\ell \in \tilde{\mathcal{L}}_h$ of (PTDF × dual difference). $\mu_{\ell}^M \mid h$ and $\mu_{\ell}^m \mid h$ are dual variables for the **upper and lower** flow limits on line $\ell$ at hour $h$.
- **PTDF** $\phi_{\ell}^{\{n,n'\}} \mid h$: the **line $\ell$ power transfer distribution factor** with respect to an injection/withdrawal at the node pair $\{n,n'\}$ in hour $h$ (see [21]). It is the **fraction of the transaction from node $n$ to node $n'$ that flows on line $\ell$** in hour $h$.

**FTR revenues and line flow changes (equations 4–6)**

- The **hour $h$ market outcomes** determine the **FTR revenues** $\eta|_h$ for the FTR $\Gamma = \{i, j, \gamma\}$:

  $$
  \eta|_h = (\lambda_j|_h - \lambda_i|_h)\,\gamma = \sum_{\ell \in \tilde{\mathcal{L}}|_h} \big(\mu_\ell^M|_h - \mu_\ell^m|_h\big)\, \phi_\ell^{\{i,j\}}|_h\,\gamma \quad (4)

  $$
- An **injection** $\gamma$ at node $i$ and **withdrawal** $\gamma$ at node $j$ cause a **change** $\Delta f_\ell|_h$ in the flow on line $\ell$ in hour $h$:

  $$
  \Delta f_\ell|_h \approx \phi_\ell^{\{i,j\}}|_h\,\gamma \quad (5)

  $$
- Assuming the approximation in (5) holds:

  $$
  \eta|_h = \sum_{\ell \in \tilde{\mathcal{L}}|_h} \big(\mu_\ell^M|_h - \mu_\ell^m|_h\big)\, \Delta f_\ell|_h \quad (6)

  $$

  So FTR revenues in hour $h$ equal the sum over **congested lines** of (transmission usage charge difference × change in line flow).

  Here, $\mu_\ell^M|_h$ and $\mu_\ell^m|_h$ are the **dual variables** for the **upper** and **lower** flow limits on line $\ell$ in hour $h$. Their difference

  $$
  \mu_\ell^M|_h - \mu_\ell^m|_h

  $$

  is the **net transmission usage charge** (in \$/MW) for using scarce capacity on line $\ell$ in its modeled positive direction. Intuitively, it is the **marginal cost per MW** of pushing additional flow on that congested line (taking both directions into account). Equation (6) therefore says that the FTR’s revenue in hour $h$ is the **dot product** of:
  (i) the vector of **transmission usage charges** on all congested lines, and
  (ii) the vector of **flows $\Delta f_\ell|_h$ induced by the FTR transaction** on those lines.
- **Transmission usage charge vs path-specific shadow price:** The term $(\mu_\ell^M|_h - \mu_\ell^m|_h)$ is a **property of the line** $\ell$ (and hour $h$); it does **not** depend on the node pair $\{i,j\}$ and is the same for every path. The **contribution of line $\ell$ to the path $i \to j$ spread** (per MW of path flow) is $(\mu_\ell^M|_h - \mu_\ell^m|_h)\, \phi_\ell^{\{i,j\}}|_h$. So the **"shadow price for the direction $i \to j$ on line $\ell$"** is the transmission usage charge **times the PTDF** for that path: $(\mu_\ell^M - \mu_\ell^m)\, \phi_\ell^{\{i,j\}}$. The transmission usage charge is line-specific; the path-specific part is the PTDF $\phi_\ell^{\{i,j\}}$.

**Revenue dependence and FTR selection**

- From (6), for every hour $h \in \mathcal{T}$, revenues $\eta|_h$ depend **only on the transmission usage charges** for the **congested lines** $\ell \in \tilde{\mathcal{L}}|_h$.
- A **portfolio construction strategy** is to include in the portfolio $\mathcal{F}$ FTRs that, for transactions with the **same node pair and amount**, induce **desired flows** $\Delta f_\ell|_h$ on **congested lines $\ell$ of interest**. Those induced flows act as **weighting factors** for the transmission usage charge of each binding constraint.
- The **decision variables** for FTR selection are the **source and sink nodes** and the **FTR MW amounts**. **FTR selection** is therefore the choice of **node pairs $\{i, j\}$** and **amounts $\gamma$** that produce the desired flows $\Delta f_\ell|_h$ on the lines $\ell$ of interest in every hour $h$ of the holding period $\mathcal{T}$.

Given the expression in (6), we no longer need to be concerned with the LMP differences between the node pairs, rather we focus on the binding constraints. We benefit from such an approach because the number of binding constraints in a system is considerably smaller than the number of possible node pairs.

We propose a methodology to solve the market participant's problem based on the selection of the FTR in $\mathcal{F}$ such that the transactions with same node pairs and amounts induce real power flows on the congested network elements of interest. A hedger is concerned only with the flows that his transactions induce on the congested lines. He wishes to purchase FTR such that the FTR reimbursements cover the congestion charges. A speculator sees FTR as "investments". The estimated revenues have to be sufficient to cover the costs of FTR acquisition and produce profits commensurate with the perceived risks. The speculator may wish to acquire FTR such that corresponding transactions with the same node pairs and in the same amounts induce flows in all congested lines of the system during the entire holding period. But, he would need to buy a huge number of FTR, for which he would incur the associated premiums.

Therefore, a speculator or a hedger limits his selection of the subset of congested lines and specifies the level of participation ($\Delta f_\ell \mid_h$) for each line $\ell$ in the selected subset of lines.

Instead of the terms congested elements and level of participation, we use the market participant's selection of the binding constraint subset and the MW position on each binding constraint.

A key challenge is to identify which constraints are binding for the holding period. A constraint binds when the transfer capability of the system is reached while meeting the demand with the available generation resources in an economic manner. Therefore, the underlying reasons for system congestion intimately depend on the physics of the situation and take into account many additional considerations. The latter include: the economics of the available generation resources and the self-scheduling practices; the maintenance schedules and forced-outage events; the demand requirements, whether fixed or price responsive; and the ever-changing nature of the network topology due to maintenance, forced outages, new transmission equipment, and the way the system and markets are operated. A development of system congestion models along with effective FTR portfolio construction is a daunting challenge. Modeling each constraint's transmission usage charge may not be meaningful. Instead, we may wish to consider a set of "focus" constraints that we examine in depth and try to construct a probabilistic model of the transmission usage charges in terms of conditional probability distributions of the transmission usage charges by using historical market outcomes together with values of observable conditioning drivers, such as generation availability, demand levels, system topology, fuel prices, generation outputs of intermittent resources, commitment behavior, and other appropriate explanatory factors.


**Historical Analysis**

Analysis of past ISO data indicates that some constraints bind under "similar" conditions—for instance, during peak demand periods or under certain fuel-price regimes. Under certain conditions for these constraints, the analysis of historical binding frequency as well as of its economic impacts provides some relevant insights into the future behavior. An example of the use of historical data to construct an approximation of the cumulative distribution function of the transmission usage charges is to classify the explanatory drivers of the constraints, which bind under "similar" conditions, into $Q$ non-overlapping system pattern classes, $C_j$, $j = 1, \ldots, Q$. Each system pattern class is associated with specific ranges of the values of the explanatory drivers. For each class, we collect the hourly $\mu_\ell$ values and construct the conditional transmission usage charge duration curve (TUCDC) with the conditioning being such that the transmission usage charges are for that class of driver range values. We interpret the conditional TUCDC to be the complement of the cumulative distribution function of the transmission usage charges $\mu_\ell$ conditioned on the event that the driver values are in that class. The TUCDCs are one possible way of modeling transmission usage charges by using historical data.

We note that having a historical transmission usage charge model has certain limitations. System topology, available generation resources, as well as their economics, and the way that power systems are operated are continually changing. Therefore, the historical system congestion pattern may fail to hold in the future. In addition, some constraints that are rather driven by "events", such as forced outages of multiple lines coupled with planned generation outages or by system voltage support capabilities or by system stability limitations, may not be appropriately represented by the transmission usage charges based on historical data.

---

## III. Proposed Solution Approach

We use the models for the transmission usage charges to categorize the constraints of the system into three classes—**"specified congestion participation"** ($\mathcal{R}_1$), **"zero congestion participation"** ($\mathcal{R}_0$) and **"do-not-care congestion participation"** $(\mathcal{R}_0 \cup \mathcal{R}_1)^c$. We use the constraints in $\mathcal{R}_1$ and $\mathcal{R}_0$ to identify the subset of node pairs from which the market participant determines the **FTR** in the portfolio that are used to generate the revenues or the needed hedges. The membership of the "do-not-care congestion participation" subset is established in a straightforward manner since this subset is the complement of the union of the two specified subsets. Based on a **"threshold"** level for a confidence metric, we decide to **"accept"** or **"reject"** the transmission usage charge model. In particular, the estimates provided by an "accept" transmission usage charge model are considered to be reliable and close to the actual outcomes over the **FTR** holding period, in contrast with the "reject" ones that do not.

**Accept model ($\mathcal{P}_1$).** The **$\mathcal{P}_1$** subset includes constraints where the transmission usage charge model has **confidence**. Specifically, it includes network elements where transmission usage charges are known to be **non-zero** during the FTR holding period. Constraints in $\mathcal{P}_1$ are candidates for portfolio construction because their associated transmission usage charges can contribute to FTR portfolio revenues or provide hedges.

**Reject model ($\mathcal{P}_0$).** For the **"reject"** model, the outcome indicates that the modeling approach is not capable of accurately describing the frequency and economic impacts of the binding constraint, or there is a lack of crucial information on causal factors. In such cases, it is better **not to take a position** on that constraint. These constraints are included in the **"zero congestion participation"** subset $\mathcal{P}_0$. Network elements in this subset are included in FTR portfolio construction in a manner that ensures their transmission usage charges will **not** impact revenues or hedging—i.e., they do not reduce FTR portfolio revenues or create payments.

**Do-not-care subset.** The **"do-not-care congestion participation"** subset consists of lines with zero transmission usage charges for most of the FTR holding period, thus having **minimal impact** on FTR portfolio revenues or hedging ability. Constraints in this subset are particularly useful because they **augment the solution space** of candidates for the FTR portfolio construction. Based on purely topological considerations, there is a limit on the number of lines on which flows can be specified [22, pp. 56–58]. Over-constraining the problem by specifying flows on lines not congested during the FTR holding period is unnecessary, as it does not affect FTR revenues. The market participant specifies their requirements in terms of **quadruplets**.

**Requirement quadruplet** $\zeta$:

$$
\zeta = \{\delta, \ell, z, \mathcal{L}^{[c]}\} \qquad (7)
$$

- $\ell$: the **line** (constraint).
- $z$: its **MW position**.
- $\delta$: a **categorical variable** indicating whether the constraint belongs in $\mathcal{P}_0$ ($\delta=0$) or $\mathcal{P}_1$ ($\delta=1$).
- $\mathcal{L}^{[c]}$: the **subset of outaged lines** (contingency case $[c]$).

If $\delta = 0$, line $\ell$ is in $\mathcal{P}_0$ and $z = 0$ (zero impact on revenues). If $\delta = 1$, line $\ell$ is in $\mathcal{P}_1$ and $z$ is the **desired MW position** by the market participant under contingency case $[c]$. For constraints in $\mathcal{P}_1$, predetermined quantities based on budget constraints and cost expectations of auction results are used to specify the MW positions.

**Transaction triplet** $\Omega$. The next step is to construct the **transactions** that satisfy the market participant's requirements—i.e., that induce the desired MW position on the lines in the $\mathcal{P}_0$ and $\mathcal{P}_1$ subsets under the specified outages. A **transaction** $\Omega$ is the triplet:

$$
\Omega = \{m, n, a\} \qquad (8)
$$

where $m$ is the **source** (from) node, $n$ is the **sink** (to) node, and $a$ is the **MW amount** of the transaction.

We propose a practical approach for a market participant to determine the number of transactions $U$ that can ensure that the requirements of the $V$ specifications $\zeta^1, \zeta^2, \ldots, \zeta^V$ can be met. The determination of the node pairs $\{m, n\}$ is too large a problem if we consider all the possible node pairs in $\mathcal{N}$ since the number is of the order of $\binom{N+1}{2}$. Instead, we select a **subset of nodes** by taking into consideration the **physical characteristics** of the network. This selection explicitly considers the **"electrical proximity"** of each line in $\mathcal{Z}_0$ and $\mathcal{Z}_1$ with respect to a node to be selected. We use the **injection shift factors (ISFs)** as the measure of "electrical proximity" [21]. An injection at, or a withdrawal from, a specified node impacts the real power flows on the network lines to a different extent, as indicated by the ISFs of such a node. If the value of the ISF of a line with respect to a node is close to **1 p.u.** in magnitude, then the line is affected markedly by an injection at/withdrawal from that node. We say that the line has a close "electrical proximity" with respect to that node. **Our aim is to induce flows on the lines in the subsets $\mathcal{Z}_0$ and $\mathcal{Z}_1$, without impacting to a great extent the other constraints of the system and, to do so by constructing a subset with as few nodes as possible.** From our extensive testing, one practical scheme is to select the **terminal nodes** of the lines in $\mathcal{Z}_0$ and $\mathcal{Z}_1$ to construct the subset of nodes. We define the set

$$
\mathcal{G} = \big\{ g : g \text{ is either a \textit{from} or a \textit{to} node of line } \ell \text{ in the specification } \zeta^v,\; v=1, \ldots, V \big\}. \qquad (9)
$$

Clearly, $|\mathcal{G}| \ll \binom{N+1}{2}$. Since not each network node is traded in FTR auctions as either a source or a sink node—a so-called **FTR pricing node**—we need a **default option** whenever a terminal node is not a pricing node. In such a case, we verify whether there is a directly connected pricing node to the terminal node of a line $\ell$ in $\mathcal{Z}_0$ and $\mathcal{Z}_1$. Whenever two or more such nodes exist, we select the node with the **largest magnitude ISF** for that line $\ell$. In case none of the directly connected nodes is a pricing node, we repeat the search to include additional nodes that are directly connected to the non-pricing nodes found and continue until a pricing node is reached. Examples of such a selection may be found in [22, p. 27, pp. 34–38].

Starting from the subset $\mathcal{G}$ we construct the set $\mathcal{X}$ of $U$ ordered node pairs $\{m, n\}$ with

$$
\mathcal{X} = \big\{ \{m, n\} : m, n \in \mathcal{G},\; m < n \big\} \qquad (10)
$$

and $U = |\mathcal{X}| = \binom{|\mathcal{G}|}{2}$. The node pairs of possible transactions are given by $\{m_u, n_u\} \in \mathcal{X}$ for $u=1, \ldots, U$ and the transactions by the triplet $\Omega_u = \{m_u, n_u, a_u\}$. The construction requires the determination of the **amounts** $a_u$ for $u=1, \ldots, U$. To do so, we write an equation for each $\zeta^v$, $v=1, \ldots, V$. The transactions must induce the flows $z^v$ in line $\ell^v$ in the contingency case $[c]$ specified by $\zeta^v$, $v=1, \ldots, V$. We approximate the effect that a transaction has on a line $\ell$ by its **PTDF** for the specified topology [23]. Similarly, we approximate the effect of a transaction $\Omega = \{m, n, a\}$ with the line of contingency case $[c]$ outaged, on the real power flow on a non-outaged line.

Therefore, for the outage case $[c]$, the specification $\zeta^v$, $v=1, \ldots, V$ sets up the requirement

$$
\big[ \phi_{\ell^v}^{m_1,n_1}\big]^{[c]} a_1 + \cdots + \big[ \phi_{\ell^v}^{m_U,n_U}\big]^{[c]} a_U = z^v. \qquad (11)
$$

The set of $V$ requirements thus results in

$$
\widetilde{\Phi}\, a = \widetilde{z} \qquad (12)
$$

where row $v$ of $\widetilde{\Phi}$ is constructed from the PTDFs of the network topologies for the lines and contingency cases in the specifications, and $a = (a_1, \ldots, a_U)^\top$ is the vector of the $U$ transaction amounts. The matrix $\widetilde{\Phi}$ has dimensions $V \times U$. In practice $V < U$, so the system is **underdetermined**. For a solution to exist we need $U > \operatorname{rank}(\widetilde{\Phi}) = \operatorname{rank}([\widetilde{\Phi} \mid \widetilde{z}])$, i.e.,

$$
U > \operatorname{rank}(\widetilde{\Phi}) = \operatorname{rank}([\widetilde{\Phi} \mid \widetilde{z}]). \qquad (13)
$$

The **equality** in (13) shows that there exists at least one solution to the system of equations, and the **inequality** that the system is underdetermined, since the number of unknowns is greater than the number of linearly independent rows of $\widetilde{\Phi}$. To single out a unique solution we impose an additional criterion, leading to the **optimization problem**: minimize a $p$-norm of the vector $a$ subject to the constraints in (12),

$$
\min \|a\|_p \quad \text{subject to} \quad \widetilde{\Phi}\, a = \widetilde{z}. \qquad (14)
$$

**Choice $p=2$.** For the choice $p=2$, the solution may result in a **large number of non-zero** elements of $a$, leading to **incurred transaction costs** for the purchase of the corresponding FTR in the portfolio. Such a choice is thus **impractical**.

**Choice $p=0$ (minimum number of FTRs).** The choice $p=0$ minimizes the **$\ell_0$ norm** of $a$,
$$
\|a\|_0 = \lim_{p \to 0} \sum_{u=1}^{U} |a_u|^p,
$$
and determines the **minimum number of non-zero transaction amounts** that satisfy the constraints. **There are two main reasons we choose to construct an FTR portfolio with the minimum number of node pairs.** (i) If we have an FTR portfolio with minimum number of node pairs, the **FTR revenues are primarily influenced by the transmission usage charges of constraints "around" those nodes.** (ii) **It is highly impractical to participate in the FTR auction to procure a large number of FTR.** Such an effort increases the **uncertainty** of actually having the submitted bids cleared and incurs the **premium payment** for all acquired FTR. Instead, we choose the **minimum number of FTR** to lessen unintended consequences.

Minimizing the $\ell_0$ norm is a **sparse approximation problem** and is **computationally hard** (nonconvex, combinatorial). A **practical approach** is to use the **Orthogonal Matching Pursuit (OMP)** algorithm, a greedy scheme that iteratively approximates the solution to (14). By contrast, **LMP-difference-based** methods scale with the number of node pairs, which is of order $O((N+1)^2)$ for a system with $N+1$ nodes.

The number of **LMP difference variables** is **computationally highly demanding** for a large-scale network, whereas the number of **congested network elements** is typically **considerably smaller**. The proposed methodology reduces the prediction of transmission usage charges to a computation of order $O(N+1)$. The computational efficiency for **FTR portfolio selection** is further increased by concentrating on a **judiciously selected subset** of possible FTR sink or source nodes given by the set $\mathcal{Z}$. The $\ell_0$ and $\ell_1$ norms are closely related; minimizing the $\ell_0$ norm of $a$ also **reduces** the $\ell_1$ norm of $a$. A **mixed integer linear programming (MILP)** solution approach is an **equally valid alternative** for the optimization problem (14).

Once $a$ is determined by minimizing $\|a\|_0$, the **transactions** $\Omega_u = \{m_u, n_u, a_u\}$ are identified for $u = 1, \ldots, U$ where $a_u \neq 0$. A **subset $\mathcal{Z}'$ of $\mathcal{Z}$** is constructed, containing **$K$ elements** ($K \leq U$), all of which have $a_u \neq 0$. These $K$ transactions satisfy the $V$ market participant specifications. Each transaction is associated with the **FTR** for the node pair $\{m_u, n_u\}$ in the amount $a_u$, where $u \in \mathcal{Z}'$. The **portfolio** $\mathcal{F} = \{\Gamma_1, \ldots, \Gamma_K\}$ is then constructed, where each element $k$ corresponds to an element in $\mathcal{Z}'$:

$$
\Gamma_k = \{m_k, n_k, a_k\}, \qquad k = 1, \ldots, K. \qquad (15)
$$

The determination of $\mathcal{Z}'$ and the quantities $a_u$, $u \in \mathcal{Z}'$, allows the identification of each $\Gamma_k$ selected for the FTR portfolio $\mathcal{F}$, provided **all the market participant's requirements are satisfied**. The construction is complete.

**Incorporating existing FTR impacts.** To take into account **existing FTR impacts**, we evaluate the **flows** that transactions having the **same node pairs and amounts** as those in the FTR portfolio induce on the constraints within the two subsets (specified and zero congestion participation). This evaluation requires the **detailed use of the appropriate PTDFs**. These flows **modify the specified levels of participation** for the constraints in the **specified congestion participation** and **zero congestion participation** subsets. The incorporation of existing FTRs necessitates the **modification of the limits** to explicitly consider the **impacts of the MW flows** associated with the existing FTR when specifying participation levels for the constraints in those two subsets.
