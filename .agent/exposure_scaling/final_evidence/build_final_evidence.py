from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".agent/exposure_scaling/final_evidence"
FIG = OUT / "figures"
FDATA = FIG / "data"
TABLES = OUT / "tables"
COLORS = ["#0077BB", "#EE7733", "#009988", "#CC3311", "#EE3377"]

Y_BINARY = [
    {"run":"Y24","family":"Y-K0","exposure":24000,"split":"validation","samples":12381,"AUC":0.7761274819,"F1":0.7791746032,"Accuracy":0.7190856958},
    {"run":"Y24","family":"Y-K0","exposure":24000,"split":"test","samples":11544,"AUC":0.7784561583,"F1":0.7793987922,"Accuracy":0.7183818434},
    {"run":"Y48","family":"Y-K0","exposure":48000,"split":"validation","samples":12381,"AUC":0.7816111073,"F1":0.7848403087,"Accuracy":0.7230433729},
    {"run":"Y48","family":"Y-K0","exposure":48000,"split":"test","samples":11544,"AUC":0.7804671174,"F1":0.7815520945,"Accuracy":0.7181219681},
    {"run":"Y96","family":"Y-K0","exposure":96000,"split":"validation","samples":12381,"AUC":0.7843504067,"F1":0.7783174665,"Accuracy":0.7235279864},
    {"run":"Y96","family":"Y-K0","exposure":96000,"split":"test","samples":11544,"AUC":0.7853511126,"F1":0.7780238029,"Accuracy":0.7221067221},
]

Y_RANK = [
    {"run":"Y24","family":"Y-K0","exposure":24000,"split":"validation","samples":5675,"HR@1":0.2156828194,"HR@5":1.0,"NDCG@5":0.6002715889,"MRR":0.4704082232},
    {"run":"Y24","family":"Y-K0","exposure":24000,"split":"test","samples":5675,"HR@1":0.2045814978,"HR@5":1.0,"NDCG@5":0.5936288326,"MRR":0.4617444934},
    {"run":"Y48","family":"Y-K0","exposure":48000,"split":"validation","samples":5675,"HR@1":0.2165638767,"HR@5":1.0,"NDCG@5":0.5994649797,"MRR":0.4694772394},
    {"run":"Y48","family":"Y-K0","exposure":48000,"split":"test","samples":5675,"HR@1":0.2,"HR@5":1.0,"NDCG@5":0.5899793848,"MRR":0.4570337739},
    {"run":"Y96","family":"Y-K0","exposure":96000,"split":"validation","samples":5675,"HR@1":0.2211453744,"HR@5":1.0,"NDCG@5":0.6030699894,"MRR":0.4741791483},
    {"run":"Y96","family":"Y-K0","exposure":96000,"split":"test","samples":5675,"HR@1":0.2065198238,"HR@5":1.0,"NDCG@5":0.5921565513,"MRR":0.4600528634},
]

N_RANK = [
    {"run":"N24","family":"N-K0","exposure":24000,"split":"validation","samples":5675,"HR@1":0.5774449339,"HR@5":1.0,"NDCG@5":0.8067686847,"MRR":0.7420058737},
    {"run":"N24","family":"N-K0","exposure":24000,"split":"test","samples":5675,"HR@1":0.5612334802,"HR@5":1.0,"NDCG@5":0.7968087155,"MRR":0.7289720999},
    {"run":"N48","family":"N-K0","exposure":48000,"split":"validation","samples":5675,"HR@1":0.6029955947,"HR@5":1.0,"NDCG@5":0.8200163654,"MRR":0.7595418502},
    {"run":"N48","family":"N-K0","exposure":48000,"split":"test","samples":5675,"HR@1":0.5869603524,"HR@5":1.0,"NDCG@5":0.8106805727,"MRR":0.7472687225},
    {"run":"N96","family":"N-K0","exposure":96000,"split":"validation","samples":5675,"HR@1":0.6237885463,"HR@5":1.0,"NDCG@5":0.8302923694,"MRR":0.7732422907},
    {"run":"N96","family":"N-K0","exposure":96000,"split":"test","samples":5675,"HR@1":0.6100440529,"HR@5":1.0,"NDCG@5":0.8218966233,"MRR":0.7622026432},
    {"run":"N200","family":"N-K0","exposure":200000,"split":"validation","samples":5675,"HR@1":0.6516299559,"HR@5":1.0,"NDCG@5":0.8431902590,"MRR":0.7904170338},
    {"run":"N200","family":"N-K0","exposure":200000,"split":"test","samples":5675,"HR@1":0.6281938326,"HR@5":1.0,"NDCG@5":0.8318910144,"MRR":0.7753803231},
]

M_BINARY = [
    {"run":"M1-48","family":"M1","exposure":"Y48k+N48k","split":"validation","samples":12381,"AUC":0.7813698559,"F1":0.7496657048,"Accuracy":0.7127049511},
    {"run":"M1-48","family":"M1","exposure":"Y48k+N48k","split":"test","samples":11544,"AUC":0.7757951608,"F1":0.7472278796,"Accuracy":0.7097193347},
    {"run":"M1-96","family":"M1","exposure":"Y96k+N96k","split":"validation","samples":12381,"AUC":0.7868352749,"F1":0.7838427948,"Accuracy":0.7281318149},
    {"run":"M1-96","family":"M1","exposure":"Y96k+N96k","split":"test","samples":11544,"AUC":0.7864837284,"F1":0.7835646558,"Accuracy":0.7271309771},
]

M_RANK = [
    {"run":"M1-48","family":"M1","exposure":"Y48k+N48k","n_exposure":48000,"split":"validation","samples":5675,"HR@1":0.5941850220,"HR@5":1.0,"NDCG@5":0.8153243950,"MRR":0.7533392070},
    {"run":"M1-48","family":"M1","exposure":"Y48k+N48k","n_exposure":48000,"split":"test","samples":5675,"HR@1":0.5776211454,"HR@5":1.0,"NDCG@5":0.8060951596,"MRR":0.7411953010},
    {"run":"M1-96","family":"M1","exposure":"Y96k+N96k","n_exposure":96000,"split":"validation","samples":5675,"HR@1":0.6234361233,"HR@5":1.0,"NDCG@5":0.8291402759,"MRR":0.7717533040},
    {"run":"M1-96","family":"M1","exposure":"Y96k+N96k","n_exposure":96000,"split":"test","samples":5675,"HR@1":0.5973568282,"HR@5":1.0,"NDCG@5":0.8162307888,"MRR":0.7546490455},
]

BINARY_BOOT = [
    {"split":"validation","metric":"AUC","delta_definition":"M1-96 - Y96","point_estimate":0.0024848682173134184,"ci95_low":-0.0016706848975658439,"ci95_high":0.0067379230946188395,"p_delta_gt_0":0.8792},
    {"split":"validation","metric":"F1","delta_definition":"M1-96 - Y96","point_estimate":0.005525328274494035,"ci95_low":0.0009575692122464174,"ci95_high":0.010251789726088258,"p_delta_gt_0":0.9922},
    {"split":"validation","metric":"Accuracy","delta_definition":"M1-96 - Y96","point_estimate":0.004603828446813729,"ci95_low":-0.0008861776707727864,"ci95_high":0.010352412318731543,"p_delta_gt_0":0.9498},
    {"split":"test","metric":"AUC","delta_definition":"M1-96 - Y96","point_estimate":0.001132615770464307,"ci95_low":-0.003070054947687045,"ci95_high":0.0053384946117852545,"p_delta_gt_0":0.7074},
    {"split":"test","metric":"F1","delta_definition":"M1-96 - Y96","point_estimate":0.005540852830888232,"ci95_low":0.00046366580587256235,"ci95_high":0.01040823902745689,"p_delta_gt_0":0.9834},
    {"split":"test","metric":"Accuracy","delta_definition":"M1-96 - Y96","point_estimate":0.005024255024255075,"ci95_low":-0.0011198256525702943,"ci95_high":0.010976803508002965,"p_delta_gt_0":0.9434},
]

RANK_BOOT = [
    ("k5","validation","HR@1",0.0003524229074889868,-0.01039647577092511,0.011277533039647578,0.5174),
    ("k5","validation","NDCG@5",0.0011520935050120533,-0.0033722416192506223,0.005810551214506837,0.6768),
    ("k5","validation","MRR",0.0014889867841409688,-0.004569897209985313,0.007692143906020559,0.6692),
    ("k5","test","HR@1",0.012687224669603524,0.0015859030837004405,0.02378854625550661,0.988),
    ("k5","test","NDCG@5",0.005665834482332085,0.001042457002734931,0.010430093540528913,0.9904),
    ("k5","test","MRR",0.007553597650513948,0.001403597650513949,0.013929515418502184,0.9904),
    ("k20","validation","HR@1",0.11242290748898678,0.10185022026431718,0.12317180616740088,1.0),
    ("k20","validation","NDCG@5",0.1269794215501796,0.11911045598508378,0.1352631639466986,1.0),
    ("k20","validation","MRR",0.10625608014912585,0.09889481292943336,0.11407883680497348,1.0),
    ("k20","test","HR@1",0.1147136563876652,0.10396475770925111,0.12511013215859032,1.0),
    ("k20","test","NDCG@5",0.12593254339740279,0.11801060700427189,0.1338827845812851,1.0),
    ("k20","test","MRR",0.1058693093638676,0.0982253508948069,0.11335615196078587,1.0),
    ("k50","validation","HR@1",0.01709251101321586,0.012511013215859032,0.02185022026431718,1.0),
    ("k50","validation","NDCG@5",0.02895557663648938,0.024912669476297652,0.033072320269894664,1.0),
    ("k50","validation","MRR",0.025829360157151742,0.02242519693620818,0.029333196745337603,1.0),
    ("k50","test","HR@1",0.013920704845814978,0.009162995594713657,0.018854625550660795,1.0),
    ("k50","test","NDCG@5",0.02777808077651262,0.023997519292228164,0.03185254783465271,1.0),
    ("k50","test","MRR",0.023417998574650413,0.019881029270194986,0.027061761052627413,1.0),
]
RANK_BOOT = [{"variant":a,"split":b,"metric":c,"delta_definition":"N96 - M1-96","point_estimate":d,"ci95_low":e,"ci95_high":f,"p_delta_gt_0":g} for a,b,c,d,e,f,g in RANK_BOOT]
HARD_ABS = [
    {"variant":"k5","split":"validation","model":"M1-96","HR@1":0.6234361233,"NDCG@5":0.8291402759,"MRR":0.7717533040},
    {"variant":"k5","split":"validation","model":"N96","HR@1":0.6237885463,"NDCG@5":0.8302923694,"MRR":0.7732422907},
    {"variant":"k5","split":"test","model":"M1-96","HR@1":0.5973568282,"NDCG@5":0.8162307888,"MRR":0.7546490455},
    {"variant":"k5","split":"test","model":"N96","HR@1":0.6100440529,"NDCG@5":0.8218966233,"MRR":0.7622026432},
    {"variant":"k20","split":"validation","model":"M1-96","HR@1":0.27665198237885463,"NDCG@5":0.3940015350323287,"MRR":0.41863020366990455},
    {"variant":"k20","split":"validation","model":"N96","HR@1":0.3890748898678414,"NDCG@5":0.5209809565825009,"MRR":0.5248862838190325},
    {"variant":"k50","split":"validation","model":"M1-96","HR@1":0.07876651982378854,"NDCG@5":0.10548664597363892,"MRR":0.15931553733972098},
    {"variant":"k50","split":"validation","model":"N96","HR@1":0.09585903083700441,"NDCG@5":0.13444222261012798,"MRR":0.18514489749687316},
    {"variant":"k20","split":"test","model":"M1-96","HR@1":0.2611453744493392,"NDCG@5":0.37551050733874575,"MRR":0.4040452485576725},
    {"variant":"k20","split":"test","model":"N96","HR@1":0.3758590308370044,"NDCG@5":0.5014430507361404,"MRR":0.5099145579215411},
    {"variant":"k50","split":"test","model":"M1-96","HR@1":0.06907488986784141,"NDCG@5":0.09752771100003052,"MRR":0.15118706139120325},
    {"variant":"k50","split":"test","model":"N96","HR@1":0.08299559471365639,"NDCG@5":0.12530579177654286,"MRR":0.17460505996585443},
]


COVERAGE = [
    {"run":"Y96","family":"Y-K0","planned_exposure":96000,"pool_records_available":200000,"records_counted_for_coverage":96000,"unique_sample_records_in_counted_pool":96000,"duplicate_sample_records_in_counted_pool":0,"sampler_repetition_observability":"partial_epoch_random_sampler_exact_ids_not_persisted","unique_target_items":3250,"unique_history_union_target_items":3250,"ratings_item_universe":3706,"metadata_item_universe":3883,"target_coverage_vs_ratings_universe":0.8769562871019968,"history_union_target_coverage_vs_ratings_universe":0.8769562871019968,"target_coverage_vs_metadata_universe":0.836981715168684,"history_union_target_coverage_vs_metadata_universe":0.836981715168684},
    {"run":"N96","family":"N-K0","planned_exposure":96000,"pool_records_available":200000,"records_counted_for_coverage":96000,"unique_sample_records_in_counted_pool":96000,"duplicate_sample_records_in_counted_pool":0,"sampler_repetition_observability":"partial_epoch_random_sampler_exact_ids_not_persisted","unique_target_items":3340,"unique_history_union_target_items":3503,"ratings_item_universe":3706,"metadata_item_universe":3883,"target_coverage_vs_ratings_universe":0.901241230437129,"history_union_target_coverage_vs_ratings_universe":0.9452239611440907,"target_coverage_vs_metadata_universe":0.8601596703579707,"history_union_target_coverage_vs_metadata_universe":0.902137522534123},
    {"run":"M1-96-Y","family":"M1","planned_exposure":96000,"pool_records_available":200000,"records_counted_for_coverage":96000,"unique_sample_records_in_counted_pool":96000,"duplicate_sample_records_in_counted_pool":0,"sampler_repetition_observability":"expected_sequential_1_to_1_if_resume_skip_honored","unique_target_items":3250,"unique_history_union_target_items":3250,"ratings_item_universe":3706,"metadata_item_universe":3883,"target_coverage_vs_ratings_universe":0.8769562871019968,"history_union_target_coverage_vs_ratings_universe":0.8769562871019968,"target_coverage_vs_metadata_universe":0.836981715168684,"history_union_target_coverage_vs_metadata_universe":0.836981715168684},
    {"run":"M1-96-N","family":"M1","planned_exposure":96000,"pool_records_available":200000,"records_counted_for_coverage":96000,"unique_sample_records_in_counted_pool":96000,"duplicate_sample_records_in_counted_pool":0,"sampler_repetition_observability":"expected_sequential_1_to_1_if_resume_skip_honored","unique_target_items":3340,"unique_history_union_target_items":3503,"ratings_item_universe":3706,"metadata_item_universe":3883,"target_coverage_vs_ratings_universe":0.901241230437129,"history_union_target_coverage_vs_ratings_universe":0.9452239611440907,"target_coverage_vs_metadata_universe":0.8601596703579707,"history_union_target_coverage_vs_metadata_universe":0.902137522534123},
    {"run":"N200","family":"N-K0","planned_exposure":200000,"pool_records_available":200000,"records_counted_for_coverage":200000,"unique_sample_records_in_counted_pool":200000,"duplicate_sample_records_in_counted_pool":0,"sampler_repetition_observability":"first_200k_pool_no_duplicate_records_expected","unique_target_items":3501,"unique_history_union_target_items":3616,"ratings_item_universe":3706,"metadata_item_universe":3883,"target_coverage_vs_ratings_universe":0.9446842957366433,"history_union_target_coverage_vs_ratings_universe":0.9757150566648678,"target_coverage_vs_metadata_universe":0.90162245686325,"history_union_target_coverage_vs_metadata_universe":0.9312387329384496},
]



def read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nMISSING\n", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def fmt(value: Any) -> str:
    if value in (None, ""):
        return "MISSING"
    try:
        return f"{float(value):.4f}"
    except Exception:
        return str(value)


def sasrec_curve() -> list[dict[str, Any]]:
    rows = read_csv(ROOT / ".agent/exposure_scaling/alignment/seed42/sasrec_curve.csv")
    return [r for r in rows if r.get("run", "").startswith("sasrec_s") and r.get("split") in {"validation", "test"}]


def sasrec_inventory() -> list[dict[str, Any]]:
    return read_csv(ROOT / ".agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv")


def matched_sasrec() -> list[dict[str, Any]]:
    srows = sasrec_curve()
    out = []
    pairs = [(24000, "N24", "sasrec_s47"), (48000, "N48", "sasrec_s94"), (96000, "N96", "sasrec_s188"), (200000, "N200", "sasrec_s391")]
    for target, nrun, srun in pairs:
        n = next(r for r in N_RANK if r["run"] == nrun and r["split"] == "validation")
        s = next((r for r in srows if r["run"] == srun and r["split"] == "validation"), {})
        sexp = int(float(s.get("actual_exposure", 0))) if s else None
        out.append({
            "target_exposure": target,
            "n_run": nrun,
            "n_actual_exposure": n["exposure"],
            "sasrec_run": srun,
            "sasrec_actual_exposure": sexp,
            "absolute_mismatch": None if sexp is None else sexp - target,
            "mismatch_pct": None if sexp is None else (sexp - target) / target * 100,
            "n_valid_HR@1": n["HR@1"],
            "sasrec_valid_HR@1": s.get("HR@1"),
            "delta_HR@1": None if not s else n["HR@1"] - float(s["HR@1"]),
            "n_valid_NDCG@5": n["NDCG@5"],
            "sasrec_valid_NDCG@5": s.get("NDCG@5"),
            "delta_NDCG@5": None if not s else n["NDCG@5"] - float(s["NDCG@5"]),
            "n_valid_MRR": n["MRR"],
            "sasrec_valid_MRR": s.get("MRR"),
            "delta_MRR": None if not s else n["MRR"] - float(s["MRR"]),
            "verification_status": "VERIFIED_FROM_ALIGNMENT_CSV" if s else "UNVERIFIED",
        })
    return out


def build_sasrec_alignment() -> list[dict[str, Any]]:
    srows = sasrec_curve()
    inv = {r["run"]: r for r in sasrec_inventory()}
    out = []
    for run in ["sasrec_s23", "sasrec_s47", "sasrec_s94", "sasrec_s188", "sasrec_s391"]:
        valid = next((r for r in srows if r["run"] == run and r["split"] == "validation"), {})
        test = next((r for r in srows if r["run"] == run and r["split"] == "test"), {})
        meta = inv.get(run, {})
        target_exp = valid.get("target_exposure") or meta.get("target_exposure")
        actual_exp = valid.get("actual_exposure") or meta.get("actual_exposure")
        out.append({
            "run_name": run,
            "target_exposure": target_exp,
            "actual_exposure": actual_exp,
            "checkpoint": meta.get("optimizer_steps") or valid.get("optimizer_steps"),
            "seed": 42,
            "candidate_protocol": "k5_popmatch_seed42",
            "valid_hr1": valid.get("HR@1", "MISSING"),
            "valid_ndcg": valid.get("NDCG@5", "MISSING"),
            "valid_mrr": valid.get("MRR", "MISSING"),
            "test_hr1": test.get("HR@1", "MISSING"),
            "test_ndcg": test.get("NDCG@5", "MISSING"),
            "test_mrr": test.get("MRR", "MISSING"),
            "source_path": meta.get("known_metric_path") or "agent alignment csv",
            "verification_status": "VERIFIED" if valid else "UNVERIFIED",
        })
    return out


def build_tables() -> None:
    write_csv(OUT / "sasrec_exposure_alignment.csv", build_sasrec_alignment())
    write_csv(OUT / "exposure_main_table.csv", exposure_main_table())
    write_csv(TABLES / "table_task_semantics.csv", table_task_semantics())
    write_csv(TABLES / "table_exposure_scaling.csv", table_exposure_scaling())
    write_csv(TABLES / "table_specialist_multitask.csv", table_specialist_multitask())
    write_csv(TABLES / "table_hard_candidate.csv", table_hard_candidate())
    write_csv(TABLES / "table_n_sasrec.csv", matched_sasrec())


def exposure_main_table() -> list[dict[str, Any]]:
    rows = []
    for r in Y_BINARY:
        rows.append({"model": r["family"], "run": r["run"], "task": "Y-native binary", "exposure": r["exposure"], "split": r["split"], "primary_metric": "AUC", "primary_value": r["AUC"], "secondary_metrics": json.dumps({"F1": r["F1"], "Accuracy": r["Accuracy"]}), "seed": 42, "protocol": "binary preference"})
    for r in Y_RANK:
        rows.append({"model": r["family"], "run": r["run"], "task": "Y-as-ranker bridge", "exposure": r["exposure"], "split": r["split"], "primary_metric": "NDCG@5", "primary_value": r["NDCG@5"], "secondary_metrics": json.dumps({"HR@1": r["HR@1"], "MRR": r["MRR"]}), "seed": 42, "protocol": "k5_popmatch_seed42"})
    for r in N_RANK:
        rows.append({"model": r["family"], "run": r["run"], "task": "N-native ranking", "exposure": r["exposure"], "split": r["split"], "primary_metric": "HR@1", "primary_value": r["HR@1"], "secondary_metrics": json.dumps({"NDCG@5": r["NDCG@5"], "MRR": r["MRR"]}), "seed": 42, "protocol": "k5_popmatch_seed42"})
    for r in M_BINARY:
        rows.append({"model": r["family"], "run": r["run"], "task": "M-Y binary", "exposure": r["exposure"], "split": r["split"], "primary_metric": "AUC", "primary_value": r["AUC"], "secondary_metrics": json.dumps({"F1": r["F1"], "Accuracy": r["Accuracy"]}), "seed": 42, "protocol": "binary preference"})
    for r in M_RANK:
        rows.append({"model": r["family"], "run": r["run"], "task": "M-N ranking", "exposure": r["exposure"], "split": r["split"], "primary_metric": "HR@1", "primary_value": r["HR@1"], "secondary_metrics": json.dumps({"NDCG@5": r["NDCG@5"], "MRR": r["MRR"]}), "seed": 42, "protocol": "k5_popmatch_seed42"})
    return rows


def table_task_semantics() -> list[dict[str, Any]]:
    return [
        {"model":"Base Llama","native_task":"untuned base model","native_metrics":"MISSING in final exposure package","bridge_or_ranking_metrics":"MISSING in final exposure package","interpretation":"Base metrics are not part of the frozen exposure-aware claims."},
        {"model":"Y-K0","native_task":"binary preference","native_metrics":"AUC/F1/Accuracy","bridge_or_ranking_metrics":"Y-as-ranker HR@1/NDCG@5/MRR","interpretation":"Preference prediction does not become a strong next-item ranker under PopMatch-k5."},
        {"model":"N-K0","native_task":"next-item ranking","native_metrics":"HR@1/NDCG@5/MRR","bridge_or_ranking_metrics":"same as native","interpretation":"Ranking capability scales strongly with exposure."},
        {"model":"M1","native_task":"Y+N multitask","native_metrics":"M-Y binary and M-N ranking","bridge_or_ranking_metrics":"k5/k20/k50 protocols","interpretation":"Y-side is preserved, while N-side robustness remains weaker than N specialist under harder protocols."},
        {"model":"SASRec","native_task":"sequential recommendation","native_metrics":"HR@1/NDCG@5/MRR","bridge_or_ranking_metrics":"k5_popmatch_seed42","interpretation":"Exposure-aware baseline, not FLOP-matched baseline."},
    ]


def table_exposure_scaling() -> list[dict[str, Any]]:
    rows = []
    for r in Y_BINARY:
        if r["split"] == "validation":
            rows.append({"run":r["run"],"family":"Y-K0","task":"Y-native","exposure":r["exposure"],"AUC":r["AUC"],"F1":r["F1"],"Accuracy":r["Accuracy"],"HR@1":"","NDCG@5":"","MRR":""})
    for r in N_RANK:
        if r["split"] == "validation":
            rows.append({"run":r["run"],"family":"N-K0","task":"N-native","exposure":r["exposure"],"AUC":"","F1":"","Accuracy":"","HR@1":r["HR@1"],"NDCG@5":r["NDCG@5"],"MRR":r["MRR"]})
    return rows


def table_specialist_multitask() -> list[dict[str, Any]]:
    rows = []
    for r in BINARY_BOOT:
        if r["split"] == "validation":
            rows.append({"comparison":"Y96 vs M1-96-Y","metric":r["metric"],"delta_definition":r["delta_definition"],"point_estimate":r["point_estimate"],"ci95_low":r["ci95_low"],"ci95_high":r["ci95_high"],"interpretation":"positive for F1 only; AUC/Accuracy compatible with parity"})
    for r in RANK_BOOT:
        if r["variant"] == "k5" and r["split"] == "validation":
            rows.append({"comparison":"N96 vs M1-96-N k5","metric":r["metric"],"delta_definition":r["delta_definition"],"point_estimate":r["point_estimate"],"ci95_low":r["ci95_low"],"ci95_high":r["ci95_high"],"interpretation":"near parity on validation"})
    return rows


def table_hard_candidate() -> list[dict[str, Any]]:
    rows = []
    for r in RANK_BOOT:
        n_abs = next((x for x in HARD_ABS if x["variant"] == r["variant"] and x["split"] == r["split"] and x["model"] == "N96"), {})
        m_abs = next((x for x in HARD_ABS if x["variant"] == r["variant"] and x["split"] == r["split"] and x["model"] == "M1-96"), {})
        metric = r["metric"]
        rows.append({
            "candidate_protocol": r["variant"],
            "split": r["split"],
            "metric": metric,
            "N96_value": n_abs.get(metric, "MISSING"),
            "M1-96_value": m_abs.get(metric, "MISSING"),
            "delta_definition": r["delta_definition"],
            "point_estimate": r["point_estimate"],
            "ci95_low": r["ci95_low"],
            "ci95_high": r["ci95_high"],
            "p_delta_gt_0": r["p_delta_gt_0"],
            "note": "candidate sets are independently constructed and not nested",
        })
    return rows



def setup_style() -> None:
    plt.rcParams.update({
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "legend.frameon": False,
        "savefig.dpi": 450,
        "savefig.bbox": "tight",
    })


def save_plot(fig: Any, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    png = FIG / f"{name}.png"
    svg = FIG / f"{name}.svg"
    fig.savefig(png, dpi=450)
    fig.savefig(svg)
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def build_figures() -> None:
    setup_style()
    ydata = [r for r in Y_BINARY if r["split"] == "validation"]
    ndata = [r for r in N_RANK if r["split"] == "validation"]
    write_csv(FDATA / "fig_y_native_exposure.csv", ydata)
    write_csv(FDATA / "fig_n_native_exposure.csv", ndata)
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot([r["exposure"] for r in ydata], [r["AUC"] for r in ydata], marker="o", color=COLORS[0], linewidth=1.8)
    ax.set_xlabel("Y-task exposure")
    ax.set_ylabel("Validation AUC")
    ax.set_title("Y-native exposure response")
    save_plot(fig, "fig_y_native_exposure")
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot([r["exposure"] for r in ndata], [r["HR@1"] for r in ndata], marker="o", color=COLORS[2], linewidth=1.8)
    ax.set_xlabel("N-task exposure")
    ax.set_ylabel("Validation HR@1")
    ax.set_title("N-native exposure response")
    save_plot(fig, "fig_n_native_exposure")

    ns = matched_sasrec()
    write_csv(FDATA / "fig_n_vs_sasrec_exposure.csv", ns)
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    x = [r["target_exposure"] for r in ns]
    ax.plot(x, [r["n_valid_HR@1"] for r in ns], marker="o", color=COLORS[0], label="N-K0")
    ax.plot(x, [float(r["sasrec_valid_HR@1"]) for r in ns], marker="s", color=COLORS[1], label="SASRec")
    ax.set_xscale("log")
    ax.set_xlabel("N-task training-sample exposure")
    ax.set_ylabel("Validation HR@1")
    ax.set_title("N-K0 vs SASRec exposure alignment")
    ax.legend()
    save_plot(fig, "fig_n_vs_sasrec_exposure")

    spec = []
    for exposure, nrun, mrun in [(48000, "N48", "M1-48"), (96000, "N96", "M1-96")]:
        n = next(r for r in N_RANK if r["run"] == nrun and r["split"] == "validation")
        m = next(r for r in M_RANK if r["run"] == mrun and r["split"] == "validation")
        spec.append({"protocol":"k5", "exposure":exposure, "N-K0":n["HR@1"], "M1":m["HR@1"]})
    for proto in ["k20", "k50"]:
        n96 = next(r for r in HARD_ABS if r["variant"] == proto and r["split"] == "validation" and r["model"] == "N96")["HR@1"]
        m1 = next(r for r in HARD_ABS if r["variant"] == proto and r["split"] == "validation" and r["model"] == "M1-96")["HR@1"]
        spec.append({"protocol":proto, "exposure":96000, "N-K0":n96, "M1":m1})
    write_csv(FDATA / "fig_specialist_vs_multitask.csv", spec)
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    labels = [f"{r['protocol']}\n{int(r['exposure']/1000)}k" for r in spec]
    loc = range(len(spec))
    width = 0.36
    ax.bar([i - width/2 for i in loc], [r["N-K0"] for r in spec], width=width, color=COLORS[0], label="N-K0")
    ax.bar([i + width/2 for i in loc], [r["M1"] for r in spec], width=width, color=COLORS[1], label="M1")
    ax.set_xticks(list(loc), labels)
    ax.set_ylabel("Validation HR@1")
    ax.set_xlabel("Candidate protocol / exposure")
    ax.set_title("Specialist vs multitask ranking")
    ax.legend()
    save_plot(fig, "fig_specialist_vs_multitask")
    write_text(FIG / "data-manifest.md", figure_manifest())


def figure_manifest() -> str:
    return """# Figure Data Manifest

| Figure | Data file | Real/mock | Source | Script | Outputs |
|---|---|---|---|---|---|
| fig_y_native_exposure | figures/data/fig_y_native_exposure.csv | Real | Seed42 frozen Y binary metrics | build_final_evidence.py | PNG, SVG |
| fig_n_native_exposure | figures/data/fig_n_native_exposure.csv | Real | Seed42 frozen N k5 metrics | build_final_evidence.py | PNG, SVG |
| fig_n_vs_sasrec_exposure | figures/data/fig_n_vs_sasrec_exposure.csv | Real | SASRec alignment CSV and N metrics | build_final_evidence.py | PNG, SVG |
| fig_specialist_vs_multitask | figures/data/fig_specialist_vs_multitask.csv | Real | Seed42 N/M k5 and robustness metrics | build_final_evidence.py | PNG, SVG |
"""


def write_sasrec_index() -> None:
    rows = build_sasrec_alignment()
    lines = ["# SASRec Artifact Index", "", "SASRec evidence is traced through `.agent/exposure_scaling/alignment/seed42/sasrec_curve.csv` and `.agent/exposure_scaling/alignment/sasrec_checkpoint_inventory.csv`.", ""]
    lines.append("| run | actual exposure | valid HR@1 | valid NDCG@5 | test HR@1 | source | status |")
    lines.append("|---|---:|---:|---:|---:|---|---|")
    for r in rows:
        lines.append(f"| {r['run_name']} | {r['actual_exposure']} | {fmt(r['valid_hr1'])} | {fmt(r['valid_ndcg'])} | {fmt(r['test_hr1'])} | `{r['source_path']}` | {r['verification_status']} |")
    write_text(OUT / "sasrec_artifact_index.md", "\n".join(lines))


def write_claims() -> None:
    claims = [
        {"claim_id":"C1","claim":"Y and N supervision learn different recommendation semantics.","supporting_artifacts":"table_task_semantics.csv; table_exposure_scaling.csv","dataset":"MovieLens-1M","seed_coverage":"seed42 exposure trajectory plus prior low-exposure evidence","validation_test":"validation primary; test report-only","bootstrap_evidence":"not central","cross_dataset_evidence":"Amazon directional evidence only","limitations":"Y-as-ranker is a bridge metric, not Y native objective","strength":"CORE","paper_wording":"Preference and next-interaction supervision induce different recommendation capabilities."},
        {"claim_id":"C2","claim":"Y-native performance approaches a plateau earlier than N-native ranking within the tested exposure range.","supporting_artifacts":"table_exposure_scaling.csv; fig_y_native_exposure; fig_n_native_exposure","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation primary","bootstrap_evidence":"not central","cross_dataset_evidence":"not required","limitations":"Do not write strict convergence; tested range only","strength":"SUPPORTED","paper_wording":"Y-side gains weaken by 96k, while N-native ranking continues to improve through 200k."},
        {"claim_id":"C3","claim":"N remains exposure-sensitive through 200k.","supporting_artifacts":"table_exposure_scaling.csv; exposure_coverage.csv","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation primary; test same direction","bootstrap_evidence":"not central","cross_dataset_evidence":"not required","limitations":"N200 is near-full-pool anchor, not converged endpoint","strength":"CORE","paper_wording":"N-native ranking remains exposure-sensitive through the 200k near-full-pool point."},
        {"claim_id":"C4","claim":"M1-96 shows no detectable Y-side degradation.","supporting_artifacts":"table_specialist_multitask.csv; binary bootstrap","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation plus report-only test","bootstrap_evidence":"F1 positive; AUC/Accuracy compatible with parity","cross_dataset_evidence":"not required","limitations":"Do not claim overall positive transfer","strength":"SUPPORTED","paper_wording":"M1-96 preserves Y-native preference capability without detectable degradation."},
        {"claim_id":"C5","claim":"M1-96 reaches near-parity with N96 on k5 validation.","supporting_artifacts":"table_specialist_multitask.csv; ranking bootstrap","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation primary; test favors N96","bootstrap_evidence":"k5 validation CIs cross zero","cross_dataset_evidence":"not required","limitations":"Limited to k5 validation","strength":"SUPPORTED","paper_wording":"Under k5 validation, the N96-M1-96 gap is statistically compatible with parity."},
        {"claim_id":"C6","claim":"N96 is more robust than M1-96 under current harder candidate protocols.","supporting_artifacts":"table_hard_candidate.csv; candidate_protocol_audit.md","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation and report-only test","bootstrap_evidence":"k20/k50 CIs positive","cross_dataset_evidence":"not required","limitations":"Candidate size and composition are confounded; protocols are not nested","strength":"SUPPORTED","paper_wording":"Harder candidate protocols reveal a remaining N-side robustness advantage for the dedicated model."},
        {"claim_id":"C7","claim":"N-K0 outperforms SASRec under matched training-sample exposure at evaluated points.","supporting_artifacts":"table_n_sasrec.csv; sasrec_artifact_index.md","dataset":"MovieLens-1M","seed_coverage":"seed42","validation_test":"validation primary; SASRec test report-only","bootstrap_evidence":"not computed","cross_dataset_evidence":"Amazon directional evidence separate","limitations":"Exposure matching is sample-based, not FLOPs/wall-clock matched","strength":"CORE","paper_wording":"At approximately matched task-sample exposure, N-K0 outperforms SASRec across the evaluated exposure points."},
    ]
    write_csv(OUT / "claim_evidence_matrix.csv", claims)
    lines = ["# Claim Evidence Matrix", "", "| ID | Strength | Paper wording | Limitations |", "|---|---|---|---|"]
    for c in claims:
        lines.append(f"| {c['claim_id']} | {c['strength']} | {c['paper_wording']} | {c['limitations']} |")
    write_text(OUT / "claim_evidence_matrix.md", "\n".join(lines))


def write_revised_claims() -> None:
    text = """# Rejected Or Revised Claims

OLD: N specialist consistently outperforms M1.

NEW: At higher matched exposure, the k5 validation gap nearly vanishes, while harder candidate protocols still favor N.

OLD: M1 suffers task interference on both Y and N.

NEW: No detectable Y-side degradation is observed at M1-96; the remaining specialization cost is primarily visible on N-side robustness.

OLD: Candidate-size expansion reveals N advantage.

NEW: Harder candidate protocols reveal N advantage, but candidate size and candidate composition are confounded because the candidate sets are not nested.

OLD: High-exposure SASRec is stronger than LLM.

NEW: With much more supervision SASRec can surpass lower-exposure LLM anchors, while under approximately matched training-sample exposure N-K0 remains stronger at the currently evaluated points.
"""
    write_text(OUT / "rejected_or_revised_claims.md", text)



def write_results() -> None:
    text = """# 4 Results

## 4.1 Distinct supervision semantics

本节检验偏好判断监督与下一交互预测监督是否学习到相同的推荐能力。实验将 Y-K0 作为 binary preference predictor 评估，同时把同一模型放入 PopMatch-k5 候选排序协议中作为 bridge metric；N-K0 则直接按照 next-item ranking 的原生目标评估。结果显示，Y-native binary 指标在 24k 到 96k exposure 范围内保持可用表现，Y-as-ranker 的 PopMatch-k5 NDCG@5 却始终停留在约 0.60 附近。N-K0 在相同数据集上的 PopMatch-k5 排序指标明显更高，96k validation HR@1 达到 0.6238，NDCG@5 达到 0.8303。这说明 Y 与 N 的监督语义不能被视为同一任务的不同表述，二者诱导出的能力具有明确差异。

## 4.2 Task-specific exposure scaling

曝光量变化进一步放大了这种任务差异。Y-native binary 的 AUC 从 Y24 的 0.7761 上升到 Y48 的 0.7816，再到 Y96 的 0.7844，但 F1 从 Y48 的 0.7848 回落到 Y96 的 0.7783，Accuracy 在 0.723 附近变化很小。相同区间内，Y-as-ranker 的 NDCG@5 基本没有随 exposure 增长而提高。N-native ranking 呈现另一种曲线：N24、N48、N96、N200 的 validation HR@1 分别为 0.5774、0.6030、0.6238 和 0.6516，NDCG@5 也从 0.8068 提升到 0.8432。N200 覆盖了 200k 训练池且没有重复样本，target item 覆盖 ratings universe 的 94.47%，history 与 target 的并集覆盖 97.57%。因此，N200 更适合作为 near-full-pool one-pass anchor，而不是收敛终点。

## 4.3 Multi-task specialization under matched exposure

本节考察 M1 在 matched per-task exposure 下是否牺牲专门任务能力。Y-side 上，M1-96 相比 Y96 的 binary bootstrap 显示 F1 有小幅正差异，validation delta 为 +0.00553，95% CI 为 [+0.00096, +0.01025]；test delta 为 +0.00554，95% CI 为 [+0.00046, +0.01041]。AUC 与 Accuracy 的置信区间跨过 0，说明点估计虽为正，但仍与 parity 兼容。由此更稳妥的判断是 M1-96 没有观察到 Y-side degradation，而不是已经证明整体 positive transfer。N-side 上，k5 validation 的 N96-M1-96 差异极小，HR@1 delta 仅 +0.00035，95% CI 为 [-0.01040, +0.01128]，NDCG@5 与 MRR 也跨过 0。这支持 k5 validation 上的 near-parity，但 test report-only 指标仍显示 N96 占优。

## 4.4 Robustness under harder candidate protocols

k5 上的 near-parity 没有推广到更复杂候选协议。在 k20 validation 中，N96-M1-96 的 HR@1、NDCG@5 和 MRR delta 分别为 +0.11242、+0.12698 和 +0.10626，bootstrap CI 均为正；test 上也保持同向差异。k50 协议下差距缩小，但 HR@1、NDCG@5 和 MRR 的 validation CI 仍全部为正。候选协议审计显示，k5、k20 与 k50 候选集几乎不构成嵌套关系，k5_in_k20 的 nested_fraction 为 0，k20_in_k50 也接近 0，Jaccard 相似度很低。因此，本文将这些结果表述为 hard-candidate robustness，而不是单纯 candidate-size effect。现有证据表明，M1-96 在较难候选协议下仍存在 N-side robustness cost。

## 4.5 Exposure-aware comparison with SASRec

SASRec 作为 specialized sequential recommender，需要按训练样本 exposure 对齐，而不是按 wall-clock、FLOPs 或 epoch 名义值直接比较。当前 alignment artifact 验证了 S47、S94、S188 与 S391 分别对应约 24k、48k、96k 与 200k exposure。在这些 matched points 上，N-K0 的 validation HR@1 均高于 SASRec：24k 对比为 0.5774 vs 0.2731，48k 为 0.6030 vs 0.2930，96k 为 0.6238 vs 0.3281，200k 为 0.6516 vs 0.4749。差距在 200k 处缩小，但方向没有反转。这个比较支持 exposure-aware baseline claim，同时边界也很清楚：它是 task-sample exposure matching，不是计算量匹配。

## 4.6 Cross-dataset validation

Amazon 结果暂不扩展为新的训练主线，只作为外部有效性的辅助证据。它的作用是检查 Y/N 语义分离与 N-side ranking 优势是否在 MovieLens 之外保持方向一致，而不是替代本节的 exposure scaling 主结果。当前论文结果部分可以把 Amazon 放在 cross-dataset validation 位置，用于降低单数据集叙事风险；更强的跨数据集 scaling 结论仍需单独实验支持。
"""
    write_text(OUT / "paper_results_draft.md", text)


def write_discussion_outline() -> None:
    text = """# Discussion Outline

## Why supervision semantics matter

Y supervision directly优化偏好判断，N supervision 则要求模型在用户历史之后区分下一交互候选。二者都与推荐相关，但评价对象并不等价。Discussion 可以围绕这种语义差异解释为什么 Y-native 表现不能自动转化为 next-item ranking 能力。

## Why N benefits more from exposure

N 任务在 200k near-full-pool anchor 仍然提升，可能与下一交互预测对 item coverage、历史上下文组合和候选辨别边界更敏感有关。这个解释只能作为 hypothesis，不能写成机制证明。

## Why multitask interference decreases on Y/k5 but remains under hard ranking

M1-96 在 Y-side 没有可检测退化，在 k5 validation 上接近 N96，但 k20/k50 仍落后。Discussion 可以把这写成多任务共享表示对简单协议足够，但在更强候选干扰下仍缺少 N specialist 的排序锐度。

## Why random or easy candidates can hide model differences

k5 validation 的 near-parity 与 k20/k50 差距并存，说明候选协议会改变模型差异的可见性。由于当前 k20/k50 候选集不嵌套，文本必须把 candidate size 与 composition confound 一起写入限制。

## Why training-sample exposure matters in LLM-vs-SASRec comparison

SASRec 的高 epoch 或高步数结果不能直接和低 exposure LLM 比较。Exposure-aware comparison 让 baseline 更公平，但仍不等于 FLOP matching 或成本 matching。
"""
    write_text(OUT / "discussion_outline.md", text)


def write_research_questions() -> None:
    text = """# Research Questions

## RQ1: Supervision Semantics

Do preference prediction and next-interaction prediction induce different recommendation capabilities?

Core evidence: Y-native binary metrics, Y-as-ranker bridge metrics, and N-native ranking metrics.

## RQ2: Exposure Response

How do task-specific capabilities scale with supervision exposure?

Core evidence: Y24/Y48/Y96 native binary trajectory and N24/N48/N96/N200 native ranking trajectory.

## RQ3: Multi-task Unification

How does multi-task tuning affect specialized capabilities under matched per-task exposure?

Core evidence: Y96 vs M1-96-Y binary bootstrap and N96 vs M1-96-N k5 bootstrap.

## RQ4: Ranking Robustness

Does the apparent N/M relationship persist under harder candidate protocols?

Core evidence: k5, k20, and k50 comparisons with the explicit caveat that candidate protocols are not nested.

## RQ5: Exposure-aware Baseline Comparison

How does N-K0 compare with a specialized sequential recommender under approximately matched training-sample exposure?

Core evidence: N-K0 vs SASRec matched points at approximately 24k, 48k, 96k, and 200k.
"""
    write_text(OUT / "research_questions.md", text)


def write_multiseed_decision() -> None:
    text = """# Multiseed Decision

## Version A: no additional multiseed

论文措辞保持限定：seed42 exposure analysis suggests。可使用的证据组合包括低 exposure 3-seed evidence、seed42 exposure trajectory、prediction-level bootstrap，以及 Amazon directional validation。这个版本可以支持 descriptive paper claims，但不能把 M1 positive transfer 或 N/M parity 写成跨 seed 定论。

## Version B: minimal strengthening

若后续批准，最小补强矩阵为 seed43 与 seed44 的 Y96、N96、M96。每个 seed 需要 Y-native binary、N k5/k20/k50 validation-first 评测，并在决策冻结后补 report-only test。按 seed42 经验粗估，单 seed 的 Y96+N96+M96 训练和评测可能需要数十小时单卡时间；实际取决于云端卡型、是否续训、I/O 和候选评测批大小。信息增益主要体现在三类 claim：Y-side no degradation 是否稳定，k5 N/M near-parity 是否稳定，hard-candidate robustness gap 是否稳定。

## Current recommendation

Multiseed is recommended, not required, for the current Results draft. 如果论文只写 seed42 descriptive findings，可以不补。若目标是提交时使用 stronger generalization wording，则应补最小 multiseed。
"""
    write_text(OUT / "multiseed_decision.md", text)


def write_readiness() -> None:
    text = """# Exposure Stage Close Readiness

1. Exposure scaling 的主要问题已经在 seed42 范围内回答：Y-side gains weaken by 96k，N-native ranking remains exposure-sensitive through 200k。

2. Seed42 evidence 已经足以进入论文 Results draft，但只能支持限定性表述。

3. 仍然 open 的问题包括 multiseed 稳定性、hard-candidate protocol composition confound、M1-200 是否存在高 exposure crossover，以及 Amazon 是否需要 exposure scaling 复现。

4. 这些 open questions 不是当前 Results draft 的 blocker，只影响 claim strength。

5. Multiseed 的状态是 recommended。若论文追求强泛化结论，它接近 required；若采用 seed42 descriptive language，它是 optional enhancement。

6. M200 当前不必要。它成本高，只在论文核心 claim 需要证明 200k matched multitask endpoint 时才值得运行。

7. 建议关闭 Exposure Scaling stage 的训练部分，并将本阶段切换为 evidence freeze / paper writing。

8. 建议恢复 Paper Writing / Submission Package，但必须使用本目录里的 claim boundaries，而不是旧叙事。
"""
    write_text(OUT / "exposure_stage_close_readiness.md", text)


def write_yaml_docs() -> None:
    write_text(OUT / "validated_findings.yaml", """validated_findings:
  - id: C1
    finding: Y and N supervision learn different recommendation semantics.
    strength: CORE
  - id: C2
    finding: Y-native gains weaken by 96k within the tested exposure range.
    strength: SUPPORTED
  - id: C3
    finding: N-native ranking remains exposure-sensitive through the 200k near-full-pool point.
    strength: CORE
  - id: C4
    finding: M1-96 shows no detectable Y-side degradation.
    strength: SUPPORTED
  - id: C5
    finding: M1-96 reaches near-parity with N96 on k5 validation.
    strength: SUPPORTED
  - id: C6
    finding: N96 is more robust than M1-96 under k20/k50 hard-candidate protocols.
    strength: SUPPORTED
  - id: C7
    finding: N-K0 outperforms SASRec under matched training-sample exposure at evaluated points.
    strength: CORE
""")
    write_text(OUT / "rejected_findings.yaml", """rejected_or_revised:
  - old: N specialist consistently outperforms M1.
    new: At higher matched exposure, the k5 validation gap nearly vanishes, while harder candidate protocols still favor N.
  - old: M1 suffers task interference on both Y and N.
    new: No detectable Y-side degradation is observed at M1-96; remaining specialization cost is primarily visible on N-side robustness.
  - old: Candidate-size expansion reveals N advantage.
    new: Harder candidate protocols reveal N advantage, but candidate size and composition are confounded.
  - old: High-exposure SASRec is stronger than LLM.
    new: Under approximately matched training-sample exposure, N-K0 remains stronger at evaluated points.
""")
    write_text(OUT / "open_questions.yaml", """open_questions:
  - question: Are seed42 M1/Y and M1/N relationships stable across seeds?
    blocker: false
  - question: How much of the k20/k50 robustness gap is candidate composition rather than candidate count?
    blocker: false
  - question: Does M1-200 change the high-exposure specialist/multitask relationship?
    blocker: false
  - question: Should Amazon receive exposure scaling or remain directional validation?
    blocker: false
""")
    write_text(OUT / "wiki_update_proposal.yaml", """wiki_update_proposal:
  authorized: false
  note: Do not modify durable wiki until user grants one-time write authorization.
  proposed_updates:
    - file: wiki/current_state.md
      operation: update
      reason: Record exposure scaling training pause and evidence freeze state.
    - file: wiki/reports/exposure_scaling_seed42.md
      operation: create
      reason: Preserve final seed42 exposure-aware findings, claim boundaries, and table/figure index.
    - file: wiki/history/2026-09.md
      operation: update
      reason: Record semantic shift from training sweep to evidence consolidation.
""")


def write_summary_docs() -> None:
    write_text(OUT / "stage_summary.md", """# Stage Summary

The LLM Exposure Scaling & Convergence Validation stage has moved from training to no-training evidence consolidation. Seed42 now has complete Y24/Y48/Y96, N24/N48/N96/N200, M1-48/M1-96, k20/k50 robustness, and SASRec exposure-aligned evidence. The evidence supports a paper-ready descriptive account: Y-native gains weaken by 96k, N-native ranking keeps improving through 200k, M1-96 preserves Y-side capability while approaching N96 on k5 validation, and harder candidate protocols still favor N96. SASRec is now traceable through alignment artifacts and supports an exposure-aware baseline comparison.
""")
    write_text(OUT / "next_stage_recommendation.md", """# Next Stage Recommendation

Resume Paper Writing / Submission Package using the final evidence package as the source of truth. Do not reopen GPU training unless the paper requires stronger generalization wording. Multiseed is recommended for stronger claims, but not required for a seed42 descriptive Results section. M1-200 should remain deferred unless the paper's central argument depends on the 200k multitask endpoint.
""")
    write_text(OUT / "README.md", """# Final Evidence Package

This directory freezes the no-training evidence package for the LLM Exposure Scaling & Convergence Validation stage. It contains formal tables, figure data, generated PNG/SVG figures, claim boundaries, Results writing material, and stage close readiness notes.

No file in this package requires new training, GPU inference, new checkpoint creation, new exposure sweeps, or multiseed execution.

Primary files:

- `exposure_main_table.csv`
- `sasrec_exposure_alignment.csv`
- `sasrec_artifact_index.md`
- `claim_evidence_matrix.csv`
- `claim_evidence_matrix.md`
- `paper_results_draft.md`
- `discussion_outline.md`
- `research_questions.md`
- `multiseed_decision.md`
- `exposure_stage_close_readiness.md`

Figures are under `figures/` with PNG, SVG, and source CSV data.
""")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    FDATA.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    build_tables()
    build_figures()
    write_sasrec_index()
    write_claims()
    write_revised_claims()
    write_results()
    write_discussion_outline()
    write_research_questions()
    write_multiseed_decision()
    write_readiness()
    write_yaml_docs()
    write_summary_docs()
    print(f"Final evidence package generated: {OUT}")


if __name__ == "__main__":
    main()
