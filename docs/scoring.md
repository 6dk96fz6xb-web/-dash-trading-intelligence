# Dash scoring framework

The initial Dash score is a transparent research model totaling 100 points. It is intentionally simple enough to audit and revise.

A high score does not override a hard exclusion.

## Hard gates

Before scoring, verify:

- Reliable primary-source earnings data is available.
- Market data is timestamped and sufficiently current.
- Dollar volume and spread meet configurable liquidity standards.
- The symbol is not subject to an unresolved halt or obvious quote anomaly.
- No credential, private portfolio data, or non-public information is used.

If a gate fails, label the candidate **AVOID** or **DATA INCOMPLETE**.

## Score components

| Component | Points | What to assess |
|---|---:|---|
| Forward guidance | 25 | Revenue/EPS outlook versus consensus, tone, visibility, and raised/maintained/cut guidance |
| Reported results | 20 | Revenue/EPS surprise, growth quality, margins, and material one-time effects |
| Market confirmation | 20 | Sustained price reaction, relative volume, spread quality, and resistance to fading |
| Liquidity and execution | 15 | Dollar volume, market capitalization, spread, depth, and halt risk |
| Business quality | 10 | Cash generation, cash/debt position, recurring demand, and customer concentration |
| Context and technical setup | 10 | Sector/index backdrop, macro risk, prior earnings behavior, and nearby technical levels |
| **Total** | **100** | |

## Initial interpretation

| Score | Label | Interpretation |
|---:|---|---|
| 80–100 | ENTER candidate | Strong evidence, subject to confirmation and defined risk |
| 65–79 | WATCH | Constructive but incomplete or not yet confirmed |
| Below 65 | AVOID | Insufficient edge or unfavorable risk/reward |

These thresholds are provisional. Backtesting may show that different weights, nonlinear rules, or no composite score performs better.

## Required output fields

Every assessed ticker should display:

- Report timing and data timestamp.
- Actual versus expected revenue and EPS.
- Guidance assessment.
- Initial move and current move.
- Volume/liquidity assessment.
- Dash score and component breakdown.
- Decision label.
- Bull case, bear case, and invalidation condition.
- Missing or conflicting information.
- Sources.

## Testing standards

Any proposed scoring change should report:

- Dataset and date range.
- Universe definition.
- BMO/AMC reaction-window logic.
- Transaction costs and slippage.
- Train, validation, and out-of-sample periods.
- Win rate, average return, median return, drawdown, and risk-adjusted metrics.
- Performance by market regime and liquidity group.
- Sensitivity to alternative thresholds.

Do not optimize weights on the full dataset and then present the same dataset as independent evidence.
