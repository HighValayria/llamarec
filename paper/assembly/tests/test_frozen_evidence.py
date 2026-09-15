from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import unittest

from paper.assembly.tests.contract_snapshot import assert_current_contract, file_sha256


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
FROZEN = REPO / '.agent/exposure_scaling/final_evidence'


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


class FrozenEvidenceTests(unittest.TestCase):
    def test_historical_export_and_current_contract_hashes(self):
        report = json.loads((ROOT / 'evidence/asset_provenance.json').read_text(encoding='utf-8'))
        contract = assert_current_contract(self, REPO)
        historical = {row['path']: row for row in contract['historical_baselines']}
        baseline_path = 'paper/evidence/asset_provenance.json'
        self.assertEqual(file_sha256(REPO / baseline_path), historical[baseline_path]['sha256'])
        for path, expected in report['sources_sha256'].items():
            self.assertEqual(hashlib.sha256((REPO / path).read_bytes()).hexdigest(), expected, path)

    def test_all_native_metrics_keep_run_split_exposure_and_values(self):
        original = rows(FROZEN / 'exposure_main_table.csv')
        rendered = rows(ROOT / 'tables/binary_exposure.csv') + rows(ROOT / 'tables/exposure_scaling.csv')
        expected = [r for r in original if 'bridge' not in r['task']]
        self.assertEqual(len(rendered), len(expected))
        for record in expected:
            target = [r for r in rendered if r['run'] == record['run'] and r['split'] == record['split'] and record['primary_metric'] in r]
            self.assertEqual(len(target), 1)
            self.assertEqual(target[0]['exposure'], record['exposure'])
            self.assertEqual(target[0]['seed'], '42')
            values = {record['primary_metric']: record['primary_value'], **json.loads(record['secondary_metrics'])}
            for key, value in values.items():
                self.assertAlmostEqual(float(target[0][key]), float(value), places=10)

    def test_paired_intervals_and_signs_are_copied_without_recalculation(self):
        for name in ('hard_candidate', 'specialist_multitask'):
            self.assertEqual((ROOT / f'tables/{name}.csv').read_bytes(), (FROZEN / f'tables/table_{name}.csv').read_bytes())
        hard = rows(ROOT / 'tables/hard_candidate.csv')
        self.assertEqual(len(hard), 18)
        for row in hard:
            self.assertAlmostEqual(float(row['point_estimate']), float(row['N96_value']) - float(row['M1-96_value']), places=9)
            low, high = float(row['ci95_low']), float(row['ci95_high'])
            self.assertLess(low, high)
            if row['candidate_protocol'] == 'k5' and row['split'] == 'validation':
                self.assertLess(low, 0)
                self.assertGreater(high, 0)
            else:
                self.assertGreater(low, 0)

    def test_sasrec_uses_actual_exposure_and_correct_splits(self):
        source = {r['run_name']: r for r in rows(FROZEN / 'sasrec_exposure_alignment.csv')}
        table = rows(ROOT / 'tables/n_vs_sasrec_exposure.csv')
        self.assertEqual(len(table), 8)
        for row in table:
            reference = source[row['SASRec_run']]
            self.assertEqual(row['SASRec_exposure'], reference['actual_exposure'])
            prefix = 'valid' if row['split'] == 'validation' else 'test'
            self.assertAlmostEqual(float(row['SASRec_HR@1']), float(reference[prefix + '_hr1']), places=10)
        self.assertEqual({r['SASRec_exposure'] for r in table if r['N_run'] == 'N200'}, {'200000'})

    def test_amazon_is_ranking_only_seed42_full_test(self):
        table = rows(ROOT / 'tables/cross_dataset.csv')
        self.assertEqual(len(table), 5)
        self.assertEqual({r['split'] for r in table}, {'test'})
        self.assertEqual({r['samples'] for r in table}, {'57439'})
        self.assertEqual({r['seed'] for r in table}, {'42'})
        self.assertNotIn('F1', table[0])

    def test_manual_training_counts_match_batch_and_task_split(self):
        for row in rows(ROOT / 'tables/training_exposure.csv'):
            total = int(row['total_exposure'])
            self.assertEqual(total, int(row['optimizer_steps']) * int(row['effective_batch']))
            self.assertEqual(total, int(row['Y_exposure']) + int(row['N_exposure']))
            if row['run'].startswith('M1'):
                self.assertEqual(row['Y_exposure'], row['N_exposure'])


if __name__ == '__main__':
    unittest.main()
