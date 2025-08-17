# Part 5: Referral Bonus Optimization

import unittest
from source.Optimization import min_bonus_for_target
from source.Simulation import simulate

class TestOptimization(unittest.TestCase):
    """
    Comprehensive tests for the Part 5 bonus optimization functionality.
    """

    def test_min_bonus_finds_correct_bonus(self):
        """
        Tests the binary search finds a bonus that lands on a $10 increment.
        """
        def mock_adoption_prob(bonus):
            return bonus / 1000.0
            
        days = 15
        target_hires = 205
        
        expected_bonus = 80
        actual_bonus = min_bonus_for_target(days, target_hires, mock_adoption_prob)
        self.assertEqual(actual_bonus, expected_bonus)

    def test_min_bonus_unachievable_target(self):
        """
        Tests that the function returns None if the target is impossible.
        """
        def mock_low_prob(bonus):
            return 0.0001
        days = 30
        target_hires = 5000
        result = min_bonus_for_target(days, target_hires, mock_low_prob)
        self.assertIsNone(result)

    def test_min_bonus_for_zero_target(self):
        """
        Tests the edge case where the target is 0.
        """
        def mock_prob(bonus):
            return bonus / 1000.0
        result = min_bonus_for_target(days=30, target_hires=0, adoption_prob_func=mock_prob)
        self.assertEqual(result, 0)
        
    def test_min_bonus_rounding_logic(self):
        """
        Tests that the bonus is correctly rounded up to the nearest $10.
        """
        def mock_adoption_prob(bonus):
            return bonus / 1000.0
            
        days = 15
        
        # Find the absolute maximum hires achievable with a bonus of exactly $80 (p=0.08).
        max_hires_at_80_bonus = simulate(p=0.08, days=15)[-1] # This will be ~205.8

        # Set our target to be just one hire more than is possible at $80.
        # This guarantees that a bonus of $80 will fail.
        target_hires = int(max_hires_at_80_bonus) + 1 # Target will be 206

        # The function finds a bonus slightly higher than $80,
        # which will round up to $90.
        expected_bonus = 90
        actual_bonus = min_bonus_for_target(days, target_hires, mock_adoption_prob)
        self.assertEqual(actual_bonus, expected_bonus)

if __name__ == '__main__':
    unittest.main()