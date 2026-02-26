import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { TripDetail } from './pages/TripDetail';
import { MyTrips } from './pages/MyTrips';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/trips/:id" element={<TripDetail />} />
        <Route path="/my-trips" element={<MyTrips />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
