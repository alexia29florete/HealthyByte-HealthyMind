import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class NutritionMCP:
    def __init__(self, 
                 mcp_path="/home/maria/mcp-opennutrition/build/index.js",
                 node_path="/home/maria/.nvm/versions/node/v20.19.6/bin/node"):
        """
        Args:
            mcp_path: calea către build/index.js din mcp-opennutrition
            node_path: calea completă către node executable
        """
        self.session = None
        self.mcp_path = mcp_path
        self.node_path = node_path
    
    async def connect(self):
        """Conectează la MCP OpenNutrition server"""
        server_params = StdioServerParameters(
            command=self.node_path,
            args=[self.mcp_path],
            env=None
        )
        
        # Folosește async with pentru stdio_client
        stdio_context = stdio_client(server_params)
        self.stdio_read, self.stdio_write = await stdio_context.__aenter__()
        
        self.session = ClientSession(
            self.stdio_read,
            self.stdio_write
        )
        
        await self.session.initialize()
        print("✅ Conectat la OpenNutrition MCP!")
        
        # Listează tool-urile disponibile
        tools = await self.session.list_tools()
        print(f"📋 Tool-uri disponibile: {[t.name for t in tools.tools]}")
    
    async def search_food(self, food_name):
        """
        Caută un aliment în baza de date
        
        Args:
            food_name: numele alimentului (ex: "bread", "apple")
        
        Returns:
            informații despre aliment
        """
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(
            "search_food",
            arguments={"query": food_name}
        )
        
        return result
    
    async def get_nutrition_info(self, food_name, quantity_grams):
        """
        Obține informații nutriționale pentru un aliment
        
        Args:
            food_name: numele alimentului
            quantity_grams: cantitatea în grame
        
        Returns:
            dict cu calorii, proteine, carbs, grăsimi calculate
        """
        if not self.session:
            await self.connect()
        
        # Caută alimentul
        food_data = await self.search_food(food_name)
        
        # Aici ar trebui să extragi datele și să calculezi pe baza cantității
        # Formatul exact depinde de ce returnează MCP-ul
        return food_data
    
    async def close(self):
        """Închide conexiunea MCP"""
        if self.session:
            await self.session.close()
            print("Deconectat de la OpenNutrition MCP")

# Test
async def test_mcp():
    mcp = NutritionMCP()
    await mcp.connect()
    
    # Test căutare
    result = await mcp.get_nutrition_info("bread", 200)
    print(f"Nutrition info: {result}")
    
    await mcp.close()

if __name__ == "__main__":
    asyncio.run(test_mcp())