'use client';

import { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface RequestItem {
  id: number;
  type?: string;
  name: string;
  quantity: number;
}

interface RequestFormProps {
  items: RequestItem[];
  onClose: () => void;
  onSuccess?: () => void;
}

export default function RequestForm({ items, onClose, onSuccess }: RequestFormProps) {
  const [formData, setFormData] = useState({
    contact_name: '',
    contact_email: '',
    contact_phone: '',
    company_name: '',
    project_name: '',
    project_description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPdfUrl(null);

    try {
      const payload = {
        contact_name: formData.contact_name,
        contact_email: formData.contact_email,
        contact_phone: formData.contact_phone,
        company_name: formData.company_name,
        project_name: formData.project_name,
        project_description: formData.project_description,
        items: items.map(item => ({
          product_id: item.id,
          product_name: item.name,
          quantity: item.quantity,
        })),
      };

      // Используем /api/v1/quote-requests – при наличии rewrites в next.config.js
      // запрос будет перенаправлен на бэкенд
      const response = await fetch('/api/v1/quote-requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Ошибка отправки заявки');
      }

      const data = await response.json();
      if (data.pdf_url) {
        setPdfUrl(data.pdf_url);
      }

      alert('Заявка успешно отправлена! Менеджер свяжется с вами в ближайшее время.');
      onSuccess?.();
      // Не закрываем форму сразу, чтобы пользователь успел скачать PDF
      // onClose(); – раскомментируй, если хочешь закрывать автоматически
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">Запрос коммерческого предложения</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Ваше имя *</label>
            <input
              type="text"
              name="contact_name"
              required
              value={formData.contact_name}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Email *</label>
            <input
              type="email"
              name="contact_email"
              required
              value={formData.contact_email}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Телефон</label>
            <input
              type="tel"
              name="contact_phone"
              value={formData.contact_phone}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Компания</label>
            <input
              type="text"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Название проекта (опционально)</label>
            <input
              type="text"
              name="project_name"
              value={formData.project_name}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Комментарий / требования</label>
            <textarea
              name="project_description"
              rows={3}
              value={formData.project_description}
              onChange={handleChange}
              className="w-full p-2 border rounded focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="bg-gray-50 rounded-lg p-3">
            <h3 className="font-semibold mb-2">Выбранные товары:</h3>
            <ul className="text-sm space-y-1">
              {items.map((item, idx) => (
                <li key={idx}>• {item.name} x {item.quantity}</li>
              ))}
            </ul>
          </div>

          {error && <div className="text-red-600 text-sm">{error}</div>}

          {pdfUrl && (
            <div className="mt-2 text-center">
              <a
                href={pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                📄 Скачать коммерческое предложение (PDF)
              </a>
            </div>
          )}

          <div className="flex space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border rounded hover:bg-gray-50"
            >
              Закрыть
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Отправка...' : 'Отправить заявку'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}