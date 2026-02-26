import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { tripApi } from '../api/trips';
import { Trip } from '../types/trip';

export function TripDetail() {
  const { id } = useParams<{ id: string }>();
  const [trip, setTrip] = useState<Trip | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const fetchTrip = async () => {
      try {
        const data = await tripApi.getTrip(id);
        setTrip(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrip();
  }, [id]);

  if (loading) return <div className="p-8 text-center">加载中...</div>;
  if (!trip) return <div className="p-8 text-center">行程不存在</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <Link to="/" className="text-blue-500 hover:underline">
            ← 返回
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h1 className="text-2xl font-bold mb-4">{trip.destination}</h1>

          <div className="flex gap-4 mb-6">
            <span className="px-3 py-1 bg-gray-100 rounded">
              {trip.duration}天
            </span>
            <span className="px-3 py-1 bg-gray-100 rounded">
              {trip.travelers}人
            </span>
            <span className="px-3 py-1 bg-gray-100 rounded">
              ¥{trip.budget}
            </span>
          </div>

          {trip.plan && (
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap">{trip.plan}</pre>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
