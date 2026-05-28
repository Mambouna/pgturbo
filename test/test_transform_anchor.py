from unittest import TestCase
from pgturbo.actor import transform_anchor

root2 = 2 ** 0.5


def assertVecEqual(a, b, decimal_places=7):
    for t in (a, b):
        if not isinstance(t, tuple):
            raise AssertionError('%r is not a tuple' % t)
        if len(t) != 2:
            raise AssertionError('Expected 2-tuple, not %r' % t)

    ax, ay = a
    bx, by = b
    epsilon = 10 ** -decimal_places
    if abs(ax - bx) > epsilon or abs(ay - by) > epsilon:
        raise AssertionError('%r != %r (to %d decimal places)' % (
            a, b, decimal_places
        ))


class TransformAnchorTest(TestCase):
    def test_identity(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 1.0, 1.0),
            (5, 5)
        )

    def test_45deg(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 45, 1.0, 1.0),
            (5 * root2, 5 * root2)
        )

    def test_45deg_offset(self):
        assertVecEqual(
            transform_anchor(0, 0.5, 1, 1, 45, 1.0, 1.0),
            (0.25 * root2, 0.75 * root2)
        )

    def test_scale_total_up(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 2.5, 2.5),
            (12.5, 12.5)
        )

    def test_scale_total_down(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 0.25, 0.25),
            (1.25, 1.25)
        )

    def test_scale_x_up(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 2.5, 1.0),
            (12.5, 5)
        )

    def test_scale_x_down(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 0.25, 1.0),
            (1.25, 5)
        )

    def test_scale_y_up(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 1.0, 2.5),
            (5, 12.5)
        )

    def test_scale_y_down(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0, 1.0, 0.25),
            (5, 1.25)
        )

    def test_45deg_scale_total_up(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 45, 2.5, 2.5),
            (12.5 * root2, 12.5 * root2)
        )

    def test_45deg_scale_total_up(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 45, 0.25, 0.25),
            (1.25 * root2, 1.25 * root2)
        )
