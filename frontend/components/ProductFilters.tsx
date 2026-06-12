'use client';

import { useState, useEffect } from 'react';

interface Filters {
  power_min?: number;
  power_max?: number;
  speed_min?: number;
  speed_max?: number;
  price_min?: number;
  price_max?: number;
  manufacturer?: string;
  search?: string;
}

interface ProductFiltersProps {
  onFilterChange: (filters: Filters) => void;
  manufacturers: { id: number; name: string }[];
}

export default function ProductFilters({ onFilterChange, manufacturers }: ProductFiltersProps) {
  const [filters, setFilters] = useState<Filters>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const newFilters = { ...filters, [name]: value || undefined };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-gray-100 p-4 rounded-lg mb-6">
      <h3 className="font-semibold mb-2">Фильтры</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input type="text" name="search" placeholder="Поиск по названию/артикулу" onChange={handleChange} className="p-2 border rounded" />
        <select name="manufacturer" onChange={handleChange} className="p-2 border rounded">
          <option value="">Все производители</option>
          {manufacturers.map(m => <option key={m.id} value={m.name}>{m.name}</option>)}
        </select>
        <div className="flex gap-2">
          <input type="number" name="power_min" placeholder="Мощность от (кВт)" onChange={handleChange} className="p-2 border rounded w-1/2" />
          <input type="number" name="power_max" placeholder="Мощность до (кВт)" onChange={handleChange} className="p-2 border rounded w-1/2" />
        </div>
        <div className="flex gap-2">
          <input type="number" name="speed_min" placeholder="Обороты от" onChange={handleChange} className="p-2 border rounded w-1/2" />
          <input type="number" name="speed_max" placeholder="Обороты до" onChange={handleChange} className="p-2 border rounded w-1/2" />
        </div>
        <div className="flex gap-2">
          <input type="number" name="price_min" placeholder="Цена от" onChange={handleChange} className="p-2 border rounded w-1/2" />
          <input type="number" name="price_max" placeholder="Цена до" onChange={handleChange} className="p-2 border rounded w-1/2" />
        </div>
      </div>
    </div>
  );
}