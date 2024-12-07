from typing import Literal

from .enums import DamageType


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
        "0": None,
    }

    DAMAGE_TYPES = {
        "1": DamageType.PHYSICAL,
        "physic": DamageType.PHYSICAL,
        "pure": DamageType.PHYSICAL,
        "2": DamageType.FIRE,
        "fire": DamageType.FIRE,
        "3": DamageType.ICE,
        "snow": DamageType.ICE,
        "ice": DamageType.ICE,
        "4": DamageType.ENERGY,
        "power": DamageType.ENERGY,
        "5": DamageType.LIGHT,
        "light": DamageType.LIGHT,
        "6": DamageType.POISON,
        "poison": DamageType.POISON,
        "none": DamageType.NONE,
        "null": DamageType.NONE,
        ";": DamageType.NONE,
    }

    @classmethod
    def unificate_weapon_type(cls, weapon_type: str) -> str | None | Literal["Unknown"]:
        return cls.WEAPON_TYPES.get(weapon_type, "Unknown")

    @classmethod
    def unificate_damage_type(cls, damage_type: str) -> DamageType:
        return cls.DAMAGE_TYPES[damage_type]
