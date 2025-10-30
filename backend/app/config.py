from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Maze Generator & Pathfinding"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = "sqlite:///./maze_app.db"
    
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    MAX_MAZE_SIZE: int = 100
    MIN_MAZE_SIZE: int = 5
    DEFAULT_MAZE_SIZE: int = 20
    
    GENERATION_ALGORITHMS: list = [
        "recursive_backtracking",
        "prims",
        "kruskals"
    ]
    
    PATHFINDING_ALGORITHMS: list = [
        "bfs",
        "dfs",
        "astar"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()