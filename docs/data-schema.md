# Dash v0.1 CSV schema

Dash v0.1 accepts one candidate per CSV row. The input represents completed research; v0.1 does not automatically fetch earnings or market data.

## Identity and timing

| Field | Type | Requirement |
|---|---|---|
| `ticker` | Text | Required; normalized to uppercase |
| `company` | Text | Required |
| `report_timing` | Text | `AMC`, `BMO`, or `UNKNOWN` |
| `data_timestamp` | ISO-8601 timestamp | Required; include the timezone when possible |

## Hard-gate inputs

| Field | Type | Default rule |
|---|---|---|
| `primary_source_verified` | Boolean | Must be true; otherwise `DATA INCOMPLETE` |
| `market_data_current` | Boolean | Must be true; otherwise `DATA INCOMPLETE` |
| `avg_daily_dollar_volume` | Number in USD | At least $20 million |
| `spread_pct` | Percentage number | No more than 0.75 |
| `market_cap_millions` | Number in USD millions | At least 300 |
| `unresolved_halt` | Boolean | Must be false |
| `quote_anomaly` | Boolean | Must be false |

The dashboard allows the three numeric liquidity thresholds to be changed. Thresholds are provisional and must be validated before live use.

Accepted Boolean values are `true/false`, `yes/no`, `y/n`, and `1/0`.

## Score inputs

| Field | Allowed range | Weight |
|---|---:|---:|
| `guidance_score` | 0–25 | 25% |
| `results_score` | 0–20 | 20% |
| `market_confirmation_score` | 0–20 | 20% |
| `liquidity_score` | 0–15 | 15% |
| `business_quality_score` | 0–10 | 10% |
| `context_score` | 0–10 | 10% |

## Evidence fields

The fields `bull_case`, `bear_case`, `invalidation_condition`, and `sources` are required. They make the output auditable and discourage unsupported scores.

## Decision order

1. Missing primary-source verification or stale market data → `DATA INCOMPLETE`.
2. Any other hard-gate failure → `AVOID`, regardless of total score.
3. Passing score of 80–100 → `ENTER`.
4. Passing score of 65–79 → `WATCH`.
5. Passing score below 65 → `AVOID`.

See [`data/sample_earnings.csv`](../data/sample_earnings.csv) for synthetic examples.
