/**
 * API Service
 * 处理所有后端 API 请求
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 类型定义
export interface Ingredient {
  id?: number;
  name: string;
  quantity: string;
  category?: string;
  state?: string;
  image?: string;
}

export interface Recipe {
  name: string;
  description: string;
  difficulty: string;
  time: string;
  calories: string;
  ingredients: Array<{
    name: string;
    quantity: string;
    status: string;
  }>;
  steps: string[];
  tags: string[];
}

export interface RecipeFilters {
  cuisine?: string;
  taste?: string;
  scenario?: string;
  skill?: string;
}

// API 方法
export const recipeAPI = {
  generate: async (ingredients: Ingredient[], filters?: RecipeFilters) => {
    const response = await api.post('/recipes/generate', { ingredients, filters });
    return response.data;
  },
  getHistory: async (limit = 20) => {
    const response = await api.get(`/recipes/history?limit=${limit}`);
    return response.data;
  },
};

export const ingredientAPI = {
  getAll: async () => {
    const response = await api.get('/ingredients');
    return response.data;
  },
  add: async (ingredient: Ingredient) => {
    const response = await api.post('/ingredients', ingredient);
    return response.data;
  },
  update: async (id: number, data: Partial<Ingredient>) => {
    const response = await api.put(`/ingredients/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await api.delete(`/ingredients/${id}`);
    return response.data;
  },
};

export const favoriteAPI = {
  getAll: async () => {
    const response = await api.get('/favorites');
    return response.data;
  },
  add: async (recipe: Recipe, group = '默认分组') => {
    const response = await api.post('/favorites', { recipe, group });
    return response.data;
  },
  delete: async (id: number) => {
    const response = await api.delete(`/favorites/${id}`);
    return response.data;
  },
};

export const shoppingListAPI = {
  getAll: async () => {
    const response = await api.get('/shopping-list');
    return response.data;
  },
  generate: async (recipes: Recipe[]) => {
    const response = await api.post('/shopping-list/generate', { recipes });
    return response.data;
  },
  add: async (name: string, quantity: string) => {
    const response = await api.post('/shopping-list', { name, quantity });
    return response.data;
  },
  update: async (id: number, checked: boolean) => {
    const response = await api.put(`/shopping-list/${id}`, { checked });
    return response.data;
  },
  delete: async (id: number) => {
    const response = await api.delete(`/shopping-list/${id}`);
    return response.data;
  },
};

export default api;
