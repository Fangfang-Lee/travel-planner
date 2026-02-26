import { Trip } from '../types/trip';

interface Props {
  trip: Trip;
  onClick?: () => void;
}

export function TripCard({ trip, onClick }: Props) {
  const statusColors = {
    pending: 'bg-gray-100',
    processing: 'bg-yellow-100',
    completed: 'bg-green-100',
    failed: 'bg-red-100',
  };

  return (
    <div
      onClick={onClick}
      className="p-4 border rounded-lg hover:shadow-md cursor-pointer transition"
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold">{trip.destination}</h3>
          <p className="text-gray-600">
            {trip.duration}天 · {trip.travelers}人 · ¥{trip.budget}
          </p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm ${statusColors[trip.status]}`}>
          {trip.status === 'processing' ? '规划中' : trip.status}
        </span>
      </div>
      <div className="mt-2 flex gap-2">
        {trip.preferences.map(p => (
          <span key={p} className="text-xs bg-gray-100 px-2 py-1 rounded">
            {p}
          </span>
        ))}
      </div>
    </div>
  );
}
