import random
from typing import List, Tuple, Set


class MazeGenerator:
    """Сервис генерации лабиринтов"""
    
    WALL = 1
    PATH = 0
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[int]] = []
    
    def generate(self, algorithm: str = "recursive_backtracking") -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """
        Генерация лабиринта
        
        Returns:
            Tuple[grid, start, end]
        """
        if algorithm == "recursive_backtracking":
            return self._recursive_backtracking()
        elif algorithm == "prims":
            return self._prims_algorithm()
        elif algorithm == "kruskals":
            return self._kruskals_algorithm()
        else:
            raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    
    def _recursive_backtracking(self) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """
        Recursive Backtracking (DFS)
        Создает лабиринт с одним решением
        """
        # Инициализация сетки стенами
        self.grid = [[self.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Начальная позиция
        start_x, start_y = 0, 0
        self.grid[start_y][start_x] = self.PATH
        
        # Стек для backtracking
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y)}
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            
            # Найти непосещенных соседей
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Выбрать случайного соседа
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Убрать стену между текущей клеткой и соседом
                wall_x, wall_y = x + dx // 2, y + dy // 2
                self.grid[wall_y][wall_x] = self.PATH
                self.grid[ny][nx] = self.PATH
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Определить конечную точку
        end_x, end_y = self.width - 1, self.height - 1
        if self.grid[end_y][end_x] == self.WALL:
            # Найти ближайший путь к углу
            for dy in range(self.height - 1, -1, -1):
                for dx in range(self.width - 1, -1, -1):
                    if self.grid[dy][dx] == self.PATH:
                        end_x, end_y = dx, dy
                        break
                if self.grid[end_y][end_x] == self.PATH:
                    break
        
        return self.grid, (start_x, start_y), (end_x, end_y)
    
    def _prims_algorithm(self) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """
        Алгоритм Прима
        Создает более разветвленный лабиринт
        """
        self.grid = [[self.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        start_x, start_y = 0, 0
        self.grid[start_y][start_x] = self.PATH
        
        # Список границ (стен между путями и непосещенными клетками)
        walls = []
        self._add_walls(start_x, start_y, walls)
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while walls:
            # Выбрать случайную стену
            wall_x, wall_y = random.choice(walls)
            walls.remove((wall_x, wall_y))
            
            # Найти клетки по обе стороны стены
            cells = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                cx, cy = wall_x + dx, wall_y + dy
                if 0 <= cx < self.width and 0 <= cy < self.height:
                    cells.append((cx, cy))
            
            # Если одна клетка - путь, а другая - стена, открыть проход
            path_cells = [c for c in cells if self.grid[c[1]][c[0]] == self.PATH]
            wall_cells = [c for c in cells if self.grid[c[1]][c[0]] == self.WALL]
            
            if len(path_cells) == 1 and len(wall_cells) >= 1:
                self.grid[wall_y][wall_x] = self.PATH
                
                for wx, wy in wall_cells:
                    if self.grid[wy][wx] == self.WALL:
                        self.grid[wy][wx] = self.PATH
                        self._add_walls(wx, wy, walls)
                        break
        
        end_x, end_y = self.width - 1, self.height - 1
        if self.grid[end_y][end_x] == self.WALL:
            for dy in range(self.height - 1, -1, -1):
                for dx in range(self.width - 1, -1, -1):
                    if self.grid[dy][dx] == self.PATH:
                        end_x, end_y = dx, dy
                        break
                if self.grid[end_y][end_x] == self.PATH:
                    break
        
        return self.grid, (start_x, start_y), (end_x, end_y)
    
    def _add_walls(self, x: int, y: int, walls: List[Tuple[int, int]]) -> None:
        """Добавить стены вокруг клетки"""
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            wall_x, wall_y = x + dx // 2, y + dy // 2
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] == self.WALL and (wall_x, wall_y) not in walls:
                    walls.append((wall_x, wall_y))
    
    def _kruskals_algorithm(self) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
        """
        Алгоритм Краскала
        Использует union-find для создания лабиринта
        """
        self.grid = [[self.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Инициализация путей (каждая вторая клетка)
        cells = []
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                self.grid[y][x] = self.PATH
                cells.append((x, y))
        
        # Union-Find структура
        parent = {cell: cell for cell in cells}
        
        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1, cell2):
            root1, root2 = find(cell1), find(cell2)
            if root1 != root2:
                parent[root1] = root2
                return True
            return False
        
        # Список всех стен между клетками
        edges = []
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                if x + 2 < self.width:
                    edges.append(((x, y), (x + 2, y), (x + 1, y)))
                if y + 2 < self.height:
                    edges.append(((x, y), (x, y + 2), (x, y + 1)))
        
        random.shuffle(edges)
        
        # Объединять клетки, убирая стены
        for cell1, cell2, wall in edges:
            if union(cell1, cell2):
                wall_x, wall_y = wall
                self.grid[wall_y][wall_x] = self.PATH
        
        start_x, start_y = 0, 0
        end_x, end_y = self.width - 1, self.height - 1
        
        if self.grid[end_y][end_x] == self.WALL:
            for dy in range(self.height - 1, -1, -1):
                for dx in range(self.width - 1, -1, -1):
                    if self.grid[dy][dx] == self.PATH:
                        end_x, end_y = dx, dy
                        break
                if self.grid[end_y][end_x] == self.PATH:
                    break
        
        return self.grid, (start_x, start_y), (end_x, end_y)