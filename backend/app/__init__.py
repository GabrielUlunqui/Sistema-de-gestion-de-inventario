from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, ensure_columns, seed_if_empty
from .routers import items, stats


def create_app() -> FastAPI:
    app = FastAPI(title="API de Inventario", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)
    ensure_columns()
    seed_if_empty()

    app.include_router(items.router, prefix="/api")
    app.include_router(stats.router, prefix="/api")

    @app.get("/")
    def root():
        return {"status": "ok", "mensaje": "API de inventario funcionando"}

    return app
