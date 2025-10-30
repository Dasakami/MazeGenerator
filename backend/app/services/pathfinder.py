import time
from typing import List, Tuple, Dict, Set, Optional
from collections import deque
import heapq


class PathFinder:
    """Сервис поиска пути в лабиринте"""
    
    def __init__(self, grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
        self.start = start
        self.end = end
        self.PATH = 0
        self.WALL = 1
    
    def find_path(self, algorithm: str) -> Dict:
        """
        Найти путь в лабиринте
        
        Returns:
            Dict с path, steps и stats
        """
        start_time = time.time()
        
        if algorithm == "bfs":
            result = self._bfs()
        elif algorithm == "dfs":
            result = self._dfs()
        elif algorithm == "astar":
            result = self._astar()
        else:
            raise ValueError(f"Неизвестный алгоритм: {algorithm}")
        
        execution_time = time.time() - start_time
        
        return {
            "path": result["path"],
            "steps": result["steps"],
            "stats": {
                "nodes_explored": result["nodes_explored"],
                "path_length": len(result["path"]),
                "execution_time": execution_time
            }
        }
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Получить соседей клетки"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == self.PATH:
                    neighbors.append((nx, ny))
        return neighbors
    
    def _reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Восстановить путь из came_from"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def _bfs(self) -> Dict:
        """
        Breadth-First Search (поиск в ширину)
        Гарантирует кратчайший путь
        """
        queue = deque([self.start])
        visited = {self.start}
        came_from = {}
        steps = []
        
        while queue:
            current = queue.popleft()
            
            # Записать шаг
            steps.append({
                "current": current,
                "visited": list(visited),
                "frontier": list(queue)
            })
            
            if current == self.end:
                path = self._reconstruct_path(came_from, current)
                return {
                    "path": path,
                    "steps": steps,
                    "nodes_explored": len(visited)
                }
            
            for neighbor in self._get_neighbors(*current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        # Путь не найден
        return {
            "path": [],
            "steps": steps,
            "nodes_explored": len(visited)
        }
    
    def _dfs(self) -> Dict:
        """
        Depth-First Search (поиск в глубину)
        Быстрый, но не гарантирует кратчайший путь
        """
        stack = [self.start]
        visited = {self.start}
        came_from = {}
        steps = []
        
        while stack:
            current = stack.pop()
            
            # Записать шаг
            steps.append({
                "current": current,
                "visited": list(visited),
                "frontier": list(stack)
            })
            
            if current == self.end:
                path = self._reconstruct_path(came_from, current)
                return {
                    "path": path,
                    "steps": steps,
                    "nodes_explored": len(visited)
                }
            
            for neighbor in self._get_neighbors(*current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)
        
        return {
            "path": [],
            "steps": steps,
            "nodes_explored": len(visited)
        }
    
    def _astar(self) -> Dict:
        """
        A* алгоритм с Manhattan distance эвристикой
        Оптимальный и эффективный
        """
        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
            """Manhattan distance"""
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        # Приоритетная очередь: (f_score, counter, node)
        counter = 0
        open_set = [(0, counter, self.start)]
        came_from = {}
        
        # g_score: стоимость пути от start до узла
        g_score = {self.start: 0}
        
        # f_score: g_score + heuristic
        f_score = {self.start: heuristic(self.start, self.end)}
        
        visited = set()
        steps = []
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Записать шаг
            frontier = [node for _, _, node in open_set]
            steps.append({
                "current": current,
                "visited": list(visited),
                "frontier": frontier
            })
            
            if current == self.end:
                path = self._reconstruct_path(came_from, current)
                return {
                    "path": path,
                    "steps": steps,
                    "nodes_explored": len(visited)
                }
            
            for neighbor in self._get_neighbors(*current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, self.end)
                    
                    if neighbor not in visited:
                        counter += 1
                        heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
        
        return {
            "path": [],
            "steps": steps,
            "nodes_explored": len(visited)
        }