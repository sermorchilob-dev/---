'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { productsApi, Product } from '@/services/api';

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadProduct();
    }
  }, [id]);

  const loadProduct = async () => {
    try {
      const data = await productsApi.getById(Number(id));
      setProduct(data);
    } catch (err) {
      setError('Не удалось загрузить информацию о продукте');
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

  if (error || !product) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error || 'Продукт не найден'}</p>
        <Link href="/products" className="text-blue-600 hover:underline">
          Вернуться к списку
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="p-8">
        <Link href="/products" className="text-blue-600 hover:underline mb-4 inline-block">
          ← Назад к списку
        </Link>

        <div className="flex justify-between items-start mb-6">
          <div>
            <span className="text-sm text-gray-500">{product.product_code}</span>
            <h1 className="text-3xl font-bold mt-1">{product.name}</h1>
          </div>
          <div className="text-right">
            <span className="text-3xl font-bold text-blue-600">
              {product.price?.toLocaleString()} {product.currency}
            </span>
            <p className="text-gray-600 mt-1">
              {product.in_stock ? '✅ В наличии' : '⏳ Под заказ'}
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Левая колонка - изображение и производитель */}
          <div>
            <div className="bg-gray-100 rounded-lg h-64 flex items-center justify-center mb-6">
              <span className="text-8xl">⚙️</span>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-2">Производитель</h2>
              <p className="text-gray-800">{product.manufacturer_name || 'Не указан'}</p>
            </div>
          </div>

          {/* Правая колонка - характеристики */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Технические характеристики</h2>
            <table className="w-full">
              <tbody className="divide-y">
                <tr><td className="py-2 text-gray-600">Мощность</td><td className="py-2 font-medium">{product.power_kw} кВт</td></tr>
                <tr><td className="py-2 text-gray-600">Частота вращения</td><td className="py-2 font-medium">{product.speed_rpm} об/мин</td></tr>
                <tr><td className="py-2 text-gray-600">Напряжение</td><td className="py-2 font-medium">{product.voltage}</td></tr>
                <tr><td className="py-2 text-gray-600">Тип монтажа</td><td className="py-2 font-medium">{product.mounting_type}</td></tr>
                <tr><td className="py-2 text-gray-600">Степень защиты</td><td className="py-2 font-medium">{product.ip_rating}</td></tr>
              </tbody>
            </table>

            <div className="mt-8">
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition">
                Запросить коммерческое предложение
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
