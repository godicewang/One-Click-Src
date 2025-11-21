from __future__ import annotations

import asyncio
import json
import shlex
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Sequence
from urllib.parse import urlparse

from ..base import BaseTool, ToolError, ToolResult


class NmapTool(BaseTool):
    """封装常用 nmap 扫描模式的工具类。"""

    name = "nmap"
    description = (
        "使用 nmap 执行常见扫描模式，支持主机发现、快速扫描、版本探测等。"
    )

    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "需要扫描的 IP 或域名，可带 http(s) 前缀。",
            },
            "mode": {
                "type": "string",
                "enum": [
                    "host_discovery",
                    "fast_scan",
                    "top_ports",
                    "service_version",
                    "os_detection",
                    "full_scan",
                ],
                "description": "扫描模式：主机发现/快速扫描/Top端口/服务版本/系统识别/全端口。",
            },
            "top_ports": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000,
                "default": 100,
                "description": "top_ports 模式下扫描的端口数量。",
            },
            "extra_args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "附加的 nmap 参数（谨慎使用）。",
            },
        },
        "required": ["target", "mode"],
        "additionalProperties": False,
    }

    MODE_FLAGS: Dict[str, Sequence[str]] = {
        "host_discovery": ("-sn",),
        "fast_scan": ("-T4", "-F", "-Pn"),
        "top_ports": ("-T4", "-Pn"),
        "service_version": ("-sV", "-T4", "-Pn"),
        "os_detection": ("-O", "-T4", "-Pn"),
        "full_scan": ("-sS", "-T4", "-Pn", "-p-",),
    }

    async def run(
        self,
        *,
        target: str,
        mode: str,
        top_ports: int = 100,
        extra_args: Sequence[str] | None = None,
    ) -> ToolResult:
        normalized_target = self._normalize_target(target)
        flags = list(self.MODE_FLAGS.get(mode, ()))
        if not flags:
            raise ToolError(f"未知的模式：{mode}")

        cmd = ["nmap", *flags]
        if mode == "top_ports":
            cmd.extend(["--top-ports", str(top_ports)])
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(normalized_target)

        stdout, stderr, returncode = await self._run_cmd(cmd)
        if returncode != 0:
            raise ToolError(
                f"nmap 执行失败，返回码 {returncode}，stderr: {stderr.strip()}"
            )

        summary = self._parse_scan_result(stdout, normalized_target)
        summary["mode"] = mode
        content = json.dumps(summary, ensure_ascii=False)
        return ToolResult(name=self.name, content=content, metadata=summary)

    @staticmethod
    def _normalize_target(target: str) -> str:
        cleaned = target.strip()
        if not cleaned:
            raise ToolError("target 不能为空")

        parsed = urlparse(cleaned)
        if parsed.scheme and parsed.netloc:
            return parsed.hostname or parsed.netloc
        if cleaned.startswith("//"):
            parsed = urlparse(f"http:{cleaned}")
            if parsed.hostname:
                return parsed.hostname
        return cleaned.strip("/")

    async def _run_cmd(self, cmd: Sequence[str]) -> tuple[str, str, int]:
        cmd = [*cmd, "-oX", "-"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise ToolError("系统未安装 nmap，请先安装后再使用该工具。") from exc

        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout = stdout_bytes.decode(errors="ignore")
        stderr = stderr_bytes.decode(errors="ignore")
        return stdout, stderr, proc.returncode

    def _parse_scan_result(self, xml_text: str, fallback_target: str) -> Dict[str, Any]:
        """把 nmap XML 输出整理为指定结构。"""
        ip = fallback_target
        alive = False
        alive_ports: List[int] = []

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return {"ip": ip, "alive": alive, "alive_port": alive_ports}

        host = root.find("host")
        if host is None:
            return {"ip": ip, "alive": alive, "alive_port": alive_ports}

        address = host.find('address[@addrtype="ipv4"]') or host.find(
            'address[@addrtype="ipv6"]'
        )
        if address is not None and address.get("addr"):
            ip = address.get("addr", ip)

        status = host.find("status")
        if status is not None:
            alive = status.get("state") == "up"

        ports = host.find("ports")
        if ports is not None:
            for port in ports.findall("port"):
                state_elem = port.find("state")
                if state_elem is None or state_elem.get("state") != "open":
                    continue
                portid = port.get("portid")
                try:
                    alive_ports.append(int(portid))
                except (TypeError, ValueError):
                    continue

        alive_ports.sort()
        return {"ip": ip, "alive": alive, "alive_port": alive_ports}


