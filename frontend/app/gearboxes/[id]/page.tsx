'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { gearboxesApi, GearboxWithManufacturer } from '@/services/api';

export default function GearboxDetailPage() {
  const { id } = useParams();
  const [gearbox, setGearbox] = useState<GearboxWithManufacturer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadGearbox();
    }
  }, [id]);

  const loadGearbox = async () => {
    try {
      const data = await gearboxesApi.getById(Number(id));
      setGearbox(data);
    } catch (err) {
      setError('Не удалось загрузить информацию о редукторе');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !gearbox) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error || 'Редуктор не найден'}</p>
        <Link href="/gearboxes" className="text-blue-600 hover:underline">
          Вернуться к списку
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="p-8">
        <Link href="/gearboxes" className="text-blue-600 hover:underline mb-4 inline-block">
          ← Назад к списку
        </Link>

        <div className="flex justify-between items-start mb-6">
          <div>
            <span className="text-sm text-gray-500">{gearbox.gearbox_number}</span>
            <h1 className="text-3xl font-bold mt-1">
              {gearbox.name || `${getTypeName(gearbox.gearbox_type)} редуктор`}
            </h1>
            <div className="mt-2 text-gray-600">
              <span className="mr-4">Серия: {gearbox.series || '—'}</span>
              <span>Производитель: {gearbox.manufacturer?.name || 'ESQ'}</span>
            </div>
          </div>
          <div className="text-right">
            <span className="text-3xl font-bold text-blue-600">
              {gearbox.price?.toLocaleString() ?? '—'} {gearbox.currency ?? 'RUB'}
            </span>
            <p className="text-gray-600 mt-1">Цена по запросу</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Левая колонка - основные характеристики */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Основные параметры</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Тип редуктора</td><td className="py-2 font-medium">{getTypeName(gearbox.gearbox_type)}</td></tr>
                <tr><td className="py-2 text-gray-600">Количество ступеней</td><td className="py-2 font-medium">{gearbox.stages}</td></tr>
                <tr><td className="py-2 text-gray-600">Передаточное число (i)</td><td className="py-2 font-medium">{gearbox.ratio}</td></tr>
                <tr><td className="py-2 text-gray-600">Мощность на входе</td><td className="py-2 font-medium">{gearbox.input_power_kw} кВт</td></tr>
                <tr><td className="py-2 text-gray-600">Крутящий момент на выходе</td><td className="py-2 font-medium">{gearbox.output_torque_nm} Нм</td></tr>
                <tr><td className="py-2 text-gray-600">Частота вращения вх.</td><td className="py-2 font-medium">{gearbox.input_speed_rpm} об/мин</td></tr>
                <tr><td className="py-2 text-gray-600">Частота вращения вых.</td><td className="py-2 font-medium">{gearbox.output_speed_rpm} об/мин</td></tr>
                <tr><td className="py-2 text-gray-600">Сервис-фактор (f.s.)</td><td className="py-2 font-medium">{gearbox.service_factor}</td></tr>
                <tr><td className="py-2 text-gray-600">КПД</td><td className="py-2 font-medium">{gearbox.efficiency}%</td></tr>
              </tbody>
            </table>
          </div>

          {/* Правая колонка - конструктивные особенности */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Конструкция и монтаж</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Монтажное положение</td><td className="py-2 font-medium">{gearbox.mounting_position}</td></tr>
                <tr><td className="py-2 text-gray-600">Диаметр выходного вала</td><td className="py-2 font-medium">{gearbox.output_shaft_diameter_mm} мм</td></tr>
                <tr><td className="py-2 text-gray-600">Длина выходного вала</td><td className="py-2 font-medium">{gearbox.output_shaft_length_mm} мм</td></tr>
                <tr><td className="py-2 text-gray-600">Тип выходного фланца</td><td className="py-2 font-medium">{gearbox.output_flange_type || '—'}</td></tr>
                <tr><td className="py-2 text-gray-600">Полый вал</td><td className="py-2 font-medium">{gearbox.hollow_shaft ? 'Да' : 'Нет'}</td></tr>
                <tr><td className="py-2 text-gray-600">Объём масла</td><td className="py-2 font-medium">{gearbox.oil_volume_l} л</td></tr>
                <tr><td className="py-2 text-gray-600">Радиальная нагрузка</td><td className="py-2 font-medium">{gearbox.radial_load_n} Н</td></tr>
                <tr><td className="py-2 text-gray-600">Вес</td><td className="py-2 font-medium">{gearbox.weight_kg} кг</td></tr>
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
      </div>
    </div>
  );
}
