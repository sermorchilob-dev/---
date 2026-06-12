import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold">
            ⚙️ Конфигуратор
          </Link>
          <div className="flex space-x-4">
            <Link href="/products" className="hover:bg-blue-700 px-3 py-2 rounded">
              Двигатели
            </Link>
            <Link href="/bearings" className="hover:bg-blue-700 px-3 py-2 rounded">
              Подшипники
            </Link>
            <Link href="/bearing-units" className="hover:bg-blue-700 px-3 py-2 rounded">
              Узлы ASAHI
            </Link>
            <Link href="/gearboxes" className="hover:bg-blue-700 px-3 py-2 rounded">
              Редукторы
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}