"""Aggregate frozen MS96 summaries; no model evaluation or statistical tests."""
import argparse
import csv
import hashlib
import io
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FROZEN = ROOT / ".agent/exposure_scaling/final_evidence"
IMPORTED = ROOT / ".agent/ms96_integration/imported/a9c6cd9/artifacts/multiseed96"
COMMIT = "a9c6cd959cf32afe046bb05be9eb5096bebfc5fb"
BINARY = ("AUC", "F1", "Accuracy")
RANKING = ("HR@1", "NDCG@5", "MRR")
PROTOCOLS = ("k5", "k20_seed42", "k50_seed42")


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def read_sections(path):
    sections, lines = [], []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("=="):
            if lines:
                sections.append(list(csv.DictReader(lines, delimiter="\t")))
            lines = []
        elif line.strip():
            lines.append(line)
    if lines:
        sections.append(list(csv.DictReader(lines, delimiter="\t")))
    if len(sections) != 2:
        raise ValueError(f"Expected two TSV sections: {path}")
    return sections


def load_records():
    records = []
    sources = set()

    def add(seed, split, model, interface, protocol, values, source, samples=""):
        keys = BINARY if interface == "Y" else RANKING
        for metric in keys:
            raw = str(values[metric])
            value = float(raw)
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError((seed, split, model, metric, raw))
            records.append(dict(training_seed=seed, split=split, model=model,
                                interface=interface, protocol=protocol,
                                candidate_seed="" if interface == "Y" else 42,
                                samples=samples, metric=metric, value=raw,
                                source=source.relative_to(ROOT).as_posix()))
        sources.add(source)

    main = FROZEN / "exposure_main_table.csv"
    for row in read_csv(main):
        if row["run"] not in ("Y96", "M1-96") or "binary" not in row["task"]:
            continue
        values = json.loads(row["secondary_metrics"])
        values[row["primary_metric"]] = row["primary_value"]
        add(42, row["split"], row["run"], "Y", "binary", values, main)
    hard = FROZEN / "tables/table_hard_candidate.csv"
    groups = {}
    for row in read_csv(hard):
        protocol = row["candidate_protocol"]
        if protocol != "k5":
            protocol += "_seed42"
        for model, col in (("N96", "N96_value"), ("M1-96", "M1-96_value")):
            groups.setdefault((row["split"], model, protocol), {})[row["metric"]] = row[col]
    for (split, model, protocol), values in groups.items():
        add(42, split, model, "N", protocol, values, hard)

    for seed in (43, 44):
        for split, filename in (("validation", "validation_summary.txt"), ("test", "test_summary.txt")):
            path = IMPORTED / f"seed{seed}" / filename
            base, alternatives = read_sections(path)
            if len(base) != 3 or len(alternatives) != 4:
                raise ValueError(f"Incomplete summary: {path}")
            ranking_count = next(int(r["samples"]) for r in base if r["run"] == "N96")
            for row in base + alternatives:
                if int(row["seed"]) != seed or row.get("split", split) != split:
                    raise ValueError(f"Seed/split mismatch: {path}")
            for row in base:
                model = row["run"]
                if model in ("Y96", "M1-96"):
                    expected = 12381 if split == "validation" else 11544
                    if int(row["samples"]) != expected:
                        raise ValueError(f"Binary sample count: {path}")
                    add(seed, split, model, "Y", "binary", row, path, expected)
                if model in ("N96", "M1-96"):
                    # The mixed summary's M1 samples column describes Y, not ranking.
                    add(seed, split, model, "N", "k5", row, path, ranking_count)
            for row in alternatives:
                if row["variant"] not in PROTOCOLS[1:] or int(row["samples"]) != ranking_count:
                    raise ValueError(f"Protocol/sample mismatch: {path}")
                add(seed, split, row["run"], "N", row["variant"], row, path, ranking_count)
        duplicate = IMPORTED / f"seed{seed}" / "summary.txt"
        if duplicate.read_text() != (duplicate.parent / "validation_summary.txt").read_text():
            raise ValueError(f"Unexpected validation duplicate: {duplicate}")
    keys = [(r["training_seed"], r["split"], r["model"], r["interface"], r["protocol"], r["metric"])
            for r in records]
    if len(keys) != 144 or len(set(keys)) != 144:
        raise ValueError("MS96 coverage must contain 144 unique native metric records")
    return records, sorted(sources)


def csv_text(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def build_outputs():
    records, sources = load_records()
    lookup = {(r["training_seed"], r["split"], r["model"], r["interface"], r["protocol"], r["metric"]): r
              for r in records}

    def value(seed, split, model, interface, protocol, metric):
        return lookup[seed, split, model, interface, protocol, metric]["value"]

    outputs, deltas = {}, []
    for split in ("validation", "test"):
        main, protocol_rows = [], []
        for seed in (42, 43, 44):
            row = {"training_seed": seed}
            for model, label, interface, protocol, metrics in (
                ("Y96", "Y96", "Y", "binary", BINARY),
                ("M1-96", "M1-Y", "Y", "binary", BINARY),
                ("N96", "N96", "N", "k5", RANKING),
                ("M1-96", "M1-N", "N", "k5", RANKING),
            ):
                for metric in metrics:
                    row[f"{label}_{metric}"] = value(seed, split, model, interface, protocol, metric)
            main.append(row)
            for protocol in ("binary",) + PROTOCOLS:
                interface = "Y" if protocol == "binary" else "N"
                metrics = BINARY if interface == "Y" else RANKING
                prow = dict(training_seed=seed, protocol=protocol)
                for metric in metrics:
                    specialist = value(seed, split, "Y96" if interface == "Y" else "N96",
                                       interface, protocol, metric)
                    multitask = value(seed, split, "M1-96", interface, protocol, metric)
                    delta = (float(multitask) - float(specialist) if interface == "Y"
                             else float(specialist) - float(multitask))
                    deltas.append(dict(training_seed=seed, split=split, protocol=protocol,
                                       metric=metric, specialist_value=specialist,
                                       multitask_value=multitask, delta=delta,
                                       delta_definition="M1-Y - Y96" if interface == "Y" else "N96 - M1-N"))
                    if interface == "N":
                        prow[f"N_{metric}"] = specialist
                        prow[f"M_{metric}"] = multitask
                        prow[f"delta_{metric}"] = delta
                if interface == "N":
                    protocol_rows.append(prow)
        outputs[f"paper/tables/ms96_main_{split}.csv"] = csv_text(main)
        outputs[f"paper/tables/ms96_protocol_{split}.csv"] = csv_text(protocol_rows)
    summary = []
    for split in ("validation", "test"):
        for protocol in ("binary",) + PROTOCOLS:
            for metric in BINARY if protocol == "binary" else RANKING:
                group = [r for r in deltas if (r["split"], r["protocol"], r["metric"]) == (split, protocol, metric)]
                values = [r["delta"] for r in group]
                summary.append(dict(split=split, protocol=protocol, metric=metric,
                                    delta_definition=group[0]["delta_definition"],
                                    mean=statistics.mean(values), sample_std=statistics.stdev(values),
                                    n_training_seeds=3, ddof=1, minimum=min(values), maximum=max(values)))
    outputs["paper/tables/ms96_delta_summary.csv"] = csv_text(summary)
    outputs["paper/evidence/ms96_raw_metrics.csv"] = csv_text(records)
    outputs["paper/evidence/ms96_per_seed_deltas.csv"] = csv_text(deltas)
    provenance = dict(commit=COMMIT, aggregate="equal seed weight; sample std ddof=1; n=3; descriptive only",
                      seed42_precision="Frozen point estimates retained; original bootstrap deltas/CIs unchanged.",
                      count_note="Blank seed42 counts are unavailable in these metric sources, not zero. M1 mixed-summary samples belong to binary Y.",
                      excluded="Y-as-ranker bridge columns and duplicate summary.txt are not additional native-task observations.",
                      sources=[dict(path=p.relative_to(ROOT).as_posix(),
                                    sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources])
    outputs["paper/evidence/ms96_data_provenance.json"] = json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated files without writing.")
    args = parser.parse_args()
    outputs = build_outputs()
    mismatches = []
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                mismatches.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if mismatches:
        raise SystemExit("Stale/missing: " + ", ".join(mismatches))
    print(f"{'Checked' if args.check else 'Generated'} {len(outputs)} MS96 data artifacts; no inference or resampling.")


if __name__ == "__main__":
    main()
