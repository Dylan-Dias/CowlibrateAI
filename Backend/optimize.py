import sys
import json
import pulp  # import pulp as a whole for solver cmd access
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value

def run_optimization(bovines, feeds):
    if not bovines:
        return []

    feed_impact = {
        f['feed_type']: 1 + (f['feed_percentage'] / 100) * 0.1
        for f in feeds
    }

    prob = LpProblem("Maximize Milk Yield", LpMaximize)
    cow_vars = {
        cow['id']: LpVariable(f"cow_{cow['id']}", cat='Binary')
        for cow in bovines
    }

    prob += lpSum([
        cow_vars[cow['id']] * cow['milk_yield'] * feed_impact.get(cow['breed'], 1.0)
        for cow in bovines
    ])

    prob += lpSum([cow_vars[cow['id']] for cow in bovines]) <= 10
    prob += lpSum([
        cow_vars[cow['id']] * (1 if cow['health'].lower() == 'healthy' else 0)
        for cow in bovines
    ]) >= 1

    # Suppress solver output here:
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    selected = [
        {
            'id': cow['id'],
            'milk_yield': cow['milk_yield'],
            'health': cow['health'],
            'breed': cow['breed'],
            'lactation_stage': cow['lactation_stage'],
            'age': cow['age']
        }
        for cow in bovines
        if value(cow_vars[cow['id']]) == 1
    ]

    return selected

def main():
    input_data = json.load(sys.stdin)
    bovines = input_data.get('bovines', [])
    feeds = input_data.get('feeds', [])

    result = run_optimization(bovines, feeds)
    print(json.dumps({'selected_cows': result}))

if __name__ == '__main__':
    main()
