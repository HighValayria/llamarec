# Project Overview

## Paper Type

Venue-neutral empirical/systematic analysis paper.

## Working Positioning

Systematic empirical study of recommendation supervision semantics,
multi-task tradeoffs, hard-candidate robustness, and
sample-efficiency-aware baseline positioning for recommendation-tuned LLMs.

## Central Question

What do different recommendation supervision signals teach an LLM, can
preference and next-item abilities be unified, and how do those conclusions
change under harder candidates, specialized sequential baselines, and a second
dataset?

## Evidence Boundary

Use existing evidence first. Do not launch new experiments in this stage unless
the user explicitly approves a scoped proposal.

## Current Evidence Base

- MovieLens-1M main Y/N/M results.
- Phase 2B result synthesis.
- Phase 2C PopMatch hard-candidate diagnosis.
- Popularity, BPR-MF, and SASRec baseline reports.
- Fair-budget and sample-efficiency SASRec positioning.
- Cold/tail item slice diagnostic.
- MovieLens seed42/43/44 multi-seed stability.
- Amazon Musical Instruments seed42 cross-dataset validation.

## Main Writing Risk

The paper is strongest as an empirical evidence and evaluation-regime paper.
It should not be framed as a new architecture or as universal LLM superiority
over sequential recommenders.
