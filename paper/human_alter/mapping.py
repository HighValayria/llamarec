from __future__ import annotations

import re
from pathlib import Path

from docx_model import normalized_text, paragraph_text


ROOT = Path(__file__).resolve().parents[2]


def source_records() -> list[dict]:
    records = []
    directive = re.compile(r"<!--\s*(PARAGRAPH|INCLUDE):\s*([^<>]+?)\s*-->")

    def visit(path: Path) -> None:
        text = path.read_text(encoding="utf-8-sig")
        matches = list(directive.finditer(text))
        for index, match in enumerate(matches):
            kind, value = match.group(1), match.group(2).strip()
            if kind == "INCLUDE":
                visit(ROOT / value)
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            segment = text[match.end():end]
            pair = re.search(r"\*\*EN\*\*\s*(.*?)\s*\*\*ZH\*\*\s*(.*)", segment, re.S)
            if pair is None:
                raise ValueError(f"Missing EN/ZH pair for {value} in {path}")
            records.append({
                "id": value,
                "source": path.relative_to(ROOT).as_posix(),
                "en": pair.group(1).strip(),
                "zh": pair.group(2).strip(),
            })

    ordered = [ROOT / "paper/modules/10_abstract.md"]
    ordered.extend(sorted((ROOT / "paper/modules").glob("0[1-9]_*.md")))
    for path in ordered:
        visit(path)
    if len(records) != 78 or len({row["id"] for row in records}) != 78:
        raise ValueError(f"Expected 78 unique manuscript paragraph IDs, found {len(records)}")
    return records


def alignment_text(value: str, language: str) -> str:
    value = re.sub(r"\[((?:\s*@[-:.\w]+\s*(?:;\s*)?)+)\]", " ", value)
    value = re.sub(r"\[(?:TABLE|FIGURE):\s*[a-z][a-z0-9_]*\]", " ", value)
    value = re.sub(r"\[(?:\d+)(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+)*\]", " ", value)
    value = re.sub(r"\b(?:Table|Figure|Fig[.])\s+[IVX\d]+\b", " ", value, flags=re.I)
    value = value.replace("**", "").replace("`", "")
    value = normalized_text(value, compact_cjk=language == "zh", casefold=language == "en")
    value = re.sub(r"[^0-9a-z\u3400-\u9fff%]+", "", value.casefold())
    return value


def score(source: str, target: str, language: str) -> float:
    left, right = alignment_text(source, language), alignment_text(target, language)
    if not left or not right:
        return 0.0
    def grams(value: str) -> set[str]:
        if len(value) < 3:
            return {value}
        return {value[index:index + 3] for index in range(len(value) - 2)}
    left_grams, right_grams = grams(left), grams(right)
    ratio = (2.0 * len(left_grams & right_grams)) / (len(left_grams) + len(right_grams))
    length = min(len(left), len(right)) / max(len(left), len(right))
    return 0.85 * ratio + 0.15 * length


def align_records(records: list[dict], paragraphs, language: str, minimum: float = 0.48) -> list[dict]:
    candidates = [(index, paragraph_text(p)) for index, p in enumerate(paragraphs) if len(normalized_text(paragraph_text(p))) >= 35]
    n, m = len(records), len(candidates)
    neg = -10**9
    dp = [[neg] * (m + 1) for _ in range(n + 1)]
    take = [[False] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        dp[0][j] = 0.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i][j - 1]
            value = score(records[i - 1][language], candidates[j - 1][1], language)
            if value >= minimum and dp[i - 1][j - 1] > neg / 2 and dp[i - 1][j - 1] + value > dp[i][j]:
                dp[i][j] = dp[i - 1][j - 1] + value
                take[i][j] = True
    if dp[n][m] <= neg / 2:
        raise ValueError(f"Unable to align all {n} {language} source blocks")
    output = []
    i, j = n, m
    while i:
        if j <= 0:
            raise ValueError(f"Incomplete {language} alignment")
        if take[i][j]:
            index, text = candidates[j - 1]
            output.append({"id": records[i - 1]["id"], "paragraph_index": index, "score": score(records[i - 1][language], text, language)})
            i -= 1
            j -= 1
        else:
            j -= 1
    output.reverse()
    return output


def split_bilingual(value: str) -> tuple[str, str | None]:
    if " / " not in value:
        return value, None
    left, right = value.split(" / ", 1)
    return left.strip(), right.strip()


def section_for(identifier: str) -> str:
    return identifier.split(".", 1)[0]
