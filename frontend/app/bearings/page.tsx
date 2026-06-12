'use client';

import { useEffect, useState } from 'react';
import { bearingsApi, Bearing } from '@/services/api';
import BearingCard from '@/components/bearings/BearingCard';
import BearingFilter from '@/components/bearings/BearingFilter';

export default function BearingsPage() {
  const [bearings, setBearings] = useState<Bearing[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    loadBearings();
  }, [filters]);

  const loadBearings = async () => {
    setLoading(true);
    try {
      const data = await bearingsApi.getAll(filters);
      setBearings(data);
    } catch (error) {
      console.error('Ошибка загрузки подшипников:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Подшипники</h1>
      <BearingFilter onFilter={setFilters} />
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <>
          <p className="mb-4 text-gray-600">Найдено: {bearings.length}</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bearings.map(bearing => (
              <BearingCard key={bearing.id} bearing={bearing} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
