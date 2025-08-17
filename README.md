# Mercor Challenge: Referral Network

This repository contains the complete solution for the Mercor coding challenge, implemented in Python. The project is organized into logical modules for the referral network graph, simulation, and optimization logic, and includes a comprehensive test suite that validates all functionality.

## Language & Setup

Language: Python
Version: 3.11.0
Dependencies: None

To set up the project, simply clone the repository. No dependency installation is required.

git clone https://github.com/xxXazLuCaRzdXxx/mercor-challenge

cd mercor-challenge

## Running Tests

Here is the command for running the test cases: 

python -m unittest discover

## Design Choices & Implementation Notes

### Part 1: Referral Graph Data Structure

The core of the referral network is implemented in the ReferralNetwork class. The primary data structure is an adjacency list (using a Python dict) to store the graph. This provides efficient O(1) average time complexity for adding new users and retrieving their direct referrals.
The implementation strictly enforces the three required constraints:

Unique Referrer Constraint: This is enforced by a separate referrers dictionary that maps a candidate to their unique referrer. This allows for an O(1) check to see if a candidate has already been referred before adding a new one.

Acyclic Graph Constraint: To prevent cycles, the code performs an efficient upstream traversal from the referrer. Before adding a new edge referrer -> candidate, it checks if the candidate is an ancestor of the referrer. This check is highly efficient, with a time complexity of O(d) where d is the depth of the referrer in the network.

No Self-Referrals: A simple check (referrer == candidate) is performed at the beginning of the add_referral method.

### Part 2: Top Referrers & Choosing k

The get_top_k_referrers function is implemented as described in the prompt, by calling the get_total_referral_count function (which uses a standard BFS traversal) for each user in the network and sorting the results.
The choice of an appropriate k is dependent on the business objective:

For a Public Leaderboard: A small, fixed number like k = 10 or k = 20 is suitable for display and encouraging competition.
For a Marketing Campaign: k could be a larger number like 50 or 100 to identify a significant group of key influencers to reward.
For Internal Analysis: k is often best calculated as a percentage of the total user base (e.g., the top 1%) to make the analysis scalable as the network grows.

### Part 3: Comparison of Influence Metrics

This project implements three distinct metrics for identifying influential users, each suited for a different business scenario:

Total Reach (Part 2):
Measures: Gross network size or "audience". It identifies users who can broadcast a message to the most people, regardless of audience overlap.
Business Scenario: Best for simple, broad marketing campaigns where the goal is maximum message saturation, such as awarding a "Top Referrer of the Month" prize.

Unique Reach Expansion (Part 3):
Measures: Network coverage and efficiency. It identifies the most efficient set of users to activate to cover the maximum number of unique individuals with minimal redundancy.
Business Scenario: Ideal for targeted marketing with a limited budget. For example, selecting a small, diverse group of "brand ambassadors" to promote a new feature, ensuring minimal audience overlap and maximum new exposure.

Flow Centrality (Part 3):
Measures: Network health and connectivity. It finds the critical "brokers" or "connectors" who bridge different communities within the network.
Business Scenario: A network health metric, useful for community management and risk analysis. It can identify key users who are vital for information flow or whose departure would fragment the user base.

## Algorithmic Complexity and Implementation Details

Here V is the number of users (vertices), E is the number of referrals (edges), d is the depth of a user, C is the number of active cohorts in the simulation, and D is the maximum number of simulation days.

#### ReferralNetwork Class

1. add_referral(referrer, candidate):
- Implementation: The method first runs O(1) checks for self-referrals and unique referrers. The main work is the cycle check, which performs an upstream traversal from the referrer to see if the candidate is an ancestor.
- Time Complexity: O(d). The performance is dominated by the cycle check, which in the worst case traverses the entire chain of referrers above the given referrer, a path of length d.
- Space Complexity: O(1). The operation uses a fixed amount of extra memory, regardless of the graph's size.
<br>

2. get_total_referral_count(user):

- Implementation: This method performs a Breadth-First Search (BFS) starting from the given user's direct referrals. Due to the "unique referrer" constraint, the referral graph is a forest, so a visited set is not required for correctness.
- Time Complexity: O(V_sub + E_sub), where V_sub and E_sub are the number of users and referrals in the subgraph downstream from the user. This is the standard optimal complexity for a graph traversal.
- Space Complexity: O(V_sub). In the worst case (a very wide and shallow referral tree), the BFS queue could hold all nodes at a single level.
<br>

3. get_top_k_referrers(k):

- Implementation: This function iterates through every user in the graph. For each user, it calls get_total_referral_count to calculate their full downstream reach. The results are stored, sorted in descending order by reach, and the names of the top k users are returned.
- Time Complexity: O(V * (V + E)). The function calls get_total_referral_count (which can be up to O(V+E)) for each of the V users. The final sort of O(V log V) is overshadowed by this main loop.
- Space Complexity: O(V). Space is required to store the reach count for all V users before sorting.
<br>

4. get_influencers_by_unique_reach():

- Implementation: This follows a greedy algorithm. It first pre-computes the reach set for all users using a memoized recursion (O(V+E)). Then, it enters a loop that runs up to V times. In each iteration, it finds the user who adds the most new members to the globally covered set, which involves iterating over the remaining users and performing set difference operations.
- Time Complexity: O(V^2 * avg_set_size). The nested loop structure for the greedy selection dominates the complexity.
- Space Complexity: O(V^2) in the worst case. The space is required to store the reach set for every user, if in a graph the first user's set contains all other V users.
<br>

5. get_influencers_by_flow_centrality():

- Implementation: This is a clear, correct implementation as prioritized by the prompt. It first computes all-pairs shortest paths by running BFS from every node (O(V * (V+E))). It then iterates through every possible triplet of users (s, t, v) to check if v lies on a shortest path between s and t.
- Time Complexity: O(V^3). The three nested loops for checking every triplet are the dominant factor.
- Space Complexity: O(V^2). This is required to store the distance matrix for all pairs of users.
<br>

#### Simulation & Optimization Functions:

6. simulate(p, days):

- Implementation: This function simulates network growth for a fixed number of days. Instead of tracking thousands of individual agents, it groups users into "cohorts" to efficiently calculate the expected number of new referrals each day. This model correctly handles the retirement of cohorts that reach their 10-referral capacity. A safety limit (MAX_SIMULATION_DAYS) is included as a circuit breaker to prevent impractically long simulations (for handling Part 5 test cases), which could otherwise occur with very low referral probabilities.
- Time Complexity: O(days * C). The complexity is linear with respect to the number of days simulated and the number of active cohorts.
- Space Complexity: O(days + C). O(days) is for the results list, and O(C) is for the queue holding the active cohorts.
<br>

7. days_to_target(p, target_total):

- Implementation: This function simulates day by day until a target_total is reached. It has a safety circuit breaker (D = MAX_SIMULATION_DAYS) to prevent impractically long loops.
- Time Complexity: O(D * C). In the worst case, it simulates up to D days, processing C cohorts each day.
- Space Complexity: O(C). The space is primarily for the active_cohorts queue.
<br>

8. min_bonus_for_target(days, target_hires, adoption_prob_func, eps):

- Implementation: This function uses a binary search to find the minimum required bonus. In each step of the search, it calls the days_to_target function to evaluate the effectiveness of the chosen bonus.
- Time Complexity: O(log(N) * D * C). The binary search over the bonus range N takes log(N) steps. Each step is dominated by the call to days_to_target, which has a complexity of O(D * C).
- Space Complexity: O(C). The space complexity is determined by the days_to_target helper function.

