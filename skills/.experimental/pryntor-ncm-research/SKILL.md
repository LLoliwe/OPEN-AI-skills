---
name: pryntor-ncm-research
description: Safely evaluate the public HazyResearch Next-Concept Modeling release using an offline experiment-evidence gate, with zero-new-spend, no private data, and human review.
---

# Pryntor R&D-002 / PRY-266 — NCM optional research skill

Scope: **research only**. Paper: https://arxiv.org/abs/2610.14162 (9 Oct 2026).
Source: https://github.com/HazyResearch/ncm (MIT source; observed revision
c70274273f489abc73832b2b98584a8483b6b203).
Checkpoints: https://huggingface.co/hazyresearch/ncm-checkpoints (MIT metadata).
Do not copy checkpoint weights into this repository. Do not claim model installation.

## Why
NCM is a multiscale residual VQ-VAE tokenizer and transformer predicting codes
coarse-to-fine, all positions within a level in parallel. Reported on one H100:
21x LM1B, 10x OpenWebText, 31x XSum vs selected diffusion baselines. Sudoku
result is not proof of school-maths error diagnosis. Models evaluated are research
scale; authors flag fixed hierarchy depth, separate tokenizer, generation artifacts.
These improvements are NOT proven versus Pryntor's production baseline.

## R0 acceptance workflow
1. Classify task fit: XSum summarization is first public research candidate. Keep
   education grading/proof validation, sensitive client operations and production
   routes unchanged. No private prompts, curricula or learner data.
2. Freeze SHA-pinned upstream source, checkpoint, public dataset; preregister
   baseline, quality tolerance, minimum speed ratio, all seeds, hardware, batch
   size, output length, analysis metric, security region and spending cap before
   running. Conform to company experiment integrity PRY-199 and GPU cost PRY-223.
3. Confirm **existing, applicable free** compute entitlement and direct job cost
   before any real inference. No spend/new subscription or unapproved GPU launch.
4. Independently execute baseline and NCM on same inputs, retain raw logs and
   SHA256 digests, and report ALL planned runs including failures. Compare both
   absolute quality and actual latency. Do not substitute lab's H100 times.
5. Audit manifest with local command:
       python3 gate.py ./manifest.json
   Exit 0 means STRUCTURALLY_ELIGIBLE_FOR_HUMAN_REVIEW, not genuine measured
   performance or scientific reproducibility. Test data in tests are SYNTHETIC
   claims deliberately manufactured for structural checks. No inference runs here.
6. Independent reviewer checks artifact identities, full run logs, fairness,
   accuracy, bias/privacy and downstream relevance. Human founder and domain
   expert approval required to touch actual apps or make performance claims.

## Scope limitations
- No CUDA, PyTorch, checkpoint load, model weights or dataset downloads.
- No automatic deployment or routing change, no teacher-facing scoring.
- Offline gate validates consistency of user-supplied JSON claims; it cannot
  verify benchmark logs, price, identity, copyright, actual model use or novelty.
- Any quality win must also survive held-out real customer/domain testing.
