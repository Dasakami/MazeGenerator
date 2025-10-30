import React, { useState, useEffect, useCallback } from 'react';
import { mazeApi } from './api/mazeApi';
import MazeGrid from './components/MazeGrid';
import Controls from './components/Controls';
import Stats from './components/Stats';

function App() {
  const [maze, setMaze] = useState(null);
  const [solution, setSolution] = useState(null);

  const [generationAlgorithm, setGenerationAlgorithm] = useState('recursive_backtracking');
  const [pathfindingAlgorithm, setPathfindingAlgorithm] = useState('astar');
  const [mazeSize, setMazeSize] = useState(20);
  
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showPath, setShowPath] = useState(false);


  const [isGenerating, setIsGenerating] = useState(false);
  const [isSolving, setIsSolving] = useState(false);
  const [error, setError] = useState(null);


  const handleGenerate = useCallback(async () => {
    try {
      setIsGenerating(true);
      setError(null);
      setSolution(null);
      setCurrentStepIndex(0);
      setShowPath(false);

      const newMaze = await mazeApi.generateMaze(
        mazeSize,
        mazeSize,
        generationAlgorithm
      );

      setMaze(newMaze);
    } catch (err) {
      setError('Ошибка генерации лабиринта: ' + err.message);
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  }, [mazeSize, generationAlgorithm]);

 const handleSolve = async () => {
    if (!maze) return;

    try {
      setIsSolving(true);
      setError(null);
      setCurrentStepIndex(0);
      setShowPath(false);

      const newSolution = await mazeApi.solveMaze(maze.id, pathfindingAlgorithm);
      setSolution(newSolution);
    } catch (err) {
      setError('Ошибка поиска пути: ' + err.message);
      console.error(err);
    } finally {
      setIsSolving(false);
    }
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setCurrentStepIndex(0);
    setIsPlaying(false);
    setShowPath(false);
  };

  const handleStepForward = () => {
    if (solution && currentStepIndex < solution.steps.length - 1) {
      setCurrentStepIndex(currentStepIndex + 1);
    }
  };

  useEffect(() => {
    
    if (!isPlaying || !solution) return;

    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev >= solution.steps.length - 1) {
          setIsPlaying(false);
          setShowPath(true);
          return prev;
        }
        return prev + 1;
      });
    }, 100); 

    return () => clearInterval(interval);
  }, [isPlaying, solution]);

  useEffect(() => {
  handleGenerate();
}, [handleGenerate]); // ✅ добавили handleGenerate в зависимости


  const currentStep = solution?.steps[currentStepIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Генератор Лабиринтов & Поиск Пути
          </h1>
          <p className="text-gray-600">
            Визуализация алгоритмов BFS, DFS и A* в действии
          </p>
        </header>

        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <Controls
              generationAlgorithm={generationAlgorithm}
              setGenerationAlgorithm={setGenerationAlgorithm}
              pathfindingAlgorithm={pathfindingAlgorithm}
              setPathfindingAlgorithm={setPathfindingAlgorithm}
              mazeSize={mazeSize}
              setMazeSize={setMazeSize}
              onGenerate={handleGenerate}
              onSolve={handleSolve}
              isPlaying={isPlaying}
              onPlayPause={handlePlayPause}
              onReset={handleReset}
              onStepForward={handleStepForward}
              isGenerating={isGenerating}
              isSolving={isSolving}
              hasSolution={!!solution}
            />
          </div>

          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold mb-4 text-center">
                {isGenerating && 'Генерация лабиринта...'}
                {isSolving && 'Поиск пути...'}
                {!isGenerating && !isSolving && maze && `Лабиринт ${maze.width}x${maze.height}`}
              </h2>
              
              {maze ? (
                <MazeGrid
                  maze={maze}
                  solution={solution}
                  currentStep={currentStep}
                  showPath={showPath}
                />
              ) : (
                <div className="flex items-center justify-center h-96">
                  <div className="text-gray-400">Загрузка лабиринта...</div>
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-1">
            {solution ? (
              <Stats solution={solution} currentStepIndex={currentStepIndex} />
            ) : (
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <h3 className="text-lg font-semibold mb-4">Статистика</h3>
                <p className="text-gray-500 text-center py-8">
                  Решите лабиринт, чтобы увидеть статистику
                </p>
              </div>
            )}
          </div>
        </div>

        <footer className="mt-8 text-center text-gray-600 text-sm">
          <p>
            Курсовая работа: Генератор лабиринтов и поиск пути
          </p>
          <p className="mt-2">
            Технологии: FastAPI, React, SQLite, Docker
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;