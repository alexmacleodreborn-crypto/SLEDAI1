def hospital_birth_suite():
    return {
        "id": "hospital.birth_suite",
        "type": "hospital_room",
        "features": [
            "bright_lights",
            "machines_beeping",
            "sterile_smell",
            "cold_air",
        ],
        "connected_to": ["hospital.corridor"],
    }

def family_home():
    return {
        "id": "home.main",
        "type": "house",
        "features": [
            "warm",
            "quiet",
            "fabric_smell",
        ],
        "connected_to": ["home.bedroom", "street.front"],
    }

def bedroom():
    return {
        "id": "home.bedroom",
        "type": "room",
        "features": [
            "bed",
            "soft_light",
            "quiet",
        ],
        "connected_to": ["home.main"],
    }