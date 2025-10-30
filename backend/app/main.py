from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.api.routes import maze

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    pass


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API для генерации лабиринтов и поиска пути с использованием BFS, DFS и A*",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(maze.router)


@app.get("/")
async def root():
    return {
        "message": "Maze Generator & Pathfinding API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "algorithms": {
            "generation": settings.GENERATION_ALGORITHMS,
            "pathfinding": settings.PATHFINDING_ALGORITHMS
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)