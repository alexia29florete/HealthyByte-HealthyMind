"""
Test simplu pentru MCP OpenNutrition
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp():
    """Test conexiune MCP"""
    
    node_path = "/home/maria/.nvm/versions/node/v20.19.6/bin/node"
    mcp_path = "/home/maria/mcp-opennutrition/build/index.js"
    
    server_params = StdioServerParameters(
        command=node_path,
        args=[mcp_path],
        env=None
    )
    
    print("🔄 Conectare la MCP OpenNutrition...")
    
    # Folosește async with pentru gestionarea corectă
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inițializează sesiunea
            await session.initialize()
            print("✅ Conectat la MCP!")
            
            # Listează tool-urile
            tools = await session.list_tools()
            print(f"\n📋 Tool-uri disponibile:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test căutare 'apple'
            print("\n=== Test căutare 'apple' ===")
            result = await session.call_tool(
                "search-food-by-name",
                arguments={"query": "apple"}
            )
            print(f"Rezultat: {result}")
            
            # Test căutare 'bread'
            print("\n=== Test căutare 'bread' ===")
            result2 = await session.call_tool(
                "search-food-by-name",
                arguments={"query": "bread"}
            )
            print(f"Rezultat: {result2}")
            
            print("\n✅ Testare completă!")

if __name__ == "__main__":
    try:
        asyncio.run(test_mcp())
    except KeyboardInterrupt:
        print("\n⚠️  Întrerupt de utilizator")
    except Exception as e:
        print(f"❌ Eroare: {e}")
        import traceback
        traceback.print_exc()
