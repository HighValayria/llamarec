from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from assemble import assemble
from template_adapter import AssemblyError, detect_template_type, parse_yaml


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'paper/assembly/paper_manifest.yaml'
        self.spec = {
            'version': 1, 'evidence_ids': ['C1'],
            'modules': [{'id': 'sample', 'source': 'paper/modules/sample.md'}],
            'tables': {}, 'figures': {},
        }
        self.write_manifest()
        self.source('paper/modules/sample.md', 'sample', self.paragraph())

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def write_manifest(self):
        self.write('paper/assembly/paper_manifest.yaml', yaml.safe_dump(self.spec, allow_unicode=True))

    def source(self, path, identifier, body, status='ready'):
        head = yaml.safe_dump({'id': identifier, 'title': {'en': 'English title', 'zh': '中文标题'}, 'status': status}, allow_unicode=True)
        return self.write(path, f'---\n{head}---\n\n{body}\n')

    def paragraph(self, identifier='sample.p01', en='The score is 0.25, with 4 candidates.', zh='评分为 0.25，候选数为 4。', extra=''):
        return f'<!-- PARAGRAPH: {identifier} -->\n<!-- EVIDENCE: C1 -->\n{extra}\n**EN**\n\n{en}\n\n**ZH**\n\n{zh}\n'

    def build(self, **kwargs):
        return assemble(self.manifest, root=self.root, **kwargs)

    def test_three_languages_strip_markers_and_keep_selected_heading(self):
        for lang in ('en', 'zh', 'bilingual'):
            with self.subTest(lang=lang):
                result = self.build(lang=lang, mode='final')
                content = Path(result['output']).read_text(encoding='utf-8')
                self.assertNotIn('PARAGRAPH', content)
                self.assertNotIn('EVIDENCE', content)
                if lang == 'en':
                    self.assertIn('English title', content)
                    self.assertNotIn('中文标题', content)
                    self.assertNotIn('**EN**', content)
                    self.assertNotIn('**ZH**', content)
                elif lang == 'zh':
                    self.assertIn('中文标题', content)
                    self.assertNotIn('The score', content)
                else:
                    self.assertLess(content.index('**EN**'), content.index('**ZH**'))

    def test_pending_in_hidden_language_blocks_final_without_overwrite(self):
        old = self.write('paper/builds/paper_en.md', 'existing build')
        self.source('paper/modules/sample.md', 'sample', self.paragraph(zh='评分 0.25，候选数 4。TODO 完成。'))
        with self.assertRaisesRegex(AssemblyError, 'final build'):
            self.build(lang='en', mode='final')
        self.assertEqual(old.read_text(), 'existing build')

    def test_all_pending_marker_types_block(self):
        for marker in ('EVIDENCE_PENDING: MS96', 'TODO', 'PENDING-MS96', 'ABSTRACT_NOT_FINAL', 'CITATION_NEEDED: topic', 'citation_needed: topic'):
            with self.subTest(marker=marker):
                self.source('paper/modules/sample.md', 'sample', self.paragraph(extra=f'<!-- {marker} -->'))
                with self.assertRaisesRegex(AssemblyError, 'final build'):
                    self.build(mode='final', check=True)
                self.assertTrue(self.build(check=True)['pending'])


    def test_citation_needed_in_hidden_language_blocks_final(self):
        old = self.write('paper/builds/paper_en.md', 'existing build')
        self.source('paper/modules/sample.md', 'sample', self.paragraph(
            zh='评分 0.25，候选数 4。[CITATION_NEEDED: topic]'))
        draft = self.build(lang='en', check=True)
        self.assertTrue(any('CITATION_NEEDED' in row for row in draft['pending']))
        with self.assertRaisesRegex(AssemblyError, 'CITATION_NEEDED'):
            self.build(lang='en', mode='final')
        self.assertEqual(old.read_text(), 'existing build')

    def test_citation_needed_in_nested_part_is_visible_in_draft(self):
        self.source('paper/modules/sample.md', 'sample',
                    '<!-- INCLUDE: paper/modules_parts/child.md -->')
        self.source('paper/modules_parts/child.md', 'child', self.paragraph(
            'child.p01', en='Result. [CITATION_NEEDED: topic]',
            zh='结果。[CITATION_NEEDED: topic]'))
        result = self.build(lang='bilingual')
        self.assertIn('[CITATION_NEEDED: topic]',
                      Path(result['output']).read_text(encoding='utf-8'))
        for lang in ('en', 'zh', 'bilingual'):
            with self.subTest(lang=lang):
                with self.assertRaisesRegex(AssemblyError, 'CITATION_NEEDED'):
                    self.build(lang=lang, mode='final', check=True)

    def test_citation_needed_in_caption_or_template_blocks_final(self):
        self.add_table(caption='[CITATION_NEEDED: sampling]')
        with self.assertRaisesRegex(AssemblyError, 'CITATION_NEEDED'):
            self.build(mode='final')
        self.spec['tables']['scores']['caption']['en'] = 'Measured score'
        self.write_manifest()
        venue = self.root / 'paper/templates/example'
        self.write('paper/templates/example/template_manifest.yaml',
                   'format: markdown\nentry: template.md\n')
        self.write('paper/templates/example/template.md',
                   '[CITATION_NEEDED: template]\n{{content}}')
        with self.assertRaisesRegex(AssemblyError, 'CITATION_NEEDED'):
            self.build(template=venue, mode='final')

    def test_draft_status_blocks_final(self):
        self.source('paper/modules/sample.md', 'sample', self.paragraph(), status='draft')
        with self.assertRaisesRegex(AssemblyError, 'final build'):
            self.build(mode='final')

    def test_nested_include_pending_and_order(self):
        self.source('paper/modules/sample.md', 'sample', self.paragraph() + '\n<!-- INCLUDE: paper/modules_parts/child.md -->')
        self.source('paper/modules_parts/child.md', 'child', self.paragraph('child.p01', extra='<!-- EVIDENCE_PENDING: MS96 -->'))
        result = self.build(check=True)
        self.assertEqual(list(result['paragraphs']), ['sample.p01', 'child.p01'])
        with self.assertRaisesRegex(AssemblyError, 'final build'):
            self.build(mode='final')

    def test_include_cycle(self):
        self.source('paper/modules/sample.md', 'sample', '<!-- INCLUDE: paper/modules_parts/child.md -->')
        self.source('paper/modules_parts/child.md', 'child', '<!-- INCLUDE: paper/modules/sample.md -->')
        with self.assertRaisesRegex(AssemblyError, '循环'):
            self.build(check=True)

    def test_missing_translation_and_numeric_drift(self):
        for body in (self.paragraph().replace('**ZH**', '**XX**'), self.paragraph(zh='评分 0.35，候选数 4。')):
            self.source('paper/modules/sample.md', 'sample', body)
            with self.assertRaises(AssemblyError):
                self.build(check=True)

    def test_duplicate_paragraph_id(self):
        self.source('paper/modules/sample.md', 'sample', self.paragraph() + self.paragraph())
        with self.assertRaisesRegex(AssemblyError, '重复'):
            self.build(check=True)

    def test_unknown_evidence_and_unmarked_prose(self):
        for body in (self.paragraph().replace('EVIDENCE: C1', 'EVIDENCE: C999'), 'Plain unpaired text.'):
            self.source('paper/modules/sample.md', 'sample', body)
            with self.assertRaises(AssemblyError):
                self.build(check=True)

    def test_missing_asset_and_mismatched_language_reference(self):
        body = self.paragraph(en='Result 0.25. [TABLE: absent]', zh='结果 0.25。[TABLE: absent]')
        self.source('paper/modules/sample.md', 'sample', body)
        with self.assertRaisesRegex(AssemblyError, '未登记图表'):
            self.build(check=True)
        self.source('paper/modules/sample.md', 'sample', self.paragraph(en='Result 0.25. [TABLE: absent]', zh='结果 0.25。'))
        with self.assertRaisesRegex(AssemblyError, '引用不对应'):
            self.build(check=True)

    def add_table(self, caption='Measured score'):
        self.spec['tables']['scores'] = {
            'source': 'tables/scores.csv', 'caption': {'en': caption, 'zh': '测量评分'},
            'columns': [{'key': 'score', 'title': {'en': 'Score', 'zh': '评分'}}],
        }
        self.write_manifest()
        self.write('paper/tables/scores.csv', 'score\n0.25\n')
        self.source('paper/modules/sample.md', 'sample', self.paragraph(en='Result 0.25. [TABLE: scores]', zh='结果 0.25。[TABLE: scores]'))

    def test_table_resolution_and_copy(self):
        self.add_table()
        result = self.build(lang='en', mode='final')
        content = Path(result['output']).read_text(encoding='utf-8')
        self.assertIn('[Table 1](#table-scores)', content)
        self.assertNotIn('[TABLE:', content)
        self.assertIn('0.25000', content)
        self.assertTrue((self.root / 'paper/builds/assets/tables/scores.csv').is_file())
        provenance = json.loads(Path(result['output']).with_suffix('.build.json').read_text(encoding='utf-8'))
        self.assertIn('paper/tables/scores.csv', provenance['sources_sha256'])

    def test_pending_caption_and_missing_file(self):
        self.add_table(caption='TODO measured score')
        with self.assertRaisesRegex(AssemblyError, 'final build'):
            self.build(mode='final')
        (self.root / 'paper/tables/scores.csv').unlink()
        with self.assertRaisesRegex(AssemblyError, '不存在'):
            self.build(check=True)

    def test_output_cannot_overwrite_source(self):
        source = self.root / 'paper/modules/sample.md'
        before = source.read_bytes()
        with self.assertRaisesRegex(AssemblyError, 'paper/builds'):
            self.build(output=source)
        self.assertEqual(source.read_bytes(), before)

    def test_include_cannot_escape_authoring_directories(self):
        self.source('paper/modules/sample.md', 'sample', '<!-- INCLUDE: wiki/current_state.md -->')
        with self.assertRaisesRegex(AssemblyError, '正文只能'):
            self.build(check=True)

    def test_markdown_template_mapping_and_heading(self):
        venue = self.root / 'paper/templates/example'
        self.write('paper/templates/example/template_manifest.yaml', 'format: markdown\nentry: template.md\nmodule_order: [sample]\nsection_titles:\n  sample: {en: Venue Results, zh: 结果}\n')
        self.write('paper/templates/example/template.md', 'Review\n\n{{content}}\n')
        result = self.build(template=venue, lang='en', mode='final')
        content = Path(result['output']).read_text(encoding='utf-8')
        self.assertTrue(content.startswith('Review'))
        self.assertIn('# Venue Results', content)

    def test_template_cannot_drop_selected_module(self):
        venue = self.root / 'paper/templates/example'
        self.write('paper/templates/example/template_manifest.yaml', 'format: markdown\nentry: template.md\nmodule_order: []\n')
        self.write('paper/templates/example/template.md', '{{content}}')
        with self.assertRaisesRegex(AssemblyError, '恰好覆盖'):
            self.build(template=venue)

    def test_unsupported_template_is_explicit(self):
        venue = self.root / 'paper/templates/example'
        self.write('paper/templates/example/main.tex', 'example')
        self.assertEqual(detect_template_type(venue), 'latex')
        with self.assertRaisesRegex(AssemblyError, '尚未实现'):
            self.build(template=venue)

    def test_pending_template_blocks_final(self):
        venue = self.root / 'paper/templates/example'
        self.write('paper/templates/example/template_manifest.yaml', 'format: markdown\nentry: template.md\n')
        self.write('paper/templates/example/template.md', '<!-- TODO template -->\n{{content}}')
        with self.assertRaisesRegex(AssemblyError, 'final build'):
            self.build(template=venue, mode='final')

    def test_check_writes_nothing_and_duplicate_yaml_rejected(self):
        self.build(check=True)
        self.assertFalse((self.root / 'paper/builds').exists())
        with self.assertRaisesRegex(AssemblyError, '重复键'):
            parse_yaml('version: 1\nversion: 2\n')


if __name__ == '__main__':
    unittest.main()
