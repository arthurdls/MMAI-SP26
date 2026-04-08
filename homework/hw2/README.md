# Homework 2 — Multimodal Alignment and Fusion Techniques

**Course:** Multimodal AI (MAS.S60 / 6.S985) · Spring 2026 · MIT

## Overview

This assignment explores how different multimodal fusion and alignment strategies affect performance on two tasks: digit classification on AV-MNIST and tool prediction on ToolBench. The central question is whether explicitly modeling cross-modal interactions outperforms simpler combination strategies.

## Datasets

| Dataset | Modalities | Task | Classes |
|---------|-----------|------|---------|
| **AV-MNIST** | Audio spectrograms + digit images | Digit classification | 10 |
| **ToolBench** | User instructions (TF-IDF) + API descriptions (TF-IDF) | Tool name prediction | Hundreds |

## Key Work

### Unimodal Baselines (AV-MNIST)
- **Audio encoder**: Conv2D → BatchNorm → GRU → MLP (41.14% test accuracy)
- **Image encoder**: Conv2D → BatchNorm → FC layers (64.80% test accuracy)
- Image significantly outperforms audio, showing visual information is more discriminative for digit recognition.

### Fusion Methods (ToolBench)

| Method | Test Accuracy | Parameters | Convergence |
|--------|-------------|------------|-------------|
| **Tensor Fusion** | **44.41%** | ~6M | Epoch 53 (fastest) |
| Early Fusion | 43.73% | ~6M | — |
| LMF | 40.07% | ~1.89M | Epoch 99 |
| Late Fusion | 40.21% | ~1.78M | — |

Methods that explicitly model cross-modal interactions (tensor, early) outperform those that don't (late, LMF) by ~4 percentage points, demonstrating that fine-grained instruction-API interactions are critical for correct tool prediction.

### Contrastive Learning (ToolBench)
- Trained a dual-encoder model with symmetric cross-entropy contrastive loss to align instruction and API list embeddings.
- Achieved **62.1% top-1** and **81.3% top-5** retrieval accuracy using only TF-IDF features — no pretrained language models.
- t-SNE visualization shows the model discovers semantic clustering by API service category without explicit category supervision.

## Key Findings

- **Fusion strategy matters**: Tensor fusion wins on accuracy and convergence speed. Explicitly modeling cross-modal feature interactions yields a meaningful improvement over simple concatenation or averaging.
- **Contrastive alignment works with simple features**: Even TF-IDF embeddings can achieve strong retrieval when properly aligned, motivating the contrastive approach explored in the course project.
- **Failure modes**: The contrastive model struggles to distinguish functionally similar APIs with overlapping descriptions — a key challenge that hard-negative mining (explored in the project) aims to address.

## Notebook

[`adls_mmai_HW2.ipynb`](./adls_mmai_HW2.ipynb)
