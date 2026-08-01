"""STEP 4：Base/Y/N/M 共用 prompt 渲染。"""

from __future__ import annotations

import hashlib
from typing import Any


def render_yesno_prompt(sample: dict[str, Any]) -> str:
    """渲染 Y 任务 prompt，不泄漏 target rating。"""

    lines = [
        "Task: Preference Prediction",
        "",
        "User history:",
    ]
    lines.extend(_history_lines(sample.get("history", []), include_ratings=True))
    lines.extend(
        [
            "",
            "Target movie:",
            _movie_title(sample["target"]),
            "",
            "Question:",
            "Would the user like the target movie?",
            "",
            "Answer with exactly one option:",
            "Yes",
            "No",
            "",
            "Answer:",
        ]
    )
    return "\n".join(lines)


def render_candidate_prompt(
    record: dict[str, Any],
    movie_lookup: dict[str, dict[str, str]],
) -> str:
    """渲染 N 候选选择 prompt，不泄漏 candidate rating。"""

    label_set = record.get("label_set", ["A", "B", "C", "D", "E"])
    lines = [
        "Task: Next-item Prediction",
        "",
        "User history:",
    ]
    lines.extend(_history_lines(record.get("history", []), include_ratings=False))
    lines.extend(["", "Candidates:"])

    for label, movie_id in zip(label_set, record["candidate_movie_ids"]):
        title = _candidate_title(movie_id, movie_lookup)
        lines.append(f"{label}. {title}")

    lines.extend(
        [
            "",
            "Question:",
            "Which candidate is the user's next interaction?",
            "",
            "Answer with exactly one option:",
            *label_set,
            "",
            "Answer:",
        ]
    )
    return "\n".join(lines)


def prompt_hash(prompt: str) -> str:
    """返回 prompt 的短 hash，用于 prediction 追踪。"""

    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def assert_no_target_rating_in_yesno_prompt(prompt: str, sample: dict[str, Any]) -> None:
    """检查 Y prompt 的 target 区域没有泄漏 target rating。"""

    target_title = _movie_title(sample["target"])
    target_section = prompt.split("Target movie:", 1)[-1]

    assert target_title in target_section
    if "rating" in sample["target"]:
        target_rating = str(sample["target"]["rating"])
        assert f"rating: {target_rating}" not in target_section
        assert f"rating {target_rating}" not in target_section


def assert_no_candidate_rating_in_candidate_prompt(prompt: str) -> None:
    """检查 N prompt 候选区域没有显式 rating 字段。"""

    candidate_section = prompt.split("Candidates:", 1)[-1]
    assert "rating:" not in candidate_section.lower()


def _history_lines(
    history: list[dict[str, Any]],
    include_ratings: bool,
) -> list[str]:
    if not history:
        return ["No prior history."]

    lines = []
    for index, item in enumerate(history, start=1):
        title = _movie_title(item)
        if include_ratings:
            lines.append(f"{index}. {title} (rating: {_format_rating(item['rating'])})")
        else:
            lines.append(f"{index}. {title}")
    return lines


def _candidate_title(movie_id: str, movie_lookup: dict[str, dict[str, str]]) -> str:
    movie = movie_lookup.get(str(movie_id), {})
    title = movie.get("title")
    if title:
        return title
    return f"Movie {movie_id}"


def _movie_title(item: dict[str, Any]) -> str:
    return str(item.get("title") or f"Movie {item['movie_id']}")


def _format_rating(rating: Any) -> str:
    numeric = float(rating)
    if numeric.is_integer():
        return str(int(numeric))
    return str(numeric)
