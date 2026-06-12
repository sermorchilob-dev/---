'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { productsApi, Product } from '@/services/api';

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await productsApi.getAll({ limit: 3 });
      setProducts(data);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-4">
        ⚙️ Конфигуратор приводной техники
      </h1>
      <p className="text-xl text-center text-gray-600 mb-12">
        Профессиональный подбор электродвигателей, подшипников и редукторов
      </p>
      <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6 mb-12">
        <Link href="/products" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
          <div className="text-5xl mb-4">⚡</div>
          <h2 className="text-2xl font-semibold mb-2">Электродвигатели</h2>
          <p className="text-gray-600">Асинхронные, серво, взрывозащищенные</p>
        </Link>
        <Link href="/bearings" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
          <div className="text-5xl mb-4">🔧</div>
          <h2 className="text-2xl font-semibold mb-2">Подшипники</h2>
          <p className="text-gray-600">Шариковые, роликовые, игольчатые</p>
        </Link>
        <Link href="/bearing-units" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
          <div className="text-5xl mb-4">🏭</div>
          <h2 className="text-2xl font-semibold mb-2">Подшипниковые узлы</h2>
          <p className="text-gray-600">ASAHI, NKE, готовые решения</p>
        </Link>
        <Link href="/gearboxes" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
          <div className="text-5xl mb-4">⚙️</div>
          <h2 className="text-2xl font-semibold mb-2">Редукторы ESQ</h2>
          <p className="text-gray-600">Червячные, цилиндрические, конические</p>
        </Link>
        <Link href="/selection" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
          <div className="text-5xl mb-4">🎯</div>
          <h2 className="text-2xl font-semibold mb-2">Мастер подбора</h2>
          <p className="text-gray-600">Пошаговый подбор по параметрам</p>
        </Link>
      </div>
      {!loading && products.length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-semibold mb-4">Популярные товары</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {products.map(product => (
              <div key={product.id} className="bg-white rounded-lg shadow p-4">
                <div className="font-bold">{product.product_code}</div>
                <div className="text-sm text-gray-600 mt-1">{product.name}</div>
                <div className="mt-2 text-blue-600 font-semibold">
                  {product.price?.toLocaleString()} {product.currency}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
