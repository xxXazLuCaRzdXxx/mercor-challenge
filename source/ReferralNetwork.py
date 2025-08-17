from collections import deque

class ReferralNetwork:

    def __init__(self):

        self.graph = {}
        self.referrers = {}

    def add_user(self, user):
        
        if user not in self.graph:
            self.graph[user] = []

    def add_referral(self, referrer, candidate):

        # Constraint 1
        if referrer == candidate:
            print(f"Error: Users cannot refer themselves ({referrer} -> {candidate})")
            return False
        
        # Constraint 2
        if candidate in self.referrers:
            print(f"Error: Candidate '{candidate}' has already been referred")
            return False

        self.add_user(referrer)
        self.add_user(candidate)
        
        # Constraint 3
        if self._creates_cycle(referrer, candidate):
            print(f"Error: Adding this referral would create a cycle ({referrer} -> {candidate})")
            return False

        self.graph[referrer].append(candidate)
        self.referrers[candidate] = referrer

        return True

    def _creates_cycle(self, referrer, candidate):

        current_node = referrer
        while current_node in self.referrers:

            current_node = self.referrers[current_node]
            if current_node == candidate:
                return True            

        return False

    def get_direct_referrals(self, user):

        return self.graph.get(user, [])

    