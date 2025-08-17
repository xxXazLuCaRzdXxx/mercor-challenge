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

class TestReferralNetworkParts2And3(unittest.TestCase):

    def setUp(self):
        """
        Set up a complex, non-trivial network to test advanced functions.
        The structure is:
        - Two main networks, one rooted at A, one at H.
        - A is a major influencer.
        - B is a sub-influencer under A.
        - K is an isolated user who has referred no one.
        """
        self.network = ReferralNetwork()
        referrals = [
            ('A', 'B'), ('A', 'C'),
            ('B', 'D'), ('B', 'E'),
            ('C', 'F'),
            ('D', 'G'),
            ('H', 'I'), ('H', 'J')
        ]
        for referrer, candidate in referrals:
            self.network.add_referral(referrer, candidate)
        
        # Adding K, an isolated user who refers no one
        self.network.add_user('K')

    # Part 2 Tests

    def test_get_total_referral_count(self):
        """
        Tests the calculation of total downstream reach for various users.
        """
        # A is the root of the largest network
        self.assertEqual(self.network.get_total_referral_count('A'), 6, "Reach of A should be 6 (B,C,D,E,F,G)")
        # B is a mid-level influencer
        self.assertEqual(self.network.get_total_referral_count('B'), 3, "Reach of B should be 3 (D,E,G)")
        # H is the root of the smaller network
        self.assertEqual(self.network.get_total_referral_count('H'), 2, "Reach of H should be 2 (I,J)")
        # D has a single person in their downstream
        self.assertEqual(self.network.get_total_referral_count('D'), 1, "Reach of D should be 1 (G)")
        # A leaf node like G should have a reach of 0
        self.assertEqual(self.network.get_total_referral_count('G'), 0, "Reach of a leaf node (G) should be 0")
        # An isolated user K should have a reach of 0
        self.assertEqual(self.network.get_total_referral_count('K'), 0, "Reach of an isolated user (K) should be 0")
        # A non-existent user should have a reach of 0
        self.assertEqual(self.network.get_total_referral_count('Z'), 0, "Reach of a non-existent user should be 0")

    def test_get_top_k_referrers(self):
        """
        Tests the ranking of top referrers by their total reach.
        """
        # Test getting the top 3
        # Expected reach: A=6, B=3, H=2, C=1, D=1, others=0
        top_3 = self.network.get_top_k_referrers(3)
        self.assertEqual(top_3, ['A', 'B', 'H'])

        # Test getting just the top 1
        top_1 = self.network.get_top_k_referrers(1)
        self.assertEqual(top_1, ['A'])

        # Test edge case k=0
        self.assertEqual(self.network.get_top_k_referrers(0), [])
        
        # Test getting the top 5 (note: order of C and D is not guaranteed as they have the same reach)
        top_5 = self.network.get_top_k_referrers(5)
        self.assertEqual(top_5[:3], ['A', 'B', 'H'])
        self.assertIn('C', top_5[3:])
        self.assertIn('D', top_5[3:])


    # --- Part 3: Test Influencer Metrics ---

    def test_get_influencers_by_unique_reach(self):
        """
        Tests the greedy algorithm for finding influencers by unique reach expansion.
        """
        # Step 1: 'A' is chosen, covering 6 unique users {B,C,D,E,F,G}.
        # Step 2: 'H' is chosen, covering 2 new unique users {I,J}.
        # Step 3: All other users (B,C,D) now have a new contribution of 0. Loop terminates.
        expected_ranking = ['A', 'H']
        self.assertEqual(self.network.get_influencers_by_unique_reach(), expected_ranking)

    def test_get_influencers_by_flow_centrality(self):
        """
        Tests the ranking of "broker" users based on flow centrality.
        """
        # Pre-calculated scores based on the setUp graph:
        # - B is on paths A->D, A->E, A->G (score=3)
        # - D is on paths A->G, B->G (score=2)
        # - C is on path A->F (score=1)
        # - All other nodes are either roots or leaves of paths, so they don't lie *between*
        #   any two other nodes. Their scores are 0.
        
        ranked_list = self.network.get_influencers_by_flow_centrality()
        
        # We can confidently assert the order of the top 3 brokers.
        self.assertEqual(ranked_list[:3], ['B', 'D', 'C'])

if __name__ == '__main__':
    unittest.main()