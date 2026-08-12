"""STEP 8 测试：结果汇总与基础错误分析。"""

import csv
import json
from pathlib import Path

from src.analysis.basic_error_analysis import run_basic_error_analysis
from src.analysis.candidate_set_diagnostics import run_candidate_set_diagnostics
from src.analysis.grouped_error_analysis import run_grouped_error_analysis, _write_csv
from src.analysis.phase2a_robustness_report import run_phase2a_robustness_report
from src.analysis.phase2b_result_synthesis import run_phase2b_result_synthesis
from src.analysis.phase2c_popmatch_grouped import run_phase2c_popmatch_grouped
from src.analysis.phase2c_result_summary import run_phase2c_result_summary
from src.analysis.prediction_file_clean import run_prediction_file_clean
from src.analysis.prediction_file_audit import run_prediction_file_audit
from src.analysis.sasrec_candidate_size_robustness import run_sasrec_candidate_size_robustness
from src.analysis.sasrec_grouped_diagnostics import run_sasrec_grouped_diagnostics
from src.analysis.summarize_results import run_result_summary
from src.analysis.threshold_calibration import run_threshold_calibration
from src.analysis.threshold_comparison import run_threshold_comparison


def test_result_summary_writes_csv_and_report(tmp_path):
    _write_config(tmp_path)
    _write_metrics_tree(tmp_path)

    summary = run_result_summary(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        n_run="run_n",
        m_run="run_m",
        splits=["test"],
        output_csv=tmp_path / "outputs" / "results.csv",
        report_path=tmp_path / "outputs" / "report.md",
    )

    rows = list(csv.DictReader((tmp_path / "outputs" / "results.csv").open()))

    assert summary["rows"] == 4
    assert [row["model"] for row in rows] == ["Base", "Y-K0", "N-K0", "M-K0"]
    assert rows[2]["binary_auc"] == ""
    assert rows[2]["hr_at_1"] == "0.7000000000"
    assert "MVP Results" in (tmp_path / "outputs" / "report.md").read_text(
        encoding="utf-8"
    )


def test_basic_error_analysis_writes_summaries_and_examples(tmp_path):
    _write_config(tmp_path)
    _write_prediction_tree(tmp_path)

    summary = run_basic_error_analysis(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        n_run="run_n",
        m_run="run_m",
        split_name="test",
        output_dir=tmp_path / "outputs" / "error_analysis" / "toy",
        example_limit=2,
    )

    output_dir = Path(summary["output_dir"])
    binary_rows = list(csv.DictReader((output_dir / "test_binary_error_summary.csv").open()))
    ranking_rows = list(csv.DictReader((output_dir / "test_ranking_error_summary.csv").open()))
    examples = [
        json.loads(line)
        for line in (output_dir / "test_error_examples.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert summary["binary_models"] == 3
    assert summary["ranking_models"] == 4
    assert binary_rows[0]["fp"] == "1"
    assert ranking_rows[0]["rank_distribution"] == '{"1": 1, "2": 1}'
    assert any(example["error_type"] == "ranking_miss" for example in examples)
    assert (output_dir / "test_error_analysis.md").exists()


def test_threshold_calibration_uses_validation_threshold_on_test(tmp_path):
    _write_config(tmp_path)
    _write_prediction_tree(tmp_path)
    _write_calibration_predictions(tmp_path)

    summary = run_threshold_calibration(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        m_runs=["run_m"],
        m_labels=["M1"],
        output_dir=tmp_path / "outputs" / "calibration" / "toy",
    )

    output_dir = Path(summary["output_dir"])
    rows = list(csv.DictReader((output_dir / "threshold_calibration.csv").open()))
    m_validation = next(row for row in rows if row["model"] == "M1" and row["split"] == "validation")
    m_test = next(row for row in rows if row["model"] == "M1" and row["split"] == "test")

    assert summary["models"] == 3
    assert m_validation["threshold"] == "0.4"
    assert m_validation["f1"] == "0.8"
    assert m_test["threshold"] == "0.4"
    assert m_test["f1"] == "1.0"
    assert m_test["fp"] == "0"
    assert (output_dir / "threshold_calibration.md").exists()


def test_threshold_comparison_writes_three_binary_tables(tmp_path):
    _write_config(tmp_path)
    _write_prediction_tree(tmp_path)
    _write_calibration_predictions(tmp_path)

    summary = run_threshold_comparison(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        m_runs=["run_m"],
        m_labels=["M1"],
        output_dir=tmp_path / "outputs" / "calibration" / "toy" / "comparison",
    )

    output_dir = Path(summary["output_dir"])
    auc_rows = list(csv.DictReader((output_dir / "binary_auc.csv").open()))
    fixed_rows = list(csv.DictReader((output_dir / "binary_fixed_0_5.csv").open()))
    calibrated_rows = list(csv.DictReader((output_dir / "binary_calibrated.csv").open()))
    m_fixed_test = next(row for row in fixed_rows if row["model"] == "M1" and row["split"] == "test")
    m_calibrated_test = next(
        row for row in calibrated_rows if row["model"] == "M1" and row["split"] == "test"
    )

    assert summary["models"] == 3
    assert summary["rows"] == {"auc": 6, "fixed_0_5": 6, "validation_calibrated": 6}
    assert len(auc_rows) == 6
    assert m_fixed_test["threshold"] == "0.5"
    assert m_fixed_test["f1"] == "0.0"
    assert m_calibrated_test["threshold"] == "0.4"
    assert m_calibrated_test["f1"] == "1.0"
    assert (output_dir / "threshold_comparison.md").exists()


def test_grouped_error_analysis_joins_metadata_and_writes_group_tables(tmp_path):
    _write_config(tmp_path)
    _write_prediction_tree(tmp_path)
    _write_grouped_metadata_tree(tmp_path)

    summary = run_grouped_error_analysis(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        y_run="run_y",
        n_run="run_n",
        m_runs=["run_m"],
        m_labels=["M1"],
        split_name="test",
        threshold_mode="fixed_0.5",
        output_dir=tmp_path / "outputs" / "error_analysis" / "toy" / "grouped",
    )

    output_dir = Path(summary["output_dir"])
    binary_rows = list(csv.DictReader((output_dir / "test_binary_group_metrics.csv").open()))
    ranking_rows = list(csv.DictReader((output_dir / "test_ranking_group_metrics.csv").open()))
    binary_all = next(row for row in binary_rows if row["model"] == "M1" and row["group_field"] == "all")
    binary_rating_5 = next(
        row
        for row in binary_rows
        if row["model"] == "M1"
        and row["group_field"] == "target_rating"
        and row["group_value"] == "5.0"
    )
    ranking_position_1 = next(
        row
        for row in ranking_rows
        if row["model"] == "N-K0"
        and row["group_field"] == "ground_truth_position"
        and row["group_value"] == "1"
    )

    assert summary["binary_models"] == 3
    assert summary["ranking_models"] == 4
    assert binary_all["samples"] == "2"
    assert binary_all["fp"] == "1"
    assert binary_rating_5["yes_labels"] == "1"
    assert ranking_position_1["samples"] == "1"
    assert ranking_position_1["hr_at_1"] == "0.0"
    assert (output_dir / "test_grouped_error_analysis.md").exists()


def test_candidate_set_diagnostics_writes_popularity_gap_summary(tmp_path):
    _write_config(tmp_path)
    _write_grouped_metadata_tree(tmp_path)

    summary = run_candidate_set_diagnostics(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        output_dir=tmp_path / "outputs" / "phase2c" / "toy" / "candidate_set_diagnostics",
        variant_name="toy_variant",
        splits=["test"],
    )

    output_dir = Path(summary["output_dir"])
    rows = list(csv.DictReader((output_dir / "candidate_set_diagnostics.csv").open()))
    payload = json.loads(
        (output_dir / "candidate_set_diagnostics.json").read_text(encoding="utf-8")
    )

    assert summary["rows"] == 1
    assert rows[0]["split"] == "test"
    assert rows[0]["variant_name"] == "toy_variant"
    assert rows[0]["samples"] == "2"
    assert rows[0]["mean_abs_popularity_gap"] == "1.0"
    assert payload["diagnostics"][0]["target_popularity_buckets"] == '{"<=10": 2}'
    assert (output_dir / "candidate_set_diagnostics.md").exists()


def test_phase2c_popmatch_grouped_writes_bucketed_ranking(tmp_path):
    _write_config(tmp_path)
    _write_grouped_metadata_tree(tmp_path)
    eval_dir = tmp_path / "outputs" / "phase2c" / "movielens-1m" / "popmatch_eval"
    _write_popmatch_eval_predictions(eval_dir)

    summary = run_phase2c_popmatch_grouped(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        split_name="test",
        candidate_file=tmp_path / "data" / "candidates" / "toy" / "test.jsonl",
        eval_dir=eval_dir,
        output_dir=tmp_path / "outputs" / "phase2c" / "toy" / "popmatch_grouped",
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    rows = list(csv.DictReader((output_dir / "test_ranking_by_target_popularity.csv").open()))
    n_row = next(row for row in rows if row["model"] == "N-K0" and row["group_value"] == "<=10")
    m1_row = next(row for row in rows if row["model"] == "M1" and row["group_value"] == "<=10")

    assert summary["models"] == 4
    assert n_row["samples"] == "2"
    assert n_row["HR@1"] == "1.0"
    assert m1_row["HR@1"] == "0.5"
    assert (output_dir / "test_ranking_by_target_popularity.md").exists()


def test_sasrec_grouped_diagnostics_computes_available_runs(tmp_path):
    _write_config(tmp_path)
    _write_grouped_metadata_tree(tmp_path)
    prediction_dir = tmp_path / "outputs" / "fair_budget"
    _write_jsonl(
        prediction_dir / "sasrec.jsonl",
        [
            _ranking_prediction_with_scores("sasrec", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
            _ranking_prediction_with_scores("sasrec", "u2", ["c", "d"], "d", 1, [0.7, 0.3]),
        ],
    )

    summary = run_sasrec_grouped_diagnostics(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        split_name="test",
        candidate_file=tmp_path / "data" / "candidates" / "toy" / "test.jsonl",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs={"SASRec s1500": prediction_dir / "sasrec.jsonl"},
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    rows = list(csv.DictReader((output_dir / "sasrec_grouped_diagnostics.csv").open()))
    payload = json.loads(
        (output_dir / "sasrec_grouped_diagnostics.json").read_text(encoding="utf-8")
    )

    assert summary["missing_runs"] == 0
    assert rows[0]["model"] == "SASRec s1500"
    assert rows[0]["HR@1"] == "0.5"
    assert payload["answers"]["sasrec_popularity_dependence"] == "not established"


def test_sasrec_grouped_diagnostics_marks_missing_runs(tmp_path):
    _write_config(tmp_path)
    _write_grouped_metadata_tree(tmp_path)

    summary = run_sasrec_grouped_diagnostics(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        split_name="test",
        candidate_file=tmp_path / "data" / "candidates" / "toy" / "test.jsonl",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs={"SASRec s1500": tmp_path / "missing.jsonl"},
    )

    rows = list(csv.DictReader(Path(summary["paths"]["csv"]).open()))
    report = Path(summary["paths"]["markdown"]).read_text(encoding="utf-8")

    assert summary["missing_runs"] == 1
    assert rows[0]["evidence_status"] == "missing_prediction_file"
    assert rows[0]["HR@1"] == "unavailable"
    assert "Do not interpret unavailable rows as negative results" in report


def test_sasrec_candidate_size_robustness_writes_metrics_and_deltas(tmp_path):
    _write_config(tmp_path)
    root = tmp_path / "outputs" / "fair_budget_inputs"
    runs = {
        "N-K0": {
            "k5": _write_candidate_size_run(root, "n_k5", 0.8, 1.0, 1.0, 0.9, 1.0, 0.9, ranks=[1, 2]),
            "k20": _write_candidate_size_run(root, "n_k20", 0.5, 0.9, 0.9, 0.7, 0.8, 0.6, ranks=[2, 3]),
            "k50": _write_candidate_size_run(root, "n_k50", 0.2, 0.5, 0.6, 0.4, 0.5, 0.3, ranks=[4, 5]),
        },
        "SASRec s3000": {
            "k5": _write_candidate_size_run(root, "s_k5", 0.9, 1.0, 1.0, 0.95, 1.0, 0.95, ranks=[1, 1]),
            "k20": _write_candidate_size_run(root, "s_k20", 0.7, 1.0, 1.0, 0.85, 0.9, 0.8, ranks=[1, 2]),
            "k50": _write_candidate_size_run(root, "s_k50", 0.4, 0.8, 0.9, 0.6, 0.7, 0.5, ranks=[2, 3]),
        },
    }

    summary = run_sasrec_candidate_size_robustness(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs=runs,
    )

    output_dir = Path(summary["paths"]["csv"]).parent
    metric_rows = list(csv.DictReader((output_dir / "sasrec_candidate_size_robustness.csv").open()))
    delta_rows = list(
        csv.DictReader((output_dir / "sasrec_candidate_size_robustness_deltas.csv").open())
    )
    payload = json.loads(
        (output_dir / "sasrec_candidate_size_robustness.json").read_text(encoding="utf-8")
    )

    assert summary["missing_metric_rows"] == 0
    assert metric_rows[0]["mean_rank"] == "1.5"
    n_k5_to_k50 = next(row for row in delta_rows if row["model"] == "N-K0" and row["comparison"] == "k5_to_k50")
    assert n_k5_to_k50["delta_HR@1"] == "-0.6"
    assert payload["answers"]["sasrec_degrades_with_candidate_size"] == "yes"


def test_sasrec_candidate_size_robustness_marks_missing_metrics(tmp_path):
    _write_config(tmp_path)

    summary = run_sasrec_candidate_size_robustness(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        output_dir=tmp_path / "outputs" / "fair_budget",
        runs={"SASRec s1500": {"k5": (tmp_path / "missing.json", tmp_path / "missing.jsonl"), "k20": (tmp_path / "missing2.json", tmp_path / "missing2.jsonl"), "k50": (tmp_path / "missing3.json", tmp_path / "missing3.jsonl")}},
    )

    rows = list(csv.DictReader(Path(summary["paths"]["csv"]).open()))
    report = Path(summary["paths"]["markdown"]).read_text(encoding="utf-8")

    assert summary["missing_metric_rows"] == 3
    assert rows[0]["evidence_status"] == "missing_metrics_file"
    assert rows[0]["HR@1"] == "unavailable"
    assert "unavailable until SASRec k5/k20/k50 eval metrics exist" in report


def test_phase2c_result_summary_writes_final_report(tmp_path):
    _write_config(tmp_path)
    eval_dir = tmp_path / "outputs" / "phase2c" / "toy" / "popmatch_eval_clean"
    grouped_dir = tmp_path / "outputs" / "phase2c" / "toy" / "popmatch_grouped"
    diagnostics_path = (
        tmp_path
        / "outputs"
        / "phase2c"
        / "toy"
        / "candidate_set_diagnostics"
        / "k5_popmatch_seed42"
        / "candidate_set_diagnostics.json"
    )
    _write_popmatch_metrics(eval_dir)
    _write_popmatch_grouped_csv(grouped_dir / "test_ranking_by_target_popularity.csv")
    _write_json(
        diagnostics_path,
        {
            "diagnostics": [
                {
                    "split": "test",
                    "method": "popularity_matched",
                    "samples": 2,
                    "mean_abs_popularity_gap": 4.5,
                }
            ]
        },
    )

    summary = run_phase2c_result_summary(
        config_path=tmp_path / "configs" / "experiment.yaml",
        dataset_key="toy",
        eval_dir=eval_dir,
        candidate_diagnostics_json=diagnostics_path,
        grouped_csv=grouped_dir / "test_ranking_by_target_popularity.csv",
        output_dir=tmp_path / "outputs" / "phase2c" / "toy" / "result_summary",
    )

    payload = json.loads(Path(summary["paths"]["json"]).read_text(encoding="utf-8"))
    report = Path(summary["paths"]["markdown"]).read_text(encoding="utf-8")

    assert payload["n_k0_minus_m1"][0]["delta"] == 0.1
    assert payload["bucket_n_k0_minus_m1"][0]["delta_HR@1"] == 0.2
    assert "Phase 2C is a diagnosis and consolidation stage" in report
    assert "N-K0 remains the strongest" in report


def test_prediction_file_audit_detects_safe_duplicates_and_rank_conflicts(tmp_path):
    input_dir = tmp_path / "outputs" / "phase2c" / "popmatch_eval"
    safe = [
        _ranking_prediction_with_scores("n_k0", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
        _ranking_prediction_with_scores("n_k0", "u1", ["a", "b"], "a", 0, [0.7, 0.3]),
    ]
    conflict = [
        _ranking_prediction_with_scores("m1", "u2", ["c", "d"], "d", 1, [0.8, 0.2]),
        _ranking_prediction_with_scores("m1", "u2", ["c", "d"], "d", 1, [0.2, 0.8]),
    ]
    binary = [
        _binary_prediction("base", "u3", "Yes", 0.9),
        _binary_prediction("base", "u3", "Yes", 0.8),
    ]
    _write_jsonl(input_dir / "n" / "n_test_predictions.jsonl", safe)
    _write_jsonl(input_dir / "m" / "m_n_test_predictions.jsonl", conflict)
    _write_jsonl(input_dir / "base" / "y_test_predictions.jsonl", binary)

    summary = run_prediction_file_audit(input_dir)

    rows = list(csv.DictReader((input_dir / "audit" / "prediction_file_audit.csv").open()))
    safe_row = next(
        row
        for row in rows
        if row["relative_path"].replace("\\", "/") == "n/n_test_predictions.jsonl"
    )
    conflict_row = next(
        row
        for row in rows
        if row["relative_path"].replace("\\", "/") == "m/m_n_test_predictions.jsonl"
    )
    binary_row = next(
        row
        for row in rows
        if row["relative_path"].replace("\\", "/") == "base/y_test_predictions.jsonl"
    )

    assert summary["files"] == 3
    assert safe_row["rows"] == "2"
    assert safe_row["unique_keys"] == "1"
    assert safe_row["rank_conflicts"] == "0"
    assert safe_row["safe_exact_rank_duplicates"] == "True"
    assert conflict_row["rank_conflicts"] == "1"
    assert binary_row["binary_rows"] == "2"
    assert (input_dir / "audit" / "prediction_file_audit.md").exists()


def test_prediction_file_clean_writes_deduplicated_copy(tmp_path):
    input_dir = tmp_path / "outputs" / "phase2c" / "popmatch_eval"
    output_dir = tmp_path / "outputs" / "phase2c" / "popmatch_eval_clean"
    _write_jsonl(
        input_dir / "n" / "n_test_predictions.jsonl",
        [
            _ranking_prediction_with_scores("n_k0", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
            _ranking_prediction_with_scores("n_k0", "u1", ["a", "b"], "a", 0, [0.7, 0.3]),
        ],
    )
    _write_jsonl(
        input_dir / "base" / "y_test_predictions.jsonl",
        [
            _binary_prediction("base", "u3", "Yes", 0.9),
            _binary_prediction("base", "u3", "Yes", 0.9),
        ],
    )

    summary = run_prediction_file_clean(input_dir, output_dir)

    n_rows = [
        json.loads(line)
        for line in (output_dir / "n" / "n_test_predictions.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    manifest_rows = list(csv.DictReader((output_dir / "prediction_file_clean_manifest.csv").open()))

    assert summary["files"] == 2
    assert len(n_rows) == 1
    assert sum(int(row["removed_rows"]) for row in manifest_rows) == 2


def test_prediction_file_clean_rejects_binary_score_conflicts(tmp_path):
    input_dir = tmp_path / "outputs" / "phase2c" / "popmatch_eval"
    _write_jsonl(
        input_dir / "base" / "y_test_predictions.jsonl",
        [
            _binary_prediction("base", "u3", "Yes", 0.9),
            _binary_prediction("base", "u3", "Yes", 0.8),
        ],
    )

    try:
        run_prediction_file_clean(input_dir, tmp_path / "clean")
    except ValueError as exc:
        assert "conflicting predictions" in str(exc)
    else:
        raise AssertionError("Expected binary duplicate score conflict")


def test_write_csv_accepts_dynamic_fields_after_first_row(tmp_path):
    output_path = tmp_path / "dynamic.csv"

    _write_csv(
        output_path,
        [
            {"model": "base", "hr_at_1": 0.1},
            {"model": "n_k0", "hr_at_1": 0.2, "hr_at_10": 0.8},
        ],
    )

    rows = list(csv.DictReader(output_path.open()))

    assert "hr_at_10" in rows[0]
    assert rows[0]["hr_at_10"] == ""
    assert rows[1]["hr_at_10"] == "0.8"


def test_phase2a_robustness_report_writes_variant_metrics_and_deltas(tmp_path):
    input_dir = tmp_path / "outputs" / "phase2a" / "ranking_robustness"
    _write_phase2a_metrics(input_dir)

    summary = run_phase2a_robustness_report(
        input_dir=input_dir,
        dataset_key="toy",
    )

    metrics_rows = list(csv.DictReader((input_dir / "phase2a_ranking_robustness_metrics.csv").open()))
    comparison_rows = list(csv.DictReader((input_dir / "phase2a_ranking_robustness_comparison.csv").open()))
    n_minus_m1 = next(
        row
        for row in comparison_rows
        if row["comparison"] == "n_k0_minus_m1"
        and row["variant"] == "k20_seed42"
    )

    assert summary["rows"] == 6
    assert metrics_rows[0]["model_key"] == "base"
    assert metrics_rows[0]["variant"] == "k20_seed42"
    assert n_minus_m1["delta_HR@1"] == "0.05"
    assert (input_dir / "phase2a_ranking_robustness_report.md").exists()


def test_phase2b_result_synthesis_writes_paper_ready_tables(tmp_path):
    inputs = _write_phase2b_inputs(tmp_path)

    summary = run_phase2b_result_synthesis(
        threshold_json=inputs["threshold_json"],
        grouped_json=inputs["grouped_json"],
        phase2a_metrics_json=inputs["phase2a_metrics_json"],
        phase2a_comparison_csv=inputs["phase2a_comparison_csv"],
        output_dir=tmp_path / "outputs" / "phase2b" / "result_synthesis",
        dataset_key="toy",
    )

    output_dir = Path(summary["output_dir"])
    binary_rows = list(csv.DictReader((output_dir / "phase2b_binary_calibrated_test.csv").open()))
    ranking_rows = list(csv.DictReader((output_dir / "phase2b_canonical_ranking_test.csv").open()))
    robustness_rows = list(csv.DictReader((output_dir / "phase2b_robustness_test.csv").open()))
    claims = json.loads((output_dir / "phase2b_paper_ready_claims.json").read_text(encoding="utf-8"))
    report = (output_dir / "phase2b_result_synthesis.md").read_text(encoding="utf-8")

    assert summary["rows"]["binary_calibrated_test"] == 2
    assert summary["rows"]["canonical_ranking_test"] == 2
    assert summary["rows"]["robustness_test"] == 4
    assert binary_rows[0]["model"] == "Y-K0"
    assert ranking_rows[0]["model"] == "N-K0"
    assert robustness_rows[0]["variant"] == "k20_seed42"
    assert any(claim["topic"] == "multi_task_ranking_boundary" for claim in claims)
    assert "Phase 2B Result Synthesis" in report
    assert "Do not claim that M1 surpasses" in report


def _write_config(root: Path) -> None:
    config_dir = root / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "experiment.yaml").write_text(
        "\n".join(
            [
                "dataset:",
                "  formal: toy",
                "outputs:",
                "  base: outputs/base/{dataset}",
                "  y: outputs/y/{dataset}",
                "  n: outputs/n/{dataset}",
                "  m: outputs/m/{dataset}",
                "  aggregate_results: outputs/results.csv",
                "processed_outputs:",
                "  full_sequences: data/processed/{dataset}/full_sequences.jsonl",
                "  preference_samples:",
                "    validation: data/processed/{dataset}/preference_valid.jsonl",
                "    test: data/processed/{dataset}/preference_test.jsonl",
                "  next_item_samples:",
                "    validation: data/processed/{dataset}/next_item_valid.jsonl",
                "    test: data/processed/{dataset}/next_item_test.jsonl",
                "candidates:",
                "  save_files:",
                "    validation: data/candidates/{dataset}/valid.jsonl",
                "    test: data/candidates/{dataset}/test.jsonl",
            ]
        ),
        encoding="utf-8",
    )


def _write_metrics_tree(root: Path) -> None:
    metrics = {
        "base": _metrics(binary_auc=0.6, hr_at_1=0.3),
        "y": _metrics(binary_auc=0.8, hr_at_1=0.25),
        "n": _metrics(binary_auc=None, hr_at_1=0.7),
        "m": _metrics(binary_auc=0.75, hr_at_1=0.65),
    }
    _write_json(root / "outputs" / "base" / "toy" / "test_metrics.json", metrics["base"])
    _write_json(root / "outputs" / "y" / "toy" / "run_y" / "test_metrics.json", metrics["y"])
    _write_json(root / "outputs" / "n" / "toy" / "run_n" / "test_metrics.json", metrics["n"])
    _write_json(root / "outputs" / "m" / "toy" / "run_m" / "test_metrics.json", metrics["m"])


def _write_phase2a_metrics(root: Path) -> None:
    rows = {
        "base_k20_seed42": (0.10, 0.30, 0.20),
        "base_k50_seed42": (0.05, 0.15, 0.10),
        "n_k0_k20_seed42": (0.40, 0.80, 0.60),
        "n_k0_k50_seed42": (0.20, 0.45, 0.32),
        "m1_k20_seed42": (0.35, 0.70, 0.53),
        "m1_k50_seed42": (0.12, 0.30, 0.23),
    }
    for run_dir, values in rows.items():
        hr_at_1, hr_at_5, mrr = values
        payload = {
            "model": run_dir.split("_k", 1)[0],
            "dataset": "toy",
            "split": "test",
            "ranking": {
                "HR@1": hr_at_1,
                "HR@5": hr_at_5,
                "NDCG@5": hr_at_5 - 0.1,
                "MRR": mrr,
                "samples": 2,
            },
        }
        _write_json(root / run_dir / "test_metrics.json", payload)


def _write_phase2b_inputs(root: Path) -> dict[str, Path]:
    threshold_json = root / "threshold_comparison.json"
    grouped_json = root / "test_grouped_error_analysis.json"
    phase2a_metrics_json = root / "phase2a_ranking_robustness_metrics.json"
    phase2a_comparison_csv = root / "phase2a_ranking_robustness_comparison.csv"

    _write_json(
        threshold_json,
        {
            "dataset": "toy",
            "tables": {
                "validation_calibrated": [
                    {
                        "model": "Y-K0",
                        "run_name": "run_y",
                        "split": "test",
                        "threshold": 0.4,
                        "auc": 0.78,
                        "f1": 0.80,
                        "accuracy": 0.70,
                        "precision": 0.72,
                        "recall": 0.89,
                        "fp": 3,
                        "fn": 1,
                    },
                    {
                        "model": "M1",
                        "run_name": "run_m1",
                        "split": "test",
                        "threshold": 0.32,
                        "auc": 0.77,
                        "f1": 0.79,
                        "accuracy": 0.71,
                        "precision": 0.74,
                        "recall": 0.86,
                        "fp": 2,
                        "fn": 2,
                    },
                ]
            },
        },
    )
    _write_json(
        grouped_json,
        {
            "dataset": "toy",
            "split": "test",
            "ranking": [
                {
                    "model": "N-K0",
                    "run_name": "run_n",
                    "split": "test",
                    "group_field": "all",
                    "group_value": "ALL",
                    "samples": 2,
                    "hr_at_1": 0.72,
                    "hr_at_5": 1.0,
                    "ndcg_at_5": 0.88,
                    "mrr": 0.84,
                    "mean_rank": 1.4,
                    "mean_margin": 0.37,
                },
                {
                    "model": "M1",
                    "run_name": "run_m1",
                    "split": "test",
                    "group_field": "all",
                    "group_value": "ALL",
                    "samples": 2,
                    "hr_at_1": 0.69,
                    "hr_at_5": 1.0,
                    "ndcg_at_5": 0.86,
                    "mrr": 0.82,
                    "mean_rank": 1.5,
                    "mean_margin": 0.33,
                },
            ],
        },
    )
    _write_json(
        phase2a_metrics_json,
        [
            _phase2a_metric_row("n_k0", "k20_seed42", 0.42, 0.79, 0.58),
            _phase2a_metric_row("m1", "k20_seed42", 0.37, 0.70, 0.53),
            _phase2a_metric_row("n_k0", "k50_seed42", 0.20, 0.44, 0.32),
            _phase2a_metric_row("m1", "k50_seed42", 0.12, 0.31, 0.23),
        ],
    )
    _write_csv_rows(
        phase2a_comparison_csv,
        [
            {
                "comparison": "n_k0_minus_m1",
                "variant": "k20_seed42",
                "delta_HR@1": 0.05,
                "delta_HR@5": 0.09,
                "delta_NDCG@5": 0.07,
                "delta_MRR": 0.05,
            },
            {
                "comparison": "n_k0_k50_minus_k20",
                "variant": "candidate_size",
                "delta_HR@1": -0.22,
                "delta_HR@5": -0.35,
                "delta_NDCG@5": -0.29,
                "delta_MRR": -0.26,
            },
        ],
    )
    return {
        "threshold_json": threshold_json,
        "grouped_json": grouped_json,
        "phase2a_metrics_json": phase2a_metrics_json,
        "phase2a_comparison_csv": phase2a_comparison_csv,
    }


def _phase2a_metric_row(model_key: str, variant: str, hr_at_1: float, hr_at_5: float, mrr: float):
    return {
        "model_key": model_key,
        "variant": variant,
        "split": "test",
        "samples": 2,
        "HR@1": hr_at_1,
        "HR@5": hr_at_5,
        "NDCG@5": hr_at_5 - 0.1,
        "MRR": mrr,
    }


def _write_csv_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _metrics(binary_auc, hr_at_1):
    payload = {
        "model": "model",
        "dataset": "toy",
        "split": "test",
        "ranking": {
            "HR@1": hr_at_1,
            "HR@5": 1.0,
            "NDCG@5": 0.8,
            "MRR": 0.75,
            "samples": 2,
        },
    }
    if binary_auc is not None:
        payload["binary"] = {
            "AUC": binary_auc,
            "F1": 0.7,
            "Accuracy": 0.65,
            "samples": 2,
        }
    return payload


def _write_prediction_tree(root: Path) -> None:
    _write_jsonl(
        root / "outputs" / "base" / "toy" / "y_test_predictions.jsonl",
        _binary_predictions("base"),
    )
    _write_jsonl(
        root / "outputs" / "base" / "toy" / "n_test_predictions.jsonl",
        _ranking_predictions("base"),
    )
    _write_jsonl(
        root / "outputs" / "y" / "toy" / "run_y" / "y_test_predictions.jsonl",
        _binary_predictions("y_k0"),
    )
    _write_jsonl(
        root / "outputs" / "y" / "toy" / "run_y" / "n_test_predictions.jsonl",
        _ranking_predictions("y_k0"),
    )
    _write_jsonl(
        root / "outputs" / "n" / "toy" / "run_n" / "n_test_predictions.jsonl",
        _ranking_predictions("n_k0"),
    )
    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_y_test_predictions.jsonl",
        _binary_predictions("m_k0"),
    )
    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_n_test_predictions.jsonl",
        _ranking_predictions("m_k0"),
    )


def _write_calibration_predictions(root: Path) -> None:
    for path in [
        root / "outputs" / "base" / "toy" / "y_valid_predictions.jsonl",
        root / "outputs" / "y" / "toy" / "run_y" / "y_valid_predictions.jsonl",
    ]:
        _write_jsonl(path, _binary_predictions("calibration_ref"))

    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_y_valid_predictions.jsonl",
        [
            _binary_prediction("m_k0", "u1", "Yes", 0.4),
            _binary_prediction("m_k0", "u2", "Yes", 0.45),
            _binary_prediction("m_k0", "u3", "No", 0.3),
            _binary_prediction("m_k0", "u4", "No", 0.6),
        ],
    )
    _write_jsonl(
        root / "outputs" / "m" / "toy" / "run_m" / "m_y_test_predictions.jsonl",
        [
            _binary_prediction("m_k0", "u5", "Yes", 0.42),
            _binary_prediction("m_k0", "u6", "No", 0.35),
        ],
    )


def _write_grouped_metadata_tree(root: Path) -> None:
    _write_jsonl(
        root / "data" / "processed" / "toy" / "full_sequences.jsonl",
        [
            {
                "user_id": "u1",
                "interactions": [
                    _interaction("h1", 4, 1, 0),
                    _interaction("m1", 5, 2, 1),
                    _interaction("a", 5, 3, 2),
                ],
            },
            {
                "user_id": "u2",
                "interactions": [
                    _interaction("h2", 2, 1, 0),
                    _interaction("m2", 2, 2, 1),
                    _interaction("d", 3, 3, 2),
                ],
            },
        ],
    )
    _write_jsonl(
        root / "data" / "processed" / "toy" / "preference_test.jsonl",
        [
            _preference_sample("u1", "m1", "Yes", 5, [_interaction("h1", 4, 1, 0)]),
            _preference_sample("u2", "m2", "No", 2, [_interaction("h2", 2, 1, 0)]),
        ],
    )
    _write_jsonl(
        root / "data" / "candidates" / "toy" / "test.jsonl",
        [
            _candidate_sample("u1", ["a", "b"], "a", 0, 5),
            _candidate_sample("u2", ["c", "d"], "d", 1, 3),
        ],
    )


def _write_popmatch_eval_predictions(root: Path) -> None:
    rows_by_run = {
        "base_k5_popmatch_seed42/n_test_predictions.jsonl": [
            _ranking_prediction_with_scores("base", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
            _ranking_prediction_with_scores("base", "u2", ["c", "d"], "d", 1, [0.7, 0.3]),
        ],
        "n_k0_k5_popmatch_seed42/n_test_predictions.jsonl": [
            _ranking_prediction_with_scores("n_k0", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
            _ranking_prediction_with_scores("n_k0", "u2", ["c", "d"], "d", 1, [0.3, 0.7]),
        ],
        "m1_k5_popmatch_seed42/m_n_test_predictions.jsonl": [
            _ranking_prediction_with_scores("m1", "u1", ["a", "b"], "a", 0, [0.8, 0.2]),
            _ranking_prediction_with_scores("m1", "u2", ["c", "d"], "d", 1, [0.7, 0.3]),
        ],
        "y_k0_k5_popmatch_seed42/n_test_predictions.jsonl": [
            _ranking_prediction_with_scores("y_k0", "u1", ["a", "b"], "a", 0, [0.2, 0.8]),
            _ranking_prediction_with_scores("y_k0", "u2", ["c", "d"], "d", 1, [0.7, 0.3]),
        ],
    }
    for path, rows in rows_by_run.items():
        _write_jsonl(root / path, rows)


def _write_popmatch_metrics(root: Path) -> None:
    rows = {
        "base_k5_popmatch_seed42/test_metrics.json": (0.3, 0.6, 0.5, 0.62, 0.70),
        "n_k0_k5_popmatch_seed42/test_metrics.json": (0.6, 0.8, 0.7, None, None),
        "m1_k5_popmatch_seed42/test_metrics.json": (0.5, 0.75, 0.65, 0.76, 0.73),
        "y_k0_k5_popmatch_seed42/test_metrics.json": (0.2, 0.55, 0.4, 0.77, 0.78),
    }
    for path, values in rows.items():
        hr_at_1, ndcg_at_5, mrr, auc, f1 = values
        payload = {
            "ranking": {
                "HR@1": hr_at_1,
                "NDCG@5": ndcg_at_5,
                "MRR": mrr,
            }
        }
        if auc is not None:
            payload["binary"] = {"AUC": auc, "F1": f1}
        _write_json(root / path, payload)


def _write_popmatch_grouped_csv(path: Path) -> None:
    _write_csv_rows(
        path,
        [
            {
                "model": "N-K0",
                "group_value": "<=10",
                "samples": 2,
                "HR@1": 0.7,
                "NDCG@5": 0.8,
                "MRR": 0.75,
            },
            {
                "model": "M1",
                "group_value": "<=10",
                "samples": 2,
                "HR@1": 0.5,
                "NDCG@5": 0.7,
                "MRR": 0.65,
            },
        ],
    )


def _write_candidate_size_run(
    root: Path,
    run_name: str,
    hr_at_1: float,
    hr_at_5: float,
    hr_at_10: float,
    ndcg_at_5: float,
    ndcg_at_10: float,
    mrr: float,
    ranks: list[int],
):
    run_dir = root / run_name
    _write_json(
        run_dir / "test_metrics.json",
        {
            "ranking": {
                "HR@1": hr_at_1,
                "HR@5": hr_at_5,
                "HR@10": hr_at_10,
                "NDCG@5": ndcg_at_5,
                "NDCG@10": ndcg_at_10,
                "MRR": mrr,
                "samples": len(ranks),
            }
        },
    )
    prediction_rows = []
    for rank in ranks:
        scores = [1.0 - index * 0.01 for index in range(max(10, rank + 1))]
        ground_truth_index = rank - 1
        prediction_rows.append(
            _ranking_prediction_with_scores(
                "model",
                f"u{rank}",
                [str(index) for index in range(len(scores))],
                str(ground_truth_index),
                ground_truth_index,
                scores,
            )
        )
    _write_jsonl(run_dir / "n_test_predictions.jsonl", prediction_rows)
    return run_dir / "test_metrics.json", run_dir / "n_test_predictions.jsonl"


def _preference_sample(user_id: str, movie_id: str, label: str, rating: float, history: list[dict]):
    return {
        "task": "Y",
        "user_id": user_id,
        "split": "test",
        "history": history,
        "target": _interaction(movie_id, rating, 10, 2),
        "label": label,
    }


def _candidate_sample(
    user_id: str,
    candidate_movie_ids: list[str],
    ground_truth_movie_id: str,
    ground_truth_index: int,
    rating: float,
):
    return {
        "task": "N",
        "user_id": user_id,
        "split": "test",
        "history": [_interaction(f"h-{user_id}", 4, 1, 0)],
        "target": _interaction(ground_truth_movie_id, rating, 10, 2),
        "candidate_movie_ids": candidate_movie_ids,
        "ground_truth_movie_id": ground_truth_movie_id,
        "ground_truth_index": ground_truth_index,
        "label": "A" if ground_truth_index == 0 else "B",
    }


def _interaction(movie_id: str, rating: float, timestamp: int, sequence_index: int):
    return {
        "user_id": "u",
        "movie_id": movie_id,
        "rating": float(rating),
        "timestamp": timestamp,
        "title": f"Movie {movie_id}",
        "sequence_index": sequence_index,
    }


def _binary_prediction(model: str, user_id: str, label: str, p_yes: float):
    return {
        "model": model,
        "task": "Y",
        "split": "test",
        "user_id": user_id,
        "target_movie_id": f"m-{user_id}",
        "label": label,
        "p_yes": p_yes,
        "predicted_label": "Yes" if p_yes >= 0.5 else "No",
    }


def _binary_predictions(model: str):
    return [
        {
            "model": model,
            "task": "Y",
            "split": "test",
            "user_id": "u1",
            "target_movie_id": "m1",
            "label": "Yes",
            "p_yes": 0.9,
            "predicted_label": "Yes",
        },
        {
            "model": model,
            "task": "Y",
            "split": "test",
            "user_id": "u2",
            "target_movie_id": "m2",
            "label": "No",
            "p_yes": 0.8,
            "predicted_label": "Yes",
        },
    ]


def _ranking_predictions(model: str):
    return [
        {
            "model": model,
            "task": "N",
            "split": "test",
            "user_id": "u1",
            "candidate_movie_ids": ["a", "b"],
            "ground_truth_movie_id": "a",
            "ground_truth_index": 0,
            "scores": [0.9, 0.1],
        },
        {
            "model": model,
            "task": "N",
            "split": "test",
            "user_id": "u2",
            "candidate_movie_ids": ["c", "d"],
            "ground_truth_movie_id": "d",
            "ground_truth_index": 1,
            "scores": [0.7, 0.3],
        },
    ]


def _ranking_prediction_with_scores(
    model: str,
    user_id: str,
    candidate_movie_ids: list[str],
    ground_truth_movie_id: str,
    ground_truth_index: int,
    scores: list[float],
):
    return {
        "model": model,
        "task": "N",
        "split": "test",
        "user_id": user_id,
        "candidate_movie_ids": candidate_movie_ids,
        "ground_truth_movie_id": ground_truth_movie_id,
        "ground_truth_index": ground_truth_index,
        "scores": scores,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )
