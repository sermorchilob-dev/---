'use client';

import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { bearingManufacturersApi, BearingManufacturer } from '@/services/api';

interface BearingFilterProps {
  onFilter: (filters: any) => void;
}

export default function BearingFilter({ onFilter }: BearingFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [manufacturers, setManufacturers] = useState<BearingManufacturer[]>([]);
  const [filters, setFilters] = useState({
    search: '',
    bore_diameter_min: '',
    bore_diameter_max: '',
    outer_diameter_min: '',
    outer_diameter_max: '',
    width_min: '',
    width_max: '',
    manufacturer_id: '',
    seal_type: '',
    clearance: '',
  });

  useEffect(() => {
    loadManufacturers();
  }, []);

  const loadManufacturers = async () => {
    //try {
    //  const data = await bearingManufacturersApi.getAll();
     // setManufacturers(data);
    //} catch (error) {
    //  console.error('Ошибка загрузки производителей', error);
    //}
  setManufacturers([]);
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
      bore_diameter_min: '',
      bore_diameter_max: '',
      outer_diameter_min: '',
      outer_diameter_max: '',
      width_min: '',
      width_max: '',
      manufacturer_id: '',
      seal_type: '',
      clearance: '',
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
            <label className="block text-sm font-medium mb-1">Поиск по номеру</label>
            <div className="relative">
              <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-2.5 text-gray-400" />
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleChange}
                placeholder="Номер подшипника..."
                className="pl-10 w-full p-2 border rounded"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Внутр. диаметр от (мм)</label>
              <input type="number" name="bore_diameter_min" value={filters.bore_diameter_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Внутр. диаметр до (мм)</label>
              <input type="number" name="bore_diameter_max" value={filters.bore_diameter_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Наруж. диаметр от (мм)</label>
              <input type="number" name="outer_diameter_min" value={filters.outer_diameter_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Наруж. диаметр до (мм)</label>
              <input type="number" name="outer_diameter_max" value={filters.outer_diameter_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ширина от (мм)</label>
              <input type="number" name="width_min" value={filters.width_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ширина до (мм)</label>
              <input type="number" name="width_max" value={filters.width_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Производитель</label>
            <select name="manufacturer_id" value={filters.manufacturer_id} onChange={handleChange} className="w-full p-2 border rounded">
              <option value="">Все производители</option>
              {manufacturers.map(m => (
                <option key={m.id} value={m.id}>{m.name} {m.country ? `(${m.country})` : ''}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Тип уплотнения</label>
            <select name="seal_type" value={filters.seal_type} onChange={handleChange} className="w-full p-2 border rounded">
              <option value="">Любой</option>
              <option value="OPEN">Открытый (OPEN)</option>
              <option value="2Z">Две защитные шайбы (2Z)</option>
              <option value="2RS">Два уплотнения (2RS)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Зазор</label>
            <select name="clearance" value={filters.clearance} onChange={handleChange} className="w-full p-2 border rounded">
              <option value="">Любой</option>
              <option value="CN">Нормальный (CN)</option>
              <option value="C3">Увеличенный (C3)</option>
              <option value="C4">Большой (C4)</option>
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
