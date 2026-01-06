"""
Integrator: OpenAI + MCP OpenNutrition
Analizează jurnalul alimentar cu date nutriționale reale
"""
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

class SmartFoodAnalyzer:
    """Analizor alimentar inteligent care combină OpenAI cu MCP"""
    
    def __init__(self):
        # OpenAI setup
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found!")
        self.openai_client = OpenAI(api_key=api_key)
        
        # MCP setup
        self.node_path = "/home/maria/.nvm/versions/node/v20.19.6/bin/node"
        self.mcp_path = "/home/maria/mcp-opennutrition/build/index.js"
    
    def extract_foods_with_llm(self, user_text):
        """
        Pasul 1: Folosește OpenAI pentru a extrage alimentele din text
        
        Returns:
            Lista de alimente menționate (fără date nutriționale)
        """
        prompt = f"""
Analizează următorul text și extrage DOAR numele alimentelor menționate.
Returnează un JSON cu lista de alimente, fără cantități sau alte detalii.

Text utilizator: "{user_text}"

Format răspuns (JSON):
{{
  "foods": ["apple", "bread", "cheese"]
}}

Răspunde DOAR cu JSON valid, nimic altceva.
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You extract food names from text. Return only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        data = json.loads(result_text)
        return data.get("foods", [])
    
    async def get_nutrition_from_mcp(self, food_names):
        """
        Pasul 2: Obține date nutriționale reale din MCP pentru fiecare aliment
        
        Returns:
            Dict cu date nutriționale pentru fiecare aliment
        """
        server_params = StdioServerParameters(
            command=self.node_path,
            args=[self.mcp_path],
            env=None
        )
        
        nutrition_data = {}
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                for food_name in food_names:
                    try:
                        result = await session.call_tool(
                            "search-food-by-name",
                            arguments={"query": food_name}
                        )
                        nutrition_data[food_name] = result
                    except Exception as e:
                        print(f"⚠️ Nu s-au găsit date pentru '{food_name}': {e}")
                        nutrition_data[food_name] = None
        
        return nutrition_data
    
    def analyze_with_llm(self, user_text, nutrition_data):
        """
        Pasul 3: Trimite datele reale către OpenAI pentru analiză finală
        
        Returns:
            Feedback empatic și sugestii bazate pe date reale
        """
        # Parsează și extrage datele nutriționale specifice din JSON
        nutrition_summary = ""
        for food_name, data in nutrition_data.items():
            if data and not data.isError and data.content:
                try:
                    # Parsează JSON-ul din content
                    foods_list = json.loads(data.content[0].text)
                    if foods_list and len(foods_list) > 0:
                        # Ia primul rezultat (cel mai relevant)
                        food_info = foods_list[0]
                        nutr = food_info.get('nutrition_100g', {})
                        
                        nutrition_summary += f"\n- {food_name} ({food_info.get('name', 'Unknown')}):\n"
                        nutrition_summary += f"  * Calorii: {nutr.get('calories', 'N/A')} kcal/100g\n"
                        nutrition_summary += f"  * Proteine: {nutr.get('protein', 'N/A')}g/100g\n"
                        nutrition_summary += f"  * Grăsimi: {nutr.get('total_fat', 'N/A')}g/100g\n"
                        nutrition_summary += f"  * Carbohidrați: {nutr.get('carbohydrates', 'N/A')}g/100g\n"
                        nutrition_summary += f"  * Fier: {nutr.get('iron', 'N/A')}mg/100g\n"
                        nutrition_summary += f"  * Potasiu: {nutr.get('potassium', 'N/A')}mg/100g\n"
                        nutrition_summary += f"  * Calciu: {nutr.get('calcium', 'N/A')}mg/100g\n"
                        nutrition_summary += f"  * Vitamina A: {nutr.get('vitamin_a', 'N/A')}µg/100g\n"
                        nutrition_summary += f"  * Vitamina C: {nutr.get('vitamin_c', 'N/A')}mg/100g\n"
                        nutrition_summary += f"  * Vitamina D: {nutr.get('vitamin_d', 'N/A')}µg/100g\n"
                    else:
                        nutrition_summary += f"\n- {food_name}: Nu s-au găsit rezultate\n"
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    nutrition_summary += f"\n- {food_name}: Eroare la parsare: {e}\n"
            else:
                nutrition_summary += f"\n- {food_name}: Date indisponibile\n"
        
        prompt = f"""
Ești un asistent profesional și empatic de nutriție și sănătate mentală.

Utilizatorul a spus: "{user_text}"

Date nutriționale REALE din baza de date:
{nutrition_summary}

Analizează aceste date și oferă un răspuns sub forma unui text continuu, profesional dar prietenos. NU folosi liste numerotate, bullet points sau fragmente separate (cu excepția valorilor nutriționale).

Structura răspunsului:
1. Începe cu valorile nutriționale totale în format:
   - Calorii totale: X kcal
   - Proteine: Xg
   - Grăsimi: Xg
   - Carbohidrați: Xg
   - Fier: Xmg (sau menționează dacă date indisponibile)
   - Potasiu: Xmg (sau menționează dacă date indisponibile)
   - Calciu: Xmg (sau menționează dacă date indisponibile)
   - Vitamina A: X (sau menționează dacă date indisponibile)
   - Vitamina C: X (sau menționează dacă date indisponibile)
   - Vitamina D: X (sau menționează dacă date indisponibile)

2. După această listă, continuă cu text fluid care include:
- Analiza echilibrului nutrițional (ce lipsește sau e deficitar și ce efecte poate avea)
- Ce nutrienți sunt în exces și ce efecte poate avea
- Impactul asupra stării emoționale și nivelului de energie
- Feedback empatic și realist, fără exagerări
- Sugestii practice și concrete
- O recomandare pentru următoarea masă

Ton: Profesional dar empatic, direct și sincer, fără formule exagerate de tipul "mă bucur", "hai să vedem", etc. Vorbește clar și la obiect.
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional, empathetic nutrition assistant. Write in a clear, direct style without excessive friendliness or exaggeration."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def analyze_complete(self, user_text):
        """
        Analiza completă: LLM + MCP + LLM
        
        Fluxul complet în 3 pași:
        1. OpenAI extrage alimente din text
        2. MCP obține date nutriționale reale
        3. OpenAI analizează cu date reale și oferă feedback
        """
        # Pasul 1: Extrage alimente
        foods = self.extract_foods_with_llm(user_text)
        
        # Pasul 2: Obține date nutriționale
        nutrition_data = await self.get_nutrition_from_mcp(foods)
        
        # Pasul 3: Analiză finală
        final_analysis = self.analyze_with_llm(user_text, nutrition_data)
        
        return final_analysis


# Test integrat
async def test_complete():
    """Test complet: OpenAI + MCP"""
    
    analyzer = SmartFoodAnalyzer()
    
    # Exemplu de input utilizator
    user_input = "Am mâncat 200g pâine, 150g ouă fierte și 80g brânză. Mă simt vinovat că am mâncat prea mult."
    
    # Analiza completă
    result = await analyzer.analyze_complete(user_input)
    
    print(result)


if __name__ == "__main__":
    try:
        asyncio.run(test_complete())
    except KeyboardInterrupt:
        print("\n⚠️ Întrerupt de utilizator")
    except Exception as e:
        print(f"❌ Eroare: {e}")
        import traceback
        traceback.print_exc()
