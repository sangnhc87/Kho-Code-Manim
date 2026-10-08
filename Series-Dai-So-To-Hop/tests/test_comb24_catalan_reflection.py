import unittest
from math import comb
from itertools import product
from comb24_lesson_data import (BEATS,CHAPTERS,FORMULAS,validate,
    catalan,dyck_words,all_balanced_multiset_paths,bad_dyck_words,
    reflect_bad_prefix,inv_reflected,catalan_recurrence,
    ballot_weak,ballot_strict,peak_count,narayana,count_narayana_independent)

class TestComb24(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_beats_48(self):self.assertEqual(len(BEATS),48)
    def test_chapters_8(self):self.assertEqual(len(CHAPTERS),8)
    def test_formulas_48(self):self.assertEqual(len(FORMULAS),48)
    def test_chapter_beats_6(self):
        for c,_ in CHAPTERS:self.assertEqual(sum(b.section==c for b in BEATS),6)
    def test_narration_not_blank(self):self.assertTrue(all(len(b.narration.split())>35 for b in BEATS))
    def test_no_duplicate_formula_ids(self):self.assertEqual(len(set(FORMULAS)),48)
    def test_catalan_known_values(self):self.assertEqual([catalan(i) for i in range(8)],[1,1,2,5,14,42,132,429])
    def test_negative_catalan(self):
        with self.assertRaises(ValueError):catalan(-1)
    def test_negative_dyck(self):
        with self.assertRaises(ValueError):dyck_words(-1)
    def test_unique_dyck(self):
        for n in range(7):self.assertEqual(len(dyck_words(n)),len(set(dyck_words(n))))
    def test_dyck_counts(self):
        for n in range(7):self.assertEqual(len(dyck_words(n)),catalan(n))
    def test_dyck_prefix_valid(self):
        for n in range(6):
            for w in dyck_words(n):
                h=0
                for step in w:
                    h+=1 if step=='U' else -1
                    self.assertGreaterEqual(h,0)
                self.assertEqual(h,0)
    def test_all_balanced_count(self):
        for n in range(7):self.assertEqual(len(all_balanced_multiset_paths(n)),comb(2*n,n))
    def test_bad_count_reflection(self):
        for n in range(1,7):self.assertEqual(len(bad_dyck_words(n)),comb(2*n,n+1))
    def test_reflection_map_full(self):
        for n in range(1,6):
            bad=bad_dyck_words(n)
            images=[reflect_bad_prefix(w) for w in bad]
            target={''.join(z) for z in product('UD',repeat=2*n) if z.count('U')==n+1}
            self.assertEqual(set(images),target)
            self.assertEqual(len(images),len(set(images)))
            self.assertTrue(all(inv_reflected(reflect_bad_prefix(w))==w for w in bad))
    def test_reflection_invalid_input(self):
        with self.assertRaises(ValueError):reflect_bad_prefix('UUUDDD')
    def test_inverse_invalid(self):
        with self.assertRaises(ValueError):inv_reflected('DDD')
    def test_reflection_example(self):self.assertEqual(reflect_bad_prefix('UDDUUD'),'DUUUUD')
    def test_recurrence(self):
        for n in range(1,16):self.assertEqual(catalan_recurrence(n),catalan(n))
    def test_empty_recurrence(self):self.assertEqual(catalan_recurrence(0),1)
    def test_ballot_weak_case(self):self.assertEqual(ballot_weak(5,3),28)
    def test_ballot_strict_case(self):self.assertEqual(ballot_strict(5,3),14)
    def test_ballot_invalid_cases(self):
        with self.assertRaises(ValueError):ballot_weak(1,2)
        with self.assertRaises(ValueError):ballot_strict(3,3)
    def test_ballot_bruteforce(self):
        for p in range(1,7):
            for q in range(p+1):
                weak=strong=0
                for seq in product('AB',repeat=p+q):
                    if seq.count('A')!=p:continue
                    tally=0;minim=999;strict=True
                    for ch in seq:
                        tally+=1 if ch=='A' else -1
                        minim=min(minim,tally)
                        if tally<=0:strict=False
                    weak+=(minim>=0)
                    strong+=strict
                self.assertEqual(weak,ballot_weak(p,q))
                if p>q:self.assertEqual(strong,ballot_strict(p,q))
    def test_narayana_n6_k3(self):self.assertEqual(narayana(6,3),50)
    def test_narayana_all(self):
        for n in range(1,8):
            self.assertEqual(sum(narayana(n,k) for k in range(1,n+1)),catalan(n))
            for k in range(1,n+1):
                self.assertEqual(narayana(n,k),count_narayana_independent(n,k))
    def test_peaks_n3(self):self.assertEqual([sum(peak_count(w)==k for w in dyck_words(3)) for k in (1,2,3)],[1,3,1])
    def test_narayana_invalid(self):self.assertEqual(narayana(0,0),0)
    def test_nonnegative_beat_timing(self):self.assertTrue(all(b.min_seconds>=28 for b in BEATS))

if __name__=='__main__':unittest.main()
