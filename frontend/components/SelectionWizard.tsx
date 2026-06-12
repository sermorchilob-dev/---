'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

interface Question {
  id: string;
  question: string;
  type: string;
  unit?: string;
  options?: string[];
}

interface Answer {
  [key: string]: any;
}

export default function SelectionWizard() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer>({});
  const [loading, setLoading] = useState(true);
  const [finished, setFinished] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  // Запуск сессии при монтировании
  useEffect(() => {
    startSelection();
  }, []);

  const startSelection = async () => {
    try {
      const response = await axios.post('/api/selection/start', null, {
        params: { device_type: 'electric_motor' }
      });
      setSessionId(response.data.session_id);
      setQuestions(response.data.questions);
      setCurrentIndex(0);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка запуска мастера:', error);
      setLoading(false);
    }
  };

  const submitAnswer = async (answerValue: any) => {
    if (!sessionId) return;
    const currentQuestion = questions[currentIndex];
    const newAnswers = { ...answers, [currentQuestion.id]: answerValue };
    setAnswers(newAnswers);

    try {
      const response = await axios.post('/api/selection/answer', {
        session_id: sessionId,
        answer_id: currentQuestion.id,
        value: answerValue
      });

      if (response.data.finished) {
        // Получаем результаты
        const resultRes = await axios.post('/api/selection/result', null, {
          params: { session_id: sessionId }
        });
        setResults(resultRes.data);
        setFinished(true);
      } else {
        // Переходим к следующему вопросу
        setCurrentIndex(currentIndex + 1);
      }
    } catch (error) {
      console.error('Ошибка отправки ответа:', error);
    }
  };

  const renderQuestion = () => {
    const q = questions[currentIndex];
    if (!q) return null;

    const handleNumberSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      const value = formData.get('value');
      if (value) submitAnswer(parseFloat(value as string));
    };

    if (q.type === 'number') {
      return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
          <h2 className="text-xl font-semibold mb-4">{q.question}</h2>
          <form onSubmit={handleNumberSubmit} className="space-y-4">
            <input
              type="number"
              name="value"
              step="any"
              className="w-full p-2 border rounded"
              placeholder={`Введите значение (${q.unit})`}
              required
            />
            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
              Далее
            </button>
          </form>
        </div>
      );
    }

    if (q.type === 'select' && q.options) {
      return (
        <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
          <h2 className="text-xl font-semibold mb-4">{q.question}</h2>
          <div className="space-y-2">
            {q.options.map(opt => (
              <button
                key={opt}
                onClick={() => submitAnswer(opt)}
                className="w-full text-left p-2 border rounded hover:bg-gray-100"
              >
                {opt}
              </button>
            ))}
          </div>
        </div>
      );
    }

    return null;
  };

  if (loading) {
    return <div className="text-center py-8">Загрузка мастера подбора...</div>;
  }

  if (finished) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold mb-4">Результаты подбора</h2>
        {results.length === 0 ? (
          <p>К сожалению, ничего не найдено. Попробуйте изменить параметры.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((product: any) => (
              <div key={product.id} className="bg-white rounded-lg shadow-md p-4">
                <h3 className="font-semibold">{product.name}</h3>
                <p>Код: {product.product_code}</p>
                <p>Мощность: {product.power_kw} кВт</p>
                <p>Обороты: {product.speed_rpm} об/мин</p>
                <p>Производитель: {product.manufacturer_name}</p>
                <p className="text-xl font-bold text-blue-600">{product.price?.toLocaleString()} ₽</p>
                <button className="mt-2 w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
                  Запросить КП
                </button>
              </div>
            ))}
          </div>
        )}
        <div className="mt-6 text-center">
          <button
            onClick={() => window.location.reload()}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Начать заново
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="py-8">
      <div className="max-w-md mx-auto">
        <div className="mb-4 bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-blue-600 h-2.5 rounded-full"
            style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
        <p className="text-center text-sm text-gray-600 mb-4">
          Вопрос {currentIndex + 1} из {questions.length}
        </p>
        {renderQuestion()}
      </div>
    </div>
  );
}