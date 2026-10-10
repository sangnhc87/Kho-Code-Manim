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


EPISODES = sorted(p.name for p in ROOT.glob('int[0-9][0-9]') if (p / 'scene.py').exists())


class Episodes(unittest.TestCase):
    """Runs the same checks on every produced episode (int01, int02, …)."""

    def test_produced_episodes_are_marked_in_plan(self):
        plan = json.loads((ROOT / 'series_plan.json').read_text('utf-8'))
        status = {f"int{e['n']:02d}": e['status'] for e in plan['episodes']}
        for ep in EPISODES:
            self.assertIn(status[ep], {'production', 'published'}, ep)

    def test_validate(self):
        for ep in EPISODES:
            with self.subTest(ep=ep):
                self.assertTrue(episode.load(ep).validate())

    def test_every_beat_has_a_scene_method(self):
        for ep in EPISODES:
            lesson = episode.load(ep)
            src = (ROOT / ep / 'scene.py').read_text('utf-8')
            for b in lesson.BEATS:
                with self.subTest(ep=ep, beat=b.id):
                    self.assertRegex(src, rf'def beat_{b.id}\(self, T\)')

    def test_every_formula_used_exists_and_every_formula_is_used(self):
        for ep in EPISODES:
            with self.subTest(ep=ep):
                lesson = episode.load(ep)
                src = (ROOT / ep / 'scene.py').read_text('utf-8')
                called = set(re.findall(r"self\.M\('([A-Za-z0-9_]+)'", src))
                self.assertTrue(called <= set(lesson.FORMULAS), called - set(lesson.FORMULAS))
                unused = {k for k in lesson.FORMULAS if f"'{k}'" not in src}
                self.assertEqual(unused, set())

    def test_offline_plan_length_is_a_full_lesson(self):
        for ep in EPISODES:
            with self.subTest(ep=ep):
                total = sum(voice.estimate(b.text)[0] for b in episode.load(ep).BEATS)
                self.assertTrue(7 * 60 < total < 18 * 60, total)

    def test_episode_metadata(self):
        for ep in EPISODES:
            with self.subTest(ep=ep):
                e = episode.load(ep).EPISODE
                self.assertEqual(e['code'], ep.upper())
                self.assertEqual(e['number'], int(ep[3:]))

    def test_typst_source_has_colour_helpers(self):
        self.assertIn('#let gold', source('x'))

    def test_srt_and_chapters_from_timeline(self):
        for ep in EPISODES:
            with self.subTest(ep=ep):
                beats = []
                for b in episode.load(ep).BEATS:
                    d, sentences = voice.estimate(b.text)
                    beats.append({'id': b.id, 'chapter': b.chapter, 'duration': d + 1, 'sentences': sentences})
                plan = {'beats': beats}
                starts, t = [], 0.0
                for b in beats:
                    starts.append(t)
                    t += b['duration']
                self.assertTrue(voice.build_srt(plan, starts).startswith('1\n00:00:00,'))
                chapters = voice.chapters(plan, starts)
                self.assertEqual(chapters[0][0], 0.0)
                gaps = [b[0] - a[0] for a, b in zip(chapters, chapters[1:])]
                self.assertTrue(all(g >= 10 for g in gaps), gaps)  # YouTube needs >= 10 s per chapter


if __name__ == '__main__':
    unittest.main()
