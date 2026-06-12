'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { bearingsApi, Bearing } from '@/services/api';

export default function BearingDetailPage() {
  const { id } = useParams();
  const [bearing, setBearing] = useState<Bearing | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadBearing();
    }
  }, [id]);

  const loadBearing = async () => {
    try {
      const data = await bearingsApi.getById(Number(id));
      setBearing(data);
    } catch (err) {
      setError('Не удалось загрузить информацию о подшипнике');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !bearing) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error || 'Подшипник не найден'}</p>
        <Link href="/bearings" className="text-blue-600 hover:underline">
          Вернуться к списку
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="p-8">
        <Link href="/bearings" className="text-blue-600 hover:underline mb-4 inline-block">
          ← Назад к списку
        </Link>

        <div className="flex justify-between items-start mb-6">
          <div>
            <span className="text-sm text-gray-500">{bearing.bearing_number}</span>
            <h1 className="text-3xl font-bold mt-1">
              {bearing.type_name || bearing.bearing_type?.name || 'Подшипник'}
            </h1>
            <div className="mt-2 text-gray-600">
              <span className="mr-4">Серия: {bearing.series_code || bearing.series?.series_code || '—'}</span>
              <span>Производитель: {bearing.manufacturer_name || bearing.manufacturer?.name || '—'}</span>
            </div>
          </div>
          <div className="text-right">
            <span className="text-3xl font-bold text-blue-600">
              {bearing.price?.toLocaleString() ?? '—'} {bearing.currency ?? 'RUB'}
            </span>
            <p className="text-gray-600 mt-1">
              {bearing.price ? 'Цена по запросу' : 'Цена по запросу'}
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Левая колонка - основные характеристики */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Основные размеры</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Внутренний диаметр (d)</td><td className="py-2 font-medium">{bearing.bore_diameter_mm} мм</td></tr>
                <tr><td className="py-2 text-gray-600">Наружный диаметр (D)</td><td className="py-2 font-medium">{bearing.outer_diameter_mm} мм</td></tr>
                <tr><td className="py-2 text-gray-600">Ширина (B)</td><td className="py-2 font-medium">{bearing.width_mm} мм</td></tr>
                {bearing.width_inner_mm && <tr><td className="py-2 text-gray-600">Ширина внутренняя (B)</td><td className="py-2 font-medium">{bearing.width_inner_mm} мм</td></tr>}
                {bearing.width_outer_mm && <tr><td className="py-2 text-gray-600">Ширина наружная (C)</td><td className="py-2 font-medium">{bearing.width_outer_mm} мм</td></tr>}
              </tbody>
            </table>

            <h2 className="text-xl font-semibold mt-6 mb-4">Нагрузки и скорости</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Динамическая грузоподъёмность (C)</td><td className="py-2 font-medium">{bearing.dynamic_load_rating_kn} кН</td></tr>
                <tr><td className="py-2 text-gray-600">Статическая грузоподъёмность (C0)</td><td className="py-2 font-medium">{bearing.static_load_rating_kn} кН</td></tr>
                <tr><td className="py-2 text-gray-600">Предел усталости (Pu)</td><td className="py-2 font-medium">{bearing.fatigue_load_limit_kn ?? '—'} кН</td></tr>
                <tr><td className="py-2 text-gray-600">Справочная скорость</td><td className="py-2 font-medium">{bearing.reference_speed_rpm ?? '—'} об/мин</td></tr>
                <tr><td className="py-2 text-gray-600">Предельная скорость</td><td className="py-2 font-medium">{bearing.limiting_speed_rpm ?? '—'} об/мин</td></tr>
              </tbody>
            </table>
          </div>

          {/* Правая колонка - конструктивные особенности */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Конструкция</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Тип уплотнения</td><td className="py-2 font-medium">{bearing.seal_type || 'OPEN'}</td></tr>
                <tr><td className="py-2 text-gray-600">Тип сепаратора</td><td className="py-2 font-medium">{bearing.cage_type || '—'}</td></tr>
                <tr><td className="py-2 text-gray-600">Зазор</td><td className="py-2 font-medium">{bearing.clearance || 'CN'}</td></tr>
                <tr><td className="py-2 text-gray-600">Класс точности</td><td className="py-2 font-medium">{bearing.tolerance_class || '—'}</td></tr>
                <tr><td className="py-2 text-gray-600">Материал</td><td className="py-2 font-medium">{bearing.material_type || '—'}</td></tr>
                <tr><td className="py-2 text-gray-600">Смазка</td><td className="py-2 font-medium">{bearing.lubrication_type || '—'}</td></tr>
              </tbody>
            </table>

            <h2 className="text-xl font-semibold mt-6 mb-4">Прочее</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Вес</td><td className="py-2 font-medium">{bearing.weight_kg} кг</td></tr>
                <tr><td className="py-2 text-gray-600">Применение</td><td className="py-2 font-medium">{bearing.application || '—'}</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-8 flex space-x-4">
          <button className="flex-1 bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition">
            Запросить коммерческое предложение
          </button>
          <button className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-lg text-lg font-semibold hover:bg-gray-300 transition">
            Добавить в сравнение
          </button>
        </div>

        {/* Блок совместимых двигателей (заглушка) */}
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-2">Совместимые электродвигатели</h3>
          <p className="text-gray-600">Информация о совместимости будет добавлена позже.</p>
        </div>

        {/* Блок документации (заглушка) */}
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-2">Документация</h3>
          <p className="text-gray-600">Чертежи и сертификаты будут доступны позже.</p>
        </div>
      </div>
    </div>
  );
}
