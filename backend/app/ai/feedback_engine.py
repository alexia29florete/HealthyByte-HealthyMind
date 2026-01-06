from typing import List, Dict, Any

def generate_feedback(foods: List[str], emotions: List[str], nutrients: Dict[str, Any]) -> str:
    parts: List[str] = []

    if emotions:
        parts.append(f"Am observat emoțiile: {', '.join(emotions)}.")
        if "anxious" in emotions or "stressed" in emotions:
            parts.append("Poate ajută să încetinești ritmul mesei și să respiri 1 minut înainte să mănânci.")
        if "guilty" in emotions:
            parts.append("Încearcă să eviți auto-critica; un singur episod nu definește progresul tău.")
    else:
        parts.append("Mulțumesc pentru jurnal. Dacă vrei, poți nota și cum te-ai simțit înainte și după masă.")

    if foods:
        parts.append(f"Alimente detectate: {', '.join(foods)}.")

    # basic nutrient hint
    kcal = (nutrients or {}).get("calories")
    if isinstance(kcal, (int, float)) and kcal > 0:
        parts.append(f"Estimare calorii: {int(round(kcal))} kcal.")

    parts.append("Recomandare generală: adaugă o sursă de proteine + fibre la următoarea masă (ex: iaurt + fruct, pui + salată).")
    return " ".join(parts)
