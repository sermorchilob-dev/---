'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Gearbox } from '@/services/api';
import RequestForm from '@/components/RequestForm';

interface GearboxCardProps {
  gearbox: Gearbox;
}

export default function GearboxCard({ gearbox }: GearboxCardProps) {
  const [showForm, setShowForm] = useState(false);

  const getTypeName = (type: string) => {
    const types: Record<string, string> = {
      'WORM': 'Червячный',
      'HELICAL': 'Цилиндрический',
      'HELICAL_BEVEL': 'Коническо-цилиндрический',
      'PARALLEL_SHAFT': 'Плоскоцилиндрический',
      'VARIATOR': 'Вариатор',
      'INDUSTRIAL': 'Индустриальный'
    };
    return types[type] || type;
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      <div className="p-5">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-sm text-gray-500">{gearbox.gearbox_number}</span>
            <h3 className="text-lg font-semibold mt-1">
              {gearbox.name || `${getTypeName(gearbox.gearbox_type)} редуктор`}
            </h3>
          </div>
          <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded">
            {gearbox.series || '—'}
          </span>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div><span className="text-gray-500">Тип:</span> {getTypeName(gearbox.gearbox_type)}</div>
          <div><span className="text-gray-500">i:</span> {gearbox.ratio}</div>
          <div><span className="text-gray-500">Мощность:</span> {gearbox.input_power_kw} кВт</div>
          <div><span className="text-gray-500">Момент:</span> {gearbox.output_torque_nm} Нм</div>
          <div><span className="text-gray-500">n вх:</span> {gearbox.input_speed_rpm} об/мин</div>
          <div><span className="text-gray-500">n вых:</span> {gearbox.output_speed_rpm} об/мин</div>
        </div>
        <div className="mt-4 flex justify-between items-center">
          <span className="text-sm text-gray-600">{gearbox.manufacturer?.name || 'ESQ'}</span>
          <span className="text-xl font-bold text-blue-600">
            {gearbox.price?.toLocaleString() ?? '—'} {gearbox.currency ?? 'RUB'}
          </span>
        </div>
        <div className="mt-4 flex space-x-2">
          <Link 
            href={`/gearboxes/${gearbox.id}`} 
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
          items={[{ id: gearbox.id, type: 'gearbox', name: gearbox.gearbox_number, quantity: 1 }]}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}