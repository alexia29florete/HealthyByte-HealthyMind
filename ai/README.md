# AI Module - HealthyByte-HealthyMind

AI-powered food journal analysis using OpenAI GPT-3.5 and MCP OpenNutrition database.

## Prerequisites

1. **Python 3.12+**
2. **Node.js v20.19+** (for MCP OpenNutrition)
3. **OpenAI API Key**

## Setup Instructions

### 1. Install MCP OpenNutrition

```bash
# Clone the repository
git clone https://github.com/deadletterq/mcp-opennutrition.git
cd mcp-opennutrition

# Install dependencies
npm install

# Build the project
npm run build
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

Edit `.env` file:
- **OPENAI_API_KEY**: Your OpenAI API key from https://platform.openai.com/api-keys
- **NODE_PATH**: Full path to your Node.js executable
  - Linux/Mac: Run `which node` to find it
  - Windows: Run `where node` to find it
- **MCP_OPENNUTRITION_PATH**: Full path to `mcp-opennutrition/build/index.js`

**Example `.env` file:**
```env
OPENAI_API_KEY=sk-proj-...your-key-here...
NODE_PATH=/home/username/.nvm/versions/node/v20.19.6/bin/node
MCP_OPENNUTRITION_PATH=/home/username/mcp-opennutrition/build/index.js
```

### 3. Install Python Dependencies

```bash
# Create virtual environment (from project root)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r ai/requirements.txt
```

### 4. Test the Setup

```bash
cd ai
python3 smart_analyzer.py
```

You should see:
- Nutritional summary with calculated values
- AI analysis of the food journal entry

## Usage

The main file is `smart_analyzer.py` which contains the `SmartFoodAnalyzer` class.

**Example:**
```python
import asyncio
from smart_analyzer import SmartFoodAnalyzer

async def analyze():
    analyzer = SmartFoodAnalyzer()
    user_input = "I ate 200g bread, 150g cucumber, and 80g cheese."
    result = await analyzer.analyze_complete(user_input)
    print(result)

asyncio.run(analyze())
```

## Architecture

### 3-Step Analysis Pipeline:
1. **LLM Extract** → OpenAI extracts food names from user text
2. **MCP Query** → MCP OpenNutrition retrieves nutritional data
3. **LLM Analyze** → OpenAI analyzes data and provides empathetic feedback

### Components:
- `extract_foods_with_llm()` - Extracts food items using GPT-3.5
- `get_nutrition_from_mcp()` - Queries MCP OpenNutrition database
- `analyze_with_llm()` - Generates nutritional analysis and recommendations
- `analyze_complete()` - Orchestrates the full pipeline

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Make sure you created `.env` file from `.env.example`
- Check that your API key is valid

**Error: "MCP_OPENNUTRITION_PATH not found"**
- Verify the path in `.env` points to `build/index.js`
- Make sure you ran `npm run build` in mcp-opennutrition folder

**Error: "No module named 'openai'"**
- Activate virtual environment: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## Team Notes

⚠️ **Do NOT commit `.env` file** - it contains your API key!

The `.env.example` file is committed to help others set up their environment.
