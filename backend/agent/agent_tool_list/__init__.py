from __future__ import annotations

from typing import Any, Dict, List, MutableMapping, Sequence

from .base import BaseTool, ToolError, ToolResult
from .nmap import NmapTool
"""工具列表"""



class Tools:
    """工具容器，集中注册与调度可用工具"""

    def __init__(self, *tools: BaseTool) -> None:
        self._tools: MutableMapping[str, BaseTool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: BaseTool) -> None:
        """注册单个工具实例，名称重复时抛出异常。"""
        if tool.name in self._tools:
            raise ValueError(f"工具 {tool.name} 已被注册")
        self._tools[tool.name] = tool

    def has_tools(self) -> bool:
        """判断当前容器是否至少拥有一个可用工具。"""
        return bool(self._tools)

    def get(self, name: str) -> BaseTool:
        """根据名称获取对应工具实例。"""
        if name not in self._tools:
            raise ToolError(f"工具 {name} 未注册")
        return self._tools[name]

    async def run(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        """执行指定工具，并返回统一的 ToolResult。"""
        tool = self.get(name)
        return await tool.run(**arguments)

    def as_openai_tools(self) -> List[Dict[str, Any]]:
        """把容器内工具转换为 OpenAI 函数调用所需的描述。"""
        payload: List[Dict[str, Any]] = []
        for tool in self._tools.values():
            payload.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )
        return payload

    @classmethod
    def merge(cls, tool_sets: Sequence["Tools"]) -> "Tools":
        """把多个工具容器合并为一个新的容器。"""
        merged = cls()
        for tool_set in tool_sets:
            for name, tool in tool_set._tools.items():
                if name in merged._tools:
                    raise ValueError(f"重复注册工具: {name}")
                merged._tools[name] = tool
        return merged

    def list_names(self) -> List[str]:
        """列出容器中所有工具名称。"""
        return list(self._tools.keys())


__all__ = [
    "BaseTool",
    "ToolError",
    "ToolResult",
    "Tools",
    "NmapTool",
]

