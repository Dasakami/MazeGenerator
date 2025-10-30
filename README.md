# Генератор Лабиринтов и Поиск Пути

Профессиональное веб-приложение для генерации лабиринтов и визуализации алгоритмов поиска пути (BFS, DFS, A*).

## Технологический стек

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **SQLite** - база данных
- **Pydantic** - валидация данных
- **uvicorn** - ASGI сервер

### Frontend
- **React 18** - UI библиотека
- **TypeScript** - типизированный JavaScript
- **Tailwind CSS** - стилизация
- **Lucide React** - иконки

### Архитектура Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Точка входа FastAPI
│   ├── config.py               # Конфигурация
│   ├── database.py             # Настройка БД
│   ├── models/
│   │   ├── __init__.py
│   │   └── maze.py            # SQLAlchemy модели
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── maze.py            # Pydantic схемы
│   ├── services/
│   │   ├── __init__.py
│   │   ├── maze_generator.py # Генерация лабиринтов
│   │   └── pathfinder.py      # Алгоритмы поиска
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── maze_repository.py # Работа с БД
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           └── maze.py        # API эндпоинты
├── tests/                      # Тесты
├── requirements.txt
└── Dockerfile
```

## Быстрый старт

### Запуск через Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker-compose up --build

# Приложение доступно:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Локальный запуск

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Генерация лабиринта
```http
POST /api/maze/generate
Content-Type: application/json

{
  "width": 20,
  "height": 20,
  "algorithm": "recursive_backtracking"
}

Response: {
  "id": 1,
  "width": 20,
  "height": 20,
  "grid": [[0, 1, 0, ...], ...],
  "start": [0, 0],
  "end": [19, 19]
}
```

### Поиск пути
```http
POST /api/maze/{maze_id}/solve
Content-Type: application/json

{
  "algorithm": "astar"
}

Response: {
  "path": [[0, 0], [0, 1], ...],
  "steps": [
    {
      "current": [0, 0],
      "visited": [[0, 0]],
      "frontier": [[0, 1], [1, 0]]
    },
    ...
  ],
  "stats": {
    "nodes_explored": 150,
    "path_length": 38,
    "execution_time": 0.023
  }
}
```

### Получение лабиринта
```http
GET /api/maze/{maze_id}
```

### История лабиринтов
```http
GET /api/maze/history?limit=10&offset=0
```

## Алгоритмы

### Генерация лабиринтов
- **Recursive Backtracking** - классический DFS подход
- **Prim's Algorithm** - минимальное остовное дерево
- **Kruskal's Algorithm** - объединение множеств

### Поиск пути
- **BFS (Breadth-First Search)** - поиск в ширину, гарантирует кратчайший путь
- **DFS (Depth-First Search)** - поиск в глубину, быстрый но не оптимальный
- **A*** - эвристический поиск, оптимальный и быстрый

## Структура базы данных

```sql
CREATE TABLE mazes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    grid TEXT NOT NULL,  -- JSON
    start_x INTEGER NOT NULL,
    start_y INTEGER NOT NULL,
    end_x INTEGER NOT NULL,
    end_y INTEGER NOT NULL,
    algorithm TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE solutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maze_id INTEGER NOT NULL,
    algorithm TEXT NOT NULL,
    path TEXT NOT NULL,  -- JSON
    steps TEXT NOT NULL,  -- JSON
    nodes_explored INTEGER,
    path_length INTEGER,
    execution_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maze_id) REFERENCES mazes(id)
);
```

## Особенности реализации

### Backend
- **Слойная архитектура**: разделение на API, сервисы и репозитории
- **Dependency Injection**: использование FastAPI зависимостей
- **Async/Await**: асинхронные операции с БД
- **Type hints**: полная типизация кода
- **Error handling**: централизованная обработка ошибок
- **CORS**: настроенный для фронтенда

### Frontend
- **Component-based**: модульная структура компонентов
- **State management**: React hooks (useState, useEffect)
- **Responsive design**: адаптивный дизайн через Tailwind
- **Real-time visualization**: пошаговая анимация алгоритмов
- **Performance**: оптимизация рендеринга больших лабиринтов

## Производительность

- Генерация лабиринта 50x50: ~50ms
- A* поиск на лабиринте 50x50: ~20-100ms
- BFS поиск на лабиринте 50x50: ~30-150ms
- DFS поиск на лабиринте 50x50: ~10-80ms

## Требования

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (опционально)

## Разработка

### Тестирование Backend
```bash
cd backend
pytest
```

### Линтинг
```bash
# Backend
cd backend
black app/
flake8 app/

# Frontend
cd frontend
npm run lint
```

## Для защиты курсовой

Проект демонстрирует:
1. ✅ Профессиональную архитектуру backend (слои, DI, async)
2. ✅ REST API с документацией (Swagger UI)
3. ✅ Работу с БД через ORM
4. ✅ Реализацию классических алгоритмов (BFS, DFS, A*)
5. ✅ Современный frontend на React
6. ✅ Контейнеризацию через Docker
7. ✅ Визуализацию алгоритмов в реальном времени

## Скриншоты

### Главный экран
![Maze Generation](docs/screenshots/maze-generation.png)

### Визуализация BFS
![BFS Visualization](docs/screenshots/bfs-visualization.png)

### Сравнение алгоритмов
![Algorithm Comparison](docs/screenshots/comparison.png)

## Тестирование

```bash
# Запуск тестов
cd backend
pytest

# С покрытием кода
pytest --cov=app --cov-report=html

# Конкретный тест
pytest tests/test_maze.py::TestMazeGeneration::test_generate_maze_bfs -v
```

## Документация кода

### Backend
Документация генерируется автоматически через Swagger UI:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

### Frontend
React компоненты документированы в JSDoc формате

## Лицензия

MIT License

Copyright (c) 2024

## Автор

Курсовая работа по теме "Генератор лабиринтов и поиск пути"

Разработано с ❤️ для демонстрации алгоритмов и профессиональной архитектуры