'use client';

import { useState } from 'react';
import Link from 'next/link';
import RequestForm from '@/components/RequestForm';

interface BearingUnit {
  id: number;
  unit_number: string;
  shaft_diameter_mm: number;
  housing_type: string;
  housing_material: string;
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
  manufacturer?: { name: string };
}

interface BearingUnitCardProps {
  unit: BearingUnit;
}

export default function BearingUnitCard({ unit }: BearingUnitCardProps) {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      <div className="p-5">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-sm text-gray-500">{unit.unit_number}</span>
            <h3 className="text-lg font-semibold mt-1">Подшипниковый узел</h3>
          </div>
          <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded">
            {unit.housing_type?.replace('_', ' ') || '—'}
          </span>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div><span className="text-gray-500">Вал:</span> {unit.shaft_diameter_mm} мм</div>
          <div><span className="text-gray-500">Масса:</span> {unit.weight_kg} кг</div>
          <div><span className="text-gray-500">Дин. нагрузка:</span> {unit.dynamic_load_kn} кН</div>
          <div><span className="text-gray-500">Стат. нагрузка:</span> {unit.static_load_kn} кН</div>
        </div>
        <div className="mt-4 flex justify-between items-center">
          <span className="text-sm text-gray-600">{unit.manufacturer?.name || 'ASAHI'}</span>
        </div>
        <div className="mt-4 flex space-x-2">
          <Link 
            href={`/bearing-units/${unit.id}`} 
            className="flex-1 text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Подробнее
          </Link>
          <button
            onClick={() => setShowForm(true)}
            className="flex-1 text-center bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Запросить КП
          </button>
        </div>
      </div>
      {showForm && (
        <RequestForm
          items={[{ id: unit.id, type: 'bearing_unit', name: unit.unit_number, quantity: 1 }]}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}