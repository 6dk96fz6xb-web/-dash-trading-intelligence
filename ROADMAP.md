# Dash roadmap

## Phase 0 — Foundation

- Define the post-earnings momentum hypothesis.
- Document liquidity, privacy, and evidence standards.
- Establish a transparent initial scoring model.
- Choose an open-source license.
- Add issue and pull-request templates.

## Phase 1 — Data model

Create normalized schemas for:

- Earnings calendar and BMO/AMC timing.
- Consensus and reported revenue/EPS.
- Forward guidance.
- Price, volume, spread, and market context.
- Prior earnings reactions.
- Sources, timestamps, and confidence.

Deliverable: versioned sample data using synthetic or freely redistributable information only.

## Phase 2 — Research pipeline

- Ingest primary earnings releases and filings.
- Calculate surprises without near-zero denominator errors.
- Measure BMO and AMC reaction windows correctly.
- Detect missing, stale, conflicting, or anomalous data.
- Produce a reproducible daily candidate table.

Deliverable: command-line research report with tests.

## Phase 3 — Backtesting

- Define the investable universe without survivorship bias.
- Model opening gaps, slippage, spreads, fees, and halts.
- Separate training, validation, and out-of-sample periods.
- Test one-session and two-session holding rules.
- Compare the scoring model against simple baselines.
- Report results across bull, bear, high-rate, and high-volatility regimes.

Deliverable: reproducible notebook and machine-readable results.

## Phase 4 — Dashboard

- Earnings calendar.
- ENTER/WATCH/AVOID table with score breakdown.
- Evidence and source panel.
- Prior-reaction visualization.
- Market-context panel.
- Data freshness and uncertainty indicators.

Deliverable: read-only local web dashboard.

## Phase 5 — Community validation

- Publish methodology changes through pull requests.
- Track proposed ideas as testable hypotheses.
- Require evidence for scoring changes.
- Maintain a changelog and versioned model cards.
- Invite independent reproduction of backtests.

## Not currently in scope

- Live trade execution.
- Brokerage credential storage.
- Copy trading.
- Guaranteed-return claims.
- Personalized portfolio publication.
