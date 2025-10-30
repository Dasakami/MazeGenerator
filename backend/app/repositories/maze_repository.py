from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.models.maze import Maze, Solution
from app.schemas.maze import MazeResponse, SolutionResponse


class MazeRepository:
    """Репозиторий для работы с лабиринтами в БД"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_maze(
        self,
        width: int,
        height: int,
        grid: List[List[int]],
        start: tuple,
        end: tuple,
        algorithm: str
    ) -> Maze:
        """Создать новый лабиринт"""
        maze = Maze(
            width=width,
            height=height,
            grid=json.dumps(grid),
            start_x=start[0],
            start_y=start[1],
            end_x=end[0],
            end_y=end[1],
            algorithm=algorithm
        )
        self.db.add(maze)
        self.db.commit()
        self.db.refresh(maze)
        return maze
    
    def get_maze(self, maze_id: int) -> Optional[Maze]:
        """Получить лабиринт по ID"""
        return self.db.query(Maze).filter(Maze.id == maze_id).first()
    
    def get_mazes(self, skip: int = 0, limit: int = 10) -> tuple[List[Maze], int]:
        """Получить список лабиринтов с пагинацией"""
        total = self.db.query(Maze).count()
        mazes = (
            self.db.query(Maze)
            .order_by(Maze.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return mazes, total
    
    def delete_maze(self, maze_id: int) -> bool:
        """Удалить лабиринт"""
        maze = self.get_maze(maze_id)
        if maze:
            self.db.delete(maze)
            self.db.commit()
            return True
        return False
    
    def create_solution(
        self,
        maze_id: int,
        algorithm: str,
        path: List[tuple],
        steps: List[dict],
        nodes_explored: int,
        path_length: int,
        execution_time: float
    ) -> Solution:
        """Создать решение лабиринта"""
        solution = Solution(
            maze_id=maze_id,
            algorithm=algorithm,
            path=json.dumps(path),
            steps=json.dumps(steps),
            nodes_explored=nodes_explored,
            path_length=path_length,
            execution_time=execution_time
        )
        self.db.add(solution)
        self.db.commit()
        self.db.refresh(solution)
        return solution
    
    def get_solution(self, solution_id: int) -> Optional[Solution]:
        """Получить решение по ID"""
        return self.db.query(Solution).filter(Solution.id == solution_id).first()
    
    def get_solutions_for_maze(self, maze_id: int) -> List[Solution]:
        """Получить все решения для лабиринта"""
        return (
            self.db.query(Solution)
            .filter(Solution.maze_id == maze_id)
            .order_by(Solution.created_at.desc())
            .all()
        )
    
    @staticmethod
    def maze_to_response(maze: Maze) -> dict:
        """Преобразовать модель Maze в ответ"""
        return {
            "id": maze.id,
            "width": maze.width,
            "height": maze.height,
            "grid": json.loads(maze.grid),
            "start": (maze.start_x, maze.start_y),
            "end": (maze.end_x, maze.end_y),
            "algorithm": maze.algorithm,
            "created_at": maze.created_at
        }
    
    @staticmethod
    def solution_to_response(solution: Solution) -> dict:
        """Преобразовать модель Solution в ответ"""
        return {
            "id": solution.id,
            "maze_id": solution.maze_id,
            "algorithm": solution.algorithm,
            "path": json.loads(solution.path),
            "steps": json.loads(solution.steps),
            "stats": {
                "nodes_explored": solution.nodes_explored,
                "path_length": solution.path_length,
                "execution_time": solution.execution_time
            },
            "created_at": solution.created_at
        }