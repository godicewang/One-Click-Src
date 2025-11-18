from dataclasses import dataclass
import json
from pathlib import Path
from openai import OpenAI


@dataclass
class AgentConfig:
    base_url: str
    model_name: str
    api_key: str

def load_config() -> AgentConfig:
    """加载配置文件"""
    config_path = Path(__file__).resolve().parents[1] / "config.json"
    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return AgentConfig(**data)


def main():
    config = load_config()
    client = OpenAI(api_key = config.api_key, base_url = config.base_url)
    print("Config loaded:", config)
    # TODO: 每次调用模型的时候load config


if __name__ == "__main__":
    main()