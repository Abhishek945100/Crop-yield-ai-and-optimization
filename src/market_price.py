import pandas as pd
import random

# =========================
# 📊 Price Fetch (FINAL)
# =========================
def get_price_details(crop, season, state, city):
    try:
        df = pd.read_csv("data/mandi_prices.csv")

        row = df[
            (df["crop"] == crop) &
            (df["season"] == season) &
            (df["state"] == state) &
            (df["city"] == city)
        ]

        if not row.empty:
            base_min = int(row["min_price"].values[0])
            base_max = int(row["max_price"].values[0])
        else:
            crop_df = df[df["crop"] == crop]
            base_min = int(crop_df["min_price"].mean())
            base_max = int(crop_df["max_price"].mean())

        # 🔥 dynamic fluctuation
        random.seed(f"{crop}-{state}-{season}")
        fluctuation = random.randint(-200, 200)

        min_price = max(1000, base_min + fluctuation)
        max_price = base_max + fluctuation
        modal_price = (min_price + max_price) // 2

        return {
            "min": min_price,
            "max": max_price,
            "modal": modal_price
        }

    except Exception as e:
        print("Price error:", e)
        return {"min": 1500, "max": 2500, "modal": 2000}


# =========================
# 💰 PROFIT FUNCTION (IMPORTANT)
# =========================
def estimate_profit(predicted_yield, land_size, crop, season, state, city):

    price_data = get_price_details(crop, season, state, city)
    price = price_data["modal"]

    # 🌾 cost
    cost_components = {
        "wheat": {"seed": 2500, "fertilizer": 6000, "labor": 7000, "irrigation": 4000},
        "rice": {"seed": 3000, "fertilizer": 7000, "labor": 9000, "irrigation": 6000},
        "maize": {"seed": 2000, "fertilizer": 5000, "labor": 6000, "irrigation": 5000},
        "mustard": {"seed": 1500, "fertilizer": 4000, "labor": 5000, "irrigation": 4500},
        "gram": {"seed": 1800, "fertilizer": 4500, "labor": 5000, "irrigation": 3500},
        "cotton": {"seed": 3500, "fertilizer": 9000, "labor": 10000, "irrigation": 7500},
        "soybean": {"seed": 2200, "fertilizer": 5500, "labor": 6000, "irrigation": 5000},
        "watermelon": {"seed": 4000, "fertilizer": 6000, "labor": 7000, "irrigation": 5000},
        "muskmelon": {"seed": 4200, "fertilizer": 6200, "labor": 7200, "irrigation": 5200},
        "cucumber": {"seed": 3800, "fertilizer": 5800, "labor": 6500, "irrigation": 4800}
    }

    components = cost_components.get(
        crop,
        {"seed": 2000, "fertilizer": 5000, "labor": 6000, "irrigation": 4000}
    )

    cost_per_acre = sum(components.values())
    total_cost = cost_per_acre * land_size

    # 🌾 production
    total_tons = predicted_yield * land_size
    total_quintal = total_tons * 10

    # 💰 revenue & profit
    revenue = total_quintal * price
    profit = revenue - total_cost

    return profit, revenue, total_cost, total_tons, total_quintal, price_data, components, cost_per_acre