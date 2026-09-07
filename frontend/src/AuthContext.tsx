import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react'
import { authAPI } from './api'

interface User {
  id: number
  email: string
  username: string
  full_name: string | null
  is_active: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchCurrentUser = useCallback(async () => {
    try {
      const userData = await authAPI.getCurrentUser()
      setUser(userData)
    } catch {
      setUser(null)
      localStorage.removeItem('access_token')
    }
  }, [])

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchCurrentUser().finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [fetchCurrentUser])

  const login = useCallback(async (username: string, password: string) => {
    await authAPI.login({ username, password })
    await fetchCurrentUser()
  }, [fetchCurrentUser])

  const register = useCallback(async (email: string, username: string, password: string) => {
    await authAPI.register({ email, username, password })
    await authAPI.login({ username, password })
    await fetchCurrentUser()
  }, [fetchCurrentUser])

  const logout = useCallback(() => {
    authAPI.logout()
    setUser(null)
  }, [])

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: user !== null,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
