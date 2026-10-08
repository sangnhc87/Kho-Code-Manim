import unittest
from fractions import Fraction as F
from geometry.triangle_membership import orient,membership,barycentric

A=(F(0),F(3)); B=(F(-1),F(2)); C=(F(2),F(1))


def point(m):
    return (m,m-F(1,2))


class TestGeo01(unittest.TestCase):
    def test_counterclockwise(self):
        self.assertEqual(orient(A,B,C),4)

    def test_segment_boundaries(self):
        self.assertEqual(membership(A,B,C,point(F(13,8))), 'boundary')
        self.assertEqual(membership(A,B,C,point(F(7,4))), 'boundary')

    def test_interval_interior(self):
        for m in (F(27,16),F(17,10),F(69,40)):
            self.assertEqual(membership(A,B,C,point(m)), 'inside')

    def test_interval_exterior(self):
        for m in (F(-1),F(1),F(8,5),F(9,5),F(3)):
            self.assertEqual(membership(A,B,C,point(m)), 'outside')

    def test_answer(self):
        a,b=F(13,8),F(7,4)
        self.assertEqual(8*a+4*b,20)

    def test_barycentric(self):
        m=F(27,16)
        lam=barycentric(A,B,C,point(m))
        self.assertEqual(sum(lam),1)
        self.assertTrue(all(v>0 for v in lam))

    def test_orientation_reverse(self):
        for m in (F(27,16),F(13,8),F(3)):
            self.assertEqual(membership(A,B,C,point(m)),membership(A,C,B,point(m)))

    def test_degenerate(self):
        with self.assertRaises(ValueError):
            membership((0,0),(1,1),(2,2),(0,0))

    def test_wedge_inequalities_equivalent(self):
        # Three half-plane tests for ABC, with strict inequalities.
        for ii in range(-10,41):
            for jj in range(-5,41):
                x,y=F(ii,10),F(jj,10)
                cond=(x-y+3>0 and x+3*y-5>0 and 3-x-y>0)
                self.assertEqual(cond, membership(A,B,C,(x,y))=='inside')

    def test_formula_correct_midpoint(self):
        m=F(27,16)
        x,y=point(m)
        self.assertEqual(x-y+3,F(7,2))
        self.assertEqual(x+3*y-5,4*m-F(13,2))
        self.assertEqual(3-x-y,F(7,2)-2*m)

if __name__=='__main__':
    unittest.main()
