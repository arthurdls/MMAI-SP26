# Homework 5 — AI Agents in the Wild

**Course:** Multimodal AI (MAS.S60 / 6.S985) · Spring 2026 · MIT

## Overview

This assignment shifts from training models to **building, evaluating, and improving a goal-directed AI agent**. The agent — **PaperLens** — is an arxiv-paper research assistant built on `smolagents`, with text and vision variants, a custom benchmark, safety mitigations, and end-to-end observability via Langfuse.

## Setup

| Component | Details |
|-----------|---------|
| **Framework** | [`smolagents`](https://huggingface.co/docs/smolagents/) (`ToolCallingAgent`, `CodeAgent`) |
| **Model** | Qwen2.5-VL-7B-Instruct via `TransformersModel` (bf16) |
| **Environment** | Google Colab, NVIDIA L4 (24 GB VRAM), `do_sample=True`, `temperature=0.5`, `max_new_tokens=1024` |
| **Observability** | Langfuse via `SmolagentsInstrumentor()` (OpenTelemetry-compatible) |
| **Domain** | arxiv paper retrieval and Q&A |

## Eval Design

12 tasks across three categories:

| Category | Count | Examples |
|----------|-------|----------|
| Normal (`n1`–`n5`) | 5 | Verifiable Q&A with ground truth (authors, metrics, dataset facts) |
| Edge (`e1`–`e3`) | 3 | Empty retrieval, multi-paper synthesis, graceful failure on bad IDs |
| Adversarial (`a1`–`a4`) | 4 | Prompt injection, out-of-scope, PII, loaded framing — rubric flips so refusal is the "correct" outcome |

## Key Work

### Part 3 — Text Agent (smolagents baseline + custom tools)
- **Stage A (baseline):** `ToolCallingAgent` with built-in `WebSearch` + `VisitWebpage`.
- **Stage B (custom tools):** Added `ArxivSearchTool` and `ArxivAbstractTool` for structured access to arxiv. Custom tools improved answer specificity on several normal tasks but increased latency on others.

### Part 4 — Multimodal (Vision) Agent — PaperLens
- `CodeAgent` backed by the same Qwen2.5-VL model, with the VLM consuming arxiv abstract-page screenshots as observations.
- Controlled A/B comparison: text-only vs. vision-augmented variants on the same eval set.
- **Safety mitigation:** Added a pre-prompt + tool-output sanitization mitigation; ran 3 adversarial prompts (injection, out-of-scope, PII) before and after. The mitigated variant correctly refused or redirected on all three.

### Part 5 — Observability and Online Eval
- `SmolagentsInstrumentor()` exports OpenTelemetry traces to Langfuse, surfacing per-step model calls, tool I/O, and latency.
- Recorded 5+ traces, drilled into spans on `n2`/`n3`/`e1`/`e3`/`a2` to confirm trace fields map back to the eval schema designed in Part 2.
- **Config comparison** on a 5-task slice:

  | Config | Success | Avg latency | Est. cost |
  |---|---|---|---|
  | A: built-in tools only | 3/5 | 9.86 s | $0.00033 |
  | B: A + arxiv custom tools | 2/5 | 167.7 s | higher |

  The custom-tool config is more accurate on tasks it can answer but much slower and more expensive per query — a real trade-off, not a free win.

### Part 6 — Discord Integration
Packaged the agent for the class Discord world so it can run alongside other students' agents.

## Key Findings

- **Custom tools ≠ automatic improvement.** Arxiv-specific tools helped on some tasks but hurt latency and occasionally caused the agent to over-rely on a brittle structured path instead of falling back to general web search.
- **Vision helps on screenshot-friendly pages, hurts elsewhere.** PaperLens's vision variant won on tasks where the abstract page rendered cleanly; on cluttered pages or non-arxiv sources, the text-only variant was more reliable.
- **Observability is a force multiplier for eval.** Langfuse spans made it obvious where time and tokens were being burned — most of the latency in config B came from a single tool that kept retrying on near-misses.
- **Safety mitigations are cheap and effective.** A short pre-prompt was enough to flip all three adversarial cases from unsafe to safe behavior, with no measurable regression on normal tasks.

## Files

| File | Description |
|------|-------------|
| [`adls_mmai_HW5.ipynb`](./adls_mmai_HW5.ipynb) | Main notebook (agent code, eval set, traces, results) |
