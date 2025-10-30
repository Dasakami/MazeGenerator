import React from 'react';
import { Clock, RouterIcon, TrendingUp, Zap } from 'lucide-react';

const Stats = ({ solution, currentStepIndex }) => {
  if (!solution) return null;

  const { stats, algorithm } = solution;
  const progress = solution.steps.length > 0 
    ? Math.round((currentStepIndex / solution.steps.length) * 100)
    : 0;

  const algorithmNames = {
    bfs: 'BFS (Breadth-First Search)',
    dfs: 'DFS (Depth-First Search)',
    astar: 'A* Algorithm',
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold mb-4">Статистика</h3>
      
      <div className="space-y-4">
        <div>
          <div className="text-sm text-gray-600 mb-1">Алгоритм</div>
          <div className="text-lg font-semibold text-blue-600">
            {algorithmNames[algorithm] || algorithm.toUpperCase()}
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Прогресс визуализации</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Шаг {currentStepIndex} из {solution.steps.length}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-3 rounded-lg">
            <div className="flex items-center gap-2 text-blue-600 mb-1">
              <TrendingUp size={16} />
              <span className="text-xs font-medium">Узлов изучено</span>
            </div>
            <div className="text-2xl font-bold text-blue-700">
              {stats.nodes_explored}
            </div>
          </div>

          <div className="bg-green-50 p-3 rounded-lg">
            <div className="flex items-center gap-2 text-green-600 mb-1">
              <RouterIcon size={16} />
              <span className="text-xs font-medium">Длина пути</span>
            </div>
            <div className="text-2xl font-bold text-green-700">
              {stats.path_length}
            </div>
          </div>

          <div className="bg-purple-50 p-3 rounded-lg">
            <div className="flex items-center gap-2 text-purple-600 mb-1">
              <Clock size={16} />
              <span className="text-xs font-medium">Время (сек)</span>
            </div>
            <div className="text-2xl font-bold text-purple-700">
              {stats.execution_time.toFixed(4)}
            </div>
          </div>

          <div className="bg-orange-50 p-3 rounded-lg">
            <div className="flex items-center gap-2 text-orange-600 mb-1">
              <Zap size={16} />
              <span className="text-xs font-medium">Эффективность</span>
            </div>
            <div className="text-2xl font-bold text-orange-700">
              {stats.nodes_explored > 0 
                ? Math.round((stats.path_length / stats.nodes_explored) * 100)
                : 0}%
            </div>
          </div>
        </div>
        <div className="bg-gray-50 p-3 rounded-lg text-sm">
          <div className="font-medium mb-1">О алгоритме:</div>
          <div className="text-gray-600">
            {algorithm === 'bfs' && 'BFS гарантирует кратчайший путь, исследуя все узлы на одинаковом расстоянии.'}
            {algorithm === 'dfs' && 'DFS исследует путь до конца перед возвратом, может быть быстрее но не оптимален.'}
            {algorithm === 'astar' && 'A* использует эвристику для эффективного поиска оптимального пути.'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Stats;