import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TripForm } from '../components/TripForm';
import { tripApi } from '../api/trips';
import { TripRequest, Trip } from '../types/trip';

export function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: TripRequest) => {
    setLoading(true);
    try {
      const trip: Trip = await tripApi.createPlan(data);
      navigate(`/trips/${trip.id}`);
    } catch (error) {
      console.error(error);
      alert('规划失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">智能旅行规划助手</h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-2">规划你的下一次旅行</h2>
          <p className="text-gray-600">AI 驱动，多 Agent 协作，为你打造专属行程</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-8">
          <TripForm onSubmit={handleSubmit} loading={loading} />
        </div>
      </main>
    </div>
  );
}
