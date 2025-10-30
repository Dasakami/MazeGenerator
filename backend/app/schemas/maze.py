from pydantic import BaseModel, Field, field_validator
from typing import List, Tuple, Optional
from datetime import datetime


class MazeGenerateRequest(BaseModel):
    """Запрос на генерацию лабиринта"""
    width: int = Field(ge=5, le=100, description="Ширина лабиринта")
    height: int = Field(ge=5, le=100, description="Высота лабиринта")
    algorithm: str = Field(default="recursive_backtracking", description="Алгоритм генерации")
    
    @field_validator('algorithm')
    @classmethod
    def validate_algorithm(cls, v):
        valid = ["recursive_backtracking", "prims", "kruskals"]
        if v not in valid:
            raise ValueError(f"Алгоритм должен быть одним из: {', '.join(valid)}")
        return v


class MazeSolveRequest(BaseModel):
    """Запрос на решение лабиринта"""
    algorithm: str = Field(default="astar", description="Алгоритм поиска")
    
    @field_validator('algorithm')
    @classmethod
    def validate_algorithm(cls, v):
        valid = ["bfs", "dfs", "astar"]
        if v not in valid:
            raise ValueError(f"Алгоритм должен быть одним из: {', '.join(valid)}")
        return v


class MazeResponse(BaseModel):
    """Ответ с данными лабиринта"""
    id: int
    width: int
    height: int
    grid: List[List[int]]
    start: Tuple[int, int]
    end: Tuple[int, int]
    algorithm: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class PathfindingStep(BaseModel):
    """Шаг алгоритма поиска"""
    current: Tuple[int, int]
    visited: List[Tuple[int, int]]
    frontier: List[Tuple[int, int]]


class SolutionStats(BaseModel):
    """Статистика решения"""
    nodes_explored: int
    path_length: int
    execution_time: float


class SolutionResponse(BaseModel):
    """Ответ с решением лабиринта"""
    id: int
    maze_id: int
    algorithm: str
    path: List[Tuple[int, int]]
    steps: List[PathfindingStep]
    stats: SolutionStats
    created_at: datetime
    
    class Config:
        from_attributes = True


class MazeListResponse(BaseModel):
    """Список лабиринтов"""
    items: List[MazeResponse]
    total: int
    page: int
    size: int