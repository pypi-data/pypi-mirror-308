from enum import Enum


class ItemCategory(Enum):
    WEAPON = "weapon"
    COSTUME = "costume"
    BADGE = "badge"
    PET = "pet"


class SkillCategory(Enum):
    EQUIP = "equip"
    PET = "pet"


class DamageType(Enum):
    PHYSICAL = "Physical"
    FIRE = "Fire"
    ICE = "Ice"
    ENERGY = "Energy"
    LIGHT = "Light"
    POISON = "Poison"
    NONE = None
