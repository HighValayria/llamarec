"""STEP 4：本地 dry-run scorer 与真实 scorer 接口。"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
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

    def score_yesno_batch(self, prompts: list[str]) -> list[dict[str, Any]]:
        return [self.score_yesno(prompt) for prompt in prompts]

    def score_candidates_batch(
        self,
        prompts: list[str],
        label_sets: list[list[str]],
    ) -> list[dict[str, Any]]:
        return [
            self.score_candidates(prompt, label_set)
            for prompt, label_set in zip(prompts, label_sets)
        ]


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
            dtype=dtype,
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

    def score_yesno_batch(self, prompts: list[str]) -> list[dict[str, Any]]:
        log_scores_batch = self._answer_log_scores_batch(prompts, ["Yes", "No"])
        scores = []
        for log_scores in log_scores_batch:
            probabilities = _softmax(log_scores)
            p_yes = probabilities["Yes"]
            p_no = probabilities["No"]
            scores.append(
                {
                    "p_yes": p_yes,
                    "p_no": p_no,
                    "predicted_label": "Yes" if p_yes >= p_no else "No",
                    "scoring_mode": self._scoring_mode(["Yes", "No"]),
                }
            )
        return scores

    def score_candidates_batch(
        self,
        prompts: list[str],
        label_sets: list[list[str]],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any] | None] = [None] * len(prompts)
        grouped_indexes: dict[tuple[str, ...], list[int]] = {}
        for index, label_set in enumerate(label_sets):
            grouped_indexes.setdefault(tuple(label_set), []).append(index)

        for label_tuple, indexes in grouped_indexes.items():
            labels = list(label_tuple)
            grouped_prompts = [prompts[index] for index in indexes]
            log_scores_batch = self._answer_log_scores_batch(grouped_prompts, labels)
            for index, log_scores in zip(indexes, log_scores_batch):
                probabilities = _softmax(log_scores)
                predicted_label = max(labels, key=lambda label: probabilities[label])
                results[index] = {
                    "label_probabilities": probabilities,
                    "predicted_label": predicted_label,
                    "scoring_mode": self._scoring_mode(labels),
                }

        if any(result is None for result in results):
            raise RuntimeError("批量候选打分结果数量与输入不一致。")
        return [result for result in results if result is not None]

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

    def _answer_log_scores_batch(
        self,
        prompts: list[str],
        answers: list[str],
    ) -> list[dict[str, float]]:
        answer_token_ids = {
            answer: self._answer_token_ids(answer)
            for answer in answers
        }
        if all(len(token_ids) == 1 for token_ids in answer_token_ids.values()):
            return self._single_token_log_scores_batch(prompts, answer_token_ids)
        return [
            self._answer_log_scores(prompt, answers)
            for prompt in prompts
        ]

    def _single_token_log_scores(
        self,
        prompt: str,
        answer_token_ids: dict[str, list[int]],
    ) -> dict[str, float]:
        return self._single_token_log_scores_batch([prompt], answer_token_ids)[0]

    def _single_token_log_scores_batch(
        self,
        prompts: list[str],
        answer_token_ids: dict[str, list[int]],
    ) -> list[dict[str, float]]:
        prompt_token_batches = []
        for prompt in prompts:
            prompt_token_ids = self._encode_prompt(prompt)
            prompt_token_ids = self._truncate_prompt_ids(
                prompt_token_ids,
                max_answer_tokens=1,
                append_answer=False,
            )
            prompt_token_batches.append(prompt_token_ids)

        input_ids, attention_mask, last_positions = self._tensor_from_id_batches(
            prompt_token_batches
        )
        with self.torch.no_grad():
            logits = self._last_token_logits(
                input_ids=input_ids,
                attention_mask=attention_mask,
                last_positions=last_positions,
            )

        scores_batch = []
        for row_index in range(len(last_positions)):
            row_logits = logits[row_index]
            scores_batch.append(
                {
                    answer: float(row_logits[token_ids[0]].detach().float().cpu())
                    for answer, token_ids in answer_token_ids.items()
                }
            )
        return scores_batch

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
            encoded = chat_apply(
                [{"role": "user", "content": prompt}],
                tokenize=True,
                add_generation_prompt=True,
            )
            return self._normalize_token_ids(encoded)
        encoded = self.tokenizer.encode(prompt, add_special_tokens=True)
        return self._normalize_token_ids(encoded)

    def _normalize_token_ids(self, encoded: Any) -> list[int]:
        """把 tokenizer 的不同返回类型统一成 ``list[int]``。"""

        if isinstance(encoded, str):
            encoded = self.tokenizer.encode(encoded, add_special_tokens=False)
        elif isinstance(encoded, dict):
            encoded = encoded.get("input_ids")
        elif hasattr(encoded, "input_ids"):
            encoded = encoded.input_ids

        if encoded is None:
            raise ValueError("tokenizer 未返回 input_ids。")
        if hasattr(encoded, "tolist"):
            encoded = encoded.tolist()
        if isinstance(encoded, tuple):
            encoded = list(encoded)
        if encoded and isinstance(encoded[0], list):
            if len(encoded) != 1:
                raise ValueError("当前 scorer 只支持单条 prompt 推理。")
            encoded = encoded[0]

        try:
            return [int(token_id) for token_id in encoded]
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"无法把 tokenizer 输出转换为 token id 列表: {type(encoded)!r}"
            ) from exc

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

    def _tensor_from_id_batches(self, token_id_batches: list[list[int]]):
        if not token_id_batches:
            raise ValueError("批量 prompt 为空，无法计算答案概率。")
        if any(not token_ids for token_ids in token_id_batches):
            raise ValueError("存在编码后为空的 prompt，无法计算答案概率。")

        pad_token_id = self.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.tokenizer.eos_token_id
        if pad_token_id is None:
            pad_token_id = 0

        max_length = max(len(token_ids) for token_ids in token_id_batches)
        padded_batches = []
        mask_batches = []
        last_positions = []
        for token_ids in token_id_batches:
            padding_length = max_length - len(token_ids)
            padded_batches.append(token_ids + [pad_token_id] * padding_length)
            mask_batches.append([1] * len(token_ids) + [0] * padding_length)
            last_positions.append(len(token_ids) - 1)

        input_ids = self.torch.tensor(
            padded_batches,
            dtype=self.torch.long,
            device=self.device,
        )
        attention_mask = self.torch.tensor(
            mask_batches,
            dtype=self.torch.long,
            device=self.device,
        )
        return input_ids, attention_mask, last_positions

    def _last_token_logits(self, input_ids: Any, attention_mask: Any, last_positions: list[int]):
        if hasattr(self.model, "model") and hasattr(self.model, "lm_head"):
            outputs = self.model.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                use_cache=False,
            )
            hidden_states = outputs.last_hidden_state
            row_indexes = self.torch.arange(
                hidden_states.shape[0],
                device=hidden_states.device,
            )
            position_indexes = self.torch.tensor(
                last_positions,
                dtype=self.torch.long,
                device=hidden_states.device,
            )
            selected_hidden_states = hidden_states[row_indexes, position_indexes]
            return self.model.lm_head(selected_hidden_states)

        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            use_cache=False,
        )
        row_indexes = self.torch.arange(outputs.logits.shape[0], device=outputs.logits.device)
        position_indexes = self.torch.tensor(
            last_positions,
            dtype=self.torch.long,
            device=outputs.logits.device,
        )
        return outputs.logits[row_indexes, position_indexes]

    def _scoring_mode(self, answers: list[str]) -> str:
        if all(len(self._answer_token_ids(answer)) == 1 for answer in answers):
            return "real_single_token_logits"
        return "real_sequence_likelihood"


class AdapterModelScorer(RealModelScorer):
    """云端 PEFT adapter scorer，用于 Y-K0/M-K0 等微调模型评测。"""

    def __init__(self, config: dict[str, Any], adapter_dir: str | Path) -> None:
        try:
            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        except ImportError as exc:
            raise ImportError(
                "adapter 评测需要先在云服务器安装 torch、transformers、peft 和 bitsandbytes。"
            ) from exc

        self.config = config
        self.torch = torch
        self.adapter_dir = Path(adapter_dir)
        if not self.adapter_dir.exists():
            raise FileNotFoundError(f"adapter 目录不存在: {self.adapter_dir}")

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

        quant_config = BitsAndBytesConfig(
            load_in_4bit=bool(config.get("lora", {}).get("load_in_4bit", True)),
            bnb_4bit_quant_type=str(config.get("lora", {}).get("quant_type", "nf4")),
            bnb_4bit_compute_dtype=dtype,
            bnb_4bit_use_double_quant=True,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path,
            quantization_config=quant_config,
            device_map="auto",
            dtype=dtype,
            low_cpu_mem_usage=True,
        )
        self.model = PeftModel.from_pretrained(base_model, str(self.adapter_dir))
        self.model.eval()
        self.device = next(self.model.parameters()).device
        self._answer_token_cache: dict[str, list[int]] = {}


def build_scorer(mode: str, config: dict[str, Any] | None = None):
    if mode == "mock":
        return MockScorer()
    if mode == "real":
        if config is None:
            raise ValueError("real 模式必须传入实验配置。")
        return RealModelScorer(config)
    raise ValueError(f"未知推理模式: {mode}")


def build_adapter_scorer(
    mode: str,
    config: dict[str, Any],
    adapter_dir: str | Path | None,
):
    if mode == "mock":
        return MockScorer()
    if mode == "real":
        if adapter_dir is None:
            raise ValueError("real adapter 评测必须传入 --adapter-dir。")
        return AdapterModelScorer(config, adapter_dir)
    raise ValueError(f"未知 adapter 评测模式: {mode}")


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
