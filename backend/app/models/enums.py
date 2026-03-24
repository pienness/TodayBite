from enum import Enum


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    AFTERNOON_TEA = "afternoon_tea"
    DINNER = "dinner"
    LATE_NIGHT = "late_night"


class CalorieConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class NutrientLevel(str, Enum):
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class NutrientTag(str, Enum):
    HIGH_PROTEIN = "高蛋白"
    DIETARY_FIBER = "膳食纤维"
    VITAMIN_B = "维生素B族"
    VITAMIN_C = "维生素C"
    LOW_FAT = "低脂"
    LOW_CARB = "低碳水"
    IRON_RICH = "富含铁"
    CALCIUM_RICH = "富含钙"
    OMEGA_3 = "Omega-3"


class TasteLike(str, Enum):
    SPICY = "辣"
    MILD_SPICY = "微辣"
    LIGHT = "清淡"
    SWEET_SOUR = "酸甜"
    SALTY = "咸鲜"
    MALA = "麻辣"


class TasteExclude(str, Enum):
    NO_SPICY = "不吃辣"
    NO_GARLIC = "不吃蒜"
    NO_CILANTRO = "不吃香菜"
    NO_PORK = "不吃猪肉"
    NO_BEEF = "不吃牛肉"
    NO_SEAFOOD = "不吃海鲜"
    NO_ORGAN = "不吃内脏"
    VEGETARIAN = "素食"
    LACTOSE_FREE = "无乳糖"
    GLUTEN_FREE = "无麸质"


class LLMProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    OLLAMA = "ollama"
