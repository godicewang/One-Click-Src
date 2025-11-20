import json
import asyncio
from openai import AsyncOpenAI
from tool import basic_tool




async def main():
    config = await basic_tool.load_config()
    print("Config loaded:", config)
    # TODO: 每次调用模型的时候load config


if __name__ == "__main__":
    asyncio.run(main())