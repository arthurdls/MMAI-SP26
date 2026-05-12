# Homework 4 — Reinforcement Learning for Vision-Language Models (GRPO)

**Course:** Multimodal AI (MAS.S60 / 6.S985) · Spring 2026 · MIT

## Overview

This assignment explores **Group Relative Policy Optimization (GRPO)** as an alternative to SFT/LoRA for adapting vision-language models. Where HW3 fine-tuned a VLM via supervised learning on API-card images, HW4 keeps the same dataset but trains the model with RL, using simple rule-based rewards instead of teacher-forced labels.

## Setup

| Component | Details |
|-----------|---------|
| **Model** | Qwen3-VL-2B-Instruct |
| **Algorithm** | GRPO via TRL `GRPOTrainer` (vanilla implementation) |
| **Adapter** | LoRA (r=16, alpha=32) |
| **Dataset** | Same API-card image / instruction / answer triples as HW3 |
| **Rewards** | Accuracy (exact match after `Answer:`) + format compliance |
| **Environment** | Google Colab, A100-80GB |

## Key Work

- **Group-relative advantage computation** — Implemented the core GRPO mechanic: sample G completions per prompt, normalize rewards within the group (`A_i = (r_i − μ) / σ`), and use that as the advantage signal. Avoids a separate critic network entirely.
- **Rule-based rewards** — Two simple, deterministic reward functions: a binary accuracy reward (does the text after `Answer:` match ground truth?) and a format reward (does the completion include the `Answer:` marker?).
- **Dataset adapter** — Converted HW3's `data.jsonl` into the conversational/`image`/`answer` columns expected by `GRPOTrainer`.
- **Hyperparameter sweep** — Best config: `NUM_GENERATIONS=32`, `MAX_COMPLETION_LENGTH=512`, `LR=1e-5`, `MAX_STEPS=300`, `EPSILON=0.2`, `TEMPERATURE=0.9`, `BETA=0.0`, `LORA_R=16`, `LORA_ALPHA=32`. Trains in ~11 minutes on A100-80GB.
- **Post-training evaluation** — Compared the GRPO-trained adapters against the zero-shot base model and the HW3 SFT model on held-out test images.

## Key Findings

- **Format compliance:** GRPO model reached 75% format compliance (3/4 test samples used `Answer:`), substantially better than the zero-shot base and the HW3 SFT model. The format reward did its job.
- **GRPO vs. SFT (HW3):** GRPO converged on this small dataset without the catastrophic visual-signal collapse seen in HW3's SFT runs. The group-relative baseline lets the model explore multiple completions per prompt and reinforce ones that happen to attend to the image content.
- **Failure mode:** Occasional reasoning loops where the model burns its entire 512-token budget repeating phrases before ever emitting `Answer:`.

## Files

| File | Description |
|------|-------------|
| [`Homework_4_GRPO_VLMs.ipynb`](./Homework_4_GRPO_VLMs.ipynb) | Main notebook |
| [`api_card_renderer.py`](./api_card_renderer.py) | API JSON → styled card image renderer (reused from HW3) |
