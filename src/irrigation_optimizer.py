def irrigation_plan(rainfall, sunshine, moisture, crop):

    # 🌾 Crop-wise irrigation interval (in days)
    crop_schedule = {
        "rice": (3, 5),         # needs frequent water
        "wheat": (7, 12),
        "maize": (6, 10),
        "mustard": (12, 18),
        "barley": (10, 15),
        "gram": (12, 20),
        "cotton": (7, 12),
        "soybean": (6, 10),
        "watermelon": (4, 7),
        "muskmelon": (4, 7),
        "cucumber": (3, 6)
    }

    min_days, max_days = crop_schedule.get(crop, (7, 12))

    # 🌧️ Rainfall effect
    if rainfall > 200:
        return "No immediate irrigation needed (sufficient rainfall)"

    # 🌱 Soil moisture effect
    if moisture < 25:
        return f"Irrigation needed soon (every {min_days}–{min_days+2} days)"

    elif moisture > 60:
        return "Soil moisture is high → avoid irrigation"

    # ☀️ High temperature / sunshine
    if sunshine > 9:
        return f"Irrigate moderately (every {min_days+1}–{max_days} days)"

    # ✅ Normal condition
    return f"Irrigate every {min_days}–{max_days} days depending on soil condition"