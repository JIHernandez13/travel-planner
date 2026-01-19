import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import HomePage from './pages/HomePage'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* TODO: Add more routes */}
          {/* <Route path="/login" element={<LoginPage />} /> */}
          {/* <Route path="/trips" element={<TripsPage />} /> */}
          {/* <Route path="/trips/:id" element={<TripDetailPage />} /> */}
        </Routes>
      </div>
    </Router>
  )
}

export default App
