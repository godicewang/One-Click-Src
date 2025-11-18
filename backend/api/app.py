from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import register_routes


def create_app() -> FastAPI:
    """Factory for FastAPI app so后续可以灵活扩展。"""
    app = FastAPI(title="AgentSrc Backend")
    register_routes(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


