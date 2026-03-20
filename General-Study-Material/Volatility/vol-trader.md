# Volatility Trader: Daily Work, Analysis, Methodologies, and What to Expect from an Analyst

A practical guide from the perspective of a **seasoned volatility trader** in energy (power, gas) options: what I do **daily**, what **analysis** I run, **methodologies** I use (with **pros**, **cons**, **assumptions**, **formulas**), and what I **expect from an analyst**.

---

## 1. Who is a vol trader and what we do

A **volatility trader** runs a **book** of **options** (and related vol exposure) and is responsible for **marking** options at a **consistent** vol surface, **managing** **vega** (and related Greeks), and **trading** **vol** — i.e. taking view on whether **implied vol** is **rich** or **cheap** vs **realized** or vs **relative** value across strikes, tenors, or underlyings. We care about **level** (ATM vol), **smile** (skew), **term structure**, and **vega** P&amp;L. In energy, options are mostly **OTC** (power, gas) and some **listed**; **liquidity** is often **ATM** and **near-term**, so **wings** and **long-dated** require **interpolation** and **judgment**.

---

## 2. Daily routine

| Time / phase | What I do |
|--------------|-----------|
| **Pre-open / morning** | **Check** overnight **broker** runs and **exchange** settles (if any). **Refresh** **forward curve** and **vol surface** (inputs from curve team / analyst). **Run** **mark** and **Greeks** (delta, gamma, vega, theta, vanna, volga by bucket). **Review** **P&amp;L** vs prior day (actual vs explain). **Check** **limits** (delta, vega, gamma, stress). |
| **Surface and risk** | **Update** vol surface if **new** broker quotes or **trades**; **publish** or **align** with risk so **mark** is consistent. **Vega** by **expiry** (and optionally by strike/delta bucket); **identify** **long** vs **short** vega and **concentration**. **Scenario**: where does book **lose** if vol moves (up/down) or curve moves? |
| **Trading** | **Quote** and **trade** options (buy/sell vol, spread vol across strikes or tenors). **Hedge** **delta** with **forwards**; **vega** with **offsetting** options or **adjust** delta when we trade options. **Rehedge** when **delta** or **vega** drifts beyond threshold. **Communicate** with **brokers** and **counterparties** on **levels** and **smile**. |
| **Midday / ad hoc** | **Respond** to **requests** (quotes, risk explain, new deal approval). **Monitor** **curve** and **vol** moves; **explain** **P&amp;L** (curve, vol, theta, residual). |
| **End of day** | **Final** **mark** and **Greeks**; **reconcile** to **risk** and **finance**. **P&amp;L** explain: **delta** (curve), **vega** (vol), **theta** (time), **residual**. **Escalate** if **limit** breach or **large** residual. **Hand off** to **after-hours** or **next** day. |

---

## 3. Analysis I do (and methodologies)

### 3.1 Realized vs implied (rich/cheap)

**Idea:** Compare **realized** volatility (historical) to **implied** volatility (from option prices). If **implied** > **realized**, vol is **rich** (sell optionality); if **implied** < **realized**, vol is **cheap** (buy optionality).

**Realized vol (annualized)** from daily log-returns $r_t = \ln(F_t/F_{t-1})$ over $N$ days:
$$
\widehat{\sigma}_{\mathrm{real}} = \sqrt{\frac{N_{\mathrm{yr}}}{N}} \sqrt{ \sum_{t=1}^N (r_t - \bar{r})^2 }, \qquad N_{\mathrm{yr}} = 252.
$$
Use **same** underlying and **tenor** as the option (e.g. rolling front-month forward). **Implied** = $\sigma_{\mathrm{impl}}(K, T)$ from **market** option price (invert Black-76).

**Methodology:** Choose **lookback** $N$ (e.g. 20d, 60d, 1y); compute **realized**; compare to **ATM** implied for **matching** expiry. **Term structure**: compare **realized** over **horizon** $T$ to **implied** $\sigma_{\mathrm{impl}}(T)$.

**Pros:** **Simple**; **objective** (realized is observable). **Cons:** **Backward-looking**; **option** is on **forward** over **future** period, so **future** realized ≠ **past** realized; **liquidity** and **supply/demand** can keep implied **rich** or **cheap** for long. **Assumption:** Past realized is **informative** about future realized (often **not** fully true in energy).

---

### 3.2 Term structure (front vs back)

**Idea:** **Prompt** (short-dated) vol vs **deferred** (long-dated) vol. In energy we often see **backwardation** (prompt > deferred) or **contango** (deferred > prompt). **Trade:** Buy **back** vol, sell **front** vol (or the reverse) if we have a view.

**Methodology:** Plot $\sigma_{\mathrm{impl}}(T)$ for **ATM** (or 25Δ) across **expiries**; compare to **historical** term structure. **Relative** value: is **summer** vol rich vs **winter** (or vs **balance-of-year**)?

**Formula:** No single formula; **interpolation** (e.g. linear in **variance** $\sigma^2 T$) for smooth term structure. **Vega** bucketing: vega **per expiry** so we see **term** exposure.

**Pros:** **Visual**; **relative** value across tenors. **Cons:** **Liquidity** in **back** months often **thin** → **quotes** can be **stale** or **wide**; **structural** changes (new capacity, demand) can **shift** term structure. **Assumption:** Term structure is **stable** enough to trade (can break in stress).

---

### 3.3 Smile and skew (wings vs ATM)

**Idea:** **Smile** = vol as function of **strike** (or **delta**). **Skew** = asymmetry (e.g. OTM put vol > OTM call vol = **put skew**). In **power/gas** we often see **positive** skew (OTM **calls** richer) for **spike** risk. **Trade:** Sell **wing** (rich) vs buy **ATM** (cheap) — **skew** trade; or **calendar** + **strike** (e.g. sell front ATM, buy back 25Δ call).

**Methodology:** **Interpolate** vol in **strike** (linear or cubic) or **delta**; use **parametric** (e.g. **SABR**) for **smooth** smile and **arbitrage-free** surface. **Vanna** and **volga** tell us how **mark** moves when **curve** and **vol** move together (vanna) or when **vol** moves a lot (volga).

**Formula (Black-76):** $C = D(T)[F\Phi(d_1) - K\Phi(d_2)]$, $d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$. **Implied** vol = $\sigma$ that solves $C_{\mathrm{market}} = C_{\mathrm{Black}}(F,K,T,\sigma)$ (Newton or bisection). **Vega** = $\frac{\partial C}{\partial \sigma} = D(T)\, F\,\phi(d_1)\,\sqrt{T}$ (per 1% move in $\sigma$: multiply by 0.01).

**Pros:** **Rich/cheap** by strike; **hedging** (vega by bucket). **Cons:** **Wings** often **illiquid** → **smile** is **interpolated** or **extrapolated**; **model** (SABR, etc.) has **parameters** that can **overfit**. **Assumption:** Smile **shape** is **stable** or **predictable** (can move in stress).

---

### 3.4 Vega bucketing and revaluation

**Idea:** **Vega** is not one number — we have **vega** per **expiry** (and per **strike** if we bucket that). **Surface move** (e.g. short-dated vol +5%, long-dated flat) → **bucket** P&amp;L. **Methodology:** **Vega** by **expiry** (and optionally by **delta** bucket); **revalue** book under **vol bump** per bucket (e.g. +1% for expiry $T_i$ only) to get **vega** $T_i$. **Report** **net** vega per bucket; **limit** by bucket or **total**.

**Formula:** $\mathrm{Vega}_{T_i} \approx \frac{V(\sigma_{T_i} + \epsilon) - V(\sigma_{T_i})}{\epsilon}$ (bump **only** vol at expiry $T_i$). **P&amp;L** from vol move: $\Delta V \approx \sum_i \mathrm{Vega}_{T_i} \cdot \Delta\sigma_{T_i}$ (first order).

**Pros:** **Granular** risk; **hedge** vega **where** it matters. **Cons:** **Correlation** across tenors (parallel move) not captured by **bucket** sum; **volga** and **vanna** require **second-order** or **full reval**. **Assumption:** **Small** vol moves (first order sufficient); **bump** size $\epsilon$ is **consistent** (e.g. 1% absolute).

---

### 3.5 Sticky strike vs sticky delta (scenario P&amp;L)

**Idea:** When **forward** $F$ moves, **how** does the **vol surface** move? **Sticky strike**: $\sigma_{\mathrm{impl}}(K,T)$ **unchanged** → same strike, same vol. **Sticky delta**: $\sigma_{\mathrm{impl}}(\Delta,T)$ **unchanged** → strike **slides** with $F$ so delta is constant. **Scenario** P&amp;L: revalue book under **$F$ move** with **chosen** convention (sticky strike or sticky delta).

**Methodology:** **Default** for many energy books is **sticky strike** (simple). If **market** trades **sticky delta** (e.g. broker re-quotes by delta), use **sticky delta** for **scenario** and **hedge** logic. **Compare** P&amp;L under both to see **sensitivity** to **convention**.

**Formula:** Under **sticky strike**, no change to $\sigma(K,T)$. Under **sticky delta**, at new $F$ we have **new** $K$ for each delta: $K_{\mathrm{new}} = K(\Delta, F_{\mathrm{new}})$ from Black-76 delta formula; then $\sigma_{\mathrm{impl}}(K_{\mathrm{new}}, T)$ = same as old $\sigma_{\mathrm{impl}}(\Delta, T)$.

**Pros:** **Explicit** assumption; **consistent** with **market** convention if chosen well. **Cons:** **Market** may not follow either **perfectly**; **vanna** (cross term $\Delta F \cdot \Delta\sigma$) can be **large** when both move. **Assumption:** Surface move is **described** by one of these (reality can be **mixed**).

---

### 3.6 P&amp;L explain (Taylor)

**Idea:** Decompose **daily** P&amp;L into **curve** (delta), **vol** (vega), **time** (theta), and **residual**. **Second-order**: **gamma** $(\Delta F)^2$, **volga** $(\Delta\sigma)^2$, **vanna** $\Delta F \Delta\sigma$.

**Formula:**
$$
\Delta V \approx \Delta\,\Delta F + \mathrm{Vega}\,\Delta\sigma + \Theta\,\Delta t + \frac{1}{2}\Gamma\,(\Delta F)^2 + \frac{1}{2}\mathrm{Volga}\,(\Delta\sigma)^2 + \mathrm{Vanna}\,\Delta F\,\Delta\sigma.
$$
**Residual** = actual P&amp;L − Taylor estimate. **Large** residual → **wrong** curve/vol, **model** issue, or **large** higher-order move.

**Methodology:** **Daily** run with **prior** day **close** curve/vol vs **current**; **attribute** to **delta**, **vega**, **theta**; **report** **residual**. **Investigate** if residual > threshold.

**Pros:** **Transparent**; **catches** input or model errors. **Cons:** **Local** (Taylor); **discrete** rehedge and **path** dependence leave **residual** even with correct inputs. **Assumption:** **Smooth** value function; **Greeks** from **same** model as **mark**.

---

## 4. Methodologies: summary table (pros, cons, assumptions)

| Methodology | What it is | Pros | Cons | Main assumption |
|-------------|------------|------|------|------------------|
| **Realized vs implied** | Compare **historical** vol to **implied** (rich/cheap). | Simple; objective. | Backward-looking; future ≠ past. | Past realized informative for future. |
| **Term structure** | **Front** vs **back** vol; relative value by **expiry**. | Visual; relative value. | Back months illiquid; structure can shift. | Term structure stable enough to trade. |
| **Smile / skew** | **Vol** by **strike** (delta); **interpolation** (SABR, cubic). | Rich/cheap by strike; vega by bucket. | Wings illiquid; model overfit. | Smile shape stable or parametric. |
| **Vega bucketing** | **Vega** per **expiry** (and strike); **bump** and reval. | Granular risk; hedge where it matters. | Ignores correlation; need volga/vanna for large moves. | First-order vol move sufficient. |
| **Sticky strike / delta** | **Scenario** reval: surface **fixed** in strike or delta. | Explicit; consistent. | Market may not follow; vanna in reality. | Surface move follows one convention. |
| **P&amp;L explain (Taylor)** | **Delta** + **vega** + **theta** + **gamma** + **volga** + **vanna**. | Transparent; catches errors. | Local; residual from path/discrete hedge. | Smooth value; correct Greeks. |

---

## 5. Formulas (reference)

**Realized vol (annualized):**
$$
\widehat{\sigma}_{\mathrm{real}} = \sqrt{\frac{252}{N}} \sqrt{ \sum_{t=1}^N (r_t - \bar{r})^2 }, \quad r_t = \ln(F_t/F_{t-1}).
$$

**Implied vol:** Solve $C_{\mathrm{market}} = C_{\mathrm{Black}}(F, K, T, \sigma_{\mathrm{impl}})$ numerically.

**Black-76 call:** $C = D(T)[F\Phi(d_1) - K\Phi(d_2)]$, $d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$.

**Vega (Black-76):** $\mathrm{Vega} = D(T)\, F\, \phi(d_1)\, \sqrt{T}$ (per unit move in $\sigma$; per 1% use $\times 0.01$).

**P&amp;L explain (Taylor):**
$$
\Delta V \approx \Delta\,\Delta F + \mathrm{Vega}\,\Delta\sigma + \Theta\,\Delta t + \frac{1}{2}\Gamma\,(\Delta F)^2 + \frac{1}{2}\mathrm{Volga}\,(\Delta\sigma)^2 + \mathrm{Vanna}\,\Delta F\,\Delta\sigma.
$$

**Vega by bucket:** $\mathrm{Vega}_{T_i} = \partial V / \partial \sigma_{T_i}$ (bump vol at expiry $T_i$, revalue, difference).

---

## 6. What I expect from an analyst

An **analyst** (quant or strats) supports the **vol** desk with **data**, **tools**, **analysis**, and **consistency**. Below is what I expect so I can **trade**, **mark**, and **explain** risk without reinventing the wheel.

### 6.1 Surface build and maintenance

- **Build** and **maintain** the **vol surface** (and **curve**) used for **mark** and **Greeks**: **inputs** (broker runs, trades, historical), **interpolation** (strike/delta, term structure), **smoothness** and **arbitrage** checks. **Publish** surface (or feed to risk system) so **trading** and **risk** use the **same** vol.
- **Document** **method** (e.g. SABR per expiry, linear in variance along term structure) and **fallbacks** (e.g. no quote → historical or relative). So when **residual** is large or **dispute** with counterparty, we can **trace** the number.

**Deliverable:** **Daily** (or intraday) surface; **audit trail** of inputs and parameters.

---

### 6.2 Realized vol and rich/cheap reports

- **Compute** **realized** vol for **relevant** underlyings and **windows** (e.g. 20d, 60d, 1y) and **compare** to **ATM** implied for **matching** expiry. **Report** (e.g. table or dashboard): underlying, expiry, realized, implied, **ratio** or **spread** (implied − realized). **Update** **daily** or weekly.
- **Optionally**: **Term structure** of realized (e.g. 1m realized vs 2m vs 3m) vs **implied** term structure. So I can see **where** vol is **rich** or **cheap** by **tenor**.

**Deliverable:** **Realized vs implied** report (and history) so I can **prioritize** where to trade vol.

---

### 6.3 Greeks and risk reports

- **Vega** by **expiry** (and by **strike/delta** bucket if we use it); **delta** by **tenor** (and by underlying); **gamma**, **theta**, **vanna**, **volga** where **material**. **Limit** monitoring: **flag** when we are **close** to or **breach** limit.
- **Scenario** and **stress**: **Revalue** book under **curve** move (e.g. ±$5) and **vol** move (e.g. ±5%); **sticky strike** vs **sticky delta** if we track both. **Stress** scenario (e.g. **spike** or **crash**) with **defined** move; **report** P&amp;L and **escalate** if over **stress** limit.

**Deliverable:** **Daily** Greeks and **scenario** output; **automated** limit check and **alert**.

---

### 6.4 P&amp;L explain and residual

- **Daily** **P&amp;L** explain: **delta** (curve), **vega** (vol), **theta** (time), **gamma**, **volga**, **vanna**, **residual**. **Break** by **book** or **underlying** if needed. **Investigate** **large** residual (e.g. wrong curve, wrong vol, missing trade, model bug) and **document** or **fix**.
- **Backtest**: Compare **realized** P&amp;L to **expected** (e.g. delta × curve move) over time; **improve** **hedge** and **model** from **residual** analysis.

**Deliverable:** **P&amp;L** explain **report**; **residual** commentary when large; **periodic** backtest summary.

---

### 6.5 New products and model support

- **New** option type (e.g. new payoff, new underlying): **spec** **pricing** model (Black, Asian, Kirk, MC), **inputs** (curve, vol, correlation), **Greeks**. **Test** and **document**; **parallel** run with risk if needed. So we can **trade** and **mark** from **day one**.
- **Model** change (e.g. switch **interpolation** from linear to SABR): **impact** on **existing** book (mark, Greeks); **comparison** report; **sign-off** with risk before **go-live**.

**Deliverable:** **Model** doc and **test** results; **impact** analysis for **model** changes.

---

### 6.6 Data and automation

- **Reliable** **data** feed: **broker** runs, **exchange** settles, **curve** (forward), **rates**. **Reconciliation** (e.g. our mark vs broker) and **exception** handling. **Automate** **surface** build, **Greeks**, **P&amp;L** explain so I spend time on **trading** and **risk** decisions, not **manual** spreadsheets.
- **Dashboards** or **reports** I can **read** in **minutes**: **vega** by expiry, **realized vs implied**, **limit** status, **today’s** P&amp;L explain. **Alerts** (e.g. limit breach, large residual) so I can **act** quickly.

**Deliverable:** **Automated** pipeline; **dashboard**/report; **alert** logic.

---

### 6.7 Summary: analyst expectations (table)

| Expectation | Why it matters |
|-------------|----------------|
| **Surface build and maintenance** | **One** consistent vol (and curve) for **mark** and **hedge**; **traceability**. |
| **Realized vs implied (rich/cheap)** | **Trade** vol where it is **rich** or **cheap**; **prioritize** flow. |
| **Greeks and risk reports** | **Monitor** **vega**, **delta**, **limits**; **scenario** and **stress** for **capital** and **escalation**. |
| **P&amp;L explain and residual** | **Explain** P&amp;L; **catch** input/model error; **improve** over time. |
| **New products and model support** | **Trade** new payoffs/underlyings with **clean** mark and risk from **start**. |
| **Data and automation** | **Less** manual work; **faster** and **reliable** numbers; **alerts** for **limits** and **residual**. |

---

## 7. One-page recap

- **Vol trader** runs **option** book: **mark** at **consistent** vol surface, **manage** **vega** (and delta, gamma), **trade** vol (rich/cheap vs realized or relative). **Daily**: surface update, Greeks, limits, trading, hedge, P&amp;L explain.
- **Analysis**: **Realized vs implied** (rich/cheap); **term structure** (front vs back); **smile/skew** (wings vs ATM); **vega** bucketing; **sticky strike/delta** (scenario); **P&amp;L** explain (Taylor: delta, vega, theta, gamma, volga, vanna, residual).
- **Methodologies**: Each has **pros** (simple, interpretable, granular) and **cons** (backward-looking, illiquid, model risk); **assumptions** (e.g. past realized informative, smile stable, first-order sufficient). **Formulas**: realized vol, Black-76, vega, Taylor P&amp;L.
- **Expect from analyst**: **Surface** build and maintenance; **realized vs implied** report; **Greeks** and **risk** (scenario, stress, limits); **P&amp;L** explain and **residual** investigation; **new product** and **model** support; **data** and **automation** (pipeline, dashboard, alerts). So the vol desk can **trade** and **manage** risk with **consistent** marks and **actionable** analysis.
