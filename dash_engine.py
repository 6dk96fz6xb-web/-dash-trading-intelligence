"""Core scoring engine for Dash Trading Intelligence v0.1.

The engine is deliberately dependency-free.  It accepts explicit research
inputs, enforces hard data/liquidity gates, and produces an auditable score.
It does not fetch market data or place trades.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


COMPONENT_LIMITS = {
    "guidance_score": 25.0,
    "results_score": 20.0,
    "market_confirmation_score": 20.0,
    "liquidity_score": 15.0,
    "business_quality_score": 10.0,
    "context_score": 10.0,
}

REQUIRED_TEXT_FIELDS = (
    "ticker",
    "company",
    "report_timing",
    "data_timestamp",
    "bull_case",
    "bear_case",
    "invalidation_condition",
    "sources",
)


@dataclass(frozen=True)
class Thresholds:
    """Configurable hard gates for the initial liquid-stock universe."""

    min_daily_dollar_volume: float = 20_000_000.0
    max_spread_pct: float = 0.75
    min_market_cap_millions: float = 300.0


@dataclass(frozen=True)
class Candidate:
    ticker: str
    company: str
    report_timing: str
    data_timestamp: str
    primary_source_verified: bool
    market_data_current: bool
    avg_daily_dollar_volume: float
    spread_pct: float
    market_cap_millions: float
    unresolved_halt: bool
    quote_anomaly: bool
    guidance_score: float
    results_score: float
    market_confirmation_score: float
    liquidity_score: float
    business_quality_score: float
    context_score: float
    bull_case: str
    bear_case: str
    invalidation_condition: str
    sources: str


@dataclass(frozen=True)
class ScoreResult:
    ticker: str
    company: str
    score: float
    label: str
    gate_failures: tuple[str, ...]
    component_scores: dict[str, float]
    bull_case: str
    bear_case: str
    invalidation_condition: str
    sources: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["gate_failures"] = list(self.gate_failures)
        return payload


def _parse_bool(value: Any, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"{field_name} must be true or false")


def _parse_float(value: Any, field_name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if number != number or number in {float("inf"), float("-inf")}:
        raise ValueError(f"{field_name} must be a finite number")
    return number


def candidate_from_mapping(row: Mapping[str, Any]) -> Candidate:
    """Validate and normalize one dictionary-like candidate record."""

    missing = [name for name in REQUIRED_TEXT_FIELDS if not str(row.get(name, "")).strip()]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    timing = str(row["report_timing"]).strip().upper()
    if timing not in {"AMC", "BMO", "UNKNOWN"}:
        raise ValueError("report_timing must be AMC, BMO, or UNKNOWN")

    timestamp = str(row["data_timestamp"]).strip()
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("data_timestamp must use ISO-8601 format") from exc

    component_scores: dict[str, float] = {}
    for field_name, maximum in COMPONENT_LIMITS.items():
        score = _parse_float(row.get(field_name), field_name)
        if not 0 <= score <= maximum:
            raise ValueError(f"{field_name} must be between 0 and {maximum:g}")
        component_scores[field_name] = score

    numeric_fields = {
        "avg_daily_dollar_volume": _parse_float(
            row.get("avg_daily_dollar_volume"), "avg_daily_dollar_volume"
        ),
        "spread_pct": _parse_float(row.get("spread_pct"), "spread_pct"),
        "market_cap_millions": _parse_float(
            row.get("market_cap_millions"), "market_cap_millions"
        ),
    }
    if any(value < 0 for value in numeric_fields.values()):
        raise ValueError("liquidity and market-cap inputs cannot be negative")

    return Candidate(
        ticker=str(row["ticker"]).strip().upper(),
        company=str(row["company"]).strip(),
        report_timing=timing,
        data_timestamp=timestamp,
        primary_source_verified=_parse_bool(
            row.get("primary_source_verified"), "primary_source_verified"
        ),
        market_data_current=_parse_bool(
            row.get("market_data_current"), "market_data_current"
        ),
        unresolved_halt=_parse_bool(row.get("unresolved_halt"), "unresolved_halt"),
        quote_anomaly=_parse_bool(row.get("quote_anomaly"), "quote_anomaly"),
        **numeric_fields,
        **component_scores,
        bull_case=str(row["bull_case"]).strip(),
        bear_case=str(row["bear_case"]).strip(),
        invalidation_condition=str(row["invalidation_condition"]).strip(),
        sources=str(row["sources"]).strip(),
    )


def _gate_failures(candidate: Candidate, thresholds: Thresholds) -> tuple[str, ...]:
    failures: list[str] = []
    if not candidate.primary_source_verified:
        failures.append("Primary earnings source is not verified")
    if not candidate.market_data_current:
        failures.append("Market data is stale or incomplete")
    if candidate.avg_daily_dollar_volume < thresholds.min_daily_dollar_volume:
        failures.append("Average daily dollar volume is below the configured minimum")
    if candidate.spread_pct > thresholds.max_spread_pct:
        failures.append("Bid-ask spread is above the configured maximum")
    if candidate.market_cap_millions < thresholds.min_market_cap_millions:
        failures.append("Market capitalization is below the configured minimum")
    if candidate.unresolved_halt:
        failures.append("The symbol has an unresolved trading halt")
    if candidate.quote_anomaly:
        failures.append("The quote is anomalous or unreliable")
    return tuple(failures)


def score_candidate(
    candidate: Candidate, thresholds: Thresholds | None = None
) -> ScoreResult:
    """Score a candidate and apply hard gates before assigning a label."""

    thresholds = thresholds or Thresholds()
    components = {
        field_name: getattr(candidate, field_name) for field_name in COMPONENT_LIMITS
    }
    total = round(sum(components.values()), 1)
    failures = _gate_failures(candidate, thresholds)

    incomplete = any(
        message.startswith("Primary earnings source")
        or message.startswith("Market data")
        for message in failures
    )
    if incomplete:
        label = "DATA INCOMPLETE"
    elif failures:
        label = "AVOID"
    elif total >= 80:
        label = "ENTER"
    elif total >= 65:
        label = "WATCH"
    else:
        label = "AVOID"

    return ScoreResult(
        ticker=candidate.ticker,
        company=candidate.company,
        score=total,
        label=label,
        gate_failures=failures,
        component_scores=components,
        bull_case=candidate.bull_case,
        bear_case=candidate.bear_case,
        invalidation_condition=candidate.invalidation_condition,
        sources=candidate.sources,
    )


def load_candidates(path_or_file: str | Path | Any) -> list[Candidate]:
    """Load validated candidates from a CSV path or text file object."""

    should_close = False
    if hasattr(path_or_file, "read"):
        handle = path_or_file
    else:
        handle = Path(path_or_file).open("r", encoding="utf-8", newline="")
        should_close = True
    try:
        return [candidate_from_mapping(row) for row in csv.DictReader(handle)]
    finally:
        if should_close:
            handle.close()


def score_many(
    candidates: Iterable[Candidate], thresholds: Thresholds | None = None
) -> list[ScoreResult]:
    return sorted(
        (score_candidate(candidate, thresholds) for candidate in candidates),
        key=lambda result: result.score,
        reverse=True,
    )


def _print_table(results: list[ScoreResult]) -> None:
    headers = ("Ticker", "Score", "Decision", "Gate failures")
    rows = [
        (
            result.ticker,
            f"{result.score:.1f}",
            result.label,
            "; ".join(result.gate_failures) or "None",
        )
        for result in results
    ]
    widths = [
        max([len(headers[index]), *(len(row[index]) for row in rows)])
        for index in range(len(headers))
    ]
    print("  ".join(header.ljust(widths[i]) for i, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[i]) for i, value in enumerate(row)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Score Dash earnings candidates")
    parser.add_argument("csv_path", help="Path to the Dash candidate CSV")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    results = score_many(load_candidates(args.csv_path))
    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2))
    else:
        _print_table(results)


if __name__ == "__main__":
    main()
