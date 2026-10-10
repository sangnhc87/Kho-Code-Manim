"""Content/plan checks that run without Manim, Typst or network."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from common import episode, voice  # noqa: E402
from common.typst_build import source  # noqa: E402


class SeriesPlan(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'series_plan.json').read_text('utf-8'))

    def test_36_episodes_in_order(self):
        self.assertEqual([e['n'] for e in self.plan['episodes']], list(range(1, 37)))

    def test_parts_cover_every_episode_once(self):
        covered = [n for p in self.plan['parts'] for n in range(p['episodes'][0], p['episodes'][1] + 1)]
        self.assertEqual(covered, list(range(1, 37)))

    def test_plan_document_lists_every_code(self):
        doc = (ROOT / 'KE_HOACH_SERIES_36_TAP.md').read_text('utf-8')
        for n in range(1, 37):
            self.assertIn(f'**INT{n:02d}**', doc)

    def test_scope_and_status_values(self):
        for e in self.plan['episodes']:
            self.assertIn(e['scope'], {'core', 'extended'})
            self.assertIn(e['status'], {'planned', 'production', 'published'})


class Int01(unittest.TestCase):
    def setUp(self):
        self.lesson = episode.load('int01')

    def test_validate(self):
        self.assertTrue(self.lesson.validate())

    def test_every_beat_has_a_scene_method(self):
        src = (ROOT / 'int01' / 'scene.py').read_text('utf-8')
        for b in self.lesson.BEATS:
            self.assertRegex(src, rf'def beat_{b.id}\(self, T\)')

    def test_every_formula_used_exists_and_every_formula_is_used(self):
        src = (ROOT / 'int01' / 'scene.py').read_text('utf-8')
        used = set(re.findall(r"self\.M\('([A-Za-z0-9_]+)'", src))
        used |= set(re.findall(r"'((?:hw_ans|hw|sum)\d)'", src))
        self.assertTrue(used <= set(self.lesson.FORMULAS), used - set(self.lesson.FORMULAS))
        self.assertEqual(set(self.lesson.FORMULAS) - used, set())

    def test_offline_plan_length_is_a_full_lesson(self):
        total = sum(voice.estimate(b.text)[0] for b in self.lesson.BEATS)
        self.assertTrue(9 * 60 < total < 18 * 60, total)

    def test_typst_source_has_colour_helpers(self):
        self.assertIn('#let gold', source('x'))

    def test_srt_and_chapters_from_timeline(self):
        beats = []
        for b in self.lesson.BEATS:
            d, sentences = voice.estimate(b.text)
            beats.append({'id': b.id, 'chapter': b.chapter, 'duration': d + 1, 'sentences': sentences})
        plan = {'beats': beats}
        starts, t = [], 0.0
        for b in beats:
            starts.append(t)
            t += b['duration']
        srt = voice.build_srt(plan, starts)
        self.assertTrue(srt.startswith('1\n00:00:00,'))
        chapters = voice.chapters(plan, starts)
        self.assertEqual(chapters[0][0], 0.0)
        gaps = [b[0] - a[0] for a, b in zip(chapters, chapters[1:])]
        self.assertTrue(all(g >= 10 for g in gaps), gaps)  # YouTube requires >= 10 s per chapter


if __name__ == '__main__':
    unittest.main()
