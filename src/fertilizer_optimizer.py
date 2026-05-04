def fertilizer_recommendation(crop, n, p, k, ph, moisture):
    suggestions = []

    # 🌾 Crop-specific base fertilizer
    crop_base = {
        "rice": ["Urea 50 kg/acre", "DAP 25 kg/acre"],
        "wheat": ["Urea 45 kg/acre", "MOP 20 kg/acre"],
        "maize": ["NPK 20:20:20 - 30 kg/acre"],
        "mustard": ["SSP 25 kg/acre", "Urea 20 kg/acre"],
        "gram": ["DAP 20 kg/acre"],
        "soybean": ["Biofertilizer Rhizobium + DAP 20 kg/acre"]
    }

    suggestions.extend(crop_base.get(crop, ["Balanced NPK 25 kg/acre"]))

    # 🧪 Nutrient deficiency logic
    if n < 50:
        suggestions.append("Nitrogen low → Add extra Urea 15 kg/acre")

    if p < 30:
        suggestions.append("Phosphorus low → Add DAP 10 kg/acre")

    if k < 30:
        suggestions.append("Potassium low → Add MOP 10 kg/acre")

    # ⚗️ pH management
    if ph < 6:
        suggestions.append("Soil acidic → Add lime 20 kg/acre")
    elif ph > 7.5:
        suggestions.append("Soil alkaline → Add gypsum 20 kg/acre")

    # 💧 moisture management
    if moisture < 35:
        suggestions.append("Low moisture → Use water-soluble fertilizer")

    return suggestions