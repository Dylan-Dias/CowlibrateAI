import math 
import itertools 
import .constants import BREED_PARAMS

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

def energy_limited_milk(nel_mcal):
    return nel_mcal / 0.74 

def protein_utilization(rdp, rup):
    rdp_eff = min(rdp / 0.10, 1.0)
    rup_eff = min(rup / 0.06, 1.0)
    return 0.6 * rdp_eff + 0.4 * rup_eff 

# Lactation Curve 
def lactation_curve(dim, breed):
    p = BREED_PARAMS[breed]