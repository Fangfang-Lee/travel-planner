import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { tripApi } from '../api/trips';
import { TripCard } from '../components/TripCard';
import { Trip } from '../types/trip';

export function MyTrips() {
  const navigate = useNavigate();
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const data = await tripApi.listTrips();
        setTrips(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrips();
  }, []);

  if (loading) return <div className="p-8 text-center">加载中...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">我的旅行</h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {trips.map(trip => (
            <TripCard
              key={trip.id}
              trip={trip}
              onClick={() => navigate(`/trips/${trip.id}`)}
            />
          ))}
        </div>

        {trips.length === 0 && (
          <p className="text-center text-gray-500">暂无旅行计划</p>
        )}
      </main>
    </div>
  );
}
