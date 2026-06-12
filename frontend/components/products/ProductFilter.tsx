'use client';

import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { manufacturersApi, Manufacturer } from '@/services/api';

interface ProductFilterProps {
  onFilter: (filters: any) => void;
}

export default function ProductFilter({ onFilter }: ProductFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [manufacturers, setManufacturers] = useState<Manufacturer[]>([]);
  const [filters, setFilters] = useState({
    search: '',
    power_min: '',
    power_max: '',
    speed_min: '',
    speed_max: '',
    manufacturer_id: '',
  });

  useEffect(() => {
    loadManufacturers();
  }, []);

  const loadManufacturers = async () => {
    try {
      const data = await manufacturersApi.getAll();
      setManufacturers(data);
    } catch (error) {
      console.error('Ошибка загрузки производителей', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const activeFilters = Object.fromEntries(
      Object.entries(filters).filter(([_, v]) => v !== '')
    );
    onFilter(activeFilters);
  };

  const handleReset = () => {
    setFilters({
      search: '',
      power_min: '',
      power_max: '',
      speed_min: '',
      speed_max: '',
      manufacturer_id: '',
    });
    onFilter({});
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center text-lg font-semibold mb-2">
        <FunnelIcon className="w-5 h-5 mr-2" /> Фильтры
      </button>
      {isOpen && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Поиск по названию или артикулу</label>
            <div className="relative">
              <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-2.5 text-gray-400" />
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleChange}
                placeholder="Введите название или артикул..."
                className="pl-10 w-full p-2 border rounded"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Мощность от (кВт)</label>
              <input type="number" name="power_min" value={filters.power_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность до (кВт)</label>
              <input type="number" name="power_max" value={filters.power_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Обороты от (об/мин)</label>
              <input type="number" name="speed_min" value={filters.speed_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Обороты до (об/мин)</label>
              <input type="number" name="speed_max" value={filters.speed_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Производитель</label>
            <select name="manufacturer_id" value={filters.manufacturer_id} onChange={handleChange} className="w-full p-2 border rounded">
              <option value="">Все производители</option>
              {manufacturers.map(m => (
                <option key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
          </div>
          <div className="flex space-x-4">
            <button type="submit" className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Применить</button>
            <button type="button" onClick={handleReset} className="flex-1 bg-gray-200 py-2 rounded hover:bg-gray-300">Сбросить</button>
          </div>
        </form>
      )}
    </div>
  );
}
