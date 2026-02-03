import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext'

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem 1rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
    paddingBottom: '1rem',
    borderBottom: '1px solid #eee',
  },
  title: {
    fontSize: '1.5rem',
    color: '#333',
    margin: 0,
  },
  logoutButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#e55',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    fontSize: '0.875rem',
    cursor: 'pointer',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    padding: '1.5rem',
    marginBottom: '1rem',
  },
  infoRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.5rem 0',
    borderBottom: '1px solid #f0f0f0',
    fontSize: '0.9375rem',
  },
  infoLabel: {
    color: '#888',
    fontWeight: 500,
  },
  infoValue: {
    color: '#333',
  },
  placeholder: {
    textAlign: 'center' as const,
    color: '#999',
    padding: '2rem',
  },
}

function DashboardPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Welcome, {user?.username}!</h1>
        <button style={styles.logoutButton} onClick={handleLogout}>
          Sign Out
        </button>
      </div>

      <div style={styles.card}>
        <h2 style={{ marginTop: 0, fontSize: '1.125rem', color: '#333' }}>
          Account Information
        </h2>
        <div style={styles.infoRow}>
          <span style={styles.infoLabel}>Username</span>
          <span style={styles.infoValue}>{user?.username}</span>
        </div>
        <div style={styles.infoRow}>
          <span style={styles.infoLabel}>Email</span>
          <span style={styles.infoValue}>{user?.email}</span>
        </div>
        <div style={styles.infoRow}>
          <span style={styles.infoLabel}>Status</span>
          <span style={styles.infoValue}>{user?.is_active ? 'Active' : 'Inactive'}</span>
        </div>
      </div>

      <div style={styles.card}>
        <p style={styles.placeholder}>
          Your trips will appear here once the trips feature is implemented.
        </p>
      </div>
    </div>
  )
}

export default DashboardPage
