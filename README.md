# awesome-ollama-models

> A sourced guide to Ollama local and cloud models, with generated comparisons and cloud catalog drift monitoring.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate catalog](https://github.com/RedBeret/awesome-ollama-models/actions/workflows/validate.yml/badge.svg?branch=init-project)](https://github.com/RedBeret/awesome-ollama-models/actions/workflows/validate.yml)

**Research snapshot: October 14, 2026.** Covers all 18 direct cloud identifiers observed that day and two additional local examples. This is a point-in-time reference, not an exhaustive local library or an availability guarantee. [Full catalog and model prices](MODEL_CATALOG.md) · [Audit and source conflicts](AUDIT.md) · [Contributing](CONTRIBUTING.md) · [Lifecycle policy](docs/LIFECYCLE.md).

## Contents

- [Getting started](#getting-started)
- [Local versus cloud](#local-versus-cloud)
- [Free versus paid](#free-versus-paid)
- [Current models](#current-models)
- [Quick decision guide](#quick-decision-guide)
- [Engineering workflows](#engineering-workflows)
- [API examples](#api-examples)
- [Integrations](#integrations)
- [Production reliability](#production-reliability)
- [Maintaining the catalog](#maintaining-the-catalog)

## Getting started

Install [Ollama](https://ollama.com/download) using its official installer. Open the app or run `ollama` and follow setup prompts. Choose a local model, or sign in for cloud access. On Linux, start `ollama serve` if the server is not already running. [Official quickstart](https://docs.ollama.com/quickstart).

```bash
# Downloads weights; subsequent inference runs locally.
ollama run gemma4:e2b "Explain Kubernetes admission control"

# Runs on Ollama infrastructure; requires sign-in, network access and available credits.
ollama run gemma4:31b-cloud "Explain Kubernetes admission control"
```

Local models require suitable hardware and a download before offline use. Memory needs vary with quantization, context, and concurrency; download size is not a complete RAM/VRAM requirement.

## Local versus cloud

| Choice | Execution and privacy | Cost and operation |
|---|---|---|
| Downloaded local tag, e.g. `gemma4:e2b` | Inference runs on your hardware; review integrations and external tools separately | No Ollama Cloud usage charge; hardware, electricity and model license terms still apply |
| CLI cloud tag, e.g. `gemma4:31b-cloud` | The local Ollama interface sends inference to cloud infrastructure | Sign-in and network required; usage billed against account credits |
| Direct API ID, e.g. `gemma4:31b` | Your application calls `https://ollama.com/api/chat` | Bearer API key required; no Ollama installation needed |

**Tag namespaces differ.** For direct cloud requests, copy an identifier from [`https://ollama.com/api/tags`](https://ollama.com/api/tags). Use the catalog's separately verified CLI tag through local Ollama. Do not mechanically strip `:cloud`: aliases and dated identifiers can differ. For example, the observed direct ID is `deepseek-v4-pro:0813`.

Ollama says cloud prompts/responses are not used for training; see its [data-handling documentation](https://docs.ollama.com/cloud#data-handling) and [privacy policy](https://ollama.com/privacy). Cloud requests still leave your machine. For local-only operation, the [FAQ](https://docs.ollama.com/faq) documents `OLLAMA_NO_CLOUD=1`; restart Ollama after changing it. Keep the local server on loopback unless you add appropriate network access controls.

## Free versus paid

The live [Ollama pricing page](https://ollama.com/pricing), checked October 14, 2026, advertises token-priced usage credits:

| Plan | Subscription | Included monthly usage | Concurrent requests |
|---|---:|---|---:|
| Free | $0 | Starter credits; amount not publicly specified | 1 |
| Pro | $20/month or $200/year | $60 in credits | 3 |
| Max | $100/month | $300 in credits | 10 |
| Team (early access) | From $500/month | $1,000 shared credits | 10 |

Free starter usage applies to a smaller starter set; purchased credits unlock all models. Included credits reset monthly and do not roll over. The page says switching from an existing Pro/Max plan removes the old session/weekly limits; existing subscribers should check their account terms. Queuing is bounded. We do not infer entitlement from a model's relative usage band. Enterprise is custom-priced.

Charges depend on input, cached-input and output tokens. Consult [the generated price table](MODEL_CATALOG.md#published-cloud-prices) and current billing page before spending. Off-peak DeepSeek rates are documented per entry. Local weights do not consume cloud credits.

## Current models

This block is generated from [`data/models.json`](data/models.json). Context labels describe the published tag, not a tested effective limit. See [source disagreements](AUDIT.md#source-disagreements) before planning large requests. Unknown local availability is shown explicitly. Public listing presence does not prove access for every account.

<!-- BEGIN GENERATED CATALOG -->

| Model / direct Cloud API ID | CLI cloud tag | Verified local tag | Context label | Input | Tools / thinking |
|---|---|---|---|---|---|
| `deepseek-v4-pro:0813` | `deepseek-v4-pro:0813-cloud` | Not verified | 1M | text | Yes / Yes |
| `deepseek-v4.1-flash` | `deepseek-v4.1-flash:cloud` | Not verified | 1M | text, image | Yes / Yes |
| `gemma4:31b` | `gemma4:31b-cloud` | `gemma4:31b` | 256K | text, image | Yes / Yes |
| Gemma 4 E2B (local only) | Not verified | `gemma4:e2b` | 128K | text, image | Yes / Yes |
| `glm-5.2` | `glm-5.2:cloud` | Not verified | 976K | text | Yes / Yes |
| `glm-5.3` | `glm-5.3:cloud` | Not verified | 1M | text | Yes / Yes |
| `glm-5.3-flash` | `glm-5.3-flash:cloud` | Not verified | 1M | text, image | Yes / Yes |
| `gpt-oss:120b` | `gpt-oss:120b-cloud` | `gpt-oss:120b` | 128K | text | Yes / Yes |
| `gpt-oss:20b` | `gpt-oss:20b-cloud` | `gpt-oss:20b` | 128K | text | Yes / Yes |
| `kimi-k2.6` | `kimi-k2.6:cloud` | Not verified | 256K | text, image | Yes / Yes |
| `kimi-k2.7-code` | `kimi-k2.7-code:cloud` | Not verified | 256K | text, image | Yes / Yes |
| `kimi-k3` | `kimi-k3:cloud` | Not verified | 1M | text, image | Yes / Yes |
| `minimax-m2.7` | `minimax-m2.7:cloud` | Not verified | 200K | text | Yes / Yes |
| `minimax-m3` | `minimax-m3:cloud` | Not verified | 512K | text, image | Yes / Yes |
| `mistral-large-3:675b` | `mistral-large-3:675b-cloud` | Not verified | 256K | text, image | Yes / No |
| `mistral-large-4` | `mistral-large-4:cloud` | Not verified | 1M | text, image | Yes / Yes |
| `nemotron-3-nano:30b` | `nemotron-3-nano:30b-cloud` | `nemotron-3-nano:30b` | 1M | text | Yes / Yes |
| `nemotron-3-super` | `nemotron-3-super:cloud` | `nemotron-3-super:120b` | 256K | text | Yes / Yes |
| `nemotron-3-ultra` | `nemotron-3-ultra:cloud` | Not verified | 256K | text | Yes / Yes |
| Qwen 3.5 9B (local only) | Not verified | `qwen3.5:9b` | 256K | text, image | Yes / Yes |

<!-- END GENERATED CATALOG -->

## Quick decision guide

**Editorial starting points, not benchmark rankings.** Evaluate representative prompts, latency, quality, and cost. Tool support means a model can request tools; your application must implement and authorize their execution.

| Task | Starting points | Selection advice |
|---|---|---|
| Everyday chat | Gemma 4 E2B locally; Gemma 4 31B cloud | Start small; use cloud when local hardware is insufficient |
| Coding assistance | GPT-OSS 20B; MiniMax M2.7 | Test against your unit tests and repository conventions |
| Complex software engineering | GLM 5.3; Kimi K2.7 Code | Evaluate multi-file fixes and long-running behavior |
| Agentic tool use | Nemotron 3 Super/Ultra | Bound tool calls, permissions, spending and elapsed time |
| Repository analysis | GLM 5.3; Kimi K3 | Retrieve relevant files before relying on a large context window |
| Long documents | DeepSeek V4.1 Flash; Mistral Large 4 | Budget input tokens and verify retrieval accuracy |
| Reasoning | GPT-OSS 120B; DeepSeek V4 Pro 0813 | Verify answers independently; reasoning modes affect cost/latency |
| Image analysis | Gemma 4 31B; MiniMax M3 | Test image resolution and document parsing quality |
| Structured outputs | Local GPT-OSS 20B | Official docs say cloud structured outputs are unsupported; validate local JSON against your schema |
| Low-cost automation | Nemotron 3 Nano 30B; GPT-OSS 20B | Compare input/output mix using current prices; no free-access assumption |
| Local/offline use | Gemma 4 E2B; Qwen 3.5 9B | Download first; verify hardware and disable cloud if required |

Structured-output limitation: [official documentation](https://docs.ollama.com/capabilities/structured-outputs). Recommendations are maintained prose; regeneration changes only the marked comparison block.

## Engineering workflows

Use these as review prompts with an appropriate model. Output is a draft to test, not authority to deploy:

| Area | Example prompt | Verification |
|---|---|---|
| Python / JavaScript | “Review this function, propose a minimal patch, and explain its failure cases.” | Unit tests, linting, dependency review |
| PowerShell | “Make this script idempotent and add a dry-run option.” | Disposable directory and representative filenames |
| Kubernetes / DevOps | “Explain this manifest and propose resource requests and health probes.” | Schema validation, diff, staging rollout |
| GitLab CI/CD | “Simplify this pipeline while preserving protected deployment rules.” | GitLab CI lint and a test pipeline |
| YAML / Infrastructure as Code | “Generate a minimal configuration from these requirements.” | Parse it, run the provider's validator and review the plan |
| Code review | “Find behavior changes in this diff and missing regression coverage.” | Reproduce each finding |
| Local agents | “Analyze these approved files using read-only tools.” | Sandbox paths; approve state changes and external transmission |

Remove secrets and private data before sending material to cloud models. Keep agent credentials separate from prompts.

## API examples

These Bash examples use curl with connection and total timeouts. Run local inference after installing Ollama and downloading `gemma4:e2b`:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 --max-time 120 \
  http://localhost:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma4:e2b","messages":[{"role":"user","content":"Explain Kubernetes admission control"}],"stream":false}'
```

To route through your signed-in local server to cloud, replace the model with `gemma4:31b-cloud`. A cloud suffix changes where inference executes, even when the HTTP endpoint is localhost.

For direct cloud access, create an [Ollama API key](https://ollama.com/settings/keys) and supply it through your environment or secret manager. This reads it without echoing it or putting its value in shell history:

```bash
read -r -s -p 'Ollama API key: ' OLLAMA_API_KEY; printf '\n'
export OLLAMA_API_KEY
: "${OLLAMA_API_KEY:?Set OLLAMA_API_KEY first}"
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 --max-time 120 \
  https://ollama.com/api/chat \
  -H "Authorization: Bearer ${OLLAMA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma4:31b","messages":[{"role":"user","content":"Explain Kubernetes admission control"}],"stream":false}'
```

In PowerShell 7, use a secret-store-provided `$env:OLLAMA_API_KEY`:

```powershell
if (-not $env:OLLAMA_API_KEY) { throw 'Set OLLAMA_API_KEY from your secret store first' }
$requestBody = @{
    model = 'gemma4:31b'
    messages = @(@{ role = 'user'; content = 'Explain Kubernetes admission control' })
    stream = $false
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri 'https://ollama.com/api/chat' `
    -Headers @{ Authorization = "Bearer $env:OLLAMA_API_KEY" } `
    -ContentType 'application/json' -Body $requestBody -TimeoutSec 120
```

Public model discovery requires no API key:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 --max-time 30 https://ollama.com/api/tags
```

See [API base URLs and authentication](https://docs.ollama.com/api/introduction). Examples were checked against the docs; paid inference was not executed in this audit. Avoid verbose HTTP tracing with credentials.

## Integrations

The existing references remain useful. Configure each tool for the intended endpoint/model and check its own authentication and feature support:

| Tool | Purpose | Reference |
|---|---|---|
| Open WebUI | Browser chat interface | [Project](https://github.com/open-webui/open-webui) |
| Continue | Editor assistant | [Project](https://continue.dev) |
| Aider | Terminal coding assistant | [Project](https://aider.chat) |
| LangChain | Application framework | [Project](https://python.langchain.com) |
| LlamaIndex | Retrieval and data framework | [Project](https://llamaindex.ai) |
| ollama-model-router | Related routing project | [RedBeret/ollama-model-router](https://github.com/RedBeret/ollama-model-router) |

## Production reliability

- Treat 401/403 as credential/access failures; fix configuration instead of retrying indefinitely. A listing is not an entitlement check.
- Treat 404 or a missing model as a reason to inspect tags, aliases and lifecycle notices. Absence alone does not prove retirement.
- Honor `Retry-After` on 429 where present; cap delay, attempts and job time. Reduce concurrency when queues fill.
- Retry transient 5xx/network failures with capped exponential backoff and jitter. Inference retries can duplicate work or spend credits; retry tool side effects only when idempotent.
- Bound connections and response waits. Fallback needs explicit cost, quality and privacy rules. Do not silently send local-only private prompts to cloud.
- Pre-download and test a local fallback. An editorial example is `gemma4:31b-cloud` → `gpt-oss:20b-cloud` → `gemma4:e2b` (local); evaluate each independently.
- Keep keys in a secret manager or environment. Avoid logging keys, prompts, full responses or tool credentials.
- Inspect streaming error objects as well as HTTP status: a mid-stream error can leave the status unchanged. [API errors](https://docs.ollama.com/api/errors).

## Maintaining the catalog

Python **3.12+**, standard library only:

```bash
python scripts/catalog.py validate
python scripts/catalog.py generate
python scripts/catalog.py generate --check
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
git diff --check
```

The small issue-maintenance script uses Node's standard library and is tested with `node --test tests/test_drift_issue.cjs` (Node 22+). GitHub-hosted runners supply Node; catalog editing needs no Node installation.

Validation runs offline on PRs and selected pushes. Weekly drift polling uses separate 10-second connection and 30-second response timeouts, at most three attempts, capped backoff and a 2 MiB response limit. It reports identifier changes, maintains one bot-owned issue, leaves unchanged drift quiet, and closes its issue once resolved. A network/schema failure fails the job without publishing a disappearance report. It never edits catalog data or merges changes.

Scheduled monitoring starts only after the workflow reaches the default branch. Manual runs also require that branch. [Contributing](CONTRIBUTING.md) explains verification, [lifecycle policy](docs/LIFECYCLE.md) covers retired tags, and [security review](SECURITY_REVIEW.md) records safeguards and limitations.

## Sources and verification

The [audit](AUDIT.md) maps corrections to official sources. Each entry includes source URLs, verification date and documented uses. JSON is the maintained source; `MODEL_CATALOG.md` and the marked README block are generated. Prices, plan terms and editorial recommendations need manual review; drift monitoring checks identifiers only.

## License

[MIT](LICENSE). This repository's license does not replace model licenses or cloud service terms.
