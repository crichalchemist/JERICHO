"""
Jericho FastAPI application factory.

Phase 0: Serves same routes as src/api/server.js using JSON file storage.
Phase 1: Loads model registry + initialises OpenTelemetry tracing at startup.
Phase 2: JSON adapter replaced by Supabase repositories.
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jericho.config import get_settings
from jericho.constants import CORS_ALLOW_ORIGINS
from jericho.db.client import create_db_client
from jericho.llm.registry import load_registry
from jericho.observability.tracing import setup_tracing
from jericho.routers import accountability, ai, calendar, goals, health, identity, internal, native, pipeline, rhythms, state, tasks, team
from jericho.workers.scheduler import create_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown lifecycle."""
    settings = get_settings()

    # Phase 1: load model registry once; stored on app.state for routers to use
    app.state.registry = load_registry(settings.model_registry_path)

    # Phase 1: initialise tracing (console exporter when OTLP endpoint unset)
    app.state.tracer_provider = setup_tracing(
        service_name=settings.otel_service_name,
        otlp_endpoint=settings.otel_exporter_otlp_endpoint or None,
    )

    # Phase 2: initialise Supabase client when credentials are present
    if settings.supabase_url and settings.supabase_service_role_key:
        app.state.db_client = await create_db_client(settings)
    else:
        app.state.db_client = None  # JSON adapter mode (Phase 0/1)
    # Phase 4: start APScheduler nightly rescheduler
    scheduler = create_scheduler(app.state.db_client)
    scheduler.start()
    app.state.scheduler = scheduler
    app.state.settings = settings
    yield
    # Shutdown: stop scheduler, close DB connections
    scheduler.shutdown(wait=False)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Jericho API",
        version="0.1.0",
        description="Jericho 2.0 closed-loop behavioral execution platform.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(CORS_ALLOW_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(state.router)
    app.include_router(goals.router)
    app.include_router(identity.router)
    app.include_router(tasks.router)
    app.include_router(pipeline.router)
    app.include_router(calendar.router, prefix="/calendar")
    app.include_router(accountability.router, prefix="/accountability")
    app.include_router(rhythms.router, prefix="/rhythms")
    app.include_router(ai.router, prefix="/ai")
    app.include_router(team.router, prefix="/team")
    app.include_router(internal.router, prefix="/internal")
    app.include_router(native.router, prefix="/native")

    return app


app = create_app()
