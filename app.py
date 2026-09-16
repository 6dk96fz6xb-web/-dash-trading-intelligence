"""Streamlit interface for Dash Trading Intelligence v0.1."""

from __future__ import annotations

import io
from pathlib import Path

import streamlit as st

from dash_engine import Thresholds, load_candidates, score_many


APP_ROOT = Path(__file__).parent
SAMPLE_PATH = APP_ROOT / "data" / "sample_earnings.csv"

st.set_page_config(page_title="Dash Trading Intelligence", page_icon="📊", layout="wide")

st.title("Dash Trading Intelligence")
st.caption("Research-only v0.1 · Post-earnings momentum · No trade execution")

with st.sidebar:
    st.header("Hard liquidity gates")
    min_volume_millions = st.number_input(
        "Minimum average daily dollar volume ($M)",
        min_value=1.0,
        value=20.0,
        step=5.0,
    )
    max_spread_pct = st.number_input(
        "Maximum bid-ask spread (%)",
        min_value=0.05,
        value=0.75,
        step=0.05,
    )
    min_market_cap = st.number_input(
        "Minimum market cap ($M)",
        min_value=1.0,
        value=300.0,
        step=50.0,
    )
    st.divider()
    st.warning("A high score never overrides a failed data, liquidity, halt, or quote gate.")

uploaded = st.file_uploader("Upload a Dash-format CSV", type="csv")

try:
    if uploaded is None:
        candidates = load_candidates(SAMPLE_PATH)
        st.info("Showing synthetic sample data. Upload a CSV to assess your own research inputs.")
    else:
        text = uploaded.getvalue().decode("utf-8-sig")
        candidates = load_candidates(io.StringIO(text))

    thresholds = Thresholds(
        min_daily_dollar_volume=min_volume_millions * 1_000_000,
        max_spread_pct=max_spread_pct,
        min_market_cap_millions=min_market_cap,
    )
    results = score_many(candidates, thresholds)
except (UnicodeDecodeError, ValueError) as exc:
    st.error(f"Could not score this file: {exc}")
    st.stop()

counts = {label: sum(result.label == label for result in results) for label in (
    "ENTER", "WATCH", "AVOID", "DATA INCOMPLETE"
)}
columns = st.columns(4)
for column, label in zip(columns, counts):
    column.metric(label, counts[label])

st.subheader("Ranked candidates")
summary_rows = [
    {
        "Ticker": result.ticker,
        "Company": result.company,
        "Score": result.score,
        "Decision": result.label,
        "Hard-gate result": "; ".join(result.gate_failures) or "Passed",
    }
    for result in results
]
st.dataframe(summary_rows, use_container_width=True, hide_index=True)

if not results:
    st.warning("No candidates were found in the uploaded file.")
    st.stop()

selected_ticker = st.selectbox("Inspect a candidate", [result.ticker for result in results])
selected = next(result for result in results if result.ticker == selected_ticker)

left, right = st.columns([1, 1])
with left:
    st.subheader(f"{selected.ticker} · {selected.label} · {selected.score:.1f}/100")
    component_labels = {
        "guidance_score": "Forward guidance",
        "results_score": "Reported results",
        "market_confirmation_score": "Market confirmation",
        "liquidity_score": "Liquidity and execution",
        "business_quality_score": "Business quality",
        "context_score": "Context and technical setup",
    }
    st.dataframe(
        [
            {"Component": component_labels[name], "Points": points}
            for name, points in selected.component_scores.items()
        ],
        use_container_width=True,
        hide_index=True,
    )
with right:
    st.subheader("Decision evidence")
    if selected.gate_failures:
        st.error("\n".join(f"• {message}" for message in selected.gate_failures))
    else:
        st.success("All configured hard gates passed.")
    st.markdown(f"**Bull case:** {selected.bull_case}")
    st.markdown(f"**Bear case:** {selected.bear_case}")
    st.markdown(f"**Invalidation:** {selected.invalidation_condition}")
    st.markdown(f"**Sources:** {selected.sources}")

st.divider()
st.caption(
    "Dash v0.1 uses analyst-entered component scores. Scores and thresholds are provisional, "
    "unvalidated, and for research only. Verify every primary source and timestamp."
)
