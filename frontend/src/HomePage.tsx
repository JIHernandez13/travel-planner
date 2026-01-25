import { useState, useEffect } from 'react'

function HomePage() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...')

  useEffect(() => {
    // Check API connection
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    fetch(`${apiUrl}/`)
      .then(res => res.json())
      .then(data => {
        setApiStatus(`✅ Connected - ${data.message}`)
      })
      .catch(() => {
        setApiStatus('❌ API not reachable')
      })
  }, [])

  return (
    <div className="home-page">
      <header className="header">
        <h1>🌍 Travel Planner</h1>
        <p>Plan your perfect trip</p>
      </header>

      <main className="content">
        <div className="status-card">
          <h2>System Status</h2>
          <p>Backend API: {apiStatus}</p>
        </div>

        <div className="welcome-card">
          <h2>Welcome to Your Travel Planner</h2>
          <p>Start planning your next adventure!</p>
          
          <div className="features">
            <div className="feature">
              <h3>📅 Plan Trips</h3>
              <p>Organize your itineraries day by day</p>
            </div>
            <div className="feature">
              <h3>💰 Track Budget</h3>
              <p>Keep your spending in check</p>
            </div>
            <div className="feature">
              <h3>🗺️ Explore Places</h3>
              <p>Discover activities and attractions</p>
            </div>
          </div>

          <button className="cta-button">Get Started</button>
        </div>
      </main>
    </div>
  )
}

export default HomePage
