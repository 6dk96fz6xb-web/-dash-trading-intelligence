import csv
import io
import unittest

from dash_engine import (
    Candidate,
    _print_table,
    candidate_from_mapping,
    load_candidates,
    score_candidate,
)


def make_candidate(**overrides):
    values = {
        "ticker": "TEST",
        "company": "Synthetic Test Company",
        "report_timing": "AMC",
        "data_timestamp": "2026-09-16T20:15:00Z",
        "primary_source_verified": True,
        "market_data_current": True,
        "avg_daily_dollar_volume": 100_000_000,
        "spread_pct": 0.10,
        "market_cap_millions": 5_000,
        "unresolved_halt": False,
        "quote_anomaly": False,
        "guidance_score": 23,
        "results_score": 18,
        "market_confirmation_score": 18,
        "liquidity_score": 14,
        "business_quality_score": 8,
        "context_score": 7,
        "bull_case": "Synthetic evidence is favorable.",
        "bear_case": "The initial reaction could fade.",
        "invalidation_condition": "The move loses confirmation.",
        "sources": "Synthetic fixture",
    }
    values.update(overrides)
    return Candidate(**values)


class ScoreCandidateTests(unittest.TestCase):
    def test_enter_candidate(self):
        result = score_candidate(make_candidate())
        self.assertEqual(result.score, 88)
        self.assertEqual(result.label, "ENTER")
        self.assertEqual(result.gate_failures, ())

    def test_watch_candidate(self):
        result = score_candidate(
            make_candidate(guidance_score=18, market_confirmation_score=10)
        )
        self.assertEqual(result.score, 75)
        self.assertEqual(result.label, "WATCH")

    def test_low_score_is_avoid(self):
        result = score_candidate(
            make_candidate(
                guidance_score=10,
                results_score=10,
                market_confirmation_score=8,
                liquidity_score=10,
                business_quality_score=5,
                context_score=5,
            )
        )
        self.assertEqual(result.label, "AVOID")

    def test_liquidity_gate_overrides_high_score(self):
        result = score_candidate(make_candidate(avg_daily_dollar_volume=1_000_000))
        self.assertEqual(result.label, "AVOID")
        self.assertIn("dollar volume", result.gate_failures[0])

    def test_unverified_source_is_data_incomplete(self):
        result = score_candidate(make_candidate(primary_source_verified=False))
        self.assertEqual(result.label, "DATA INCOMPLETE")


class ValidationTests(unittest.TestCase):
    def test_component_above_maximum_is_rejected(self):
        values = make_candidate().__dict__.copy()
        values["guidance_score"] = 26
        with self.assertRaisesRegex(ValueError, "guidance_score"):
            candidate_from_mapping(values)

    def test_invalid_boolean_is_rejected(self):
        values = make_candidate().__dict__.copy()
        values["quote_anomaly"] = "maybe"
        with self.assertRaisesRegex(ValueError, "quote_anomaly"):
            candidate_from_mapping(values)

    def test_csv_loader(self):
        values = make_candidate().__dict__.copy()
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=values.keys())
        writer.writeheader()
        writer.writerow(values)
        stream.seek(0)
        loaded = load_candidates(stream)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].ticker, "TEST")

    def test_empty_table_does_not_fail(self):
        _print_table([])


if __name__ == "__main__":
    unittest.main()
