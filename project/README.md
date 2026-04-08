# Course Project — Multimodal Tool Retrieval via Hard-Negative Mining

All project code, experiments, and results live in the shared team repository under [`project/`](https://github.com/arthurdls/multimodal-tool-retrieval/tree/main/project).

**Team repo:** [multimodal-tool-retrieval](https://github.com/arthurdls/multimodal-tool-retrieval)

## Quick Links

- [Project README](https://github.com/arthurdls/multimodal-tool-retrieval/tree/main/project)
- [Notebook 01 — Index APIs](https://github.com/arthurdls/multimodal-tool-retrieval/tree/main/project/notebooks/01_index_apis.ipynb)
- [Notebook 02 — Baseline Eval](https://github.com/arthurdls/multimodal-tool-retrieval/tree/main/project/notebooks/02_baseline_eval.ipynb)
- [Notebook 03 — Hard-Negative Ablation](https://github.com/arthurdls/multimodal-tool-retrieval/tree/main/project/notebooks/03_hard_negative_eval.ipynb)

## Summary

We establish a dense retrieval baseline using OpenAI `text-embedding-3-small` over 16,000+ ToolBench APIs (R@5 = 0.421) and evaluate three negative-sampling strategies — random, category-sibling, and DFSDT failure-path negatives. Category-level and DFSDT negatives reduce R@1 by ~10 points vs. random, confirming the model's inability to distinguish semantically related but functionally different tools.

**Next steps:** Hierarchical Contrastive Loss and a Code-Enhanced Tri-Encoder with CodeBERT.

## Team

| Member | Repository |
|--------|-----------|
| Arthur De Los Santos | [MMAI-SP26](https://github.com/arthurdls/MMAI-SP26) |
| Dylan Mazard | [MMAI-Spring2026](https://github.com/Dmazard/MMAI-Spring2026) |
| Michael Serrano | [mmai](https://github.com/michaelyserrano/mmai) |
