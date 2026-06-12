'use client';

import { useEffect, useState } from 'react';
import { bearingUnitsApi, BearingUnit } from '@/services/api';
import BearingUnitCard from '@/components/bearing-units/BearingUnitCard';

export default function BearingUnitsPage() {
  const [units, setUnits] = useState<BearingUnit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUnits();
  }, []);

  const loadUnits = async () => {
    try {
      const data = await bearingUnitsApi.getAll();
      setUnits(data);
    } catch (error) {
      console.error('Ошибка загрузки подшипниковых узлов:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Подшипниковые узлы ASAHI</h1>
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <>
          <p className="mb-4 text-gray-600">Найдено: {units.length}</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {units.map(unit => (
              <BearingUnitCard key={unit.id} unit={unit} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
