from unittest import TestCase
from nodeview.geometry import Rectangle


class TestRectangle(TestCase):

    def test_init_default_values(self):
        rect = Rectangle()

        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 0)
        self.assertEqual(rect.width, 0)
        self.assertEqual(rect.height, 0)

    def test_init_custom_values(self):
        rect = Rectangle(1, 2, 3, 4)

        self.assertEqual(rect.x, 1)
        self.assertEqual(rect.y, 2)
        self.assertEqual(rect.width, 3)
        self.assertEqual(rect.height, 4)

    def test_equity(self):
        rect_a = Rectangle(1, 2, 3, 4)
        rect_b = Rectangle(1, 2, 3, 4)

        self.assertEqual(rect_a, rect_b)

    def test_inequity(self):
        rect_a = Rectangle(1, 2, 3, 4)
        rect_b = Rectangle(0, 2, 3, 4)

        self.assertNotEqual(rect_a, rect_b)

        rect_a = Rectangle(1, 2, 3, 4)
        rect_b = Rectangle(1, 0, 3, 4)

        self.assertNotEqual(rect_a, rect_b)

        rect_a = Rectangle(1, 2, 3, 4)
        rect_b = Rectangle(1, 2, 0, 4)

        self.assertNotEqual(rect_a, rect_b)

        rect_a = Rectangle(1, 2, 3, 4)
        rect_b = Rectangle(1, 2, 3, 0)

        self.assertNotEqual(rect_a, rect_b)
