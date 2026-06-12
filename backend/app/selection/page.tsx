'use client';

import { useState } from 'react';
import { productsApi, bearingsApi, gearboxesApi } from '@/services/api';
import { Product, Bearing, Gearbox } from '@/services/api';

type EquipmentType = 'motor' | 'bearing' | 'gearbox';

export default function SelectionPage() {
  const [step, setStep] = useState(1);
  const [equipmentType, setEquipmentType] = useState<EquipmentType>('motor');
  const [params, setParams] = useState({
    power_min: '',
    power_max: '',
    speed_min: '',
    speed_max: '',
    bore_min: '',
    bore_max: '',
    outer_min: '',
    outer_max: '',
    width_min: '',
    width_max: '',
    ratio_min: '',
    ratio_max: '',
    manufacturer_id: '',
  });
  const [results, setResults] = useState<{ products: Product[]; bearings: Bearing[]; gearboxes: Gearbox[] }>({
    products: [],
    bearings: [],
    gearboxes: [],
  });
  const [loading, setLoading] = useState(false);

  const handleTypeSelect = (type: EquipmentType) => {
    setEquipmentType(type);
    setStep(2);
  };

  const handleParamChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setParams(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const requestBody: any = { equipment_type: equipmentType };

      if (equipmentType === 'motor') {
        if (params.power_min) requestBody.power_kw_min = parseFloat(params.power_min);
        if (params.power_max) requestBody.power_kw_max = parseFloat(params.power_max);
        if (params.speed_min) requestBody.speed_rpm_min = parseInt(params.speed_min);
        if (params.speed_max) requestBody.speed_rpm_max = parseInt(params.speed_max);
        if (params.manufacturer_id) requestBody.manufacturer_id = parseInt(params.manufacturer_id);
      } else if (equipmentType === 'bearing') {
        if (params.bore_min) requestBody.bore_diameter_min = parseFloat(params.bore_min);
        if (params.bore_max) requestBody.bore_diameter_max = parseFloat(params.bore_max);
        if (params.outer_min) requestBody.outer_diameter_min = parseFloat(params.outer_min);
        if (params.outer_max) requestBody.outer_diameter_max = parseFloat(params.outer_max);
        if (params.width_min) requestBody.width_min = parseFloat(params.width_min);
        if (params.width_max) requestBody.width_max = parseFloat(params.width_max);
        if (params.manufacturer_id) requestBody.manufacturer_id = parseInt(params.manufacturer_id);
      } else if (equipmentType === 'gearbox') {
        if (params.power_min) requestBody.power_kw_min = parseFloat(params.power_min);
        if (params.power_max) requestBody.power_kw_max = parseFloat(params.power_max);
        if (params.ratio_min) requestBody.ratio_min = parseFloat(params.ratio_min);
        if (params.ratio_max) requestBody.ratio_max = parseFloat(params.ratio_max);
        if (params.speed_min) requestBody.speed_rpm_min = parseInt(params.speed_min);
        if (params.speed_max) requestBody.speed_rpm_max = parseInt(params.speed_max);
        if (params.manufacturer_id) requestBody.manufacturer_id = parseInt(params.manufacturer_id);
      }

      const response = await fetch('/api/proxy/selection/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });
      const data = await response.json();
      setResults(data);
      setStep(3);
    } catch (error) {
      console.error('Ошибка при подборе:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Выберите тип оборудования</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => handleTypeSelect('motor')}
          className="p-6 border rounded-lg hover:bg-blue-50 hover:border-blue-500 transition"
        >
          <div className="text-4xl mb-2">⚡</div>
          <div className="font-semibold">Электродвигатели</div>
          <div className="text-sm text-gray-600">Асинхронные, серво, взрывозащищенные</div>
        </button>
        <button
          onClick={() => handleTypeSelect('bearing')}
          className="p-6 border rounded-lg hover:bg-blue-50 hover:border-blue-500 transition"
        >
          <div className="text-4xl mb-2">🔧</div>
          <div className="font-semibold">Подшипники</div>
          <div className="text-sm text-gray-600">Шариковые, роликовые, игольчатые</div>
        </button>
        <button
          onClick={() => handleTypeSelect('gearbox')}
          className="p-6 border rounded-lg hover:bg-blue-50 hover:border-blue-500 transition"
        >
          <div className="text-4xl mb-2">⚙️</div>
          <div className="font-semibold">Редукторы</div>
          <div className="text-sm text-gray-600">Червячные, цилиндрические, конические</div>
        </button>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">
        {equipmentType === 'motor' && 'Параметры электродвигателя'}
        {equipmentType === 'bearing' && 'Параметры подшипника'}
        {equipmentType === 'gearbox' && 'Параметры редуктора'}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {equipmentType === 'motor' && (
          <>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность от (кВт)</label>
              <input type="number" name="power_min" value={params.power_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность до (кВт)</label>
              <input type="number" name="power_max" value={params.power_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Обороты от (об/мин)</label>
              <input type="number" name="speed_min" value={params.speed_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Обороты до (об/мин)</label>
              <input type="number" name="speed_max" value={params.speed_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Производитель (ID)</label>
              <input type="number" name="manufacturer_id" value={params.manufacturer_id} onChange={handleParamChange} className="w-full p-2 border rounded" placeholder="1 - Siemens, 2 - ABB, 3 - SEW..." />
            </div>
          </>
        )}
        {equipmentType === 'bearing' && (
          <>
            <div>
              <label className="block text-sm font-medium mb-1">Внутренний диаметр от (мм)</label>
              <input type="number" name="bore_min" value={params.bore_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Внутренний диаметр до (мм)</label>
              <input type="number" name="bore_max" value={params.bore_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Наружный диаметр от (мм)</label>
              <input type="number" name="outer_min" value={params.outer_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Наружный диаметр до (мм)</label>
              <input type="number" name="outer_max" value={params.outer_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ширина от (мм)</label>
              <input type="number" name="width_min" value={params.width_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ширина до (мм)</label>
              <input type="number" name="width_max" value={params.width_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Производитель (ID)</label>
              <input type="number" name="manufacturer_id" value={params.manufacturer_id} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
          </>
        )}
        {equipmentType === 'gearbox' && (
          <>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность от (кВт)</label>
              <input type="number" name="power_min" value={params.power_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Мощность до (кВт)</label>
              <input type="number" name="power_max" value={params.power_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Передаточное число от</label>
              <input type="number" name="ratio_min" value={params.ratio_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Передаточное число до</label>
              <input type="number" name="ratio_max" value={params.ratio_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Выходные обороты от (об/мин)</label>
              <input type="number" name="speed_min" value={params.speed_min} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Выходные обороты до (об/мин)</label>
              <input type="number" name="speed_max" value={params.speed_max} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Производитель (ID)</label>
              <input type="number" name="manufacturer_id" value={params.manufacturer_id} onChange={handleParamChange} className="w-full p-2 border rounded" />
            </div>
          </>
        )}
      </div>
      <div className="mt-6 flex justify-between">
        <button onClick={() => setStep(1)} className="px-4 py-2 border rounded hover:bg-gray-100">Назад</button>
        <button onClick={handleSubmit} className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Подобрать</button>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Результаты подбора</h2>
      {loading && <div className="text-center">Загрузка...</div>}
      {!loading && (
        <>
          {results.products.length > 0 && (
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Электродвигатели ({results.products.length})</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {results.products.map(p => (
                  <div key={p.id} className="border p-3 rounded">
                    <div className="font-bold">{p.product_code}</div>
                    <div className="text-sm text-gray-600">{p.name}</div>
                    <div className="text-blue-600 font-semibold">{p.power_kw} кВт, {p.speed_rpm} об/мин</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {results.bearings.length > 0 && (
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Подшипники ({results.bearings.length})</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {results.bearings.map(b => (
                  <div key={b.id} className="border p-3 rounded">
                    <div className="font-bold">{b.bearing_number}</div>
                    <div className="text-sm text-gray-600">d={b.bore_diameter_mm} D={b.outer_diameter_mm} B={b.width_mm}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {results.gearboxes.length > 0 && (
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Редукторы ({results.gearboxes.length})</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {results.gearboxes.map(g => (
                  <div key={g.id} className="border p-3 rounded">
                    <div className="font-bold">{g.gearbox_number}</div>
                    <div className="text-sm text-gray-600">{g.name}</div>
                    <div className="text-blue-600">i={g.ratio}, M={g.output_torque_nm} Нм</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {results.products.length === 0 && results.bearings.length === 0 && results.gearboxes.length === 0 && (
            <p className="text-center text-gray-500">Ничего не найдено. Попробуйте изменить параметры.</p>
          )}
          <div className="mt-6 flex justify-between">
            <button onClick={() => setStep(2)} className="px-4 py-2 border rounded hover:bg-gray-100">Назад</button>
            <button onClick={() => { setStep(1); setResults({ products: [], bearings: [], gearboxes: [] }); }} className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Новый подбор</button>
          </div>
        </>
      )}
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">🎯 Мастер подбора оборудования</h1>
      {step === 1 && renderStep1()}
      {step === 2 && renderStep2()}
      {step === 3 && renderStep3()}
    </div>
  );
}
