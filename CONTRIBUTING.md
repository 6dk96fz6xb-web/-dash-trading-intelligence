# Contributing to Dash

Thank you for helping improve Dash. Contributions may include bug reports, data-quality fixes, research proposals, tests, documentation, or code.

## Before proposing a strategy change

Please describe:

1. The exact hypothesis.
2. Why it might produce an edge.
3. The data required to test it.
4. Possible sources of bias or leakage.
5. How success and failure will be measured.
6. Whether the idea changes risk, holding period, or liquidity requirements.

## Pull requests

A useful pull request should:

- Have a focused purpose and clear description.
- Include tests for new calculations.
- Cite data definitions and source assumptions.
- Preserve timestamps and BMO/AMC logic.
- Avoid look-ahead and survivorship bias.
- Include transaction-cost assumptions for performance claims.
- Avoid committing generated secrets, paid datasets, or personal financial information.

Maintainers may request changes or decline proposals that lack reproducible evidence.

## Issues

Use issues for:

- Missing or incorrect earnings events.
- Scoring-model proposals.
- Data-source discussions.
- Dashboard ideas.
- Reproducible bugs.

Do not post brokerage screenshots, account numbers, API keys, private statements, or personally identifying portfolio information.

## Code style

Until a language and application architecture are selected:

- Favor small, testable functions.
- Use explicit names and documented units.
- Keep data acquisition separate from scoring and presentation.
- Make thresholds configurable.
- Fail visibly on stale or incomplete data.
- Record source and timestamp metadata.

## Financial claims

Do not describe backtested performance as guaranteed or expected live performance. Clearly label hypothetical results and disclose assumptions, limitations, and conflicts of interest.
