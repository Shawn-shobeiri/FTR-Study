# Quantitative Researcher — Knowledge & Skills Expected

**Perspective:** Chief Risk Officer, energy commodity prop shop (FTR, power, gas).

---

## 1. Domain knowledge

### Power & FTR/CRR
- **ISO market design:** Day-ahead vs real-time; LMP formation; congestion component and its link to constraint shadow prices.
- **FTR/CRR mechanics:** Obligation vs option; path (source–sink); payoff = quantity × spread (reference price); auction design and allocation.
- **Transmission & constraints:** Binding constraints; thermal/interface limits; PTDFs and LODFs; how outages and topology change binding and congestion.
- **Production cost / dispatch:** Security-constrained economic dispatch (SCED); unit commitment (UC); use of PCM output (shadow prices, binding) for fair value and scenario analysis.
- **Relevant ISOs:** ERCOT, CAISO (and ideally PJM, SPP, MISO) — structure, data sources, auction calendars.

### Gas
- **Physical vs financial:** Basis, hub pricing; pipeline capacity and nominations; storage optionality.
- **Term structure:** Forward curves; seasonal patterns; curve-building and no-arbitrage constraints.
- **Link to power:** Gas–power spread; gas as marginal fuel; impact of gas price/availability on LMPs and congestion.

### Commodity quant foundations
- **Term structure:** Forward curves; contango/backwardation; calendar spreads; curve-building methods (interpolation, splines, no-arbitrage).
- **Valuation:** Mark-to-market of forwards, options, and path-based products; discounting and risk-neutral vs real-world measures where relevant.

---

## 2. Quantitative & analytical skills

### Math & statistics
- **Probability & stats:** Distributions, conditioning, expectations; estimation (MLE, method of moments); hypothesis testing; correlation and dependence (including tail dependence for stress).
- **Time series:** Stationarity; autocorrelation; seasonality; simple forecasting (ARIMA, regression on fundamentals); volatility modeling where applicable.
- **Optimization:** Linear programming (LP); familiarity with security-constrained OPF/economic dispatch; constraint handling; sensitivity (duals/shadow prices).
- **Numerical methods:** Root-finding; numerical integration; basic Monte Carlo; stability and numerical robustness.

### Risk & valuation
- **Risk metrics:** VaR (historical, parametric, Monte Carlo); expected shortfall (ES); stress testing; scenario design (outages, demand, fuel, weather).
- **P&L attribution:** Decomposing P&L into curve, spread, vol, and residual; explaining mark-to-market moves.
- **Exposure aggregation:** Position limits; factor/sensitivity-based risk (e.g. constraint-level, path-level); concentration risk.

### Modeling
- **Stochastic models:** Mean-reversion; seasonal components; jump-diffusion where relevant; calibration to market or historical data.
- **Scenario generation:** Plausible paths for LMPs, congestion, outages; coherent scenarios for stress and capital.
- **Backtesting:** Out-of-sample tests; comparison of model vs realized; clear documentation of assumptions and limitations.

---

## 3. Data & implementation

### Data
- **Data sourcing:** ISO publications (LMPs, binding constraints, shadow prices, outages); broker/vendor data (Enverus, Yes Energy, Panorama, etc.); mapping (nodes, zones, paths, constraints).
- **Data quality:** Missing data; outliers; timing and alignment (e.g. delivery period, time zone); reconciliation with exchange/clearing.
- **Data pipelines:** Reproducible ingestion; versioning; audit trail for risk and compliance.

### Programming & tools
- **Programming:** Strong fluency in at least one of Python, R, or C++; readable, maintainable code; use of version control (e.g. Git).
- **Numerical/scientific stack:** NumPy/SciPy, pandas (or R equivalents); optimization (e.g. SciPy, Gurobi/CPLEX if LP used); optional: probabilistic programming (Stan, PyMC).
- **Reproducibility:** Scripts over one-off analysis; documentation; ability to hand off and explain models to risk and trading.

### Optional but valued
- **Power-flow / OPF:** DC power flow; PTDF/LODF computation; running or interfacing with PCM tools (e.g. Dayzer, Power World, commercial PCMs).
- **Machine learning:** Use with clear guardrails: feature design, overfitting, interpretability, and how models feed into risk limits and stress.

---

## 4. Risk culture & communication

- **Model risk awareness:** Knowing what a model assumes; when it breaks; communicating uncertainty to trading and senior risk.
- **Documentation:** Model docs; assumption logs; change control so risk can validate and audit.
- **Communication:** Explaining methodology and results to non-quants (traders, CRO, compliance); written and verbal.
- **Ethics & conduct:** Integrity of data and models; no gaming of risk metrics; escalation when limits or assumptions are breached.

---

## 5. What the CRO cares about

- **Robustness:** Models and curves that don’t introduce arbitrage or nonsensical risk numbers; stress tests that reflect real market and operational events (outages, extreme weather, demand spikes).
- **Consistency:** One source of truth for curves and risk; alignment between valuation (trading) and risk (VaR, limits, capital).
- **Traceability:** Clear lineage from data → model → risk metric; ability to explain large P&L or VaR moves.
- **Independent challenge:** Quants who can challenge trader assumptions and existing models; healthy skepticism without blocking the business.
- **FTR-specific:** Understanding path payoffs, constraint binding, and outage impact so that FTR risk (exposure to congestion and topology) is measured and limited properly.

---

## 6. Summary checklist (for hiring)

| Area | Expectation |
|------|-------------|
| **Power / FTR** | LMP, congestion, constraints, PTDF/LODF, shadow prices, PCM, auction flow |
| **Gas** | Basis, term structure, link to power |
| **Curves** | Term structure, no-arbitrage, curve-building methods |
| **Math / stats** | Probability, time series, optimization, numerical methods |
| **Risk** | VaR, ES, stress, scenarios, P&L attribution, exposure |
| **Data** | Sourcing, quality, pipelines, mapping |
| **Code** | Python/R/C++, scientific stack, reproducibility, version control |
| **Risk culture** | Model risk, documentation, communication, ethics |
