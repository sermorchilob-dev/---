'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Product } from '@/services/api';
import RequestForm from '@/components/RequestForm';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      <div className="p-5">
        <div className="flex justify-between items-start">
          <div>
            <span className="text-sm text-gray-500">{product.product_code}</span>
            <h3 className="text-lg font-semibold mt-1">{product.name}</h3>
          </div>
          {product.in_stock ? (
            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">В наличии</span>
          ) : (
            <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">Под заказ</span>
          )}
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
          <div><span className="text-gray-500">Мощность:</span> {product.power_kw} кВт</div>
          <div><span className="text-gray-500">Обороты:</span> {product.speed_rpm} об/мин</div>
          <div><span className="text-gray-500">Напряжение:</span> {product.voltage}</div>
          <div><span className="text-gray-500">Монтаж:</span> {product.mounting_type}</div>
        </div>
        <div className="mt-4 flex justify-between items-center">
          <span className="text-sm text-gray-600">{product.manufacturer_name}</span>
          <span className="text-xl font-bold text-blue-600">
            {product.price?.toLocaleString()} {product.currency}
          </span>
        </div>
        <div className="mt-4">
          <Link href={`/products/${product.id}`} className="block w-full text-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
            Подробнее
          </Link>
          <button
            onClick={() => setShowForm(true)}
            className="mt-2 w-full text-center bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Запросить КП
          </button>
        </div>
      </div>
      {showForm && (
        <RequestForm
          items={[{ id: product.id, type: 'product', name: product.name, quantity: 1 }]}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}