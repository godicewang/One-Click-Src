from __future__ import annotations
import asyncio
import sys
from pathlib import Path

# 确保可以在任意目录执行此脚本
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from agent.tool.agent_talk import AgentTalker, ChatHistory, ChatMessage  # type: ignore  # noqa: E402
from agent.agent_tool_list.nmap import NmapTool  # type: ignore  # noqa: E402


async def main() -> None:
    nmap_tool = NmapTool()
    result = await nmap_tool.run(target="https://cyber.cuit.edu.cn/", mode = "host_discovery")  # "host_discovery", "fast_scan", "service_version"
    print(result)

if __name__ == "__main__":
    asyncio.run(main())