
import unittest

from source.Simulation import simulate, days_to_target

class TestSimulation(unittest.TestCase):
    """
    Comprehensive tests for the Part 4 simulation functionality.
    """

    # Tests for simulate()

    def test_simulate_normal_growth(self):
        """
        Tests the simulation with a moderate, predictable probability.
        """
        p = 0.1
        days = 3
        # Day 1: 100 * 0.1 = 10 new. Total = 10.
        # Day 2: (100+10) * 0.1 = 11 new. Total = 10 + 11 = 21.
        # Day 3: (110+11) * 0.1 = 12.1 new. Total = 21 + 12.1 = 33.1.
        expected_results = [10.0, 21.0, 33.1]
        
        actual_results = simulate(p, days)
        
        self.assertEqual(len(actual_results), len(expected_results))
        for expected, actual in zip(expected_results, actual_results):
            self.assertAlmostEqual(expected, actual, places=5)

    def test_simulate_no_growth(self):
        """
        Tests the edge case where the probability is 0.
        """
        p = 0
        days = 5
        expected_results = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(simulate(p, days), expected_results)

    def test_simulate_with_capacity_exhaustion(self):
        """
        Tests with a high probability to ensure the retirement logic is working.
        With p=5.0, the initial 100 referrers are exhausted after 2 days (5+5=10).
        """
        p = 5.0
        days = 3
        # Day 1: 100 * 5 = 500 new. Total=500. Active Referrers = 100(original) + 500(new) = 600.
        #        Cohort1(100) has made 5 referrals each.
        # Day 2: 600 * 5 = 3000 new. Total=3500. Active Referrers = 600 + 3000 = 3600.
        #        Cohort1(100) makes 5 more, hits capacity (10), and retires.
        #        Active Referrers becomes 3600 - 100 = 3500.
        #        Cohort2(500) has now made 5 referrals each.
        # Day 3: 3500 * 5 = 17500 new. Total = 3500 + 17500 = 21000.
        expected_results = [500.0, 3500.0, 21000.0]

        actual_results = simulate(p, days)
        
        self.assertEqual(len(actual_results), len(expected_results))
        for expected, actual in zip(expected_results, actual_results):
            self.assertAlmostEqual(expected, actual, places=5)


    # Tests for days_to_target()

    def test_days_to_target_achievable(self):
        """
        Tests a standard scenario where the target is a few days away.
        """
        # From our test_simulate_normal_growth, we know it takes 3 days to pass 30.
        self.assertEqual(days_to_target(p=0.1, target_total=30), 3)
        self.assertEqual(days_to_target(p=0.1, target_total=21), 2)

    def test_days_to_target_met_in_one_day(self):
        """
        Tests a target that should be met on the very first day.
        """
        # On day 1, 10 referrals are made.
        self.assertEqual(days_to_target(p=0.1, target_total=10), 1)
        self.assertEqual(days_to_target(p=0.1, target_total=1), 1)

    def test_days_to_target_zero_or_negative(self):
        """
        Tests the edge case of a non-positive target.
        """
        self.assertEqual(days_to_target(p=0.1, target_total=0), 0)
        self.assertEqual(days_to_target(p=0.1, target_total=-100), 0)
        
    def test_days_to_target_unachievable(self):
        """
        Tests the edge case where p=0, making any positive target impossible.
        """
        self.assertEqual(days_to_target(p=0, target_total=1), -1)

if __name__ == '__main__':
    unittest.main()