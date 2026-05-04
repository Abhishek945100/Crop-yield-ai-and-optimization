def next_crop(previous_crop):
    mapping = {
        "rice": "wheat",
        "wheat": "maize",
        "maize": "rice"
    }

    return mapping.get(previous_crop, "wheat")