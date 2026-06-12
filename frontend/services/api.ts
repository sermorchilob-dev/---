// services/api.ts – минимальная версия для работы с simple_server
import axios from 'axios';

// Базовый URL оставляем пустым, чтобы запросы шли через Next.js rewrites
export const api = axios.create({
  baseURL: '',
  headers: { 'Content-Type': 'application/json' },
});

// ---------- Интерфейсы ----------
export interface Product {
  id: number;
  product_code: string;
  name: string;
  power_kw?: number;
  speed_rpm?: number;
  voltage?: string;
  mounting_type?: string;
  ip_rating?: string;
  price?: number;
  currency: string;
  manufacturer_name?: string;
  in_stock: boolean;
}

// Заглушки для остальных типов (чтобы не ломать импорты)
export interface Manufacturer { id: number; name: string; }
export interface Category { id: number; name: string; }
export interface Bearing { id: number; bearing_number: string; }
export interface BearingUnit { id: number; unit_number: string; }
export interface Gearbox { id: number; gearbox_number: string; }

// ---------- API для продуктов (реально работает) ----------
export const productsApi = {
  getAll: async (params?: any) => {
    // Теперь путь начинается с /api/v1, baseURL пустой – итоговый URL: /api/v1/products
    const response = await api.get<Product[]>('/api/v1/products', { params });
    return response.data;
  },
  getById: async (id: number) => {
    const response = await api.get<Product>(`/api/v1/products/${id}`);
    return response.data;
  },
  search: async (query: string) => {
    const response = await api.get<Product[]>('/api/v1/products', { params: { search: query } });
    return response.data;
  },
};

// ---------- API для заявок ----------
export const quoteRequestsApi = {
  create: async (data: any) => {
    const response = await api.post('/api/v1/quote-requests', data);
    return response.data;
  },
  getAll: async () => {
    const response = await api.get('/api/v1/quote-requests');
    return response.data;
  },
};

// ---------- Производители (реальный эндпоинт) ----------
export const manufacturersApi = {
  getAll: async () => {
    const response = await api.get<Manufacturer[]>('/api/v1/manufacturers');
    return response.data;
  },
};

// ---------- Заглушки для остальных API, чтобы не падал импорт ----------
export const categoriesApi = {
  getAll: async () => [],
};

export const bearingsApi = {
  getAll: async () => [],
  getById: async () => null,
  getByShaft: async () => [],
  search: async () => [],
};

export const bearingManufacturersApi = {
  getAll: async () => [],
};

export const bearingUnitsApi = {
  getAll: async () => [],
  getById: async () => null,
  getByNumber: async () => null,
};

export const gearboxesApi = {
  getAll: async () => [],
  getById: async () => null,
  getByNumber: async () => null,
};

// Перечисления (чтобы не сломать импорты)
export enum GearboxType {
  WORM = 'WORM',
  HELICAL = 'HELICAL',
}
export enum MountingPosition {
  M1 = 'M1',
}