# Volatility and Volatility Surfaces in Energy Commodity Trading

A practical guide from a quant perspective: what vol and vol surfaces are, how we use them, and how they behave in **FTR**, **power**, and **gas** markets.

---

## 1. What is volatility?

**Volatility** ($\sigma$) measures the **uncertainty** or **variability** of a price (or return) over a horizon. In options and risk we care about:

- **Realized (historical) volatility:** The **observed** standard deviation of **returns** (e.g. log-returns) over a past window. Example: daily log-returns $r_t = \ln(S_t/S_{t-1})$; **realized vol** (annualized) = $\widehat{\sigma} = \sqrt{252} \cdot \text{std}(\{r_t\})$.
- **Implied volatility:** The **volatility** that, when plugged into a **pricing model** (e.g. Black-76), reproduces the **market price** of an option. So it is **market-implied** and reflects the option market’s view of future uncertainty (and supply/demand for optionality).

**Why it matters:** Option **value** and **vega** depend on $\sigma$; **VaR** and **risk** depend on the **distribution** of price/return, of which vol is a key parameter. In energy, **spot** and **forward** volatility differ; **vol** often varies by **season**, **tenor**, and **strike** — hence we need a **vol surface**, not a single number.

---

## 2. What is a volatility surface?

A **volatility surface** is the function $\sigma(K, T)$ — or $\sigma(\Delta, T)$ — that gives **volatility** for each **strike** $K$ (or **delta** $\Delta$) and **expiry** $T$. So we have:

- **Term structure of vol:** $\sigma(T)$ for a given strike (e.g. ATM). Vol can **increase** or **decrease** with time to expiry depending on market (e.g. power prompt often more volatile than deferred).
- **Smile / skew:** $\sigma(K)$ for a given expiry. **Smile** = vol higher for OTM puts and OTM calls than ATM; **skew** = vol higher for low strikes (OTM puts) than high strikes — common when **downside** or **spikes** are feared. In energy we often see **positive skew** (right tail: spikes) or **reverse skew** in some products.

**Conventions:**

- **Underlying:** Vol surface is **per underlying** (e.g. ERCOT North 5x16, Henry Hub gas month). Each **hub × block × expiry** can have its own surface (or we share a **relative** smile across underlyings).
- **Quote:** Vol is usually quoted in **absolute** terms (e.g. 40% = 0.40) as **lognormal** (Black) vol — i.e. the $\sigma$ in $dF/F = \mu\,dt + \sigma\,dW$ so that option price is $C = D(T)[F\Phi(d_1) - K\Phi(d_2)]$ with $d_1 = (\ln(F/K) + \frac{1}{2}\sigma^2 T)/(\sigma\sqrt{T})$.
- **Delta convention:** Surfaces are sometimes quoted in **delta** (e.g. 10Δ put, 25Δ put, ATM, 25Δ call, 10Δ call) instead of strike, especially when the **forward** moves a lot; delta is more stable for interpolation.

**Uses:** (1) **Mark** options at consistent vol; (2) **Vega** risk and hedging (vega by bucket); (3) **P&amp;L** explain (vega × Δσ); (4) **Risk** (VaR with vol as risk factor); (5) **New** option pricing (strike/expiry not liquid — read vol from surface).

---

## 3. Formulas (reference)

**Realized volatility (annualized)** from daily log-returns $r_t = \ln(P_t/P_{t-1})$:
$$
\widehat{\sigma}_{\mathrm{real}} = \sqrt{\frac{N_{\mathrm{yr}}}{N}} \sqrt{ \sum_{t=1}^N (r_t - \bar{r})^2 },
$$
where $N$ is the number of days and $N_{\mathrm{yr}}$ = 252 (or 365). For **forward** returns, use the forward price series for the **same** delivery period (e.g. rolling front-month).

**Implied volatility:** Solve for $\sigma_{\mathrm{impl}}$ in $C_{\mathrm{market}} = C_{\mathrm{Black}}(F, K, T, \sigma_{\mathrm{impl}})$ (e.g. by Newton or bisection). No closed form; numerical inversion.

**Black-76 (reminder):** $C = D(T)[F\Phi(d_1) - K\Phi(d_2)]$, $d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$. So **vega** (sensitivity to $\sigma$) drives how much option value moves when **implied vol** changes.

**Vol surface representation:** In practice we **interpolate** in $(K, T)$ or $(\Delta, T)$ — e.g. linear or cubic in strike, linear in variance $\sigma^2 T$ along term structure, or use a **parametric** model (e.g. SABR) so the surface is **smooth** and **arbitrage-free**.

---

## 4. Implied volatility and local volatility (by market)

### 4.1 Implied volatility (recap and context)

**Definition:** **Implied volatility** $\sigma_{\mathrm{impl}}(K, T)$ is the **volatility** that, when used in a **given** pricing model (e.g. Black-76), **matches** the **market price** of an option with strike $K$ and expiry $T$. So:
$$
C_{\mathrm{market}}(K, T) = C_{\mathrm{Black}}(F, K, T, \sigma_{\mathrm{impl}}(K, T)).
$$
We **invert** numerically (Newton, bisection). The set of $\sigma_{\mathrm{impl}}(K, T)$ across strikes and expiries is the **implied vol surface**; it encodes **all** liquid option prices in a single object.

**Interpretation:** Implied vol reflects (1) the market’s **expectation** of future volatility, (2) **supply/demand** for optionality (e.g. hedgers buying puts → put vol rich), and (3) **model** choice (Black vs something else). **Smile** means $\sigma_{\mathrm{impl}}$ varies with $K$; **term structure** means it varies with $T$.

### 4.2 Local volatility (recap and context)

**Definition:** A **local volatility** model assumes the **forward** (or spot) follows a **one-factor** diffusion with **deterministic** volatility that depends on **underlying level** and **time**:
$$
dF_t = \mu_t F_t\, dt + \sigma_{\mathrm{loc}}(F_t, t)\, F_t\, dW_t.
$$
**Dupire’s equation** (and the **Dupire formula**) shows that, under **no arbitrage**, there is a **unique** function $\sigma_{\mathrm{loc}}(K, T)$ that is **consistent** with the **entire** implied vol surface — i.e. all European option prices are matched. So **local vol** is **implied** from the **implied vol surface** (or from option prices directly). Formula (in forward space, zero drift for simplicity):
$$
\sigma_{\mathrm{loc}}^2(K, T) = \frac{ \frac{\partial C}{\partial T} }{ \frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2} },
$$
where $C = C(K, T)$ is the **market** (or model) call price. In practice we **bootstrap** local vol from the **calibrated** implied surface (or from a parametric smile model) so that **prices** and **Greeks** are consistent across strikes and expiries.

**Use:** **Exotics** and **path-dependent** options (e.g. barriers, Asians) can be priced with a **single** diffusion that **fits** the vanilla surface; **hedging** (delta, gamma) is **consistent** with the smile. **Limitation:** Local vol is **deterministic** in $(F, t)$ — it does **not** model **stochastic** vol; so **vol-of-vol** and **forward smile** behavior can be wrong for long-dated or vol-sensitive products. For that, **stochastic vol** (e.g. SABR, Heston) is used; local vol remains a **simple** and **transparent** way to use the smile in a single-factor diffusion.

---

### 4.3 Power market: implied vol and local vol

**Implied vol:**

- **Where it exists:** Options on **power forwards** (e.g. monthly peak, base, 5x16) trade **OTC** and, in some markets, **listed**. Where they are **liquid**, we have **market** option prices and can **invert** to get $\sigma_{\mathrm{impl}}(K, T)$ per **underlying** (hub × block × expiry).
- **Typical shape:** **Positive skew** (OTM calls richer than OTM puts) because of **spike** risk; **term structure** often **backwardated** (prompt vol > deferred). **Liquidity** is often **concentrated** in **ATM** and **near-term** months; **wings** and **long-dated** may be **broker-quoted** or **interpolated** from historical smile.
- **Use:** **Mark** power options (vanilla, caps, floors); **vega** risk and **vega** hedging; **P&amp;L** explain (vega × Δσ). **Same** surface (or consistent construction) for **trading** and **risk** so marks align.

**Local vol:**

- **Relevance:** If we have a **reasonably smooth** implied vol surface for a **power** underlying (e.g. ERCOT North 5x16), we can **derive** a **local vol** function $\sigma_{\mathrm{loc}}(F, t)$ via Dupire (or discrete analogue) so that **path-dependent** power options (e.g. **Asian**, **barrier**, or **American-style** daily) are priced **consistent** with the **vanilla** surface. That gives **consistent** delta and gamma across strikes.
- **Caveats:** Power **forwards** are **seasonal** and **mean-reverting** in reality; a **pure** local vol model (no mean reversion) is a **convention** for the **option’s** delivery period. **Stochastic vol** (e.g. SABR) is often used for **smile** interpolation and **vega** bucketing; **local vol** is then less central than in rates/equity, but still a valid **tool** for exotics when the desk wants a **single-factor** diffusion that fits the smile.
- **Summary:** **Implied vol** = main object for **marking** and **vega** in power where options trade. **Local vol** = optional **model** for **exotics** and **consistent** hedging when we want **one** diffusion that matches the implied surface.

---

### 4.4 Gas market: implied vol and local vol

**Implied vol:**

- **Where it exists:** Options on **gas forwards** (e.g. Henry Hub monthly, seasonal strips) trade **OTC** and **listed** (NYMEX, ICE). **Liquidity** is better at **Henry Hub** and **major** hubs; we can **invert** market option prices to get $\sigma_{\mathrm{impl}}(K, T)$ per **hub** and **product** (e.g. monthly, winter strip).
- **Typical shape:** **Smile** often **less pronounced** than in power; **term structure** **backwardated** (prompt > deferred); **seasonal** bumps (e.g. winter strip vol higher). **Spread** options (e.g. basis, spark) require **two** underlyings and **correlation** — we have **implied** vol (and correlation) **per** leg and **joint** for the spread.
- **Use:** **Mark** gas options (vanilla, caps, floors, swaptions); **vega** risk; **P&amp;L** explain. **Basis** or **spark** options: **two** implied vol surfaces (one per hub or per power/gas) plus **correlation**; no single “implied vol” for the spread, but **implied** parameters (vols + correlation) from **spread** option prices where they exist.

**Local vol:**

- **Relevance:** For **gas** forwards with a **liquid** option market and **smile**, we can **build** a **local vol** surface $\sigma_{\mathrm{loc}}(F, t)$ from the **implied** surface (Dupire) and use it to price **exotics** (e.g. **Asian**, **barrier**, **swing**-like structures) in a **consistent** way with vanillas.
- **Caveats:** Gas can have **mean reversion** and **seasonality**; local vol is still **deterministic** in $(F, t)$ and does **not** add **stochastic** vol. For **spread** options, **local vol** for **each** leg (or a **joint** local vol / correlation model) is used in **two-factor** pricing (e.g. Kirk + local vol, or MC with local vol drivers).
- **Summary:** **Implied vol** = standard for **gas** option marking and vega where options trade. **Local vol** = tool for **exotics** and **spread** exotics when we want **consistency** with the vanilla smile.

---

### 4.5 FTR market: implied vol and local vol

**Implied vol:**

- **Does not apply** in the **standard** sense. FTR payoff is the **path spread** (sink − source) over the CRR period; there are **no** traded **options on path spread** (no calls/puts on the spread). So there is **no** market option price to **invert** and **no** $\sigma_{\mathrm{impl}}(K, T)$.
- **What we use instead:** We work with the **distribution** of the **path spread** (or **constraint shadow**): **historical** or **model-based** **variance** (vol), **percentiles**, and **correlation** across paths. For **MtM** and **VaR** we need **vol** or **volatility structure** of the **spread** (e.g. conditional on binding), not “implied” from options.
- **If options on FTR ever existed:** In a hypothetical market with options on **path spread** (e.g. call on spread), we could define **implied vol** for that underlying (spread); it would be **per path** (and per period), not per strike in the same way as power/gas, because the “underlying” is already a **spread**. Today we simply **don’t** have that product, so **no** implied vol for FTR.

**Local vol:**

- **Does not apply** in the **standard** sense. **Local vol** is defined in the context of a **diffusion** for a **single** underlying whose **option** prices (and thus **implied** surface) are observed. For FTR we have **no** option surface; the “underlying” (path spread) has a **mixed** distribution (zero-inflated, non-normal) and is **not** naturally modeled as a **single** lognormal diffusion with a deterministic $\sigma(F, t)$.
- **Conceptual analogue:** In **modeling** the **path spread** (e.g. for VaR or scenario generation), we might use a **state-dependent** or **regime-dependent** vol: e.g. **vol = 0** when the constraint does not bind (spread fixed at 0), and **vol = σ_b** (or a function of level) when it **does** bind. That is **analogous** to “vol depends on state,” but it is **not** local vol in the Dupire sense — there is **no** implied surface to fit. It is simply **vol** (or **variance**) of the **spread** **conditional** on the **binding** regime.
- **Summary:** **No** implied vol and **no** local vol for FTR in the **option-market** sense. We use **distribution** and **correlation** of path spread (or constraint shadow); any “vol” is **realized** or **model-implied** from our **process** (e.g. mixture, regime), not **option-implied**.

---

## 5. Sticky delta, sticky strike, and sticky tree

When the **underlying** (spot or forward) **moves**, the **volatility surface** we use for **revaluation** and **risk** can be updated in different ways. The three main **conventions** are **sticky strike**, **sticky delta**, and **sticky tree**. They answer: *"After a move in $F$ (or $S$), what implied vol do we use for a given option?"*

### 5.1 Sticky strike

**Definition:** The **implied vol** for each **strike** $K$ (and expiry $T$) is **unchanged** when the underlying moves. So $\sigma_{\mathrm{impl}}(K, T)$ is **fixed** in **strike space** — the surface is "stuck" to strikes.

**Mechanics:** If the forward moves from $F_0$ to $F_1$, we still use $\sigma_{\mathrm{impl}}(K, T)$ for an option with strike $K$. The **same strike** keeps the **same vol**; the **delta** of that option changes (because $F$ changed).

**Used for:**

- **Scenario P&amp;L** and **stress tests**: "If forward moves by $X$, what is option P&amp;L?" assuming vol surface does not shift in strike space.
- **Vega hedging** when the desk assumes smile is **strike-anchored** (e.g. certain listed options quoted by strike).
- **Simple** risk reports and **VaR** where we don't model smile dynamics.

**Pros:**

- **Simple**: no need to rebuild or shift the surface after each move.
- **Stable** in $(K, T)$: easy to interpolate and store; same vol for same contract (same $K$).
- **Familiar** in markets where options are **strike-quoted** (e.g. some equity/index and commodity options).

**Cons:**

- In **delta space** the smile **moves** with spot: the same **delta** (e.g. 25Δ put) will have a **different** implied vol before and after the move, because the strike that gives 25Δ has changed. So **delta-based** hedging or **delta-quoted** markets can be **inconsistent** with sticky strike.
- **Understates** vega and **smile** revaluation when the market actually trades **sticky delta** (e.g. FX): after a move, market vols are re-anchored by delta, so our "sticky strike" P&amp;L can be wrong.

---

### 5.2 Sticky delta

**Definition:** The **implied vol** for each **delta** $\Delta$ (and expiry $T$) is **unchanged** when the underlying moves. So $\sigma_{\mathrm{impl}}(\Delta, T)$ is **fixed** in **delta space** — the surface is "stuck" to deltas (e.g. 10Δ put, 25Δ put, ATM, 25Δ call, 10Δ call).

**Mechanics:** If the forward moves from $F_0$ to $F_1$, we keep the **same vol** for, say, the **25Δ put**. That 25Δ put **strike** is **different** at $F_1$ than at $F_0$ (strike "slides" with $F$ so that delta stays 25Δ). So in **strike space** the smile **moves** with the underlying; in **delta space** it is **fixed**.

**Used for:**

- **FX** and **rates** where options are **quoted by delta** (e.g. 25Δ risk reversals, strangles). Revaluation after a spot move: same vol per delta, new strike per delta.
- **Commodity** desks that **quote** or **hedge** in delta (e.g. "vega per 25Δ put").
- **Scenario** and **stress** when we believe the **market** will keep the smile **fixed in delta** (e.g. after a large move, market re-quotes by delta, not by strike).

**Pros:**

- **Consistent** with **delta-quoted** markets: vega by delta bucket is stable; no spurious "smile move" when only spot moved.
- **Better** for **cross-market** comparison (e.g. 25Δ put vol across underlyings) and for **hedging** in delta space.
- Often **closer** to **observed** behavior in liquid delta-markets (FX): after a spot move, dealers re-anchor by delta.

**Cons:**

- **Strike space** is **unstable**: the same **strike** $K$ has a **different** implied vol before and after the move (because its delta changed). So strike-based reports or strike-quoted books need a **conversion** (delta → strike at new $F$) to get vol.
- **Implementation**: we must **invert** delta to strike at the **current** forward for each revaluation; slightly more work than sticky strike.

---

### 5.3 Sticky tree (sticky local vol)

**Definition:** The **local volatility** function $\sigma_{\mathrm{loc}}(S, t)$ (or $\sigma_{\mathrm{loc}}(F, t)$) is **fixed**. When the underlying **moves**, we are at a **different point** on the **same** local vol surface; **implied** vol for a given **strike** $K$ (and expiry $T$) **changes** because the **path distribution** and the **option's effective** volatility exposure change. So the **implied vol surface** in $(K, T)$ **moves** in a **model-consistent** way implied by the **fixed** local vol.

**Mechanics:** Local vol model: $dF = \mu F\,dt + \sigma_{\mathrm{loc}}(F,t)\,F\,dW$. After $F$ moves from $F_0$ to $F_1$, we still use the **same** $\sigma_{\mathrm{loc}}(F,t)$. So the **tree** (or PDE grid) is "sticky" — same local vol at each $(F,t)$. Implied vol $\sigma_{\mathrm{impl}}(K,T)$ is **recomputed** from the **model** at the new spot; it will generally **differ** from the old $\sigma_{\mathrm{impl}}(K,T)$ because the **conditional** distribution of $F_T$ given $F_{\mathrm{now}} = F_1$ is different from that given $F_0$.

**Used for:**

- **Exotics** and **path-dependent** options priced with a **local vol** model: revaluation after spot move is **consistent** with the same model (no ad hoc "sticky" rule for implied vol).
- **Consistent** delta and gamma from the **same** diffusion; **hedging** assumes the **local vol** dynamics are correct.
- **Theoretical** benchmark: "What does the **Dupire** model say after a move?" — sticky tree is the **native** behavior of that model.

**Pros:**

- **Internally consistent**: one **single** model (local vol) for **pricing** and **scenario**; no mix of "sticky strike" vs "sticky delta."
- **Arbitrage-free** by construction (local vol is derived from / consistent with the implied surface at calibration time).
- **Smooth** behavior of **implied** vol as spot moves (no jump in vol just because we switched convention).

**Cons:**

- **Assumes** local vol is the "true" dynamics — in reality **stochastic vol** or **jumps** may matter; then sticky tree can **misstate** revaluation.
- **Not** a direct **market** convention: traders often think in **sticky strike** or **sticky delta**; risk systems may use one of those for **reporting** and **limits**, so we need to **align** or **explain** the difference.
- **Computation**: we need the **local vol** surface and **reprice** options (or recompute implied vol) at the new spot; heavier than just "keep σ(K,T) fixed."

---

### 5.4 Summary: when to use which (energy context)

| Convention    | Typical use | Energy / power / gas note |
|-------------|-------------|----------------------------|
| **Sticky strike**  | Strike-quoted options; simple P&amp;L explain; VaR with fixed surface. | Common for **power** and **gas** when options are **strike-quoted** (e.g. listed monthly options). Easy for **mark** and **risk** if we store $\sigma(K,T)$. |
| **Sticky delta**   | Delta-quoted markets; vega by delta; scenario when market re-anchors by delta. | Used when the desk **quotes** or **hedges** in **delta** (e.g. 25Δ put vol); more relevant if **broker** quotes are **delta-based**. |
| **Sticky tree**    | Exotics and path-dependent options; consistent revaluation under local vol. | For **power/gas** **exotics** (Asian, barrier, swing) priced with **local vol**: revaluation and **scenario** use **sticky tree** so that **Greeks** and **P&amp;L** are consistent with the model. |

**Practical note:** Many **energy** option books are **strike-quoted**; **sticky strike** is often the **default** for **vanilla** marking and **stress**. For **exotics** on the same underlying, **sticky tree** (same local vol model) keeps **pricing** and **hedging** consistent. **Sticky delta** is used when the **trading** or **risk** convention is **delta-based** (e.g. vega bucketing by delta).

---

## 6. Characteristics: Power market

### 6.1 Underlyings and liquidity

- **Spot:** Hourly or block (peak, off-peak) LMP. **No** traded spot options in many markets; **realized** vol is from **historical** LMP (or hub index). Used for **physical** optionality, **storage**, and **risk**.
- **Forwards:** Monthly or quarterly **base**, **peak**, **off-peak** (e.g. 5x16, 7x16). **Options** (calls, puts, caps, floors) are mostly **OTC**; some **listed** (e.g. CME, ICE). **Liquidity** is often **concentrated** in **near-term** months and **ATM**; **smile** and **term structure** may be **broker-quoted** or **historical**.

### 6.2 Vol characteristics (power)

| Feature | Description |
|--------|-------------|
| **Level** | **Spot** vol is **high** (e.g. 50–150%+ annualized) and **state-dependent**: higher when **price** is high (spikes). **Forward** vol is typically **lower** (e.g. 30–80%) and more stable. |
| **Term structure** | **Short-dated** (prompt month, next month) often **higher** vol than **deferred** (next quarter, next year) — **backwardation in vol**. Exception: **seasonal** peaks (e.g. summer strip) can have **higher** vol as expiry approaches because of **weather** and **load** uncertainty. |
| **Seasonality** | **Summer** and **winter** strips can have **higher** vol than **shoulder** (spring, fall). **Peak** blocks often **more** volatile than **off-peak** (demand and congestion more variable in peak). |
| **Smile / skew** | **Positive skew** is common: **OTM calls** (high strike) trade **richer** vol than **OTM puts** (low strike) because of **spike** risk (right tail). So vol **increases** with **strike** (call skew). In some hubs or blocks the smile is **flat** or **reverse** (e.g. when caps or regulatory limits cap upside). |
| **Spikes and jumps** | **Realized** distribution has **fat tails** and **positive skew**; **implied** vol (when options exist) often **elevated** for **OTM calls**. **Jump** or **regime** models are used to capture **spike** risk; **single** lognormal vol **understates** tail risk. |

### 6.3 Vol surface (power): practical notes

- **Build:** Use **broker** runs or **historical** vol per expiry; **interpolate** in strike (or delta) and term. **ATM** vol per month is the **anchor**; **smile** can be **relative** (e.g. 10Δ put = ATM + 2%, 25Δ call = ATM + 4%) from history or broker.
- **Conventions:** One surface **per hub × block** (e.g. ERCOT North 5x16); or **one** surface with **adjustments** by block (e.g. peak vol = base × 1.2). **Settlement** (e.g. average price vs final price) affects **option** definition and thus **implied** vol.
- **Limitations:** **Thin** option liquidity → **wide** bid–ask on vol; **historical** vol may **lag** regime change (e.g. more renewables, new congestion). **Stress** vol (e.g. +20%) for **risk** and **capital**.

---

## 7. Characteristics: Gas market

### 7.1 Underlyings and liquidity

- **Spot:** Daily or within-day hub price (e.g. Henry Hub, regional hubs). **Forward:** Monthly, seasonal (winter, summer), calendar strips. **Options** (calls, puts, caps, floors, swaptions) trade **OTC** and **listed** (e.g. NYMEX, ICE). **Liquidity** is better at **Henry Hub** and **key** hubs; **smile** and **term structure** are **quoted** or **implied** where options exist.

### 7.2 Vol characteristics (gas)

| Feature | Description |
|--------|-------------|
| **Level** | **Spot** vol is **moderate to high** (e.g. 40–100% annualized); **cold snaps** and **supply** events cause **spikes**. **Forward** vol is typically **lower** than spot and **decreases** with **tenor** (term structure). |
| **Term structure** | **Backwardation in vol** common: **prompt** vol > **deferred**. **Winter** strip vol can **rise** as expiry approaches (**weather** uncertainty). **Long-dated** (e.g. Cal strip) often **lower** and **flatter** term structure. |
| **Seasonality** | **Winter** months (heating demand) and **shoulder** (storage refill) can have **higher** vol than **summer** (except heat-driven demand). **Storage** dynamics (inject/withdraw) add **seasonal** pattern to **prompt** vol. |
| **Smile / skew** | **Positive skew** (OTM calls richer) when **spike** risk is priced; **negative skew** in some periods (e.g. supply glut, downside fear). **Smile** is often **less pronounced** than in **power** (gas less spikey). **Basis** options (spread options) have **joint** vol and **correlation**; no single “vol surface” — we need **two** underlyings and **correlation**. |
| **Basis** | **Basis** (hub A − hub B) has its **own** volatility (and often **mean reversion**). **Basis** vol can be **higher** than **absolute** hub vol when **locations** decouple (pipeline, weather). |

### 7.3 Vol surface (gas): practical notes

- **Build:** **Henry Hub** and **major** hubs have **broker** or **exchange** vol; **term structure** (ATM vol by month/season) and **smile** (by delta or strike). **Correlation** between hubs (and between gas and power) for **spread** options.
- **Conventions:** Surface **per hub** (and per **product** if winter/summer strips differ). **Settlement** (e.g. monthly average, daily) affects **option** definition and **implied** vol.
- **Limitations:** **Illiquid** strikes or tenors → **extrapolate** from ATM and **historical** smile; **correlation** for spread options is **unstable** and **regime-dependent**.

---

## 8. Characteristics: FTR market

### 8.1 What “volatility” means for FTR

FTR **payoff** is the **path spread** (sink − source price) over the CRR period. There are **no** traded **options on path spread** in most markets, so there is **no** “implied vol surface” in the option sense. “Volatility” for FTR means:

- **Volatility of path spread** (or of **constraint shadow price**): the **standard deviation** (or **distribution**) of the **realized** or **simulated** spread over the settlement period (or of daily/monthly spread changes for MtM/VaR).
- **Zero-inflation:** Path spread is **zero** when constraints **don’t bind** and **non-zero** (positive or negative) when they do. So the **unconditional** distribution is **mixed** (mass at zero + continuous part). “Vol” is often quoted **conditional on binding** or as **variance of the full** distribution (including zeros).
- **Correlation:** **Correlation** across **paths** (or across **constraint** shadow prices) is central to **portfolio** risk and **VaR**; more important than a single “vol” number.

### 8.2 Vol characteristics (FTR)

| Feature | Description |
|--------|-------------|
| **Level** | **Conditional** vol (when spread ≠ 0) can be **high** (shadow prices and spreads are **spiky** when constraints bind). **Unconditional** vol (including zero) depends on **binding frequency** and **conditional** variance. |
| **Distribution** | **Non-normal**: **zero-inflated**, **positive or negative** skew depending on path direction; **fat tails** when binding (large shadows). **No** lognormal assumption; we use **historical** or **simulated** distribution (and possibly **mixture** / **regime** models). |
| **Term structure** | “Term” here is **time to end of CRR period**. **Variance** of path spread often **decreases** as we get **closer** to settlement (fewer intervals left; more information). For **MtM** and **VaR** we need **vol** or **distribution** by **remaining** tenor. |
| **Seasonality** | **Binding** frequency and **shadow** magnitude vary by **season** (summer/winter congestion). So **vol** of path spread is **seasonal** (e.g. higher in peak months). |
| **Correlation** | **Paths** that share **constraints** have **correlated** payoffs. **Correlation matrix** of path spreads (or of constraint shadows) is needed for **portfolio** VaR and **diversification**. |
| **No smile** | There is **no** strike or delta for FTR payoff; **no** vol smile. We work with **full distribution** (or **scenarios**) and **percentiles** (e.g. 5th, 95th) for risk. |

### 8.3 “Surface” for FTR: what we use instead

- **Path-level:** For each **path** (and optionally **month**), we need **distribution** of path spread: e.g. **mean**, **variance** (or **vol**), **percentiles**, **probability of zero** (no binding). From **historical** realizations, **PCM** scenarios, or **MC** (outage + shadow model).
- **Constraint-level:** **Distribution** of **constraint shadow price** (or **binding** frequency and **conditional** shadow distribution). Then **path** distribution = PTDF-weighted combination of constraint distributions (with **correlation**).
- **Correlation:** **Correlation matrix** of path spreads (or constraint shadows) by **period** (e.g. by month or by remaining tenor). Used for **portfolio** VaR and **stress** (e.g. many paths go wrong together).
- **No implied vol:** We do **not** have a $\sigma(K, T)$ surface; we have **historical** or **model-based** **vol** (or **variance**) and **distribution** per path/constraint and **correlation** across them.

---

## 9. Summary table: vol and “surface” by market

| Market | Underlying | Vol type | Term structure | Smile / skew | “Surface” / main object |
|--------|------------|----------|-----------------|--------------|--------------------------|
| **Power** | Spot, forwards (hub × block × expiry) | Realized (spot); implied (forwards where options exist) | Often backwardation (prompt > deferred); seasonal | Positive skew (spikes); OTM calls rich | $\sigma(K, T)$ or $\sigma(\Delta, T)$ per hub×block; ATM + relative smile |
| **Gas** | Spot, forwards (hub × month/strip) | Realized; implied where options exist | Backwardation; winter/storage seasonality | Positive or negative; less pronounced than power | $\sigma(K, T)$ per hub; correlation for basis/spread options |
| **FTR** | Path spread, constraint shadow | Realized or model-based; **no** implied (no options) | Vol/variance by remaining tenor; seasonal binding | N/A (no strike) | Distribution (and correlation) per path/constraint; no $\sigma(K,T)$ |

---

## 10. One-page recap

- **Volatility** = uncertainty in price/return; **realized** (historical) vs **implied** (from options). **Vol surface** = $\sigma(K, T)$ or $\sigma(\Delta, T)$ for **option** pricing and **vega** risk.
- **Power:** High **spot** vol, **state-dependent**; **forward** vol lower; **backwardation** in vol term structure; **positive skew** (spike risk). Surface **per hub × block**; ATM + smile from broker or history.
- **Gas:** **Moderate** vol; **seasonal** (winter, storage); **backwardation** in vol; **smile** less pronounced; **basis** vol and **correlation** for spread options.
- **FTR:** No **option** market → no **implied** vol surface. “Vol” = **distribution** of **path spread** (or **constraint shadow**): **zero-inflated**, **fat-tailed**, **seasonal**; **correlation** across paths is key. We use **historical** or **model** distribution and **correlation matrix**, not $\sigma(K, T)$.
