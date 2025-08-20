import sys
import json
import pulp
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value


def adjusted_yield(animal, feed_amount, hydration_amount, temperature, gait_score=1.0, bloat_index=0.0):
    # Lactation stage multiplier
    lactation_factor = {
        'early': 1.2,
        'mid': 1.0,
        'late': 0.8
    }
    lactation_mult = lactation_factor.get(animal['lactation_stage'].lower(), 1.0)

    # Age penalty (older than 6 loses 5% per year)
    age_penalty = max(0, (animal['age'] - 6) * 0.05)

    # Temperature penalty (hot environments reduce milk yield)
    temp_penalty = 1.0
    if temperature > 28:
        temp_penalty = 1 - 0.02 * (temperature - 28)

    # Bloat and gait modifiers from CV
    health_score = gait_score * (1 - bloat_index)

    # Final yield formula with feed/hydration impact (simplified linear model)
    return (
        animal['milk_yield'] *
        feed_amount *
        hydration_amount *
        lactation_mult *
        (1 - age_penalty) *
        temp_penalty *
        health_score
    )


def run_optimization(bovines, goats, feeds, temperature, hydration_data):
    if not bovines and not goats:
        return ['No herd data']

    herd = bovines + goats

    # Create optimization problem
    prob = LpProblem("Maximize Milk Yield for Entire Herd", LpMaximize)

    # Parameters (you can adjust these based on real data)
    total_feed_budget = 1000  # e.g., kg or $
    total_hydration_budget = 800  # e.g., liters
    max_feed_per_animal = 10
    max_hydration_per_animal = 8

    # Create decision variables for feed and hydration per animal
    feed_vars = {
        animal['id']: LpVariable(f"feed_{animal['id']}", 0, max_feed_per_animal)
        for animal in herd
    }

    hydration_vars = {
        animal['id']: LpVariable(f"hydration_{animal['id']}", 0, max_hydration_per_animal)
        for animal in herd
    }

    # Placeholder: You can replace these with actual CV scores
    dummy_gait_scores = {animal['id']: 1.0 for animal in herd}
    dummy_bloat_indices = {animal['id']: 0.0 for animal in herd}

    # Objective: Maximize total adjusted milk yield
    prob += lpSum([
        adjusted_yield(
            animal,
            feed_vars[animal['id']],
            hydration_vars[animal['id']],
            temperature,
            dummy_gait_scores[animal['id']],
            dummy_bloat_indices[animal['id']]
        )
        for animal in herd
    ])

    # Constraint: Feed budget
    prob += lpSum([feed_vars[a['id']] for a in herd]) <= total_feed_budget

    # Constraint: Hydration budget
    prob += lpSum([hydration_vars[a['id']] for a in herd]) <= total_hydration_budget

    # Optional: Require that all animals get at least some minimal feed and water
    for animal in herd:
        prob += feed_vars[animal['id']] >= 1
        prob += hydration_vars[animal['id']] >= 1

    # Solve problem silently
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Output selected feeding plan
    selected = []
    for animal in herd:
        if value(feed_vars[animal['id']]) > 0:
            selected.append({
                'id': animal['id'],
                'type': 'goat' if animal in goats else 'cow',
                'allocated_feed': round(value(feed_vars[animal['id']]), 2),
                'allocated_water': round(value(hydration_vars[animal['id']]), 2),
                'estimated_yield': round(adjusted_yield(
                    animal,
                    value(feed_vars[animal['id']]),
                    value(hydration_vars[animal['id']]),
                    temperature,
                    dummy_gait_scores[animal['id']],
                    dummy_bloat_indices[animal['id']]
                ), 2)
            })

    return selected
