from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.storage.redis_client import init_redis, close_redis
from app.api.routes import chat_routes, session_routes, admin_routes
from app.middleware.cors import add_cors_middleware
from app.middleware.error_handler import global_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_redis()
    yield
    # Shutdown
    await close_redis()

app = FastAPI(
    title=settings.APP_NAME,
    description="Gateway for protecting LLMs from adaptive attacks",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Middleware
add_cors_middleware(app)

# Error handlers
app.add_exception_handler(Exception, global_exception_handler)

# Routes
app.include_router(chat_routes.router, prefix="/api")
app.include_router(session_routes.router, prefix="/api")
app.include_router(admin_routes.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
