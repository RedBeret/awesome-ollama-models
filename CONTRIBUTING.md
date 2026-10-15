# Contributing

Use Python 3.12+; no Python dependencies are required. Fork or branch from the current default branch (`init-project` at the October 14, 2026 audit). Do not push catalog changes directly to it.

## Update a model

1. Read the [official cloud listing](https://ollama.com/api/tags), the specific [model/tag page](https://ollama.com/library), [cloud docs](https://docs.ollama.com/cloud), and [pricing](https://ollama.com/pricing). A search-card summary is not enough to resolve variant-specific specs.
2. Edit `data/models.json`. `id` equals the exact direct API identifier for cloud entries, or the local tag for a local-only entry. Verify CLI cloud and local tags independently; do not derive aliases by string replacement.
3. Record `sources`, `verified_on`, documented use cases, and any disagreement in `notes`. Use null for unverified context, tools, thinking, local tags or prices; do not treat null as false/zero. Modalities must contain at least one verified input type. Add an entry only when at least one execution tag and input type are verified.
4. The strict schema is implemented by `validate_catalog` in `scripts/catalog.py`; all defined fields are required, including nullable fields. New fields require a schema/code/test change. Model identifiers and execution tags must be unique. Lifecycle values: `active`, `retiring`, `retired`, `unknown`; see [the policy](docs/LIFECYCLE.md).
5. Update the catalog-level verification date to cover the most recent entry date. Each entry retains its own verification date. Pricing has a separate source/date; update it only after checking the current rate.
6. Generate and validate documentation, then inspect the diff. Edit prose outside the README markers directly; never hand-edit `MODEL_CATALOG.md` or the marked table.

```bash
python scripts/catalog.py validate
python scripts/catalog.py generate
python scripts/catalog.py generate --check
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
git diff --check
```

For changes to issue maintenance, also run `node --test tests/test_drift_issue.cjs` with Node 22+. Tests mock network failures and GitHub writes; no API key or internet is needed. The captured `tests/fixtures/cloud-tags.json` is a dated test fixture, not the maintained catalog or a live entitlement check.

## Monitor drift

```bash
python scripts/catalog.py drift
```

This fetches only the fixed public Ollama endpoint. Exit 0 means a valid comparison was written, even when drift exists. Exit 1 means invalid local data or a monitoring error; no current drift report is available. Reports are ignored by Git and written to `reports/drift.json` and `reports/drift.md`.

Review additions/removals manually. Check tag aliases, dates, pricing, modalities and context before changing recommendations or lifecycle. The monitor never updates the catalog. It checks IDs only: metadata-only changes need periodic human review.

GitHub monitoring is enabled after merge into the default branch. The schedule is Monday 09:23 UTC, and manual runs are restricted to that branch. The job uses `contents: read` and `issues: write`; no Ollama secret is needed for the public listing. Repository Actions policy must permit the SHA-pinned official actions. Report network/auth/schema errors via the failed run; do not create a removal issue from a failed poll. GitHub may disable inactive scheduled workflows; check the Actions page periodically.

## Pull requests

Describe what changed, link official evidence, list uncertainty, include verification dates and actual test results. Flag plan/privacy/license changes explicitly. Editorial recommendations must remain separate from source facts. Do not invent benchmarks or guaranteed free access. Human review is required before merging.

Official actions are pinned by full commit SHA, verified against their upstream major-version refs during the audit. Dependabot proposes monthly updates; review release notes and rerun checks before accepting them.

## Operational impact and rollback

This is a documentation/tooling repository; there is no service to deploy. Validation runs on PRs and selected pushes. Scheduled/manual monitoring can create, update or close its own drift issue; unchanged reports cause no issue write. The concurrency group serializes runs. Any bot issue already created remains an auditable record.

To roll back after an approved merge, revert the modernization merge/commit through a new PR. To pause monitoring temporarily, disable **Cloud catalog drift** on the Actions page. No model weights, account plan, secrets or default-branch settings are changed by this modernization.
