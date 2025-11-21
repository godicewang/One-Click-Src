from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

"""工具&工具结果基类"""


class ToolError(Exception):
    """工具执行过程中抛出的统一异常。"""


@dataclass
class ToolResult:
    """工具执行完成后返回的统一结果结构。"""

    name: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

    def to_chat_message_payload(self) -> Dict[str, Any]:
        """把工具结果转换为 ChatMessage 的格式"""
        payload = {
            "role": "tool_result",
            "name": self.name,
            "content": self.content,
        }
        if self.metadata is not None:
            payload["metadata"] = self.metadata
        return payload


class BaseTool:
    """所有工具的基类，约束必要的属性与接口。"""

    name: str
    description: str
    parameters: Dict[str, Any]

    async def run(self, **kwargs: Any) -> ToolResult:  # pragma: no cover - 接口定义
        raise NotImplementedError


