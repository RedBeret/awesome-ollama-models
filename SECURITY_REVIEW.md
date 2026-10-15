# Security and reliability review

Scope: Python catalog tooling, the GitHub issue-maintenance script, workflows and documentation introduced by this modernization. No web framework or service is deployed. Review date: October 14, 2026.

## Findings

No confirmed high/critical vulnerability remained after the local review and regression checks. This is a focused source/test review, not an external penetration test. Model recommendations and source claims are not security guarantees.

## Safeguards reviewed

- No API credentials are needed by catalog validation or public polling. Cloud examples reference an environment variable; no key value is committed. Checkout does not persist GitHub credentials.
- [`decode_json` (line 61)](scripts/catalog.py#L61) rejects duplicate JSON keys and non-finite constants. [`validate_catalog` (line 100)](scripts/catalog.py#L100) checks types, official HTTPS URLs, dates, statuses, tags, identifiers, capabilities and pricing. Unknown fields fail rather than being silently ignored. Markdown rendering escapes untrusted text/HTML.
- [`fetch_live` (line 302)](scripts/catalog.py#L302) uses TLS certificate validation, a fixed host/path, no credential header and no redirects. Connection and response timeouts are separate. Reads are capped at 2 MiB, listings at 1,000 entries, attempts at three, and backoff/Retry-After at 60 seconds. The workflow adds a ten-minute job bound. OS DNS resolution and socket timeouts are not a hard wall-clock deadline for every possible slow-peer behavior; the job bound limits monitoring runtime.
- HTTP 401/403 and other permanent failures stop without retry. Only 429 and selected transient 5xx retry, together with network exceptions. Certificate validation failure stops immediately. Malformed or empty responses fail closed and cannot become an all-models-removed report.
- A failed polling command removes previous report files and exits nonzero. Subsequent report/issue steps run only on success. Drift data never edits reviewed catalog data or opens model-update PRs automatically.
- Validation has `contents: read` only, and runs no PR secrets or `pull_request_target` code. Monitoring has only `contents: read` plus `issues: write`, runs reviewed default-branch code, and uses GitHub's short-lived job token.
- Official actions are pinned to full upstream commit SHAs, with monthly Dependabot proposals. No Python runtime dependency chain was introduced. The small issue script uses Node built-ins and the pinned GitHub action client.
- Identifier validation prevents report text from becoming arbitrary Markdown/mentions. Report size and digest are checked before GitHub writes. Reports are read from files, not interpolated into shell commands or expressions.
- Workflow concurrency serializes monitoring runs. Only the exact bot-owned marker/title issue is maintained; unchanged changes cause no write, resolved drift closes it, and multiple matching issues fail for human cleanup. A process failure after GitHub accepts issue creation can be reconciled by the next run's lookup.
- Inference examples use timeouts and document auth/rate errors, idempotency, cloud privacy and fallback rules. Running local inference is not permission to expose a local server publicly.

## Residual limitations

1. Public listing presence is not proof of account access. Pricing/metadata/retirement notices need manual review; identifier polling cannot validate them.
2. GitHub Actions and issue writes require repository policy to permit them. The schedule becomes active only on the default branch, and GitHub may suspend inactive schedules.
3. Inference examples were checked against official docs but not executed with a paid account. Tool requests require separate application authorization and validation.

Regression tests cover invalid schemas, duplicate keys/tags, Markdown escaping, malformed/oversized responses, empty listings, auth failures, retry bounds, stale reports and issue deduplication. See the PR/delivery for commands actually run and their results.
