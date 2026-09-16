# Dash Trading Intelligence

Dash is an open-source research framework for finding short-term, post-earnings momentum opportunities in liquid U.S. stocks.

Its purpose is to turn an earnings release into a transparent decision:

- **ENTER** — strong report, strong guidance, confirmed market reaction, and acceptable liquidity/risk.
- **WATCH** — promising setup that still needs confirmation.
- **AVOID** — weak guidance, low liquidity, contradictory price action, excessive valuation risk, or an unfavorable market backdrop.

Dash is designed for research and decision support. It does **not** place trades and is not financial advice.

## Core philosophy

A headline EPS beat is not enough. Dash weighs:

1. Revenue and EPS versus expectations.
2. Forward guidance and management commentary.
3. Margins, cash generation, and balance-sheet quality.
4. After-hours or premarket price reaction.
5. Trading volume, spread, market capitalization, and liquidity.
6. The stock's reaction to previous earnings reports.
7. Sector performance and the broader macro environment.
8. Confirmation after the market opens.

The initial trading hypothesis is that a strong earnings report followed by confirmed price-and-volume momentum may continue for one or two sessions. That hypothesis must be tested rather than assumed.

## Repository structure

- [Strategy](docs/strategy.md) — the trading hypothesis, process, and safeguards.
- [Scoring framework](docs/scoring.md) — a transparent 100-point model.
- [Roadmap](ROADMAP.md) — proposed development stages.
- [Contributing](CONTRIBUTING.md) — how to suggest ideas or submit improvements.
- [Security](SECURITY.md) — rules for credentials and sensitive financial information.

## Privacy boundary

This public repository must never contain:

- Personal holdings, capital, entry prices, or broker statements.
- Brokerage usernames, passwords, account numbers, cookies, or tokens.
- API keys or paid-data credentials.
- Private trading history unless fully anonymized and intentionally contributed.
- Any mechanism that can place a live order without an explicit, separately reviewed design.

Use environment variables for credentials and keep local private files in ignored directories.

## Status

Dash is at the **foundation/design stage**. The scoring weights and trading hypothesis have not yet been validated through robust out-of-sample testing.

## Contributions

Ideas, corrections, research, tests, and pull requests are welcome. Please explain the evidence behind strategy changes and disclose assumptions, data sources, transaction costs, and possible biases.

## Disclaimer

This software and its documentation are for educational and research purposes only. Markets involve substantial risk. Outputs may be incomplete, delayed, or incorrect. Always verify source data and make independent decisions.
