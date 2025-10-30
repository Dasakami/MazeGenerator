from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Создание тестовой БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestMazeGeneration:
    """Тесты генерации лабиринтов"""
    
    def test_generate_maze_recursive_backtracking(self):
        """Тест генерации алгоритмом Recursive Backtracking"""
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 20,
                "height": 20,
                "algorithm": "recursive_backtracking"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["width"] == 20
        assert data["height"] == 20
        assert data["algorithm"] == "recursive_backtracking"
        assert len(data["grid"]) == 20
        assert len(data["grid"][0]) == 20
        assert "start" in data
        assert "end" in data
        assert "id" in data
    
    def test_generate_maze_prims(self):
        """Тест генерации алгоритмом Prim's"""
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 15,
                "height": 15,
                "algorithm": "prims"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "prims"
    
    def test_generate_maze_kruskals(self):
        """Тест генерации алгоритмом Kruskal's"""
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 25,
                "height": 25,
                "algorithm": "kruskals"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "kruskals"
    
    def test_generate_maze_invalid_size(self):
        """Тест генерации с неверным размером"""
        # Слишком маленький
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 3,
                "height": 3,
                "algorithm": "recursive_backtracking"
            }
        )
        assert response.status_code == 422
        
        # Слишком большой
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 150,
                "height": 150,
                "algorithm": "recursive_backtracking"
            }
        )
        assert response.status_code == 422
    
    def test_generate_maze_invalid_algorithm(self):
        """Тест генерации с неверным алгоритмом"""
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 20,
                "height": 20,
                "algorithm": "invalid_algorithm"
            }
        )
        
        assert response.status_code == 422


class TestMazeSolving:
    """Тесты решения лабиринтов"""
    
    def setup_method(self):
        """Создать тестовый лабиринт перед каждым тестом"""
        response = client.post(
            "/api/maze/generate",
            json={
                "width": 15,
                "height": 15,
                "algorithm": "recursive_backtracking"
            }
        )
        self.maze_id = response.json()["id"]
    
    def test_solve_maze_bfs(self):
        """Тест решения алгоритмом BFS"""
        response = client.post(
            f"/api/maze/{self.maze_id}/solve",
            json={"algorithm": "bfs"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["algorithm"] == "bfs"
        assert "path" in data
        assert "steps" in data
        assert "stats" in data
        assert data["stats"]["nodes_explored"] > 0
        assert data["stats"]["path_length"] > 0
        assert data["stats"]["execution_time"] > 0
    
    def test_solve_maze_dfs(self):
        """Тест решения алгоритмом DFS"""
        response = client.post(
            f"/api/maze/{self.maze_id}/solve",
            json={"algorithm": "dfs"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "dfs"
    
    def test_solve_maze_astar(self):
        """Тест решения алгоритмом A*"""
        response = client.post(
            f"/api/maze/{self.maze_id}/solve",
            json={"algorithm": "astar"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "astar"
    
    def test_solve_nonexistent_maze(self):
        """Тест решения несуществующего лабиринта"""
        response = client.post(
            "/api/maze/99999/solve",
            json={"algorithm": "bfs"}
        )
        
        assert response.status_code == 404
    
    def test_solve_maze_invalid_algorithm(self):
        """Тест решения с неверным алгоритмом"""
        response = client.post(
            f"/api/maze/{self.maze_id}/solve",
            json={"algorithm": "invalid"}
        )
        
        assert response.status_code == 422
    
    def test_compare_algorithms(self):
        """Тест сравнения всех алгоритмов на одном лабиринте"""
        algorithms = ["bfs", "dfs", "astar"]
        results = {}
        
        for algo in algorithms:
            response = client.post(
                f"/api/maze/{self.maze_id}/solve",
                json={"algorithm": algo}
            )
            assert response.status_code == 200
            results[algo] = response.json()["stats"]
        
        # BFS и A* должны найти путь одинаковой длины (оптимальный)
        assert results["bfs"]["path_length"] <= results["dfs"]["path_length"]
        
        # A* должен исследовать меньше узлов чем BFS
        assert results["astar"]["nodes_explored"] <= results["bfs"]["nodes_explored"]


class TestMazeCRUD:
    """Тесты CRUD операций"""
    
    def test_get_maze(self):
        """Тест получения лабиринта"""
        # Создать лабиринт
        create_response = client.post(
            "/api/maze/generate",
            json={"width": 10, "height": 10, "algorithm": "prims"}
        )
        maze_id = create_response.json()["id"]
        
        # Получить лабиринт
        get_response = client.get(f"/api/maze/{maze_id}")
        
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == maze_id
        assert data["width"] == 10
        assert data["height"] == 10
    
    def test_get_nonexistent_maze(self):
        """Тест получения несуществующего лабиринта"""
        response = client.get("/api/maze/99999")
        assert response.status_code == 404
    
    def test_get_mazes_list(self):
        """Тест получения списка лабиринтов"""
        # Создать несколько лабиринтов
        for i in range(5):
            client.post(
                "/api/maze/generate",
                json={"width": 10, "height": 10, "algorithm": "prims"}
            )
        
        # Получить список
        response = client.get("/api/maze/?page=1&size=10")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["total"] >= 5
        assert len(data["items"]) >= 5
    
    def test_delete_maze(self):
        """Тест удаления лабиринта"""
        # Создать лабиринт
        create_response = client.post(
            "/api/maze/generate",
            json={"width": 10, "height": 10, "algorithm": "prims"}
        )
        maze_id = create_response.json()["id"]
        
        # Удалить лабиринт
        delete_response = client.delete(f"/api/maze/{maze_id}")
        assert delete_response.status_code == 200
        
        # Проверить, что удалён
        get_response = client.get(f"/api/maze/{maze_id}")
        assert get_response.status_code == 404
    
    def test_get_maze_solutions(self):
        """Тест получения решений лабиринта"""
        # Создать лабиринт
        create_response = client.post(
            "/api/maze/generate",
            json={"width": 15, "height": 15, "algorithm": "recursive_backtracking"}
        )
        maze_id = create_response.json()["id"]
        
        # Решить разными алгоритмами
        algorithms = ["bfs", "dfs", "astar"]
        for algo in algorithms:
            client.post(
                f"/api/maze/{maze_id}/solve",
                json={"algorithm": algo}
            )
        
        # Получить все решения
        response = client.get(f"/api/maze/{maze_id}/solutions")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Проверить, что есть все алгоритмы
        solution_algorithms = [s["algorithm"] for s in data]
        for algo in algorithms:
            assert algo in solution_algorithms


class TestAPIGeneral:
    """Общие тесты API"""
    
    def test_root_endpoint(self):
        """Тест корневого эндпоинта"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "algorithms" in data
        assert "generation" in data["algorithms"]
        assert "pathfinding" in data["algorithms"]
    
    def test_health_check(self):
        """Тест health check"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_docs_available(self):
        """Тест доступности документации"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200


# Запуск тестов с pytest
# pytest tests/test_maze.py -v
# pytest tests/test_maze.py -v --cov=app