# Part 4: Network Growth Simulation

from collections import deque

INITIAL_REFERRERS = 100
REFERRAL_CAPACITY = 10

MAX_SIMULATION_DAYS = 1000


def simulate(p: float, days: int) -> list[float]:
    
    if p <= 0 or days <= 0:
        return [0.0] * days

    # A deque to manage cohorts of active referrers.
    active_cohorts = deque([(INITIAL_REFERRERS, 0)])
    
    total_active_referrers = float(INITIAL_REFERRERS)
    cumulative_referrals = 0.0
    daily_cumulative_totals = []

    for _ in range(days):

        if total_active_referrers < 1:
            daily_cumulative_totals.append(cumulative_referrals)
            continue

        # 1. Calculate new referrals for today
        new_referrals_today = total_active_referrers * p
        cumulative_referrals += new_referrals_today
        daily_cumulative_totals.append(cumulative_referrals)
        
        # 2. Age and retire existing cohorts
        temp_cohorts = deque()
        while active_cohorts:
            count, referrals_made = active_cohorts.popleft()
            
            # For convenience, each person in the cohort makes 'p' more referrals
            new_referrals_for_this_cohort = referrals_made + p
            
            if new_referrals_for_this_cohort < REFERRAL_CAPACITY:
                temp_cohorts.append((count, new_referrals_for_this_cohort))
            else:
                # If the group exceeds referral capacity, we make that group unactive
                total_active_referrers -= count
        
        active_cohorts = temp_cohorts

        # 3. Add the new cohort for the next day
        if new_referrals_today > 0:
            active_cohorts.append((new_referrals_today, 0.0))
            total_active_referrers += new_referrals_today
        
    return daily_cumulative_totals


def days_to_target(p: float, target_total: int) -> int:

    if target_total <= 0:
        return 0
    if p <= 0:
        return -1 

    active_cohorts = deque([(INITIAL_REFERRERS, 0)])
    total_active_referrers = float(INITIAL_REFERRERS)
    cumulative_referrals = 0.0
    days_elapsed = 0

    while cumulative_referrals < target_total:
        days_elapsed += 1
        
        if days_elapsed > MAX_SIMULATION_DAYS:
            return -1

        if total_active_referrers < 1:
            return -1

        # 1. Calculate new referrals for today
        new_referrals_today = total_active_referrers * p
        cumulative_referrals += new_referrals_today
        
        # 2. Age and retire existing cohorts
        temp_cohorts = deque()
        while active_cohorts:
            count, referrals_made = active_cohorts.popleft()
            new_referrals_for_this_cohort = referrals_made + p
            if new_referrals_for_this_cohort < REFERRAL_CAPACITY:
                temp_cohorts.append((count, new_referrals_for_this_cohort))
            else:
                total_active_referrers -= count
        
        active_cohorts = temp_cohorts

        # 3. Add the new cohort for the next day
        if new_referrals_today > 0:
            active_cohorts.append((new_referrals_today, 0))
            total_active_referrers += new_referrals_today

    return days_elapsed