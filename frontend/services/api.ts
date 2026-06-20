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
export interface Manufacturer {
  id: number;
  name: string;
  country?: string;
  website?: string;
}
export interface Gearbox {
  id: number;
  gearbox_number: string;
  name?: string;
  gearbox_type?: string;          // или enum
  series?: string;
  stages?: number;
  input_power_kw?: number;
  output_torque_nm?: number;
  ratio?: number;
  input_speed_rpm?: number;
  output_speed_rpm?: number;
  service_factor?: number;
  efficiency?: number;
  weight_kg?: number;
  mounting_position?: string;
  output_shaft_diameter_mm?: number;
  output_shaft_length_mm?: number;
  output_flange_type?: string;
  hollow_shaft?: boolean;
  oil_volume_l?: number;
  radial_load_n?: number;
  price?: number;
  currency?: string;
  manufacturer?: { id: number; name: string };
  is_active?: boolean;
}
export interface Bearing {
  id: number;
  bearing_number: string;
  bore_diameter_mm?: number;
  outer_diameter_mm?: number;
  width_mm?: number;
  bearing_type?: {
    id?: number;
    name: string;
  };
  type_name?: string;          // если используется отдельно
  seal_type?: string;
  clearance?: string;
  dynamic_load_rating_kn?: number;
  static_load_rating_kn?: number;
  limiting_speed_rpm?: number;
  weight_kg?: number;
  price?: number;
  currency?: string;
  manufacturer?: { id: number; name: string };
  series_code?: string;
  manufacturer_name?: string;   // если бэкенд отдаёт строку
}
export interface BearingUnit {
  id: number;
  unit_number: string;
  shaft_diameter_mm?: number;
  housing_type?: string;
  housing_material?: string;
  a_mm?: number;
  e_mm?: number;
  i_mm?: number;
  g_mm?: number;
  l_mm?: number;
  s_mm?: number;
  b_mm?: number;
  weight_kg?: number;
  dynamic_load_kn?: number;
  static_load_kn?: number;
  manufacturer?: { id: number; name: string };
}

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
// ---------- Заглушки для остальных API, чтобы не падал импорт ----------
export const categoriesApi = {
  getAll: async () => [],
};

export const bearingsApi = {
  getAll: async (params?: any) => {
    // Если есть реальный эндпоинт, можно раскомментировать:
    // const response = await api.get('/api/v1/bearings', { params });
    // return response.data;
    return [];
  },
  getById: async (id: number) => {
    // const response = await api.get(`/api/v1/bearings/${id}`);
    // return response.data;
    return null;
  },
  getByShaft: async (shaftDiameter: number, tolerance: number = 0.1) => {
    // const response = await api.get(`/api/v1/bearings/by-shaft/${shaftDiameter}`, { params: { tolerance } });
    // return response.data;
    return [];
  },
  search: async (query: string) => {
    // const response = await api.get('/api/v1/bearings/search', { params: { q: query } });
    // return response.data;
    return [];
  },
};

export const bearingManufacturersApi = {
  getAll: async () => [],
};

export const bearingUnitsApi = {
  getAll: async (params?: any) => {
    return [];
  },
  getById: async (id: number) => {
    return null;
  },
  getByNumber: async (number: string) => {
    return null;
  },
};

export const gearboxesApi = {
  getAll: async (params?: any) => {
    return [];
  },
  getById: async (id: number) => {
    return null;
  },
  getByNumber: async (number: string) => {
    return null;
  },
};

// Перечисления (чтобы не сломать импорты)
export enum GearboxType {
  WORM = 'WORM',
  HELICAL = 'HELICAL',
}
export enum MountingPosition {
  M1 = 'M1',
}