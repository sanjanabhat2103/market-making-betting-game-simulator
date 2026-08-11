"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    values = np.asarray(values, dtype = float)
    probabilities = np.asarray(probabilities, dtype = float)
    return float(np.sum(values * probabilities))

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    if not isinstance(sides, int) or sides < 1:
        raise ValueError("sides must be a positive integer")
    mean = (sides + 1) / 2
    reroll_faces = [face for face in range(1, sides + 1) if face < mean]
    value = (
        sum(face for face in range(1, sides + 1) if face not in reroll_faces)
        + len(reroll_faces) * mean
    ) / sides
    return {
        "value": value,
        "reroll_faces": sorted(reroll_faces),
    }

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    best_threshold = None
    best_value = float("-inf")
    for t in range(1, sides + 1):
        value = ((t + sides) / 2) - ((t - 1) / (sides - t + 1) * reroll_cost)
        if value > best_value:
            best_value = value
            best_threshold = t
    return {
        'threshold': best_threshold, 
        'value': best_value
    }

# Step 4 - red_black_card_game_value
from functools import lru_cache


def red_black_card_game_value(num_red, num_black):
    @lru_cache(maxsize = None)
    def V(r, b):
        if r == 0:
            return 0.0
        if b == 0:
            return float(r)
        total = r + b
        cont = (
            r / total * (1 + V(r - 1, b))
            + b / total * (-1 + V(r, b - 1))
        )

        return max(0.0, cont)
    r = num_red
    b = num_black
    if r == 0:
        cont = 0.0
    elif b == 0:
        cont = float(r)
    else:
        total = r + b
        cont = (
            r / total * (1 + V(r - 1, b))
            + b / total * (-1 + V(r, b - 1))
        )
    return {
        "value": max(0.0, cont),
        "stop_now": cont <= 0.0,
    }

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    half = spread_width / 2
    bid = fair_value - half
    ask = fair_value + half
    return {"bid": bid, "ask": ask}

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    c = state["cash"]
    i = state["inventory"]
    if side == "buy":
        c += size * ask
        i -= size
    elif side == "sell":
        c -= size * bid
        i += size
    return {"cash": c, "inventory": i}

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    return cash + inventory * settlement_value

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    informed_values = np.asarray(informed_values, dtype = float)
    informed_probabilities = np.asarray(informed_probabilities, dtype = float)
    ask_side_excess = np.maximum(informed_values - ask, 0)
    bid_side_excess = np.maximum(bid - informed_values, 0)
    return float(np.sum(informed_probabilities * ask_side_excess) + np.sum(informed_probabilities * bid_side_excess))

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    return base_spread + uncertainty

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    half = spread_width / 2.0
    shift = skew_strength * inventory
    mid_prime = fair_value - shift
    return {
        'bid': mid_prime - half,
        'ask': mid_prime + half,
    }

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    half_spread = (ask - bid) / 2.0
    if side == "buy":
        fair_value += adjustment * half_spread
    elif side == "sell":
        fair_value -= adjustment * half_spread
    return float(fair_value)

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    remaining_counts_c = dict(remaining_counts)
    remaining_counts_c[revealed_value] -= 1
    if remaining_counts_c[revealed_value] <= 0:
        del remaining_counts_c[revealed_value]
    N = sum(remaining_counts_c.values())
    if N == 0:
        ev = 0.0
    else:
        values = list(remaining_counts_c.keys())
        probabilities = [
            count / N for count in remaining_counts_c.values()
        ]
        ev = expected_value(values, probabilities)
    return {"remaining_counts": remaining_counts_c, "expected_value": ev}

# Step 13 - run_market_making_episode
def run_market_making_episode(true_value, counterparty_sides, initial_fair_value, config):
    base_spread = config.get("base_spread", 0)
    uncertainty = config.get("uncertainty", 0)
    skew_strength = config.get("skew_strength", 0)
    belief_adjustment = config.get("belief_adjustment", 0)
    cash = 0.0
    inventory = 0.0
    fair_value = initial_fair_value
    history = []
    for side in counterparty_sides:
        spread = uncertainty_spread(base_spread, uncertainty)
        quotes = inventory_skewed_quotes(fair_value, spread, inventory, skew_strength)
        state = execute_trade({"cash": cash, "inventory": inventory}, side, quotes["bid"], quotes["ask"])
        cash = state["cash"]
        inventory = state["inventory"]
        fair_value = update_fair_value_from_trade(fair_value, side, quotes["bid"], quotes["ask"], belief_adjustment)
        history.append({"bid": quotes["bid"], "ask": quotes["ask"], "side": side, "cash": cash, "inventory": inventory, "fair_value": fair_value})
    pnl = mark_to_market_pnl(cash, inventory, true_value)
    return {"pnl": pnl, "cash": cash, "inventory": inventory, "fair_value": fair_value, "history": history}

# Step 14 - summarize_episode_pnls
def summarize_episode_pnls(pnls):
    pnls = np.asarray(pnls, dtype = float)
    mean = float(np.mean(pnls))
    std = float(np.std(pnls))
    worst = float(np.min(pnls))
    return {'mean': mean, 'std': std, 'worst': worst}

