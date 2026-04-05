# awesome-ollama-models

> Curated list of free Ollama cloud models - what to use, when to use it, and how to set it up

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Ollama](https://ollama.com) runs many models on cloud datacenter GPUs for free. No local GPU needed. Just add `:cloud` to the model tag and it runs on their infrastructure.

This list helps you pick the right model for your task instead of guessing.

## Contents

- [What is Ollama Cloud?](#what-is-ollama-cloud)
- [Quick Decision Guide](#quick-decision-guide)
- [Models](#models)
- [Benchmarks](#benchmarks)
- [Use Cases](#use-cases)
- [Setup](#setup)
- [Integrations](#integrations)
- [Tips and Tricks](#tips-and-tricks)
- [FAQ](#faq)
- [Contributing](#contributing)

## What is Ollama Cloud?

Ollama cloud models run on datacenter GPUs instead of your local machine. No GPU required, no VRAM limits, no downloading 50GB model files. Just install Ollama and use the `:cloud` tag:

```bash
ollama run kimi-k2.5:cloud "explain quicksort"
```

All cloud models are **free**. Response times vary by model and server load but typically range from 700ms to 3s for first token.

### How it works

1. You send a request with `:cloud` in the model name
2. Ollama routes it to their datacenter GPUs
3. The response streams back to you
4. No model download, no local GPU needed

### Requirements

- [Ollama](https://ollama.com/download) installed (macOS, Linux, or Windows)
- Internet connection
- That's it

## Quick Decision Guide

Not sure which model to use? Start here:

| I want to... | Use this | Why |
|---|---|---|
| Write or debug code | `minimax-m2.7:cloud` | Top coding benchmarks, strong tool use |
| General chat and Q&A | `kimi-k2.5:cloud` | Great balance of quality and speed |
| Fast reasoning | `gpt-oss:120b-cloud` | ~700ms response, good logic |
| Analyze images | `gemma4:cloud` | Clean multimodal support |
| Process long documents | `kimi-k2.5:cloud` | 256K context window |
| Quick lightweight tasks | `nemotron-3-nano:cloud` | Small, fast, gets the job done |
| Deep reasoning | `deepseek-v3.2:cloud` | Strong chain-of-thought |
| Multilingual work | `qwen3.5:cloud` | Best multilingual coverage |
| Code generation at scale | `qwen3-coder-next:cloud` | Built specifically for code |

## Models

### Full model comparison

| Model | Params | Context | Vision | Tools | Thinking | Best For |
|---|---|---|---|---|---|---|
| **kimi-k2.5** | Large MoE | 256K | Yes | Yes | Yes | Coding, reasoning, long context |
| **minimax-m2.7** | ~200B MoE | 200K | No | Yes | Yes | Coding, agent workflows, office docs |
| **minimax-m2.5** | ~200B MoE | 200K | No | Yes | Yes | Coding, general tasks |
| **minimax-m2** | ~200B MoE | 200K | No | Yes | Yes | General tasks |
| **deepseek-v3.2** | Large MoE | 128K | No | Yes | Yes | Reasoning, code |
| **gpt-oss** | 120B | 128K | No | No | No | Fast reasoning, code |
| **glm-5** | 744B (40B active) | 128K | No | Yes | Yes | Reasoning, general |
| **glm-4.7** | Large | 128K | No | Yes | Yes | General tasks |
| **nemotron-3-super** | 120B | 128K | No | Yes | Yes | Reasoning, general |
| **nemotron-3-nano** | 4B-30B | 128K-1M | No | Yes | Yes | Fast tasks, huge context |
| **gemma4** | 26B/31B | 128K | Yes | Yes | Yes | General chat, multimodal |
| **qwen3.5** | Up to 122B | 128K | Yes | Yes | Yes | General, multilingual |
| **qwen3-coder-next** | Large | 128K | No | Yes | No | Code generation |
| **qwen3-vl** | Up to 235B | 128K | Yes | Yes | Yes | Vision tasks |
| **qwen3-next** | 80B | 128K | No | Yes | Yes | Reasoning |
| **devstral-2** | 123B | 32K | No | Yes | No | Code (heavy lifting) |
| **devstral-small-2** | 24B | 32K | Yes | Yes | No | Code (lighter) |
| **ministral-3** | 3B-14B | 128K | Yes | Yes | No | Fast lightweight tasks |
| **cogito-2.1** | 671B | Large | No | No | No | Deep reasoning |
| **rnj-1** | 8B | 32K | No | Yes | No | Lightweight tasks |
| **gemini-3-flash-preview** | Large | 128K | Yes | Yes | Yes | Multimodal, fast |

### What the columns mean

- **Params**: Model parameter count. MoE (Mixture of Experts) models only activate a fraction per request
- **Context**: Maximum input+output token window
- **Vision**: Can process images alongside text
- **Tools**: Supports function/tool calling for agents
- **Thinking**: Has explicit chain-of-thought reasoning mode

## Benchmarks

Tested from a Mac Mini (M-series). Your times may vary based on server load.

### Response speed (time to first token)

| Model | Avg Response Time | Notes |
|---|---|---|
| gpt-oss:120b-cloud | ~700ms | Fastest cloud model tested |
| kimi-k2.5:cloud | ~1400ms | Good speed for the quality |
| minimax-m2.7:cloud | ~2500ms | Slower but worth it for code |
| glm-5:cloud | ~2800ms | Largest model, expect some wait |
| nemotron-3-nano:cloud | ~500ms | Ultra fast for simple tasks |
| gemma4:cloud | ~1000ms | Quick for a multimodal model |

### Quality notes

| Model | Coding | Reasoning | Chat | Vision |
|---|---|---|---|---|
| kimi-k2.5 | Excellent | Excellent | Excellent | Good |
| minimax-m2.7 | Excellent | Good | Good | N/A |
| deepseek-v3.2 | Excellent | Excellent | Good | N/A |
| gpt-oss | Good | Very good | Good | N/A |
| gemma4 | Good | Good | Very good | Excellent |
| qwen3.5 | Good | Good | Very good | Good |
| glm-5 | Good | Very good | Very good | N/A |

## Use Cases

### Coding assistant

**Best choice:** `minimax-m2.7:cloud`
**Runner-up:** `kimi-k2.5:cloud`

```bash
ollama run minimax-m2.7:cloud "write a Python function that parses CSV files and returns a list of dicts"
```

Why: MiniMax M2.7 scores highest on coding benchmarks among free cloud models. Kimi K2.5 is a close second with faster responses.

### General chat and Q&A

**Best choice:** `kimi-k2.5:cloud`
**Runner-up:** `gemma4:cloud`

```bash
ollama run kimi-k2.5:cloud "what are the trade-offs between microservices and monoliths"
```

Why: Kimi K2.5 gives well-structured, thoughtful answers with a good speed/quality balance.

### Image analysis

**Best choice:** `gemma4:cloud`
**Runner-up:** `qwen3-vl:cloud`

```bash
ollama run gemma4:cloud "describe this image" --image screenshot.png
```

Why: Gemma 4 has clean multimodal support and handles screenshots, diagrams and photos well.

### Long document processing

**Best choice:** `kimi-k2.5:cloud` (256K context)
**Runner-up:** `nemotron-3-nano:cloud` (up to 1M context)

```bash
cat long-document.txt | ollama run kimi-k2.5:cloud "summarize this document"
```

Why: Kimi K2.5 has the largest context window among quality models at 256K. Nemotron-3-nano can handle up to 1M tokens but with less quality.

### Agent and tool use workflows

**Best choice:** `minimax-m2.7:cloud`
**Runner-up:** `kimi-k2.5:cloud`

Models with tool support can call functions, making them useful for building agents that interact with APIs, databases and other systems.

### Fast lightweight tasks

**Best choice:** `nemotron-3-nano:cloud`
**Runner-up:** `ministral-3:cloud`

```bash
ollama run nemotron-3-nano:cloud "convert 72 fahrenheit to celsius"
```

Why: When you need a quick answer and don't need deep reasoning. Sub-second responses.

### Deep reasoning and math

**Best choice:** `deepseek-v3.2:cloud`
**Runner-up:** `gpt-oss:120b-cloud`

```bash
ollama run deepseek-v3.2:cloud "prove that the square root of 2 is irrational"
```

Why: DeepSeek V3.2 has strong chain-of-thought capabilities for complex logic problems.

### Multilingual

**Best choice:** `qwen3.5:cloud`
**Runner-up:** `kimi-k2.5:cloud`

Why: Qwen models have the strongest multilingual coverage across CJK languages, European languages and more.

## Setup

### Install Ollama

**macOS:**
```bash
brew install ollama
# or download from https://ollama.com/download
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**

Download from [ollama.com/download](https://ollama.com/download) and run the installer.

### Start Ollama

```bash
ollama serve
```

Or on macOS it runs as a menu bar app automatically.

### Run a cloud model

```bash
# just add :cloud to the model name
ollama run kimi-k2.5:cloud "hello world"

# interactive chat
ollama run kimi-k2.5:cloud

# with an image (vision models only)
ollama run gemma4:cloud "what is in this image" --image photo.jpg
```

### Use the API

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "kimi-k2.5:cloud",
  "prompt": "explain REST APIs in simple terms",
  "stream": false
}'
```

### Python

```python
import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "kimi-k2.5:cloud",
    "prompt": "write a fibonacci function in python",
    "stream": False,
})
print(response.json()["response"])
```

### JavaScript/TypeScript

```javascript
const response = await fetch("http://localhost:11434/api/generate", {
  method: "POST",
  body: JSON.stringify({
    model: "kimi-k2.5:cloud",
    prompt: "explain async/await",
    stream: false,
  }),
});
const data = await response.json();
console.log(data.response);
```

## Integrations

Cloud models work anywhere local Ollama models work. Here are popular integrations:

| Tool | What it does | Link |
|---|---|---|
| **Open WebUI** | Chat interface like ChatGPT | [github.com/open-webui/open-webui](https://github.com/open-webui/open-webui) |
| **Continue** | VS Code/JetBrains AI assistant | [continue.dev](https://continue.dev) |
| **LangChain** | Build LLM-powered apps | [python.langchain.com](https://python.langchain.com) |
| **LlamaIndex** | Build RAG pipelines | [llamaindex.ai](https://llamaindex.ai) |
| **Aider** | AI pair programming in terminal | [aider.chat](https://aider.chat) |
| **ollama-model-router** | Auto-pick the best model per prompt | [github.com/RedBeret/ollama-model-router](https://github.com/RedBeret/ollama-model-router) |

### Continue (VS Code) config example

```json
{
  "models": [
    {
      "title": "Kimi K2.5 Cloud",
      "provider": "ollama",
      "model": "kimi-k2.5:cloud"
    }
  ]
}
```

### Open WebUI

Just point Open WebUI at your Ollama instance. Cloud models appear in the model picker automatically.

## Tips and Tricks

### Spread requests across models

Cloud models have per-model rate limits (roughly 10-20 requests/minute observed). If you hit a 429, switch to an alternate model or wait 30 seconds.

### Use the right model size for the job

Don't use a 200B parameter model to convert units. `nemotron-3-nano:cloud` handles simple tasks in under a second. Save the big models for tasks that need them.

### Combine local and cloud

Run small models locally for fast iteration and use cloud models for complex tasks:

```bash
# fast local model for simple stuff
ollama run phi4-mini "format this JSON"

# cloud model for complex reasoning
ollama run deepseek-v3.2:cloud "review this architecture for scaling issues"
```

### Enable thinking mode

Models that support thinking mode show their reasoning process. Useful for debugging complex logic:

```bash
ollama run kimi-k2.5:cloud "think step by step: what causes a deadlock in concurrent programming?"
```

### Handle rate limits in code

```python
import time
import requests

def query_with_fallback(prompt, models=None):
    if models is None:
        models = ["kimi-k2.5:cloud", "glm-5:cloud", "gemma4:cloud"]
    for model in models:
        try:
            resp = requests.post("http://localhost:11434/api/generate", json={
                "model": model, "prompt": prompt, "stream": False
            }, timeout=30)
            if resp.status_code == 200:
                return resp.json()["response"]
            if resp.status_code == 429:
                time.sleep(5)
                continue
        except requests.RequestException:
            continue
    return None
```

## FAQ

### Are cloud models really free?

Yes. As of April 2026, all `:cloud` models on Ollama are free to use. There are rate limits but no charges.

### How fast are cloud models?

Fastest response times are around 500-700ms (nemotron-3-nano, gpt-oss). Larger models like minimax-m2.7 and glm-5 take 2-3 seconds. All are fast enough for interactive use.

### Can I use cloud models offline?

No. Cloud models require an internet connection. For offline use, download and run models locally with `ollama pull`.

### What are the rate limits?

Rate limits are not officially documented. From testing, expect roughly 10-20 requests per minute per model. Different models have independent limits. If you get a 429 error, wait 30 seconds or switch to another model.

### Do cloud models support streaming?

Yes. Streaming works the same as local models. Responses stream back token by token.

### Can I fine-tune cloud models?

No. Cloud models are inference-only. For fine-tuning, you need to run models locally.

### Which model has the biggest context window?

`nemotron-3-nano:cloud` supports up to 1M tokens. `kimi-k2.5:cloud` supports 256K and is better quality for most tasks.

### Do cloud models support images?

Models with vision support do: `gemma4`, `qwen3.5`, `qwen3-vl`, `devstral-small-2`, `ministral-3`, `gemini-3-flash-preview`, and `kimi-k2.5`.

### How do cloud models compare to ChatGPT/Claude?

Cloud models are free alternatives. They are competitive for many tasks but may not match the latest proprietary models on the hardest benchmarks. For most everyday coding, reasoning and chat tasks, the gap is small.

## Contributing

Contributions welcome. Here is how you can help:

- **Add a model**: Open a PR with the model details and your experience using it
- **Share benchmarks**: Run models on standard tasks and share response times and quality notes
- **Report issues**: If a model listing is wrong or outdated, open an issue
- **Suggest use cases**: Share how you use cloud models in your workflow

### Format for new models

```markdown
| model-name | params | context | vision? | tools? | thinking? | best for |
```

Include a short description of your experience with the model and any benchmark data you have.

## License

[MIT](LICENSE)
