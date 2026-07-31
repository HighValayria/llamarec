"""STEP 4：答案 tokenization 检查。"""

from __future__ import annotations

from typing import Any


DEFAULT_ANSWERS = ["Yes", "No", "A", "B", "C", "D", "E"]


def build_tokenization_report(
    mode: str,
    tokenizer: Any | None = None,
    answers: list[str] | None = None,
) -> dict[str, Any]:
    """生成答案 tokenization 报告。

    mock 模式没有 tokenizer，只记录待检查答案；real 模式必须传入 tokenizer。
    """

    answers = answers or DEFAULT_ANSWERS
    if tokenizer is None:
        return {
            "mode": mode,
            "checked": False,
            "reason": "tokenizer_not_loaded_in_local_dry_run",
            "answers": answers,
        }

    answer_reports = {}
    for answer in answers:
        token_ids = tokenizer.encode(answer, add_special_tokens=False)
        answer_reports[answer] = {
            "token_ids": token_ids,
            "token_count": len(token_ids),
            "single_token": len(token_ids) == 1,
        }

    return {
        "mode": mode,
        "checked": True,
        "answers": answer_reports,
        "use_sequence_likelihood_for": [
            answer
            for answer, report in answer_reports.items()
            if not report["single_token"]
        ],
    }
