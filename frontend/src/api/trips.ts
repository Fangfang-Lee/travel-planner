import axios from 'axios';
import { Trip, TripRequest } from '../types/trip';

const api = axios.create({
  baseURL: '/api',
});

export const tripApi = {
  createPlan: (data: TripRequest): Promise<Trip> =>
    api.post('/trips/plan', data).then(res => res.data),

  getTrip: (id: string): Promise<Trip> =>
    api.get(`/trips/${id}`).then(res => res.data),

  listTrips: (): Promise<Trip[]> =>
    api.get('/trips').then(res => res.data),
};
