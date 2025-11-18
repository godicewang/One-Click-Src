from fastapi import FastAPI

from .config import router as config_router


def register_routes(app: FastAPI) -> None:
    """将所有路由注册到app"""
    app.include_router(config_router)




