# Contributing

Thanks for helping make this list better.

## How to add a model

1. Fork this repo
2. Add the model to the appropriate category table in README.md
3. Include: model name, parameter count, context window, capabilities and a short note
4. Open a PR with a clear title like "add llama-4:cloud to chat models"

## How to add benchmarks

1. Run your tests on cloud models using `ollama run <model>:cloud`
2. Include your hardware specs, ollama version and network type
3. Test at least 3 prompts per category (code, reasoning, chat, creative)
4. Add results as a new section or update existing numbers with your data point
5. Open a PR with your methodology described

## How to suggest a use case

1. Open an issue describing the use case and which model worked best for you
2. Include example prompts and why that model was better than alternatives
3. If you want to write it up yourself, open a PR adding it to the Use Cases section

## Guidelines

- One model per PR (keeps reviews simple)
- Only add models that have a `:cloud` variant on Ollama
- Be honest about quality - if a model is mediocre at something say so
- Include the ollama library link for the model
- Keep descriptions short and factual

## Reporting issues

If benchmark data seems wrong or a model has been removed from Ollama cloud, open an issue and we'll update it.
