from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class FoodAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found!")
        self.client = OpenAI(api_key=api_key)
    
    def analyze_entry(self, user_text):
       
        prompt = f"""
User ate: {user_text}

Calculate the calories and macronutrients and show them in a list.
Say only the total from all the aliments and every category on separate lines.
After that, say whether the person has too much or too low from one category.
Explain how that can affect their mood and energy (separate line).
Suggest what they should change in an empathetic way (separate line).
Make the ressponse personal, addressing to the user, not in general.
Suggest an idea of the next meal.
"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result_text = response.choices[0].message.content
        return result_text

# Test
if __name__ == "__main__":
    analyzer = FoodAnalyzer()
    
    # Exemplu de input utilizator
    test_input = "I ate: 200g bread, 150g boiled eggs, 80g cheese, 3 spoons oh honey"
    
    result = analyzer.analyze_entry(test_input)
    print(result)