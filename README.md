# awesome-ollama-models

> Curated guide to Ollama local and cloud models, including plan limits, usage levels and model lifecycle status

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Last verified:** July 12, 2026

[Ollama](https://ollama.com) can run open models on your hardware or offload supported `:cloud` models to Ollama-managed infrastructure. Local execution does not consume Ollama Cloud usage. Cloud access is available through Free, Pro and Max plans.

> [!IMPORTANT]
> Ollama does not publish a stable model-by-model Free versus paid entitlement table. Model pages publish a relative cloud usage level instead. This guide separates official plan facts from practical model guidance so it does not present inferred access as a guarantee.

## Contents

- [Cloud plans](#cloud-plans)
- [Free versus paid guidance](#free-versus-paid-guidance)
- [Current cloud models](#current-cloud-models)
- [Quick decision guide](#quick-decision-guide)
- [Deprecations](#deprecations)
- [Setup](#setup)
- [API access](#api-access)
- [Integrations](#integrations)
- [Reliability guidance](#reliability-guidance)
- [FAQ](#faq)
- [Contributing](#contributing)

## Cloud plans

| Plan | Price | Concurrent cloud models | Included cloud usage | Official positioning |
|---|---:|---:|---|---|
| Free | $0 | 1 | Light | Chat, evaluation, coding and assistants with smaller models |
| Pro | $20/month or $200/year | 3 | 50x Free | Larger models, coding automation and deep research |
| Max | $100/month | 10 | 5x Pro | Sustained agents, concurrent workflows and extended large-model use |

Ollama measures cloud usage primarily by GPU time rather than a fixed token or requests-per-minute allowance. Session limits reset every five hours and weekly limits reset every seven days. Running models on your own hardware remains unlimited from Ollama's cloud-plan perspective.

Always check the [official pricing page](https://ollama.com/pricing) for current terms.

## Free versus paid guidance

Ollama model pages classify cloud consumption as **low**, **medium**, **high** or **extra high** usage. These are usage bands, not published plan entitlements.

### Free plan starting points

Ollama currently labels two cloud models as low usage. Medium-usage models can also be useful for evaluation on Free, but they will consume the plan allowance faster.

| Model | Usage | Context | Input | Good for |
|---|---|---:|---|---|
| [`gpt-oss:20b-cloud`](https://ollama.com/library/gpt-oss) | Low | 128K | Text | Lightweight reasoning, coding and tool use |
| [`nemotron-3-nano:30b-cloud`](https://ollama.com/library/nemotron-3-nano) | Low | 1M | Text | Efficient agent tasks and very long context |
| [`gpt-oss:120b-cloud`](https://ollama.com/library/gpt-oss) | Medium | 128K | Text | Stronger reasoning and coding |
| [`gemma4:cloud`](https://ollama.com/library/gemma4) | Medium | 256K | Text, image | Multimodal chat, coding and image analysis |
| [`qwen3.5:cloud`](https://ollama.com/library/qwen3.5) | Medium | 256K | Text, image | General, multilingual and multimodal work |
| [`deepseek-v4-flash:cloud`](https://ollama.com/library/deepseek-v4-flash) | Medium | 1M | Text | Long context, reasoning and coding |
| [`minimax-m2.7:cloud`](https://ollama.com/library/minimax-m2.7) | Medium | 200K | Text | Coding and agent workflows |
| [`minimax-m2.5:cloud`](https://ollama.com/library/minimax-m2.5) | Medium | 198K | Text | Coding and productivity |
| [`nemotron-3-super:cloud`](https://ollama.com/library/nemotron-3-super) | Medium | 256K | Text | Agentic and multilingual reasoning |

> [!NOTE]
> “Free plan starting point” does not mean unlimited or permanently guaranteed on Free. Confirm access while signed in and watch your account usage.

### Paid-plan recommended

High and extra-high usage models are practical Pro or Max choices for repeated work. A Free account may allow limited evaluation, but this guide does not treat that as guaranteed access.

| Model | Usage | Context | Input | Good for |
|---|---|---:|---|---|
| [`glm-5.2:cloud`](https://ollama.com/library/glm-5.2) | High | 976K | Text | Long-horizon engineering and large repositories |
| [`glm-5.1:cloud`](https://ollama.com/library/glm-5.1) | High | 198K | Text | Agentic engineering and coding |
| [`mistral-large-3:675b-cloud`](https://ollama.com/library/mistral-large-3) | High | 256K | Text, image | Multilingual and multimodal production tasks |
| [`minimax-m3:cloud`](https://ollama.com/library/minimax-m3) | High | 512K | Text, image | Coding, agents and long multimodal context |
| [`kimi-k2.7-code:cloud`](https://ollama.com/library/kimi-k2.7-code) | High | 256K | Text, image | Long-horizon coding and tool use |
| [`kimi-k2.6:cloud`](https://ollama.com/library/kimi-k2.6) | High | 256K | Text, image | Coding, design and agent orchestration |
| [`kimi-k2.5:cloud`](https://ollama.com/library/kimi-k2.5) | High | 256K | Text, image | General multimodal agent tasks |
| [`nemotron-3-ultra:cloud`](https://ollama.com/library/nemotron-3-ultra) | High | 256K | Text | Long-running, high-throughput agents |
| [`deepseek-v4-pro:cloud`](https://ollama.com/library/deepseek-v4-pro) | Extra high | 1M | Text | Frontier reasoning and difficult coding tasks |

## Current cloud models

The [official cloud catalog](https://ollama.com/search?c=cloud) changes frequently. The following active tags were verified on July 12, 2026.

| Usage | Models |
|---|---|
| Low | `gpt-oss:20b-cloud`, `nemotron-3-nano:30b-cloud` |
| Medium | `gpt-oss:120b-cloud`, `gemma4:cloud`, `gemma4:31b-cloud`, `qwen3.5:cloud`, `qwen3.5:397b-cloud`, `deepseek-v4-flash:cloud`, `minimax-m2.5:cloud`, `minimax-m2.7:cloud`, `nemotron-3-super:cloud` |
| High | `glm-5.1:cloud`, `glm-5.2:cloud`, `mistral-large-3:675b-cloud`, `minimax-m3:cloud`, `kimi-k2.5:cloud`, `kimi-k2.6:cloud`, `kimi-k2.7-code:cloud`, `nemotron-3-ultra:cloud` |
| Extra high | `deepseek-v4-pro:cloud` |

Models with a published retirement date are listed separately below instead of being recommended as current defaults.

## Quick decision guide

| Task | Lower-usage choice | Higher-capability choice |
|---|---|---|
| General work | `qwen3.5:cloud` | `kimi-k2.5:cloud` |
| Lightweight tasks | `gpt-oss:20b-cloud` | `gpt-oss:120b-cloud` |
| Coding assistant | `minimax-m2.7:cloud` | `kimi-k2.7-code:cloud` |
| Deep reasoning | `deepseek-v4-flash:cloud` | `deepseek-v4-pro:cloud` |
| Long documents | `deepseek-v4-flash:cloud` | `glm-5.2:cloud` |
| Images and screenshots | `gemma4:cloud` | `minimax-m3:cloud` |
| Multi-agent automation | `nemotron-3-super:cloud` | `nemotron-3-ultra:cloud` |

## Deprecations

Ollama occasionally retires cloud models. Retirement does not remove an independently available local model.

### Already retired

| Retired cloud model | Retirement date | Recommended replacement |
|---|---|---|
| `kimi-k2-thinking:cloud` | June 16, 2026 | `kimi-k2.6:cloud` |
| `kimi-k2:1t-cloud` | June 16, 2026 | `kimi-k2.6:cloud` |
| `minimax-m2:cloud` | June 16, 2026 | `minimax-m3:cloud` |
| `glm-4.6:cloud` | June 16, 2026 | `glm-5.1:cloud` |
| `qwen3-next:80b-cloud` | June 16, 2026 | `qwen3.5:cloud` |
| `qwen3-vl:235b-cloud` | June 16, 2026 | `qwen3.5:cloud` |
| `qwen3-vl:235b-instruct-cloud` | June 16, 2026 | `qwen3.5:cloud` |
| `cogito-2.1:671b-cloud` | June 16, 2026 | `deepseek-v4-flash:cloud` |
| `rnj-1:8b-cloud` | June 30, 2026 | None listed |

### Scheduled for retirement July 15, 2026

Do not use these tags for new integrations.

| Retiring cloud model | Recommended replacement |
|---|---|
| `deepseek-v3.1:671b-cloud` | `deepseek-v4-flash:cloud` |
| `deepseek-v3.2:cloud` | `deepseek-v4-flash:cloud` |
| `devstral-2:123b-cloud` | `mistral-large-3:675b-cloud` |
| `devstral-small-2:24b-cloud` | None listed |
| `ministral-3:3b-cloud` | None listed |
| `ministral-3:8b-cloud` | None listed |
| `ministral-3:14b-cloud` | None listed |
| `gemini-3-flash-preview:cloud` | `minimax-m3:cloud` |
| `gemma3:4b-cloud`, `gemma3:12b-cloud`, `gemma3:27b-cloud` | `gemma4:31b-cloud` |
| `glm-4.7:cloud`, `glm-5:cloud` | `glm-5.2:cloud` |
| `minimax-m2.1:cloud` | `minimax-m3:cloud` |
| `qwen3-coder-next:cloud`, `qwen3-coder:480b-cloud` | `qwen3.5:397b-cloud` |

Check the [official cloud deprecations](https://docs.ollama.com/cloud#deprecations) before merging model changes.

## Setup

Install [Ollama](https://ollama.com/download), then sign in for cloud access:

```bash
ollama signin
```

Run a cloud model:

```bash
ollama run qwen3.5:cloud "Explain Kubernetes admission control"
```

Run a local model without consuming cloud usage:

```bash
ollama run qwen3.5:9b "Format this JSON"
```

## API access

Use a cloud tag through the local Ollama endpoint:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 \
  --max-time 120 \
  http://localhost:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3.5:cloud",
    "messages": [{"role": "user", "content": "Explain Kubernetes admission control"}],
    "stream": false
  }'
```

The direct Ollama Cloud API uses the exact model names returned by `/api/tags`. These names do not use the local `:cloud` suffix and may include a size tag. Create an API key in your Ollama account, then:

```bash
curl --fail-with-body --silent --show-error \
  --connect-timeout 10 \
  --max-time 120 \
  https://ollama.com/api/chat \
  -H "Authorization: Bearer ${OLLAMA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-oss:120b",
    "messages": [{"role": "user", "content": "Explain Kubernetes admission control"}],
    "stream": false
  }'
```

List models currently exposed by the direct cloud API:

```bash
curl --fail-with-body --silent --show-error https://ollama.com/api/tags
```

See the [official cloud API documentation](https://docs.ollama.com/cloud#cloud-api-access) for current authentication and tag conventions.

## Integrations

Cloud models use the same Ollama interfaces as local models.

| Tool | Purpose | Link |
|---|---|---|
| Open WebUI | Browser chat interface | [github.com/open-webui/open-webui](https://github.com/open-webui/open-webui) |
| Continue | VS Code and JetBrains assistant | [continue.dev](https://continue.dev) |
| LangChain | LLM application framework | [python.langchain.com](https://python.langchain.com) |
| LlamaIndex | RAG and data framework | [llamaindex.ai](https://llamaindex.ai) |
| Aider | Terminal coding assistant | [aider.chat](https://aider.chat) |
| ollama-model-router | Route prompts among Ollama models | [github.com/RedBeret/ollama-model-router](https://github.com/RedBeret/ollama-model-router) |

## Reliability guidance

- Do not hard-code a cloud model without a fallback.
- Prefer active models over tags with a published retirement date.
- Treat HTTP 401 and 403 as authentication or access failures.
- Treat HTTP 429 as a rate-limit response and honor `Retry-After` when present.
- Retry transient 5xx failures with capped exponential backoff.
- Set connection and response timeouts.
- Keep a local fallback when privacy, availability or cost is critical.
- Do not log API keys or sensitive prompts.

Example fallback order:

```text
qwen3.5:cloud
  -> gpt-oss:20b-cloud
  -> qwen3.5:9b (local)
```

## FAQ

### Are Ollama cloud models free?

Ollama has a Free cloud plan with light usage. Pro and Max provide more usage and concurrency. Pro also advertises access to larger, more powerful cloud models. It is no longer accurate to call every cloud model universally free.

### Which exact models are on the Free tier?

Ollama does not publish a stable per-model entitlement matrix. Start with low-usage models, use medium-usage models cautiously and confirm access while signed in. The usage bands in this guide describe relative compute consumption, not guaranteed plan eligibility.

### Are local models free?

Running public models on your own hardware does not consume Ollama Cloud usage. Your hardware, electricity and infrastructure costs still apply.

### What are the rate limits?

Ollama publishes session and weekly usage limits rather than a fixed requests-per-minute allowance. Concurrency is one cloud model on Free, three on Pro and ten on Max.

### Can cloud models run offline?

No. Use a local model tag for offline operation.

## Sources

- [Ollama pricing](https://ollama.com/pricing)
- [Ollama Cloud documentation](https://docs.ollama.com/cloud)
- [Ollama cloud model catalog](https://ollama.com/search?c=cloud)
- Individual Ollama model pages linked above

## Contributing

Before adding or changing a cloud model:

1. Confirm it appears in the official cloud catalog.
2. Confirm the exact tag, context, input types and usage level on its model page.
3. Check the cloud deprecations list.
4. Avoid unsupported benchmark, latency, price or rate-limit claims.
5. Include the verification date in the pull request.

Suggested row format:

```markdown
| model-tag | usage | context | input | good for |
```

## License

[MIT](LICENSE)
