'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Bearing } from '@/services/api';
import RequestForm from '@/components/RequestForm';

interface BearingCardProps {
  bearing: Bearing;
}

export default function BearingCard({ bearing }: BearingCardProps) {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      <div className="p-5">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-sm text-gray-500">{bearing.bearing_number}</span>
            <h3 className="text-lg font-semibold mt-1">
              {bearing.type_name || bearing.bearing_type?.name || 'Подшипник'}
            </h3>
          </div>
          <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded">
            {bearing.series_code || bearing.series?.series_code || '—'}
          </span>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div><span className="text-gray-500">d:</span> {bearing.bore_diameter_mm} мм</div>
          <div><span className="text-gray-500">D:</span> {bearing.outer_diameter_mm} мм</div>
          <div><span className="text-gray-500">B:</span> {bearing.width_mm} мм</div>
          <div><span className="text-gray-500">Уплотнение:</span> {bearing.seal_type || 'OPEN'}</div>
          <div><span className="text-gray-500">Зазор:</span> {bearing.clearance || 'CN'}</div>
          <div><span className="text-gray-500">Дин. C:</span> {bearing.dynamic_load_rating_kn} кН</div>
        </div>

        <div className="mt-4 flex justify-between items-center">
          <span className="text-sm text-gray-600">
            {bearing.manufacturer_name || bearing.manufacturer?.name || 'Неизвестный производитель'}
          </span>
          <span className="text-xl font-bold text-blue-600">
            {bearing.price?.toLocaleString() ?? '—'} {bearing.currency ?? 'RUB'}
          </span>
        </div>

        <div className="mt-4 flex space-x-2">
          <Link 
            href={`/bearings/${bearing.id}`} 
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
          items={[{ id: bearing.id, type: 'bearing', name: bearing.bearing_number, quantity: 1 }]}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}