# tests/test_ReferralNetwork.py

import unittest
from source.ReferralNetwork import ReferralNetwork

class TestReferralNetworkPart1(unittest.TestCase):

    def setUp(self):
        
        self.network = ReferralNetwork()

    # Test Core Functionality

    def test_add_valid_referral(self):
        """
        Tests that a valid, simple referral is added successfully.
        """
        result = self.network.add_referral('A', 'B')
        self.assertTrue(result, "add_referral should return True for a valid referral.")
        self.assertIn('B', self.network.get_direct_referrals('A'), "Candidate 'B' should be in referrer 'A's list.")
        self.assertEqual(self.network.referrers['B'], 'A', "The referrer of 'B' should be 'A'.")

    def test_get_direct_referrals(self):
        """
        Tests retrieving direct referrals for a user with multiple referrals.
        """
        self.network.add_referral('A', 'B')
        self.network.add_referral('A', 'C')
        referrals = self.network.get_direct_referrals('A')
        self.assertIn('B', referrals)
        self.assertIn('C', referrals)
        self.assertEqual(len(referrals), 2)

    # Test Edge Cases

    def test_get_referrals_for_user_with_none(self):
        """
        Tests that a user who has made no referrals returns an empty list.
        """
        self.network.add_user('A')
        self.assertEqual(self.network.get_direct_referrals('A'), [], "Should return an empty list for a user with no referrals.")

    def test_get_referrals_for_non_existent_user(self):
        """
        Tests that a non-existent user returns an empty list without error.
        """
        self.assertEqual(self.network.get_direct_referrals('Z'), [], "Should return an empty list for a non-existent user.")

    # Test Constraint 1: No Self-Referrals

    def test_rejects_self_referral(self):
        """
        Ensures that a user cannot refer themselves.
        """
        result = self.network.add_referral('A', 'A')
        self.assertFalse(result, "add_referral should return False for a self-referral.")
        self.assertEqual(len(self.network.graph), 0, "Graph should be empty after a failed self-referral.")
        self.assertEqual(len(self.network.referrers), 0, "Referrers dict should be empty.")

    # Test Constraint 2: Unique Referrer

    def test_rejects_duplicate_candidate_referral(self):
        """
        Ensures a candidate can only be referred by one unique referrer.
        """
        self.network.add_referral('A', 'C') # First, valid referral
        
        # Attempt to refer the same candidate 'C' from a different referrer 'B'
        result = self.network.add_referral('B', 'C')
        
        self.assertFalse(result, "add_referral should return False for a duplicate candidate.")
        self.assertNotIn('C', self.network.get_direct_referrals('B'), "'C' should not be in 'B's referral list.")
        self.assertEqual(self.network.referrers['C'], 'A', "The original referrer of 'C' should remain 'A'.")

    # Test Constraint 3: Acyclic Graph

    def test_rejects_direct_cycle(self):
        """
        Ensures a direct cycle (A -> B -> A) is rejected.
        """
        self.network.add_referral('A', 'B')
        result = self.network.add_referral('B', 'A')
        
        self.assertFalse(result, "add_referral should return False for a direct cycle.")
        self.assertNotIn('A', self.network.get_direct_referrals('B'), "The cycle-creating referral should not be added.")
        self.assertIsNone(self.network.referrers.get('A'), "A's referrer should remain None.")

    def test_rejects_long_cycle(self):
        """
        Ensures a longer, indirect cycle (A -> B -> C -> A) is rejected.
        """
        self.network.add_referral('A', 'B')
        self.network.add_referral('B', 'C')
        
        # Attempt to add the link from C back to A
        result = self.network.add_referral('C', 'A')
        
        self.assertFalse(result, "add_referral should return False for a long cycle.")
        self.assertNotIn('A', self.network.get_direct_referrals('C'), "The cycle-creating referral should not be added.")
        self.assertIsNone(self.network.referrers.get('A'), "A's referrer should remain None.")

if __name__ == '__main__':
    unittest.main()