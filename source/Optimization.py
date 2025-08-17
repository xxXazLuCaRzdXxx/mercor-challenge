# Part 5: Referral Bonus Optimization

import math
from source.Simulation import days_to_target

# A reasonable upper bound for the bonus search space.
# We assume no bonus will ever need to be higher than this.
MAX_BONUS_SEARCH_RANGE = 5000.0

def min_bonus_for_target(days: int, target_hires: int, adoption_prob_func: callable, eps: float = 0.01) -> int | None:
    
    if target_hires <= 0:
        return 0

    low_bonus = 0.0
    high_bonus = MAX_BONUS_SEARCH_RANGE
    min_working_bonus = float('inf')

    while high_bonus - low_bonus > eps:
        mid_bonus = (low_bonus + high_bonus) / 2
        p = adoption_prob_func(mid_bonus)

        # Check if this bonus is sufficient
        days_needed = days_to_target(p, target_hires)
        if days_needed != -1 and days_needed <= days:
            # Try to find an even smaller bonus that also works.
            min_working_bonus = mid_bonus
            high_bonus = mid_bonus
        else:
            # This bonus is too low. We need to offer more.
            low_bonus = mid_bonus

    if min_working_bonus == float('inf'):
        # Check if the absolute max bonus works, as a last resort
        p_max = adoption_prob_func(MAX_BONUS_SEARCH_RANGE)
        days_needed = days_to_target(p_max, target_hires)
        if days_needed != -1 and days_needed <= days:
            min_working_bonus = MAX_BONUS_SEARCH_RANGE
        else:
            return None

    # Round the result UP to the nearest $10
    return math.ceil(min_working_bonus / 10) * 10