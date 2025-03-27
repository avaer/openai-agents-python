import os
from agents import Agent, function_tool, Runner
from agents.mcp import MCPServerStdio

# Define a simple tool
@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

async def main():
    # Create an MCP server connection
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "filesystem_example/sample_files")
    
    # Use async context manager to properly connect to the MCP server
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as filesystem_mcp:
        # Create an agent with both our custom tool and the MCP server tools
        agent = Agent(
            name="Assistant",
            instructions="You're a helpful assistant with filesystem access and calculation abilities.",
            tools=[add],  # Add our custom tool
            mcp_servers=[filesystem_mcp]  # MCP plugins connect here
        )

        # Run the agent
        print("Running the agent...")
        result = await Runner.run(
            starting_agent=agent, 
            input="Use the filesystem tools to read the 'favorite_books.txt' file and then use the add tool to add 5 + 7."
        )
        
        print("\nAgent output:")
        print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())