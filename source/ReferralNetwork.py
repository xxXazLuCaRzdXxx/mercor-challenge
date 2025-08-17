from collections import deque

class ReferralNetwork:

    def __init__(self):

        self.graph = {}
        self.referrers = {}

    # Part 1: Referral Graph 

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

    #  Part 2: Full Network Reach

    def get_total_referral_count(self,user):

        if user not in self.graph:
            return 0

        queue = deque(self.graph.get(user, []))
        count = len(queue)

        while queue:
            current_user = queue.popleft()
            
            direct_referrals = self.graph.get(current_user, [])
            for referral in direct_referrals:
                queue.append(referral)
                count += 1
                
        return count

    def get_top_k_referrers(self, k):
        
        if k <= 0:
            return []            
        
        all_reaches = {}

        for user in self.graph:
            all_reaches[user] = self.get_total_referral_count(user)

        sorted_referrers = sorted(all_reaches.items(), key=lambda item: item[1], reverse=True)

        return [user for user, reach in sorted_referrers[:k]]

    # Part 3: Identify Influencers

    #  Metric 1: Unique Reach Expansion
    def get_influencers_by_unique_reach(self):

        all_reach_sets = self._get_all_reach_sets()
        
        globally_covered = set()
        ranked_influencers = []
        
        # Make a copy to modify during iteration
        remaining_influencers = all_reach_sets.copy()

        while remaining_influencers:
            best_user = None
            max_new_contribution = -1
            
            # Find the user who adds the most new candidates in this step
            for user, reach_set in remaining_influencers.items():
                new_contribution = len(reach_set - globally_covered)
                if new_contribution > max_new_contribution:
                    max_new_contribution = new_contribution
                    best_user = user
            
            # If no one can contribute new users, we're done
            if max_new_contribution == 0:
                break
            
            ranked_influencers.append(best_user)
            globally_covered.update(all_reach_sets[best_user])
            del remaining_influencers[best_user]
            
        return ranked_influencers

    def _get_all_reach_sets(self):
        
        reach_sets_cache = {}
        for user in self.graph:
            if user not in reach_sets_cache:
                self._calculate_reach_set_recursive(user, reach_sets_cache)
        return reach_sets_cache

    def _calculate_reach_set_recursive(self, user, cache):
        
        if user in cache:
            return cache[user]
        
        reach_set = set(self.graph.get(user, []))
        
        for direct_referral in self.graph.get(user, []):
            reach_set.update(self._calculate_reach_set_recursive(direct_referral, cache))
            
        cache[user] = reach_set
        return reach_set

    # Metric 2: Flow Centrality 
    def get_influencers_by_flow_centrality(self):

        distances = self._get_all_pairs_shortest_paths()
        users = list(self.graph.keys())
        flow_scores = {user: 0 for user in users}
        
        for s in users:
            for t in users:
                if s == t or t not in distances.get(s, {}):
                    continue
                
                dist_st = distances[s][t]
                
                for v in users:
                    if v == s or v == t:
                        continue
                        
                    if v in distances.get(s, {}) and t in distances.get(v, {}):
                        if distances[s][v] + distances[v][t] == dist_st:
                            flow_scores[v] += 1
                            
        sorted_by_score = sorted(flow_scores.items(), key=lambda item: item[1], reverse=True)
        return [user for user, score in sorted_by_score]


    def _get_all_pairs_shortest_paths(self):
        
        distances = {}
        for source_node in self.graph:
            distances[source_node] = {source_node: 0}
            queue = deque([(source_node, 0)])
            
            while queue:
                current_node, dist = queue.popleft()
                for neighbor in self.graph.get(current_node, []):
                    if neighbor not in distances[source_node]: # this if statement is unecessary due to constraints
                        distances[source_node][neighbor] = dist + 1
                        queue.append((neighbor, dist + 1))
                        
        return distances
        