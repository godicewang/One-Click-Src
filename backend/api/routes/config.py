import json
from pathlib import Path

import aiofiles
from fastapi import APIRouter
from pydantic import BaseModel  # 数据校验


class ConfigPayload(BaseModel):
    base_url: str
    model_name: str
    api_key: str


router = APIRouter(prefix="/api", tags=["config"])

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"


@router.post("/config")
async def update_config(payload: ConfigPayload):
    """接收前端传来的配置并写入 backend/config.json。"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    serialized = json.dumps(payload.model_dump(), indent=2, ensure_ascii=False)
    async with aiofiles.open(CONFIG_PATH, "w", encoding="utf-8") as f:
        await f.write(serialized)

    return {"success": True}


