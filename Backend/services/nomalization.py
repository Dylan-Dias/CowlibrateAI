# Take Raw Data from the DB, user input, JSON and convert it into safe, consistent, model ready objects 

# We will 
# Apply Defaults 
# Fix Units 
# Clamp Invalid values 
# Protect your biology from garbage input 

def normalize_cow(raw):

    # Normalize a raw cow record into a model-ready cow object 

    return {
        "id": raw["id"],
        "breed": raw.get("breed", "Holstein"),
        "age_years": max(1, float(raw.get("age", 3))),
        "days_in_milk": max(1, int(raw.get("days_in_milk", 60))),
        "health": raw.get("health_status", "healthy"),
        "scc": int(raw.get("somatic_cell_count", 150_000)),
        "water_intake": max(10.0, float(raw.get("water_intake", 60))),
        "last_milked_at": raw.get("last_milked_at"),
    }

def normalize_feed(raw): 
    
    # Normalize a feed ingredient (NRC-Style Units)

    return { 
        "name": raw["name"],
        "nel": max(0.5, float(raw["nel"])),          # Mcal/kg
        "cp": float(raw["cp"]) / 100.0,              # % → fraction
        "rdp": float(raw["rdp_frac"]),               # fraction of CP
        "rup": float(raw["rup_frac"]),               # fraction of CP
        "kg": max(0.0, float(raw["kg_per_day"])),
    }

def normalize_environment(raw):
    
    # Normalize Environmental Conditions 

    return {
        "indoor_temp": float(raw.get("indoor_temp", 18)),
        "outdoor_temp": float(raw.get("outdoor_temp", 15)),
    }