import json
import asyncio
from openai import AsyncOpenAI
from tool import basic_tool
# Agent对话与管理机制
from tool.agent_talk import ChatMessage
from tool.agent_talk import ChatHistory
from tool.agent_talk import AgentTalker




async def main():
    config = await basic_tool.load_config()
    print("Config loaded:", config)
    # TODO: 每次调用模型的时候load config


if __name__ == "__main__":
    asyncio.run(main())