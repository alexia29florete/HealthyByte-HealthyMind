from typing import List, Dict
import re

# Lightweight, deterministic heuristics:
# - food extraction: captures simple food words from a small whitelist + token heuristics
# - emotion detection: keyword spotting for common emotions

FOOD_HINTS = {
    "pizza","salad","salata","burger","pasta","spaghetti","supa","ciorba","paine","pâine",
    "ou","oua","iaurt","yogurt","lapte","milk","chicken","pui","rice","orez","banana","banane",
    "apple","mar","mere","chocolate","ciocolata","cake","prajitura","prăjitură","fish","peste","pește",
    "avocado","tomato","rosie","roșie","cartofi","potato","carne","beef","porc","pork"
}

EMOTION_RULES = {
    "anxious": ["anxios", "anxioasa", "anxioasă", "anxietate", "anxiety", "worried", "panic"],
    "sad": ["trist", "trista", "tristă", "depressed", "depresiv", "depresie", "down"],
    "stressed": ["stres", "stresat", "stresata", "stresată", "stress"],
    "happy": ["fericit", "fericita", "fericită", "bucuros", "happy", "glad"],
    "angry": ["nervos", "nervoasa", "nervoasă", "furios", "angry", "mad"],
    "guilty": ["vinovat", "vinovata", "vinovată", "guilty", "shame", "rusine", "rușine"],
    "calm": ["calm", "relaxat", "relaxata", "relaxată", "relaxed", "linistit", "liniștit"]
}

def _tokenize(text: str) -> List[str]:
    return re.findall(r"[\wăâîșțĂÂÎȘȚ'-]+", text.lower())

def extract_food(entry_text: str) -> List[str]:
    tokens = _tokenize(entry_text)
    foods = set()

    for t in tokens:
        if t in FOOD_HINTS:
            foods.add(t)

    # Also catch patterns like "am mancat X" / "i ate X"
    patterns = [
        r"(?:am\s+mancat|am\s+mâncat|i\s+ate)\s+([\wăâîșțĂÂÎȘȚ'-]+)",
        r"(?:am\s+avut|i\s+had)\s+([\wăâîșțĂÂÎȘȚ'-]+)\s+(?:la|for)\s+(?:pranz|prânz|cina|breakfast|lunch|dinner)"
    ]
    for pat in patterns:
        for m in re.finditer(pat, entry_text.lower()):
            foods.add(m.group(1))

    return sorted(foods)

def detect_emotions(entry_text: str) -> List[str]:
    text = entry_text.lower()
    emotions = []
    for label, kws in EMOTION_RULES.items():
        if any(kw in text for kw in kws):
            emotions.append(label)
    return emotions

def analyze_entry(entry_text: str) -> Dict:
    foods = extract_food(entry_text)
    emotions = detect_emotions(entry_text)
    return {"foods": foods, "emotions": emotions}
