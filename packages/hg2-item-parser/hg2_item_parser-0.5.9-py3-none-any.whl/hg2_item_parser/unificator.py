from typing import Literal


class Unificator:
    WEAPON_TYPES = {
        "autogun": "Auto Rifle",
        "near_sword": "Melee",
        "near_saw": "Melee",
        "pistol_fast": "Pistol",
        "pistol_heavy": "Heavy Pistol",
        "place_ancient": "Deploy Ancient",
        "place_battery": "Deploy Battery",
        "place_doll": "Deploy Dolly",
        "place_induce": "Deploy Trap",
        "place_mine": "Deploy Mine",
        "place_special": "Deploy Special",
        "rpg": "RPG",
        "shotgun_multi": "Spread Shotgun",
        "shotgun_single": "Single Shotgun",
        "sniper": "Sniper Rifle",
        "special": "Special",
        "special_bow": "Bow",
        "spray": "Spray",
        "spray_active": "Activate Spray",
        "spray_enchanting": "Spray",
        "spray_switch": "Switch Spray",
        "throw": "Thrown",
        0: None,
    }

    DAMAGE_TYPES = {
        "1": "Physical",
        "2": "Fire",
        "3": "Ice",
        "4": "Energy",
        "5": "Light",
        "6": "Poison",
        "physic": "Physical",
        "pure": "Physical",
        "fire": "Fire",
        "snow": "Ice",
        "ice": "Ice",
        "power": "Energy",
        "light": "Light",
        "poison": "Poison",
        "none": None,
        "null": None,
        ";": None,
    }

    @classmethod
    def unificate_weapon_type(cls, weapon_type: str) -> str | None | Literal["Unknown"]:
        return cls.WEAPON_TYPES.get(weapon_type, "Unknown")

    @classmethod
    def unificate_damage_type(cls, damage_type: str) -> str | None | Literal["Unknown"]:
        return cls.DAMAGE_TYPES.get(damage_type, "Unknown")
