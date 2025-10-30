import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const mazeApi = {
  // Генерация лабиринта
  generateMaze: async (width, height, algorithm) => {
    const response = await api.post('/api/maze/generate', {
      width,
      height,
      algorithm,
    });
    return response.data;
  },

  // Получить лабиринт
  getMaze: async (mazeId) => {
    const response = await api.get(`/api/maze/${mazeId}`);
    return response.data;
  },

  // Получить список лабиринтов
  getMazes: async (page = 1, size = 10) => {
    const response = await api.get('/api/maze/', {
      params: { page, size },
    });
    return response.data;
  },

  // Решить лабиринт
  solveMaze: async (mazeId, algorithm) => {
    const response = await api.post(`/api/maze/${mazeId}/solve`, {
      algorithm,
    });
    return response.data;
  },

  // Получить решения лабиринта
  getMazeSolutions: async (mazeId) => {
    const response = await api.get(`/api/maze/${mazeId}/solutions`);
    return response.data;
  },

  // Удалить лабиринт
  deleteMaze: async (mazeId) => {
    const response = await api.delete(`/api/maze/${mazeId}`);
    return response.data;
  },
};

export default mazeApi;