import logging

from fastapi import FastAPI

from lifeos.platform.observability.logging import configure_logging
from lifeos.platform.settings import get_settings


configure_logging()

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment,
    }