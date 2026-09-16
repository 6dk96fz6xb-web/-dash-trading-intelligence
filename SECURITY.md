# Security and privacy policy

## Never commit secrets

Do not commit:

- Brokerage credentials or account identifiers.
- API keys, access tokens, cookies, or session data.
- Database passwords or private connection strings.
- Paid-data credentials or files whose license forbids redistribution.
- Personal portfolio, statement, or transaction data.

Use local environment variables or a dedicated secret manager. Keep a redacted `.env.example` only when the application needs documented variable names.

## Reporting a vulnerability

Do not open a public issue containing an exploitable vulnerability, active credential, or personal financial information. Contact the repository owner privately through an appropriate GitHub-supported channel.

If a secret is exposed:

1. Revoke and rotate it immediately.
2. Remove it from current files.
3. Review repository history and access logs.
4. Assume deletion from the latest commit alone is insufficient.
5. Notify any affected provider or person.

## Trading safety

Dash must default to research-only behavior. Any future broker integration must:

- Be isolated from the analysis layer.
- Use paper trading by default.
- Require explicit confirmation before live-order capability.
- Apply position, loss, and order-size limits.
- Produce an auditable event log.
- Never expose credentials in logs, errors, screenshots, or client-side code.
