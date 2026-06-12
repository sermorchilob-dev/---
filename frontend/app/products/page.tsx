'use client';

import { useState, useEffect } from 'react';
import { productsApi, manufacturersApi, Product } from '@/services/api';
import ProductCard from '@/components/products/ProductCard';
import ProductFilters from '@/components/ProductFilters';

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [manufacturers, setManufacturers] = useState<{ id: number; name: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(0);
  const limit = 12;

  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await productsApi.getAll({ ...filters, limit, offset: page * limit });
      setProducts(data);
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadManufacturers = async () => {
    try {
      const data = await manufacturersApi.getAll();
      setManufacturers(data);
    } catch (error) {
      console.warn('Не удалось загрузить производителей, используем заглушку');
    }
  };

  useEffect(() => {
    loadManufacturers();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [filters, page]);

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
    setPage(0); // сбрасываем пагинацию при смене фильтров
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Каталог электродвигателей</h1>
      <ProductFilters onFilterChange={handleFilterChange} manufacturers={manufacturers} />
      {loading ? (
        <p>Загрузка...</p>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="flex justify-center gap-4 mt-8">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0}
              className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50"
            >
              Назад
            </button>
            <span className="px-4 py-2">Страница {page + 1}</span>
            <button
              onClick={() => setPage(p => p + 1)}
              className="px-4 py-2 bg-gray-300 rounded"
            >
              Вперёд
            </button>
          </div>
        </>
      )}
    </div>
  );
}