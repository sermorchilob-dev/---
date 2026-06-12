'use client';

import { useEffect, useState } from 'react';
import { gearboxesApi, Gearbox } from '@/services/api';
import GearboxCard from '@/components/gearboxes/GearboxCard';
import GearboxFilter from '@/components/gearboxes/GearboxFilter';

export default function GearboxesPage() {
  const [gearboxes, setGearboxes] = useState<Gearbox[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    loadGearboxes();
  }, [filters]);

  const loadGearboxes = async () => {
    setLoading(true);
    try {
      const data = await gearboxesApi.getAll(filters);
      setGearboxes(data);
    } catch (error) {
      console.error('Ошибка загрузки редукторов:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Редукторы ESQ</h1>
      <GearboxFilter onFilter={setFilters} />
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <>
          <p className="mb-4 text-gray-600">Найдено: {gearboxes.length}</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {gearboxes.map(gearbox => (
              <GearboxCard key={gearbox.id} gearbox={gearbox} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
