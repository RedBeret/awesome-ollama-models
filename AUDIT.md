# Repository and source audit

Reference date: **October 14, 2026** (America/Los_Angeles). Research used live official sources, not the unavailable earlier ZIP.

## Repository baseline

- Repository: [RedBeret/awesome-ollama-models](https://github.com/RedBeret/awesome-ollama-models); public; MIT.
- Default branch: `init-project`, commit `ae051d28851e31cff88f31f698d2241a341e1aca`.
- Read all four original files: `README.md` (13,100 bytes), `LICENSE`, `.gitignore`, `.whitesource`. Reviewed recent history, branches, repository metadata, rulesets and open PRs. No existing workflow files were present. Public ruleset listing returned none; repository metadata reported the branch unprotected. This does not establish every organization/Actions policy.
- Other branches were `main` and `whitesource/configure`. Open [PR #10](https://github.com/RedBeret/awesome-ollama-models/pull/10), “Update retired models and attributes,” overlaps documentation and remains untouched; coordinate before merging either PR.
- Preserved MIT and `.whitesource` byte-for-byte. Preserved integration references, local/cloud examples, routing project and reliability guidance, with corrected tags and statements.

## Corrections

| Previous README claim | Current evidence and treatment |
|---|---|
| GPU-time allowances, five-hour sessions, weekly resets, 50×/5× plan multipliers | [Pricing](https://ollama.com/pricing) now advertises token-priced credits; README documents current plans and the transition caveat for existing subscribers |
| Low-usage models as Free starting points | Starter access is a smaller set; purchased credits unlock all models. Usage bands are not entitlements |
| Older cloud tags in the current guide | [Public API](https://ollama.com/api/tags) returned 18 IDs; rebuilt cloud entries around that exact set and verified CLI tags independently |
| June/July retirement dates presented as current public facts | Current [cloud docs](https://docs.ollama.com/cloud#retirements) direct users to account usage notices; retained history, removed unconfirmed dated assertions from current recommendations |
| Reasoning, vision and tools inferred across a family | Cloud capabilities verified against each API entry and model page; local tags verified separately; Gemma cloud 31B is not labeled audio-capable |
| Cloud/local API naming treated as interchangeable | Separate direct and CLI fields; DeepSeek V4 Pro public ID is `deepseek-v4-pro:0813` |
| No generated source, validation or monitoring | Added strict JSON validation, deterministic generation, offline regression tests and bounded public polling |

The live cloud set contains newer DeepSeek V4.1 Flash, GLM 5.3/5.3 Flash, Kimi K3 and Mistral Large 4 entries. Older research candidates absent from the live listing were not promoted to active cloud entries. The local Qwen 3.5 9B tag remains separately sourced. There are **20 curated entries: 18 cloud IDs plus two local-only examples**; local variants attached to a cloud entry do not add another row.

## Source disagreements

We use the specific tag's published context label and retain conflicts in catalog notes. Labels such as K/M are not converted into exact counts. No effective inference limit was measured.

| Model | Tag page | Search/family presentation | Catalog treatment |
|---|---|---|---|
| [GLM 5.2](https://ollama.com/library/glm-5.2) | 976K | Search: 1M | 976K tag label |
| [MiniMax M2.7](https://ollama.com/library/minimax-m2.7) | 200K | Search: 192K | 200K label; verify before using the full limit |
| [MiniMax M3](https://ollama.com/library/minimax-m3) | 512K | Search: 500K; family advertises up to 1M | 512K tag label, no blanket 1M guarantee |
| [Nemotron 3 Nano 30B](https://ollama.com/library/nemotron-3-nano) | Cloud 30B: 1M | Search card: 256K and a 4B variant | 1M on the exact 30B tag; no cross-variant inference |
| [DeepSeek V4 Pro](https://ollama.com/library/deepseek-v4-pro) | Dated and undated CLI aliases; undated example | API listing: dated `:0813` | Store the observed direct ID and verified dated CLI tag |

Search source: [official cloud filter](https://ollama.com/search?c=cloud). It lists families (17), while the API lists variants (18), including two GPT-OSS sizes. These counts are different units.

## Research sources and method

Fetched [Ollama home](https://ollama.com/), [pricing](https://ollama.com/pricing), [cloud search](https://ollama.com/search?c=cloud), [library](https://ollama.com/library), [public model JSON](https://ollama.com/api/tags), [cloud docs](https://docs.ollama.com/cloud), [API introduction](https://docs.ollama.com/api/introduction), [errors](https://docs.ollama.com/api/errors), [quickstart](https://docs.ollama.com/quickstart), [FAQ](https://docs.ollama.com/faq), and [structured outputs](https://docs.ollama.com/capabilities/structured-outputs).

Individual pages fetched: [GPT-OSS](https://ollama.com/library/gpt-oss), [Gemma 4](https://ollama.com/library/gemma4), [Qwen 3.5](https://ollama.com/library/qwen3.5), [DeepSeek V4.1 Flash](https://ollama.com/library/deepseek-v4.1-flash), [DeepSeek V4 Pro](https://ollama.com/library/deepseek-v4-pro), [GLM 5.2](https://ollama.com/library/glm-5.2), [GLM 5.3](https://ollama.com/library/glm-5.3), [GLM 5.3 Flash](https://ollama.com/library/glm-5.3-flash), [MiniMax M2.7](https://ollama.com/library/minimax-m2.7), [MiniMax M3](https://ollama.com/library/minimax-m3), [Kimi K2.6](https://ollama.com/library/kimi-k2.6), [Kimi K2.7 Code](https://ollama.com/library/kimi-k2.7-code), [Kimi K3](https://ollama.com/library/kimi-k3), [Nemotron Nano](https://ollama.com/library/nemotron-3-nano), [Nemotron Super](https://ollama.com/library/nemotron-3-super), [Nemotron Ultra](https://ollama.com/library/nemotron-3-ultra), [Mistral Large 3](https://ollama.com/library/mistral-large-3), [Mistral Large 4](https://ollama.com/library/mistral-large-4).

Cloud IDs and capability flags come from the live API. CLI/local tags, context and input types were cross-checked against tag tables. Prices come from individual pages where shown, otherwise the pricing page. A captured API response is committed as an offline test fixture; it is not a current listing or a second editable catalog. Unknown local availability remains null. Catalog use cases paraphrase documented applications; the decision guide is editorial.

## Limits of verification

No paid inference, model download, hardware benchmarking or account-specific entitlement test was performed. Current source content cannot establish historical billing-change dates or reconfirm private retirement notices. The drift monitor intentionally does not detect changes to price, context, modality or terms. Review those manually. Local validation results and actual GitHub Actions status are reported in the delivery/PR, not presumed here.
