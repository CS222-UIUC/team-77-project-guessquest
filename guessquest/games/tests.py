from django.test import TestCase
from games.services import calculate_score
# Create your tests here.


class CalculateScoreTestCase(TestCase):
    def test_exact_guess(self):
        self.assertEqual(calculate_score(70, 70), 250)

    def test_close_guess(self):
        self.assertEqual(calculate_score(70, 69), 240)
        self.assertEqual(calculate_score(70, 75), 200)

    def test_far_off_guess(self):
        self.assertEqual(calculate_score(70, 100), 0)
        self.assertEqual(calculate_score(70, -100), 0)

    def test_score_never_negative(self):
        self.assertGreaterEqual(calculate_score(70, 500), 0)
    
