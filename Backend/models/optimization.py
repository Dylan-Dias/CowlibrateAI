    # Testable 
    # Resuable 
    # Callable from API, CRON Jobs, Dashboards 

from models.dairy_model import realistic_milk_yield
from models.priority import milking_priority 

def optimize_herd(cows, env, feeds, constraints):
    results = []

    for cow in cows:
        milk = realistic_milk_yield(cows, feeds, env)
        efficiency = milk / feeds["total_kg"]

        priority = milking_priority(cow, milk, efficiency)

        results.append({
            "cow_id": cow["id"],
            "ear_tag": cow["ear_tag"],
            "milk_yield": round(milk, 2),
            "efficiency": round(efficiency, 2),
            "priority": round(priority, 2)
        })

        return sorted(results, key=lambda x: x["priority"], reverse=True)
    
    