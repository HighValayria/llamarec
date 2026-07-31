"""STEP 4：本地 dry-run scorer 与真实 scorer 接口。"""

from __future__ import annotations

import hashlib
import math
from typing import Any


class MockScorer:
    """不加载模型的确定性 scorer，用于本地验证文件流和指标流。"""

    def score_yesno(self, prompt: str) -> dict[str, Any]:
        scores = _deterministic_scores(prompt, ["Yes", "No"])
        probabilities = _softmax(scores)
        p_yes = probabilities["Yes"]
        p_no = probabilities["No"]
        return {
            "p_yes": p_yes,
            "p_no": p_no,
            "predicted_label": "Yes" if p_yes >= p_no else "No",
            "scoring_mode": "mock",
        }

    def score_candidates(
        self,
        prompt: str,
        label_set: list[str],
    ) -> dict[str, Any]:
        scores = _deterministic_scores(prompt, label_set)
        probabilities = _softmax(scores)
        predicted_label = max(label_set, key=lambda label: probabilities[label])
        return {
            "label_probabilities": probabilities,
            "predicted_label": predicted_label,
            "scoring_mode": "mock",
        }


class RealModelScorer:
    """真实模型 scorer 的占位接口。

    本地不加载 Llama。云端实现时，应在这个类里接入 tokenizer/model，并用 logits
    或完整答案 sequence likelihood 计算连续概率。
    """

    def __init__(self, *_args, **_kwargs) -> None:
        raise NotImplementedError(
            "real 模式尚未在本地实现；请先使用 --mode mock 跑通 dry-run。"
        )


def build_scorer(mode: str):
    if mode == "mock":
        return MockScorer()
    if mode == "real":
        return RealModelScorer()
    raise ValueError(f"未知推理模式: {mode}")


def _deterministic_scores(prompt: str, labels: list[str]) -> dict[str, float]:
    scores = {}
    for label in labels:
        digest = hashlib.sha256(f"{prompt}\n::{label}".encode("utf-8")).hexdigest()
        raw_value = int(digest[:12], 16)
        scores[label] = raw_value / float(0xFFFFFFFFFFFF)
    return scores


def _softmax(scores: dict[str, float]) -> dict[str, float]:
    max_score = max(scores.values())
    exp_scores = {
        label: math.exp(score - max_score)
        for label, score in scores.items()
    }
    total = sum(exp_scores.values())
    return {
        label: value / total
        for label, value in exp_scores.items()
    }
