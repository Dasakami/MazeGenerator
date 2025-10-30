import React from 'react';
import { Play, Pause, RotateCcw, SkipForward, Grid } from 'lucide-react';

const Controls = ({
  generationAlgorithm,
  setGenerationAlgorithm,
  pathfindingAlgorithm,
  setPathfindingAlgorithm,
  mazeSize,
  setMazeSize,
  onGenerate,
  onSolve,
  isPlaying,
  onPlayPause,
  onReset,
  onStepForward,
  isGenerating,
  isSolving,
  hasSolution,
}) => {
  return (
    <div className="space-y-6 bg-white p-6 rounded-lg shadow-lg">
      {/* Генерация лабиринта */}
      <div>
        <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <Grid size={20} />
          Генерация лабиринта
        </h3>
        
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Размер: {mazeSize}x{mazeSize}
            </label>
            <input
              type="range"
              min="10"
              max="50"
              value={mazeSize}
              onChange={(e) => setMazeSize(parseInt(e.target.value))}
              className="w-full"
              disabled={isGenerating || isSolving}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Алгоритм генерации
            </label>
            <select
              value={generationAlgorithm}
              onChange={(e) => setGenerationAlgorithm(e.target.value)}
              className="w-full p-2 border rounded-md"
              disabled={isGenerating || isSolving}
            >
              <option value="recursive_backtracking">Recursive Backtracking</option>
              <option value="prims">Prim's Algorithm</option>
              <option value="kruskals">Kruskal's Algorithm</option>
            </select>
          </div>

          <button
            onClick={onGenerate}
            disabled={isGenerating || isSolving}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isGenerating ? 'Генерация...' : 'Сгенерировать лабиринт'}
          </button>
        </div>
      </div>

      {/* Поиск пути */}
      <div className="border-t pt-6">
        <h3 className="text-lg font-semibold mb-3">Поиск пути</h3>
        
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Алгоритм поиска
            </label>
            <select
              value={pathfindingAlgorithm}
              onChange={(e) => setPathfindingAlgorithm(e.target.value)}
              className="w-full p-2 border rounded-md"
              disabled={isSolving}
            >
              <option value="bfs">BFS (Breadth-First Search)</option>
              <option value="dfs">DFS (Depth-First Search)</option>
              <option value="astar">A* (A-Star)</option>
            </select>
          </div>

          <button
            onClick={onSolve}
            disabled={isSolving || isGenerating}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-md disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isSolving ? 'Поиск пути...' : 'Найти путь'}
          </button>
        </div>
      </div>

      {/* Визуализация */}
      {hasSolution && (
        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold mb-3">Визуализация</h3>
          
          <div className="flex gap-2">
            <button
              onClick={onPlayPause}
              className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-md flex items-center justify-center gap-2 transition-colors"
            >
              {isPlaying ? (
                <>
                  <Pause size={18} />
                  Пауза
                </>
              ) : (
                <>
                  <Play size={18} />
                  Воспроизвести
                </>
              )}
            </button>

            <button
              onClick={onStepForward}
              disabled={isPlaying}
              className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-md disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <SkipForward size={18} />
            </button>

            <button
              onClick={onReset}
              className="bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
            >
              <RotateCcw size={18} />
            </button>
          </div>
        </div>
      )}

      {/* Легенда */}
      <div className="border-t pt-6">
        <h3 className="text-sm font-semibold mb-2">Легенда</h3>
        <div className="space-y-1 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 border"></div>
            <span>Старт</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-500 border"></div>
            <span>Финиш</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-gray-800 border"></div>
            <span>Стена</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-400 border"></div>
            <span>Путь</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-200 border"></div>
            <span>Посещено</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-purple-300 border"></div>
            <span>Frontier</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-400 border"></div>
            <span>Текущая</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controls;