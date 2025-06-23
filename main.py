import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


logger = logging.getLogger(__name__)


async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""

    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API")

    config_file = "browser_mcp.json"

    logging.info("Initializing the chat!!!")

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

    agent = MCPAgent(
        llm = llm,
        client = client,
        max_steps = 15,
        memory_enabled = True
    )

    print("\n===== Interactive MCP Chat =====")
    print ("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("============================================\n")

    try:
        while True:
            user_input = input ("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower () == "clear" :
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f" \nError: {e}")
    finally:

        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
