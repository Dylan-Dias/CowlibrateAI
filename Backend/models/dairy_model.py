import math 
import itertools 
from constants import BREED_PARAMS

# Biological and Environmental Adjustment Functions
def thi(indoor, outdoor):
    return indoor + 0.36 * outdoor 

def intake_adjustment(thi_value):
    if thi_value < 68:
        return 1.0
    return max(0.70, 1 - 0.02 * (thi_value - 68))

def scc_penalty(scc):
    if scc < 200_000:
        return 1.0
    if scc < 400_000:
        return 0.95
    return 0.85 

def bcs_adjustment(bcs):
    if 2.75 <= bcs <= 3.25:
        return 1.0
    if bcs <2.75:
        return 0.92
    return 0.95 

def water_cap(milk, water):
    return min(milk, water / 4.5)

# NRC / Energy / Protein Functions 

def energy_limited_milk(nel_mcal):
    return nel_mcal / 0.74 

def protein_utilization(rdp, rup):
    rdp_eff = min(rdp / 0.10, 1.0)
    rup_eff = min(rup / 0.06, 1.0)
    return 0.6 * rdp_eff + 0.4 * rup_eff 

# Lactation Curve 
def lactation_curve(dim, breed):
    p = BREED_PARAMS[breed]

# Realistic Milk Prediction Function 
def realistic_milk_yield(cow, feed_plan, env):
    base = lactation_curve(cow["days_in_milk"], cow["breed"])
    thi_val = thi(env["indoor_temp"], env["outdoor_temp"])
    intake_adj = intake_adjustment(thi_val)
    energy_cap = energy_limited_milk(feed_plan["nel_mcal"] * intake_adj)
    protein_eff = protein_utilization(feed_plan["rdp_kg"], feed_plan["rup_kg"])

    milk = min(base, energy_cap)
    milk *= protein_eff
    milk *= bcs_adjustment(cow["bcs"])
    milk *= cow["health_status"]
    milk *= scc_penalty(cow["scc"])
    milk = water_cap(milk, cow["water_intake"])
    return max(milk, 0)

# Feed Optimization Function 
def optimize_feed(cow, env, feed_library, constraints):
    best = None
    best_score = 0

    for amounts in itertools.product([4, 6, 8], repeat=len(feed_library)):
        total_kg = sum(amounts)
        total_cost = sum(amounts[i] * feed_library[i]["cost"] for i in range(len(feed_library)))
        if total_cost > constraints["budget"]:
            continue

        nel = sum(amounts[i] * feed_library[i]["nel"] * feed_library[i]["digestibility"] for i in range(len(feed_library)))
        rdp = sum(amounts[i] * (feed_library[i]["cp"] / 100) * feed_library[i]["rdp_frac"] for i in range(len(feed_library)))
        rup = sum(amounts[i] * (feed_library[i]["cp"] / 100) * feed_library[i]["rup_frac"] for i in range(len(feed_library)))

        feed_plan = {
            "nel_mcal": nel,
            "rdp_kg": rdp,
            "rup_kg": rup,
            "total_kg": total_kg,
            "cost": total_cost,
            "breakdown": dict(zip([f["name"] for f in feed_library], amounts))
        }

        milk = realistic_milk_yield(cow, feed_plan, env)
        efficiency = milk / total_kg if total_kg else 0

        if efficiency > best_score:
            best_score = efficiency
            best = {
                "milk_yield": milk,
                "efficiency": efficiency,
                "feed_plan": feed_plan
            }

    return best

# Function 
def explain_result(result):
    return {
        "summary": f"Optimized milk yield: {result['milk_yield']:.2f} L/day",
        "efficiency": f"{result['efficiency']:.2f} L/kg feed",
        "cost": f"${result['feed_plan']['cost']:.2f} per cow/day",
        "feed_breakdown": result["feed_plan"]["breakdown"],
        "notes": [
            "Milk limited by lactation stage and energy intake",
            "Protein balanced using RDP/RUP efficiency",
            "Heat stress and water intake accounted for",
            "BCS and SCC constrained to protect health"
        ]
    }
