from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.maze import (
    MazeGenerateRequest,
    MazeSolveRequest,
    MazeResponse,
    SolutionResponse,
    MazeListResponse
)
from app.services.maze_generator import MazeGenerator
from app.services.pathfinder import PathFinder
from app.repositories.maze_repository import MazeRepository

router = APIRouter(prefix="/api/maze", tags=["maze"])


@router.post("/generate", response_model=MazeResponse)
async def generate_maze(
    request: MazeGenerateRequest,
    db: Session = Depends(get_db)
):
    try:
        generator = MazeGenerator(request.width, request.height)
        grid, start, end = generator.generate(request.algorithm)
        
        repo = MazeRepository(db)
        maze = repo.create_maze(
            width=request.width,
            height=request.height,
            grid=grid,
            start=start,
            end=end,
            algorithm=request.algorithm
        )
        
        return repo.maze_to_response(maze)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")


@router.get("/{maze_id}", response_model=MazeResponse)
async def get_maze(
    maze_id: int,
    db: Session = Depends(get_db)
):
    repo = MazeRepository(db)
    maze = repo.get_maze(maze_id)
    
    if not maze:
        raise HTTPException(status_code=404, detail="Лабиринт не найден")
    
    return repo.maze_to_response(maze)


@router.get("/", response_model=MazeListResponse)
async def get_mazes(
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    db: Session = Depends(get_db)
):
    repo = MazeRepository(db)
    skip = (page - 1) * size
    mazes, total = repo.get_mazes(skip=skip, limit=size)
    
    items = [repo.maze_to_response(maze) for maze in mazes]
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }


@router.post("/{maze_id}/solve", response_model=SolutionResponse)
async def solve_maze(
    maze_id: int,
    request: MazeSolveRequest,
    db: Session = Depends(get_db)
):
    repo = MazeRepository(db)
    maze = repo.get_maze(maze_id)
    
    if not maze:
        raise HTTPException(status_code=404, detail="Лабиринт не найден")
    
    try:
        import json
        grid = json.loads(maze.grid)
        start = (maze.start_x, maze.start_y)
        end = (maze.end_x, maze.end_y)
        
        pathfinder = PathFinder(grid, start, end)
        result = pathfinder.find_path(request.algorithm)
        
        solution = repo.create_solution(
            maze_id=maze_id,
            algorithm=request.algorithm,
            path=result["path"],
            steps=result["steps"],
            nodes_explored=result["stats"]["nodes_explored"],
            path_length=result["stats"]["path_length"],
            execution_time=result["stats"]["execution_time"]
        )
        
        return repo.solution_to_response(solution)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска пути: {str(e)}")


@router.get("/{maze_id}/solutions", response_model=List[SolutionResponse])
async def get_maze_solutions(
    maze_id: int,
    db: Session = Depends(get_db)
):
    repo = MazeRepository(db)
    maze = repo.get_maze(maze_id)
    
    if not maze:
        raise HTTPException(status_code=404, detail="Лабиринт не найден")
    
    solutions = repo.get_solutions_for_maze(maze_id)
    return [repo.solution_to_response(sol) for sol in solutions]


@router.delete("/{maze_id}")
async def delete_maze(
    maze_id: int,
    db: Session = Depends(get_db)
):
    repo = MazeRepository(db)
    success = repo.delete_maze(maze_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Лабиринт не найден")
    
    return {"message": "Лабиринт успешно удален"}