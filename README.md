# awesome-ollama-models

> Curated list of the best free Ollama cloud models with benchmarks and use case recommendations

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Ollama](https://ollama.com) now runs many models on cloud datacenter GPUs for free - no local GPU needed. Add `:cloud` to any supported model tag and it runs on their infrastructure.

This list helps you pick the right model for your task.

## Contents

- [What is Ollama Cloud?](#what-is-ollama-cloud)
- [Models](#models)
- [Benchmarks](#benchmarks)
- [Use Cases](#use-cases)
- [Setup](#setup)
- [FAQ](#faq)
- [Contributing](#contributing)

## What is Ollama Cloud?

Ollama cloud models run on datacenter GPUs instead of your local machine. No GPU required. Just install Ollama and use the `:cloud` tag:

```bash
ollama run kimi-k2.5:cloud "explain quicksort"
```

All cloud models are free. Response times vary by model and load but typically range from 700ms to 3s.

## Models

### Chat and General

Best for conversations, Q&A and general tasks.

| Model | Params | Context | Capabilities | Notes |
|-------|--------|---------|-------------|-------|
| [kimi-k2.5](https://ollama.com/library/kimi-k2.5) | Large MoE | 256K | vision, tools, thinking | excellent all-rounder with huge context |
| [glm-5](https://ollama.com/library/glm-5) | 744B (40B active) | 128K | tools, thinking | massive model, good reasoning |
| [glm-4.7](https://ollama.com/library/glm-4.7) | Large | 128K | tools, thinking | solid general purpose |
| [nemotron-3-super](https://ollama.com/library/nemotron-3-super) | 120B | 128K | tools, thinking | strong reasoning and general |
| [qwen3.5](https://ollama.com/library/qwen3.5) | up to 122B | 128K | vision, tools, thinking | great multilingual support |

### Coding

Best for code generation, debugging and refactoring.

| Model | Params | Context | Capabilities | Notes |
|-------|--------|---------|-------------|-------|
| [minimax-m2.7](https://ollama.com/library/minimax-m2.7) | ~200B MoE | 200K | tools, thinking | top coding benchmarks, has thinking mode |
| [minimax-m2.5](https://ollama.com/library/minimax-m2.5) | ~200B MoE | 200K | tools, thinking | previous gen, still very capable |
| [devstral-2](https://ollama.com/library/devstral-2) | 123B | 32K | tools | heavy code model |
| [devstral-small-2](https://ollama.com/library/devstral-small-2) | 24B | 32K | vision, tools | lighter code model with vision |
| [qwen3-coder-next](https://ollama.com/library/qwen3-coder-next) | Large | 128K | tools | dedicated code generation |

### Reasoning

Best for analysis, math, logic and step-by-step thinking.

| Model | Params | Context | Capabilities | Notes |
|-------|--------|---------|-------------|-------|
| [gpt-oss](https://ollama.com/library/gpt-oss) | 120B | 128K | reasoning | fast reasoning, good code |
| [deepseek-v3.2](https://ollama.com/library/deepseek-v3.2) | Large MoE | 128K | tools, thinking | strong reasoning and code |
| [qwen3-next](https://ollama.com/library/qwen3-next) | 80B | 128K | tools, thinking | focused reasoning model |
| [cogito-2.1](https://ollama.com/library/cogito-2.1) | 671B | Large | - | pure reasoning |

### Vision and Multimodal

Best for image understanding, screenshots and visual tasks.

| Model | Params | Context | Capabilities | Notes |
|-------|--------|---------|-------------|-------|
| [gemma4](https://ollama.com/library/gemma4) | 26B/31B | 128K | vision, tools, thinking | google's multimodal model |
| [qwen3-vl](https://ollama.com/library/qwen3-vl) | up to 235B | 128K | vision, tools, thinking | large vision model |
| [gemini-3-flash-preview](https://ollama.com/library/gemini-3-flash-preview) | Large | 128K | vision, tools, thinking | fast multimodal |

### Lightweight and Fast

Best when speed matters more than peak quality.

| Model | Params | Context | Capabilities | Notes |
|-------|--------|---------|-------------|-------|
| [nemotron-3-nano](https://ollama.com/library/nemotron-3-nano) | 4B/30B | 128K-1M | tools, thinking | extremely fast, up to 1M context |
| [ministral-3](https://ollama.com/library/ministral-3) | 3B/8B/14B | 128K | vision, tools | multiple size options |
| [rnj-1](https://ollama.com/library/rnj-1) | 8B | 32K | tools | minimal footprint |

## Benchmarks

*Coming soon - speed and quality benchmarks across common tasks.*

## Use Cases

*Coming soon - recommended models per task type.*

## Setup

*Coming soon - installation and quickstart guide.*

## FAQ

*Coming soon.*

## Contributing

*Coming soon - guidelines for submitting model reviews and benchmarks.*

## License

[MIT](LICENSE)
