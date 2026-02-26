export interface TripRequest {
  destination: string;
  duration: number;
  budget: number;
  travelers: number;
  preferences: string[];
}

export interface Trip {
  id: string;
  destination: string;
  duration: number;
  budget: number;
  travelers: number;
  preferences: string[];
  plan?: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}
