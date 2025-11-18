import argparse

import uvicorn


def main() -> None:
    """启动 FastAPI 应用，可通过 --reload 参数启用热加载。"""
    parser = argparse.ArgumentParser(description="Run AgentSrc backend API server")
    parser.add_argument("--host", default="0.0.0.0", help="绑定主机地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="开启代码热加载（开发模式使用）",
    )
    args = parser.parse_args()

    uvicorn.run(
        "api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()


