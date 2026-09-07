import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import { AuthProvider } from './AuthContext'
import HomePage from './HomePage'
import LoginPage from './LoginPage'
import RegisterPage from './RegisterPage'
import DashboardPage from './DashboardPage'
import ProtectedRoute from './ProtectedRoute'

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<DashboardPage />} />
            </Route>
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
