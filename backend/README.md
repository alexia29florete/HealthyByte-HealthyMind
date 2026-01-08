## HOW TO RUN THE APP


### Configure Environment Variables

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

### Install Python Dependencies and Run the Programm

**You need to be in the root directory, where ./run_dev.sh is located**

```bash
# Create virtual environment (from project root)
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r backend/requirements.txt

pip install "flet==0.27.6" "flet-web==0.27.6"

chmod +x ./run_dev.sh

./run_dev.sh
```