# Course Project — Multimodal Tool Retrieval

## Overview

We propose a multimodal retrieval system for agentic tool-use. The core challenge: given a natural language user instruction, retrieve the correct API tools from a large catalogue — treating user queries and structured API documentation as distinct modalities that must be aligned.

## Research Directions

| Idea | Description |
|------|-------------|
| **Hierarchical Contrastive Alignment** | Leverages ToolBench's API → Tool → Category hierarchy. A hierarchical contrastive loss simultaneously aligns user intent with fine-grained API docs and coarse category labels, acting as a regularizer for tail APIs with sparse documentation. |
| **Code-Enhanced Tri-Encoder** | Adds a third modality — executable code snippets — via a CodeBERT encoder alongside BERT encoders for instructions and API docs. Code disambiguates APIs that are textually similar but functionally different. |
| **Hard-Negative Mining (DFSDT)** | Mines hard negatives from ToolBench's Depth-First Search Decision Tree traces: APIs that the agent considered but ultimately rejected during successful trajectories. Training on these failure-path negatives teaches the model to distinguish functionally similar tools. |

## Metrics

- Recall@k (k = 1, 5, 10) — primary
- Mean Reciprocal Rank (MRR)
- API Selection F1

## Team

| Member | Repository |
|--------|-----------|
| Arthur De Los Santos | [MMAI-SP26](https://github.com/arthurdls/MMAI-SP26) |
| Dylan Mazard | [MMAI-Spring2026](https://github.com/Dmazard/MMAI-Spring2026) |
| Michael Serrano | [mmai](https://github.com/michaelyserrano/mmai) |

**Team repo:** [multimodal-tool-retrieval](https://github.com/arthurdls/multimodal-tool-retrieval)

The project code, experiments, and reports live in the shared team repository. Each member's individual repo (like this one) is included as a submodule.
