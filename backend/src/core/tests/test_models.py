from django.test import TestCase


class BasicTest(TestCase):
    def test_math_is_working(self):
        print("Running basic math test...")
        self.assertEqual(2 + 2, 4)
