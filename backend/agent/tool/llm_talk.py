from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from openai import AsyncOpenAI
from tool import basic_tool


def _validate_agent_name(name: str) -> None:
    if not name.startswith("agent"):
        raise ValueError("agent_name 必须以 'agent' 开头")


@dataclass
class ChatMessage:
    """定义消息格式:完成存储、clone、格式转换"""
    role: str  # 消息角色（system/user/agent/tool_call/tool_result）
    content: str
    name: Optional[str] = None  # 消息名称（如agent_main）
    metadata: Optional[Dict[str, Any]] = None  # 元信息(保存额外的识别信息)

    def clone(self) -> "ChatMessage":
        """深拷贝本消息对象"""
        return ChatMessage(
            role = self.role,
            content = self.content,
            name = self.name,
            metadata = copy.deepcopy(self.metadata) if self.metadata else None,
        )

    def to_openai_payload(self) -> Dict[str, Any]:
        """把本消息对象转为openai可用格式"""
        role_map = {
            "system": "system",
            "user": "user",
            "agent": "assistant",
            "tool_call": "assistant",
            "tool_result": "assistant",
        }
        payload: Dict[str, Any] = {
            "role": role_map.get(self.role, "user"),
            "content": self.content,
        }
        if self.name:
            payload["name"] = self.name
        return payload


class ChatHistory:
    """统一管理聊天消息,支持system/agent/tool_call/tool_result/user五种消息"""

    def __init__(
        self,
        *,
        agent_name: str,  # 使用本次消息列表的agent的名字
        system_prompt: str,
        initial_messages: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> None:
        _validate_agent_name(agent_name)
        self._agent_name = agent_name
        self._system_prompt = system_prompt
        self._messages: List[ChatMessage] = []
        self._add_message(role="system", content=system_prompt, name=self._agent_name)
        if initial_messages:
            self._extend_from_raw(initial_messages)
    # ---- 基础操作 ----
    async def get_messages(self) -> List[ChatMessage]:
        return [msg.clone() for msg in self._messages]

    async def overwrite(self, new_messages: Sequence[ChatMessage]) -> None:
        self._messages = [msg.clone() for msg in new_messages]

    def _extend_from_raw(self, raw_messages: Sequence[Dict[str, Any]]) -> None:
        """初始化或覆盖时载入历史消息,仅采纳消息部分,system_prompt 永远以入参为准"""
        for raw in raw_messages:
            role = raw.get("role")
            content = raw.get("content", "")
            name = raw.get("name")
            metadata = raw.get("metadata")
            if role == "system":
                # 忽略外部传入的 system，统一使用初始化时提供的 system_prompt
                continue
            if role in ("agent", "assistant"):
                agent_name = name or self._agent_name
                self._add_message(role="agent", content=content, name=agent_name)
            elif role in ("tool_call",):
                self._add_message(
                    role="tool_call", content=content, metadata=metadata
                )
            elif role in ("tool_result", "tool"):
                self._add_message(
                    role="tool_result", content=content, metadata=metadata
                )
            else:
                self._add_message(role="user", content=content)

    async def extend_from_raw(self, raw_messages: Sequence[Dict[str, Any]]) -> None:
        self._extend_from_raw(raw_messages)

    async def to_openai_messages(self) -> List[Dict[str, Any]]:
        return [msg.to_openai_payload() for msg in self._messages]

    def _add_message(
        self,
        *,
        role: str,
        content: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatMessage:
        message = ChatMessage(role=role, content=content, name=name, metadata=metadata)
        self._messages.append(message)
        return message

    def _filter_messages(
        self,
        *,
        role: str,
        name: Optional[str] = None,
    ) -> List[ChatMessage]:
        return [
            msg.clone()
            for msg in self._messages
            if msg.role == role and (name is None or msg.name == name)
        ]

    def _delete_messages(self, *, role: str, name: Optional[str] = None) -> None:
        if role == "system":
            # 保证至少存在初始 system 消息
            self._messages = [
                msg
                for msg in self._messages
                if not (msg.role == role and msg is not self._messages[0])
            ]
            if not self._messages or self._messages[0].role != "system":
                self._messages.insert(
                    0,
                    ChatMessage(
                        role="system",
                        content=self._system_prompt,
                        name=self._agent_name,
                    ),
                )
            return

        self._messages = [
            msg
            for msg in self._messages
            if not (msg.role == role and (name is None or msg.name == name))
        ]

    def _get_latest_msg(
        self,
        *,
        role: str,
        name: Optional[str] = None,
    ) -> Optional[ChatMessage]:
        for msg in reversed(self._messages):
            if msg.role != role:
                continue
            if name is not None and msg.name != name:
                continue
            return msg.clone()
        return None

    # ---- system ----
    async def update_system_msg(self, content: str) -> ChatMessage:
        # 替换第一条 system 消息，若不存在则追加
        for idx, msg in enumerate(self._messages):
            if msg.role == "system":
                self._messages[idx] = ChatMessage(
                    role="system",
                    content=content,
                    name=self._agent_name,
                )
                return self._messages[idx]

        return self._add_message(
            role="system",
            content=content,
            name=self._agent_name,
        )

    async def get_system_msgs(self) -> List[ChatMessage]:
        return self._filter_messages(role="system")

    async def get_system_latest_msg(self) -> Optional[ChatMessage]:
        return self._get_latest_msg(role="system")

    async def delete_system_msgs(self) -> None:
        self._delete_messages(role="system")

    # ---- agent ----
    async def add_agent_msg(self, agent_name: str, content: str) -> ChatMessage:
        _validate_agent_name(agent_name)
        return self._add_message(
            role="agent", content=content, name=agent_name
        )

    async def get_agent_msgs(
        self, agent_name: Optional[str] = None
    ) -> List[ChatMessage]:
        return self._filter_messages(role="agent", name=agent_name)

    async def get_agent_latest_msg(
        self, agent_name: Optional[str] = None
    ) -> Optional[ChatMessage]:
        return self._get_latest_msg(role="agent", name=agent_name)

    async def delete_agent_msgs(self, agent_name: Optional[str] = None) -> None:
        self._delete_messages(role="agent", name=agent_name)

    # ---- user ----
    async def add_user_msg(self, content: str) -> ChatMessage:
        return self._add_message(role="user", content=content)

    async def get_user_msgs(self) -> List[ChatMessage]:
        return self._filter_messages(role="user")

    async def get_user_latest_msg(self) -> Optional[ChatMessage]:
        return self._get_latest_msg(role="user")

    async def delete_user_msgs(self) -> None:
        self._delete_messages(role="user")

    # ---- tool_call ----
    async def add_tool_call_msg(
        self, content: str, *, metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        return self._add_message(
            role="tool_call", content=content, metadata=metadata
        )

    async def get_tool_call_msgs(self) -> List[ChatMessage]:
        return self._filter_messages(role="tool_call")

    async def get_tool_call_latest_msg(self) -> Optional[ChatMessage]:
        return self._get_latest_msg(role="tool_call")

    async def delete_tool_call_msgs(self) -> None:
        self._delete_messages(role="tool_call")

    # ---- tool_result ----
    async def add_tool_result_msg(
        self, content: str, *, metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        return self._add_message(
            role="tool_result", content=content, metadata=metadata
        )

    async def get_tool_result_msgs(self) -> List[ChatMessage]:
        return self._filter_messages(role="tool_result")

    async def get_tool_result_latest_msg(self) -> Optional[ChatMessage]:
        return self._get_latest_msg(role="tool_result")

    async def delete_tool_result_msgs(self) -> None:
        self._delete_messages(role="tool_result")

    # ---- 其他辅助 ----
    async def clear_non_system(self) -> None:
        self._messages = [
            msg for msg in self._messages if msg.role == "system"
        ]

    async def replace_with_external(
        self, raw_messages: Sequence[Dict[str, Any]]
    ) -> None:
        self._messages = [
            ChatMessage(
                role="system",
                content=self._system_prompt,
                name=self._agent_name,
            )
        ]
        self._extend_from_raw(raw_messages)

    async def total_count(self) -> int:
        return len(self._messages)



class LLMTalker:
    """ 统一管理配置加载与 LLM 交互的异步封装"""

    def __init__(
        self,
        agent_name: str,
        system_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        max_chat_len: int = 30,
    ) -> None:
        """
        初始化配置参数

        Args:
            agent_name: 必填，必须以 agent 开头，代表当前 LLM Agent 的名字。
            system_prompt: 必填，作为整个会话的第一条 system 消息。
            chat_history: 可选的历史消息列表（不包含 system 消息），会被追加在 system 消息之后。
            max_chat_len: 触发历史压缩的最大消息条数。
        """
        self._client: Optional[AsyncOpenAI] = None
        self._config: Optional[basic_tool.AgentConfig] = None
        self._refresh()  # 加载配置
        _validate_agent_name(agent_name)
        self._agent_name = agent_name
        self._system_prompt = system_prompt
        self._max_chat_len = max_chat_len
        self._chat_history = ChatHistory(
            agent_name=self._agent_name,
            system_prompt=self._system_prompt,
            initial_messages=chat_history,
        )


    async def _refresh(self) -> None:
        """重新加载配置并实例化客户端"""
        self._config = await basic_tool.load_config()
        self._client = AsyncOpenAI(
            api_key = self._config.api_key,
            base_url = self._config.base_url,
        )

    async def _compress_if_needed(
        self, messages: List[ChatMessage]
    ) -> List[ChatMessage]:
        """
        当消息长度超过阈值时，压缩中间历史，仅保留：
        - 第一条 system 消息（system_prompt）
        - 最后一条消息（本次 query，或最后一条消息）
        中间内容通过大模型做摘要，替换为一条简短的总结消息。
        """
        max_len = self._max_chat_len
        if len(messages) <= max_len:
            return messages

        assert self._config is not None and self._client is not None

        # 保留首尾
        first_msg = messages[0]
        last_msg = messages[-1]
        middle_msgs = messages[1:-1]

        # 将中间消息整理成可供总结的纯文本
        middle_text_parts: List[str] = []
        for m in middle_msgs:
            role = m.role
            name = m.name or ""
            prefix = f"{role}({name})" if name else role
            middle_text_parts.append(f"{prefix}: {m.content}")
        middle_text = "\n".join(middle_text_parts)

        # 构造摘要任务提示
        summary_user_prompt = (
            "你是一个对话总结助手。请阅读以下对话历史，并用简洁的中文总结对话要点、"
            "已达成的结论和对后续回答有用的关键信息，尽量短且信息密集。\n\n"
            "对话历史：\n"
            f"{middle_text}\n\n"
            "请只输出总结内容，不要添加额外说明。"
        )

        summary_payload: Dict[str, Any] = {
            "model": self._config.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个高效的对话总结助手，负责将对话压缩为简洁的要点。",
                },
                {"role": "user", "content": summary_user_prompt},
            ],
            "temperature": 0.2,
        }

        summary_resp = await self._client.chat.completions.create(**summary_payload)
        summary_msg = summary_resp.choices[0].message
        summary_content = summary_msg.content or ""

        # 用一条总结消息替换全部中间历史
        compressed_messages: List[ChatMessage] = [
            first_msg,
            ChatMessage(
                role="agent",
                name=f"{self._agent_name}_history_summary",
                content=f"对话历史总结：{summary_content}",
            ),
            last_msg,
        ]
        return compressed_messages

    async def _ensure_ready(self, force_reload: bool = False) -> None:
        """检查配置是否ready,可配置强制重加载参数"""
        if self._client is None or self._config is None or force_reload:
            await self._refresh()

    async def run_no_tool_chat(
        self,
        query: str,  # 最新的问题
        *,  # 强制后续关键词传参
        chat_history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        force_reload: bool = False,
    ) -> str:
        """
        使用最新配置向模型发送聊天消息，并返回第一条回复内容。

        Args:
            query: 当前这次的 user_prompt，会被放在 chat_history 的最后。
            chat_history: 可选外部传入的历史消息列表（不包含 system）。
                - 若传入，则用「system_prompt + 该列表 + 当前 query」组成本次发送给 LLM 的历史，
                  并覆盖内部缓存的历史。
                - 若不传入，则在已有内部历史基础上，仅在末尾追加当前 query。
            temperature: 采样温度，可选。
            max_tokens: 最大输出 tokens,可选。
            extra_params: 透传给 OpenAI 接口的其他参数。
            force_reload: 是否在本次调用前强制刷新配置。
        """
        # 确保配置正确
        await self._ensure_ready(force_reload) 
        assert self._config is not None and self._client is not None

        # 处理 chat_history 与 query，生成本次要发送给 LLM 的 messages
        if chat_history is not None:
            await self._chat_history.replace_with_external(chat_history)
            await self._chat_history.add_user_msg(query)
        else:
            await self._chat_history.add_user_msg(query)

        # 深拷贝获取构造好的历史消息
        messages = await self._chat_history.get_messages()  

        # 发送给大模型前，必要时压缩历史，保持 system_prompt 和当前 query 不变
        messages = await self._compress_if_needed(messages)
        # 压缩后的结果作为新的内部历史缓存
        await self._chat_history.overwrite(messages)

        # 构造给openai的请求参数       
        payload: Dict[str, Any] = {
            "model": self._config.model_name,
            "messages": [msg.to_openai_payload() for msg in messages],
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if extra_params:
            payload.update(extra_params)

        """和大模型交互"""
        # 获取返回
        response = await self._client.chat.completions.create(**payload)
        # 获取第一条回复，并加入历史
        first_message = response.choices[0].message
        content = first_message.content or ""
        # OpenAI ChatCompletionMessage 的 role 一般为 "assistant"
        await self._chat_history.add_agent_msg(self._agent_name, content)
        return content
