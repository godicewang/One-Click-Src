from __future__ import annotations

import asyncio
import ipaddress
import json
import socket
from typing import Any, Dict, Iterable, List, Sequence
from urllib.parse import urlparse

from .base import BaseTool, ToolError, ToolResult


class NetworkScannerTool(BaseTool):
    """支持多模式的 IP 测活与端口扫描工具。"""

    name = "network_scanner"
    description = (
        "执行 IP 测活、常见端口扫描或全端口扫描，输出结构化结果。"
    )
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "需要检测的 IP 或域名。",
            },
            "mode": {
                "type": "string",
                "enum": ["ping", "common_ports", "all_ports"],
                "description": "扫描模式：ping 测活，common_ports 常见端口，all_ports 全端口。",
            },
            "timeout": {
                "type": "number",
                "minimum": 0.1,
                "default": 1.5,
                "description": "单端口连接或 ping 的超时时间（秒）。",
            },
            "max_concurrency": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1024,
                "default": 200,
                "description": "端口扫描时的最大并发，避免过载目标。",
            },
        },
        "required": ["target", "mode"],
        "additionalProperties": False,
    }

    COMMON_PORTS: Sequence[int] = (
        21,
        22,
        23,
        25,
        53,
        67,
        68,
        80,
        88,
        110,
        111,
        123,
        135,
        137,
        138,
        139,
        143,
        161,
        389,
        443,
        445,
        465,
        500,
        514,
        587,
        631,
        873,
        993,
        995,
        1080,
        1352,
        1433,
        1521,
        1723,
        2049,
        2375,
        2483,
        2598,
        3128,
        3268,
        3306,
        3389,
        3690,
        4369,
        5000,
        5040,
        5432,
        5672,
        5900,
        5984,
        6000,
        6379,
        6667,
        7001,
        7443,
        7777,
        8000,
        8080,
        8081,
        8443,
        8888,
        9000,
        9042,
        9200,
        10000,
        11211,
        27017,
    )

    async def run(
        self,
        *,
        target: str,
        mode: str,
        timeout: float = 1.5,  # 单端口连接或 ping 的超时时间（秒）
        max_concurrency: int = 200,  # 端口扫描时的最大并发，避免过载目标
    ) -> ToolResult:
        normalized_target = self._normalize_target(target)
        self._validate_target(normalized_target)
        timeout = max(timeout, 0.1)
        max_concurrency = max(1, min(max_concurrency, 1024))

        if mode == "ping":
            result = await self._ping(normalized_target, timeout=timeout)
        elif mode == "common_ports":
            result = await self._scan_ports(
                normalized_target,
                ports=self.COMMON_PORTS,
                timeout=timeout,
                max_concurrency=max_concurrency,
                mode_label="common_ports",
                report_progress=True,
            )
        elif mode == "all_ports":
            result = await self._scan_ports(
                normalized_target,
                ports=range(1, 65536),
                timeout=timeout,
                max_concurrency=max_concurrency,
                mode_label="all_ports",
                report_progress=True,
            )
        else:
            raise ToolError(f"不支持的扫描模式：{mode}")

        content = json.dumps(result, ensure_ascii=False)
        return ToolResult(name=self.name, content=content, metadata=result)

    @staticmethod
    def _normalize_target(target: str) -> str:
        """兼容 http/https/带路径参数的输入，提取纯主机名。"""
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

    @staticmethod
    def _validate_target(target: str) -> None:
        """校验目标字符串是否为合法 IP 或域名。"""
        try:
            ipaddress.ip_address(target)
            return
        except ValueError:
            if target and any(char.isalpha() for char in target):
                return
        raise ToolError("无效 target，请输入正确的 IP 或域名")

    async def _ping(self, target: str, *, timeout: float) -> Dict[str, Any]:
        """执行 ping 命令检测目标存活状态。"""
        cmd = ["ping", "-c", "1", target]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                return {
                    "target": target,
                    "mode": "ping",
                    "alive": False,
                    "message": "ping 超时",
                }
            alive = proc.returncode == 0
            return {
                "target": target,
                "mode": "ping",
                "alive": alive,
                "stdout": stdout.decode(errors="ignore"),
                "stderr": stderr.decode(errors="ignore"),
            }
        except FileNotFoundError as exc:  # pragma: no cover - ping 未安装
            raise ToolError("系统缺少 ping 命令，无法执行测活") from exc

    async def _scan_ports(
        self,
        target: str,
        *,
        ports: Iterable[int],
        timeout: float,
        max_concurrency: int,
        mode_label: str,
        report_progress: bool = False,
    ) -> Dict[str, Any]:
        """按照指定端口集合执行 TCP 连接探测。"""
        ports_seq = (
            list(int(port) for port in ports)
            if not isinstance(ports, Sequence)
            else [int(port) for port in ports]
        )
        total_ports = len(ports_seq)
        if total_ports == 0:
            return {
                "target": target,
                "mode": mode_label,
                "open_ports": [],
                "total_scanned": 0,
                "timeout": timeout,
                "progress": [],
            }

        semaphore = asyncio.Semaphore(max_concurrency)
        open_ports: List[int] = []
        tasks = []
        completed = 0
        progress_updates: List[Dict[str, Any]] = []
        # 兼顾超大端口范围与体验：每 5% 或 1000 个端口更新一次
        percent_based = max(1, total_ports // 20)
        report_step = min(percent_based, 1000)
        report_step = max(1, report_step)
        next_report_at = report_step

        async def probe(port: int) -> None:
            nonlocal completed, next_report_at
            async with semaphore:
                if await self._probe_port(target, port, timeout):
                    open_ports.append(port)
            completed += 1
            if (
                report_progress
                and total_ports >= 10
                and completed >= next_report_at
            ):
                percent = completed / total_ports * 100
                progress_updates.append(
                    {
                        "completed": completed,
                        "total": total_ports,
                        "percent": round(percent, 1),
                    }
                )
                print(
                    f"[network_scanner][{mode_label}] "
                    f"{completed}/{total_ports} ({percent:.1f}%)"
                )
                next_report_at += report_step

        for port in ports_seq:
            tasks.append(asyncio.create_task(probe(port)))

        await asyncio.gather(*tasks)
        return {
            "target": target,
            "mode": mode_label,
            "open_ports": sorted(open_ports),
            "total_scanned": total_ports,
            "timeout": timeout,
            "progress": progress_updates,
        }

    @staticmethod
    async def _probe_port(target: str, port: int, timeout: float) -> bool:
        """尝试建立 TCP 连接判断端口是否开放，支持 IPv4/IPv6 回退。"""
        loop = asyncio.get_running_loop()
        try:
            addr_infos = await loop.getaddrinfo(
                target,
                port,
                type=socket.SOCK_STREAM,
            )
        except socket.gaierror:
            return False

        for family, socktype, proto, _, sockaddr in addr_infos:
            sock = socket.socket(family, socktype, proto)
            sock.setblocking(False)
            try:
                await asyncio.wait_for(loop.sock_connect(sock, sockaddr), timeout)
                sock.close()
                return True
            except Exception:
                sock.close()
                continue
        return False


