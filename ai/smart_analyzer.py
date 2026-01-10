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
        
        # MCP setup - get paths from environment variables
        self.node_path = os.getenv("NODE_PATH", "node")  # Default to 'node' in PATH
        self.mcp_path = os.getenv("MCP_OPENNUTRITION_PATH")
        
        if not self.mcp_path:
            raise ValueError("MCP_OPENNUTRITION_PATH not found in .env file!")
    
    def extract_foods_with_llm(self, user_text):
        """
        Step 1: Use OpenAI to extract food names from text
        
        Returns:
            List of mentioned foods (without nutritional data)
        """
        prompt = f"""
                Analyze the following text and extract ONLY the food names mentioned.
                Return a JSON with the list of foods, without quantities or other details.

                User text: "{user_text}"

                Response format (JSON):
                {{
                "foods": ["apple", "bread", "cheese"]
                }}

                Respond ONLY with valid JSON, nothing else.
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
        Step 2: Get real nutritional data from MCP for each food
        
        Returns:
            Dict with nutritional data for each food
        """
        import sys
        import subprocess
        
        server_params = StdioServerParameters(
            command=self.node_path,
            args=[self.mcp_path],
            env=None
        )
        
        nutrition_data = {}
        
        # Suppress MCP server stdout messages
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
                        print(f"⚠️ No data found for '{food_name}': {e}")
                        nutrition_data[food_name] = None
        
        return nutrition_data
    
    def analyze_with_llm(self, user_text, nutrition_data):
        """
        Step 3: Send real data to OpenAI for final analysis
        
        Returns:
            Empathetic feedback and suggestions based on real data
        """
        # Parse and extract specific nutritional data from JSON
        # Calculate totals in Python (not in LLM)
        totals = {
            'calories': 0,
            'protein': 0,
            'total_fat': 0,
            'carbohydrates': 0,
            'iron': 0,
            'potassium': 0,
            'calcium': 0,
            'vitamin_a': 0,
            'vitamin_c': 0,
            'vitamin_d': 0
        }
        
        food_details = []
        foods_with_data = 0
        
        for food_name, data in nutrition_data.items():
            if data and not data.isError and data.content:
                try:
                    # Parse JSON from content
                    foods_list = json.loads(data.content[0].text)
                    if foods_list and len(foods_list) > 0:
                        # Take first result (most relevant)
                        food_info = foods_list[0]
                        nutr = food_info.get('nutrition_100g', {})
                        
                        # Accumulate totals (assuming 100g per food item - adjust as needed)
                        for key in totals.keys():
                            value = nutr.get(key if key != 'total_fat' else 'total_fat', 0)
                            if isinstance(value, (int, float)):
                                totals[key] += value
                        
                        foods_with_data += 1
                        food_details.append(f"{food_name} ({food_info.get('name', 'Unknown')})")
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    food_details.append(f"{food_name} (data unavailable)")
        
        # Round all values to 1 decimal
        for key in totals:
            totals[key] = round(totals[key], 1)
        
        # Format nutritional summary
        nutrition_summary = f"""
Total nutritional values (based on {foods_with_data} foods):
- Total Calories: {totals['calories']} kcal
- Protein: {totals['protein']} g
- Fat: {totals['total_fat']} g
- Carbohydrates: {totals['carbohydrates']} g
- Iron: {totals['iron']} mg
- Potassium: {totals['potassium']} mg
- Calcium: {totals['calcium']} mg
- Vitamin A: {totals['vitamin_a']} µg
- Vitamin C: {totals['vitamin_c']} mg
- Vitamin D: {totals['vitamin_d']} µg

Foods analyzed: {', '.join(food_details)}
"""
        
        prompt = f"""
You are a professional and empathetic nutrition and mental health assistant.

User said: "{user_text}"

REAL nutritional data from database:
{nutrition_summary}

CRITICAL: The nutritional summary above is already displayed to the user. DO NOT repeat any numbers.

Start your response with: "In terms of nutritional balance, your meal..."

Then continue with:
- What's missing or deficient and potential effects
- What nutrients may be in excess and potential effects
- Impact on emotional state and energy levels
- Empathetic feedback about their guilt feelings
- Practical suggestions for improvement
- A specific recommendation for the next meal

Tone: Professional but empathetic, direct and honest.
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
        Complete analysis: LLM + MCP + LLM
        
        Complete flow in 3 steps:
        1. OpenAI extracts foods from text
        2. MCP gets real nutritional data
        3. OpenAI analyzes with real data and provides feedback
        """
        # Step 1: Extract foods
        foods = self.extract_foods_with_llm(user_text)
        
        # Step 2: Get nutritional data
        nutrition_data = await self.get_nutrition_from_mcp(foods)
        
        # Calculate and print nutritional totals first
        totals = {
            'calories': 0,
            'protein': 0,
            'total_fat': 0,
            'carbohydrates': 0,
            'iron': 0,
            'potassium': 0,
            'calcium': 0,
            'vitamin_a': 0,
            'vitamin_c': 0,
            'vitamin_d': 0
        }
        
        for food_name, data in nutrition_data.items():
            if data and not data.isError and data.content:
                try:
                    foods_list = json.loads(data.content[0].text)
                    if foods_list and len(foods_list) > 0:
                        food_info = foods_list[0]
                        nutr = food_info.get('nutrition_100g', {})
                        
                        for key in totals.keys():
                            value = nutr.get(key if key != 'total_fat' else 'total_fat', 0)
                            if isinstance(value, (int, float)):
                                totals[key] += value
                except:
                    pass
        
        # Round and print totals
        for key in totals:
            totals[key] = round(totals[key], 1)
        
        print("Nutritional Summary:")
        print(f"- Total Calories: {totals['calories']} kcal")
        print(f"- Protein: {totals['protein']}g")
        print(f"- Fat: {totals['total_fat']}g")
        print(f"- Carbohydrates: {totals['carbohydrates']}g")
        print(f"- Iron: {totals['iron']}mg")
        print(f"- Potassium: {totals['potassium']}mg")
        print(f"- Calcium: {totals['calcium']}mg")
        print(f"- Vitamin A: {totals['vitamin_a']}µg")
        print(f"- Vitamin C: {totals['vitamin_c']}mg")
        print(f"- Vitamin D: {totals['vitamin_d']}µg")
        print()
        
        # Step 3: Final analysis
        final_analysis = self.analyze_with_llm(user_text, nutrition_data)
        
        return final_analysis


# Integrated test
async def test_complete():
    """Complete test: OpenAI + MCP"""
    
    analyzer = SmartFoodAnalyzer()
    
    # Example user input
    user_input = "I ate 200g bread, 150g cucumber, and 80g cheese. I feel guilty that I ate too much."
    
    # Complete analysis
    result = await analyzer.analyze_complete(user_input)
    
    print(result)


if __name__ == "__main__":
    try:
        asyncio.run(test_complete())
    except KeyboardInterrupt:
        print("\n Interrupted by user")
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
