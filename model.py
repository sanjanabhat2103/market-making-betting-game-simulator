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

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

