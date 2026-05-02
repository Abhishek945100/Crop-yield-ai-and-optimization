import random

def recommend_seed_and_month(crop, season, ph, irrigation, budget):

    seed_db = {
        "rice": [
            {"name": "Pusa Basmati 1121", "type": "high", "ph": (6, 7.5), "water": "high"},
            {"name": "IR64", "type": "medium", "ph": (5.5, 7.5), "water": "medium"},
            {"name": "Swarna", "type": "low", "ph": (5, 8), "water": "low"}
        ],
        "wheat": [
            {"name": "HD-2967", "type": "high", "ph": (6, 7.5), "water": "medium"},
            {"name": "PBW-343", "type": "medium", "ph": (6, 8), "water": "medium"},
            {"name": "Lok-1", "type": "low", "ph": (5.5, 8), "water": "low"}
        ],
        "maize": [
            {"name": "HQPM-1", "type": "high", "ph": (6, 7.5), "water": "medium"},
            {"name": "Pioneer 30V92", "type": "medium", "ph": (6, 8), "water": "medium"},
            {"name": "Desi Maize", "type": "low", "ph": (5, 8.5), "water": "low"}
        ]
    }

    seeds = seed_db.get(crop, [])

    ranked = []

    for s in seeds:
        score = 0

        if s["type"] == budget.lower():
            score += 3

        if s["ph"][0] <= ph <= s["ph"][1]:
            score += 2

        if s["water"] == irrigation.lower():
            score += 2

        score += random.uniform(0, 1)

        ranked.append({
            "seed": s["name"],
            "score": round(score, 2)
        })

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:3]

    month_map = {
        "Rabi": "October–November",
        "Kharif": "June–July",
        "Zaid": "March–April"
    }

    month = month_map.get(season, "Seasonal")

    return ranked, month