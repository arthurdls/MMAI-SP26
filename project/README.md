# Course Project — Multimodal Tool Retrieval via Hard-Negative Mining

## Overview

Agentic systems that interact with large API collections face a core retrieval challenge: given a natural language instruction, identify the correct tool from 16,000+ candidates. We treat user queries and structured API schemas as distinct modalities and investigate how the quality of negative examples affects retrieval performance.

## Midterm Progress

### Dense Retrieval Baseline
We established a baseline using OpenAI `text-embedding-3-small` embeddings over the full ToolBench corpus with FAISS inner-product search.

| Model | R@1 | R@5 | R@10 | MRR |
|-------|-----|-----|------|-----|
| `text-embedding-3-small` | 0.223 | 0.421 | 0.506 | 0.435 |

### Hard-Negative Ablation
We evaluated three negative-sampling strategies of increasing difficulty using 100-candidate restricted pools:

| Negative Condition | R@1 | R@5 | R@10 | MRR |
|--------------------|-----|-----|------|-----|
| Random | 0.520 | 0.914 | 0.951 | 0.926 |
| Category Siblings | 0.417 | 0.772 | 0.839 | 0.808 |
| DFSDT Failure Paths | 0.414 | 0.774 | 0.851 | 0.810 |

**Key finding:** Category-level and DFSDT negatives reduce R@1 by ~10 points vs. random negatives, confirming that the current embedding model cannot distinguish semantically related but functionally different tools.

## Next Steps

1. **Hierarchical Contrastive Loss** — Multi-granularity alignment using ToolBench's API → Tool → Category hierarchy to improve retrieval for tail APIs with sparse documentation.
2. **Code-Enhanced Tri-Encoder** — Adding a CodeBERT encoder for functional code snippets to disambiguate textually similar but functionally different APIs.
3. **Contrastive fine-tuning** — Training a bi-encoder with weighted hard negatives (up-weighting DFSDT failure-path negatives).

## Team

| Member | Repository |
|--------|-----------|
| Arthur De Los Santos | [MMAI-SP26](https://github.com/arthurdls/MMAI-SP26) |
| Dylan Mazard | [MMAI-Spring2026](https://github.com/Dmazard/MMAI-Spring2026) |
| Michael Serrano | [mmai](https://github.com/michaelyserrano/mmai) |

**Team repo:** [multimodal-tool-retrieval](https://github.com/arthurdls/multimodal-tool-retrieval) — project code, experiments, and reports live there. Each member's individual repo is included as a submodule.
