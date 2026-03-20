# Regression Models in Energy Commodities: FTR, Power, and Gas

A practical guide from the perspective of a seasoned quant: which **regression** models we use to model **FTR** (path spread, binding, shadow prices), **power** (LMP, demand, price drivers), and **gas** (demand, price, basis), with **assumptions**, **formulas**, and **pros and cons**.

---

## 1. Why regression in energy?

We use regression to **predict** or **explain** outcomes using **observable drivers**:

- **FTR:** Path spread or **constraint shadow price** (continuous, often **zero** when not binding); **binding probability** (binary or count); **drivers**: load, temperature, renewables, outages, hour, season.
- **Power:** **LMP** or **hub price** (continuous, sometimes spiky); **demand/load** (continuous); **drivers**: load, temperature, wind/solar, hour, day type, season.
- **Gas:** **Price** or **demand** (continuous); **basis** (spread between hubs); **drivers**: temperature (heating/cooling degree days), storage, supply, season.

The **right** model depends on the **outcome** (continuous, binary, count, zero-inflated, censored) and **distribution** (normal, skewed, fat-tailed). Below we list the main models, their **formulas**, **assumptions**, and **pros/cons**, then **where** they fit for FTR, power, and gas.

---

## 2. Ordinary least squares (OLS)

**Model:** $Y_i = \mathbf{x}_i^\top \boldsymbol{\beta} + \varepsilon_i$, with $\mathbb{E}[\varepsilon_i \mid \mathbf{x}_i] = 0$, $\mathrm{Var}(\varepsilon_i) = \sigma^2$ (constant), and $\varepsilon_i$ uncorrelated across $i$.

**Estimation:** Minimize sum of squared residuals: $\widehat{\boldsymbol{\beta}}_{\mathrm{OLS}} = \arg\min_{\boldsymbol{\beta}} \sum_i (Y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2$. Closed form:
$$
\widehat{\boldsymbol{\beta}}_{\mathrm{OLS}} = (\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top \mathbf{Y}, \qquad \widehat{\sigma}^2 = \frac{1}{n-p} \sum_i \widehat{\varepsilon}_i^2, \quad \widehat{\varepsilon}_i = Y_i - \mathbf{x}_i^\top \widehat{\boldsymbol{\beta}}.
$$
Under **homoskedasticity** and **no autocorrelation**, $\mathrm{Var}(\widehat{\boldsymbol{\beta}}) = \sigma^2 (\mathbf{X}^\top \mathbf{X})^{-1}$; standard errors and **t**-tests follow.

**Assumptions:**

| Assumption | What it means | Often violated when |
|------------|----------------|---------------------|
| **Linearity** | $\mathbb{E}[Y \mid \mathbf{x}] = \mathbf{x}^\top \boldsymbol{\beta}$ | Non-linear response (e.g. price vs load convex); use **transform** (e.g. $\ln Y$) or **GAM**. |
| **Homoskedasticity** | $\mathrm{Var}(\varepsilon \mid \mathbf{x}) = \sigma^2$ | **Heteroskedasticity**: vol depends on level (e.g. high load → higher price variance) → use **WLS** or **robust** SEs. |
| **Exogeneity** | $\mathbb{E}[\varepsilon \mid \mathbf{x}] = 0$ | **Omitted** variables or **simultaneity** (e.g. price and quantity determined together). |
| **No autocorrelation** | $\mathrm{Cov}(\varepsilon_i, \varepsilon_j) = 0$ for $i \neq j$ | **Time series**: residuals **correlated** over time → use **HAC** SEs or **time-series** model. |
| **Normality** (for inference) | $\varepsilon \sim N(0, \sigma^2)$ | **Fat tails**, **skew** (e.g. price spikes) → **robust** or **bootstrap** inference; or **quantile** regression. |

**Pros:** Simple; **unbiased** under exogeneity; **BLUE** under Gauss–Markov; **interpretable** coefficients.  
**Cons:** **Sensitive** to **heteroskedasticity** (wrong SEs), **outliers**, and **non-normality**; **no** direct modeling of **tails** or **zero-inflation**.

**Use in energy:** **Power/gas** price or **demand** vs load, temperature, hour dummies when **errors** are roughly **homoskedastic** and **symmetric**; **FTR** path spread **conditional on binding** (subset of data where spread $> 0$).

---

## 3. Weighted least squares (WLS) and generalized least squares (GLS)

**Model:** $Y_i = \mathbf{x}_i^\top \boldsymbol{\beta} + \varepsilon_i$ with $\mathrm{Var}(\varepsilon_i \mid \mathbf{x}_i) = \sigma_i^2$ (known or estimated). **WLS:** weights $w_i = 1/\sigma_i^2$; minimize $\sum_i w_i (Y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2$. **GLS:** $\boldsymbol{\varepsilon} \sim (\mathbf{0}, \boldsymbol{\Omega})$; $\widehat{\boldsymbol{\beta}}_{\mathrm{GLS}} = (\mathbf{X}^\top \boldsymbol{\Omega}^{-1} \mathbf{X})^{-1} \mathbf{X}^\top \boldsymbol{\Omega}^{-1} \mathbf{Y}$.

**Typical use:** **Heteroskedasticity**: e.g. $\sigma_i^2 = \sigma^2 \cdot (\text{load}_i)^2$ or **fitted** from a first-stage OLS (squared residuals vs predictors). **Feasible GLS (FGLS):** estimate $\boldsymbol{\Omega}$ then plug in.

**Assumptions:** Same as OLS except **variance** (and possibly **correlation**) is **modeled**; **correct** $\boldsymbol{\Omega}$ gives **efficient** estimator.

**Pros:** **Efficient** when **heteroskedasticity** (or correlation) is correctly specified; **smaller** SEs than OLS.  
**Cons:** **Misspecified** weights can **worsen** efficiency; **two-step** (estimate $\boldsymbol{\Omega}$) adds **noise**. **Robust** SEs (e.g. White) are often used with **OLS** when we don’t want to model variance.

**Use in energy:** **Power** price vs load when **variance** increases with load; **gas** demand when **variance** varies by temperature band.

---

## 4. Ridge and Lasso (regularized linear regression)

**Model:** Same linear $Y_i = \mathbf{x}_i^\top \boldsymbol{\beta} + \varepsilon_i$, but **penalized** objective:
- **Ridge:** $\widehat{\boldsymbol{\beta}} = \arg\min_{\boldsymbol{\beta}} \sum_i (Y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2 + \lambda \sum_{j} \beta_j^2$.
- **Lasso:** $\widehat{\boldsymbol{\beta}} = \arg\min_{\boldsymbol{\beta}} \sum_i (Y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2 + \lambda \sum_{j} |\beta_j|$.

**Formulas:** Ridge has closed form: $\widehat{\boldsymbol{\beta}}_{\mathrm{ridge}} = (\mathbf{X}^\top \mathbf{X} + \lambda \mathbf{I})^{-1} \mathbf{X}^\top \mathbf{Y}$. Lasso typically solved by **coordinate descent** or **LARS**; some $\widehat{\beta}_j$ become **exactly zero** (variable selection).

**Assumptions:** Same **linearity** and **exogeneity** as OLS; **regularization** helps when $p$ is large or **multicollinearity** is present. **Scale** predictors (e.g. standardize) so penalty is **fair** across coefficients.

**Pros:** **Ridge**: **Stable** with **multicollinearity**; **Lasso**: **sparse** solution (interpretability, **variable selection**). Both **reduce overfitting** when many predictors.  
**Cons:** **Bias** (shrinkage); **$\lambda$** must be chosen (e.g. **cross-validation**); **inference** (SEs, p-values) is **non-standard** (bootstrap or post-selection).

**Use in energy:** **Many** drivers (load, temp, wind, solar, hour dummies, lagged price, …); **Lasso** to **select** which drivers matter for **LMP** or **path spread**; **Ridge** when we want **all** predictors but **stable** coefficients.

---

## 5. Quantile regression

**Model:** Model the **$\tau$-quantile** of $Y$ given $\mathbf{x}$: $Q_Y(\tau \mid \mathbf{x}) = \mathbf{x}^\top \boldsymbol{\beta}(\tau)$. No distributional assumption on $\varepsilon$; **asymmetric** loss.

**Estimation:** Minimize **check (pinball) loss**: $\widehat{\boldsymbol{\beta}}(\tau) = \arg\min_{\boldsymbol{\beta}} \sum_i \rho_\tau(Y_i - \mathbf{x}_i^\top \boldsymbol{\beta})$, where $\rho_\tau(u) = u\,(\tau - \mathbf{1}_{u < 0})$. Solved by **linear programming**.

**Assumptions:** **Linearity** of **quantile** (not mean); **no** assumption on **conditional distribution** (can be **skewed**, **fat-tailed**). **Exogeneity** for the **quantile** (stronger than mean exogeneity in practice).

**Pros:** **Robust** to **outliers** and **non-normality**; **direct** modeling of **tails** (e.g. 5th and 95th percentile for **VaR**); **heteroskedasticity** is **allowed** (different $\boldsymbol{\beta}(\tau)$ at different $\tau$).  
**Cons:** **Slower** than OLS; **many** quantiles → **many** coefficient vectors; **crossing** quantiles (can be fixed with constraints).

**Use in energy:** **Power/gas** price **tail** (e.g. 95th percentile of LMP vs load); **VaR**-style prediction (e.g. 5th percentile of next-day P&amp;L); **FTR** path spread **conditional** distribution (e.g. 90th percentile when binding).

---

## 6. Binary outcome: Logit and Probit

**Model:** $Y_i \in \{0, 1\}$ (e.g. constraint **binds** vs **not**). **Latent** variable: $Y_i^* = \mathbf{x}_i^\top \boldsymbol{\beta} + \varepsilon_i$, $Y_i = \mathbf{1}_{Y_i^* > 0}$. **Probit:** $\varepsilon \sim N(0,1)$ → $\mathbb{P}(Y=1 \mid \mathbf{x}) = \Phi(\mathbf{x}^\top \boldsymbol{\beta})$. **Logit:** $\varepsilon$ logistic → $\mathbb{P}(Y=1 \mid \mathbf{x}) = \frac{e^{\mathbf{x}^\top \boldsymbol{\beta}}}{1 + e^{\mathbf{x}^\top \boldsymbol{\beta}}} = \Lambda(\mathbf{x}^\top \boldsymbol{\beta})$.

**Estimation:** **Maximum likelihood**; no closed form; **Newton–Raphson** or **IRWLS**. Coefficients are in **latent** scale; **marginal effects** (derivative of $\mathbb{P}(Y=1)$ w.r.t. $x_j$) depend on $\mathbf{x}$.

**Assumptions:** **Latent** linearity; **distribution** of $\varepsilon$ (normal vs logistic — usually similar fit); **independence** of observations (or **cluster-robust** SEs for panel).

**Pros:** **Correct** for **binary** outcome; **probabilities** in $(0,1)$; **interpretable** (odds ratio for logit).  
**Cons:** **Non-linear** in $\boldsymbol{\beta}$; **marginal effects** vary with $\mathbf{x}$; **not** for **continuous** $Y$.

**Use in energy:** **FTR**: **Binding probability** (constraint binds = 1, else 0) vs load, temperature, hour, outage dummies. **Power**: Probability of **price spike** above threshold vs load, renewables.

---

## 7. Count outcome: Poisson and negative binomial (NB)

**Model:** $Y_i \in \{0, 1, 2, \ldots\}$ (e.g. **number of binding hours** per day). **Poisson:** $\mathbb{P}(Y = k \mid \mathbf{x}) = \frac{\lambda^k e^{-\lambda}}{k!}$, $\lambda = \exp(\mathbf{x}^\top \boldsymbol{\beta})$ (log link). **NB:** Same mean $\lambda$, but **variance** $= \lambda + \alpha \lambda^2$ (overdispersion).

**Estimation:** **MLE**; Poisson has **equidispersion** ($\mathrm{Var}(Y) = \mathbb{E}[Y]$); **NB** when **variance** $>$ mean (common in practice).

**Assumptions:** **Count** data; **log-linear** mean; **Poisson**: variance = mean; **NB**: **overdispersion** allowed.

**Pros:** **Correct** for **counts**; **NB** handles **overdispersion**; **interpretable** (e.g. $\beta_j$ = log relative rate per unit $x_j$).  
**Cons:** **Not** for **continuous** $Y$; **zero-inflation** (excess zeros) may need **zero-inflated** Poisson/NB (ZIP/ZINB).

**Use in energy:** **FTR**: **Number of hours** (or days) constraint **binds** per month vs load, outages, season. **Power**: **Count** of **spike hours** per month.

---

## 8. Censored outcome: Tobit (type I)

**Model:** $Y^* = \mathbf{x}^\top \boldsymbol{\beta} + \varepsilon$, $\varepsilon \sim N(0, \sigma^2)$. We observe $Y = \max(Y^*, 0)$ (or $Y = Y^*$ if $Y^* > 0$, else $Y = 0$). So **latent** outcome can be negative, but **observed** is **censored** at 0.

**Estimation:** **MLE** with **mixture** of (1) $\mathbb{P}(Y=0) = \Phi(-\mathbf{x}^\top \boldsymbol{\beta}/\sigma)$ and (2) density of **normal** for $Y > 0$ (truncated at 0).

**Assumptions:** **Latent** normality; **censoring** at 0 (or known threshold); **single** regime (same $\boldsymbol{\beta}$ for “participation” and “level”).

**Pros:** **Uses** both **zeros** and **positive** values in one model; **consistent** if **censoring** is correct.  
**Cons:** **Normality** of latent; **sensitive** to **censoring** assumption; **two-part** or **zero-inflated** often **more flexible** (separate model for zero vs positive).

**Use in energy:** **FTR**: **Shadow price** $\mu \ge 0$ (observed 0 when not binding); **path spread** when we view 0 as **censored** latent spread. **Gas**: **Demand** or **flow** censored at 0.

---

## 9. Two-part and zero-inflated models (continuous outcome with zeros)

**Problem:** $Y \ge 0$ with **mass at zero** (e.g. path spread = 0 when not binding) and **continuous** positive part. **OLS** on $Y$ is **biased**; **OLS** on $Y \mid Y > 0$ ignores **probability of zero**.

**Two-part model:**  
(1) **Binary**: $\mathbb{P}(Y > 0 \mid \mathbf{x})$ via **logit/probit**.  
(2) **Continuous**: $\mathbb{E}[\ln Y \mid Y > 0, \mathbf{x}]$ or $\mathbb{E}[Y \mid Y > 0, \mathbf{x}]$ via **OLS** (or **gamma** GLM for $Y > 0$).  
**Unconditional mean:** $\mathbb{E}[Y \mid \mathbf{x}] = \mathbb{P}(Y > 0 \mid \mathbf{x}) \times \mathbb{E}[Y \mid Y > 0, \mathbf{x}]$.

**Zero-inflated (ZI):** **Mixture**: with probability $p(\mathbf{x})$ we have $Y = 0$ (“structural” zero); with probability $1 - p(\mathbf{x})$ we draw from **continuous** distribution (e.g. lognormal, gamma). **Calibration**: fit $p$ (e.g. logit) and **conditional** distribution (e.g. OLS on $\ln Y$ given $Y > 0$).

**Assumptions:** **Correct** specification of **participation** (zero vs positive) and **conditional** distribution of $Y \mid Y > 0$; **independence** of the two parts given $\mathbf{x}$ (in two-part).

**Pros:** **Flexible**; **separate** drivers for “binding” vs “how much”; **matches** FTR **zero-inflation**.  
**Cons:** **Two** (or more) equations to fit and **interpret**; **distribution** of $Y \mid Y > 0$ may be **skewed** (use **log** or **gamma**).

**Use in energy:** **FTR**: **Path spread** or **shadow price** (zero when not binding; positive when binding). **Power**: **Congestion** component (zero when no congestion). **Gas**: **Basis** or **spread** that is often zero.

---

## 10. Application: FTR

| Outcome | Description | Suggested model | Drivers (examples) |
|---------|-------------|-----------------|---------------------|
| **Path spread** (continuous, zero-inflated) | Sink − source price per interval | **Two-part** (logit for binding + OLS/gamma for spread \| binding); **quantile** regression on $Y \mid Y \neq 0$ for **tails** | Load, temperature, wind/solar, hour, day type, outage dummies, season |
| **Binding probability** (binary) | Constraint binds = 1 | **Logit** or **Probit** | Load, flow, outage, hour, season |
| **Binding count** (count) | Hours (or days) binding per period | **Poisson** or **NB** (ZIP/ZINB if excess zeros) | Load, outages, season |
| **Shadow price** (non-negative, zero-inflated) | $\mu_\ell \ge 0$ | **Two-part** (logit + OLS on $\ln \mu \mid \mu > 0$); or **Tobit** (censored at 0) | Same as path spread; constraint-specific (flow, margin) |
| **Expected path value** | $\mathbb{E}[\text{spread}]$ or $\mathbb{E}[\max(\text{spread},0)]$ | **Two-part** gives $\mathbb{P}(\text{bind}) \times \mathbb{E}[\text{spread} \mid \text{bind}]$; or **quantile** for **distribution** | Same |

**Caveats:** **Correlation** across **paths** (and constraints) not modeled in single-equation regression; for **portfolio** or **VaR** use **multivariate** or **joint** model (e.g. **seemingly unrelated** regression, **copula**). **Outages** and **topology** change **PTDFs**; **time** and **regime** dummies help.

---

## 11. Application: Power

| Outcome | Description | Suggested model | Drivers (examples) |
|---------|-------------|-----------------|---------------------|
| **LMP / hub price** (continuous) | $/MWh | **OLS** (or **WLS** if heteroskedastic) with **log** price if skewed; **quantile** regression for **tails** (e.g. 95th percentile) | Load, temperature, wind/solar output, hour, day type, month, lagged price |
| **Demand / load** (continuous) | MW | **OLS** or **GAM** (smooth in temp); **temperature** (level, HDD/CDD), hour, day type | Temperature, hour, day of week, month, holiday |
| **Price spike** (binary) | LMP $> K$ | **Logit/Probit** | Load, renewables, hour, season |
| **Spike count** (count) | Hours above threshold per period | **Poisson** or **NB** | Load, wind/solar, season |
| **Congestion component** (zero-inflated) | Congestion $ \ge 0$ | **Two-part** or **Tobit** | Load, flow, interface, outage |

**Caveats:** **Autocorrelation** (use **lagged** price or **time-series** + regressors); **non-linearity** (load–price often **convex** → **spline** or **GAM**); **many** hubs/hours → **panel** or **fixed effects** (hub, hour).

---

## 12. Application: Gas

| Outcome | Description | Suggested model | Drivers (examples) |
|---------|-------------|-----------------|---------------------|
| **Price** (continuous) | $/MMBtu at hub | **OLS** (or **log** price); **quantile** for **tails** | Storage level, demand proxy (HDD/CDD), supply, season, lagged price |
| **Demand** (continuous) | Volume | **OLS** or **GAM**; **HDD** (heating degree days), **CDD** (cooling), day type | Temperature, day of week, month |
| **Basis** (spread, can be negative) | Hub A − Henry | **OLS** (spread as $Y$); **quantile** for **tail** basis | Pipeline capacity, local demand, season |
| **Basis** (zero or positive) | Max(spread, 0) or **positive** spread only | **Two-part** if **zero-inflation**; **OLS** on **level** if spread $ \ge 0$ always | Same |

**Caveats:** **Seasonality** (winter vs summer); **storage** and **supply** are **endogenous** in equilibrium — **IV** or **reduced form** with **lagged** fundamentals; **extreme** events (freeze) → **quantile** or **stress** dummies.

---

## 13. Summary table: model choice by outcome type

| Outcome type | Model | Main assumption | FTR | Power | Gas |
|--------------|-------|------------------|-----|--------|-----|
| **Continuous, symmetric** | OLS | Linear mean; homoskedastic | Spread \| binding | LMP, load | Price, demand |
| **Continuous, heteroskedastic** | WLS / GLS | Known or estimated variance | — | LMP (vol ~ load) | — |
| **Many predictors, multicollinearity** | Ridge / Lasso | Linearity; penalty | Drivers for spread/shadow | LMP drivers | Price/demand drivers |
| **Tails / quantiles** | Quantile regression | Linear quantile | Spread \| binding (e.g. 90th) | LMP tail (VaR-style) | Price tail |
| **Binary** | Logit / Probit | Latent linear | Binding yes/no | Spike yes/no | — |
| **Count** | Poisson / NB | Log-linear mean; (over)dispersion | Binding count | Spike count | — |
| **Censored at 0** | Tobit | Latent normal | Shadow price | Congestion | Demand (if censored) |
| **Zero-inflated continuous** | Two-part / ZI | Separate zero vs positive | Path spread, shadow | Congestion | Basis (if ZI) |

---

## 14. Assumptions recap and diagnostics

- **Linearity:** **Residual plots** ($\widehat{\varepsilon}$ vs $\mathbf{x}$ or $\widehat{Y}$); **RESET** test; **splines** or **GAM** if non-linear.
- **Homoskedasticity:** **Breusch–Pagan**; **White**; plot $|\widehat{\varepsilon}|$ vs $\widehat{Y}$. Remedy: **WLS**, **robust** SEs, or **quantile** regression.
- **Normality:** **Q–Q plot** of residuals; **skew/kurtosis**. Remedy: **robust** SEs, **bootstrap**, or **quantile** regression.
- **Autocorrelation:** **ACF** of residuals; **Durbin–Watson**. Remedy: **lagged** $Y$ or **HAC** SEs; **time-series** model (ARIMAX).
- **Exogeneity:** **Omitted** variables (economic argument); **IV** if **endogeneity** (e.g. price and quantity).
- **Binary/count:** **Goodness of fit** (e.g. **Hosmer–Lemeshow** for logit); **overdispersion** test for Poisson (use **NB** if present).

---

## 15. One-page recap

- **OLS**: Linear mean; **BLUE** under Gauss–Markov; **sensitive** to heteroskedasticity, outliers, non-normality. Use for **continuous** $Y$ (power/gas price, demand; FTR spread **conditional on binding**).
- **WLS/GLS**: **Heteroskedasticity** or **correlation**; **efficient** if $\boldsymbol{\Omega}$ correct.
- **Ridge/Lasso**: **Regularization**; **Lasso** = variable selection; use when **many** drivers (LMP, path spread).
- **Quantile regression**: **Tails** and **VaR**-style prediction; **no** distributional assumption; **heteroskedasticity** allowed.
- **Logit/Probit**: **Binary** (e.g. FTR **binding**, **price spike**).
- **Poisson/NB**: **Count** (e.g. **binding hours**, **spike count**); **NB** for **overdispersion**.
- **Tobit**: **Censored** at 0 (e.g. **shadow price**, **demand**).
- **Two-part / zero-inflated**: **Zero-inflated** continuous (e.g. **path spread**, **shadow price**, **congestion**); **separate** model for zero vs positive.
- **FTR**: Path spread / shadow → **two-part** or **quantile**; binding → **logit**; binding count → **Poisson/NB**.
- **Power**: LMP / load → **OLS** (or **WLS**, **quantile**); spike → **logit**; count → **Poisson/NB**; congestion → **two-part**.
- **Gas**: Price / demand / basis → **OLS** or **quantile**; **seasonality** and **HDD/CDD**; **two-part** for **zero-inflated** basis.
- **Diagnostics**: Linearity, homoskedasticity, normality, autocorrelation, exogeneity; **remedy** with **robust** SEs, **WLS**, **quantile**, **lagged** vars, or **different** model family.
