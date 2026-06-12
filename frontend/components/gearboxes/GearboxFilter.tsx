'use client';

import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { GearboxType } from '@/services/api';

interface GearboxFilterProps {
  onFilter: (filters: any) => void;
}

export default function GearboxFilter({ onFilter }: GearboxFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState({
    search: '',
    gearbox_type: '',
    series: '',
    input_power_min: '',
    input_power_max: '',
    output_torque_min: '',
    output_torque_max: '',
    ratio_min: '',
    ratio_max: '',
    manufacturer_id: '',
  });

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
      gearbox_type: '',
      series: '',
      input_power_min: '',
      input_power_max: '',
      output_torque_min: '',
      output_torque_max: '',
      ratio_min: '',
      ratio_max: '',
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
            <label className="block text-sm font-medium mb-1">Поиск по модели</label>
            <div className="relative">
              <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-2.5 text-gray-400" />
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleChange}
                placeholder="Номер редуктора..."
                className="pl-10 w-full p-2 border rounded"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Тип</label>
              <select name="gearbox_type" value={filters.gearbox_type} onChange={handleChange} className="w-full p-2 border rounded">
                <option value="">Все типы</option>
                <option value="WORM">Червячный</option>
                <option value="HELICAL">Цилиндрический</option>
                <option value="HELICAL_BEVEL">Коническо-цилиндрический</option>
                <option value="PARALLEL_SHAFT">Плоскоцилиндрический</option>
                <option value="VARIATOR">Вариатор</option>
                <option value="INDUSTRIAL">Индустриальный</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Серия</label>
              <input type="text" name="series" value={filters.series} onChange={handleChange} placeholder="NMRW, R, KA..." className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность от (кВт)</label>
              <input type="number" name="input_power_min" value={filters.input_power_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность до (кВт)</label>
              <input type="number" name="input_power_max" value={filters.input_power_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Момент от (Нм)</label>
              <input type="number" name="output_torque_min" value={filters.output_torque_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Момент до (Нм)</label>
              <input type="number" name="output_torque_max" value={filters.output_torque_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Передаточное число от</label>
              <input type="number" name="ratio_min" value={filters.ratio_min} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Передаточное число до</label>
              <input type="number" name="ratio_max" value={filters.ratio_max} onChange={handleChange} className="w-full p-2 border rounded" />
            </div>
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
