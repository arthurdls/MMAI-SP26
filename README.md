# MMAI 2026 — Arthur De Los Santos

Welcome to my repository for Multimodal AI (MAS.S60 / 6.S985) at MIT, Spring 2026.
This repo is a living lab notebook tracking my homework, experiments, and course project.

## Bio

Hi, I'm Arthur De Los Santos — a 6-3 student at MIT interested in AI/ML and agentic systems.

## Course Project — Multimodal Tool Retrieval via Hard-Negative Mining

We present a multimodal approach to API retrieval using the ToolBench dataset (16,000+ real-world APIs), treating user queries and structured API schemas as distinct modalities. Our midterm work establishes a dense retrieval baseline (`text-embedding-3-small`, R@5 = 0.421) and evaluates three negative-sampling strategies — random, category-sibling, and DFSDT failure-path negatives — revealing a ~10-point R@1 drop under hard conditions. Next steps: **Hierarchical Contrastive Loss** and a **Code-Enhanced Tri-Encoder** with CodeBERT.

**Team:** Arthur De Los Santos, Dylan Mazard, Michael Serrano

- [Project Overview](./project/README.md)
- [Team Repository](https://github.com/arthurdls/multimodal-tool-retrieval)

## Homework

| # | Topic | Notebook |
|---|---|---|
| 1 | Multimodal Data Preprocessing with ToolBench | [HW1](./homework/hw1/adls_mmai_HW1.ipynb) |
| 2 | Multimodal Alignment and Fusion Techniques | [HW2](./homework/hw2/adls_mmai_HW2.ipynb) |
| 3 | Fine-tuning Vision-Language Models | [HW3](./homework/hw3/adls_mmai_HW3.ipynb) |

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
