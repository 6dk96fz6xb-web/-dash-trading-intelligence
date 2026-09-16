# Dash Trading Intelligence

Dash is an open-source research tool for ranking short-term, post-earnings momentum candidates in liquid U.S. stocks.

It converts explicit earnings research into an auditable decision:

- **ENTER** — strong score, verified data, and every hard gate passed.
- **WATCH** — constructive score but not strong enough for entry.
- **AVOID** — insufficient score or a liquidity/execution gate failed.
- **DATA INCOMPLETE** — the primary earnings source is unverified or market data is stale.

Dash is research software. It does **not** fetch live data, connect to a broker, place trades, or provide financial advice.

## Dash v0.1

The first working release includes:

- A dependency-free Python scoring engine.
- A validated CSV input format.
- A command-line report with optional JSON output.
- A read-only Streamlit dashboard.
- Configurable minimum dollar volume, maximum spread, and minimum market cap.
- Synthetic examples showing that hard gates override headline scores.
- Automated unit tests and GitHub Actions.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/6dk96fz6xb-web/dash-trading-intelligence.git
cd dash-trading-intelligence
python -m venv .venv
```

Activate the virtual environment, then install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run the scoring engine without the dashboard:

```bash
python dash_engine.py data/sample_earnings.csv
python dash_engine.py data/sample_earnings.csv --json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Input data

Use [`data/sample_earnings.csv`](data/sample_earnings.csv) as the template. Every row needs:

- Company identity, report timing, and ISO-8601 timestamp.
- Primary-source and market-data verification flags.
- Dollar volume, spread, market cap, halt, and quote-quality inputs.
- Six component scores totaling a maximum of 100.
- Bull case, bear case, invalidation condition, and sources.

The complete field definitions are in the [v0.1 data schema](docs/data-schema.md).

## Score model

| Component | Maximum points |
|---|---:|
| Forward guidance | 25 |
| Reported results | 20 |
| Market confirmation | 20 |
| Liquidity and execution | 15 |
| Business quality | 10 |
| Context and technical setup | 10 |

The score is evaluated only after hard gates. A thinly traded candidate can score 98/100 and still be labeled `AVOID`.

## Project documentation

- [Trading hypothesis and safeguards](docs/strategy.md)
- [Scoring framework](docs/scoring.md)
- [CSV data schema](docs/data-schema.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Security and privacy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Privacy boundary

Never commit personal holdings, capital, entry prices, broker statements, account identifiers, credentials, tokens, paid datasets, or private trading history. Local private paths and common credential files are excluded through `.gitignore`.

## Status and limitations

Dash v0.1 uses manually researched inputs and analyst-assigned component scores. The scoring weights, thresholds, and one-to-two-session momentum hypothesis are provisional. They have not yet been validated through a bias-controlled, out-of-sample backtest.

## License

MIT. See [LICENSE](LICENSE).

## Disclaimer

This project is for education and research only. Markets involve substantial risk. Outputs may be incomplete, delayed, or incorrect. Verify every source and make independent decisions.
