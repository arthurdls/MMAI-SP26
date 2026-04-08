# Homework 1 — Multimodal Data Preprocessing with ToolBench

**Course:** Multimodal AI (MAS.S60 / 6.S985) · Spring 2026 · MIT

## Overview

This assignment focuses on extracting and analyzing multimodal signals from the ToolBench dataset — a large-scale collection of multi-turn LLM conversations where models reason about and invoke real-world APIs. The goal is to decompose these conversations into distinct modalities and understand their statistical properties before building models on top of them.

## Modalities Explored

| Modality | Type | Description |
|----------|------|-------------|
| **Instruction** | Unstructured input | Natural language user query describing what the model should do |
| **API List** | Structured input | Tool specifications (names, descriptions, parameters) available to the model |
| **Reasoning** | Unstructured output | Chain-of-thought "Thought:" traces from the assistant |
| **Function Calls** | Structured output | Structured `{name, arguments}` action invocations |

## Key Work

- **Data extraction** — Streamed and parsed the large ToolBench JSON files (~2GB training set) using `ijson` for memory-efficient loading. Extracted four modalities per conversation via regex and JSON parsing.
- **Feature engineering** — Computed word-count statistics per modality, built TF-IDF representations (200 features, bigrams), and applied PCA dimensionality reduction (50 components, GPU-accelerated).
- **Visualization & analysis** — Produced t-SNE scatter plots, word-length distributions, top-20 word frequency charts, violin plots, and perplexity scores (via DistilGPT-2) across all four modalities.
- **Evaluation framework** — Built a `ToolBenchEvaluator` class measuring JSON syntax validity, function selection success rate, argument match rate, and hallucination rate.

## Key Findings

- Structured modalities (API list, function calls) differ significantly from unstructured modalities (instruction, reasoning) in vocabulary, length distribution, and perplexity.
- Instructions are concise and varied; API lists are long and repetitive; reasoning traces sit in between.
- t-SNE reveals that modalities occupy distinct regions in embedding space, motivating the multimodal fusion approaches explored in HW2.

## Notebook

[`adls_mmai_HW1.ipynb`](./adls_mmai_HW1.ipynb)
