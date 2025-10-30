import React from 'react';

const MazeGrid = ({ maze, solution, currentStep, showPath }) => {
  if (!maze) return null;

  const { grid, start, end } = maze;
  const cellSize = Math.min(600 / maze.width, 600 / maze.height);

  // Создать set для быстрой проверки
  const pathSet = new Set(
    solution?.path?.map(([x, y]) => `${x},${y}`) || []
  );
  
  const visitedSet = new Set(
    currentStep?.visited?.map(([x, y]) => `${x},${y}`) || []
  );
  
  const frontierSet = new Set(
    currentStep?.frontier?.map(([x, y]) => `${x},${y}`) || []
  );

  const getCellColor = (x, y, cell) => {
    const key = `${x},${y}`;
    
    // Стартовая и конечная точки
    if (x === start[0] && y === start[1]) return 'bg-green-500';
    if (x === end[0] && y === end[1]) return 'bg-red-500';
    
    // Путь (если показываем финальный путь)
    if (showPath && pathSet.has(key)) return 'bg-blue-400';
    
    // Текущая клетка
    if (currentStep && x === currentStep.current[0] && y === currentStep.current[1]) {
      return 'bg-yellow-400 animate-pulse';
    }
    
    // Frontier (клетки на рассмотрении)
    if (frontierSet.has(key)) return 'bg-purple-300';
    
    // Посещенные клетки
    if (visitedSet.has(key)) return 'bg-blue-200';
    
    // Стена или путь
    return cell === 1 ? 'bg-gray-800' : 'bg-white';
  };

  return (
    <div className="flex justify-center items-center p-4">
      <div 
        className="border-2 border-gray-800 inline-block"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${maze.width}, ${cellSize}px)`,
          gap: '1px',
          backgroundColor: '#1f2937',
        }}
      >
        {grid.map((row, y) =>
          row.map((cell, x) => (
            <div
              key={`${x}-${y}`}
              className={`${getCellColor(x, y, cell)} transition-colors duration-200`}
              style={{
                width: `${cellSize}px`,
                height: `${cellSize}px`,
              }}
              title={`(${x}, ${y})`}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default MazeGrid;