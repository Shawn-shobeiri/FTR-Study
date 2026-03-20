# Statistics for Energy Commodity Trading (Quant Toolkit)

This note is a **practical** stats toolkit used constantly in energy commodity trading (power, gas, oil, emissions): **time series**, **regression**, **spreads**, **risk**, **tails**, **regimes**, and **backtesting**. The goal is not “academic statistics”—it’s: **make decisions under noise**, quantify **uncertainty**, and avoid getting fooled.

---

## 1. Data realities in energy

Energy data is messy. Your modeling choices should reflect these facts:

- **Non-stationarity**: market structure changes (pipeline expansions, LNG, renewables, policy).
- **Seasonality**: day-of-week, month-of-year, intraday (power), heating/cooling seasons (gas).
- **Spikes and fat tails**: especially power; gas has jumps in extreme weather / outages.
- **Constraints and censoring**: power price caps/floors, negative prices, congestion, outages.
- **Calendar effects**: holidays, DST, contract roll, prompt expiration.
- **Microstructure**: bid/ask, illiquidity in basis/options/long-dated forwards.

**Trading implication:** You almost always need **robust** methods, explicit **seasonality**, and you must separate **signal vs regime**.

---

## 2. Returns, stationarity, and transforms

### 2.1 Prices vs returns

- **Log return** (typical for positive prices):
  $$
  r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
  $$
- **Arithmetic return**:
  $$
  R_t = \frac{P_t - P_{t-1}}{P_{t-1}}
  $$
- **Difference** (often for spreads or mean-reverting series):
  $$
  \Delta P_t = P_t - P_{t-1}
  $$

**Rule of thumb:**
- For **level-like** series (some forwards), log returns can be reasonable.
- For **mean-reverting** series (basis, spreads), use **levels** or **differences** and model mean reversion directly.
- For **power**, be careful: negative prices break log returns; use **shifted logs**, **asinh**, or model in levels with spikes/regimes.

### 2.2 Standardization (z-scores)

For a signal \(x_t\) (spread, residual, basis):
$$
z_t = \frac{x_t - \mu}{\sigma}
$$
In practice use **rolling** estimates:
$$
z_t^{(\text{roll})} = \frac{x_t - \mu_{t,w}}{\sigma_{t,w}}
$$

**Use:** relative value (“is this spread rich/cheap vs history?”).  
**Caveat:** rolling windows fail during **regime changes** (variance shift).

---

## 3. Summary statistics you actually use

### 3.1 Moments and tail metrics

- **Mean/variance**: \(\mu, \sigma^2\)
- **Skewness**: asymmetry (power often **right-skewed** in scarcity regimes; can be left-skewed with negative pricing).
- **Kurtosis**: tail heaviness (fat tails → VaR underestimation if you assume normal).

### 3.2 Quantiles and expected shortfall

For loss \(L\) (positive = bad):
- **VaR** at level \(\alpha\):
  $$
  \mathrm{VaR}_\alpha = \inf\{l: \mathbb{P}(L \le l)\ge \alpha\}
  $$
- **Expected Shortfall (ES / CVaR)**:
  $$
  \mathrm{ES}_\alpha = \mathbb{E}[L \mid L \ge \mathrm{VaR}_\alpha]
  $$

**Trading implication:** ES is more informative for energy because tails matter (spikes).

---

## 4. Correlation, covariance, and what traders get wrong

### 4.1 Covariance and correlation

$$
\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mu_X)(Y-\mu_Y)], \quad
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}
$$

**Key pitfalls in energy:**
- Correlations are **state-dependent** (near scarcity, everything correlates differently).
- Correlation is **not** stable across seasons (winter gas vs summer).
- Correlation of **levels** vs **returns** can tell different stories.

### 4.2 Beta / hedge ratio (minimum-variance hedge)

If you hedge exposure \(X\) with instrument \(Y\), the min-variance hedge ratio is:
$$
\beta^* = \frac{\mathrm{Cov}(X,Y)}{\mathrm{Var}(Y)}
$$

**Use:** hedge basis risk, hub vs Henry, power vs gas (spark), etc.  
**Caveat:** use **rolling** and/or **regime-conditioned** betas.

### 4.3 Cointegration (spreads that “really” mean-revert)

Two price series \(X_t, Y_t\) might be non-stationary individually but a linear combo is stationary:
$$
\varepsilon_t = X_t - \beta Y_t \quad \text{is stationary}
$$

**Use:** location spreads, crack-like relationships, some linked hubs.  
**Caveat:** breaks with infrastructure/policy (pipeline expansions, LNG).

---

## 5. Time series essentials (mean reversion, seasonality, autocorrelation)

### 5.1 Autocorrelation and half-life

Autocorrelation at lag \(k\):
$$
\rho(k) = \mathrm{Corr}(x_t, x_{t-k})
$$

If a spread follows AR(1):
$$
x_t = c + \phi x_{t-1} + \epsilon_t, \quad |\phi|<1
$$
Mean reversion speed relates to \(\phi\). A common “half-life” approximation:
$$
t_{1/2} \approx \frac{\ln(0.5)}{\ln(\phi)}
$$

**Use:** choose holding period / signal decay for relative value trades.

### 5.2 OU (continuous-time mean reversion)

For a mean-reverting factor \(X_t\):
$$
dX_t = \kappa(\theta - X_t)\,dt + \sigma\,dW_t
$$
Conditional mean:
$$
\mathbb{E}[X_T \mid X_0] = \theta + (X_0-\theta)e^{-\kappa T}
$$

**Use:** basis/spread modeling; gas spot with seasonality; storage/swing valuation engines.

### 5.3 Seasonality decomposition

Additive seasonal model:
$$
x_t = \text{trend}_t + \text{seasonal}_t + \varepsilon_t
$$
Common energy seasonal components:
- **Day-of-week** (load/power), **hour-of-day** (shape)
- **Month-of-year** (gas winter/summer, maintenance seasons)
- **Holiday** indicators

**Practice:** regress out seasonality before fitting mean reversion or correlations.

---

## 6. Regression for traders (forecasting + factor attribution)

### 6.1 OLS and interpretation

Model:
$$
y = X\beta + \varepsilon
$$
OLS estimator:
$$
\hat{\beta} = (X^\top X)^{-1}X^\top y
$$

**Typical energy uses:**
- Gas demand: \( \text{consumption} \sim \mathrm{HDD}, \mathrm{CDD}, \text{day-of-week} \)
- Power price: \( P \sim \text{load}, \text{wind}, \text{solar}, \text{outages}, \text{fuel} \)
- Basis: \( \text{basis} \sim \text{flows}, \text{constraints}, \text{inventory} \) (where available)

### 6.2 Common issues (and fixes)

| Issue | Symptom | What to do |
|------|---------|------------|
| **Autocorrelated errors** | t-stats too optimistic | Newey–West standard errors; model dynamics (AR terms) |
| **Heteroskedasticity** | variance changes by regime/season | robust SE; model volatility; quantile regression |
| **Multicollinearity** | unstable betas | regularization (ridge/lasso), PCA factors |
| **Nonlinearity** | poor fit in extremes | splines, interactions (e.g. HDD × low storage), tree/GBM models |
| **Leakage** | “too good” backtest | strict time split, use only available data at time \(t\) |

### 6.3 Regularization (ridge / lasso)

- **Ridge**:
  $$
  \min_\beta \|y-X\beta\|^2 + \lambda \|\beta\|^2
  $$
- **Lasso**:
  $$
  \min_\beta \|y-X\beta\|^2 + \lambda \|\beta\|_1
  $$

**Use:** lots of correlated features (weather grids, many hubs, many lags).

---

## 7. Hypothesis testing you’ll actually use (carefully)

### 7.1 t-tests (difference in means)

Test if mean of spread is nonzero:
$$
t = \frac{\bar{x} - 0}{s/\sqrt{n}}
$$

**Caveat:** energy time series are autocorrelated → naive t-test overstates significance.

### 7.2 A/B tests for strategy changes

Compare two strategy variants on out-of-sample P&L distributions using:
- difference in means with **block bootstrap** (preserves autocorrelation)
- difference in Sharpe with bootstrap

**Avoid:** declaring victory on a few months of data.

---

## 8. Volatility, scaling, and risk forecasting

### 8.1 Realized volatility

For returns \(r_1,\dots,r_n\):
$$
\hat{\sigma} = \sqrt{\frac{1}{n-1}\sum_{i=1}^n (r_i - \bar{r})^2}
$$

Annualize (roughly):
$$
\sigma_{\text{ann}} \approx \sigma_{\text{daily}}\sqrt{252}
$$

**Caveat:** energy is seasonal; “252” is a convention—use the right horizon and calendar.

### 8.2 EWMA volatility (RiskMetrics-style)

$$
\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1-\lambda) r_{t-1}^2
$$

**Use:** quick risk scaling, dynamic position sizing.  
**Caveat:** underreacts to jumps unless \(\lambda\) is small.

### 8.3 GARCH(1,1) (common but imperfect)

$$
\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2
$$

**Use:** volatility clustering.  
**Caveat:** power spikes and regime shifts often violate standard GARCH assumptions.

---

## 9. Distributions, tails, and extreme events

### 9.1 Why normal is a trap

Energy returns often show:
- **fat tails** (kurtosis >> 3)
- **skew** (scarcity spikes)
- **mixtures** (normal times + spike regime)

### 9.2 EVT (peaks over threshold) intuition

Model exceedances above a high threshold \(u\):
$$
Y = X-u \mid X>u \sim \text{Generalized Pareto}
$$

**Use:** stress testing, “what’s a 1-in-20 winter day?”  
**Caveat:** choose \(u\) carefully; tails can be regime-dependent.

---

## 10. Regime changes (the most important “stat” in energy)

### 10.1 Mixture / regime-switching idea

Think of returns as coming from regimes:
$$
r_t \sim 
\begin{cases}
\mathcal{N}(\mu_1,\sigma_1^2), & z_t=1 \\
\mathcal{N}(\mu_2,\sigma_2^2), & z_t=2
\end{cases}
$$
where \(z_t\) follows a Markov chain (hidden Markov model / Markov switching).

**Use:** power spike vs normal, gas freeze-off regime, basis blowouts.

### 10.2 Change-point detection (practical)

Detect shifts in mean/variance/correlation and reduce reliance on “long history”:
- rolling z-scores on residuals
- CUSUM-like logic
- compare rolling vs long-run variance

**Trading implication:** treat “model fit” as conditional on regime; widen limits and stress scenarios when regime shifts.

---

## 11. Backtesting and statistical hygiene (non-negotiable)

### 11.1 Walk-forward (time series CV)

Never random-shuffle time series. Use walk-forward:
- train on \([1..T]\), test on \([T+1..T+h]\)
- roll forward and repeat

### 11.2 Overfitting controls

| Risk | Symptom | Control |
|------|---------|---------|
| **Too many knobs** | great in-sample, weak out-of-sample | reduce features, penalize, simpler model |
| **Multiple testing** | “found” many signals | hold-out set, reality check, deflated Sharpe |
| **Lookahead** | unrealistic signals | strict data availability timing |
| **Survivorship / selection** | only keep “good” hubs | predefine universe, include dead instruments |

### 11.3 Performance metrics (with caveats)

- **Sharpe**:
  $$
  \mathrm{Sharpe}=\frac{\mathbb{E}[r]}{\mathrm{Std}(r)}
  $$
  Adjust for autocorrelation and non-normality when comparing strategies.
- **Hit rate** vs **payoff ratio**: many energy strategies have low hit rate but large winners (spikes).
- **Max drawdown**: must be stress-tested under spikes / constraints.

---

## 12. Spreads and relative value (daily bread of energy trading)

### 12.1 Calendar spreads

Spread: \(S = P_{\text{winter}} - P_{\text{summer}}\) (or month \(m_1-m_2\)).  
Stats used:
- z-score of spread
- mean reversion (AR(1)/OU)
- regime conditioning (winter behaves differently)

### 12.2 Basis spreads (location)

Basis: \(B = P_{\text{hub}} - P_{\text{Henry}}\).  
Stats used:
- OU / AR(1) + seasonality
- correlation to flows / constraints proxies (when available)

### 12.3 Spark spread (cross-commodity)

Approx spark spread:
$$
\mathrm{Spark} \approx P_{\text{power}} - \mathrm{HR}\cdot P_{\text{gas}}
$$
Stats used:
- hedge ratio / beta (HR as sensitivity)
- correlation stability by season/regime
- tail dependence (scarcity hours)

---

## 13. Practical checklist (what I do before trusting a result)

- **Define** the objective (forecast, hedge ratio, relative value, risk).
- **Plot** the series: seasonality, spikes, missing data.
- **De-seasonalize** if needed (hour/day/month effects).
- **Check** stationarity (visual + ACF; formal tests are secondary).
- **Estimate** mean reversion / half-life for spreads.
- **Use robust** stats: rolling windows, robust SE, bootstrap.
- **Stress** with regimes: scarcity, freeze, outage, basis blowout.
- **Walk-forward** validate; avoid leakage.

---

## 14. One-page recap

- **Core objects**: prices, returns, spreads; de-seasonalize first.
- **Most-used stats**: z-scores, correlation/hedge ratios, AR(1)/OU mean reversion + half-life, rolling vol (EWMA), VaR/ES.
- **Most important reality**: regimes + tails. Your biggest “stat error” is assuming stability.
- **Best practice**: walk-forward backtests, robust inference, and explicit stress scenarios.

---

## 15. Worked trading examples (more context)

These are the “everyday” workflows where the concepts above show up on real desks.

### 15.1 Example A — Basis hedge ratio (Hub vs Henry)

**Problem:** You’re long physical at a regional hub and hedging with Henry futures/swaps. You want a hedge ratio that minimizes variance.

Let \(X_t\) be your exposure return (or P&L per day) and \(Y_t\) be the hedge instrument return (Henry).

**Minimum-variance hedge ratio:**
$$
\beta^*=\frac{\mathrm{Cov}(X,Y)}{\mathrm{Var}(Y)}
$$

**In practice:**
- Use **returns** for \(X,Y\) if both are liquid traded prices; use **differences** if working with spreads and levels.
- Estimate \(\beta^*\) **rolling** (e.g. 60–120 days) and compare with a long-run estimate.
- Use **robust** inference: residuals are often autocorrelated → don’t trust naive t-stats.

**Interpretation:** If \(\beta^*=0.85\), you hedge ~85% of the Henry sensitivity; the remaining risk is mostly **basis** (location constraints, outages).

**Common failure mode:** \(\beta\) is stable in “normal” flow regimes but breaks during constraint events (basis blowouts). Treat \(\beta\) as **regime-conditional**.

### 15.2 Example B — Calendar spread mean reversion and half-life

**Problem:** You trade a calendar spread \(S_t = P_{m1,t}-P_{m2,t}\) (or winter–summer). You want to know if it mean-reverts on a horizon consistent with your risk limits.

Fit AR(1) on a de-seasonalized spread:
$$
S_t = c + \phi S_{t-1} + \epsilon_t
$$
Half-life estimate:
$$
t_{1/2}\approx \frac{\ln(0.5)}{\ln(\phi)}
$$

**Trader interpretation:**
- If \(\phi=0.97\), half-life is long → the spread can stay “wrong” for weeks; size smaller and use wider stops.
- If \(\phi=0.85\), half-life is short → relative value mean reversion is plausibly tradable.

**Two practical caveats:**
- Spreads often have **seasonal variance** (winter spreads behave differently). Fit \(\phi\) by season or include seasonality.
- Don’t confuse “stat mean reversion” with “economic” mean reversion—structural changes (LNG, pipeline) can shift the mean permanently.

### 15.3 Example C — Spark spread correlation that changes in scarcity hours

**Problem:** You model spark:
$$
\mathrm{Spark}_t = P_{\text{power},t} - \mathrm{HR}\cdot P_{\text{gas},t}
$$
but you notice correlation between power and gas is different in scarcity hours.

**Workflow:**
- Split sample into regimes, e.g. “normal” vs “scarcity” using a proxy:
  - top \(q\)% load hours
  - low renewable output hours
  - price above a threshold
- Estimate correlations/betas by regime:
  $$
  \rho^{(\text{normal})},\ \rho^{(\text{scarcity})}
  $$
  and hedge ratios \(\beta^{(\cdot)}\).

**Why it matters:** Pricing/hedging a spark option or a shaped position using one unconditional \(\rho\) often **understates tail risk** because the joint behavior is different in the states that drive P&L.

### 15.4 Example D — “Is this signal real?” (walk-forward + block bootstrap)

**Problem:** You have a mean reversion signal \(z_t\) on a spread and a rule: go short when \(z>2\), long when \(z<-2\). Your backtest looks great.

**Minimum statistical hygiene:**
- Walk-forward split: train thresholds/parameters on \([1..T]\), test on \([T+1..T+h]\), roll forward.
- Use **block bootstrap** of daily returns (e.g. 5–20 day blocks) to preserve autocorrelation when estimating uncertainty of Sharpe / mean.

**Interpretation:** If the bootstrapped Sharpe distribution has mass near 0 (or negative), the “great” Sharpe was likely luck or regime-specific.

### 15.5 Example E — Tail risk: VaR vs ES for spiky commodities

**Problem:** Your portfolio has exposure to power scarcity spikes. Normal VaR says risk is small; you’re not convinced.

Compute both:
$$
\mathrm{VaR}_\alpha,\quad \mathrm{ES}_\alpha = \mathbb{E}[L\mid L\ge \mathrm{VaR}_\alpha]
$$

**Energy-specific context:**
- VaR can look fine while ES explodes because losses are concentrated in rare events.
- Stress test with “event days” (freeze, outages, congestion) as separate scenarios; treat them as regimes, not noise.

### 15.6 Example F — Gas demand model (HDD/CDD) that doesn’t lie to you

**Problem:** You want to forecast gas demand (or power burn) from weather and calendar effects, and translate that into a price view.

Typical regression skeleton:
$$
\text{Demand}_t = \beta_0 + \beta_1 \mathrm{HDD}_t + \beta_2 \mathrm{CDD}_t + \gamma^\top \text{Calendar}_t + \varepsilon_t
$$
where \(\text{Calendar}_t\) includes day-of-week, month, holiday, and potentially lag terms.

**Two “energy” upgrades that matter:**
- **Nonlinearity in extremes**: add piecewise terms, e.g.
  $$
  \text{Demand}_t = \dots + \beta_{1a}\mathrm{HDD}_t + \beta_{1b}\max(\mathrm{HDD}_t - h,0) + \dots
  $$
  to capture that very cold days have disproportionate effects.
- **Supply shock interaction** (for price): include a scarcity proxy interaction, e.g. \(\mathrm{HDD}\times \mathbb{1}[\text{low storage}]\).

**Inference context:** errors are autocorrelated and heteroskedastic; if you care about significance, use **robust** standard errors (see Example I).

### 15.7 Example G — Storage optionality as a statistical problem (state variables)

**Problem:** You want intuition for what drives storage value besides the forward winter–summer spread.

The state that matters is not just “price”; it’s:
- **inventory** \(I_t\)
- **time** \(t\) (season)
- **prompt vs deferred** structure (calendar spreads)
- **volatility** (esp. prompt)

A useful mental model:
- Storage value increases with **prompt volatility** and with **mean reversion** (more chances to buy low / sell high).
- Storage value decreases when constraints bind: low inject/withdraw rates, narrow working gas, ratchets.

**Stat tie-in:** when you regress P&L of a storage strategy, include these features (inventory, spreads, vol proxies) and expect **regime dependence** (winter behaves differently).

### 15.8 Example H — Cointegration → error-correction trade design

**Problem:** You believe two linked hubs (or related products) move together long run, but can diverge short run.

If \(X_t\) and \(Y_t\) are I(1) but \(X_t - \beta Y_t\) is stationary, define the spread:
$$
e_t = X_t - \beta Y_t
$$
Then an **error-correction model** (ECM) intuition:
$$
\Delta X_t = a + \lambda e_{t-1} + \eta \Delta Y_t + u_t
$$
with \(\lambda<0\) implying pullback when the spread is wide.

**Trading context:** the “mean” level can shift when infrastructure changes—cointegration can hold for years then break fast. Treat it as **conditional** and monitor break signals (rolling residual variance, change points).

### 15.9 Example I — Newey–West (HAC) standard errors in one line

**Problem:** You run a regression and get a huge t-stat, but the residuals are autocorrelated (common in energy). Naive OLS SE is too optimistic.

**Fix:** Use **HAC / Newey–West** standard errors (choose a lag consistent with your sampling, e.g. 5–20 days for daily; 24–168 for hourly depending on seasonality you already removed).

**Trader takeaway:** often the coefficient sign is still useful, but the “confidence” is overstated unless you adjust.

### 15.10 Example J — EVT threshold choice and “event day” stress

**Problem:** You want tail estimates for scarcity spikes or basis blowouts without pretending everything is Gaussian.

Two complementary approaches:
- **EVT (POT)**: pick a threshold \(u\) (e.g. 95th/97.5th percentile of losses), model exceedances \(Y=X-u\).
- **Event-day stress set**: explicitly maintain a library of historical event days (freeze, hurricane, major outages) and stress the portfolio on those days regardless of frequency.

**Energy reality:** EVT can help shape the tail, but “event day” scenario analysis is often the more honest representation of structural tail risk.

---

## 16. More stats concepts you’ll use a lot (and how they map to energy)

### 16.1 Bayesian updating (turn forecasts into positions)

**Concept:** Combine a prior belief with new evidence. At a desk level this is “don’t overreact to one print, but do update.”

If you have a prior for a mean \(m\) (e.g. expected spread) and observe data with noise, posterior mean is a weighted average (precision-weighted):
$$
m_{\text{post}}=\frac{m_{\text{prior}}/\sigma_{\text{prior}}^2 + \bar{x}/\sigma_{\text{obs}}^2}{1/\sigma_{\text{prior}}^2 + 1/\sigma_{\text{obs}}^2}
$$

**Energy mapping:**
- Prior: long-run seasonal mean of a basis/spread.
- Observation: latest move during a potential constraint event.
- Use: position sizing that respects uncertainty (bigger size only when signal is strong vs noise).

### 16.2 Kalman filter / state-space (time-varying hedge ratios)

**Concept:** A dynamic regression where coefficients evolve through time. This is how you model a hedge ratio that drifts with regime.

State (time-varying beta):
$$
\beta_t = \beta_{t-1} + w_t
$$
Observation equation (hedge relationship):
$$
X_t = \alpha + \beta_t Y_t + v_t
$$

**Energy mapping:**
- Hub vs Henry hedge ratio that changes with pipeline constraints.
- Power vs gas sensitivity that changes by season or scarcity.

**Trader takeaway:** Kalman gives you a smoother, faster-adapting \(\beta_t\) than rolling OLS and usually behaves better through transitions.

### 16.3 PCA / factor models (reduce many curves/hubs into a few drivers)

**Concept:** Turn many correlated series into a few orthogonal factors:
$$
X \approx F L^\top
$$
where \(F\) are factor scores and \(L\) are loadings.

**Energy mapping:**
- Forward curve moves: **level**, **slope**, **curvature** factors.
- Multi-hub basis books: a few regional flow/constraint factors explain most variance.

**Use:** risk (VaR), stress design, and “what is my book really long/short?”

### 16.4 Shrinkage covariance (when correlations are unstable)

**Concept:** Sample covariance is noisy, especially with many assets and limited data. Shrink it toward a structured target:
$$
\Sigma_{\text{shrunk}} = (1-\delta)\Sigma_{\text{sample}} + \delta \Sigma_{\text{target}}
$$

**Energy mapping:** portfolio risk across many hubs/tenors where history is short or regime shifts make estimates unstable.

**Trader takeaway:** better risk numbers, less “optimizer madness,” more stable hedges.

### 16.5 Quantile regression (model the tails directly)

**Concept:** Instead of modeling the conditional mean \(E[y|x]\), model a conditional quantile \(Q_\tau(y|x)\) (e.g. 95th percentile):
$$
Q_\tau(y|x)=x^\top \beta_\tau
$$

**Energy mapping:**
- Model **upper-tail** power price (scarcity) as function of load, outages, renewables.
- Model **tail** basis blowout risk conditional on storage/flows proxies.

**Why you care:** average behavior is often irrelevant; the tail drives risk and option value.

### 16.6 Tail dependence (correlation is not enough)

**Concept:** Two series can have modest correlation but still crash/spike together in extremes. Tail dependence measures co-movement in tails.

Upper tail dependence coefficient (conceptual):
$$
\lambda_U = \lim_{u\to 1^-} \mathbb{P}(Y>F_Y^{-1}(u)\mid X>F_X^{-1}(u))
$$

**Energy mapping:**
- Power hubs during scarcity: large joint moves.
- Gas + power during freeze events.

**Trader takeaway:** for stress and option books, focus on tail co-moves, not just \(\rho\).

### 16.7 Proper scoring rules (how to evaluate probabilistic forecasts)

**Concept:** If you forecast distributions (not point forecasts), use proper scoring rules.

Example: **log score** for a density forecast \(p(\cdot)\) at realized \(x\):
$$
\text{Score} = \log p(x)
$$

**Energy mapping:**
- Weather-driven demand distributions.
- Price path distributions used for storage/swing valuation.

**Trader takeaway:** a model that “gets the variance right” can be more valuable than one that nails the mean but misses tails.

### 16.8 The simplest “model risk” discipline: model ensembles

**Concept:** Don’t bet your book on one fragile specification; combine models.

Linear ensemble:
$$
\hat{y} = \sum_{i=1}^k w_i \hat{y}^{(i)}, \quad \sum_i w_i = 1
$$

**Energy mapping:**
- Blend: regression demand model + OU/seasonal time-series + fundamental balance sanity check.
- Use different regimes: one model for normal days, one for scarcity.

