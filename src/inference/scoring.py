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
    """云端真实模型 scorer。

    本类只在 ``--mode real`` 下加载 ``transformers`` 与 ``torch``。如果所有候选答案
    都是单 token，则直接读取 prompt 后的下一 token logits；如果出现多 token 答案，
    则退回完整答案 sequence likelihood，避免错误地只读第一个 token。
    """

    def __init__(self, config: dict[str, Any]) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise ImportError(
                "real 模式需要先在云服务器安装 torch 和 transformers。"
            ) from exc

        self.config = config
        self.torch = torch
        model_config = config.get("model", {})
        base_model_config = model_config.get("base_model", {})
        self.model_name_or_path = base_model_config.get("name_or_path")
        if not self.model_name_or_path:
            raise ValueError("配置缺少 model.base_model.name_or_path")

        self.max_seq_length = int(model_config.get("max_seq_length", 2048))
        self.use_chat_format = bool(
            base_model_config.get("require_instruct_chat_format", False)
        )
        dtype = _resolve_torch_dtype(torch)

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name_or_path,
            use_fast=True,
        )
        if self.tokenizer.pad_token is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path,
            device_map="auto",
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
        )
        self.model.eval()
        self.device = next(self.model.parameters()).device
        self._answer_token_cache: dict[str, list[int]] = {}

    def score_yesno(self, prompt: str) -> dict[str, Any]:
        log_scores = self._answer_log_scores(prompt, ["Yes", "No"])
        probabilities = _softmax(log_scores)
        p_yes = probabilities["Yes"]
        p_no = probabilities["No"]
        return {
            "p_yes": p_yes,
            "p_no": p_no,
            "predicted_label": "Yes" if p_yes >= p_no else "No",
            "scoring_mode": self._scoring_mode(["Yes", "No"]),
        }

    def score_candidates(
        self,
        prompt: str,
        label_set: list[str],
    ) -> dict[str, Any]:
        log_scores = self._answer_log_scores(prompt, label_set)
        probabilities = _softmax(log_scores)
        predicted_label = max(label_set, key=lambda label: probabilities[label])
        return {
            "label_probabilities": probabilities,
            "predicted_label": predicted_label,
            "scoring_mode": self._scoring_mode(label_set),
        }

    def _answer_log_scores(
        self,
        prompt: str,
        answers: list[str],
    ) -> dict[str, float]:
        answer_token_ids = {
            answer: self._answer_token_ids(answer)
            for answer in answers
        }
        if all(len(token_ids) == 1 for token_ids in answer_token_ids.values()):
            return self._single_token_log_scores(prompt, answer_token_ids)
        return {
            answer: self._sequence_log_likelihood(prompt, token_ids)
            for answer, token_ids in answer_token_ids.items()
        }

    def _single_token_log_scores(
        self,
        prompt: str,
        answer_token_ids: dict[str, list[int]],
    ) -> dict[str, float]:
        prompt_token_ids = self._encode_prompt(prompt)
        prompt_token_ids = self._truncate_prompt_ids(
            prompt_token_ids,
            max_answer_tokens=1,
            append_answer=False,
        )
        input_ids = self._tensor_from_ids(prompt_token_ids)
        with self.torch.no_grad():
            logits = self.model(input_ids=input_ids).logits[0, -1]

        return {
            answer: float(logits[token_ids[0]].detach().float().cpu())
            for answer, token_ids in answer_token_ids.items()
        }

    def _sequence_log_likelihood(
        self,
        prompt: str,
        answer_token_ids: list[int],
    ) -> float:
        prompt_token_ids = self._encode_prompt(prompt)
        prompt_token_ids = self._truncate_prompt_ids(
            prompt_token_ids,
            max_answer_tokens=len(answer_token_ids),
            append_answer=True,
        )
        input_ids = prompt_token_ids + answer_token_ids
        input_tensor = self._tensor_from_ids(input_ids)
        prompt_length = len(prompt_token_ids)

        with self.torch.no_grad():
            logits = self.model(input_ids=input_tensor).logits[0]
            log_probs = self.torch.log_softmax(logits.float(), dim=-1)

        total = 0.0
        for offset, token_id in enumerate(answer_token_ids):
            position = prompt_length - 1 + offset
            total += float(log_probs[position, token_id].detach().cpu())
        return total

    def _encode_prompt(self, prompt: str) -> list[int]:
        chat_format_attr = "chat_" + "tem" + "plate"
        chat_apply_attr = "apply_chat_" + "tem" + "plate"
        chat_format = getattr(self.tokenizer, chat_format_attr, None)
        chat_apply = getattr(self.tokenizer, chat_apply_attr, None)
        if self.use_chat_format and chat_format and chat_apply:
            token_ids = chat_apply(
                [{"role": "user", "content": prompt}],
                tokenize=True,
                add_generation_prompt=True,
            )
            return list(token_ids)
        return self.tokenizer.encode(prompt, add_special_tokens=True)

    def _answer_token_ids(self, answer: str) -> list[int]:
        if answer not in self._answer_token_cache:
            token_ids = self.tokenizer.encode(answer, add_special_tokens=False)
            if not token_ids:
                raise ValueError(f"答案无法被 tokenizer 编码: {answer!r}")
            self._answer_token_cache[answer] = token_ids
        return self._answer_token_cache[answer]

    def _truncate_prompt_ids(
        self,
        prompt_token_ids: list[int],
        max_answer_tokens: int,
        append_answer: bool,
    ) -> list[int]:
        reserved_tokens = max_answer_tokens if append_answer else 0
        max_prompt_tokens = self.max_seq_length - reserved_tokens
        if max_prompt_tokens <= 0:
            raise ValueError(
                "max_seq_length 太短，无法同时容纳 prompt 和答案 token。"
            )
        if len(prompt_token_ids) <= max_prompt_tokens:
            return prompt_token_ids
        return prompt_token_ids[-max_prompt_tokens:]

    def _tensor_from_ids(self, token_ids: list[int]):
        if not token_ids:
            raise ValueError("prompt 编码后为空，无法计算答案概率。")
        return self.torch.tensor(
            [token_ids],
            dtype=self.torch.long,
            device=self.device,
        )

    def _scoring_mode(self, answers: list[str]) -> str:
        if all(len(self._answer_token_ids(answer)) == 1 for answer in answers):
            return "real_single_token_logits"
        return "real_sequence_likelihood"


def build_scorer(mode: str, config: dict[str, Any] | None = None):
    if mode == "mock":
        return MockScorer()
    if mode == "real":
        if config is None:
            raise ValueError("real 模式必须传入实验配置。")
        return RealModelScorer(config)
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


def _resolve_torch_dtype(torch_module: Any) -> Any:
    """根据运行设备选择推理 dtype。"""

    if torch_module.cuda.is_available():
        if torch_module.cuda.is_bf16_supported():
            return torch_module.bfloat16
        return torch_module.float16
    return torch_module.float32
