# Model lifecycle and migration

The catalog records observations, not service guarantees. For cloud entries, `active` means the ID was present in the public API listing on the entry's verification date. For local-only entries, it means the tag was present on its official page. Availability for an individual account can differ.

| Status | Meaning | Contribution requirement |
|---|---|---|
| `active` | Observed available in its verified execution mode | Record official source and date |
| `retiring` | An official notice establishes a future cloud retirement | Link the notice and date in notes; propose a tested migration |
| `retired` | Retirement is explicitly confirmed by an official source | Keep historical evidence; exclude from current recommendations |
| `unknown` | Current lifecycle cannot be established | Describe the uncertainty; do not recommend as a current default |

The drift comparison includes active/retiring cloud IDs. A removed ID is **not automatically retired**: it may be renamed, aliased, temporarily unavailable or affected by service behavior. Empty, malformed or failed API responses are monitoring errors, never evidence that all models disappeared.

The old README listed retirement dates in June/July 2026. The current [cloud docs](https://docs.ollama.com/cloud#retirements) direct users to [usage settings](https://ollama.com/settings/usage) for notices about recently used models. This audit could not independently reconfirm the old dates from the current public docs. They are preserved in Git history at `ae051d2`, and are not presented here as newly verified facts.

Historical cloud names no longer in the October 14 public listing include `qwen3.5`, `deepseek-v4-flash`, `glm-5.1`, `kimi-k2.5`, and `minimax-m2.5`. This is an identifier observation only. Qwen 3.5's local `9b` tag is independently verified and remains in the catalog. Do not infer local removal from cloud retirement.

## Migration checklist

1. Capture the official notice or live listing change and verification date.
2. Check the exact direct API ID and CLI tag on current official pages.
3. Re-evaluate context, modalities, tools, reasoning controls, model license and costs.
4. Run representative tasks against the replacement; there is no guaranteed drop-in equivalence.
5. Update the catalog and editorial guidance through a reviewed PR; regenerate docs.
6. Test a privacy-appropriate fallback and remove old hard-coded IDs from clients.

Replacement suggestions are editorial unless a source explicitly recommends them. Downloaded local weights are not affected by cloud retirement, according to the current cloud docs.
