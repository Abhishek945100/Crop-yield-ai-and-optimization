def farmer_based_recommendation(irrigation, budget):
    if irrigation == "Low":
        crop = "maize"
    elif budget == "High":
        crop = "rice"
    else:
        crop = "wheat"

    return crop