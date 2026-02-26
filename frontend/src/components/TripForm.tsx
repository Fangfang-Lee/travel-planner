import { useState } from 'react';
import { TripRequest } from '../types/trip';

interface Props {
  onSubmit: (data: TripRequest) => void;
  loading?: boolean;
}

const preferenceOptions = ['美食', '购物', '文化', '自然', '冒险', '休闲'];

export function TripForm({ onSubmit, loading }: Props) {
  const [destination, setDestination] = useState('');
  const [duration, setDuration] = useState(5);
  const [budget, setBudget] = useState(10000);
  const [travelers, setTravelers] = useState(2);
  const [preferences, setPreferences] = useState<string[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ destination, duration, budget, travelers, preferences });
  };

  const togglePreference = (pref: string) => {
    setPreferences(prev =>
      prev.includes(pref)
        ? prev.filter(p => p !== pref)
        : [...prev, pref]
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-xl mx-auto">
      <div>
        <label className="block text-sm font-medium mb-2">目的地</label>
        <input
          type="text"
          value={destination}
          onChange={e => setDestination(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
          placeholder="例如：日本东京"
          required
        />
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">天数</label>
          <input
            type="number"
            value={duration}
            onChange={e => setDuration(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1}
            max={30}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">预算(元)</label>
          <input
            type="number"
            value={budget}
            onChange={e => setBudget(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1000}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">人数</label>
          <input
            type="number"
            value={travelers}
            onChange={e => setTravelers(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg"
            min={1}
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">偏好</label>
        <div className="flex flex-wrap gap-2">
          {preferenceOptions.map(pref => (
            <button
              key={pref}
              type="button"
              onClick={() => togglePreference(pref)}
              className={`px-4 py-2 rounded-full border ${
                preferences.includes(pref)
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-700'
              }`}
            >
              {pref}
            </button>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? '规划中...' : '开始规划'}
      </button>
    </form>
  );
}
