import SelectionWizard from '@/components/SelectionWizard';

export default function SelectionPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-6">Мастер подбора электродвигателей</h1>
      <p className="text-center text-gray-600 mb-8">
        Ответьте на несколько вопросов — мы подберём подходящее оборудование.
      </p>
      <SelectionWizard />
    </div>
  );
}