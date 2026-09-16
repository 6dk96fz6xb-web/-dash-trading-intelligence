# Dash strategy

## Objective

Identify liquid U.S. equities whose earnings releases create a credible short-term momentum opportunity. The normal research horizon is the first one or two trading sessions after the report.

Dash is a decision-support framework, not an autonomous trading system.

## Research sequence

### 1. Build the earnings universe

For every reporting company, record:

- Ticker, company, sector, market capitalization, and reporting time.
- Before market open (BMO), after market close (AMC), or timing unknown.
- Consensus revenue and adjusted EPS.
- Recent average volume and typical bid-ask spread.
- Scheduled macro events that could distort the reaction.

### 2. Apply hard liquidity gates

Exclude or flag companies with:

- Very low dollar volume or abnormally wide spreads.
- Micro-cap characteristics, unreliable quotes, or frequent trading halts.
- No dependable earnings source.
- A price move driven mainly by promotion, rumor, or a single unverified post.

Exact thresholds should be configurable and validated with data. Dash should favor execution quality over spectacular percentage moves.

### 3. Read the complete report

Capture:

- Revenue and EPS results versus consensus.
- Organic growth or other relevant operating growth.
- Forward revenue/EPS guidance versus expectations.
- Gross and operating margins.
- Free cash flow, cash balance, and material debt changes.
- Segment or geographic drivers.
- Management commentary and disclosed risks.
- One-time accounting effects.

A positive headline with weak guidance is not automatically bullish.

### 4. Measure market confirmation

For an AMC report, measure the after-hours reaction and verify it again in premarket and after the next regular session opens. For a BMO report, use premarket and regular-session confirmation.

Record:

- Price reaction from the last unaffected regular close.
- Dollar volume and volume relative to an appropriate baseline.
- Spread and quote quality.
- Whether the move holds, strengthens, or fades.
- Sector ETF and index movement over the same interval.

### 5. Compare history

Review at least the recent earnings reactions when data permits:

- Initial after-hours or premarket move.
- Opening gap.
- First-session high, low, close, and fade.
- Second-session continuation or reversal.
- Whether guidance or macro conditions explained the outcome.

### 6. Assign a decision

- **ENTER:** clears all hard gates, scores strongly, and confirms after the report.
- **WATCH:** report is constructive but confirmation, liquidity, or context is incomplete.
- **AVOID:** fails a hard gate or presents an unfavorable risk/reward profile.

Every decision must show its evidence, uncertainty, data timestamp, and invalidation condition.

## Risk principles

- Never recommend a position solely because a stock has already risen sharply.
- Never treat after-hours percentage change without liquidity and spread context.
- Do not average down automatically.
- Separate signal quality from position sizing.
- Model slippage, gaps, fees, and incomplete fills in backtests.
- Avoid look-ahead bias and survivorship bias.
- Test on unseen periods and different market regimes.
- Treat backtest results as hypotheses, not promises.

## Information hierarchy

Prefer primary sources:

1. Company investor-relations release and regulatory filing.
2. Earnings call materials and transcript.
3. Exchange-quality market data.
4. Reputable secondary financial sources.
5. Social media only as a lead to verify, never as final evidence.

## Initial research hypothesis

A company may be a short-term momentum candidate when it delivers strong results and guidance, has sound liquidity and financial quality, and the market confirms the news with sustained price-and-volume strength.

This hypothesis remains unproven until the project completes reproducible, out-of-sample testing.
