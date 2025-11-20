from dataclasses import dataclass
from pathlib import Path
import aiofiles
import json

@dataclass
class AgentConfig:
    base_url: str
    model_name: str
    api_key: str

async def load_config() -> AgentConfig:
    """加载配置文件"""
    config_path = Path(__file__).resolve().parents[2] / "config.json"
    async with aiofiles.open(config_path, "r", encoding="utf-8") as f:
        raw = await f.read()
    data = json.loads(raw)
    return AgentConfig(**data)  # 解包